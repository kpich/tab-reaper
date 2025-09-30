"""Main entry point for pdf-tab-reaper CLI tool."""

import argparse

import pychrome


def get_chrome_tabs(port: int = 9222) -> list[dict]:
    """Connect to Chrome via CDP and get all open tabs."""
    browser = pychrome.Browser(url=f"http://127.0.0.1:{port}")
    tabs = browser.list_tab()
    return tabs


def is_relevant_tab(tab: dict) -> bool:
    """Check if a tab is a paper (arxiv, biorxiv, or PDF)."""
    url = tab.get("url", "").lower()
    return any(
        [
            "arxiv.org" in url,
            "biorxiv.org" in url,
            url.endswith(".pdf"),
        ]
    )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List and manage PDF/paper tabs in Chrome"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9222,
        help="Chrome remote debugging port (default: 9222)",
    )
    args = parser.parse_args()

    tabs = get_chrome_tabs(args.port)
    relevant_tabs = [tab for tab in tabs if is_relevant_tab(tab)]

    print(f"Found {len(relevant_tabs)} relevant tabs:\n")
    for tab in relevant_tabs:
        print(f"Title: {tab.get('title', 'N/A')}")
        print(f"URL:   {tab.get('url', 'N/A')}")
        print()


if __name__ == "__main__":
    main()
