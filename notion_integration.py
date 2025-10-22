from notion_client import Client
from datetime import datetime
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def add_reflection_to_notion(ref_type, message):
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Date": {"date": {"start": datetime.now().isoformat()}},
                "Type": {"select": {"name": ref_type.capitalize()}},
                "Reflection": {"title": [{"text": {"content": message}}]},
                "Timestamp": {"date": {"start": datetime.now().isoformat()}},
                "Source": {"rich_text": [{"text": {"content": "Telegram Bot"}}]}
            }
        )
        print(f"✅ Added {ref_type} reflection to Notion.")
    except Exception as e:
        print(f"❌ Notion add failed: {e}")
