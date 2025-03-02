import json
from typing import List, Dict
from groq import Groq
from google import genai
from ...config import settings


class LLMClient:
    def __init__(self):
        self.groq_llm = Groq(api_key=settings.GROQ_API_KEY)
        self.gemini_llm = genai.Client(api_key=settings.GOOGLE_API_KEY)
        

    def get_response(self, messages: List[Dict[str, str]],is_json=True,perf=False,response_schema=None):
        print("#"*100)
        print(messages)
        try:
            if perf:
                response_format = None
                if is_json:
                    response_format = {
                        'response_mime_type': 'application/json',
                        'response_schema': response_schema,
                    }
                prompt = "".join([message['content'] if message['role']!='system' else f"{message['role']}:{message['content']}" for message in messages])
                response = self.gemini_llm.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config=response_format,
                )
                print(response.text)
                print("#"*100)
                if is_json:
                    return json.loads(response.text)
                else:
                    return response.text
            else:
                response_format = None
                if is_json:
                    response_format = {"type": "json_object"}
                response = self.groq_llm.chat.completions.create(
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