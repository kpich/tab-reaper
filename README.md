
Closes open pdf/arxiv/bioarxiv tabs and saves them to a google doc along with metadata.

Not user-friendly at all lol look I built this for myself sorry, maybe you'll find
utility if you are drowning in open arxiv tabs like I always am

## Setup

Restart Chrome with remote debugging enabled:

```bash
# Close Chrome completely (Cmd+Q)
osascript -e 'quit app "Google Chrome"'

# Start Chrome with debugging port (will restore your tabs)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```

Note: Chrome might be installed elsewhere on your system.

## Usage

```bash
pdf-tab-reaper
```
