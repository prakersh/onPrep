# awesomePrep -- Project Standards

## Content Quality (mandatory for all modules)

1. Research interview questions from 3+ sources before writing
2. Each module must cover 95%+ of commonly asked questions for its topic
3. Every question needs both `detailed` and `quick` answers
4. Every concept must have actual runnable code with expected output
5. Gotchas are required on every answer
6. Tags are required on every question

## Tech Stack

- Backend: Flask + SQLAlchemy + SQLite
- Frontend: Tailwind CSS (CDN) + Jinja2 + Highlight.js
- Fonts: Ubuntu (body), JetBrains Mono (code)
- Testing: pytest (strict TDD)

## Architecture

- Content (languages, concepts, questions, answers) is stored in SQLite, seeded from JSON
- Progress tracking is entirely client-side via browser localStorage
- No user accounts or server-side sessions
- The app is designed for public hosting where many users share one server

## TDD Rules

- Write failing tests first, then implement
- Target 90%+ code coverage
- Run `pytest --cov=app -v` before any commit

## Seed Content

- Format: `seeds/<language>/<NN>_<slug>.json`
- Meta: `seeds/<language>/_meta.json`
- Run: `flask seed <language>`
- Idempotent (safe to re-run)

## Adding a New Language

1. Research interview questions (3+ sources)
2. Create `_meta.json` with concept definitions
3. Create numbered JSON files with dual-mode answers
4. Write seed tests in `tests/test_seeds/`
5. Run `flask seed <language>` and verify
6. Validate coverage against research sources

## SVG Visualizations

- Use `var(--viz-*)` CSS custom properties for all colors
- Use CSS `@keyframes` (not SMIL), wrapped in `prefers-reduced-motion`
- Use `viewBox` for responsive sizing
- Only add where visual understanding is clearly better than text

## Expected Output

- C: `/* Expected Output:\n...\n*/`
- Python: `# Expected Output:\n# ...`
- Skip for code with no stdout (definitions, framework code)
