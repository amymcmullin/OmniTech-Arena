"""Generate the evidence files students analyze, and compute answers from them."""
import csv, json, os, random
from datetime import datetime, timedelta

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "files")
os.makedirs(OUT, exist_ok=True)
rng = random.Random(20260930)
ANS = {}

CO = "Sawgrass Logistics"
TECHS = ["J. Morales", "K. Brooks", "T. Nguyen", "R. Castillo"]
SLA_RESP = {"P1": 15, "P2": 60, "P3": 240, "P4": 480}          # minutes
SLA_RES = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}                 # hours

# ---------------------------------------------------------------- SLA policy
with open(f"{OUT}/sla_policy.txt", "w") as f:
    f.write(f"""{CO} IT Help Desk -- Service Level Agreement (internal)
=====================================================================
All targets are measured in CLOCK time from the ticket's "created" timestamp.
(Ignore business hours, weekends and holidays for this exercise.)

Priority  Meaning                                   First response   Resolution
--------  ----------------------------------------  --------------   ----------
P1        Critical - business stopped / many users       15 minutes     4 hours
P2        High - one user fully blocked, no workaround   1 hour         8 hours
P3        Medium - degraded, workaround exists           4 hours        24 hours
P4        Low - request / question / cosmetic            8 hours        72 hours

A ticket BREACHES its resolution SLA when (resolved - created) is greater than
the resolution target for its priority.

Key Performance Indicators (KPIs) tracked weekly:
  - First Response Time  (created -> first_response)
  - Resolution Time      (created -> resolved)
  - First Contact Resolution (FCR) = resolved tickets closed in ONE contact
                                     / all resolved tickets
  - Customer Satisfaction (CSAT, 1-5)
""")

# ---------------------------------------------------------------- ticket queue
people = ["Ana Ruiz", "Ben Carter", "Chloe Park", "Darnell Hayes", "Elena Vargas", "Frank Osei",
          "Grace Liu", "Hector Mendez", "Isla Thompson", "Jamal Wright", "Kira Patel", "Luis Ortega",
          "Maya Singh", "Noah Bennett", "Olivia Chen", "Priya Nair", "Quinn Adams", "Rosa Delgado",
          "Sam Fischer", "Tara Brooks", "Umar Haddad", "Vera Lopez", "Wes Turner", "Yara Haddad"]
depts = ["Accounting", "Dispatch", "Warehouse", "HR", "Sales", "Fleet", "Front Office"]
channels = ["Phone", "Email", "Chat", "Portal"]

resolved_pool = [
    ("Hardware", "Monitor flickers when laptop is docked"),
    ("Software", "Excel crashes when opening shared budget workbook"),
    ("Network", "Cannot reach shared drive S: from warehouse PC"),
    ("Account/Access", "Password expired, cannot sign in to Windows"),
    ("Email", "Outlook not receiving external email"),
    ("Printing", "Label printer prints blank labels"),
    ("Software", "Adobe Acrobat asks for license on launch"),
    ("Hardware", "Keyboard keys sticking on desktop"),
    ("Network", "VPN disconnects every 10 minutes"),
    ("Account/Access", "Needs access to Dispatch shared mailbox"),
    ("Email", "Out-of-office reply not turning on"),
    ("Printing", "Printer offline after toner change"),
    ("Software", "Teams camera not detected in meetings"),
    ("Hardware", "Laptop battery drains in under an hour"),
    ("Network", "Wi-Fi drops in break room"),
    ("Account/Access", "MFA prompt not arriving on new phone"),
    ("Email", "Mailbox almost full warning"),
    ("Printing", "Scan-to-email not delivering"),
    ("Software", "Browser keeps opening unknown homepage"),
    ("Hardware", "Docking station USB ports not working"),
    ("Network", "Slow internet at front desk kiosk"),
    ("Account/Access", "New hire needs account created"),
    ("Email", "Calendar invites showing wrong time zone"),
    ("Software", "PDF files open in wrong program"),
    ("Hardware", "Headset microphone not working"),
]
# Controlled KPI data for resolved tickets (25 tickets)
prios = ["P1", "P2", "P3", "P4", "P2", "P3", "P3", "P4", "P1", "P2", "P3", "P1", "P2",
         "P4", "P3", "P2", "P3", "P1", "P4", "P3", "P2", "P3", "P4", "P1", "P3"]
