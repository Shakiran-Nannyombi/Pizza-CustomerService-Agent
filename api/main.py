"""
FastAPI Backend for Pizza Customer Service Agent
Handles AI agent interactions and serves API endpoints
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pizza_agent.agents.api_agent import APIAgent
from pizza_agent.config import validate_config
from api.models import (
    ChatRequest,
    ChatResponse,
    StatusResponse,
    ResetResponse,
    ToolsResponse,
    Tool,
    OrderResponse
)
from pizza_agent.tools.order_management import review_current_order as get_order_summary


# Initialize FastAPI app
app = FastAPI(
    title="Pizza Customer Service Agent API",
    description="Backend API for Pizza ordering and customer service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    global agent
    try:
        if validate_config():
            agent = APIAgent(verbose=True)
            print("Agent initialized successfully")
        else:
            print("Configuration validation failed")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Pizza Customer Service Agent API",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get API status"""
    return StatusResponse(
        status="online",
        message="API is running",
        ai_available=agent is not None
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message
    
    Args:
        request: ChatRequest with message
        
    Returns:
        ChatResponse with agent's reply
    """
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="AI agent is not available. Check configuration."
        )
    
    try:
        response = agent.chat(request.message)
        return ChatResponse(
            response=response,
            success=True
        )
    except Exception as e:
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )


@app.post("/reset", response_model=ResetResponse)
async def reset_conversation():
    """Reset the conversation"""
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="AI agent is not available"
        )
    
    try:
        agent.reset_conversation()
        return ResetResponse(
            success=True,
            message="Conversation reset successfully"
        )
    except Exception as e:
        return ResetResponse(
            success=False,
            message=str(e)
        )


@app.get("/tools", response_model=ToolsResponse)
async def get_tools():
    """Get list of available tools"""
    tools = [
        Tool(name="get_pizza_quantity", description="Calculate pizzas needed for a group"),
        Tool(name="recommend_pizza", description="Get pizza recommendations based on preferences"),
        Tool(name="check_store_hours", description="Check store hours for a location"),
        Tool(name="find_nearest_location", description="Find the nearest store location"),
        Tool(name="check_delivery_availability", description="Check if delivery is available"),
        Tool(name="get_special_deals", description="Get current special deals and promotions"),
        Tool(name="calculate_order_total", description="Calculate total order cost"),
        Tool(name="get_estimated_delivery_time", description="Get estimated delivery time")
    ]
    return ToolsResponse(tools=tools)


@app.get("/order", response_model=OrderResponse)
async def get_order():
    """Get the current order summary"""
    try:
        result = get_order_summary()
        if result['success']:
            return OrderResponse(
                success=True,
                order=result['order']
            )
        else:
            return OrderResponse(
                success=False,
                message=result['message']
            )
    except Exception as e:
        return OrderResponse(
            success=False,
            message=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
