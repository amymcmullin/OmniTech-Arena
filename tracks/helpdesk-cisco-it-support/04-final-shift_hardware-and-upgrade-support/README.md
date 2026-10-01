# Help Desk: Final Shift

**Course:** Cisco NetAcad *Hardware and Upgrade Support* (Cisco estimate: 6 h)  
**Size:** 39 challenges · 7,700 points · 9 categories · 13 evidence files  
**Estimated play time:** 2-2.5 h (estimate, not yet measured with students)  
**Tested:** every flag was solved by a test student on CTFd 3.8.6 alongside the other games in this track

## Story and skills

Hardware & Upgrade technician. Students cover ESD voltages and safe practices, Windows and Mac device-information tools, `ifconfig` output, port identification, adapters vs converters, power cables, Device Manager codes, a firmware rollback decision, software layers, upgrade planning, PSU connectors and voltages, CPU socket matching, form factors, M.2 SATA vs NVMe slots, PCIe lanes, a USB 2.0 transfer-time calculation, PSU sizing with headroom, Driver tab options, WHQL, e-waste laws, recycler certifications, and a gap in an asset disposal log.

## Boss ticket

**The 32 GB Upgrade**: pick the one RAM kit that matches the board's memory type, is on the board maker's QVL, and reaches 32 GB.

## Source note

Built directly from the instructor decks. Every answer cites its source slide (`M# S##`) in the answer key.

## Load it

```
python tools/deploy.py tracks/helpdesk-cisco-it-support/04-final-shift_hardware-and-upgrade-support --url http://localhost:8000 --token ctfd_xxx
```

## Challenges

| Category | Challenge | Points | Tags |
|---|---|---|---|
| UP 1A Safety & Device Info (1.1-1.2) | Final Shift | 50 | CCST 2.1 |
| UP 1A Safety & Device Info (1.1-1.2) | Feel the Zap | 150 | CCST 2.1, Y100200 24.0 |
| UP 1A Safety & Device Info (1.1-1.2) | Safe or Sorry? | 200 | CCST 2.1, Y100200 24.0 |
| UP 1A Safety & Device Info (1.1-1.2) | Tool Time | 250 | CCST 2.2 |
| UP 1A Safety & Device Info (1.1-1.2) | Run Box Shortcut | 100 | CCST 2.2 |
| UP 1A Safety & Device Info (1.1-1.2) | Mac Address on a Mac | 200 | CCST 2.2 |
| UP 1A Safety & Device Info (1.1-1.2) | Mac Equivalents | 150 | CCST 2.2, CCST 4.2 |
| UP 1A Safety & Device Info (1.1-1.2) | Will It Run? | 300 | CCST 2.2, CCST 4.5 |
| UP 1B Ports & Cables (1.3) | Name That Port | 250 | CCST 2.3 |
| UP 1B Ports & Cables (1.3) | Adapter or Converter? | 200 | CCST 2.3 |
| UP 1B Ports & Cables (1.3) | Big Iron Power | 150 | CCST 2.3 |
| UP 1B Ports & Cables (1.3) | Thunder & Type-C | 150 | CCST 2.3 |
| UP 1C Hardware Issues (1.4) | Dead PC Checklist | 150 | CCST 2.5 |
| UP 1C Hardware Issues (1.4) | Down Arrow | 250 | CCST 2.5, Y100200 03.0 |
| UP 1C Hardware Issues (1.4) | Firmware Flashback | 300 | CCST 2.5 |
| UP 1C Hardware Issues (1.4) | Did You Reboot? | 100 | CCST 2.5 |
| UP 2A Architecture & Compatibility (2.1) | Software Layers | 200 | CCST 2.4 |
| UP 2A Architecture & Compatibility (2.1) | Should Have Planned | 250 | CCST 2.4 |
| UP 2A Architecture & Compatibility (2.1) | Tested and Approved | 100 | CCST 2.4 |
| UP 2B Core Components (2.2) | Plug It In | 250 | CCST 2.4 |
| UP 2B Core Components (2.2) | Twelve Volt Club | 100 | CCST 2.4 |
| UP 2B Core Components (2.2) | Socket Match | 300 | CCST 2.4, Y100200 10.0 |
| UP 2B Core Components (2.2) | Small Box | 150 | CCST 2.4 |
| UP 2B Core Components (2.2) | Wrong Slot | 250 | CCST 2.4, Y100200 10.0 |
| UP 2B Core Components (2.2) | North or South? | 150 | CCST 2.4 |
| UP 2B Core Components (2.2) | Forget Me Not | 100 | CCST 2.4 |
| UP 2C Interfaces & Expansion (2.3) | Lanes for Cards | 200 | CCST 2.4 |
| UP 2C Interfaces & Expansion (2.3) | Speed of a Flash Drive | 250 | CCST 2.3, Y100200 09.0 |
| UP 2C Interfaces & Expansion (2.3) | Size the PSU | 300 | CCST 2.4, Y100200 09.0 |
| UP 2C Interfaces & Expansion (2.3) | Wireless, Two Ways | 150 | CCST 2.4 |
| UP 2C Interfaces & Expansion (2.3) | Integrated vs Discrete | 150 | CCST 2.4 |
| UP 2D Drivers & Device Manager (2.4) | Driver Tab Decisions | 250 | CCST 2.4, Y100200 03.0 |
| UP 2D Drivers & Device Manager (2.4) | Printer Fix | 150 | CCST 2.4, CCST 2.5 |
| UP 2D Drivers & Device Manager (2.4) | WHQL? | 150 | CCST 2.4 |
| UP 2E E-Waste & Disposal (2.5) | Which Law? | 250 | CCST 2.1, Y100200 17.0 |
| UP 2E E-Waste & Disposal (2.5) | Certified Recyclers | 150 | CCST 2.1 |
| UP 2E E-Waste & Disposal (2.5) | Paper Trail Gap | 300 | CCST 2.1, Y100200 17.0, Y100200 46.0 |
| UP 2E E-Waste & Disposal (2.5) | Toxic Trio | 100 | CCST 2.1 |
| UP 3 Boss Ticket | The 32 GB Upgrade (locked until: Will It Run?, Socket Match, Tested and Approved) | 500 | CCST 2.2, CCST 2.4, Y100200 10.0 |

## Files

- `challenges.json`: challenge text, flags (regex, case-insensitive), hints, tags, attempt limits, unlocks
- `files/`: evidence students download from the challenges
- `facilitator-guide-and-answer-key.pdf`: setup, run-of-show, answer key with explanations
- `build/`: `gen_files.py` (regenerates `files/` and `answers.json` deterministically), `challenges.py` (source of `challenges.json`), `guide.py` (answer key HTML)
