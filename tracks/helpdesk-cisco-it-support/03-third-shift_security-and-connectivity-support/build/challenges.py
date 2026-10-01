"""Game 3 -- Help Desk: Third Shift (Security and Connectivity Support)."""
import json, os, re
A = json.load(open(os.path.join(os.path.dirname(__file__), "answers.json")))
CI = "case_insensitive"
def exact(s): return ("regex", r"^\s*" + re.escape(s) + r"\s*$", CI)
def words(*p): return ("regex", r"^\s*" + r"[\s_-]*".join(re.escape(x) for x in p) + r"s?\s*$", CI)
def letters(s): return ("regex", r"^\s*" + r"[\s,;-]*".join(re.escape(c) for c in s) + r"\s*$", CI)
def number(n): return ("regex", r"^\s*" + re.escape(str(n)) + r"(\.0+)?\s*$", CI)
def seq(*items):
    parts = [re.escape(str(i)) for i in items]
    return ("regex", r"^\s*" + r"\s*[,;\s]\s*".join(parts) + r"\s*$", CI)

CAT = {
    1: "SC 1A Directory Services & Shared Drives (1.1)",
    2: "SC 1B Accounts & Permissions (1.2)",
    3: "SC 1C Peripherals (1.3)",
    4: "SC 2A Network Types, Wired & Wireless (2.1-2.3)",
    5: "SC 2B IP Addressing & Gateways (2.4-2.5)",
    6: "SC 2C DNS, DHCP & Firewalls (2.6-2.7)",
    7: "SC 2D Network Commands (2.8)",
    8: "SC 3A Threats, Malware & Attacks (3.1-3.4)",
    9: "SC 3B Social Engineering (3.5)",
    10: "SC 3C Incident Response & Protecting Data (3.6-3.7)",
    11: "SC 4 Boss Ticket",
}
NOTE = "\n\n*Answers are not case-sensitive.*"
C = []
def ch(name, cat, value, desc, flags, hints=(), files=(), tags=(), max_attempts=0, requires=(), src=""):
    C.append(dict(name=name, category=CAT[cat], value=value, description=desc.strip() + NOTE, flags=list(flags),
                  hints=list(hints), files=list(files), tags=list(tags), max_attempts=max_attempts, requires=list(requires), src=src))

# ============================================================ 1A
ch("Night Shift", 1, 50, """
Sawgrass Logistics has made you a **Network & Security Support** technician. Your tickets now involve accounts, shared drives, printers, Wi-Fi, IP addresses, and attackers.

To clock in, submit:

`third shift`
""", [exact("third shift")], tags=["CCST 3.1"])

ch("Which Directory?", 1, 200, """
Match each organization to the best **directory service**:

- **A.** Local Users and Groups
- **B.** Active Directory
- **C.** Entra ID
- **D.** AWS IAM

1. A cloud-first startup that runs everything in Microsoft 365.
2. A development team that needs controlled access to Amazon S3 buckets.
3. A single standalone kiosk PC in the lobby that isn't joined to any domain.
4. A company with on-premises Windows servers and a traditional enterprise domain.

Enter the letters for 1 through 4 in order (example: `DCBA`).
""", [letters("CDAB")], tags=["CCST 3.1"], max_attempts=4, src="M1 S13-14 directory services comparison table")

ch("MFA Morning", 1, 250, """
Open **mfa_tickets.txt**. Four users have multi-factor authentication problems.

Match tickets **A, B, C, D** to the fix numbers listed in the file. Enter the four fix numbers in ticket order (example: `4321`).
""", [letters(A["mfa"])], hints=[("Ticket A's phone clock was set by hand.", 0)],
   files=["mfa_tickets.txt"], tags=["CCST 3.1", "Y100200 41.0"], max_attempts=4, src="M1 S16 MFA problem/solution table")

