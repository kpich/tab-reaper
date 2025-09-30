"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse
from datetime import datetime

import questionary
import richxerox

from tab_reaper.chrome import close_chrome_tabs, get_chrome_tabs, is_relevant_tab


def get_demo_tabs() -> list[dict]:
    """Return fake tab data for screenshots."""
    return [
        {
            "url": "https://arxiv.org/abs/2312.12345",
            "title": "Attention Is All You Need: A Comprehensive Survey",
        },
        {
            "url": "https://www.biorxiv.org/content/10.1101/2023.01.01.123456v1",
            "title": "Novel Mechanisms in Neural Plasticity",
        },
        {
            "url": "https://example.com/paper.pdf",
            "title": "Machine Learning Methods for Climate Prediction",
        },
        {
            "url": "https://www.google.com/search?q=is+a+car+a+kind+of+dog",
            "title": "is a car a kind of dog - Google Search",
        },
        {
            "url": "https://www.google.com/search?q=what+kind+of+horse+is+a+honda+civic",
            "title": "what kind of horse is a honda civic - Google Search",
        },
        {
            "url": "https://www.google.com/search?q=do+cars+have+feelings",
            "title": "do cars have feelings - Google Search",
        },
        {
            "url": "https://www.google.com/search?q=how+to+tell+does+your+car+hate+you",
            "title": "how to tell does your car hate you - Google Search",
        },
        {
            "url": "https://www.nature.com/articles/s41586-023-01234-5",
            "title": "Breakthrough in quantum computing error correction",
        },
    ]


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List and manage PDF/paper tabs in Chrome"
    )
    parser.add_argument(
        "--demo", action="store_true", help="Use fake tab data for screenshots"
    )
    args = parser.parse_args()

    tabs = get_demo_tabs() if args.demo else get_chrome_tabs()

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
    html = f"<h2>{current_date}</h2>\n"

    for tab in selected_tabs:
        text += f"• {tab['title']}\n  {tab['url']}\n\n"
        html += (
            f"<p>• <strong>{tab['title']}</strong><br>\n"
            f"  <a href=\"{tab['url']}\">{tab['url']}</a></p>\n"
        )

    richxerox.copy(text=text, html=html)
    print(f"\n✓ Copied {len(selected_tabs)} tabs to clipboard!")
    print("Paste anywhere with Cmd+V")

    if not args.demo:
        should_close = questionary.confirm(
            "Close all copied tabs?", default=False
        ).ask()

        if should_close:
            close_chrome_tabs(selected_tabs)
            print(f"✓ Closed {len(selected_tabs)} tabs")


if __name__ == "__main__":
    main()
