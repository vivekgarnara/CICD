import os
import requests
from datetime import datetime

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

url = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

data = {
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "GitHub CI Run"
                    }
                }
            ]
        },
        "Status": {
            "select": {
                "name": os.environ.get("CI_STATUS", "Unknown")
            }
        },
        "Branch": {
            "rich_text": [
                {
                    "text": {
                        "content": os.environ.get("GITHUB_REF_NAME", "")
                    }
                }
            ]
        },
        "Commit ID": {
            "rich_text": [
                {
                    "text": {
                        "content": os.environ.get("GITHUB_SHA", "")[:7]
                    }
                }
            ]
        },
        "Date": {
            "date": {
                "start": datetime.utcnow().isoformat()
            }
        },
        "Report Link": {
            "url": f"https://github.com/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}"
        }
    }
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)