"""Game 2 -- Help Desk: Second Shift (Cisco NetAcad Operating Systems Support). Evidence files + answers."""
import csv, io, json, os, random, tarfile, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "files")
os.makedirs(OUT, exist_ok=True)
rng = random.Random(4242)
ANS = {}
CO = "Sawgrass Logistics"

def w(name, text):
    with open(os.path.join(OUT, name), "w", newline="\n") as f:
        f.write(text.lstrip("\n"))

# ======================================================================= 1.1 power
design, full = 56004, 39203
w("battery_report_LT-0519.txt", f"""
Battery report  (output of: powercfg /batteryreport)            Computer: LT-0519
Report time: 2026-09-29 10:14   OS build: 26100 (fictional)
=====================================================================
INSTALLED BATTERIES
  NAME                    DELL 7FHHV
  MANUFACTURER            SMP
  CHEMISTRY               LiP
  DESIGN CAPACITY         {design:,} mWh
  FULL CHARGE CAPACITY    {full:,} mWh
  CYCLE COUNT             812

RECENT USAGE (last 3 sessions)
  2026-09-28 08:02  Active   Battery  100%  ->  2026-09-28 09:41  Active  Battery  9%
  2026-09-27 08:10  Active   Battery  100%  ->  2026-09-27 09:52  Active  Battery  7%
  2026-09-26 07:58  Active   Battery  100%  ->  2026-09-26 09:30  Active  Battery  11%

Company policy: replace a laptop battery when it holds LESS THAN 75% of its
design capacity.
""")
ANS["battery_pct"] = round(full / design * 100)          # 70

# ======================================================================= 1.3 BitLocker etc.
w("update_history_ACC-PC09.txt", """
Settings > Windows Update > Update history     Device: ACC-PC09
(KB numbers are fictional for this exercise)
=====================================================================
Quality Updates
  2026-09 Cumulative Update for Windows 11 (KB5099120)
        Successfully installed on 9/24/2026
  2026-09 Cumulative Update for .NET Framework (KB5098871)
        Successfully installed on 9/24/2026
  2026-09 Security Update for Windows 11 (KB5099347)
        Failed to install on 9/26/2026 - 0x800f0922
  2026-09 Security Update for Windows 11 (KB5099347)
        Failed to install on 9/27/2026 - 0x800f0922
  2026-08 Cumulative Update for Windows 11 (KB5097702)
        Successfully installed on 8/27/2026
Driver Updates
  Realtek - Audio - 6.0.9768.1   Successfully installed on 9/20/2026
  Intel - Display - 32.0.101.6078 Successfully installed on 9/20/2026
Definition Updates
  Security Intelligence Update for Microsoft Defender Antivirus - KB2267602
        Successfully installed on 9/29/2026
""")
ANS["failed_kb"] = "KB5099347"

w("task_manager_DSP-PC04.txt", """
Task Manager > Processes   (sorted by Name)   Device: DSP-PC04
User complaint: "Everything is slow since I copied the old shared drive into OneDrive."
=====================================================================
Name                               CPU      Memory      Disk         Network
-----------------------------------------------------------------------------
Antimalware Service Executable     2.1%     188.4 MB    0.1 MB/s     0 Mbps
Desktop Window Manager             1.3%     96.7 MB     0 MB/s       0 Mbps
Microsoft Edge (14)                3.8%     1,412.6 MB  0.2 MB/s     0.4 Mbps
Microsoft Excel                    0.4%     312.9 MB    0 MB/s       0 Mbps
Microsoft OneDrive                 61.7%    842.3 MB    38.4 MB/s    41.8 Mbps
Microsoft Teams                    4.9%     905.1 MB    0.1 MB/s     1.2 Mbps
Route Planner Pro                  0.6%     144.0 MB    0 MB/s       0.1 Mbps
Service Host: Windows Update       0.2%     22.4 MB     0 MB/s       0 Mbps
System                             1.1%     0.1 MB      0.6 MB/s     0 Mbps
Windows Explorer                   0.9%     121.8 MB    0 MB/s       0 Mbps

Startup apps tab (Startup impact):
  Microsoft OneDrive ............ High    Enabled
  Microsoft Teams ............... High    Enabled
  Route Planner Pro Updater ..... High    Enabled
  Realtek Audio Console ......... Low     Enabled
  Spotify ....................... Medium  Enabled
""")
ANS["cpu_hog"] = "Microsoft OneDrive"
ANS["mem_hog"] = "Microsoft Edge"