ch("Map It Right", 1, 250, """
Open **map_drive_ticket.txt**.

The user typed the wrong share path into **Map Network Drive**. Using the `net view` output, enter the **correct UNC path** for the Accounting share (example format: `\\\\SERVER\\Share`).
""", [("regex", r"^\s*\\\\fs01\\accounting\\?\s*$", CI)], hints=[("Compare what the user typed with the share names, letter by letter.", 0)],
   files=["map_drive_ticket.txt"], tags=["CCST 3.1"], max_attempts=4, src="M1 S20 mapping a shared drive")

ch("Policy Refresh", 1, 100, """
An admin just changed a **Group Policy Object (GPO)** that maps the S: drive. The user doesn't want to wait or reboot.

Which Windows **command** re-applies the GPOs to the computer and the signed-in user? (Bonus points in real life if you add the switch that forces a full refresh.)
""", [("regex", r"^\s*gpupdate(\.exe)?(\s+/force)?\s*$", CI)], tags=["CCST 3.1"], max_attempts=4, src="M1 S21 Force a Group Policy update")

# ============================================================ 1B
ch("Built-in Groups", 2, 100, """
Which default Windows group gets a **temporary profile** that's created at logon and **deleted at logoff**, and is **disabled by default**?
""", [words("guest"), words("guest", "account")], tags=["CCST 3.1"], max_attempts=3, src="M1 S24 Users and Groups")

ch("Permission Puzzle", 2, 250, """
Match each request to the **least** Windows NTFS permission that meets it:

- **A.** Full Control
- **B.** Modify
- **C.** Read and Execute
- **D.** List Folder Contents
- **E.** Read
- **F.** Write

1. A clerk needs to open, edit, and **delete** invoices, but must **not** change who has access.
2. A department lead must be able to **change permissions** and **take ownership** of the folder.
3. Drivers need to **run** the route-planning program stored in the folder.
4. Auditors only need to **see the names** of the files in the folder, not open them.

Enter the letters for 1 through 4 in order.
""", [letters("BACD")], tags=["CCST 3.1", "Y100200 48.0"], max_attempts=4, src="M1 S25 Windows permission types table")

ch("Locked Out", 2, 300, """
Open **dc01_security_log.csv**, an export from the domain controller's Security log.

Event **4625** is a failed logon. Event **4740** means **a user account was locked out**.

Which **user account** was locked out, and from which **computer** were the bad passwords coming? Enter `username,computer` (example: `jdoe,PC-01`).
""", [seq(A["locked_user"], A["locked_pc"])],
   hints=[("Filter the EventID column to 4740.", 0)], files=["dc01_security_log.csv"],
   tags=["CCST 3.1", "Y100200 39.0"], max_attempts=4, src="M1 S30 AD account lockouts")

ch("Right Console", 2, 150, """
To reset a **domain** user's password, you open **Active Directory Users and Computers (ADUC)**. What do you type in the **Run** box to open it directly? (It ends in `.msc`.)
""", [("regex", r"^\s*dsa(\.msc)?\s*$", CI)], hints=[("Local Users and Groups is lusrmgr.msc. ADUC's short name has three letters.", 0)],
   tags=["CCST 3.1"], max_attempts=3, src="M1 S29 + New Terms (Dsa.msc, Lusrmgr.msc)")

# ============================================================ 1C
ch("Stuck Spooler", 3, 150, """
Print jobs are stuck in the queue and new ones won't print. Canceling them did nothing.

Which Windows **service** do you restart in `services.msc`?
""", [words("print", "spooler"), words("spooler")], tags=["CCST 3.2"], max_attempts=3, src="M1 S36 clearing the print queue")

ch("Peripheral Triage", 3, 300, """
Match each symptom to its **most likely cause**:

- **A.** Only the HDMI cable is connected, not the USB cable
- **B.** Reflective or uneven surface under the device
- **C.** The wrong keyboard layout is selected in Windows
- **D.** The app doesn't have microphone permission
- **E.** Mechanical failure. Stop using it immediately.
- **F.** The fax is plugged into the wrong port. It needs the **LINE** port.

1. The external hard drive is making clicking noises.
2. Typing `@` produces `"` instead.
3. The fax machine has no dial tone, but a phone plugged into the same wall jack works.
4. The interactive flat panel shows the presentation, but tapping does nothing.
5. The microphone works in Sound settings but not in Teams.
6. The mouse cursor jumps around on a glass desk.

Enter six letters in order.
""", [letters("ECFADB")], tags=["CCST 3.2", "Y100200 02.0"], max_attempts=4, src="M1 S41, S52, S56, S58, S60, S69 problem/solution tables")

