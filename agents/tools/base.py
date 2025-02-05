from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from ..utils.api_client import APIClient

class BaseTool(ABC):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool description"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Return the tool parameters schema"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to Groq API format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }