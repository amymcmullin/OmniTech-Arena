# OmniTech Arena

Capture-the-flag (CTF) games for the **Computer Systems & Information Technology** program at Immokalee Technical College (iTECH). They cover the whole curriculum, not just cybersecurity.

Each game is a set of jeopardy-style challenges for [CTFd](https://github.com/CTFd/CTFd). Most flags come from **investigating realistic evidence**, such as ticket exports, logs, command output, and config files, rather than from trivia recall. Games are grouped into **tracks** by subject, and every game is tied to the course it supports so students can play it right after finishing that material in Canvas.

> **Heads-up:** this repository is public and includes every flag and answer key, so students who find it can see the answers.

## Tracks

| Track | Source course(s) | Games | Challenges | Points |
|---|---|---|---|---|
| [Help Desk / Cisco IT Support](tracks/helpdesk-cisco-it-support/) | Cisco NetAcad IT Support Specialist career path (CCST IT Support) | 4 | 153 | 32,600 |

More tracks will be added as more subjects are covered.

## Repository layout

```
OmniTech-Arena/
├── README.md                     you are here
├── docs/
│   ├── platform-setup.md         CTFd install, students, board settings, known quirks
│   └── adding-a-track.md         conventions for building new games
├── tools/
│   └── deploy.py                 loads any game into CTFd through its API
└── tracks/
    └── helpdesk-cisco-it-support/
        ├── README.md             track overview, time estimates, alignment
        ├── templates/            student import CSV template
        └── 0N-<game>/            one folder per game
            ├── README.md
            ├── challenges.json   challenge text, flags, hints, tags, unlocks
            ├── files/            evidence files students download
            ├── facilitator-guide-and-answer-key.pdf
            └── build/            scripts that generate the files and challenges
```

## Quick start

1. Set up CTFd. See [docs/platform-setup.md](docs/platform-setup.md).
2. Generate an admin access token in CTFd: **Settings → Access Tokens → Generate**.
3. Load a game:

   ```
   pip install requests
   python tools/deploy.py tracks/helpdesk-cisco-it-support/01-first-shift_it-customer-support-basics --url http://localhost:8000 --token ctfd_xxx
   ```

4. Repeat step 3 for each game you want on the server. Games load side by side and never overwrite each other.

## How the games are run at iTECH

- **Always open and self-paced.** Every game stays visible all year. With open-entry enrollment and several start dates, students move into a game when they finish the matching Canvas module.
- **One server, many games.** Category prefixes (`01`–`08`, `OS`, `SC`, `UP`, …) keep each game grouped together on the board.
- **Competitive capstones** run separately, on a different platform.
