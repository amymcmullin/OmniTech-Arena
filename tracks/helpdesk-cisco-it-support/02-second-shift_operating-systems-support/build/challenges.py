"""Game 2 -- Help Desk: Second Shift (Operating Systems Support). Challenge definitions."""
import json, os, re

A = json.load(open(os.path.join(os.path.dirname(__file__), "answers.json")))
CI = "case_insensitive"

def exact(s):
    return ("regex", r"^\s*" + re.escape(s) + r"\s*$", CI)
def words(*parts):
    return ("regex", r"^\s*" + r"[\s_-]*".join(re.escape(p) for p in parts) + r"s?\s*$", CI)
def seq(*items):
    parts = [("0?" + re.escape(str(i))) if str(i).isdigit() else re.escape(str(i)) for i in items]
    lead = r"^\D*?" if str(items[0]).isdigit() else r"^\s*"
    return ("regex", lead + r"[\s,;/-]+".join(parts) + r"\s*$", CI)
def letters(s):
    return ("regex", r"^\s*" + r"[\s,;-]*".join(re.escape(c) for c in s) + r"\s*$", CI)
def number(n, unit=r""):
    return ("regex", r"^\s*" + re.escape(str(n)) + r"(\.0+)?\s*%?\s*" + unit + r"\s*$", CI)

CAT = {
    1: "OS 1A Windows Display, Power & Access (1.1-1.2)",
    2: "OS 1B Windows Integrity & Backup (1.3-1.4)",
    3: "OS 1C Windows Boot (1.5)",
    4: "OS 2A Linux & macOS Tools (2.1-2.3)",
    5: "OS 2B Linux CLI [VM] (2.4)",
    6: "OS 2C macOS Troubleshooting (2.5)",
    7: "OS 3A Mobile Features & Security (3.1-3.3)",
    8: "OS 3B Mobile Issues & Apps (3.4-3.6)",
    9: "OS 3C The Cloud (3.7)",
    10: "OS 4 Boss Ticket",
}
NOTE = "\n\n*Answers are not case-sensitive.*"
C = []
def ch(name, cat, value, desc, flags, hints=(), files=(), tags=(), max_attempts=0, requires=()):
    C.append(dict(name=name, category=CAT[cat], value=value, description=desc.strip() + NOTE, flags=list(flags),
                  hints=list(hints), files=list(files), tags=list(tags), max_attempts=max_attempts, requires=list(requires)))

# ============================================================ 1A Display, Power, Accessibility
ch("Promoted!", 1, 50, """
Congratulations. After your first shift on the help desk, **Sawgrass Logistics** has moved you up to **Desktop & Mobile Support**. Your queue is now full of Windows, Mac, Linux, and phone problems.

To clock in, submit:

`second shift`
""", [exact("second shift")], tags=["CCST 4.1"])

ch("Four Ways to Project", 1, 200, """
Pressing **Windows key + P** opens four display modes:

- **A.** PC screen only
- **B.** Duplicate
- **C.** Extend
- **D.** Second screen only

Match each request to a mode:

1. A trainer wants the class to see **exactly what's on her laptop** on the projector.
2. A dispatcher wants to drag his route map onto the second monitor and keep email on the first, so the **two screens show different things**.
3. A user's laptop lid is broken, so she wants **only the external monitor** turned on.
4. A user wants the projector to **stop showing anything** so nobody sees his inbox, while his laptop keeps working.

Enter the letters for 1 through 4 in order (example: `ABCD`).
""", [letters("BCDA")], tags=["CCST 4.1", "Y100200 03.0"], max_attempts=4)

ch("Battery Health", 1, 250, """
Open **battery_report_LT-0519.txt**. This is the output of the Windows command `powercfg /batteryreport`.

The user says the laptop "dies in an hour and a half."

What percentage of its **design capacity** can this battery still hold? Round to a whole number (example: `82`).
""", [number(A["battery_pct"])],
   hints=[("Battery health = FULL CHARGE CAPACITY / DESIGN CAPACITY x 100.", 0)],
   files=["battery_report_LT-0519.txt"], tags=["CCST 4.1", "Y100200 09.0"], max_attempts=5)

