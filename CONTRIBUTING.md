# Contributing to [awesomePrep](https://awesomeprep.prakersh.in)

Thanks for your interest in improving awesomePrep. This guide covers how to add content, fix bugs, and submit changes.

## Ways to Contribute

- **Add questions** to existing modules
- **Add new modules** (new topics within Python or C)
- **Add new languages** (Go, Java, JavaScript, etc.)
- **Fix incorrect code or explanations**
- **Add expected output** to code blocks that are missing it
- **Add SVG visualizations** for concepts that benefit from visual aids
- **Fix UI bugs** or improve templates
- **Improve tests**

## Setup

```bash
git clone https://github.com/prakersh/awesomeprep.git
cd awesomeprep
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask seed python && flask seed c
```

Run tests to make sure everything works:

```bash
pytest --cov=app -v
```

## Content Guidelines

### Question Quality

1. **Research first.** Before writing questions for any module, check what is commonly asked in real interviews. Use 3+ sources (GeeksforGeeks, LeetCode discussions, InterviewBit, etc.).
2. **Coverage target.** Each module should cover 95%+ of commonly asked interview questions for its topic.
3. **Dual-mode answers are required.** Every question must have both a `detailed` and a `quick` answer.
   - Detailed: explanation, pseudo code, actual runnable code, key points, gotchas
   - Quick: concise key points, minimal code, same gotchas
4. **Code must be runnable.** Every `actual_code` snippet must be syntactically correct and produce the output described. Run it if you are not sure.
5. **Expected output is required.** Append a comment block at the end of `actual_code`:
   - C: `/* Expected Output:\nline1\nline2\n*/`
   - Python: `# Expected Output:\n# line1\n# line2`
   - Skip if the code has no stdout output (definitions only, framework code, etc.)
6. **Gotchas are required.** Every answer must include real-world pitfalls.
7. **Tags are required.** Each question must have a `tags` array with short keyword strings (e.g. `["pointers", "arithmetic", "arrays"]`).

### Seed File Format

Each concept is a JSON file: `seeds/<language>/<NN>_<slug>.json`

```json
{
  "concept_slug": "data-types-variables",
  "questions": [
    {
      "title": "What are the basic data types in Python?",
      "display_order": 1,
      "difficulty": "beginner",
      "tags": ["data-types", "int", "float", "str"],
      "answers": [
        {
          "mode": "detailed",
          "explanation": "Markdown text explaining the concept...",
          "pseudo_code": "Optional pseudo code",
          "actual_code": "x = 42\nprint(type(x))\n\n# Expected Output:\n# <class 'int'>",
          "code_language": "python",
          "key_points": ["Point 1", "Point 2"],
          "gotchas": ["Gotcha 1", "Gotcha 2"],
          "visualization": ""
        },
        {
          "mode": "quick",
          "explanation": "Short summary...",
          "actual_code": "x = 42\nprint(type(x))\n\n# Expected Output:\n# <class 'int'>",
          "code_language": "python",
          "key_points": ["Point 1"],
          "gotchas": ["Gotcha 1"]
        }
      ]
    }
  ]
}
```

### Meta File

Every language needs `seeds/<language>/_meta.json`:

```json
{
  "name": "Python",
  "icon": "python",
  "is_active": true,
  "display_order": 1,
  "concepts": [
    {
      "title": "Data Types & Variables",
      "slug": "data-types-variables",
      "description": "Learn about Python data types",
      "display_order": 1,
      "estimated_minutes": 30,
      "difficulty": "beginner"
    }
  ],
  "relationships": [
    {"from": "data-types-variables", "to": "operators-expressions", "type": "prerequisite"}
  ]
}
```

### Adding a New Language

1. Create `seeds/<language>/_meta.json` with concept definitions
2. Create numbered JSON files for each concept
3. Add seed tests in `tests/test_seeds/`
4. Register the language in the seed CLI command if needed
5. Run `flask seed <language>` and verify

### SVG Visualizations

The `visualization` field on answers accepts inline SVG. Requirements:

- Use CSS custom properties for colors: `var(--viz-fg)`, `var(--viz-accent)`, `var(--viz-border)`, `var(--viz-surface)`, `var(--viz-fg-muted)`
- Use CSS `@keyframes` for animation (not SMIL), wrapped in `@media (prefers-reduced-motion: no-preference)`
- Use `viewBox` for responsive sizing (no fixed width/height)
- Use `font-family: 'Ubuntu', sans-serif` for labels, `'JetBrains Mono', monospace` for code
- Only add visualizations where they genuinely help understanding (data structures, memory layout, algorithms, process diagrams)

## Submitting Changes

1. Fork the repo
2. Create a branch: `git checkout -b add-go-basics`
3. Make your changes
4. Run tests: `pytest --cov=app -v`
5. Seed and verify: `flask seed <language>`
6. Commit with a clear message
7. Open a pull request

### Commit Messages

Use conventional commits:

- `feat: add Go language with 15 modules`
- `fix: correct merge sort expected output in C module 14`
- `docs: update contributing guide`
- `chore: update dependencies`

### PR Checklist

- [ ] All tests pass (`pytest --cov=app -v`)
- [ ] Seed files are valid JSON
- [ ] Every question has both detailed and quick answers
- [ ] Code is runnable with correct expected output
- [ ] Tags are present on all questions
- [ ] No hardcoded colors in SVG visualizations (use CSS custom properties)

## Architecture Notes

- **Content is server-side.** Languages, concepts, questions, and answers live in SQLite, seeded from JSON files.
- **Progress is client-side.** All progress tracking uses browser localStorage. No user accounts, no server-side session state.
- **The seed runner is idempotent.** Running `flask seed python` multiple times is safe. It upserts.
- **Templates use Tailwind CSS via CDN.** No build step required.

## Questions?

Open an issue on GitHub or reach out via the repository discussions.
