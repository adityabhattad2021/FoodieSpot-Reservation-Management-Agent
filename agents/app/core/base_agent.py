import json
from groq import Groq
from typing import List, Dict, Any
from pydantic import BaseModel
from abc import ABC, abstractmethod

from ..config import settings

MAX_ITERATIONS = 2

class Message(BaseModel):
    role: str
    content: str

class BaseAgent(ABC):
    def __init__(self):
        self.llm_client = Groq(api_key=settings.GROQ_API_KEY)
        self.conversation_history: List[Message] = []
        self.tools = self._initialize_tools()

    @abstractmethod
    def _initialize_tools(self) -> List[Any]:
        """Override this method in specialized agents"""
        raise NotImplementedError

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Override this method in specialized agents"""
        raise NotImplementedError

    async def process_query(self,query) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": query}
        ]

        for _ in range(MAX_ITERATIONS):
            response = self.llm_client.chat.completions.create(
                model=settings.DEFAULT_MODEL,
                messages=messages,
                max_tokens=4096,
                tools=[tool.to_dict() for tool in self.tools],
                tool_choice="auto"
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls


            if tool_calls:
                messages.append({"role":"assistant","tool_calls":[
                    {
                        "id":tool_call.id,
                        "function":{
                            "name":tool_call.function.name,
                            "arguments":tool_call.function.arguments
                        },
                        "type":tool_call.type
                    }
                    for tool_call in tool_calls
                ]})

                function_name = tool_calls[0].function.name
                function_arguments = tool_calls[0].function.arguments
                tool_result = await self._execute_tool(
                    function_name, function_arguments
                )
                messages.append({
                    "tool_call_id":tool_calls[0].id,
                    "role":"tool",
                    "name":function_name,
                    "content":str(tool_result)
                })

            else:
                messages.append({"role":"assistant","content":response_message.content})
                break

        return {
            "message": response_message.content,
        }


    async def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # If we later decide to have more than one tool, the tool name can be used.
        try:
            params = json.loads(params)
            return await self.tools[0].execute(**params)
        except Exception as e: 
            return {"error": str(e)}
        
    def close(self):
        self.conversation_history.clear()