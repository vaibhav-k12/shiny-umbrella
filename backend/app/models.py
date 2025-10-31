"""Pydantic models for Task Management API"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base Task model with common attributes"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: bool = Field(default=False, description="Task completion status")
    priority: Optional[str] = Field(
        default="medium",
        pattern="^(low|medium|high)$",
        description="Task priority level"
    )


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: Optional[bool] = Field(None, description="Task completion status")
    priority: Optional[str] = Field(
        None,
        pattern="^(low|medium|high)$",
        description="Task priority level"
    )


class Task(TaskBase):
    """Complete Task model including database fields"""
    id: int = Field(..., description="Unique task identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Task creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Task last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Response model for listing tasks"""
    tasks: list[Task]
    total: int
