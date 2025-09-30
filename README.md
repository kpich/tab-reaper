
Saves open pdf/arxiv/bioarxiv tabs to your clipboard for easy pasting.

Not user-friendly at all lol look I built this for myself sorry, maybe you'll find
utility if you are drowning in open arxiv tabs like I always am

## Installation

**Option 1: Using uv (recommended)**
```bash
uv tool install git+https://github.com/kpich/tab-reaper.git
```

If you don't have uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Option 2: Manual installation**
```bash
git clone https://github.com/kpich/tab-reaper.git
cd tab-reaper
# In a venv or conda environment:
pip install .
```

## Usage

```bash
tab-reaper
```

1. Select tabs to save (PDFs/arxiv/biorxiv/nature/pubmed pre-selected, space to toggle, enter to confirm)
2. Tabs are copied to your clipboard
3. Paste anywhere with Cmd+V
4. Optionally close all copied tabs