ch("Replace or Keep?", 1, 100, """
Using **battery_report_LT-0519.txt** again, and the company policy at the bottom of the file:

Should this battery be replaced? Answer `yes` or `no`.
""", [exact("yes")], files=["battery_report_LT-0519.txt"], tags=["CCST 4.1"], max_attempts=1,
   requires=["Battery Health"])

ch("Access for Everyone", 1, 250, """
Windows 11 has accessibility features for vision, hearing, and dexterity. Match each user to the **best** feature:

- **A.** Magnifier
- **B.** Narrator
- **C.** Live captions
- **D.** On-Screen Keyboard
- **E.** Sticky Keys
- **F.** Color filters
- **G.** Mono audio

1. A user who is **blind** needs the computer to read screen content aloud.
2. A user who is **deaf** wants text subtitles for the audio in a training video.
3. A user has **red-green color blindness** and can't tell the status colors apart on a dashboard.
4. A user with **one working hand** can't hold **Ctrl + Alt + Delete** at the same time.
5. A user can hear in **only one ear** and misses sound that plays on the left channel.
6. A user's **keyboard is broken** and a replacement won't arrive until tomorrow.
7. A user with **low vision** needs part of the screen enlarged.

Enter the letters for 1 through 7 in order (example: `ABCDEFG`).
""", [letters("BCFEGDA")], hints=[("Sticky Keys lets you press modifier keys one at a time instead of together.", 0)],
   tags=["CCST 4.1", "Y100200 03.0"], max_attempts=4)

# ============================================================ 1B Integrity & Backup
ch("Patch Tuesday Problems", 2, 200, """
Open **update_history_ACC-PC09.txt**.

The security team reports that ACC-PC09 is missing a security update. Which **KB number** keeps failing to install? (Example format: `KB1234567`)
""", [("regex", r"^\s*(KB)?\s*" + A["failed_kb"][2:] + r"\s*$", CI)],
   files=["update_history_ACC-PC09.txt"], tags=["CCST 4.1", "Y100200 03.0"], max_attempts=4)

ch("Error Code Lookup", 2, 200, """
Using **update_history_ACC-PC09.txt** again:

You'll research the failure, and including the **exact error code** gives much better search results. What error code did the failed update report? (Example format: `0x12345678`)
""", [("regex", r"^\s*0x800f0922\s*$", CI)], files=["update_history_ACC-PC09.txt"], tags=["CCST 4.1", "CCST 6.2"], max_attempts=4)

ch("Who's Eating the CPU?", 2, 200, """
Open **task_manager_DSP-PC04.txt**.

The user says everything has been slow since they copied an old shared drive into OneDrive. Which process is using the **most CPU**? Enter the name exactly as Task Manager shows it.
""", [exact(A["cpu_hog"]), exact("OneDrive"), exact("OneDrive.exe")],
   files=["task_manager_DSP-PC04.txt"], tags=["CCST 4.1", "Y100200 03.0"], max_attempts=4)

ch("Memory Lane", 2, 150, """
Using **task_manager_DSP-PC04.txt** again:

Which process is using the **most memory**? Enter the name without the number in parentheses.
""", [exact(A["mem_hog"]), exact("Microsoft Edge (14)"), exact("Edge"), exact("msedge.exe")],
   files=["task_manager_DSP-PC04.txt"], tags=["CCST 4.1"], max_attempts=4)

ch("Clean Slate", 2, 100, """
A web app is showing an old version of a page even after the developers say they fixed it. Clearing the **browser cache** usually solves this.

In Microsoft Edge and Google Chrome on Windows, what **keyboard shortcut** opens *Clear browsing data* directly? (Example format: `Ctrl+Alt+X`)
""", [("regex", r"^\s*ctrl\s*\+\s*shift\s*\+\s*(del|delete)\s*$", CI)],
   hints=[("It uses Ctrl, Shift, and the key you'd use to delete things.", 0)], tags=["CCST 4.1", "CCST 4.5"], max_attempts=4)