# ======================================================================= 1.5 boot / UEFI
w("uefi_settings_TRN-LT07.txt", """
UEFI firmware setup -- configuration dump      Device: TRN-LT07 (training laptop)
Ticket: "I'm trying to boot from the Linux USB stick for the VM lab. The laptop
         goes straight into Windows. The USB stick doesn't even appear in the
         one-time boot menu (F12). The same stick boots fine on other laptops."
=====================================================================
[Main]
  BIOS Version ................ 1.31.0
  System Time ................. 09:12:44
[Boot Configuration]
  Boot Mode ................... UEFI
  Fast Boot ................... Thorough
  Boot Sequence:
     1. Windows Boot Manager
     2. UEFI: Onboard NIC (IPv4)
     3. UEFI: Onboard NIC (IPv6)
[Integrated Devices]
  USB Ports ................... Enabled
  Enable USB Boot Support ..... Disabled
  Thunderbolt ................. Enabled
[Security]
  Secure Boot ................. Enabled
  Admin Password .............. Set
  TPM 2.0 ..................... On
[Power]
  Wake on LAN ................. Disabled
""")
ANS["uefi_setting"] = "Enable USB Boot Support"

# ======================================================================= 1.4 OneDrive
w("onedrive_status_icons.txt", """
OneDrive file status -- what the user sees in File Explorer (folder: Route Plans)
=====================================================================
File                              Status icon in File Explorer
---------------------------------------------------------------------
Q3_routes_master.xlsx             Solid green circle with white check
Driver_roster.xlsx                Blue cloud
Fuel_card_log.xlsx                Green outline circle with green check
Dock_schedule.docx                Red circle with white X
Old_routes_2024.zip               Blue cloud

The user flies to the Tampa office tomorrow and will have NO internet on the
plane. She needs to edit Driver_roster.xlsx during the flight.
""")

# ======================================================================= 2 Linux/macOS
w("crontab_backup-srv.txt", """
$ crontab -l        (user: backup on server backup-srv, Ubuntu 24.04)
# m  h   dom mon dow   command
30   2   *   *   1-5   /usr/local/bin/nightly_backup.sh
0    */6 *   *   *     /usr/local/bin/sync_shares.sh
15   23  1   *   *     /usr/local/bin/rotate_logs.sh
""")
ANS["cron_week"] = 5
ANS["cron_day"] = 4

w("ls_output_fileserver.txt", """
tech@fileserver:/srv/shares/accounting$ ls -l
total 48
-rw-r--r-- 1 mreyes  accounting  8812 Sep 28 16:40 budget_2027.xlsx
-rwxr-x--- 1 root    accounting   912 Sep 02 09:15 month_end_close.sh
-rw-rw-r-- 1 gliu    accounting 15200 Sep 29 08:02 invoices_sept.csv
-rw------- 1 mreyes  mreyes      4410 Sep 25 11:31 payroll_notes.txt
drwxrwx--- 2 root    accounting  4096 Sep 29 09:10 archive
""")
ANS["octal_script"] = "750"
ANS["group_write_file"] = "invoices_sept.csv"

# ---- Linux lab tarball with REAL permissions
def tar_add(tf, path, data=None, mode=0o644, isdir=False, uname="tech", gname="tech"):
    ti = tarfile.TarInfo(path)
    ti.mtime = int(time.mktime((2026, 9, 29, 8, 0, 0, 0, 0, -1)))
    ti.uname, ti.gname, ti.uid, ti.gid = uname, gname, 1000, 1000
    if isdir:
        ti.type, ti.mode = tarfile.DIRTYPE, mode
        tf.addfile(ti)
    else:
        b = data.encode()
        ti.size, ti.mode = len(b), mode
        tf.addfile(ti, io.BytesIO(b))

