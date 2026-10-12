"""Authentication for Telegram Mini App and trusted bot-server requests."""

import hashlib
import hmac
import json
import os
import time
from urllib.parse import parse_qsl

from fastapi import HTTPException, Request, status


def _telegram_user_id(init_data: str) -> int:
    bot_token = os.getenv("TELEGRAM_TOKEN")
    if not bot_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Telegram authentication is not configured",
        )

    try:
        pairs = parse_qsl(init_data, keep_blank_values=True, strict_parsing=True)
        data = dict(pairs)
        if len(data) != len(pairs):
            raise ValueError("duplicate init data fields")
        received_hash = data.pop("hash")
        auth_date = int(data["auth_date"])
        user = json.loads(data["user"])
        user_id = int(user["id"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram Mini App data",
        ) from None

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(data.items()))
    secret_key = hmac.new(
        b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
    ).digest()
    expected_hash = hmac.new(
        secret_key, data_check_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram Mini App signature",
        )

    now = int(time.time())
    if auth_date > now + 60 or now - auth_date > 24 * 60 * 60:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telegram Mini App session has expired",
        )
    return user_id


def require_owner_id(request: Request) -> int:
    """Authenticate the caller and return the owner ID from trusted credentials."""
    configured_api_key = os.getenv("API_SECRET_KEY", "")
    api_key = request.headers.get("x-api-key", "")
    if configured_api_key and hmac.compare_digest(api_key, configured_api_key):
        try:
            return int(request.headers["x-owner-id"])
        except (KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid internal owner ID",
            ) from None

    authorization = request.headers.get("authorization", "")
    scheme, _, init_data = authorization.partition(" ")
    if scheme.lower() == "tma" and init_data:
        return _telegram_user_id(init_data)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
    )