ch("Fly Offline", 2, 250, """
Open **onedrive_status_icons.txt**.

The user needs to **edit Driver_roster.xlsx on a plane with no internet**. Right now its status is a **blue cloud**.

1. What does the blue cloud mean? Pick one: **A** = available on this device, **B** = online-only (not downloaded), **C** = sync error.
2. Which file in the list has a **sync problem** that needs fixing before she leaves?

Enter `letter,filename` (example: `A,Report.docx`).
""", [("regex", r"^\s*B\s*[,;\s]\s*Dock_schedule(\.docx)?\s*$", CI)],
   hints=[("Fix it by right-clicking the file and choosing 'Always keep on this device'. A red X means the file can't sync.", 0)],
   files=["onedrive_status_icons.txt"], tags=["CCST 4.1", "CCST 4.4"], max_attempts=3)

ch("Recycle Bin Rescue", 2, 250, """
A user deleted a folder from her **OneDrive for work or school** (Microsoft 365 business account) **45 days ago** and just realized she needs it.

Research it: by default, how many **days** does OneDrive for work or school keep deleted items before they're gone for good? Enter a number.
""", [number(93, r"(days?)?")],
   hints=[("Search: `OneDrive work or school restore deleted files how long` on support.microsoft.com", 0),
          ("Personal OneDrive accounts keep items for 30 days. Work or school accounts keep them longer.", 30)],
   tags=["CCST 4.1", "CCST 6.2"], max_attempts=4)

# ============================================================ 1C Boot
ch("Boot Order", 3, 250, """
Put the Windows (UEFI) startup sequence in order:

- **A.** The Windows kernel (**ntoskrnl.exe**) loads drivers and starts core services.
- **B.** The PC is powered on and the firmware runs **POST** (power-on self-test).
- **C.** The user signs in at the **logon screen** (Winlogon).
- **D.** UEFI firmware reads the boot order and starts **Windows Boot Manager** (bootmgfw.efi).
- **E.** Boot Manager starts the **Windows OS Loader** (winload.efi).

Enter the letters in order (example: `ABCDE`).
""", [letters("BDEAC")], tags=["CCST 4.1", "Y100200 03.0"], max_attempts=4)

ch("Safe Mode, Please", 3, 200, """
A driver is crashing Windows at startup. You go to **Settings > System > Recovery > Advanced startup > Troubleshoot > Advanced options > Startup Settings > Restart**.

The **Startup Settings** menu appears. Which **number** do you press to start **Safe Mode with Networking**, so you can download a fixed driver?
""", [("regex", r"^\s*F?5\s*$", CI)], tags=["CCST 4.1"], max_attempts=2)

ch("USB Won't Boot", 3, 300, """
Open **uefi_settings_TRN-LT07.txt**.

The user's Linux USB stick doesn't even appear in the one-time boot menu, but it boots fine on other laptops. One firmware setting stops this laptop from booting from **any** USB device.

Enter the **name of that setting** exactly as it appears in the dump.
""", [exact(A["uefi_setting"]), words("usb", "boot", "support"), words("usb", "boot")],
   hints=[("Secure Boot can block unsigned operating systems, but most Linux USBs are signed, and the stick isn't even listed. Look for something that turns off USB booting completely.", 0)],
   files=["uefi_settings_TRN-LT07.txt"], tags=["CCST 4.1", "Y100200 01.0"], max_attempts=4)

# ============================================================ 2A Linux & macOS tools, best practices, virtualization
ch("Right Tool (Mac Edition)", 4, 200, """
Match each macOS task to the built-in tool:

- **A.** Time Machine
- **B.** Disk Utility (First Aid)
- **C.** Activity Monitor
- **D.** Spotlight
- **E.** Terminal

1. Find and **force-quit** an app that's using 300% CPU.
2. Run the command `ping 8.8.8.8`.
3. Back up the whole Mac to an external drive, with hourly snapshots.
4. Quickly search the Mac for a file named *fleet_budget*.
5. Check and repair a drive that's showing errors.

Enter the letters for 1 through 5 in order.
""", [letters("CEADB")], tags=["CCST 4.2"], max_attempts=4)