# syslog sample
levels = ["INFO"] * 14 + ["WARN"] * 3 + ["ERROR"] * 2
svcs = ["cupsd", "sshd", "cron", "NetworkManager", "smbd", "systemd"]
lines, n_err = [], 0
for i in range(240):
    lv = rng.choice(levels)
    svc = rng.choice(svcs)
    msg = {"INFO": "routine status ok", "WARN": "response slower than expected",
           "ERROR": "operation failed; see details"}[lv]
    if svc == "cupsd" and lv == "ERROR":
        msg = "printer PRN-WH-02 not responding"
    n_err += lv == "ERROR"
    lines.append(f"Sep 29 {6 + i // 40:02d}:{(i * 7) % 60:02d}:{(i * 13) % 60:02d} fileserver {svc}[{1000 + i}]: {lv} {msg}")
syslog = "\n".join(lines) + "\n"
ANS["syslog_errors"] = n_err

# auth log
ips = {"203.0.113.47": 37, "198.51.100.12": 9, "192.0.2.88": 14, "10.20.4.15": 2}
auth = []
for ip, n in ips.items():
    for _ in range(n):
        user = rng.choice(["root", "admin", "test", "oracle", "tech"])
        auth.append(f"sshd[{rng.randint(2000,9000)}]: Failed password for {'invalid user ' if user!='tech' else ''}{user} from {ip} port {rng.randint(30000,65000)} ssh2")
for _ in range(25):
    auth.append(f"sshd[{rng.randint(2000,9000)}]: Accepted publickey for tech from 10.20.4.15 port {rng.randint(30000,65000)} ssh2")
rng.shuffle(auth)
auth_txt = "".join(f"Sep 29 {7 + i // 30:02d}:{(i * 11) % 60:02d}:{(i * 17) % 60:02d} fileserver {l}\n" for i, l in enumerate(auth))
ANS["auth_top_ip"] = max(ips, key=ips.get)

FLAG_HIDDEN = "dotfiles-are-sneaky"
FLAG_EXEC = "chmod-plus-x-unlocked"
script = f"""#!/bin/bash
# fix_printer.sh -- restarts the print spooler check (training version)
if [ ! -x "$0" ]; then
  echo "This script is not marked executable. Fix its permissions and run it as ./fix_printer.sh"
  exit 1
fi
echo "Printer queue check complete."
echo "FLAG: $(echo '{FLAG_EXEC[::-1]}' | rev)"
"""
ANS["flag_hidden"] = FLAG_HIDDEN
ANS["flag_exec"] = FLAG_EXEC

readme = """Sawgrass Logistics -- Linux lab pack (use inside your Linux VM)
=================================================================
1. Copy sawgrass_linux_lab.tar.gz into your VM (shared folder, USB, or download it
   from the CTF in the VM's browser).
2. Extract it IN A TERMINAL so the permissions are kept:
       tar -xzvf sawgrass_linux_lab.tar.gz
       cd sawgrass_lab
3. Useful commands: ls -la, cat, less, grep, grep -c, wc -l, cut, sort, uniq -c,
   chmod, find, pwd, cd
Answer the CTF challenges marked [VM].
"""
tpath = os.path.join(OUT, "sawgrass_linux_lab.tar.gz")
with tarfile.open(tpath, "w:gz") as tf:
    tar_add(tf, "sawgrass_lab", isdir=True, mode=0o755)
    tar_add(tf, "sawgrass_lab/README.txt", readme)
    tar_add(tf, "sawgrass_lab/.flag_hidden", f"You found the hidden file. Hidden files start with a dot and only show with ls -a.\nFLAG: {FLAG_HIDDEN}\n", mode=0o600)
    tar_add(tf, "sawgrass_lab/logs", isdir=True, mode=0o755)
    tar_add(tf, "sawgrass_lab/logs/syslog.sample", syslog)
    tar_add(tf, "sawgrass_lab/logs/auth.log", auth_txt, mode=0o640)
    tar_add(tf, "sawgrass_lab/scripts", isdir=True, mode=0o755)
    tar_add(tf, "sawgrass_lab/scripts/fix_printer.sh", script, mode=0o644)
    tar_add(tf, "sawgrass_lab/reports", isdir=True, mode=0o755)
    tar_add(tf, "sawgrass_lab/reports/q3_fleet_report.txt", "Q3 fleet report: 212 trucks, 98.1% on-time.\n", mode=0o644)
    tar_add(tf, "sawgrass_lab/reports/q3_fuel_report.txt", "Q3 fuel report: 1.2M gallons.\n", mode=0o000)
    tar_add(tf, "sawgrass_lab/reports/q3_safety_report.txt", "Q3 safety report: 0 lost-time incidents.\n", mode=0o664)
