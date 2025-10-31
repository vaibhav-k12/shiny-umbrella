"""FastAPI Task Management API

A simple REST API for managing tasks with full CRUD operations.
"""
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import Task, TaskCreate, TaskUpdate, TaskListResponse


# Create FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A simple API for managing tasks with CRUD operations",
    version="1.0.0",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
tasks_db: dict[int, Task] = {}
task_id_counter: int = 1


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Task Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task"
)
async def create_task(task: TaskCreate) -> Task:
    """
    Create a new task with the following information:

    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **completed**: Completion status (default: false)
    - **priority**: Priority level - low, medium, or high (default: medium)
    """
    global task_id_counter

    now = datetime.now()
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        created_at=now,
        updated_at=now
    )

    tasks_db[task_id_counter] = new_task
    task_id_counter += 1

    return new_task


@app.get(
    "/tasks",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="Get all tasks"
)
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$", description="Filter by priority"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return")
) -> TaskListResponse:
    """
    Retrieve all tasks with optional filtering:

    - **completed**: Filter by completion status (true/false)
    - **priority**: Filter by priority level (low/medium/high)
    - **skip**: Number of tasks to skip for pagination
    - **limit**: Maximum number of tasks to return
    """
    filtered_tasks = list(tasks_db.values())

    # Apply filters
    if completed is not None:
        filtered_tasks = [t for t in filtered_tasks if t.completed == completed]

    if priority is not None:
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

    # Sort by creation date (newest first)
    filtered_tasks.sort(key=lambda x: x.created_at, reverse=True)

    # Apply pagination
    total = len(filtered_tasks)
    paginated_tasks = filtered_tasks[skip:skip + limit]

    return TaskListResponse(tasks=paginated_tasks, total=total)


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Get a specific task"
)
async def get_task(task_id: int) -> Task:
    """
    Retrieve a specific task by ID:

    - **task_id**: Unique task identifier
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return tasks_db[task_id]


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Update a task"
)
async def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    """
    Update an existing task by ID:

    - **task_id**: Unique task identifier
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **completed**: New completion status (optional)
    - **priority**: New priority level (optional)

    Only provided fields will be updated.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    existing_task = tasks_db[task_id]
    update_data = task_update.model_dump(exclude_unset=True)

    # Update only provided fields
    for field, value in update_data.items():
        setattr(existing_task, field, value)

    # Update timestamp
    existing_task.updated_at = datetime.now()

    return existing_task


@app.patch(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Partially update a task"
)
async def patch_task(task_id: int, task_update: TaskUpdate) -> Task:
    """
    Partially update an existing task (same as PUT for this implementation):

    - **task_id**: Unique task identifier
    - Accepts partial updates to any task field
    """
    return await update_task(task_id, task_update)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task"
)
async def delete_task(task_id: int) -> None:
    """
    Delete a task by ID:

    - **task_id**: Unique task identifier
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    del tasks_db[task_id]


@app.delete(
    "/tasks",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete all tasks"
)
async def delete_all_tasks() -> None:
    """
    Delete all tasks from the system.

    Warning: This action cannot be undone!
    """
    tasks_db.clear()


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
