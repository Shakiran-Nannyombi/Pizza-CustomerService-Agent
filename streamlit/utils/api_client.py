"""
API client for communicating with FastAPI backend
"""

import os
import requests
from typing import Dict, Any, Optional


class APIClient:
    """Client for making requests to the FastAPI backend"""
    
    def __init__(self, base_url: str = None):
        # Support Docker networking via environment variable
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Send a chat message to the backend
        
        Args:
            message: User message to send
            
        Returns:
            Dict with 'response' and 'success' keys
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"message": message},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot connect to backend. Make sure the API server is running."
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Please try again."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get backend status
        
        Returns:
            Dict with status information
        """
        try:
            response = requests.get(
                f"{self.base_url}/status",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {
                "status": "offline",
                "message": "Backend is not responding"
            }
    
    def reset_conversation(self) -> Dict[str, Any]:
        """
        Reset the conversation
        
        Returns:
            Dict with success status
        """
        try:
            response = requests.post(
                f"{self.base_url}/reset",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tools(self) -> Dict[str, Any]:
        """
        Get available tools
        
        Returns:
            Dict with tools list
        """
        try:
            response = requests.get(
                f"{self.base_url}/tools",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
