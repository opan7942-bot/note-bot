from fastapi import APIRouter
from bot_database import (get_notes_data,add_note_data,delete_note_data,
                          get_todos_data,add_todo_data,delete_todo_data,
                          get_secret_data,add_secret_data,delete_secret_data
                          )
router = APIRouter()
#============================= note ====================
@router.get("/get_notes")
def get_notes(owner_id: int):
    notes_data = get_notes_data(owner_id)
    return notes_data

@router.post("/add_notes")
def add_notes(owner_id: int,text: str):
    add_note_data(owner_id, text)
    return {"message": "Note added successfully"}

@router.delete("/delete_notes")
def delete_notes(owner_id: int,note_id: int):
    delete_note_data(owner_id, note_id)
    return {"message": "Note deleted successfully"}
#=========================================================
#======================to_do==============================
@router.get("/get_todos")
def get_todos(owner_id: int):
    return get_todos_data(owner_id)

@router.post("/add_todos")
def add_todos(owner_id: int,task: str):
    add_todo_data(owner_id, task)
    return {"message": "Todos added successfully"}

@router.delete("/delete_todos")
def delete_todos(owner_id: int,todo_id: int):
    delete_todo_data(owner_id, todo_id)
    return {"message": "Todos deleted successfully"}
#=========================================================
#========================secret===========================
@router.get("/get_secrets")
def get_secrets(owner_id: int):
    return get_secret_data(owner_id)

@router.post("/add_secrets")
def add_secrets(owner_id: int,secret: str,title: str):
    add_secret_data(title,secret,owner_id)
    return {"message": "Secret added successfully"}

@router.delete("/delete_secrets")
def delete_secrets(owner_id: int,secret_id: int):
    delete_secret_data(owner_id, secret_id)
    return {"message": "Secret deleted successfully"}
#=========================================================