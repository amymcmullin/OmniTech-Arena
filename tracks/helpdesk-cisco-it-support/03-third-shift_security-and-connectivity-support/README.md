# Help Desk: Third Shift

**Course:** Cisco NetAcad *Security and Connectivity Support* (Cisco estimate: 10 h)  
**Size:** 44 challenges · 9,300 points · 11 categories · 13 evidence files  
**Estimated play time:** 2.5-3 h (estimate, not yet measured with students)  
**Tested:** every flag was solved by a test student on CTFd 3.8.6 alongside the other games in this track

## Story and skills

Network & Security Support. Students cover directory services and MFA fixes, the UNC path for a mapped drive, `gpupdate`, account lockouts in a domain controller security log (4625/4740), NTFS permissions, peripherals, Wi-Fi standard compatibility, a PoE power budget, private/public IPv4, IPv6 compression and GUA/LLA, a wrong default gateway, subnet math, APIPA, DHCP DORA, reading `ipconfig /all`, `tracert` and `netstat -ano` output, threat actors, malware, attack categories, a phishing email's real link and sender, social engineering, incident response steps and stakeholders, data classification, MFA factors, non-repudiation, and AUP.

## Boss ticket

**Patient Zero**: follow the phishing email through the proxy log to the one host that was allowed through, then match the attacker's IP to a PID and the malicious process.

## Source note

Built directly from the instructor decks. Every answer cites its source slide (`M# S##`) in the answer key.

## Load it

```
python tools/deploy.py tracks/helpdesk-cisco-it-support/03-third-shift_security-and-connectivity-support --url http://localhost:8000 --token ctfd_xxx
```

## Challenges

| Category | Challenge | Points | Tags |
|---|---|---|---|
| SC 1A Directory Services & Shared Drives (1.1) | Night Shift | 50 | CCST 3.1 |
| SC 1A Directory Services & Shared Drives (1.1) | Which Directory? | 200 | CCST 3.1 |
| SC 1A Directory Services & Shared Drives (1.1) | MFA Morning | 250 | CCST 3.1, Y100200 41.0 |
| SC 1A Directory Services & Shared Drives (1.1) | Map It Right | 250 | CCST 3.1 |
| SC 1A Directory Services & Shared Drives (1.1) | Policy Refresh | 100 | CCST 3.1 |
| SC 1B Accounts & Permissions (1.2) | Built-in Groups | 100 | CCST 3.1 |
| SC 1B Accounts & Permissions (1.2) | Permission Puzzle | 250 | CCST 3.1, Y100200 48.0 |
| SC 1B Accounts & Permissions (1.2) | Locked Out | 300 | CCST 3.1, Y100200 39.0 |
| SC 1B Accounts & Permissions (1.2) | Right Console | 150 | CCST 3.1 |
| SC 1C Peripherals (1.3) | Stuck Spooler | 150 | CCST 3.2 |
| SC 1C Peripherals (1.3) | Peripheral Triage | 300 | CCST 3.2, Y100200 02.0 |
| SC 1C Peripherals (1.3) | Slow Drive, Fast Port | 100 | CCST 2.3, CCST 3.2 |
| SC 2A Network Types, Wired & Wireless (2.1-2.3) | Network Sizes | 200 | CCST 3.3 |
| SC 2A Network Types, Wired & Wireless (2.1-2.3) | Cable Choice | 200 | CCST 2.3, Y100200 44.0 |
| SC 2A Network Types, Wired & Wireless (2.1-2.3) | Left Behind | 250 | CCST 3.3, Y100200 40.0 |
| SC 2A Network Types, Wired & Wireless (2.1-2.3) | Power Budget | 300 | CCST 3.3, Y100200 09.0 |
| SC 2A Network Types, Wired & Wireless (2.1-2.3) | Wi-Fi 6 | 100 | CCST 3.3 |
| SC 2B IP Addressing & Gateways (2.4-2.5) | Private or Public? | 250 | CCST 3.3, Y100200 04.0 |
| SC 2B IP Addressing & Gateways (2.4-2.5) | Squeeze the IPv6 | 250 | CCST 3.3, Y100200 22.0 |
| SC 2B IP Addressing & Gateways (2.4-2.5) | GUA or LLA? | 200 | CCST 3.3, Y100200 22.0 |
| SC 2B IP Addressing & Gateways (2.4-2.5) | Gateway Gone Wrong | 300 | CCST 3.3, Y100200 18.0 |
| SC 2B IP Addressing & Gateways (2.4-2.5) | Local or Remote? | 300 | CCST 3.3, Y100200 09.0, Y100200 04.0 |
| SC 2C DNS, DHCP & Firewalls (2.6-2.7) | 169.254 Means... | 150 | CCST 3.3 |
| SC 2C DNS, DHCP & Firewalls (2.6-2.7) | DORA | 150 | CCST 3.3 |
| SC 2C DNS, DHCP & Firewalls (2.6-2.7) | Stale Address | 150 | CCST 3.3 |
| SC 2C DNS, DHCP & Firewalls (2.6-2.7) | Let It Through | 150 | CCST 3.3, CCST 5.1 |
| SC 2D Network Commands (2.8) | Read the Config | 200 | CCST 3.3 |
| SC 2D Network Commands (2.8) | Where Does It Break? | 250 | CCST 3.3 |
| SC 2D Network Commands (2.8) | Who's Listening? | 300 | CCST 3.3, CCST 5.1, Y100200 34.0 |
| SC 2D Network Commands (2.8) | Modern Linux | 100 | CCST 3.3 |
| SC 3A Threats, Malware & Attacks (3.1-3.4) | Name That Threat Actor | 250 | CCST 5.1 |
| SC 3A Threats, Malware & Attacks (3.1-3.4) | Malware Lineup | 300 | CCST 5.1, Y100200 34.0 |
| SC 3A Threats, Malware & Attacks (3.1-3.4) | Attack Category | 200 | CCST 5.1, Y100200 34.0 |
| SC 3B Social Engineering (3.5) | Hook, Line & Sinker | 300 | CCST 5.2, Y100200 34.0 |
| SC 3B Social Engineering (3.5) | Return to Sender | 200 | CCST 5.2 |
| SC 3B Social Engineering (3.5) | Social Engineering Bingo | 300 | CCST 5.2 |
| SC 3B Social Engineering (3.5) | Verify, Then Trust | 150 | CCST 5.2 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | Investigation Order | 200 | CCST 5.1 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | Who Do You Call? | 250 | CCST 5.1 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | Sort the Data | 250 | CCST 5.3, Y100200 17.0 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | Know, Have, Are | 150 | CCST 5.3 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | Can't Deny It | 100 | CCST 5.3 |
| SC 3C Incident Response & Protecting Data (3.6-3.7) | The Rulebook | 150 | CCST 5.3, Y100200 47.0 |
| SC 4 Boss Ticket | Patient Zero (locked until: Hook, Line & Sinker, Who's Listening?, Investigation Order) | 500 | CCST 5.1, CCST 3.3, Y100200 34.0 |

## Files

- `challenges.json`: challenge text, flags (regex, case-insensitive), hints, tags, attempt limits, unlocks
- `files/`: evidence students download from the challenges
- `facilitator-guide-and-answer-key.pdf`: setup, run-of-show, answer key with explanations
- `build/`: `gen_files.py` (regenerates `files/` and `answers.json` deterministically), `challenges.py` (source of `challenges.json`), `guide.py` (answer key HTML)