ch("Slow Drive, Fast Port", 3, 100, """
A user's external drive copies files very slowly. You suspect it's plugged into a USB 2.0 port.

Besides an **SS** logo, what **color** is the plastic inside a USB 3.0 port usually?
""", [exact("blue")], tags=["CCST 2.3", "CCST 3.2"], max_attempts=2, src="M1 S67 external drive slow")

# ============================================================ 2A
ch("Network Sizes", 4, 200, """
Match each network to its type:

- **A.** PAN
- **B.** LAN
- **C.** WLAN
- **D.** WMN
- **E.** MAN
- **F.** WAN

1. Sawgrass connecting its Immokalee, Tampa, and Atlanta offices through a service provider.
2. Earbuds and a smartwatch connected to a driver's phone over Bluetooth.
3. Several access points working together to blanket the warehouse yard.
4. Office PCs plugged into a switch with Ethernet cables on one floor.
5. A network linking all of the city's public library branches across town.
6. Laptops connecting wirelessly in the break room.

Enter six letters in order.
""", [letters("FADBEC")], tags=["CCST 3.3"], max_attempts=4, src="M2 S30-35 network diagrams")

ch("Cable Choice", 4, 200, """
Pick the best cable for each run:

- **U** = unshielded twisted-pair (UTP)
- **S** = shielded twisted-pair (STP)
- **F** = fiber-optic

1. A normal office desk to the wall jack.
2. A run alongside heavy motors and welders on the shop floor (lots of EMI). It must stay copper.
3. A link between two buildings where you need complete immunity to EMI and RFI.

Enter three letters in order (example: `FSU`).
""", [letters("USF")], tags=["CCST 2.3", "Y100200 44.0"], max_attempts=3, src="M2 S41-44 Ethernet cabling")

ch("Left Behind", 4, 250, """
Open **warehouse_wifi_change.txt**.

Last night the warehouse SSID moved to new APs. One device now can't see the network at all. Which **device**?
""", [exact(A["wifi_device"])], hints=[("Check which frequency band each 802.11 standard uses. The new SSID is 5 GHz only.", 0)],
   files=["warehouse_wifi_change.txt"], tags=["CCST 3.3", "Y100200 40.0"], max_attempts=3, src="M2 S49-50 802.11 standards table, S59 compatibility issues")

ch("Power Budget", 4, 300, """
Open **poe_switch_SW-WH-01.txt**. The switch powers its PoE devices up in port order until the budget runs out.

Which **port** has the device that never powers on? (Example format: `Gi1/0/5`)
""", [("regex", r"^\s*(gi(gabitethernet)?\s*)?1/0/21\s*$", CI)],
   hints=[("Add up the watts port by port. Stop when the next device would push the total over the budget.", 0)],
   files=["poe_switch_SW-WH-01.txt"], tags=["CCST 3.3", "Y100200 09.0"], max_attempts=4, src="M2 S59 PoE power issues")

ch("Wi-Fi 6", 4, 100, """
Which IEEE 802.11 standard is also known as **Wi-Fi 6** (High-Efficiency Wireless)? (Example format: `802.11x`)
""", [("regex", r"^\s*(ieee\s*)?802\.11\s*ax\s*$", CI)], tags=["CCST 3.3"], max_attempts=3, src="M2 S50")