ANS["locked_report"] = "q3_fuel_report.txt"

# ======================================================================= 3 Mobile
w("battery_usage_iphone_DRV-PH22.txt", """
Settings > Battery  (iPhone, driver Luis O.)   "Last 24 Hours"
Complaint: "My phone used to last all day. Now it's dead by lunch."
=====================================================================
App                      Battery use   On Screen     Background
-----------------------------------------------------------------
FleetTrack Driver        41%           0h 22m        6h 48m
Messages                 12%           1h 05m        0h 03m
Maps                     11%           0h 58m        0h 10m
Microsoft Outlook         9%           0h 31m        0h 12m
Home & Lock Screen        8%           --            --
Camera                    4%           0h 06m        0h 00m
Spotify                   3%           0h 02m        0h 41m
""")
ANS["battery_app"] = "FleetTrack Driver"

w("hotspot_ticket.txt", """
Ticket: Field tech Tara B. can't connect her laptop to her phone's hotspot.
Other people's phones and tablets connect to it fine.
=====================================================================
Phone hotspot settings (Android)
  Hotspot name ............. TaraB-Hotspot
  Security ................. WPA2/WPA3-Personal
  Password ................. (verified correct)
  AP band .................. 5 GHz
  Connected devices ........ 2 of 10
  Turn off when no devices . 10 minutes

Laptop: LT-0288 (2016 model)
  Wireless adapter ......... Realtek RTL8188EE (802.11n), 2.4 GHz only*
  * per the manufacturer's spec sheet for this SKU
  Available networks ....... Sawgrass-Guest, DIRECT-printer, (TaraB-Hotspot NOT listed)
""")
ANS["hotspot_band"] = "2.4 GHz"

w("app_permission_requests.txt", """
New-app review queue -- Mobile Device Management (MDM) store request list
Approve only apps whose permission requests make sense for what the app does.
=====================================================================
APP                     PURPOSE                         PERMISSIONS REQUESTED
--------------------------------------------------------------------------------
FleetTrack Driver       GPS route tracking for drivers  Location (precise), Notifications
DocScan Lite            Scan delivery receipts to PDF   Camera, Files
BrightBeam Flashlight   Turns on the camera flash       Camera, Contacts, Location (precise),
                                                        Microphone, Call logs
Teams                   Chat and meetings               Microphone, Camera, Notifications, Contacts
WeatherNow              Local weather alerts            Location (approximate), Notifications
""")
ANS["bad_app"] = "BrightBeam Flashlight"

w("mdm_actions_log.txt", """
MDM console -- device actions log      Policy reminder:
  LOST device (misplaced, likely to be found)  -> Remote LOCK + Locate. Do NOT wipe.
  STOLEN device or confirmed unrecoverable      -> Remote WIPE.
=====================================================================
Time              Device ID   User        Report                                  Action
2026-09-22 10:14  MDV-1182    hmendez     "Left it in a truck cab, checking"      LOCK, LOCATE
2026-09-23 16:40  MDV-1207    ochen       "Phone stolen from car at gas station"  WIPE
2026-09-25 08:05  MDV-1149    priya.n     "Misplaced somewhere in the office"     WIPE
2026-09-26 13:22  MDV-1219    wturner     "Dropped in the bay, phone unrecoverable" WIPE
2026-09-28 09:47  MDV-1233    kpatel      "Can't find it, might be at home"       LOCK, LOCATE
""")
ANS["bad_wipe"] = "MDV-1149"

