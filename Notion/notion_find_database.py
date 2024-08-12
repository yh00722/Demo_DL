import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("NOTION_PAGE_ID")
NOTION_API_URL = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
DATABASE_API_URL = "https://api.notion.com/v1/databases"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_notion_page_content(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed, State code: {response.status_code}")
        return None

def get_database_properties(database_id):
    url = f"{DATABASE_API_URL}/{database_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        database_info = response.json()
        properties = database_info.get('properties', {})
        print(f"Database ID: {database_id}, Title: {database_info['title'][0]['plain_text']}")
        for prop_name, prop_details in properties.items():
            print(f"  Property: {prop_name}, Type: {prop_details['type']}")
        return properties
    else:
        print(f"Failed, State code: {response.status_code}")
        return None

def print_page_content(block_id, indent=0):
    page_content = get_notion_page_content(block_id)
    if page_content:
        for block in page_content['results']:
            block_type = block['type']
            indent_str = " " * indent
            print(f"{indent_str}Block type: {block_type}")

            if block_type == 'child_database':
                database_id = block['id']
                print(f"{indent_str}Found database with ID: {database_id}")
                get_database_properties(database_id)
            elif block_type == 'column_list' or block_type == 'column':
                print(f"{indent_str}Processing column list or column")
                print_page_content(block['id'], indent + 2)
            elif 'text' in block[block_type]:
                text = ''.join([t['plain_text'] for t in block[block_type]['text']])
                print(f"{indent_str}Text: {text}")
            else:
                print(f"{indent_str}No text content")

if __name__=="__main__":
    print_page_content(PAGE_ID)