p1_resp = iter([8, 12, 22, 5, 13])                   # avg 12
breach_idx = {2, 6, 11, 15, 20}                      # 5 breaches of resolution SLA
contacts_multi = {1, 4, 6, 9, 11, 15, 17, 20, 23}    # 9 multi-contact -> FCR 16/25 = 64%
start = datetime(2026, 9, 21, 7, 30)
rows = []
tid = 10380
for i, ((cat, desc), pr) in enumerate(zip(resolved_pool, prios)):
    tid += 1
    created = start + timedelta(hours=i * 3.4, minutes=rng.randint(0, 50))
    resp = next(p1_resp) if pr == "P1" else rng.randint(int(SLA_RESP[pr] * 0.2), int(SLA_RESP[pr] * 0.9))
    target = SLA_RES[pr] * 60
    if i in breach_idx:
        res_min = target + rng.randint(25, 400)
    else:
        res_min = rng.randint(int(target * 0.25), target - 10)
    res_min = max(res_min, resp + 10)
    contacts = rng.randint(2, 4) if i in contacts_multi else 1
    rows.append(dict(
        ticket_id=f"INC-{tid}", created=created, reported_by=rng.choice(people), department=rng.choice(depts),
        channel=rng.choice(channels), category=cat, categorized_by=rng.choice(["AI", "AI", "Tech"]),
        priority=pr, status="Resolved", assigned_to=rng.choice(TECHS),
        first_response=created + timedelta(minutes=resp), resolved=created + timedelta(minutes=res_min),
        contacts=contacts, csat=rng.choice([3, 4, 4, 5, 5, 5]) , description=desc))

# Open / new tickets (the current queue), created Monday 9/28 - Tuesday 9/29
mon = datetime(2026, 9, 29, 7, 0)
open_specs = [
    # (offset_min, prio, status, category, cat_by, assigned, reporter, desc)
    (5,   "P3", "In Progress", "Printing", "AI", "K. Brooks", "Rosa Delgado", "Copier CPY-2F-01 jams on every double-sided job"),
    (12,  "P2", "New", "Software", "AI", "", "Diego Alvarez", "Blue screen errors are back since last night's Windows Update - same as last month"),
    (18,  "P1", "New", "Network", "Tech", "", "Wes Turner", "Dispatch floor: all 14 PCs lost internet, trucks cannot be routed"),
    (22,  "P3", "New", "Printing", "AI", "", "Maya Singh", "2nd floor copier (CPY-2F-01) shows error SC-542 and will not print"),
    (25,  "P4", "New", "Software", "AI", "", "Priya Nair", "Request: install Visio on my laptop"),
    (31,  "P3", "Open", "Hardware", "AI", "T. Nguyen", "Kira Patel", "Laptop LT-0443 fan is very loud"),
    (34,  "P1", "In Progress", "Software", "Tech", "R. Castillo", "Marisol Reyes (CFO)", "Excel will not open at all - month-end close due today"),
    (40,  "P3", "New", "Printing", "AI", "", "Luis Ortega", "Can't scan anything on the copier by HR - CPY-2F-01 says 'fuser error'"),
    (47,  "P2", "New", "Hardware", "AI", "", "Grace Liu", "Locked out after password expired - account says 'referred account is locked'"),
    (52,  "P4", "New", "Email", "Tech", "", "Sam Fischer", "How do I add a signature in Outlook?"),
    (58,  "P2", "Open", "Network", "Tech", "J. Morales", "Tara Brooks", "Teacher laptop in training Room 114 will not connect to Wi-Fi; other devices fine"),
    (63,  "P1", "New", "Network", "AI", "", "Olivia Chen", "Warehouse scanners cannot sync - receiving dock stopped"),
    (70,  "P3", "New", "Printing", "AI", "", "Hector Mendez", "Copier on 2 (CPY-2F-01) is printing streaks on everything"),
    (76,  "P3", "New", "Software", "AI", "", "Isla Thompson", "Teams shows error caa70004 after I changed my password"),
    (81,  "P4", "Open", "Account/Access", "Tech", "K. Brooks", "Noah Bennett", "Please add me to the Sales Teams channel"),
    (88,  "P2", "New", "Email", "AI", "", "Chloe Park", "Phone shows new emails but Outlook on desktop last updated 3 days ago"),
]
for off, pr, st, cat, cb, asg, rep, desc in open_specs:
    tid += 1
    created = mon + timedelta(minutes=off)
    rows.append(dict(ticket_id=f"INC-{tid}", created=created, reported_by=rep, department=rng.choice(depts),
                     channel=rng.choice(channels), category=cat, categorized_by=cb, priority=pr, status=st,
                     assigned_to=asg, first_response=(created + timedelta(minutes=9)) if st != "New" else "",
                     resolved="", contacts="", csat="", description=desc))

