# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a personal expense tracking web application built with Flask (Python) and SQLite. It's structured as a learning/educational project where students incrementally build features.

## Development Commands

### Running the Application

```bash
# Activate the virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the Flask development server
python app.py
# Server starts at http://127.0.0.1:5001 with debug mode enabled
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests with pytest
pytest

# Run a specific test file
pytest tests/test_file.py

# Run with verbose output
pytest -v
```

## Architecture

### Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite with custom connection helpers
- **Frontend**: Jinja2 HTML templates + vanilla JavaScript
- **Styling**: Custom CSS with CSS variables
- **Testing**: pytest with pytest-flask

### Project Structure

```
app.py              # Flask app entry point with route definitions
database/           # Database layer package
├── __init__.py
└── db.py           # To contain: get_db(), init_db(), seed_db()
templates/          # Jinja2 HTML templates
├── base.html       # Base layout with navigation
├── landing.html    # Marketing page
├── login.html      # Authentication pages
├── register.html
├── terms.html      # Legal pages
└── privacy.html
static/             # Static assets
├── css/style.css   # Custom CSS with design tokens
└── js/main.js      # Vanilla JavaScript (modals, interactions)
```

### Key Architectural Patterns

**Database Layer (database/db.py)**
The database module uses standard SQLite with row factory for dictionary-like access:
- `get_db()` — Returns SQLite connection with `sqlite3.Row` factory and foreign keys enabled
- `init_db()` — Creates tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — Inserts sample data for development

**Route Organization (app.py)**
Routes are organized in sections with placeholder routes for upcoming features:
- Current: `/`, `/register`, `/login`, `/terms`, `/privacy`
- Placeholders: `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`

**Template Inheritance**
All templates extend `base.html` which provides:
- Navigation bar with brand and auth links
- Footer with legal links
- Google Fonts (DM Serif Display, DM Sans)
- CSS/JS block injection points: `{% block head %}`, `{% block content %}`, `{% block scripts %}`

**Styling System**
CSS uses design tokens in `:root` for colors, typography, and spacing:
- `--ink`, `--paper`, `--accent` — Primary color roles
- `--font-display`, `--font-body` — Typography
- `--radius-sm/md/lg` — Border radius scale

**JavaScript Patterns**
Vanilla JS only — no frameworks. Current implementation includes:
- Modal system with click-outside and Escape key dismissal
- Video iframe management (stop playback on close by clearing `src`)

## Development Notes

- **Port**: The app runs on port 5001 (not default 5000)
- **Debug**: Debug mode is enabled in `app.run(debug=True, port=5001)`
- **Database Path**: SQLite database `expense_tracker.db` is gitignored
- **No ORM**: Uses raw SQL via SQLite3 module
- **No Build Step**: No bundling or compilation required for frontend assets
