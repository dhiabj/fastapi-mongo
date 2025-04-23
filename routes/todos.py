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


@router.post("/")
def post_todo(todo: Todo):
    todo_collection.insert_one(dict(todo))


@router.put("/{id}")
def put_todo(id: str, todo: Todo):
    todo_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(todo)})


@router.delete("/{id}")
def delete_todo(id: str):
    todo_collection.find_one_and_delete({"_id": ObjectId(id)})
