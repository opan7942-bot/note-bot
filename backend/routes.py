from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.auth import require_owner_id
from backend.bot_database import (
    add_note_data,
    add_secret_data,
    add_todo_data,
    complete_todo_data,
    delete_note_data,
    delete_secret_data,
    delete_todo_data,
    get_notes_data,
    get_secret_data,
    get_todos_data,
    set_todo_status_data,
    update_note_data,
    update_secret_data,
    update_todo_data,
)


router = APIRouter()


class NotePayload(BaseModel):
    text: str = Field(min_length=1)


class TodoPayload(BaseModel):
    task: str = Field(min_length=1)


class TodoStatusPayload(BaseModel):
    status: bool


class SecretPayload(BaseModel):
    title: str = Field(min_length=1)
    secret: str = Field(min_length=1)


def _require_updated(found: bool, item_name: str) -> None:
    if not found:
        raise HTTPException(status_code=404, detail=f"{item_name} not found")


# Notes
@router.get("/get_notes")
def get_notes(owner_id: int = Depends(require_owner_id)):
    return get_notes_data(owner_id)


@router.post("/add_notes")
def add_notes(payload: NotePayload, owner_id: int = Depends(require_owner_id)):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Note text cannot be empty")
    add_note_data(owner_id, text)
    return {"message": "Note added successfully"}


@router.put("/update_notes")
def update_notes(
    note_id: int,
    payload: NotePayload,
    owner_id: int = Depends(require_owner_id),
):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Note text cannot be empty")
    _require_updated(update_note_data(owner_id, note_id, text), "Note")
    return {"message": "Note updated successfully"}


@router.delete("/delete_notes")
def delete_notes(note_id: int, owner_id: int = Depends(require_owner_id)):
    _require_updated(delete_note_data(owner_id, note_id), "Note")
    return {"message": "Note deleted successfully"}


# Todos
@router.get("/get_todos")
def get_todos(owner_id: int = Depends(require_owner_id)):
    return get_todos_data(owner_id)


@router.post("/add_todos")
def add_todos(payload: TodoPayload, owner_id: int = Depends(require_owner_id)):
    task = payload.task.strip()
    if not task:
        raise HTTPException(status_code=422, detail="Todo task cannot be empty")
    add_todo_data(owner_id, task)
    return {"message": "Todo added successfully"}


@router.put("/update_todos")
def update_todos(
    todo_id: int,
    payload: TodoPayload,
    owner_id: int = Depends(require_owner_id),
):
    task = payload.task.strip()
    if not task:
        raise HTTPException(status_code=422, detail="Todo task cannot be empty")
    _require_updated(update_todo_data(owner_id, todo_id, task), "Todo")
    return {"message": "Todo updated successfully"}


@router.put("/set_todo_status")
def set_todo_status(
    todo_id: int,
    payload: TodoStatusPayload,
    owner_id: int = Depends(require_owner_id),
):
    _require_updated(
        set_todo_status_data(owner_id, todo_id, payload.status), "Todo"
    )
    return {"message": "Todo status updated successfully"}


@router.post("/complete_todo")
def complete_todo(todo_id: int, owner_id: int = Depends(require_owner_id)):
    _require_updated(complete_todo_data(owner_id, todo_id), "Todo")
    return {"message": "Todo marked as completed"}


@router.delete("/delete_todos")
def delete_todos(todo_id: int, owner_id: int = Depends(require_owner_id)):
    _require_updated(delete_todo_data(owner_id, todo_id), "Todo")
    return {"message": "Todo deleted successfully"}


# Secrets
@router.get("/get_secrets")
def get_secrets(owner_id: int = Depends(require_owner_id)):
    return get_secret_data(owner_id)


@router.post("/add_secrets")
def add_secrets(payload: SecretPayload, owner_id: int = Depends(require_owner_id)):
    title = payload.title.strip()
    secret = payload.secret.strip()
    if not title or not secret:
        raise HTTPException(status_code=422, detail="Secret title and value are required")
    add_secret_data(title, secret, owner_id)
    return {"message": "Secret added successfully"}


@router.put("/update_secrets")
def update_secrets(
    secret_id: int,
    payload: SecretPayload,
    owner_id: int = Depends(require_owner_id),
):
    title = payload.title.strip()
    secret = payload.secret.strip()
    if not title or not secret:
        raise HTTPException(status_code=422, detail="Secret title and value are required")
    _require_updated(
        update_secret_data(owner_id, secret_id, title, secret), "Secret"
    )
    return {"message": "Secret updated successfully"}


@router.delete("/delete_secrets")
def delete_secrets(secret_id: int, owner_id: int = Depends(require_owner_id)):
    _require_updated(delete_secret_data(owner_id, secret_id), "Secret")
    return {"message": "Secret deleted successfully"}
