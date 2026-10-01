"""Game 3 -- Help Desk: Third Shift (Cisco NetAcad Security and Connectivity Support)."""
import csv, ipaddress, json, os, random
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "files")
os.makedirs(OUT, exist_ok=True)
rng = random.Random(3303)
ANS = {}
def w(name, text):
    with open(os.path.join(OUT, name), "w", newline="\n") as f:
        f.write(text.lstrip("\n"))

# ================================================================ 1.1 MFA tickets (deck S16)
w("mfa_tickets.txt", """
Sawgrass Logistics -- MFA tickets in the queue this morning
=====================================================================
TICKET A  "My Microsoft Authenticator codes keep getting rejected. I set my phone's
           clock myself last week when I was traveling."
TICKET B  "I dropped my phone in the canal. New phone today. How do I sign in?"
TICKET C  "I deleted the authenticator app by accident while cleaning up my phone."
TICKET D  "The setup page shows a QR code but my phone's camera app just opens a
           web page instead of adding the account."

FIXES (from the MFA troubleshooting table)
  1. Make sure "Set Automatically" is turned on for date and time.
  2. Help reset MFA using backup codes or recovery options (may need admin help).
  3. Make sure they're using the correct authenticator app and the camera works.
  4. User must re-register MFA on a new device.
""")
ANS["mfa"] = "1243"

# ================================================================ 1.1 Shared drive mapping
w("map_drive_ticket.txt", r"""
Ticket: "Map Network Drive says 'Windows can't access \\FS01\Acounting. The network
         path was not found.' Everyone else in Accounting has the S: drive."
=====================================================================
C:\> net view \\FS01
Shared resources at \\FS01

Share name     Type  Used as  Comment
-------------------------------------------------------------------------------
Accounting     Disk           Accounting team share (S:)
Dispatch       Disk           Dispatch route plans (R:)
HR-Private     Disk           HR only
Public         Disk           Company-wide read-only
Scans          Disk           Scan-to-folder drop
The command completed successfully.
""")
ANS["unc"] = r"\\FS01\Accounting"

# ================================================================ 1.2 lockouts (event 4625 / 4740)
start = datetime(2026, 9, 30, 7, 40)
rows = []
def ev(t, eid, user, comp, msg):
    rows.append(dict(TimeCreated=t.strftime("%Y-%m-%d %H:%M:%S"), EventID=eid, TargetUser=user, CallerComputer=comp, Message=msg))
for i in range(3):
    ev(start + timedelta(minutes=i), 4625, "gliu", "ACC-PC02", "An account failed to log on. Bad password.")
for i in range(5):
    ev(start + timedelta(minutes=12, seconds=i * 9), 4625, "wturner", "DSP-PC09", "An account failed to log on. Bad password.")
ev(start + timedelta(minutes=12, seconds=50), 4740, "wturner", "DSP-PC09", "A user account was locked out.")
for i in range(2):
    ev(start + timedelta(minutes=20, seconds=i * 30), 4625, "mreyes", "LT-0611", "An account failed to log on. Bad password.")
