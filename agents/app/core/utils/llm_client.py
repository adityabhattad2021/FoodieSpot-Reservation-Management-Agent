import json
from typing import List, Dict
from groq import Groq
from ...config import settings


class LLMClient:
    def __init__(self):
        self.llm = Groq(api_key=settings.GROQ_API_KEY)

    def get_response(self, messages: List[Dict[str, str]],is_json=True):
        print("#"*100)
        print(messages)
        try:
            response_format = None
            if is_json:
                response_format = {"type": "json_object"}
            response = self.llm.chat.completions.create(
                model=settings.DEFAULT_MODEL,
                messages=messages,
                temperature=1,
                max_completion_tokens=100,
                top_p=1,
                stream=False,
                response_format=response_format,
                stop=None,
            )
            print(response.choices[0].message.content)
            print("#"*100)
            if is_json:
                return json.loads(response.choices[0].message.content)
            else:
                return response.choices[0].message.content
        except Exception as e:
            return {"Error in LLM Client": str(e)}