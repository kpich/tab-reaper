"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse
import subprocess

import questionary

from tab_reaper.chrome import get_chrome_tabs, is_relevant_tab


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

    text = ""
    for tab in selected_tabs:
        text += f"• {tab['title']}\n  {tab['url']}\n\n"

    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    print(f"\n✓ Copied {len(selected_tabs)} tabs to clipboard!")
    print("Paste into your Google Doc with Cmd+V")


if __name__ == "__main__":
    main()
