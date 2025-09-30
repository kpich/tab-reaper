"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse
from pathlib import Path
import re
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import questionary

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


def get_chrome_tabs() -> list[dict]:
    """Get all open Chrome tabs via AppleScript."""
    script = """
    set output to ""
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set output to output & (URL of t) & "\\n" & (title of t) & "\\n"
            end repeat
        end repeat
    end tell
    return output
    """
    result = subprocess.run(
        ["osascript", "-e", script], capture_output=True, text=True, check=True
    )
    output = result.stdout.strip()
    if not output:
        return []

    tabs = []
    lines = output.split("\n")
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            url = lines[i].strip()
            title = lines[i + 1].strip()
            tabs.append({"url": url, "title": title})
    return tabs


def is_relevant_tab(tab: dict) -> bool:
    """Check if a tab is a paper (arxiv, biorxiv, nature, pubmed, or PDF)."""
    url = tab.get("url", "").lower()

    if url.startswith("file://"):
        return False

    return any(
        [
            "arxiv.org" in url,
            "biorxiv.org" in url,
            "nature.com" in url,
            "pubmed.ncbi.nlm.nih.gov" in url,
            url.endswith(".pdf"),
        ]
    )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List and manage PDF/paper tabs in Chrome"
    )
    parser.parse_args()

    tabs = get_chrome_tabs()

    choices = [
        questionary.Choice(
            title=f"{tab['title'][:80]}... - {tab['url'][:50]}"
            if len(tab["title"]) > 80
            else f"{tab['title']} - {tab['url'][:50]}",
            value=tab,
            checked=is_relevant_tab(tab),
        )
        for tab in tabs
    ]

    selected_tabs = questionary.checkbox(
        "Tabs to add to gdoc and close (space/arrows, enter=confirm, Ctrl+C=cancel):",
        choices=choices,
        instruction="",
    ).ask()

    if selected_tabs is None:
        print("Cancelled.")
        return

    if not selected_tabs:
        print("No tabs selected.")
        return

    doc_url = questionary.text("Paste Google Doc URL:").ask()

    if not doc_url:
        print("Cancelled.")
        return

    doc_id = extract_doc_id(doc_url)
    if not doc_id:
        print("Error: Invalid Google Docs URL")
        return

    service = get_google_docs_service()
    if not service:
        return

    print(f"\nAppending {len(selected_tabs)} tabs to Google Doc...")
    append_to_doc(service, doc_id, selected_tabs)
    print("✓ Successfully added tabs to Google Doc!")


if __name__ == "__main__":
    main()
