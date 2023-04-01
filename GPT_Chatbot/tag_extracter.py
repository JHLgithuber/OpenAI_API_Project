from bs4 import BeautifulSoup, Tag, NavigableString
from bs4.builder import LXMLTreeBuilder

class InvalidTagError(Exception):
    pass

class MissingClosingTagError(Exception):
    pass

class CustomLXMLTreeBuilder(LXMLTreeBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_endtag(self, name):
        tag = self.soup.tagStack[-1]
        if tag and tag.name.lower() != name.lower():
            raise InvalidTagError(f"Mismatched closing tag: {name}")
        super().handle_endtag(name)

def extract_tags_with_info_and_errors_throw_bs(text):
    builder = CustomLXMLTreeBuilder()
    soup = BeautifulSoup(text, 'lxml', builder=builder)
    tags_with_info = []

    for element in soup.recursiveChildGenerator():
        if isinstance(element, Tag):
            if element.name.lower() in ['html', 'body']:
                continue

            tag_info = {}
            tag_info["Name"] = element.name
            tag_info.update(element.attrs)

            if element.string and element.parent is None:  # Check if the element has no parent
                tag_info["content"] = element.string

            tags_with_info.append(tag_info)
        elif isinstance(element, NavigableString) and element.parent is None:  # Check if the element has no parent
            if str(element).strip():  # Ignore empty or whitespace-only strings
                text_info = {"Name": "unknown", "content": str(element).strip()}
                tags_with_info.append(text_info)

    return tags_with_info

if __name__ == "__main__":
    try:
        tags_with_info_and_errors_throw_bs = extract_tags_with_info_and_errors_throw_bs(None)
        for tag in tags_with_info_and_errors_throw_bs:
            print(tag)
    except (InvalidTagError, MissingClosingTagError) as e:
        print(e)
