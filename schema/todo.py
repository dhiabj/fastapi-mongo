def individual_todo(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "complete": todo["complete"]
    }


def list_serial(todos) -> list:
    return [individual_todo(todo) for todo in todos]