# ============================================================ 2B
ch("Private or Public?", 5, 250, """
Which of these IPv4 addresses are **public**, meaning they can be routed on the internet?

- **A.** 10.44.2.9
- **B.** 172.20.1.5
- **C.** 172.32.0.9
- **D.** 192.168.50.7
- **E.** 8.8.8.8
- **F.** 169.254.10.3

Enter the letters of the public addresses in alphabetical order (example: `AB`).
""", [letters("CE")], hints=[("The private ranges are 10.0.0.0/8, 172.16.0.0 to 172.31.255.255, and 192.168.0.0/16. 169.254 is APIPA, which is local only.", 0)],
   tags=["CCST 3.3", "Y100200 04.0"], max_attempts=3, src="M2 S73 private IPv4 table, S91 APIPA")

ch("Squeeze the IPv6", 5, 250, """
Compress this IPv6 address using **both** rules (omit leading zeros, and replace consecutive all-zero hextets with `::`):

`2001:0DB8:0000:0000:00A0:0000:0000:0001`

Both zero runs are the same length, so put the `::` on the **first** one, which is the standard convention.
""", [("regex", r"^\s*2001:db8::a0:0:0:1\s*$", CI), ("regex", r"^\s*2001:db8:0:0:a0::1\s*$", CI)],
   hints=[("`::` can be used only once in an address.", 0)], tags=["CCST 3.3", "Y100200 22.0"], max_attempts=4, src="M2 S68-69 IPv6 compression rules")

ch("GUA or LLA?", 5, 200, """
Classify each IPv6 address:

- **G** = Global Unicast Address (GUA)
- **L** = Link-Local Address (LLA)
- **B** = Loopback

1. `fe80::4d1:9b3e:72c0:aa18`
2. `2001:db8:acad:20::5c1`
3. `::1`
4. `fe80::1`
5. `3001:4a2b::10`

Enter five letters in order.
""", [letters("LGBLG")], tags=["CCST 3.3", "Y100200 22.0"], max_attempts=3, src="M2 S78-79 GUA starts with 2 or 3, LLA fe80::/10; S83 loopback ::1")

ch("Gateway Gone Wrong", 5, 300, """
Open **ipconfig_DSP-PC11.txt**.

The user can reach the file server on the **same network** but can't reach the **internet**. Compare the PC's settings with the network documentation.

What should the **default gateway** be?
""", [exact(A["gateway"])], files=["ipconfig_DSP-PC11.txt"], tags=["CCST 3.3", "Y100200 18.0"], max_attempts=3,
   src="M2 S85-87 default gateway and troubleshooting")

ch("Local or Remote?", 5, 300, """
A PC is configured as **192.168.10.37/26** (subnet mask 255.255.255.192).

Which **one** of these destinations is on a **different** network, so the PC must send it to the default gateway?

- 192.168.10.1
- 192.168.10.62
- 192.168.10.70
- 192.168.10.45
""", [exact("192.168.10.70")], hints=[("A /26 makes blocks of 64 addresses: .0 to .63, .64 to .127, and so on.", 25)],
   tags=["CCST 3.3", "Y100200 09.0", "Y100200 04.0"], max_attempts=2, src="M2 S66, S84 host forwarding decision with subnet mask")

# ============================================================ 2C
ch("169.254 Means...", 6, 150, """
Open **ipconfig_FRT-KSK1.txt**.

The kiosk has a **169.254.x.x** address and no default gateway. Which network **service** did the kiosk fail to reach? (Four letters.)
""", [exact("DHCP"), words("dhcp", "server")], files=["ipconfig_FRT-KSK1.txt"], tags=["CCST 3.3"], max_attempts=2, src="M2 S91-92 APIPA")

ch("DORA", 6, 150, """
Put the DHCPv4 lease messages in order:

- **A.** DHCPREQUEST
- **B.** DHCPACK
- **C.** DHCPDISCOVER
- **D.** DHCPOFFER

Enter four letters.
""", [letters("CDAB")], tags=["CCST 3.3"], max_attempts=3, src="M2 S94 + New Terms")

ch("Stale Address", 6, 150, """
The vendor portal moved to a new server. Running `nslookup` shows the **new** IP, but the user's PC keeps trying the **old** one.

Which **command** clears the Windows DNS cache?
""", [("regex", r"^\s*ipconfig\s+/flushdns\s*$", CI)], tags=["CCST 3.3"], max_attempts=3, src="M2 S90 DNS caching/TTL, S110")

