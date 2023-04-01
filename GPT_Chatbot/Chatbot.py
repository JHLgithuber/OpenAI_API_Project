import openai
import os
from dotenv import load_dotenv

class GPT_Complication:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages_stack=[]

    def request_system(self,content):
        self.messages_stack.append({"role": "system", "content": content})

    def request_user(self,content):
        self.messages_stack.append({"role": "user", "content": content})


    def response_gpt_35(self): 
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo", 
          messages=self.messages_stack
        )
        self.messages_stack.append(completion.choices[0].message)
        return completion.choices[0].message.content

    def response_gpt_4(self): 
        completion = openai.ChatCompletion.create(
          model="gpt-4", 
          messages=self.messages_stack
        )
        self.messages_stack.append(completion.choices[0].message)
        return completion.choices[0].message.content

if __name__ == '__main__':
    New_session=GPT_Complication()
    while(True):
        New_session.request_user(input("USER: ").encode("euc-kr").decode("euc-kr"))
        print("GPT-3.5-Trubo: "+New_session.response_gpt_35())
        print("GPT-4: "+New_session.response_gpt_4())
