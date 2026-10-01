"""Regenerate each game's README.md from its challenges.json. Run from this folder."""
import json, os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = [
    ("01-first-shift_it-customer-support-basics", "Help Desk: First Shift", "IT Customer Support Basics", "4 h", "1.5-2 h",
     "Students are brand-new Tier 1 techs at **Sawgrass Logistics** (a fictional company). They work a ticket queue and calculate SLA breaches, FCR and response times from a CSV; identify customer types and hold/transfer mistakes in call transcripts; QA ticket notes for confidentiality and missing outcomes; order the 8-step troubleshooting process; audit remote-session logs for missing consent and sessions left open; spot an AI-invented `ipconfig` switch and a privacy-leaking AI prompt; and classify app and email failures.",
     "**The CFO's Month-End Meltdown**: follow the CFO's ticket to the remote-session notes to the error code to the internal KB article's resolution code.",
     "Built directly from the instructor decks' slide content (help desk concepts, ticket fields, KPIs, customer types, the Diego blue-screen scenario, the 8 troubleshooting steps, remote-access tool comparison)."),
    ("02-second-shift_operating-systems-support", "Help Desk: Second Shift", "Operating Systems Support", "10 h", "2-3 h",
     "Promoted to Desktop & Mobile Support. Students work through Win+P display modes, a `powercfg` battery report, failed Windows updates, Task Manager, OneDrive status icons, the UEFI boot order and a UEFI setting that blocks USB booting, Safe Mode keys, macOS tools, cron schedules, Linux permissions, hypervisor types, the mobile MDM wipe policy, hotspot bands, app permissions, mobile mail ports, and IaaS/PaaS/SaaS. It includes a **hands-on Linux pack** (`sawgrass_linux_lab.tar.gz`) with five [VM] challenges: hidden files, `grep -c`, finding a brute-force IP, a mode-000 file, and `chmod +x`.",
     "**The Board Meeting Lockout**: find the CFO's correct BitLocker recovery key by Key ID. Her laptop has two keys, and another laptop has a key ID that looks almost the same.",
     "The Module 1-3 instructor decks for this course contain **slide titles only** (no body text), so challenges are built from the Scope & Sequence topics (1.1-3.7) using standard CCST IT Support / A+ content. Spot-check the answer key against the NetAcad course pages."),
    ("03-third-shift_security-and-connectivity-support", "Help Desk: Third Shift", "Security and Connectivity Support", "10 h", "2.5-3 h",
     "Network & Security Support. Students cover directory services and MFA fixes, the UNC path for a mapped drive, `gpupdate`, account lockouts in a domain controller security log (4625/4740), NTFS permissions, peripherals, Wi-Fi standard compatibility, a PoE power budget, private/public IPv4, IPv6 compression and GUA/LLA, a wrong default gateway, subnet math, APIPA, DHCP DORA, reading `ipconfig /all`, `tracert` and `netstat -ano` output, threat actors, malware, attack categories, a phishing email's real link and sender, social engineering, incident response steps and stakeholders, data classification, MFA factors, non-repudiation, and AUP.",
     "**Patient Zero**: follow the phishing email through the proxy log to the one host that was allowed through, then match the attacker's IP to a PID and the malicious process.",
     "Built directly from the instructor decks. Every answer cites its source slide (`M# S##`) in the answer key."),
    ("04-final-shift_hardware-and-upgrade-support", "Help Desk: Final Shift", "Hardware and Upgrade Support", "6 h", "2-2.5 h",
     "Hardware & Upgrade technician. Students cover ESD voltages and safe practices, Windows and Mac device-information tools, `ifconfig` output, port identification, adapters vs converters, power cables, Device Manager codes, a firmware rollback decision, software layers, upgrade planning, PSU connectors and voltages, CPU socket matching, form factors, M.2 SATA vs NVMe slots, PCIe lanes, a USB 2.0 transfer-time calculation, PSU sizing with headroom, Driver tab options, WHQL, e-waste laws, recycler certifications, and a gap in an asset disposal log.",
     "**The 32 GB Upgrade**: pick the one RAM kit that matches the board's memory type, is on the board maker's QVL, and reaches 32 GB.",
     "Built directly from the instructor decks. Every answer cites its source slide (`M# S##`) in the answer key."),
]

for folder, title, course, cisco_h, ctf_h, story, boss, source in GAMES:
    d = os.path.join(HERE, folder)
    C = json.load(open(os.path.join(d, "challenges.json")))
    cats = OrderedDict()
    for c in C:
        cats.setdefault(c["category"], []).append(c)
    pts = sum(c["value"] for c in C)
    nfiles = len(os.listdir(os.path.join(d, "files")))
    lines = [f"# {title}", "",
             f"**Course:** Cisco NetAcad *{course}* (Cisco estimate: {cisco_h})  ",
             f"**Size:** {len(C)} challenges · {pts:,} points · {len(cats)} categories · {nfiles} evidence files  ",
             f"**Estimated play time:** {ctf_h} (estimate, not yet measured with students)  ",
             "**Tested:** every flag was solved by a test student on CTFd 3.8.6 alongside the other games in this track", "",
             "## Story and skills", "", story, "", "## Boss ticket", "", boss, "", "## Source note", "", source, "",
             "## Load it", "", "```",
             f"python tools/deploy.py tracks/helpdesk-cisco-it-support/{folder} --url http://localhost:8000 --token ctfd_xxx",
             "```", "", "## Challenges", "", "| Category | Challenge | Points | Tags |", "|---|---|---|---|"]
    for cat, items in cats.items():
        for c in items:
            lock = " (locked until: " + ", ".join(c["requires"]) + ")" if c.get("requires") else ""
            lines.append(f"| {cat} | {c['name']}{lock} | {c['value']} | {', '.join(c.get('tags', []))} |")
    lines += ["", "## Files", "",
              "- `challenges.json`: challenge text, flags (regex, case-insensitive), hints, tags, attempt limits, unlocks",
              "- `files/`: evidence students download from the challenges",
              "- `facilitator-guide-and-answer-key.pdf`: setup, run-of-show, answer key with explanations",
              "- `build/`: `gen_files.py` (regenerates `files/` and `answers.json` deterministically), `challenges.py` (source of `challenges.json`), `guide.py` (answer key HTML)", ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(lines))
    print(folder, len(C), pts)
