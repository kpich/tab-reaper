
Closes open pdf/arxiv/bioarxiv tabs and saves them to a google doc along with metadata.

Not user-friendly at all lol look I built this for myself sorry, maybe you'll find
utility if you are drowning in open arxiv tabs like I always am

## Setup

### Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the Google Docs API
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Choose "Desktop app" as application type
6. Download the credentials JSON file
7. Save it to `~/.tab-reaper/credentials.json`

On first run, the tool will open a browser for you to authorize access. After that, it saves a token for future use.

## Usage

```bash
tab-reaper
```

1. Select tabs to save (space to toggle, enter to confirm)
2. Paste your Google Doc URL
3. Tabs are appended to the doc