ch("Cron Job Detective", 4, 250, """
Open **crontab_backup-srv.txt**. Cron schedules tasks on Linux and macOS. The five fields are **minute, hour, day-of-month, month, day-of-week**.

1. How many times **per week** does `nightly_backup.sh` run?
2. How many times **per day** does `sync_shares.sh` run?

Enter both numbers as `week,day` (example: `7,1`).
""", [seq(A["cron_week"], A["cron_day"])],
   hints=[("`1-5` in the day-of-week field means Monday through Friday. `*/6` in the hour field means every 6 hours.", 0)],
   files=["crontab_backup-srv.txt"], tags=["CCST 4.2", "Y100200 03.0"], max_attempts=4)

ch("Hypervisor Sort", 4, 250, """
A **Type 1** (bare-metal) hypervisor runs directly on the hardware. A **Type 2** (hosted) hypervisor runs as an app on top of a normal operating system.

Classify each product as `1` or `2`:

1. Oracle VirtualBox
2. VMware ESXi
3. Microsoft Hyper-V
4. VMware Workstation
5. Parallels Desktop for Mac

Enter five digits in order (example: `12121`).
""", [("regex", r"^\s*2[\s,;-]*1[\s,;-]*1[\s,;-]*2[\s,;-]*2\s*$", CI)],
   tags=["CCST 4.4", "Y100200 03.0"], max_attempts=4)

ch("Read the Permissions", 4, 250, """
Open **ls_output_fileserver.txt**.

1. What are the permissions of `month_end_close.sh` in **octal** (numeric) form? (Example: `644`)
2. Which **file** (not directory) can be **modified by any member of the accounting group**?

Enter `octal,filename` (example: `600,notes.txt`).
""", [("regex", r"^\s*0?750\s*[,;\s]\s*" + re.escape(A["group_write_file"]) + r"\s*$", CI)],
   hints=[("r = 4, w = 2, x = 1. Add them up for owner, group, and others. Look for **w** in the middle three characters (the group).", 0)],
   files=["ls_output_fileserver.txt"], tags=["CCST 4.2", "Y100200 03.0"], max_attempts=4)

# ============================================================ 2B Linux CLI [VM]
LAB = "sawgrass_linux_lab.tar.gz"
VMNOTE = "\n\n**[VM]** Do this in your **Linux virtual machine** (topic 2.3). Extract the pack in a terminal:\n\n`tar -xzvf sawgrass_linux_lab.tar.gz && cd sawgrass_lab`"
ch("Hidden in Plain Sight", 5, 200, """
In the Linux lab pack, there's a file that a plain `ls` won't show you.

Find it, read it, and submit the flag inside.""" + VMNOTE,
   [exact(A["flag_hidden"]), exact("FLAG: " + A["flag_hidden"])],
   hints=[("Try `ls -a`. Files whose names start with a dot are hidden.", 0)],
   files=[LAB], tags=["CCST 4.2", "Y100200 11.0"], max_attempts=0)

ch("Count the Errors", 5, 250, """
In the lab pack, `logs/syslog.sample` holds a morning of log messages from the file server.

How many lines contain the word **ERROR** (all capital letters)?""" + VMNOTE,
   [number(A["syslog_errors"])],
   hints=[("`grep -c ERROR logs/syslog.sample` counts matching lines.", 0)],
   files=[LAB], tags=["CCST 4.2", "Y100200 11.0"], max_attempts=5)

ch("Knock Knock", 5, 350, """
`logs/auth.log` records SSH sign-ins on the file server. Someone is trying to guess passwords.

Which **IP address** has the most **Failed password** attempts?""" + VMNOTE,
   [exact(A["auth_top_ip"])],
   hints=[("Start with `grep \"Failed password\" logs/auth.log`. Then pull out the IPs and count them.", 0),
          ("`grep \"Failed password\" logs/auth.log | grep -oE \"from [0-9.]+\" | sort | uniq -c | sort -rn`", 75)],
   files=[LAB], tags=["CCST 4.2", "Y100200 11.0", "Y100200 34.0"], max_attempts=4)

ch("Permission Denied", 5, 250, """
One file in `reports/` can't be opened, even by its owner. `cat` just returns *Permission denied*.

What is that file's **name**?""" + VMNOTE,
   [exact(A["locked_report"])],
   hints=[("`ls -l reports/`. Look for a file with no r, w, or x at all: `----------`.", 0)],
   files=[LAB], tags=["CCST 4.2", "Y100200 11.0"], max_attempts=3)

