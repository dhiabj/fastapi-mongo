from fastapi import APIRouter
from models.todo import Todo
from config.database import todo_collection
from schema.todo import list_todo
from bson import ObjectId

router = APIRouter()


@router.get("/")
def get_todos():
    todos = list_todo(todo_collection.find())
    return todos
