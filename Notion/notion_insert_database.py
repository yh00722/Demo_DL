import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def split_text_into_blocks(content: str, max_length=2000):
    content = content.encode('utf-8', 'replace').decode('utf-8')
    return [content[i:i + max_length] for i in range(0, len(content), max_length)]

def create_notion_page(title: str, content: str):
    content_blocks = split_text_into_blocks(content)

    children_blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": block
                        }
                    }
                ]
            }
        } for block in content_blocks
    ]

    new_page_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "名前": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "transcript"
                            }
                        }
                    ],
                    "children": children_blocks
                }
            }
        ]
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=new_page_data)

    if response.status_code == 200:
        print("Success")
        return response.json()
    else:
        print(f"Failed, State code: {response.status_code}")
        print(response.json())
        return None

if __name__=="__main__":
    page_title = "New Notion Page"
    page_content = "Contents in Page" * 10
    create_notion_page(page_title, page_content)