ch("Make It Run", 5, 300, """
`scripts/fix_printer.sh` refuses to run until it's set up correctly. Fix its permissions, run it as `./fix_printer.sh` from inside the `scripts` folder, and submit the flag it prints.""" + VMNOTE,
   [exact(A["flag_exec"]), exact("FLAG: " + A["flag_exec"])],
   hints=[("A script needs the execute (x) permission. `chmod +x fix_printer.sh`", 0)],
   files=[LAB], tags=["CCST 4.2", "Y100200 11.0"], max_attempts=0)

# ============================================================ 2C macOS
ch("Frozen Mac", 6, 100, """
A Mac app has frozen and won't respond to clicks. What **keyboard shortcut** opens the **Force Quit Applications** window? (Example format: `Command+Shift+X`)
""", [("regex", r"^\s*(cmd|command|⌘)\s*\+\s*(opt|option|alt|⌥)\s*\+\s*(esc|escape)\s*$", CI),
      ("regex", r"^\s*(opt|option|alt|⌥)\s*\+\s*(cmd|command|⌘)\s*\+\s*(esc|escape)\s*$", CI)],
   tags=["CCST 4.2"], max_attempts=4)

ch("Drive Swap", 6, 250, """
A user moves files between her **Mac** and a **Windows** PC on a USB drive. On the Mac, she can **open** files on the drive but **can't save or delete** anything. The drive was formatted on the Windows PC.

1. Which file system is the drive **probably** using? (The one macOS can read but not write by default.)
2. Which file system should you reformat it to so **both** computers can read **and** write? (It also handles files bigger than 4 GB.)

Enter both as `current,new` (example: `APFS,HFS+`).
""", [("regex", r"^\s*ntfs\s*[,;\s]\s*ex-?fat\s*$", CI)],
   hints=[("FAT32 works on both but has a 4 GB file size limit.", 0)],
   tags=["CCST 4.2", "Y100200 03.0"], max_attempts=3)

# ============================================================ 3A Mobile features & security
ch("Ten Strikes", 7, 150, """
A company iPhone has the **Erase Data** setting turned on (Settings > Face ID & Passcode).

After how many **failed passcode attempts** in a row will the iPhone erase all of its data?
""", [number(10)], tags=["CCST 4.3"], max_attempts=3)

ch("Lock, Don't Wipe", 7, 250, """
Open **mdm_actions_log.txt**. The policy at the top says when to **lock and locate** a device and when to **wipe** it.

One wipe broke the policy. It erased a device that was only **lost**, not stolen or unrecoverable. Which **Device ID** was it?
""", [exact(A["bad_wipe"])], files=["mdm_actions_log.txt"], tags=["CCST 4.3", "Y100200 17.0"], max_attempts=3)

ch("Pocket Rules", 7, 150, """
**Mobile Device Management (MDM)** lets IT control company phones. Which of these can MDM **not** do?

- **A.** Push an app to every company phone
- **B.** Require a passcode and enforce its length
- **C.** Remotely lock or wipe a lost device
- **D.** Read the user's passcode so IT can unlock the phone

Enter one letter. **You have 2 attempts.**
""", [exact("D")], tags=["CCST 4.3"], max_attempts=2)

# ============================================================ 3B Mobile issues & apps
ch("Battery Vampire", 8, 200, """
Open **battery_usage_iphone_DRV-PH22.txt**.

The driver's phone is dead by lunch. Which **app** is the main cause? Look at **background** activity, not just total percentage.
""", [exact(A["battery_app"]), exact("FleetTrack")], files=["battery_usage_iphone_DRV-PH22.txt"],
   tags=["CCST 4.3"], max_attempts=3)

