# Track: Help Desk / Cisco IT Support

Four CTF games that follow the **Cisco Networking Academy IT Support Specialist career path**, which prepares students for the **Cisco Certified Support Technician (CCST) IT Support** certification. Each game matches one course in the path. Students play a technician at **Sawgrass Logistics** (a fictional company) who is promoted shift by shift, from Tier 1 help desk to hardware and upgrade support.

| # | Game | Cisco course | Prefix | Challenges | Points | Cisco course time | Est. game time |
|---|---|---|---|---|---|---|---|
| 1 | [First Shift](01-first-shift_it-customer-support-basics/) | IT Customer Support Basics | `01`–`08` | 33 | 7,550 | 4 h | 1.5–2 h |
| 2 | [Second Shift](02-second-shift_operating-systems-support/) | Operating Systems Support | `OS` | 37 | 8,050 | 10 h | 2–3 h |
| 3 | [Third Shift](03-third-shift_security-and-connectivity-support/) | Security and Connectivity Support | `SC` | 44 | 9,300 | 10 h | 2.5–3 h |
| 4 | [Final Shift](04-final-shift_hardware-and-upgrade-support/) | Hardware and Upgrade Support | `UP` | 39 | 7,700 | 6 h | 2–2.5 h |
| | **Total** | | | **153** | **32,600** | **30 h** | **≈ 8–11 h** |

Courses plus games together come to about **38–41 hours**. That's roughly 1 to 1.5 weeks for a full-time student, or 3–5 weeks at a couple of hours a day. The game times are estimates, not yet measured with students, and self-paced students will vary a lot (fast students take about half the time, students new to spreadsheets or the command line up to about 1.5×).

## Alignment

- **CCST IT Support objectives.** Every challenge is tagged in CTFd: 1.1–1.3 (help desk, documentation, problem solving), 2.1–2.5 (safety, device info, ports and cables, components, hardware issues), 3.1–3.3 (network resources, peripherals, connectivity), 4.1–4.5 (Windows, macOS, mobile, virtualization/cloud, applications), 5.1–5.3 (threats, social engineering, data protection), and 6.1–6.2 (remote access, research tools).
- **Florida CTE program Y100200 (Computer Systems & Information Technology).** Where a challenge fits a standard, it carries a matching tag, for example `Y100200 02.0` troubleshooting, `09.0` math, `13.0` communication, `17.0` ethics/legal, `22.0` IPv6, `34.0` attacks, `40.0` wireless.

## How it's used

- All four games stay **open all year** on one CTFd server. Students start each game after finishing the matching Canvas/NetAcad course, in any order.
- Each game has one **boss ticket** that unlocks after three related challenges and chains several evidence files together.
- Game 2 includes a **Linux lab pack** that must be extracted *inside* a Linux VM (topic 2.3) so file permissions survive.
- Setup, student import, and board settings are in [docs/platform-setup.md](../../docs/platform-setup.md).

## Load all four games

```
python tools/deploy.py tracks/helpdesk-cisco-it-support/01-first-shift_it-customer-support-basics      --url http://localhost:8000 --token ctfd_xxx
python tools/deploy.py tracks/helpdesk-cisco-it-support/02-second-shift_operating-systems-support      --url http://localhost:8000 --token ctfd_xxx
python tools/deploy.py tracks/helpdesk-cisco-it-support/03-third-shift_security-and-connectivity-support --url http://localhost:8000 --token ctfd_xxx
python tools/deploy.py tracks/helpdesk-cisco-it-support/04-final-shift_hardware-and-upgrade-support    --url http://localhost:8000 --token ctfd_xxx
```

## Other files in this folder

- `templates/student_import_template.csv`: format for bulk-importing students (fictional example rows).
- `build_readmes.py`: regenerates each game's README from its `challenges.json`.

## Credits

Game design and evidence files were created for iTECH's Computer Systems & IT program. The Cisco course names, topics, and CCST objectives belong to Cisco Systems. No Cisco course materials are included in this repository; answer keys only cite module and slide numbers.
