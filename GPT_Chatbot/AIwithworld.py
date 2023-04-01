import Chatbot
import tag_extracter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup, Tag
from bs4.builder import LXMLTreeBuilder
import re
import sys

def get_user_input(prompt):
    user_input = input(prompt)
    if sys.stdin.encoding != 'UTF-8':
        user_input = user_input.encode(sys.stdin.encoding).decode('utf-8')
    return user_input


# 파일 열기
file_path = 'Guide for GPT'  # 텍스트 파일 경로
with open(file_path, 'r', encoding='utf-8') as file:
    guide = file.read()  # 파일 내용 읽기
# 파일 내용 출력
print(guide)

session=Chatbot.GPT_Complication()

session.request_system(guide)
print("AI: "+session.response_gpt_4())
while(True):
    request=input("USER: ", errors='ignore')
    session.request_user(request)
    response=session.response_gpt_4()
    print("AI: ",response)
    try:
        tags_with_info_and_errors_throw_bs = tag_extracter.extract_tags_with_info_and_errors_throw_bs(response)
        for tag in tags_with_info_and_errors_throw_bs:
            print(tag)
    except (tag_extracter.InvalidTagError, tag_extracter.MissingClosingTagError) as e:
        print(e)
        tags_with_info = tag_extracter.extract_tags_with_info_and_errors_throw_bs()
        for tag in tags_with_info:
            print(tag)