ch("Let It Through", 6, 150, """
A line-of-business app can't reach its server because **Windows Defender Firewall** blocks it. You want to allow **only that app**, not turn the firewall off.

In Windows Defender Firewall, which link do you choose? Complete it: **"Allow an app or feature through ________"**.
""", [("regex", r"^\s*(the\s+)?(windows\s+)?(defender\s+)?firewall\s*$", CI)], tags=["CCST 3.3", "CCST 5.1"], max_attempts=3, src="M2 S104 configuring exceptions")

# ============================================================ 2D
ch("Read the Config", 7, 200, """
Open **ipconfig_all_HR-LT03.txt**.

1. What is the laptop's **MAC (physical) address**?
2. Which **DHCP server** gave it its address?

Enter `MAC,DHCPserver` (example: `00-11-22-33-44-55,10.0.0.1`).
""", [("regex", r"^\s*3c[-:]58[-:]c2[-:]9a[-:]17[-:]e4\s*[,;\s]\s*10\.20\.1\.5\s*$", CI)],
   files=["ipconfig_all_HR-LT03.txt"], tags=["CCST 3.3"], max_attempts=4, src="M2 S108 ipconfig")

ch("Where Does It Break?", 7, 250, """
Open **tracert_output.txt**.

What is the IP address of the **last router that responded** before the trace starts timing out?
""", [exact(A["last_hop"])], files=["tracert_output.txt"], tags=["CCST 3.3"], max_attempts=3, src="M2 S112 traceroute/tracert")

ch("Who's Listening?", 7, 300, """
Open **netstat_ano_ACC-PC05.txt**. The user says the PC is slow and the mouse sometimes moves by itself, which can be a sign of a **remote-access Trojan**.

One **ESTABLISHED** connection goes to an unusual outside port that isn't web traffic (443). What is the **PID** of the process that owns it?
""", [number(A["bad_pid"])], hints=[("Port 4444 is a common default for remote-control tools used by attackers.", 25)],
   files=["netstat_ano_ACC-PC05.txt"], tags=["CCST 3.3", "CCST 5.1", "Y100200 34.0"], max_attempts=3, src="M2 S116-118 netstat; M3 S33 remote-access Trojan")

ch("Modern Linux", 7, 100, """
On modern Linux, the **iproute2** suite replaces older tools. Which short command is the modern replacement for **netstat**?
""", [exact("ss")], tags=["CCST 3.3"], max_attempts=3, src="M2 S120 iproute2")

# ============================================================ 3A
ch("Name That Threat Actor", 8, 250, """
Match each case to the type of threat actor:

- **A.** Script kiddie
- **B.** Hacktivist
- **C.** State-sponsored
- **D.** Insider
- **E.** Ethical hacker
- **F.** Cyber criminal

1. A teenager runs a downloaded attack tool against the company website "just to see what happens."
2. A former contractor whose VPN account was never disabled copies customer lists.
3. A group defaces the website to protest the company's new truck yard near a wetland.
4. A hired penetration tester breaks into the warehouse Wi-Fi and reports how she did it.
5. A crew sells stolen driver payroll data and banking Trojans on underground markets.
6. A foreign government's team quietly steals logistics plans for military shipments.

Enter six letters in order.
""", [letters("ADBEFC")], tags=["CCST 5.1"], max_attempts=4, src="M3 S26-27 types of hackers")

ch("Malware Lineup", 8, 300, """
Match each symptom to the malware type:

- **A.** Ransomware
- **B.** Adware
- **C.** Rootkit
- **D.** Spyware
- **E.** Keylogger Trojan
- **F.** Macro virus

1. Antivirus finds nothing, but an attacker has hidden admin-level access and a backdoor.
2. All files on the shared drive now end in `.locked`, and a note demands Bitcoin.
3. Someone's typed credit card numbers are being recorded as they type them into a web form.
4. Pop-up ads keep appearing after the user installed a "free PDF converter."
5. A Word document's built-in automation infects other documents when it's opened.
6. Browsing history is quietly being sent to an unknown server without the user knowing.

Enter six letters in order.
""", [letters("CAEBFD")], tags=["CCST 5.1", "Y100200 34.0"], max_attempts=4, src="M3 S32-34 virus, Trojan, and other malware tables")

