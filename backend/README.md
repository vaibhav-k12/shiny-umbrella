# Task Management API

A simple and efficient REST API built with FastAPI for managing tasks. This API provides full CRUD (Create, Read, Update, Delete) operations with proper validation using Pydantic models.

## Features

- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Type Safety**: Complete type hints throughout the codebase
- **Data Validation**: Pydantic models ensure data integrity
- **Filtering**: Filter tasks by completion status and priority
- **Pagination**: Support for paginated results
- **API Documentation**: Auto-generated interactive API docs
- **CORS Support**: Ready for frontend integration

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   └── models.py        # Pydantic models
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Root

- `GET /` - API information
- `GET /health` - Health check endpoint

### Tasks

#### Create a Task
```http
POST /tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "completed": false,
  "priority": "high"
}
```

#### Get All Tasks
```http
GET /tasks?completed=false&priority=high&skip=0&limit=10
```

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `priority` (optional): Filter by priority (low/medium/high)
- `skip` (optional): Number of tasks to skip (default: 0)
- `limit` (optional): Maximum tasks to return (default: 100, max: 1000)

#### Get a Specific Task
```http
GET /tasks/{task_id}
```

#### Update a Task
```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true
}
```

#### Partially Update a Task
```http
PATCH /tasks/{task_id}
Content-Type: application/json

{
  "completed": true
}
```

#### Delete a Task
```http
DELETE /tasks/{task_id}
```

#### Delete All Tasks
```http
DELETE /tasks
```

## Data Models

### Task

```python
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "priority": "medium",
  "created_at": "2025-10-31T12:00:00",
  "updated_at": "2025-10-31T12:00:00"
}
```

**Fields**:
- `id` (integer): Unique task identifier
- `title` (string): Task title (1-200 characters, required)
- `description` (string): Task description (max 1000 characters, optional)
- `completed` (boolean): Completion status (default: false)
- `priority` (string): Priority level - "low", "medium", or "high" (default: "medium")
- `created_at` (datetime): Task creation timestamp
- `updated_at` (datetime): Last update timestamp

## Example Usage with cURL

### Create a task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium"
  }'
```

### Get all tasks
```bash
curl -X GET "http://localhost:8000/tasks"
```

### Get a specific task
```bash
curl -X GET "http://localhost:8000/tasks/1"
```

### Update a task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### Delete a task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Example Usage with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a task
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "title": "Learn FastAPI",
        "description": "Complete the FastAPI tutorial",
        "priority": "high"
    }
)
task = response.json()
print(f"Created task: {task}")

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks")
tasks = response.json()
print(f"Total tasks: {tasks['total']}")

# Update a task
task_id = task['id']
response = requests.put(
    f"{BASE_URL}/tasks/{task_id}",
    json={"completed": True}
)
updated_task = response.json()
print(f"Updated task: {updated_task}")

# Delete a task
response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
print(f"Task deleted: {response.status_code == 204}")
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 style guidelines and uses type hints throughout.

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

## Future Enhancements

- [ ] Database integration (PostgreSQL/SQLite)
- [ ] User authentication and authorization
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] File attachments
- [ ] Search functionality
- [ ] Task sorting options

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