ev(start + timedelta(minutes=33), 4624, "gliu", "ACC-PC02", "An account was successfully logged on.")
rows.sort(key=lambda r: r["TimeCreated"])
with open(os.path.join(OUT, "dc01_security_log.csv"), "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
ANS["locked_user"] = "wturner"
ANS["locked_pc"] = "DSP-PC09"

# ================================================================ 2.3 Wi-Fi clients (deck S49-50 standards)
w("warehouse_wifi_change.txt", """
Change ticket CHG-0412: Warehouse SSID "Sawgrass-WH" moved to the new APs last night.
New AP radio settings for Sawgrass-WH:  5 GHz only   Network mode: 802.11n/ac/ax mixed
=====================================================================
Device inventory -- devices that use Sawgrass-WH          Wi-Fi standard (spec sheet)
  WH-SCAN-01  handheld scanner (2023)                     802.11ax
  WH-SCAN-02  handheld scanner (2023)                     802.11ax
  WH-PRN-02   label printer (2014)                        802.11b/g
  WH-TAB-05   receiving tablet (2020)                     802.11ac
  WH-LT-03    supervisor laptop (2018)                    802.11n (dual band)
This morning: one device in the list can't see Sawgrass-WH at all.
""")
ANS["wifi_device"] = "WH-PRN-02"

# ================================================================ 2.3 PoE budget
budget = 370
ports = [("Gi1/0/%d" % (i + 1), d, wv) for i, (d, wv) in enumerate(
    [("AP-WH-1", 25.5), ("AP-WH-2", 25.5), ("AP-WH-3", 25.5), ("AP-WH-4", 25.5), ("AP-OFF-1", 25.5), ("AP-OFF-2", 25.5),
     ("CAM-DOCK-1 (PTZ)", 25.5), ("CAM-DOCK-2 (PTZ)", 25.5), ("CAM-YARD-1 (PTZ)", 25.5), ("CAM-YARD-2 (PTZ)", 25.5)]
    + [("PHONE-%02d" % k, 6.5) for k in range(1, 11)]
    + [("KIOSK-LOBBY display", 60.0), ("BADGE-READER-1", 4.0)])]
running, fail = 0.0, None
lines = []
for p, d, wv in ports:
    if fail is None and running + wv > budget:
        fail = (p, d)
        lines.append(f"{p:<10} {d:<22} {wv:>6.1f} W   requested")
        continue
    if fail is None:
        running += wv
    lines.append(f"{p:<10} {d:<22} {wv:>6.1f} W   requested")
w("poe_switch_SW-WH-01.txt", f"""
Switch SW-WH-01 -- PoE port plan (powered up in port order at boot)
Total PoE budget: {budget} W
Ticket: "After we added a couple of new devices, one of them never powers on."
=====================================================================
Port       Device                  Power needed
{chr(10).join(lines)}
""")
ANS["poe_port"] = fail[0]
ANS["poe_device"] = fail[1]
ANS["poe_total_before"] = running

# ================================================================ 2.5 gateway
w("ipconfig_DSP-PC11.txt", """
Ticket: "I can open files on the S: drive, but no websites load and Teams says offline."
C:\\> ipconfig
Windows IP Configuration
Ethernet adapter Ethernet:
   Connection-specific DNS Suffix  . : sawgrass.local
   IPv4 Address. . . . . . . . . . . : 10.20.4.57
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.20.5.1

--- Network documentation (Dispatch VLAN) ---------------------------
   Network ........ 10.20.4.0 /24
   Router (default gateway) interface ... 10.20.4.1
   DHCP scope ..... 10.20.4.50 - 10.20.4.200
   File server FS01 ... 10.20.4.10
""")
ANS["gateway"] = "10.20.4.1"

# ================================================================ 2.6 APIPA
w("ipconfig_FRT-KSK1.txt", """
Ticket: "The lobby kiosk has no internet. Nothing works."
C:\\> ipconfig
Ethernet adapter Ethernet:
   Autoconfiguration IPv4 Address. . : 169.254.88.14
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . :
""")

# ================================================================ 2.8 ipconfig /all
w("ipconfig_all_HR-LT03.txt", """
C:\\> ipconfig /all
Windows IP Configuration
   Host Name . . . . . . . . . . . . : HR-LT03
   Primary Dns Suffix  . . . . . . . : sawgrass.local
Wireless LAN adapter Wi-Fi:
   Description . . . . . . . . . . . : Intel(R) Wi-Fi 6 AX201 160MHz
   Physical Address. . . . . . . . . : 3C-58-C2-9A-17-E4
   DHCP Enabled. . . . . . . . . . . : Yes
   IPv6 Address. . . . . . . . . . . : 2001:db8:acad:20::5c1
   Link-local IPv6 Address . . . . . : fe80::4d1:9b3e:72c0:aa18%12
   IPv4 Address. . . . . . . . . . . : 10.20.8.112(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : Tuesday, September 29, 2026 7:58:12 AM
   Lease Expires . . . . . . . . . . : Wednesday, September 30, 2026 7:58:12 AM
   Default Gateway . . . . . . . . . : 10.20.8.1
   DHCP Server . . . . . . . . . . . : 10.20.1.5
   DNS Servers . . . . . . . . . . . : 10.20.1.10
                                       10.20.1.11
""")
ANS["mac"] = "3C-58-C2-9A-17-E4"
ANS["dhcp_server"] = "10.20.1.5"

w("tracert_output.txt", """
Ticket: "The fleet-tracking portal times out from the Tampa office."
C:\\> tracert fleet.vendor-portal.example
Tracing route to fleet.vendor-portal.example [198.51.100.40]
over a maximum of 30 hops:
  1     1 ms    <1 ms    <1 ms  10.30.0.1
  2     8 ms     7 ms     8 ms  203.0.113.1
  3    11 ms    12 ms    10 ms  203.0.113.65
  4    19 ms    18 ms    21 ms  192.0.2.200
  5     *        *        *     Request timed out.
  6     *        *        *     Request timed out.
  7     *        *        *     Request timed out.
""")
ANS["last_hop"] = "192.0.2.200"

w("netstat_ano_ACC-PC05.txt", """
Ticket: "ACC-PC05 has been really slow and the mouse sometimes moves by itself."
C:\\> netstat -ano
Active Connections
  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       1048
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    10.20.6.31:49702       10.20.4.10:445         ESTABLISHED     4
  TCP    10.20.6.31:49811       52.112.0.14:443        ESTABLISHED     8124
  TCP    10.20.6.31:49830       13.107.42.16:443       ESTABLISHED     6672
  TCP    10.20.6.31:50117       203.0.113.99:4444      ESTABLISHED     7316
  TCP    10.20.6.31:50122       142.250.72.110:443     TIME_WAIT       0
  UDP    0.0.0.0:5353           *:*                                    2236
""")
ANS["bad_pid"] = "7316"

# ================================================================ 3.5 phishing email
w("phish_email.eml", """
Return-Path: <bounce@sawgrass-logistics-support.example>
Received: from mail.sawgrass-logistics-support.example (198.51.100.77)
From: "Sawgrass IT Help Desk" <helpdesk@sawgrass-logistics-support.example>
To: all-staff@sawgrass.example
Subject: URGENT: Your mailbox will be DISABLED in 2 hours
Date: Tue, 29 Sep 2026 06:12:44 -0400
Content-Type: text/html

<p>Dear valued employee,</p>
<p>Our system detected unusual activity. Your mailbox will be <b>permanently disabled
within 2 hours</b> unless you verify your account now.</p>
<p><a href="http://m365-verify-login.example/sawgrass/auth?id=8812">
   https://portal.sawgrass.example/verify</a></p>
<p>Failure to comply will result in loss of all email.</p>
<p>Thank you,<br>IT Help Desk</p>
""")
ANS["phish_domain"] = "m365-verify-login.example"
ANS["phish_sender_domain"] = "sawgrass-logistics-support.example"

# ================================================================ Boss: patient zero
proxy = []
t0 = datetime(2026, 9, 29, 6, 20)
users = [("ACC-PC02", "gliu"), ("WH-PC07", "ochen"), ("DSP-PC03", "wturner"), ("HR-LT03", "ithompson"), ("SLS-LT12", "nbennett")]
noise = ["teams.microsoft.com/", "outlook.office.com/mail/", "fleet.vendor-portal.example/login", "www.weather.example/tampa", "sharepoint.sawgrass.example/sites/hr"]
for i in range(40):
    h, u = rng.choice(users)
    proxy.append([(t0 + timedelta(minutes=i * 3 + rng.randint(0, 2))).strftime("%Y-%m-%d %H:%M:%S"), h, u, "GET", "https://" + rng.choice(noise), "200", "allowed"])
evil = [("06:31:05", "ACC-PC02", "gliu", "http://m365-verify-login.example/sawgrass/auth?id=8812", "403", "blocked-category:phishing"),
        ("06:44:19", "HR-LT03", "ithompson", "http://m365-verify-login.example/sawgrass/auth?id=8812", "403", "blocked-category:phishing"),
        ("07:02:40", "WH-PC07", "ochen", "http://m365-verify-login.example/sawgrass/auth?id=8812", "200", "allowed (category: uncategorized - proxy bypass on WH VLAN)"),
        ("07:02:58", "WH-PC07", "ochen", "http://m365-verify-login.example/dl/MailboxRestore_Tool.exe", "200", "allowed (category: uncategorized - proxy bypass on WH VLAN)")]
for tm, h, u, url, code, act in evil:
    proxy.append(["2026-09-29 " + tm, h, u, "GET", url, code, act])
proxy.sort()
with open(os.path.join(OUT, "proxy_log_2026-09-29.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["time", "host", "user", "method", "url", "status", "action"]); wr.writerows(proxy)

w("WH-PC07_netstat_tasklist.txt", """
Collected by Tier 1 from WH-PC07 at 08:15 (Step 2: Initial Evidence Collection)
=====================================================================
C:\\> netstat -ano
  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       996
  TCP    10.20.9.44:49731       52.112.0.14:443        ESTABLISHED     5520
  TCP    10.20.9.44:49740       10.20.4.10:445         ESTABLISHED     4
  TCP    10.20.9.44:50288       198.51.100.77:8443     ESTABLISHED     9032
  TCP    10.20.9.44:50290       20.190.151.6:443       ESTABLISHED     3388

C:\\> tasklist
Image Name                     PID Session Name        Mem Usage
========================= ======== ================ ============
System                           4 Services              2,104 K
svchost.exe                    996 Services             18,420 K
OneDrive.exe                  3388 Console              96,200 K
ms-teams.exe                  5520 Console             412,880 K
explorer.exe                  6140 Console             141,360 K
MailboxRestore_Tool.exe       9032 Console              22,716 K
WmsClient.exe                 7764 Console              88,104 K
""")
ANS["boss_host"] = "WH-PC07"
ANS["boss_process"] = "MailboxRestore_Tool.exe"

json.dump(ANS, open(os.path.join(HERE, "answers.json"), "w"), indent=2)
print(json.dumps(ANS, indent=2))
