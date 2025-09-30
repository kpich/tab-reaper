"""Google Docs integration."""

from pathlib import Path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents"]


def extract_doc_id(url: str) -> str | None:
    """Extract document ID from Google Docs URL."""
    match = re.search(r"/document/d/([a-zA-Z0-9-_]+)", url)
    return match.group(1) if match else None


def get_google_docs_service():
    """Authenticate and return Google Docs API service."""
    creds = None
    token_path = Path.home() / ".tab-reaper" / "token.json"
    credentials_path = Path.home() / ".tab-reaper" / "credentials.json"

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"\nError: credentials.json not found at {credentials_path}")
                print("Please download OAuth credentials from Google Cloud Console")
                print("and save to ~/.tab-reaper/credentials.json")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return build("docs", "v1", credentials=creds)


def append_to_doc(service, doc_id: str, tabs: list[dict]) -> None:
    """Append formatted tab list to Google Doc."""
    doc = service.documents().get(documentId=doc_id).execute()
    content_length = doc.get("body", {}).get("content", [{}])[-1].get("endIndex", 1)

    text = "\n\n"
    for tab in tabs:
        text += f"• {tab['title']}\n  {tab['url']}\n\n"

    requests = [
        {
            "insertText": {
                "location": {"index": content_length - 1},
                "text": text,
            }
        }
    ]

    service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()