w("mobile_mail_settings.txt", """
Ticket: "I get new mail on my phone, but nothing I send ever leaves the Outbox."
=====================================================================
COMPANY STANDARD (IT knowledge base)          USER'S PHONE (Mail > Account > Advanced)
Incoming: IMAP  mail.sawgrass.example         Incoming: IMAP  mail.sawgrass.example
          Port 993, SSL/TLS on                          Port 993, SSL/TLS on
Outgoing: SMTP  smtp.sawgrass.example         Outgoing: SMTP  smtp.sawgrass.example
          Port 587, STARTTLS, auth required             Port 25, STARTTLS, auth required
Username: full email address                  Username: lortega@sawgrass.example
""")
ANS["smtp_port"] = "587"

# ======================================================================= Boss: BitLocker
w("boss_ticket_INC-20077.txt", """
INC-20077 | P1 | Reported by: Marisol Reyes (CFO) | Phone call 07:52
"After IT pushed the BIOS update last night my laptop shows a blue screen asking
 for a BitLocker recovery key. I have the board meeting at 9."

Tier 1 notes:
 - User is reading the screen to us over the phone (her photo of it is attached
   as bitlocker_recovery_screen.txt).
 - Asset tag on the bottom of the laptop: LT-0611
 - Verified identity with callback to her desk number and manager approval.
 - Next step: find the matching recovery key in the escrow export and read it
   to her. MAKE SURE the Key ID matches - devices can have more than one key.
""")
w("bitlocker_recovery_screen.txt", """
                                  BitLocker recovery

  Enter the recovery key for this drive
  _ _ _ _ _ _ - _ _ _ _ _ _ - _ _ _ _ _ _ - _ _ _ _ _ _ - ...

  Use the number keys or function keys F1-F10 (use F10 for 0).

  Use this to identify your key:
  Recovery key ID: 9C3E71A4

  Here's how to find your key:
  - Contact your organization's help desk
  - Sign in to your work or school account on another device

  Recovery key ID: 9C3E71A4-...
  Drive label: LT-0611 OS C: 9/30/2026
""")
def key():
    return "-".join(f"{rng.randint(0, 65535) * 11:06d}" for _ in range(8))
devices = [("LT-0588", "4F1D22B0"), ("LT-0611", "2B7A90C3"), ("LT-0611", "9C3E71A4"),
           ("LT-0612", "9C3E7F02"), ("ACC-PC09", "A0D41E77"), ("LT-0519", "71BC3E9A")]
rows = []
for dev, kid in devices:
    full_id = kid + "-" + "-".join("%04X" % rng.randint(0, 65535) for _ in range(3)) + "-" + "%012X" % rng.getrandbits(48)
    rows.append(dict(DeviceName=dev, KeyID=full_id, RecoveryKey=key(), Created=rng.choice(["2025-11-04", "2026-03-18", "2026-08-30"])))
with open(os.path.join(OUT, "bitlocker_escrow_export.csv"), "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=["DeviceName", "KeyID", "RecoveryKey", "Created"])
    wr.writeheader(); wr.writerows(rows)
ANS["boss_key"] = [r for r in rows if r["KeyID"].startswith("9C3E71A4")][0]["RecoveryKey"]
ANS["boss_wrong_key"] = [r for r in rows if r["DeviceName"] == "LT-0611" and not r["KeyID"].startswith("9C3E71A4")][0]["RecoveryKey"]

json.dump(ANS, open(os.path.join(HERE, "answers.json"), "w"), indent=2)
print(json.dumps(ANS, indent=2))
