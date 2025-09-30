
Saves open pdf/arxiv/bioarxiv tabs to your clipboard for easy pasting.

Not user-friendly at all lol look I built this for myself sorry, maybe you'll find
utility if you are drowning in open arxiv tabs like I always am

## Easiest: One command to run

Open Terminal (or iTerm) and run:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run tab-reaper
uvx --from git+https://github.com/kpich/tab-reaper.git tab-reaper
```

Then:
1. Select tabs to save (PDFs/arxiv/biorxiv/nature/pubmed pre-selected, space to toggle, enter to confirm)
   ![Selection screen](readme_images/step1_selection.png)

2. Tabs are copied to your clipboard
   ![Copied confirmation](readme_images/step2_copied.png)

3. Paste anywhere with Cmd+V
   ![Pasted output](readme_images/step3_pasted.png)

4. Optionally close all copied tabs
   ![Close tabs prompt](readme_images/step4_close.png)

## More complicated: Installing + running separately

**Option 1: Using uv**
```bash
uv tool install git+https://github.com/kpich/tab-reaper.git
tab-reaper
```

**Option 2: Manual installation**
```bash
git clone https://github.com/kpich/tab-reaper.git
cd tab-reaper
# In a venv or conda environment:
pip install .
tab-reaper
```
