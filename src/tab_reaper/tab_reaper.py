"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse
from datetime import datetime

import questionary
import richxerox

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
        "Tabs to save (space/arrows, enter=confirm, Ctrl+C=cancel):",
        choices=choices,
        instruction="",
    ).ask()

    if selected_tabs is None:
        print("Cancelled.")
        return

    if not selected_tabs:
        print("No tabs selected.")
        return

    current_date = datetime.now().strftime("%Y-%m-%d")

    text = f"{current_date}\n\n"
    html = f"<p><strong>{current_date}</strong></p>\n"

    for tab in selected_tabs:
        text += f"• {tab['title']}\n  {tab['url']}\n\n"
        html += (
            f"<p>• <strong>{tab['title']}</strong><br>\n"
            f"  <a href=\"{tab['url']}\">{tab['url']}</a></p>\n"
        )

    richxerox.copy(text=text, html=html)
    print(f"\n✓ Copied {len(selected_tabs)} tabs to clipboard!")
    print("Paste anywhere with Cmd+V")


if __name__ == "__main__":
    main()
