# [awesomePrep](https://awesomeprep.prakersh.in)

Open source interview prep for software engineers. 774 questions across Python and C with runnable code, expected output, SVG visualizations, and text-to-speech narration. No accounts required -- progress is saved in your browser.

**Try it now -->** [awesomeprep.prakersh.in](https://awesomeprep.prakersh.in)

## Features

- **774 questions** across 53 modules (28 Python, 25 C)
- **Dual study modes** -- Detailed (full explanation, pseudo code, actual code, gotchas) and Quick (key points, minimal code)
- **Expected output** on every code block -- collapsible panel inside the code card
- **28 SVG visualizations** for data structures, memory layout, sorting algorithms, process lifecycle
- **Narration mode** -- listen to answers with sentence-level highlighting, voice picker, speed control
- **No signup** -- progress tracked in browser localStorage, works for multiple users on the same server
- **Interview planner** -- add deadlines, get auto-generated daily study plans
- **Light and dark mode** -- follows system preference, remembers your choice

## Quick Start

```bash
git clone https://github.com/prakersh/awesomeprep.git
cd awesomeprep
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

flask db upgrade
flask seed python
flask seed c

flask run
```

Open http://localhost:5000 in your browser.

## Tech Stack

| Layer | Tool |
|-------|------|
| Backend | Flask, SQLAlchemy, SQLite |
| Frontend | Tailwind CSS (CDN), Jinja2, Highlight.js |
| Fonts | Ubuntu, JetBrains Mono (Google Fonts) |
| Markdown | mistune |
| Tests | pytest (460+ tests) |

## Project Layout

```
app/
  blueprints/       # Routes: dashboard, study, planner, api
  models/           # SQLAlchemy models: content, progress
  services/         # Scheduler logic
  templates/        # Jinja2 templates
seeds/
  python/           # 28 JSON files (questions + answers + visualizations)
  c/                # 25 JSON files
  seed_runner.py    # Loads JSON into the database (idempotent)
tests/              # Mirrors app/ structure
migrations/         # Alembic database migrations
```

## Adding Content

Each topic is a JSON file in `seeds/<language>/`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Quick version:

1. Create or edit a numbered JSON file (e.g. `seeds/python/29_new_topic.json`)
2. Add the concept definition to `seeds/python/_meta.json`
3. Run `flask seed python`

Every question needs two answers: `detailed` and `quick`. Code must be runnable with expected output.

## Running Tests

```bash
pytest --cov=app -v
```

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding questions, fixing content, and submitting PRs.

## Support

If this project helps your interview prep:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/prakersh)

## License

GPL-3.0. See [LICENSE](LICENSE) for details.