ch("Attack Category", 8, 200, """
Classify each event:

- **R** = Reconnaissance
- **A** = Access attack
- **S** = Social engineering
- **D** = Denial of service

1. A ping sweep of 10.20.0.0/16 from an unknown host.
2. Thousands of password guesses against the FTP server (brute force).
3. Someone follows an employee through the badge door without scanning in.
4. A botnet floods the customer portal until it stops responding.
5. A port scan of the active IP addresses found earlier.

Enter five letters in order.
""", [letters("RASDR")], tags=["CCST 5.1", "Y100200 34.0"], max_attempts=3, src="M3 S36-49 network attack categories")

# ============================================================ 3B
ch("Hook, Line & Sinker", 9, 300, """
Open **phish_email.eml**. Hovering over a link reveals where it really goes.

The link **text** says `https://portal.sawgrass.example/verify`. What **domain** does the link actually point to?
""", [exact(A["phish_domain"])], hints=[("Look at the `href=` part of the `<a>` tag, not the text shown to the reader.", 0)],
   files=["phish_email.eml"], tags=["CCST 5.2", "Y100200 34.0"], max_attempts=3, src="M3 S53 hover over links")

ch("Return to Sender", 9, 200, """
Using **phish_email.eml** again: which **sender domain** is the email really from? (Sawgrass's real domain is `sawgrass.example`.)
""", [exact(A["phish_sender_domain"])], files=["phish_email.eml"], tags=["CCST 5.2"], max_attempts=3,
   src="M3 S52-54 red flags, double-check email sources")

ch("Social Engineering Bingo", 9, 300, """
Match each situation to the attack:

- **A.** Baiting
- **B.** Tailgating
- **C.** Shoulder surfing
- **D.** Dumpster diving
- **E.** Smishing
- **F.** Something for something (quid pro quo)
- **G.** Vishing

1. A USB drive labeled "Q4 Layoffs" is left in the parking lot.
2. A text message says a package is held and asks you to "confirm your address" at a link.
3. Someone in the airport lounge watches a sales rep type her VPN password.
4. A stranger digs through the recycling bins behind accounting.
5. A caller offers a free gift card for "completing a short survey" that asks for your employee ID.
6. A "delivery driver" with full arms slips in behind an employee at the secure door.
7. A caller claiming to be from the bank's fraud team asks you to read back a one-time code.

Enter seven letters in order.
""", [letters("AECDFBG")], tags=["CCST 5.2"], max_attempts=4, src="M3 S42-44 social engineering tables")

ch("Verify, Then Trust", 9, 150, """
A caller says he's the CFO, he's at the airport, his MFA phone is broken, and he needs MFA reset to a new number **right now** or "heads will roll."

According to the course, which of these is the **right** response?

- **A.** Reset it. He's an executive and it's urgent.
- **B.** Verify his identity independently, for example by calling back on the number in the company directory and getting manager approval, before changing anything.
- **C.** Ask him to email you his password so you can confirm it's him.
- **D.** Hang up without saying anything.

Enter one letter. **You have 1 attempt.**
""", [exact("B")], tags=["CCST 5.2"], max_attempts=1, src="M3 S51 'Amelia Answers an Urgent Call'")

# ============================================================ 3C
ch("Investigation Order", 10, 200, """
Put the steps for investigating a possible security incident in order:

- **A.** Log analysis
- **B.** Documentation and reporting
- **C.** Symptom identification
- **D.** Preliminary diagnosis
- **E.** Initial evidence collection

Enter five letters in order.
""", [letters("CEADB")], tags=["CCST 5.1"], max_attempts=3, src="M3 S60-61 investigating the incident")