ch("Hotspot Not Found", 8, 300, """
Open **hotspot_ticket.txt**.

Phones and tablets join Tara's hotspot without trouble, but her older laptop can't even **see** it. Which **frequency band** should the hotspot's AP band be changed to so the laptop can connect? (Example format: `6 GHz`)
""", [("regex", r"^\s*2\.4\s*(ghz)?\s*$", CI)],
   hints=[("Compare the hotspot's AP band with the bands the laptop's wireless adapter supports.", 0)],
   files=["hotspot_ticket.txt"], tags=["CCST 4.3", "Y100200 40.0"], max_attempts=3)

ch("Permission Creep", 8, 150, """
Open **app_permission_requests.txt**.

Best practice: apps should get **only** the permissions they need. Which app should **not** be approved because it asks for permissions that have nothing to do with what it does?
""", [exact(A["bad_app"]), exact("BrightBeam")], files=["app_permission_requests.txt"],
   tags=["CCST 4.3", "CCST 4.5"], max_attempts=2)

ch("Stuck in the Outbox", 8, 250, """
Open **mobile_mail_settings.txt**.

The user receives email on her phone but can't send. Compare her settings with the company standard. What should the **outgoing (SMTP) port** be?
""", [number(587)], files=["mobile_mail_settings.txt"], tags=["CCST 4.3", "CCST 4.5", "Y100200 32.0"], max_attempts=3)

# ============================================================ 3C Cloud
ch("As a Service", 9, 250, """
Classify each service with the cloud model it represents:

- **I** = IaaS (Infrastructure as a Service)
- **P** = PaaS (Platform as a Service)
- **S** = SaaS (Software as a Service)

1. Microsoft 365 (Outlook, Word, Teams in the browser)
2. Renting a virtual machine on Amazon EC2 and installing your own OS updates
3. Uploading your web app's code to Azure App Service and letting Microsoft run the servers and OS
4. Gmail
5. Creating virtual networks and virtual disks in Google Compute Engine

Enter five letters in order (example: `IPSSP`).
""", [letters("SIPSI")], tags=["CCST 4.4", "Y100200 15.0"], max_attempts=4)

ch("The Big Three", 9, 100, """
Three companies run the largest public clouds: **Amazon Web Services**, **Microsoft Azure**, and one more.

Which company runs the third? (One word.)
""", [("regex", r"^\s*google(\s*cloud(\s*platform)?)?\s*$", CI), exact("GCP")], tags=["CCST 4.4"], max_attempts=3)

ch("Cloud Deployment", 9, 150, """
Sawgrass keeps its payroll database on servers it owns in its own data center, and runs its website and email in Microsoft's public cloud. The two are connected and managed together.

What is this **cloud deployment model** called? (One word.)
""", [exact("hybrid"), words("hybrid", "cloud")], tags=["CCST 4.4"], max_attempts=3)

# ============================================================ Boss
ch("The Board Meeting Lockout", 10, 500, """
**P1 ticket, 07:52.** The CFO's laptop is asking for a **BitLocker recovery key** after last night's BIOS update. Her board meeting starts at 9:00.

You have three files:

1. **boss_ticket_INC-20077.txt**: the ticket and the asset tag
2. **bitlocker_recovery_screen.txt**: what her screen shows
3. **bitlocker_escrow_export.csv**: every recovery key IT has stored

Some devices have **more than one** key, and one key ID looks a lot like hers. A wrong key wastes time she doesn't have.

Enter the full **48-digit recovery key** you'll read to her, including dashes.
""", [("regex", r"^\s*" + re.escape(A["boss_key"]).replace(r"\-", r"[\s-]?") + r"\s*$", CI)],
   hints=[("Match on the **Key ID** shown on the screen, not just the device name.", 0),
          ("Two keys belong to LT-0611. Only one Key ID starts with the 8 characters on her screen.", 100)],
   files=["boss_ticket_INC-20077.txt", "bitlocker_recovery_screen.txt", "bitlocker_escrow_export.csv"],
   tags=["CCST 4.1", "Y100200 42.0"], max_attempts=3,
   requires=["Safe Mode, Please", "Patch Tuesday Problems", "Lock, Don't Wipe"])

if __name__ == "__main__":
    print(len(C), "challenges,", sum(c["value"] for c in C), "points")
    from collections import Counter
    for k, v in sorted(Counter(c["category"] for c in C).items()):
        print(f"  {k}: {v}")
