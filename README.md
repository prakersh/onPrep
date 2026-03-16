# onPrep

A single-user web app helping software engineers prepare for technical interviews. Starting with Python, with plans to expand to C, C++, and Linux.

## Features

- **Dual Study Modes**: Detailed explanations with code or quick recap cards
- **450+ Interview Questions**: Across 28 Python modules (beginner to advanced)
- **Deadline-Based Scheduling**: Set your interview date, get a study plan
- **Progress Tracking**: Track completion and confidence per question
- **Code-Backed Answers**: Every explanation includes runnable code and gotchas

## Tech Stack

- **Backend**: Flask + SQLAlchemy + SQLite
- **Frontend**: Tailwind CSS + Jinja2 + Highlight.js
- **Testing**: pytest (strict TDD, >90% coverage target)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize database
flask db upgrade

# Seed Python content
flask seed python

# Run
flask run
```

## Testing

```bash
pytest --cov=app -v
```

## Project Structure

```
onprep/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Dev/test/prod configs
│   ├── extensions.py        # SQLAlchemy, Migrate
│   ├── models/              # Content + Progress models
│   ├── blueprints/          # Dashboard, Study, Planner, API
│   ├── services/            # Scheduler, Progress calculation
│   └── templates/           # Jinja2 templates
├── seeds/
│   ├── seed_runner.py       # JSON → DB seeder
│   └── python/              # 28 concept JSON files
├── tests/                   # Mirrors app/ structure
├── run.py
└── requirements.txt
```
