# 🚀 GitHub Deployment Guide — NikeSenti

Complete step-by-step guide to push your project to GitHub and optionally deploy it live on **Streamlit Cloud** (free).

---

## ✅ Prerequisites

Before starting, make sure you have:

| Tool | Check | Install Link |
|---|---|---|
| Git | `git --version` | https://git-scm.com/downloads |
| Python 3.10+ | `python --version` | https://python.org |
| GitHub account | — | https://github.com/join |
| Streamlit account (optional, for live deploy) | — | https://share.streamlit.io |

---

## PART 1 — Push Project to GitHub

### Step 1 · Create a GitHub repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name**: `nike-sentiment-analysis`
   - **Description**: `AI-powered Nike review sentiment dashboard | CAPACITI Bootcamp Week 3`
   - **Visibility**: ✅ Public *(required for free Streamlit Cloud deploy)*
3. ❌ Do **NOT** tick "Add a README" (you already have one)
4. Click **"Create repository"**

You'll land on a page that shows your repo URL — copy it. It looks like:
```
https://github.com/YOUR_USERNAME/nike-sentiment-analysis.git
```

---

### Step 2 · Open your terminal

Navigate to your project folder:

```bash
cd path/to/sentiment-analysis-tool
```

**Windows example:**
```bash
cd C:\Users\YourName\Documents\sentiment-analysis-tool
```

**Mac/Linux example:**
```bash
cd ~/Documents/sentiment-analysis-tool
```

---

### Step 3 · Initialise Git

```bash
git init
```

This creates a hidden `.git` folder — your local repository is now ready.

---

### Step 4 · Configure your Git identity (first time only)

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your@email.com"
```

---

### Step 5 · Stage all files

```bash
git add .
```

Check what will be committed:
```bash
git status
```

You should see all your project files listed in green. The `.gitignore` will have excluded `venv/`, `__pycache__/`, and `.DS_Store` automatically.

---

### Step 6 · Make your first commit

```bash
git commit -m "🚀 Initial commit — NikeSenti AI Sentiment Dashboard"
```

---

### Step 7 · Connect to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/nike-sentiment-analysis.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

### Step 8 · Push to GitHub

```bash
git branch -M main
git push -u origin main
```

If prompted, enter your GitHub **username** and a **Personal Access Token** (PAT) as password.

> **How to create a PAT:**
> GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
> Tick `repo` scope → Generate → Copy and paste it as your password.

---

### Step 9 · Verify on GitHub

Open `https://github.com/YOUR_USERNAME/nike-sentiment-analysis` in your browser.

All files should be visible ✅

---

## PART 2 — Deploy Live on Streamlit Cloud (Free)

Turn your dashboard into a public URL anyone can visit — no server required.

### Step 1 · Go to Streamlit Cloud

Visit: **https://share.streamlit.io**

Sign in with your GitHub account.

---

### Step 2 · Create a new app

1. Click **"New app"**
2. Fill in:
   - **Repository**: `YOUR_USERNAME/nike-sentiment-analysis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy"**

Streamlit will:
- Pull your repo
- Install `requirements.txt` automatically
- Launch your app at a public URL like:
  `https://your-username-nike-sentiment-analysis-app-xxxxx.streamlit.app`

---

### Step 3 · One-time TextBlob corpus fix

Because Streamlit Cloud needs TextBlob's NLTK data, create this file in your project:

**Create file: `setup.sh`**
```bash
#!/bin/bash
python -m textblob.download_corpora
```

**Create file: `packages.txt`** (leave it empty — just create it so Streamlit knows to look):
```
# No system packages needed
```

Then update your repo:
```bash
git add setup.sh packages.txt
git commit -m "fix: add TextBlob corpus setup for Streamlit Cloud"
git push
```

Streamlit Cloud will re-deploy automatically.

---

## PART 3 — Updating Your Project

Every time you change code locally, push updates like this:

```bash
# Stage changed files
git add .

# Commit with a descriptive message
git commit -m "feat: add word cloud visualisation"

# Push to GitHub
git push
```

Streamlit Cloud will automatically redeploy within ~30 seconds.

---

## PART 4 — Good Git Commit Message Conventions

| Prefix | When to use |
|---|---|
| `feat:` | New feature added |
| `fix:` | Bug fixed |
| `docs:` | README or documentation updated |
| `style:` | UI/CSS changes only |
| `refactor:` | Code restructured without behaviour change |
| `data:` | Dataset updated |
| `chore:` | Dependency or config updates |

**Examples:**
```bash
git commit -m "feat: add rating vs polarity chart"
git commit -m "fix: correct neutral threshold in classifier"
git commit -m "docs: update README with screenshots"
git commit -m "data: expand Nike reviews to 75 entries"
```

---

## PART 5 — Recommended README Badge URLs

Add these to the top of your `README.md` after pushing:

```markdown
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?logo=streamlit)
![TextBlob](https://img.shields.io/badge/NLP-TextBlob-green)
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/nike-sentiment-analysis)
![Live App](https://img.shields.io/badge/Live%20App-Streamlit%20Cloud-brightgreen?logo=streamlit)
```

---

## PART 6 — Project Folder Checklist Before Pushing

Run this to confirm your structure:

```bash
ls -la
```

Expected output:
```
.gitignore
.streamlit/
  config.toml
app.py
charts.py
insights_report.md
packages.txt
project_structure.txt
README.md
requirements.txt
reviews.csv
sentiment_analyzer.py
setup.sh
styles.css
```

---

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| `git push` asks for password | Use a Personal Access Token, not your GitHub password |
| `ModuleNotFoundError: textblob` | Run `pip install -r requirements.txt` |
| `TextBlob corpus error` | Run `python -m textblob.download_corpora` |
| Streamlit Cloud shows blank app | Check that `app.py` is in the root of the repo, not in a subfolder |
| Charts not showing | Ensure `matplotlib` is in `requirements.txt` |
| `.streamlit/config.toml` not found | Create the `.streamlit/` folder manually |

---

*Guide written for CAPACITI AI Bootcamp · Week 3 · NikeSenti Project · 2026*
