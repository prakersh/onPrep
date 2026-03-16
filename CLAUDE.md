# onPrep — Project Standards

## Content Quality Process (MANDATORY for all modules)
1. **Research first**: Before writing questions for any module, research the top
   interview questions for that topic from 3+ authoritative sources (InterviewBit,
   GeeksforGeeks, LeetCode discussions, etc.)
2. **Coverage target**: Each module must cover >95% of commonly asked interview
   questions for its topic. Cross-reference against real interview question lists.
3. **Dual-mode answers**: Every question MUST have both detailed AND quick answers.
   - Detailed: explain underlying logic, pseudo code, actual runnable code, gotchas
   - Quick: concise key points, minimal code, same gotchas
4. **Code-backed explanations**: Every concept must be backed by actual code.
   No hand-wavy explanations. If unsure, run the code and verify output.
5. **Gotchas are mandatory**: Each answer must include real-world pitfalls.
6. **Verify all code**: Every `actual_code` snippet must be syntactically correct
   and produce the described output. Run it if uncertain.

## Tech Stack
- Backend: Flask + SQLAlchemy + SQLite
- Frontend: Tailwind CSS + Jinja2 + Highlight.js
- Testing: pytest (strict TDD — tests before implementation)

## TDD Rules
- Write failing tests FIRST, then implement
- Target >90% code coverage
- Run `pytest --cov=app -v` before any commit

## Seed Content Format
- Each concept: `seeds/<language>/<NN>_<slug>.json`
- Meta file: `seeds/<language>/_meta.json`
- Runner: `flask seed <language>`
- Idempotent — safe to re-run

## Adding a New Language/Module
1. Research interview questions for the topic (3+ sources)
2. Create `_meta.json` with concept definitions
3. Create numbered JSON files with questions + dual-mode answers
4. Write seed tests in `tests/test_seeds/`
5. Run `flask seed <language>` and verify
6. Validate coverage against research sources
