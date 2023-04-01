import re

def extract_tags_with_info_and_errors(text):
    tags_with_info = []  # 결과를 저장할 리스트 생성
    tag_pattern = re.compile(r'<([^>]+)>')  # 태그를 찾기 위한 정규 표현식 패턴 생성

    stack = []  # 올바른 태그 쌍을 확인하기 위한 스택

    # 대화 텍스트에서 태그를 찾아 반복 처리
    for match in tag_pattern.finditer(text):
        tag_info = {}  # 태그 정보를 저장할 딕셔너리 생성
        tag_content = match.group(1)  # 괄호 안의 태그 내용 추출
        tag_parts = tag_content.split()  # 태그 내용을 공백을 기준으로 분리

        # 태그 이름 추출
        tag_name = tag_parts[0]
        tag_info["Name"] = tag_name

        if not tag_name.startswith("/"):
            stack.append(tag_name)

        if "content" in tag_content:
            if tag_name.startswith("/"):
                if not stack or tag_name[1:] != stack[-1]:
                    tag_info["error"] = "Mismatched closing tag"
                else:
                    stack.pop()

            else:
                tag_info["content"] = tag_content.split('"')[1]

        # 추가 속성 추출
        attribute_pattern = re.compile(r'(\w+)="([^"]+)"')  # 속성 이름과 값 쌍을 찾기 위한 정규 표현식 패턴 생성
        attributes = attribute_pattern.findall(tag_content)  # 태그 내용에서 속성 이름과 값 쌍을 찾음
        for attribute in attributes:
            tag_info[attribute[0]] = attribute[1]  # 찾은 속성 이름과 값 쌍을 딕셔너리에 저장

        tags_with_info.append(tag_info)  # 딕셔너리를 결과 리스트에 추가

    for tag_name in stack:
        tags_with_info.append({"Name": tag_name, "error": "Missing closing tag"})

    return tags_with_info

conversation = """
AI: <START>
USER: 안녕
AI: <USER>안녕하세요! 어떻게 도와드릴까요?</USER>
USER: 오늘 날씨 알려줘
AI: <Weather search="current">오늘 날씨</Weather>
USER: 인터넷에서 오늘 주요기사에 대해 검색해줘
AI: <Google>오늘 주요 기사</Google>
AI: <START></START>
AI: <Weather></Weahter>
USER:
"""

tags_with_info_and_errors = extract_tags_with_info_and_errors(conversation)
print(tags_with_info_and_errors)
