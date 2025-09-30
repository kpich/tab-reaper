"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse

import questionary

from tab_reaper.chrome import get_chrome_tabs, is_relevant_tab
from tab_reaper.gdocs import append_to_doc, extract_doc_id, get_google_docs_service


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
