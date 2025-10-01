"""Chrome tab interaction via AppleScript."""

import subprocess


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
            "pmc.ncbi.nlm.nih.gov" in url,
            "sciencedirect.com" in url,
            "cell.com" in url,
            "biomedcentral.com" in url,
            "frontiersin.org" in url,
            "science.org" in url,
            "plos.org" in url,
            url.endswith(".pdf"),
        ]
    )


def close_chrome_tabs(tabs: list[dict]) -> None:
    """Close Chrome tabs matching the given URLs."""
    if not tabs:
        return

    urls = [tab["url"] for tab in tabs]
    urls_applescript = ", ".join(f'"{url}"' for url in urls)

    script = f"""
    set urlsToClose to {{{urls_applescript}}}
    tell application "Google Chrome"
        repeat with w in windows
            set tabList to tabs of w
            repeat with i from (count of tabList) to 1 by -1
                set currentTab to item i of tabList
                if URL of currentTab is in urlsToClose then
                    close currentTab
                end if
            end repeat
        end repeat
    end tell
    """

    subprocess.run(["osascript", "-e", script], check=True)
