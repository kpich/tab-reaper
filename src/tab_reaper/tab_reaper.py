"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse
import subprocess

import questionary


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

    print(f"\nSelected {len(selected_tabs)} tabs to file:\n")
    for tab in selected_tabs:
        print(f"Title: {tab['title']}")
        print(f"URL:   {tab['url']}")
        print()


if __name__ == "__main__":
    main()
