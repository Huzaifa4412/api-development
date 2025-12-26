# Todo API

A modern RESTful API for managing todo items, built with FastAPI and Pydantic.

![Todo API Demo](image.png)

## Features

- CRUD operations for todo items
- Pagination support for listing todos
- Filter todos by completion status
- Search functionality across title and description
- Toggle completion status endpoint
- Statistics endpoint for summary insights
- Auto-generated OpenAPI documentation
- UUID-based todo identification
- Automatic timestamps (created_at, updated_at)

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **uvicorn** - ASGI server

## Installation

```bash
# Install dependencies using uv
uv sync

# Or with pip
pip install fastapi[standard] uvicorn
```

## Running the API

```bash
# Using uv (recommended)
uv run uvicorn main:app --reload

# Or with uvicorn directly
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```
GET /
```
Returns API status and version.

### List Todos
```
GET /todos
```
Query Parameters:
- `skip` (int, default: 0) - Number of items to skip
- `limit` (int, default: 100, max: 100) - Max items to return
- `completed` (bool, optional) - Filter by completion status
- `search` (string, optional) - Search in title and description

### Get Single Todo
```
GET /todos/{todo_id}
```

### Create Todo
```
POST /todos
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Get milk, eggs, and bread"
}
```

### Update Todo
```
PUT /todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "is_completed": true
}
```

### Toggle Completion
```
PATCH /todos/{todo_id}/toggle
```
Toggles the `is_completed` status of a todo.

### Delete Todo
```
DELETE /todos/{todo_id}
```

### Get Statistics
```
GET /todos/stats/summary
```
Returns:
```json
{
  "total": 10,
  "completed": 5,
  "pending": 5,
  "completion_rate": 50.0
}
```

## Example Usage

### Create a Todo
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Build FastAPI project", "description": "Create a complete Todo API"}'
```

### List All Todos
```bash
curl "http://localhost:8000/todos"
```

### Filter Completed Todos
```bash
curl "http://localhost:8000/todos?completed=false"
```

### Search Todos
```bash
curl "http://localhost:8000/todos?search=FastAPI"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/todos/{id}" \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'
```

### Toggle Completion
```bash
curl -X PATCH "http://localhost:8000/todos/{id}/toggle"
```

### Delete a Todo
```bash
curl -X DELETE "http://localhost:8000/todos/{id}"
```

## Data Model

### TodoCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | 1-200 characters |
| description | string | No | Max 2000 characters |

### TodoUpdate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | 1-200 characters |
| description | string | No | Max 2000 characters |
| is_completed | boolean | No | Completion status |

### TodoResponse
| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID v4 |
| title | string | Todo title |
| description | string | Todo description (nullable) |
| is_completed | boolean | Completion status |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

## License

MIT
