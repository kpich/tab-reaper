# Environment
- All commands should be run in the conda env llmmtl: `conda activate pdfreaper`
- IMPORTANT: For bash commands in Claude Code, always prefix with: `source ~/miniforge3/etc/profile.d/conda.sh && conda activate pdfreaper && `

# CRITICAL WORKFLOW RULE
⚠️ **NEVER PUSH DIRECTLY TO MAIN** ⚠️
- ALL development work MUST be done on feature branches
- NEVER use `git push origin main` or equivalent commands
- Always create feature branches for any changes
- Use pull requests to merge into main

# Code style
- Avoid vacuous comments that restate what the code already says. Only add comments when they explain WHY something is done or clarify non-obvious behavior.
- Unit tests are in pytest and go next to the file they're testing (so f.py's is
  `f_test.py` right next to it in the same directory). Prefer self-contained tests
  rather than complex fixtures.
- Test function names should be declarative sentences with verbs describing behavior
  (e.g. `test_empty_manifest_returns_empty_types` not `test_empty_manifest_empty_types`)

# Workflow
- `git commit -a` will run precommits so you may need to add and commit twice.
- Do NOT add "Co-Authored-By: Claude" or similar attribution to commit messages
- See CRITICAL WORKFLOW RULE above - always use feature branches

# Commit Message Guidelines
- When pre-commit hooks modify files (formatting, linting), just run `git add .` and commit again with the same meaningful message
- NEVER create separate commits with "Fix formatting from pre-commit hooks" - these are not useful
- Keep using the original descriptive commit message when adding the formatted files
