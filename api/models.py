"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    success: bool = True
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    status: str
    message: str
    ai_available: bool


class ResetResponse(BaseModel):
    """Response model for reset endpoint"""
    success: bool
    message: str


class Tool(BaseModel):
    """Model for a tool definition"""
    name: str
    description: str


class ToolsResponse(BaseModel):
    """Response model for tools endpoint"""
    tools: List[Tool]
    success: bool = True
