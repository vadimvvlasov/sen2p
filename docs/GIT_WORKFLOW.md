# Git Workflow for sen2p

Guide for working with git in the sen2p project.

## Current Status

```bash
Branch: main
Tag: v0.1.0
Commits: 1 (initial release)
```

## Daily Workflow

### Making Changes

```bash
# 1. Check status
git status

# 2. Make your changes
# ... edit files ...

# 3. See what changed
git diff

# 4. Add changes
git add .
# Or add specific files:
git add sen2p/downloader.py docs/README.md

# 5. Commit
git commit -m "Add feature: description"

# 6. Push (if remote configured)
git push origin main
```

### Viewing History

```bash
# Short log
git log --oneline

# Detailed log
git log

# See specific commit
git show <commit-hash>

# See changes in last commit
git show HEAD
```

## Branching Strategy

### Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Work on feature
# ... make changes ...
git add .
git commit -m "Add new feature"

# Merge back to main
git checkout main
git merge feature/new-feature

# Delete feature branch
git branch -d feature/new-feature
```

### Bug Fixes

```bash
# Create bugfix branch
git checkout -b fix/bug-description

# Fix bug
# ... make changes ...
git add .
git commit -m "Fix: bug description"

# Merge to main
git checkout main
git merge fix/bug-description

# Delete branch
git branch -d fix/bug-description
```

## Release Workflow

### Creating a Release

```bash
# 1. Update version in files
# - pyproject.toml
# - sen2p/__init__.py
# - CHANGELOG.md

# 2. Commit changes
git add pyproject.toml sen2p/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"

# 3. Create tag
git tag -a v0.2.0 -m "Release v0.2.0

Features:
- Feature 1
- Feature 2

Fixes:
- Fix 1
- Fix 2"

# 4. Push (if remote configured)
git push origin main
git push origin v0.2.0
```

### Viewing Tags

```bash
# List tags
git tag -l

# Show tag details
git show v0.1.0

# Checkout specific version
git checkout v0.1.0
```

## Commit Message Guidelines

### Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Simple feature
git commit -m "feat: add polygon footprint support"

# Bug fix with details
git commit -m "fix: handle network timeout errors

- Add retry logic with exponential backoff
- Improve error messages
- Add timeout parameter to download()

Closes #42"

# Documentation update
git commit -m "docs: update QUICKSTART guide with new examples"

# Multiple files
git commit -m "refactor: reorganize download logic

- Extract search logic to separate method
- Improve error handling
- Add type hints"
```

## Undoing Changes

### Before Commit

```bash
# Discard changes in working directory
git checkout -- <file>

# Unstage file
git reset HEAD <file>

# Discard all local changes
git reset --hard HEAD
```

### After Commit

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Amend last commit
git commit --amend -m "New commit message"
```

## Working with Remote

### Initial Setup

```bash
# Add remote
git remote add origin https://github.com/username/sen2p.git

# Push initial commit
git push -u origin main

# Push tags
git push --tags
```

### Regular Workflow

```bash
# Fetch changes
git fetch origin

# Pull changes
git pull origin main

# Push changes
git push origin main

# Push specific tag
git push origin v0.2.0
```

## Checking Out Versions

### View Specific Version

```bash
# Checkout tag
git checkout v0.1.0

# Return to latest
git checkout main
```

### Compare Versions

```bash
# Compare two tags
git diff v0.1.0 v0.2.0

# Compare with current
git diff v0.1.0 HEAD

# Show files changed
git diff --name-only v0.1.0 v0.2.0
```

## Useful Commands

### Status and Info

```bash
# Detailed status
git status -v

# Show remote info
git remote -v

# Show branch info
git branch -a

# Show tags
git tag -l -n

# Show commit history graph
git log --graph --oneline --all
```

### Cleaning

```bash
# Remove untracked files (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked directories
git clean -fd
```

## .gitignore

Current `.gitignore` excludes:

```
# Python
__pycache__/
*.pyc
*.egg-info
build/
dist/

# Virtual environments
.venv/
venv/

# Environment files
.env

# Downloaded data
sentinel_data/
data/
*.SAFE/

# Outputs
outputs/
ndvi/
*.tif

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

## Best Practices

1. **Commit Often** - Small, focused commits
2. **Write Clear Messages** - Describe what and why
3. **Use Branches** - For features and fixes
4. **Tag Releases** - Version all releases
5. **Review Before Commit** - Check `git diff`
6. **Keep History Clean** - Meaningful commits
7. **Don't Commit Secrets** - Use .env files
8. **Test Before Push** - Run tests first

## Git Hooks (Optional)

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Run tests
uv run tests/test_imports.py
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Run ruff check
uv run ruff check .
if [ $? -ne 0 ]; then
    echo "Ruff check failed. Commit aborted."
    exit 1
fi

echo "All checks passed."
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Troubleshooting

### Merge Conflicts

```bash
# See conflicted files
git status

# Edit files to resolve conflicts
# ... fix conflicts ...

# Mark as resolved
git add <file>

# Complete merge
git commit
```

### Accidentally Committed Wrong Files

```bash
# Remove from staging
git reset HEAD <file>

# If already committed
git reset --soft HEAD~1
# Fix and recommit
```

### Need to Change Last Commit

```bash
# Amend commit message
git commit --amend -m "New message"

# Add forgotten files
git add forgotten_file.py
git commit --amend --no-edit
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Quick Reference

```bash
# Status
git status              # Show status
git log --oneline       # Show history
git diff                # Show changes

# Making changes
git add .               # Stage all
git commit -m "msg"     # Commit
git push                # Push to remote

# Branching
git branch              # List branches
git checkout -b name    # Create branch
git merge name          # Merge branch

# Tags
git tag -a v1.0 -m ""  # Create tag
git push --tags         # Push tags

# Undo
git reset HEAD file     # Unstage
git checkout -- file    # Discard changes
git reset --soft HEAD~1 # Undo commit
```
