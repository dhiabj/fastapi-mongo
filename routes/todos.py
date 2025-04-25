from fastapi import APIRouter
from models.todo import Todo
from config.database import todo_collection
from schema.todo import list_serial
from bson import ObjectId

router = APIRouter()


@router.get("/todos")
async def get_todos():
    todos_list = await todo_collection.find().to_list(length=None)  # Fetch all documents
    todos = list_serial(todos_list)  # Serialize the list
    return todos


@router.post("/add-todo")
async def post_todo(todo: Todo):
    await todo_collection.insert_one(dict(todo))


@router.put("/update-todo/{id}")
async def put_todo(id: str, todo: Todo):
    await todo_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(todo)})


@router.delete("/delete-todo/{id}")
async def delete_todo(id: str):
    await todo_collection.find_one_and_delete({"_id": ObjectId(id)})