ch("Who Do You Call?", 10, 250, """
Match each incident detail to the stakeholder you'd bring in:

- **A.** Physical Security and Facilities
- **B.** Human Resources
- **C.** Public Affairs and Media Relations
- **D.** Legal Department
- **E.** Information Assurance

1. Firewall rules need to change during containment.
2. The attacker got in by tailgating through the dock door.
3. Someone must check that the incident plan follows federal guidelines.
4. The investigation shows an employee caused the breach on purpose.
5. Customers' personal information was exposed and they must be told.

Enter five letters in order.
""", [letters("EADBC")], tags=["CCST 5.1"], max_attempts=3, src="M3 S58-59 incident response stakeholders")

ch("Sort the Data", 10, 250, """
Classify each item:

- **C** = Confidential
- **P** = Proprietary
- **I** = PII
- **F** = Financial and payment
- **H** = Health/PHI
- **L** = Legal and regulatory

1. The route-optimization algorithm's source code.
2. A driver's name, home address, and Social Security number.
3. Next year's expansion strategy presented to the board.
4. Payroll records and corporate credit card numbers.
5. An employee's workers' comp medical records.
6. Contracts and documents from a pending lawsuit.

Enter six letters in order.
""", [letters("PICFHL")], tags=["CCST 5.3", "Y100200 17.0"], max_attempts=4, src="M3 S70 categories of sensitive data")

ch("Know, Have, Are", 10, 150, """
Classify each MFA factor:

- **K** = Something you know
- **H** = Something you have
- **A** = Something you are

1. A YubiKey hardware security key
2. A 6-digit PIN
3. A fingerprint
4. A code from Microsoft Authenticator on your phone
5. Face recognition

Enter five letters in order.
""", [letters("HKAHA")], tags=["CCST 5.3"], max_attempts=3, src="M3 S67-68 MFA factors")

ch("Can't Deny It", 10, 100, """
A user claims she never approved a $40,000 vendor payment, but the system logs and her digital signature prove she did.

What **security concept** means a person can't deny an action they took? (One hyphenated word.)
""", [("regex", r"^\s*non[\s-]?repudiation\s*$", CI)], tags=["CCST 5.3"], max_attempts=3, src="M3 S72-73 non-repudiation")

ch("The Rulebook", 10, 150, """
Which company policy spells out how employees may and may not use company devices, networks, and resources? Give its full name or its three-letter abbreviation.
""", [("regex", r"^\s*(acceptable\s+use\s+policy|aup)\s*$", CI)], tags=["CCST 5.3", "Y100200 47.0"], max_attempts=3, src="M3 S71 company policies")

# ============================================================ Boss
ch("Patient Zero", 11, 500, """
**Security incident, 08:30.** The phishing email in **phish_email.eml** went to all staff. The web proxy blocks the phishing site, so most clicks were stopped. Security thinks **one** PC was compromised anyway.

Follow the evidence:

1. **proxy_log_2026-09-29.csv**: who visited the phishing domain, and whose request was actually **allowed**, including a file download?
2. **WH-PC07_netstat_tasklist.txt**: the evidence Tier 1 collected from that PC. Find the connection to the attacker's mail server IP (it's in the email headers), then match its PID to a process.

Enter the **name of the malicious process** (example format: `something.exe`).
""", [exact(A["boss_process"]), exact(A["boss_process"].replace(".exe", ""))],
   hints=[("Only one host has status 200 for the phishing domain. Everyone else was blocked (403).", 0),
          ("The Received: header shows 198.51.100.77. Find that IP in netstat, then look up its PID in tasklist.", 100)],
   files=["phish_email.eml", "proxy_log_2026-09-29.csv", "WH-PC07_netstat_tasklist.txt"],
   tags=["CCST 5.1", "CCST 3.3", "Y100200 34.0"], max_attempts=3,
   requires=["Hook, Line & Sinker", "Who's Listening?", "Investigation Order"],
   src="M3 S60-61 investigation steps, M2 S116 netstat, M3 S53 links")

if __name__ == "__main__":
    print(len(C), "challenges,", sum(c["value"] for c in C), "points")
