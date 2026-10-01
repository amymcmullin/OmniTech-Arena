# Adding a new game or track

Conventions used so far. Follow them so new games sit cleanly next to the existing ones on one CTFd server.

## Where things go

- **Track** = a subject area, e.g. `tracks/helpdesk-cisco-it-support/`. Start a new track folder for a new subject (e.g. networking, cybersecurity, AI lab).
- **Game** = one folder per course, numbered in order: `0N-<short-game-name>_<course-slug>/`.
- Each game folder contains `README.md`, `challenges.json`, `files/`, `facilitator-guide-and-answer-key.pdf`, and `build/`.

## Category prefixes must be unique and sort in order

CTFd sorts categories alphabetically with the theme setting in [platform-setup.md](platform-setup.md). Pick a two-letter prefix that sorts **after** every prefix already in use:

| In use | Game |
|---|---|
| `01`–`08` | Help Desk 1: First Shift |
| `OS` | Help Desk 2: Second Shift |
| `SC` | Help Desk 3: Third Shift |
| `UP` | Help Desk 4: Final Shift |

Challenge **names** must also be unique across the whole server. `deploy.py` matches unlock requirements by name.

## Design rules we follow

1. **Evidence over trivia.** Most flags should come from analyzing a file (logs, exports, configs, command output). Keep pure recall to short warm-ups.
2. **Tie every answer to the source.** Cite the module and slide (`M2 S73`) or topic in `challenges.py` (the `src` field).
3. **Make wrong guesses expensive.** For letter-sequence or multiple-choice answers, shuffle so the answer isn't `ABCD`, and set `max_attempts`.
4. **Accept reasonable formats.** Use the regex helpers (`exact`, `words`, `letters`, `seq`, `number`) so `INC-10408` and `10408`, or `1,3,5,8` and `1 3 5 8`, both work.
5. **One boss ticket per game** that chains 2–3 files and unlocks after related challenges (`requires`).
6. **A fictional world.** Use the Sawgrass Logistics company and `.example` domains, and the reserved documentation IP ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, 2001:db8::/32).

## Build workflow

```
cd tracks/<track>/<game>/build
python gen_files.py     # writes ../files/* and answers.json (deterministic)
python challenges.py    # sanity check: prints challenge count and points
python -c "import json, challenges as c; json.dump(c.C, open('../challenges.json','w'), indent=2)"
python guide.py         # writes guide.html; print it to PDF as ../facilitator-guide-and-answer-key.pdf
```

Before publishing a game, load it into a test CTFd that already holds the other games. Then, as a test student, submit every correct answer and a few wrong ones. Every game in this repo was checked that way.
