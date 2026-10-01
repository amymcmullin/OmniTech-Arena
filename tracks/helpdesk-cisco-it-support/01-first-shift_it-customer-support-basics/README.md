# Help Desk: First Shift

**Course:** Cisco NetAcad *IT Customer Support Basics* (Cisco estimate: 4 h)  
**Size:** 33 challenges · 7,550 points · 8 categories · 16 evidence files  
**Estimated play time:** 1.5-2 h (estimate, not yet measured with students)  
**Tested:** every flag was solved by a test student on CTFd 3.8.6 alongside the other games in this track

## Story and skills

Students are brand-new Tier 1 techs at **Sawgrass Logistics** (a fictional company). They work a ticket queue and calculate SLA breaches, FCR and response times from a CSV; identify customer types and hold/transfer mistakes in call transcripts; QA ticket notes for confidentiality and missing outcomes; order the 8-step troubleshooting process; audit remote-session logs for missing consent and sessions left open; spot an AI-invented `ipconfig` switch and a privacy-leaking AI prompt; and classify app and email failures.

## Boss ticket

**The CFO's Month-End Meltdown**: follow the CFO's ticket to the remote-session notes to the error code to the internal KB article's resolution code.

## Source note

Built directly from the instructor decks' slide content (help desk concepts, ticket fields, KPIs, customer types, the Diego blue-screen scenario, the 8 troubleshooting steps, remote-access tool comparison).

## Load it

```
python tools/deploy.py tracks/helpdesk-cisco-it-support/01-first-shift_it-customer-support-basics --url http://localhost:8000 --token ctfd_xxx
```

## Challenges

| Category | Challenge | Points | Tags |
|---|---|---|---|
| 01 Orientation (1.1) | Clock In | 50 | CCST 1.1 |
| 01 Orientation (1.1) | Alphabet Soup | 100 | CCST 1.1, Y100200 07.0 |
| 01 Orientation (1.1) | Set in Stone | 100 | CCST 1.1 |
| 01 Orientation (1.1) | KPI Speedrun | 100 | CCST 1.1 |
| 01 Orientation (1.1) | Queue Jumper | 200 | CCST 1.1, Y100200 07.0 |
| 01 Orientation (1.1) | Breach! | 300 | CCST 1.1, Y100200 09.0 |
| 01 Orientation (1.1) | First Contact | 300 | CCST 1.1, Y100200 09.0 |
| 01 Orientation (1.1) | Fast Response | 250 | CCST 1.1, Y100200 09.0 |
| 01 Orientation (1.1) | Same Problem, Different People | 200 | CCST 1.1 |
| 01 Orientation (1.1) | Robot Coworker | 250 | CCST 1.1 |
| 02 Front Line (1.2) | Open or Closed? | 150 | CCST 1.2, Y100200 13.0 |
| 02 Front Line (1.2) | Who's On the Line? | 300 | CCST 1.2, Y100200 13.0 |
| 02 Front Line (1.2) | Hold, Please | 250 | CCST 1.2, Y100200 13.0 |
| 02 Front Line (1.2) | Say It Back | 200 | CCST 1.2, Y100200 13.0 |
| 03 Paper Trail (1.3) | Loose Lips | 200 | CCST 1.2, Y100200 17.0 |
| 03 Paper Trail (1.3) | Just the Facts | 200 | CCST 1.2, Y100200 13.0 |
| 03 Paper Trail (1.3) | Unfinished Business | 250 | CCST 1.2 |
| 03 Paper Trail (1.3) | Deja Vu | 300 | CCST 1.2, Y100200 02.0 |
| 04 Troubleshooting (2.1) | Eight Steps | 200 | CCST 1.3, Y100200 02.0, Y100200 14.0 |
| 04 Troubleshooting (2.1) | One Thing at a Time | 250 | CCST 1.3, Y100200 02.0 |
| 04 Troubleshooting (2.1) | What Changed? | 300 | CCST 1.3, Y100200 02.0, Y100200 14.0 |
| 05 Remote Access (2.2) | Right Tool, Right Job | 250 | CCST 6.1, Y100200 15.0 |
| 05 Remote Access (2.2) | Who Let You In? | 250 | CCST 6.1, Y100200 17.0 |
| 05 Remote Access (2.2) | Close the Door | 250 | CCST 6.1, Y100200 17.0 |
| 06 Research Desk (2.3) | Stop Code Detective | 200 | CCST 6.2, Y100200 03.0 |
| 06 Research Desk (2.3) | Trust but Verify | 300 | CCST 6.2, Y100200 03.0 |
| 06 Research Desk (2.3) | Prompt Check | 250 | CCST 6.2, Y100200 17.0 |
| 06 Research Desk (2.3) | Source Check | 200 | CCST 6.2 |
| 06 Research Desk (2.3) | Check the KB First | 200 | CCST 6.2 |
| 07 App Support (2.4) | Where'd You Get That? | 200 | CCST 4.5, Y100200 05.0 |
| 07 App Support (2.4) | Why Won't It Install? | 250 | CCST 4.5, Y100200 03.0 |
| 07 App Support (2.4) | Mail Call | 250 | CCST 4.5, Y100200 04.0 |
| 08 Boss Ticket | The CFO's Month-End Meltdown (locked until: Queue Jumper, Close the Door, Check the KB First) | 500 | CCST 1.1, CCST 6.1, CCST 6.2, CCST 4.5 |

## Files

- `challenges.json`: challenge text, flags (regex, case-insensitive), hints, tags, attempt limits, unlocks
- `files/`: evidence students download from the challenges
- `facilitator-guide-and-answer-key.pdf`: setup, run-of-show, answer key with explanations
- `build/`: `gen_files.py` (regenerates `files/` and `answers.json` deterministically), `challenges.py` (source of `challenges.json`), `guide.py` (answer key HTML)
