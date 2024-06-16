from openai import OpenAI
from dotenv import load_dotenv
import os
import crud

load_dotenv() 

class GPT():

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, history, user_id, db):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = history,
            stream=True
        )
        response_str = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                response_str += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content

        crud.create_chat_message(db, role="assistant", text=response_str, user_id=user_id)

# obj = GPT()
# stream = obj.get_simple_response("tell me about biryani")
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