# Shuffle a little by channel so it's not perfectly sorted, keep chronological-ish
rows.sort(key=lambda r: r["ticket_id"])
fmt = lambda v: v.strftime("%Y-%m-%d %H:%M") if isinstance(v, datetime) else v
with open(f"{OUT}/ticket_queue_export.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow({k: fmt(v) for k, v in r.items()})

# ---- compute answers from the data
res = [r for r in rows if r["status"] == "Resolved"]
breaches = [r for r in res if (r["resolved"] - r["created"]) > timedelta(hours=SLA_RES[r["priority"]])]
ANS["sla_breaches"] = len(breaches)
ANS["sla_breach_ids"] = [r["ticket_id"] for r in breaches]
fcr = sum(1 for r in res if r["contacts"] == 1) / len(res) * 100
ANS["fcr_pct"] = fcr
p1 = [r for r in res if r["priority"] == "P1"]
ANS["p1_avg_resp_min"] = sum((r["first_response"] - r["created"]).total_seconds() / 60 for r in p1) / len(p1)
new = [r for r in rows if r["status"] == "New"]
new.sort(key=lambda r: (r["priority"], r["created"]))
ANS["queue_next"] = new[0]["ticket_id"]
ANS["copier_tickets"] = [r["ticket_id"] for r in rows if "CPY-2F-01" in r["description"] and r["status"] != "Resolved"]
# AI mis-categorisation: account lockout filed as Hardware
mis = [r for r in rows if r["categorized_by"] == "AI" and r["category"] == "Hardware" and "locked" in r["description"].lower()]
ANS["ai_miscat"] = mis[0]["ticket_id"]
ANS["cfo_ticket"] = [r["ticket_id"] for r in rows if "CFO" in r["reported_by"]][0]
ANS["diego_ticket"] = [r["ticket_id"] for r in rows if r["reported_by"] == "Diego Alvarez"][0]
ANS["room114_ticket"] = [r["ticket_id"] for r in rows if "Room 114" in r["description"]][0]

# ---------------------------------------------------------------- calls (customer types)
with open(f"{OUT}/call_transcripts.txt", "w") as f:
    f.write(f"""{CO} Help Desk -- recorded call excerpts (training use)
Identify the customer TYPE in each call.
=====================================================================

CALL A  (caller: warehouse systems lead)
 Caller: Hi, VPN client on my laptop fails at phase 2. I already flushed DNS,
         renewed my DHCP lease, and confirmed my certificate hasn't expired.
         I think the profile got pushed with the wrong gateway. Can you
         check what the config server sent me?
 Tech:   Sounds like you've covered the basics. Let me tell you what I want
         to verify on our side...

CALL B  (caller: new front office temp)
 Caller: Um, hi. The... the internet thing isn't working? The blue "e"?
         Or maybe it's the Google one. The box on the floor has a light
         but I don't know if it's supposed to be green.
 Tech:   No problem at all, we'll figure it out together. Can you tell me
         what you see on the screen right now?

CALL C  (caller: dispatch supervisor)
 Caller: This is the THIRD time this week! I was on hold for twenty
         minutes and my whole route plan is GONE. I had forty trucks
         scheduled and now I have nothing. Do you understand what that
         costs us?!
 Tech:   (lets the caller finish) I'm really sorry about the wait and
         about losing that work. Let's get your route plan back.

CALL D  (caller: sales rep)
 Caller: So the laptop, right, it's the one I took to my nephew's wedding
         in Tampa -- beautiful venue, you'd love it, right on the water --
         and my sister-in-law was saying her laptop does the same thing,
         and anyway the battery was fine at the reception but then the
         next morning at the hotel, and the hotel breakfast was...
 Tech:   (after about a minute) That sounds like a great trip! So I can
         help quickly -- is the laptop charging when it's plugged in?

CALL E  (caller: accounting manager)
 Caller: Is Marcus there? He's the only one over there who actually knows
         anything. Honestly, I don't know why they let you people answer
         the phones. Just fix my printer and don't waste my time asking
         me if it's plugged in.
 Tech:   I can help you right now, or I can see if Marcus is available.
         Which would you prefer?
""")
ANS["calls"] = "DEACB"  # Talkative, Rude, Knowledgeable, Angry, Inexperienced

# ---------------------------------------------------------------- hold / transfer transcript
hold_lines = [
    "Tech: Thank you for calling Sawgrass IT, this is Jordan. How can I help?",
    "Caller: Hi, my shared mailbox for Dispatch disappeared from Outlook.",
    "Tech: I'm sorry about that. Can I get your name and the ticket number if you have one?",
    "Caller: Sure, Tara Brooks. No ticket yet.",
    "Tech: Thanks, Tara. Is it just the Dispatch mailbox that's missing, or your own mail too?",
    "Tech: Hang on.  [places caller on hold immediately - 4 minutes of silence]",
    "Tech: Okay, I'm back. I checked and your permissions look fine.",
    "Caller: So why can't I see it?",
    "Tech: I'd like to check one setting with our Exchange admin. May I place you on hold for about two minutes?",
    "Caller: Sure, that's fine.",
    "Tech: Thank you for holding, Tara. The admin says it's a sync issue on your profile.",
    "Caller: Okay, what do we do?",
    "Tech: [transfers call without saying anything - caller hears ringing]",
    "Tier 2: Messaging team, this is Priya.",
    "Caller: Uh, hi? I was just talking to someone about my mailbox?",
    "Tier 2: Okay... what's the problem?",
    "Caller: I have to explain all of this again?",
    "Tier 2: Actually this is a desktop issue, let me put you back in the general queue.  [call drops to queue]",
    "Caller: ...",
    "Tech (callback 1 hr later): Hi Tara, this is Jordan. I'm sorry you were bounced around - I'll stay with you until it's fixed.",
]
with open(f"{OUT}/hold_and_transfer_call.txt", "w") as f:
    f.write("Call review: hold and transfer handling\n")
    f.write("Line numbers are on the left. Some lines show PROPER technique; some do not.\n")
    f.write("=" * 70 + "\n")
    for i, l in enumerate(hold_lines, 1):
        f.write(f"{i:02d}  {l}\n")
ANS["hold_lines"] = [6, 13, 18]

# ---------------------------------------------------------------- ticket notes review
with open(f"{OUT}/ticket_notes_review.txt", "w") as f:
    f.write(f"""{CO} -- Closed ticket notes submitted this week (QA review)
Your lead wants you to review these before they are added to the knowledge base.
=====================================================================

INC-10302  | Tech: T. Nguyen | Monitor flickers when docked
Issue: User's external monitor flickers only when the laptop is in the dock.
Steps:
  1. Swapped DisplayPort cable - flicker continued.
  2. Updated dock firmware from 1.0.12 to 1.0.19 - flicker stopped.
  3. Monitored for 20 minutes with user - no flicker.
Outcome: Resolved by dock firmware update.
Next steps: None. Added dock firmware check to the docking KB article.

INC-10303  | Tech: K. Brooks | Cannot sign in after password reset
Issue: User could not sign in after self-service password reset.
Steps:
  1. Confirmed account was not locked in Active Directory.
  2. User's new password is Sunshine2026! -- reset it to this again and
     had user sign in successfully.
Outcome: Resolved. User signed in.
Next steps: None.

INC-10304  | Tech: R. Castillo | Excel formulas not calculating
Issue: Formulas in the user's workbook show old values.
Steps:
  1. Found calculation set to Manual. Switched to Automatic.
  2. User clearly doesn't know what they're doing, typical Accounting.
     Took forever because she kept clicking things.
Outcome: Resolved. Calculation set to Automatic.
Next steps: None.

INC-10305  | Tech: J. Morales | Scan-to-email not delivering
Issue: Scans from the HR copier are not arriving in user inboxes.
Steps:
  1. Verified the copier's address book entry for the user was correct.
  2. Checked the SMTP relay settings on the copier.
  3. Sent a test scan to my own mailbox.
  4. Checked the mail flow logs in the admin center.

INC-10306  | Tech: T. Nguyen | Headset microphone not working
Issue: User's USB headset mic is not picked up in Teams calls.
Steps:
  1. Checked Windows sound settings - headset set as output but not input.
  2. Set headset as default input device; tested with Windows mic test - works.
  3. Made Teams test call - user heard clearly.
Outcome: Resolved - input device was set to laptop's built-in mic.
Next steps: Showed user how to pick the device in Teams settings.

INC-10307  | Tech: K. Brooks | Browser opens unknown homepage
Issue: Edge opens an unfamiliar search page on launch.
Steps:
  1. Found an unapproved browser extension "QuickSearch Helper" installed 9/20.
  2. Removed the extension and reset Edge startup settings.
  3. Ran a full Defender scan - no other threats found.
Outcome: Resolved - extension removed.
Next steps: Reminded user to install extensions only from the approved list.
""")
ANS["notes_leak"] = "INC-10303"
ANS["notes_opinion"] = "INC-10304"
ANS["notes_missing_outcome"] = "INC-10305"

# ---------------------------------------------------------------- Diego history
with open(f"{OUT}/diego_ticket_history.txt", "w") as f:
    f.write(f"""Knowledge base -> customer history for: Diego Alvarez (Dispatch)
=====================================================================
INC-09811 | 2026-08-24 | Tech: A. Kim | Priority P2 | Resolved
Issue: Diego's desktop computer shows blue screen errors frequently since the
       last system update.
Troubleshooting Steps:
  1. Asked Diego to note the specific error code displayed on the blue screen.
     Error code: "STOP 0x0000007E SYSTEM_THREAD_EXCEPTION_NOT_HANDLED."
  2. Guided Diego to boot the computer in Safe Mode. The system successfully
     booted without errors.
  3. Checked for recently installed drivers or software updates. Found a new
     graphics driver (version 32.0.15.6094) was installed yesterday.
  4. Assisted Diego in rolling back the graphics driver to the previous
     version, 31.0.15.4601.
  5. Restarted the computer normally. No blue screen error occurred after
     30 minutes of operation.
Outcome: Rolling back the graphics driver resolved the blue screen errors.
Next Steps: Advised Diego to avoid updating the graphics driver until a stable
     version is released. Provided instructions on how to disable automatic
     driver updates.
Notes: Diego was comfortable following technical instructions with guidance.

INC-09102 | 2026-06-02 | Tech: J. Morales | Priority P4 | Resolved
Issue: Diego requested a second monitor for his workstation.
Outcome: Monitor MON-0212 delivered and connected. Resolved.
""")
ANS["diego_driver"] = "31.0.15.4601"

# ---------------------------------------------------------------- eight steps (shuffled)
steps = {
    "A": "Observe the results of the changes.",
    "B": "Define the problem.",
    "C": "Document the changes made to resolve the problem.",
    "D": "Devise a plan to resolve the problem.",
    "E": "Gather detailed information.",
    "F": "If the problem is not resolved, repeat the process.",
    "G": "Make necessary changes to implement the plan.",
    "H": "Identify a probable cause of the failure.",
}
ANS["eight_steps"] = "BEHDGAFC"

# ---------------------------------------------------------------- Kyle's log
with open(f"{OUT}/troubleshooting_log_kyle.txt", "w") as f:
    f.write("""Troubleshooting log -- Tech: Kyle (Tier 1, week 2)
Ticket: Front desk kiosk PC "internet is super slow"
=====================================================================
[1] 09:02  Asked user what "slow" means. User: web pages take 30+ seconds to load.
[2] 09:05  Asked when it started. User: this morning. Nothing installed that they know of.
[3] 09:09  Checked other front desk PC - loads pages normally. Issue isolated to kiosk.
[4] 09:14  Probable cause: kiosk-specific (network adapter, DNS, or software).
[5] 09:16  Plan: check adapter speed/duplex first; then DNS; then startup software.
[6] 09:20  Updated network driver, changed DNS to 8.8.8.8, disabled Windows
           Firewall, and uninstalled two toolbars. Rebooted.
[7] 09:31  Pages load fast now.
[8] 09:33  User asked what fixed it. Not sure - told user "one of those things."
[9] 09:35  Closed ticket.
""")
ANS["kyle_entry"] = 6

# ---------------------------------------------------------------- Room 114 event log
with open(f"{OUT}/room114_laptop_events.txt", "w") as f:
    f.write("""Exported events -- Host: TRN114-LT01 (training Room 114 teacher laptop)
Filter: Setup / System / WLAN-AutoConfig        Times are local
=====================================================================
2026-09-08 10:14  WindowsUpdate  Installed: Intel(R) Wi-Fi 6E AX211 160MHz driver 23.40.0.4
2026-09-08 10:16  WLAN-AutoConfig  Connected to SSID "Sawgrass-Staff"
2026-09-15 08:01  WLAN-AutoConfig  Connected to SSID "Sawgrass-Staff"
2026-09-22 08:03  WLAN-AutoConfig  Connected to SSID "Sawgrass-Staff"
2026-09-24 12:40  WindowsUpdate  Installed: 2026-09 Cumulative Update for Windows 11 (fictional KB5099120)
2026-09-25 07:58  WLAN-AutoConfig  Connected to SSID "Sawgrass-Staff"
2026-09-26 16:22  WindowsUpdate  Installed: Intel(R) Wi-Fi 6E AX211 160MHz driver 23.60.0.9
2026-09-26 16:23  System  Device PCI\\VEN_8086&DEV_51F0 requires further installation
2026-09-29 07:55  WLAN-AutoConfig  The wireless adapter is not present or disabled
2026-09-29 07:56  WLAN-AutoConfig  The wireless adapter is not present or disabled
2026-09-29 08:40  WindowsUpdate  Installed: Security Intelligence Update for Microsoft Defender
2026-09-29 09:05  WLAN-AutoConfig  The wireless adapter is not present or disabled
""")
ANS["room114_driver"] = "23.60.0.9"

# ---------------------------------------------------------------- remote sessions log
sess = []
def s(sid, t, tech, user, ticket, tool, events):
    sess.append((sid, t, tech, user, ticket, tool, events))
s("RS-4471", "2026-09-29 07:40", "jmorales", "tbrooks", ANS["room114_ticket"], "Windows Remote Assistance",
  ["INVITE_SENT", "USER_ACCESS_GRANTED", "CONNECTED", "NOTE narrated steps to user", "DISCONNECTED", "LOGGED_OUT"])
s("RS-4474", "2026-09-29 08:05", "kbrooks", "rdelgado", "INC-10406", "TeamViewer",
  ["ONE_TIME_CODE_ISSUED", "USER_ACCESS_GRANTED", "CONNECTED", "FILE_TRANSFER copier_driver.zip", "DISCONNECTED", "LOGGED_OUT"])
s("RS-4479", "2026-09-29 08:31", "tnguyen", "kpatel", "INC-10411", "VNC",
  ["CONNECTED (admin override - user prompt skipped)", "NOTE checked fan speed utility", "DISCONNECTED", "LOGGED_OUT"])
s("RS-4480", "2026-09-29 08:52", "rcastillo", "mreyes", ANS["cfo_ticket"], "Microsoft Remote Desktop",
  ["USER_ACCESS_GRANTED", "CONNECTED", "NOTE EXCEL.EXE fails at launch: 'The application was unable to start correctly (0xc0000142)'",
   "NOTE outside Tier 1 scope - ESCALATED to Tier 2 (desktop engineering). Fix is documented in internal KB; look it up by error code.",
   "DISCONNECTED", "LOGGED_OUT"])
s("RS-4483", "2026-09-29 09:10", "kbrooks", "nbennett", "INC-10420", "Windows Remote Assistance",
  ["INVITE_SENT", "USER_ACCESS_GRANTED", "CONNECTED", "NOTE added user to Sales Teams channel, verified access", "NOTE tech left for break"])
s("RS-4486", "2026-09-29 09:24", "kbrooks", "sfischer", "INC-10415", "Cisco Webex",
  ["ONE_TIME_CODE_ISSUED", "USER_ACCESS_GRANTED", "CONNECTED", "NOTE showed user Outlook signature settings", "DISCONNECTED", "LOGGED_OUT"])
with open(f"{OUT}/remote_sessions.log", "w") as f:
    f.write("# Remote support gateway -- session audit log -- 2026-09-29\n")
    f.write("# Every session should: get user consent, connect, do the work, then DISCONNECT and LOG OUT.\n")
    for sid, t, tech, user, ticket, tool, evs in sess:
        base = datetime.strptime(t, "%Y-%m-%d %H:%M")
        f.write(f"{base:%Y-%m-%d %H:%M:%S} {sid} START tech={tech} user={user} ticket={ticket} tool=\"{tool}\"\n")
        for j, e in enumerate(evs, 1):
            f.write(f"{base + timedelta(minutes=j * 2, seconds=rng.randint(0,59)):%Y-%m-%d %H:%M:%S} {sid} {e}\n")
    f.write("# end of log\n")
ANS["open_session"] = "RS-4483"
ANS["no_consent_session"] = "RS-4479"

# ---------------------------------------------------------------- KB index
kb = [
    ("KB0105", "Outlook repeatedly prompts for password (Microsoft 365)", "Credential prompt loop", "Clear cached credentials in Credential Manager; re-sign in.", "RC-P0W3"),
    ("KB0142", "Copier error SC-542 (fuser temperature)", "SC-542, fuser error, streaks", "Power-cycle once; if error persists, open vendor service call. Do not open the fuser.", "RC-F7X2"),
    ("KB0217", "Wireless adapter 'not present' after driver update", "WLAN adapter missing, Code 10", "Roll back adapter driver in Device Manager; pause driver updates.", "RC-W1F1"),
    ("KB0288", "Office apps fail to start: 0xc0000142", "EXCEL.EXE / WINWORD.EXE 0xc0000142 at launch", "Run Office Quick Repair; if it fails, Online Repair. Check for pending reboot first.", "RC-OFC142"),
    ("KB0317", "Teams sign-in error caa70004", "caa70004 after password change", "Sign out of Teams, clear Teams cache, sign back in.", "RC-T70K"),
    ("KB0350", "Shared mailbox missing from Outlook", "Shared mailbox not listed", "Re-add via Account Settings; wait for automapping.", "RC-SMB9"),
    ("KB0402", "Blue screen 0x7E after graphics driver update", "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED", "Safe Mode, roll back GPU driver, block driver update.", "RC-BSD7E"),
    ("KB0419", "Scanner guns fail to sync with WMS", "Scanners offline, dock sync failed", "Check WMS service on APP-02; restart sync service.", "RC-WMS4"),
]
with open(f"{OUT}/internal_kb_index.txt", "w") as f:
    f.write(f"{CO} internal knowledge base -- article index (Tier 1 view)\n")
    f.write("Search this index by symptom or error code before researching elsewhere.\n")
    f.write("=" * 70 + "\n\n")
    for kid, title, sym, fix, rc in kb:
        f.write(f"{kid}  {title}\n    Symptoms / codes: {sym}\n    Resolution: {fix}\n    Resolution code (enter in ticket): {rc}\n\n")
ANS["kb_teams"] = "KB0317"
ANS["boss_code"] = "RC-OFC142"

# ---------------------------------------------------------------- AI prompts
with open(f"{OUT}/ai_prompts.txt", "w") as f:
    f.write("""Prompts Tier 1 techs typed into a public AI chatbot last week
(pulled from browser history during a policy review)
=====================================================================
PROMPT 1
  wifi broke fix

PROMPT 2
  User dana.kim@sawgrasslogistics.example can't get into the VPN. Her
  password is Tr0pic@l!2026 and her employee ID is 44817. What's wrong
  with her account?

PROMPT 3
  Why is Outlook slow?

PROMPT 4
  I'm a Tier 1 help desk tech. A Windows 11 laptop with an Intel AX211
  Wi-Fi adapter shows "wireless adapter is not present" right after a
  driver update to 23.60.0.9. Other devices on the same network connect
  fine. Give me concise, step-by-step troubleshooting in the order I
  should try them, starting with the least disruptive.

PROMPT 5
  Write me something about printers.
""")
ANS["prompts"] = "2,4"

# ---------------------------------------------------------------- forum threads
with open(f"{OUT}/research_results.txt", "w") as f:
    f.write("""Research results for: "Outlook Microsoft 365 keeps asking for password"
You need to pick what to try FIRST and what to AVOID.
=====================================================================
[A] techforum-archive.example -- posted 2013-03-11
    "Fix for Outlook 2010 on Windows 7: open regedit, delete the whole
     HKCU\\Software\\Microsoft\\Office key and reboot. Worked for me!"

[B] free-outlook-fixer.example -- "Outlook Password Fixer PRO"
    "Download OutlookFixPro_setup.exe (free!) - fixes ALL password
     prompts in one click. Disable your antivirus before installing."

[C] support.microsoft.com -- "Outlook keeps prompting for password"
    Last updated: 2026-07 | Applies to: Outlook for Microsoft 365
    Official steps: check Credential Manager, verify modern authentication,
    update Office, recreate profile if needed.

[D] reddit.com/r/sysadmin -- posted 2026-08
    Thread: "M365 password loop after tenant change - what worked for us"
    Practical tips from admins; several replies reference the Microsoft
    article above.
""")
ANS["research"] = "C,B"

# ---------------------------------------------------------------- AI chat export (hallucination)
with open(f"{OUT}/ai_chat_export.txt", "w") as f:
    f.write("""AI assistant chat export (tech: K. Brooks)
=====================================================================
Tech: A Windows 11 PC can reach IP addresses but websites won't load by
      name. What commands should I try?

AI:   Here are commands to run in an elevated Command Prompt, in order:
        1. ipconfig /flushdns      - clears the local DNS resolver cache
        2. ipconfig /registerdns   - refreshes DHCP leases and re-registers DNS names
        3. ipconfig /release       - releases the current IP address
        4. ipconfig /renew         - requests a new IP address
        5. ipconfig /resetstack    - resets the entire TCP/IP stack to defaults
        6. netsh winsock reset     - resets the Winsock catalog (reboot after)
      Let me know if you need anything else!

Lead's note: "Cross-reference before you run anything. One of these is not a
real ipconfig option. Verify against Microsoft's command reference."
""")
ANS["fake_switch"] = "/resetstack"

# ---------------------------------------------------------------- app installs
with open(f"{OUT}/app_install_audit.log", "w") as f:
    f.write("""# Endpoint software install audit -- week of 2026-09-21
# time | host | user | package | source
2026-09-21 09:12 | ACC-PC07 | rdelgado | Microsoft Teams (work or school) 25.x | Microsoft Store
2026-09-21 13:40 | SLS-LT12 | nbennett | Zoom Workplace 6.x | Company Portal (approved)
2026-09-22 08:55 | DSP-PC03 | wturner  | 7-Zip 24.x | Company Portal (approved)
2026-09-22 15:18 | HR-LT04  | lortega  | PDFEditorPro_FREE_Setup.exe | http://free-pdf-editor-download.example/dl/setup.exe
2026-09-23 10:02 | WH-PC11  | ochen    | Microsoft Power BI Desktop | Microsoft Store
2026-09-24 11:31 | FRT-KSK1 | ithompson| Google Chrome Enterprise | Company Portal (approved)
2026-09-25 14:07 | ACC-PC02 | gliu     | Adobe Acrobat Reader | Company Portal (approved)
""")
ANS["untrusted_file"] = "PDFEditorPro_FREE_Setup.exe"

with open(f"{OUT}/store_install_errors.txt", "w") as f:
    f.write("""Four users could not install an app from an approved marketplace.
Classify each as:  P = Permissions denied   C = Compatibility   I = Interrupted download
=====================================================================
USER 1  Microsoft Store: "This app requires Windows 11 version 22H2 or later."
        Device is running Windows 10.
USER 2  Download reached 67%, laptop moved from dock to Wi-Fi, then:
        "Something unexpected happened. Package could not be verified (corrupt)."
USER 3  "Your organization has blocked this app. Ask your IT admin for
        permission to install it."
USER 4  Google Play: "Your device isn't compatible with this version."
""")
ANS["store"] = "CIPC"

with open(f"{OUT}/email_tickets.txt", "w") as f:
    f.write("""Three email / collaboration tickets. Classify the most likely issue type:
  CFG = Configuration error    NET = Connectivity problem    SYN = Account synchronization failure
=====================================================================
TICKET 1  After the mail migration, Outlook on Ben's new laptop can receive
          but not send. His profile shows outgoing server smtp.oldhost.example
          on port 25; everyone else uses the new server on port 587.

TICKET 2  Chloe's phone shows today's email and calendar changes. Outlook on
          her desktop says "Last updated 3 days ago" and her phone's calendar
          edits never appear on the desktop. Internet on the desktop is fine.

TICKET 3  Frank is at a hotel. Outlook says "Disconnected" and Teams says
          "Can't connect." His browser opens only the hotel's Wi-Fi sign-in
          page, which he hasn't accepted yet.
""")
ANS["email"] = "CFG,SYN,NET"

with open(os.path.join(os.path.dirname(__file__), "answers.json"), "w") as f:
    json.dump(ANS, f, indent=2, default=str)
print(json.dumps(ANS, indent=2, default=str))
