# Help Desk: Second Shift

**Course:** Cisco NetAcad *Operating Systems Support* (Cisco estimate: 10 h)  
**Size:** 37 challenges · 8,050 points · 10 categories · 16 evidence files  
**Estimated play time:** 2-3 h (estimate, not yet measured with students)  
**Tested:** every flag was solved by a test student on CTFd 3.8.6 alongside the other games in this track

## Story and skills

Promoted to Desktop & Mobile Support. Students work through Win+P display modes, a `powercfg` battery report, failed Windows updates, Task Manager, OneDrive status icons, the UEFI boot order and a UEFI setting that blocks USB booting, Safe Mode keys, macOS tools, cron schedules, Linux permissions, hypervisor types, the mobile MDM wipe policy, hotspot bands, app permissions, mobile mail ports, and IaaS/PaaS/SaaS. It includes a **hands-on Linux pack** (`sawgrass_linux_lab.tar.gz`) with five [VM] challenges: hidden files, `grep -c`, finding a brute-force IP, a mode-000 file, and `chmod +x`.

## Boss ticket

**The Board Meeting Lockout**: find the CFO's correct BitLocker recovery key by Key ID. Her laptop has two keys, and another laptop has a key ID that looks almost the same.

## Source note

The Module 1-3 instructor decks for this course contain **slide titles only** (no body text), so challenges are built from the Scope & Sequence topics (1.1-3.7) using standard CCST IT Support / A+ content. Spot-check the answer key against the NetAcad course pages.

## Load it

```
python tools/deploy.py tracks/helpdesk-cisco-it-support/02-second-shift_operating-systems-support --url http://localhost:8000 --token ctfd_xxx
```

## Challenges

| Category | Challenge | Points | Tags |
|---|---|---|---|
| OS 1A Windows Display, Power & Access (1.1-1.2) | Promoted! | 50 | CCST 4.1 |
| OS 1A Windows Display, Power & Access (1.1-1.2) | Four Ways to Project | 200 | CCST 4.1, Y100200 03.0 |
| OS 1A Windows Display, Power & Access (1.1-1.2) | Battery Health | 250 | CCST 4.1, Y100200 09.0 |
| OS 1A Windows Display, Power & Access (1.1-1.2) | Replace or Keep? (locked until: Battery Health) | 100 | CCST 4.1 |
| OS 1A Windows Display, Power & Access (1.1-1.2) | Access for Everyone | 250 | CCST 4.1, Y100200 03.0 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Patch Tuesday Problems | 200 | CCST 4.1, Y100200 03.0 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Error Code Lookup | 200 | CCST 4.1, CCST 6.2 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Who's Eating the CPU? | 200 | CCST 4.1, Y100200 03.0 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Memory Lane | 150 | CCST 4.1 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Clean Slate | 100 | CCST 4.1, CCST 4.5 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Fly Offline | 250 | CCST 4.1, CCST 4.4 |
| OS 1B Windows Integrity & Backup (1.3-1.4) | Recycle Bin Rescue | 250 | CCST 4.1, CCST 6.2 |
| OS 1C Windows Boot (1.5) | Boot Order | 250 | CCST 4.1, Y100200 03.0 |
| OS 1C Windows Boot (1.5) | Safe Mode, Please | 200 | CCST 4.1 |
| OS 1C Windows Boot (1.5) | USB Won't Boot | 300 | CCST 4.1, Y100200 01.0 |
| OS 2A Linux & macOS Tools (2.1-2.3) | Right Tool (Mac Edition) | 200 | CCST 4.2 |
| OS 2A Linux & macOS Tools (2.1-2.3) | Cron Job Detective | 250 | CCST 4.2, Y100200 03.0 |
| OS 2A Linux & macOS Tools (2.1-2.3) | Hypervisor Sort | 250 | CCST 4.4, Y100200 03.0 |
| OS 2A Linux & macOS Tools (2.1-2.3) | Read the Permissions | 250 | CCST 4.2, Y100200 03.0 |
| OS 2B Linux CLI [VM] (2.4) | Hidden in Plain Sight | 200 | CCST 4.2, Y100200 11.0 |
| OS 2B Linux CLI [VM] (2.4) | Count the Errors | 250 | CCST 4.2, Y100200 11.0 |
| OS 2B Linux CLI [VM] (2.4) | Knock Knock | 350 | CCST 4.2, Y100200 11.0, Y100200 34.0 |
| OS 2B Linux CLI [VM] (2.4) | Permission Denied | 250 | CCST 4.2, Y100200 11.0 |
| OS 2B Linux CLI [VM] (2.4) | Make It Run | 300 | CCST 4.2, Y100200 11.0 |
| OS 2C macOS Troubleshooting (2.5) | Frozen Mac | 100 | CCST 4.2 |
| OS 2C macOS Troubleshooting (2.5) | Drive Swap | 250 | CCST 4.2, Y100200 03.0 |
| OS 3A Mobile Features & Security (3.1-3.3) | Ten Strikes | 150 | CCST 4.3 |
| OS 3A Mobile Features & Security (3.1-3.3) | Lock, Don't Wipe | 250 | CCST 4.3, Y100200 17.0 |
| OS 3A Mobile Features & Security (3.1-3.3) | Pocket Rules | 150 | CCST 4.3 |
| OS 3B Mobile Issues & Apps (3.4-3.6) | Battery Vampire | 200 | CCST 4.3 |
| OS 3B Mobile Issues & Apps (3.4-3.6) | Hotspot Not Found | 300 | CCST 4.3, Y100200 40.0 |
| OS 3B Mobile Issues & Apps (3.4-3.6) | Permission Creep | 150 | CCST 4.3, CCST 4.5 |
| OS 3B Mobile Issues & Apps (3.4-3.6) | Stuck in the Outbox | 250 | CCST 4.3, CCST 4.5, Y100200 32.0 |
| OS 3C The Cloud (3.7) | As a Service | 250 | CCST 4.4, Y100200 15.0 |
| OS 3C The Cloud (3.7) | The Big Three | 100 | CCST 4.4 |
| OS 3C The Cloud (3.7) | Cloud Deployment | 150 | CCST 4.4 |
| OS 4 Boss Ticket | The Board Meeting Lockout (locked until: Safe Mode, Please, Patch Tuesday Problems, Lock, Don't Wipe) | 500 | CCST 4.1, Y100200 42.0 |

## Files

- `challenges.json`: challenge text, flags (regex, case-insensitive), hints, tags, attempt limits, unlocks
- `files/`: evidence students download from the challenges
- `facilitator-guide-and-answer-key.pdf`: setup, run-of-show, answer key with explanations
- `build/`: `gen_files.py` (regenerates `files/` and `answers.json` deterministically), `challenges.py` (source of `challenges.json`), `guide.py` (answer key HTML)
