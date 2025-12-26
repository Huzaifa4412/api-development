from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Todo API", version="0.1.0")


# Models
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    is_completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime


# In-memory storage
todos_db: dict[str, TodoResponse] = {}


# Endpoints
@app.get("/", tags=["Health"])
def home():
    return {"message": "Todo API is running!", "version": "0.1.0"}


@app.get("/todos", response_model=list[TodoResponse], tags=["Todos"])
def get_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max items to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search in title and description")
):
    """Get all todos with optional filtering and pagination."""
    todos = list(todos_db.values())

    # Filter by completion status
    if completed is not None:
        todos = [t for t in todos if t.is_completed == completed]

    # Search functionality
    if search:
        search_lower = search.lower()
        todos = [
            t for t in todos
            if search_lower in t.title.lower() or (t.description and search_lower in t.description.lower())
        ]

    # Sort by created_at descending (newest first)
    todos.sort(key=lambda x: x.created_at, reverse=True)

    # Pagination
    return todos[skip : skip + limit]


@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def get_todo(todo_id: str):
    """Get a single todo by ID."""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]


@app.post("/todos", response_model=TodoResponse, status_code=201, tags=["Todos"])
def create_todo(todo: TodoCreate):
    """Create a new todo."""
    now = datetime.now()
    new_todo = TodoResponse(
        id=str(uuid4()),
        title=todo.title,
        description=todo.description,
        is_completed=False,
        created_at=now,
        updated_at=now
    )
    todos_db[new_todo.id] = new_todo
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo(todo_id: str, todo: TodoUpdate):
    """Update an existing todo."""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing = todos_db[todo_id]
    update_data = todo.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now()

    updated_todo = existing.model_copy(update=update_data)
    todos_db[todo_id] = updated_todo
    return updated_todo


@app.patch("/todos/{todo_id}/toggle", response_model=TodoResponse, tags=["Todos"])
def toggle_todo(todo_id: str):
    """Toggle the completion status of a todo."""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing = todos_db[todo_id]
    updated_todo = existing.model_copy(
        update={"is_completed": not existing.is_completed, "updated_at": datetime.now()}
    )
    todos_db[todo_id] = updated_todo
    return updated_todo


@app.delete("/todos/{todo_id}", status_code=204, tags=["Todos"])
def delete_todo(todo_id: str):
    """Delete a todo."""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]


@app.get("/todos/stats/summary", tags=["Stats"])
def get_stats():
    """Get summary statistics about todos."""
    todos = list(todos_db.values())
    total = len(todos)
    completed = sum(1 for t in todos if t.is_completed)
    pending = total - completed

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
    }


def main():
    print("Hello from api-development!")


if __name__ == "__main__":
    main()