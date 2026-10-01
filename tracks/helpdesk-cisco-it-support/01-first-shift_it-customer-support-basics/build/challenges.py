"""Challenge definitions for Help Desk: First Shift. Flags are built from answers.json."""
import json, os, re

A = json.load(open(os.path.join(os.path.dirname(__file__), "answers.json")))

CI = "case_insensitive"
def exact(s):
    """Case-insensitive exact answer, tolerant of surrounding spaces."""
    return ("regex", r"^\s*" + re.escape(s) + r"\s*$", CI)
def words(*parts):
    """Words separated by space/underscore/hyphen, optional trailing s."""
    return ("regex", r"^\s*" + r"[\s_-]*".join(re.escape(p) for p in parts) + r"s?\s*$", CI)
def seq(*items):
    """Items in this order, any separator (comma, space, dash)."""
    parts = [("0?" + re.escape(str(i))) if str(i).isdigit() else re.escape(str(i)) for i in items]
    lead = r"^\D*?" if str(items[0]).isdigit() else r"^\s*"
    return ("regex", lead + r"[\s,;/-]+".join(parts) + r"\s*$", CI)
def letters(s):
    """Letter sequence, separators optional: DEACB, D-E-A-C-B, D,E,A,C,B."""
    return ("regex", r"^\s*" + r"[\s,;-]*".join(re.escape(c) for c in s) + r"\s*$", CI)
def ticket(t):
    n = t.split("-")[1]
    return ("regex", r"^\s*(INC[\s-]?)?" + n + r"\s*$", CI)
def number(n):
    return ("regex", r"^\s*" + re.escape(str(n)) + r"(\.0+)?\s*%?\s*(min(ute)?s?)?\s*$", CI)

CAT = {
    1: "01 Orientation (1.1)",
    2: "02 Front Line (1.2)",
    3: "03 Paper Trail (1.3)",
    4: "04 Troubleshooting (2.1)",
    5: "05 Remote Access (2.2)",
    6: "06 Research Desk (2.3)",
    7: "07 App Support (2.4)",
    8: "08 Boss Ticket",
}
ANSWER_NOTE = "\n\n*Answers are not case-sensitive.*"

C = []
def ch(name, cat, value, desc, flags, hints=(), files=(), tags=(), max_attempts=0, requires=()):
    C.append(dict(name=name, category=CAT[cat], value=value, description=desc.strip() + ANSWER_NOTE,
                  flags=list(flags), hints=list(hints), files=list(files), tags=list(tags),
                  max_attempts=max_attempts, requires=list(requires)))

# ============================================================ 01 Orientation (1.1)
ch("Clock In", 1, 50, """
Welcome to **Sawgrass Logistics IT**. You're the newest Tier 1 help desk technician and your first shift starts now.

Every challenge gives you a situation and usually a file to investigate, just like a real ticket. Read carefully, then type your answer in the box.

To prove you're here, submit this exact text:

`first shift`
""", [exact("first shift")], tags=["CCST 1.1"])

ch("Alphabet Soup", 1, 100, """
Your lead says: *"Before you touch the queue, you need to know the promise we make to customers about how fast we respond and resolve."*

That promise has a three-letter name: **SLA**. What does SLA stand for?
""", [words("service", "level", "agreement")],
   hints=[("It's an *agreement* about a *level* of *service*.", 0)], tags=["CCST 1.1", "Y100200 07.0"])

ch("Set in Stone", 1, 100, """
Ticketing systems have many fields: category, priority, status, assigned to...

Which field is **generated automatically** by the system and **never changes** for the life of the request? (Two words.)
""", [words("ticket", "number"), words("ticket", "id"), words("ticket", "#")],
   hints=[("Look at the first column of any ticket export.", 0)], tags=["CCST 1.1"])

ch("KPI Speedrun", 1, 100, """
Which help desk **KPI** measures the percentage of issues that are solved during the customer's **first** interaction, with no callbacks or follow-ups? (Three words.)
""", [words("first", "contact", "resolution"), words("first", "call", "resolution"), exact("FCR")],
   tags=["CCST 1.1"])

ch("Queue Jumper", 1, 200, """
Open **ticket_queue_export.csv** (Excel, Google Sheets, or any text editor works).

You've just logged in. Your lead says: *"Grab the next ticket. Only take tickets that are **New** (unassigned). Highest priority first (P1 is highest). If there's a tie, take the one that's been waiting the longest."*

Which ticket do you take? (Example format: `INC-12345`)
""", [ticket(A["queue_next"])],
   hints=[("Filter the **status** column to *New*, then sort by **priority** and then **created**.", 0),
          ("There are two P1 tickets with status New. Compare their created times.", 20)],
   files=["ticket_queue_export.csv"], tags=["CCST 1.1", "Y100200 07.0"], max_attempts=5)

ch("Breach!", 1, 300, """
Use **ticket_queue_export.csv** and **sla_policy.txt**.

Your manager is preparing the weekly SLA report. Look only at tickets with status **Resolved**.

**How many resolved tickets breached their *resolution* SLA?** Enter a number.
""", [number(A["sla_breaches"])],
   hints=[("Resolution time = resolved - created. Compare it to the resolution target for that ticket's priority.", 0),
          ("In a spreadsheet: `=(L2-B2)*24` gives hours (L = resolved, B = created). Then compare with 4 / 8 / 24 / 72 depending on priority.", 30)],
   files=["ticket_queue_export.csv", "sla_policy.txt"], tags=["CCST 1.1", "Y100200 09.0"], max_attempts=6)

ch("First Contact", 1, 300, """
Use **ticket_queue_export.csv** and the FCR definition in **sla_policy.txt**.

Calculate the help desk's **First Contact Resolution (FCR)** rate for the resolved tickets in this export.

Enter a whole-number percentage (example: `75`).
""", [number(round(A["fcr_pct"]))],
   hints=[("FCR = resolved tickets with **contacts = 1**, divided by **all** resolved tickets, x 100.", 0)],
   files=["ticket_queue_export.csv", "sla_policy.txt"], tags=["CCST 1.1", "Y100200 09.0"], max_attempts=6)

ch("Fast Response", 1, 250, """
Use **ticket_queue_export.csv**.

For **resolved P1** tickets only, what is the **average First Response Time in minutes**? (first_response - created)

Enter a whole number.
""", [number(round(A["p1_avg_resp_min"]))],
   hints=[("There are 5 resolved P1 tickets. Find the minutes between created and first_response for each, then average them.", 0)],
   files=["ticket_queue_export.csv"], tags=["CCST 1.1", "Y100200 09.0"], max_attempts=6)

ch("Same Problem, Different People", 1, 200, """
Use **ticket_queue_export.csv**.

Grouping similar tickets is a key strategy for managing a busy queue. Several **open** tickets from different people are really the **same underlying problem**, even though each person describes it differently.

What is the **asset tag** of the device behind all of them?
""", [exact("CPY-2F-01")],
   hints=[("Read the description column for the tickets that are not Resolved. Look for a device mentioned more than once.", 0)],
   files=["ticket_queue_export.csv"], tags=["CCST 1.1"], max_attempts=5)

ch("Robot Coworker", 1, 250, """
Use **ticket_queue_export.csv**.

The ticketing system now uses **AI to categorize and prioritize** new tickets (see the `categorized_by` column). AI saves time, but a good tech still checks its work.

One **AI-categorized** ticket is clearly in the **wrong category** based on its description. Which ticket is it?
""", [ticket(A["ai_miscat"])],
   hints=[("Filter `categorized_by` = AI, then read each description and ask: does this category make sense?", 0),
          ("Look for a 'Hardware' ticket that has nothing to do with hardware.", 25)],
   files=["ticket_queue_export.csv"], tags=["CCST 1.1"], max_attempts=4)

# ============================================================ 02 Front Line (1.2)
ch("Open or Closed?", 2, 150, """
Good questioning finds the problem fast. **Open-ended** questions get the customer talking and explaining. **Closed-ended** questions get a specific, short answer (often yes/no or a choice).

1. What happens when you try to open the file?
2. Is the computer plugged in?
3. Can you describe what the error message says?
4. Did you restart it?
5. What were you working on when it froze?
6. Is anyone else in your office affected?
7. Are you using Chrome or Edge?
8. What changes have you noticed since the update?

Enter the numbers of the **open-ended** questions in ascending order, separated by commas (example: `2,4,6`).
""", [seq(1, 3, 5, 8)],
   hints=[("Closed-ended questions can be answered with one word: yes, no, or picking one option.", 0)],
   tags=["CCST 1.2", "Y100200 13.0"], max_attempts=5)

ch("Who's On the Line?", 2, 300, """
Open **call_transcripts.txt**. It has five calls, A through E.

Match each call to the customer type from the course. Enter the call letters in this order:

**Talkative, Rude, Knowledgeable, Angry, Inexperienced**

Example format: `ABCDE`
""", [letters(A["calls"])],
   hints=[("The **rude** customer insults the tech and asks for their favorite technician. The **angry** customer is upset about the *problem* and the wait.", 0),
          ("The talkative customer tells stories unrelated to the problem. The knowledgeable one uses technical terms and has already tried the basics.", 30)],
   files=["call_transcripts.txt"], tags=["CCST 1.2", "Y100200 13.0"], max_attempts=4)

ch("Hold, Please", 2, 250, """
Open **hold_and_transfer_call.txt**.

Your lead is reviewing this call. Some lines show the **proper** way to place a customer on hold or transfer them. **Three** lines show the improper way.

Enter the three line numbers of the **improper** hold or transfer handling in ascending order, separated by commas (example: `1,2,3`).
""", [seq(*A["hold_lines"])],
   hints=[("Proper hold: ask permission, explain why, and give a time estimate. Proper transfer: explain why, say who you're transferring to, and make sure the call isn't lost.", 0),
          ("Line 09 is an example of doing it **right**. Compare the other hold and transfer moments to it.", 25)],
   files=["hold_and_transfer_call.txt"], tags=["CCST 1.2", "Y100200 13.0"], max_attempts=4)

ch("Say It Back", 2, 200, """
Active listening means letting the customer finish, then **summarizing and paraphrasing** to confirm you understand, using simple language.

The customer says:

> "Ever since they moved me to the desk by the window on Monday, my laptop keeps dropping the Wi-Fi, maybe every twenty minutes or so, and I have to turn the Wi-Fi off and on to get it back. My old desk was fine. Teams calls cut out too."

Which summary is the best example of active listening?

- **A.** "So your wireless NIC is failing association with the AP due to RSSI degradation. Correct?"
- **B.** "Okay, the internet is broken. I'll open a ticket."
- **C.** "So since you moved to the window desk on Monday, your laptop loses Wi-Fi about every 20 minutes and you have to toggle it to reconnect, and Teams calls drop too. Is that right?"
- **D.** "Have you tried restarting it?"

Enter one letter. **You have 2 attempts.**
""", [exact("C")], tags=["CCST 1.2", "Y100200 13.0"], max_attempts=2)

# ============================================================ 03 Paper Trail (1.3)
ch("Loose Lips", 3, 200, """
Open **ticket_notes_review.txt**. These closed-ticket notes are about to be added to the knowledge base, so your lead asked you to do a QA review first.

One note breaks the rule about **confidentiality**: it includes sensitive information that should never appear in documentation.

Which ticket is it?
""", [ticket(A["notes_leak"])],
   files=["ticket_notes_review.txt"], tags=["CCST 1.2", "Y100200 17.0"], max_attempts=3)

ch("Just the Facts", 3, 200, """
Using the same file, **ticket_notes_review.txt**:

Documentation should use **professional, neutral language** and stick to facts, with no personal opinions or commentary.

Which ticket's note breaks this rule?
""", [ticket(A["notes_opinion"])],
   files=["ticket_notes_review.txt"], tags=["CCST 1.2", "Y100200 13.0"], max_attempts=3)

ch("Unfinished Business", 3, 250, """
Using the same file, **ticket_notes_review.txt**:

Good troubleshooting documentation starts with a clear problem statement, lists each step, and **concludes with the resolution or next steps**.

One note lists its steps but never tells the next tech how things ended. Which ticket is it?
""", [ticket(A["notes_missing_outcome"])],
   hints=[("Look for a note with no Outcome and no Next steps.", 0)],
   files=["ticket_notes_review.txt"], tags=["CCST 1.2"], max_attempts=3)

ch("Deja Vu", 3, 300, """
New ticket in the queue from **Diego Alvarez**: *"Blue screen errors are back since last night's Windows Update, same as last month."*

This is where good documentation pays off. Open **diego_ticket_history.txt**. You don't need to troubleshoot from scratch.

Last month, which **graphics driver version** was confirmed as the stable version to roll back to? Enter the version number exactly.
""", [exact(A["diego_driver"])],
   hints=[("Read step 4 of the earlier ticket.", 0)],
   files=["diego_ticket_history.txt"], tags=["CCST 1.2", "Y100200 02.0"], max_attempts=4)

# ============================================================ 04 Troubleshooting (2.1)
ch("Eight Steps", 4, 200, """
The troubleshooting process has **eight steps**. They've been scrambled:

- **A.** Observe the results of the changes.
- **B.** Define the problem.
- **C.** Document the changes made to resolve the problem.
- **D.** Devise a plan to resolve the problem.
- **E.** Gather detailed information.
- **F.** If the problem is not resolved, repeat the process.
- **G.** Make necessary changes to implement the plan.
- **H.** Identify a probable cause of the failure.

Enter the letters in the correct order (example: `ABCDEFGH`).
""", [letters(A["eight_steps"])],
   hints=[("It starts with defining the problem and ends with documenting.", 0)],
   tags=["CCST 1.3", "Y100200 02.0", "Y100200 14.0"], max_attempts=5)

ch("One Thing at a Time", 4, 250, """
Open **troubleshooting_log_kyle.txt**. Kyle fixed the problem, but his lead isn't happy.

When you implement a plan, you should **make only one change at a time** so you can track what actually fixed it. Kyle's log also shows what happens when you don't.

Enter the **entry number** where Kyle broke the one-change-at-a-time rule.
""", [number(A["kyle_entry"])],
   hints=[("Look at entry 8. Why couldn't Kyle explain the fix?", 0)],
   files=["troubleshooting_log_kyle.txt"], tags=["CCST 1.3", "Y100200 02.0"], max_attempts=2)

ch("What Changed?", 4, 300, """
**Ticket:** *"The laptop in training Room 114 just stopped connecting to Wi-Fi Monday morning. Phones and other laptops in the room connect fine."*

Other devices connect, so you've already **eliminated the router**. Now **gather information**: *Has anything changed recently?*

Open **room114_laptop_events.txt**. What is the **version number of the driver** installed right before the problem started?
""", [exact(A["room114_driver"])],
   hints=[("Find the first 'adapter is not present' event, then look at what was installed just before it.", 0),
          ("Watch out: one update happened *after* the problem began, and another driver update happened weeks earlier while Wi-Fi still worked.", 25)],
   files=["room114_laptop_events.txt"], tags=["CCST 1.3", "Y100200 02.0", "Y100200 14.0"], max_attempts=4)

# ============================================================ 05 Remote Access (2.2)
ch("Right Tool, Right Job", 5, 250, """
Match each situation to the **best** remote access tool:

- **A.** Microsoft Remote Desktop
- **B.** Windows Remote Assistance
- **C.** Cisco Webex
- **D.** Remote Desktop (macOS)
- **E.** TeamViewer

1. A user wants quick, **one-time** help. You want a simple tool that is **built into Windows**, where the user invites you.
2. The design department uses **only Apple computers**. You need screen sharing, file transfer, and to run commands on them.
3. You're **training 10 staff members** at once and need video, screen sharing, and collaboration.
4. You need to support a user's **Android phone and their Windows PC**. You want one **cross-platform** tool.
5. You need to connect to a **Windows 11 Pro office workstation** to use its files, apps, and network resources as if you were sitting at it.

Enter the letters for situations 1 through 5 in order (example: `ABCDE`).
""", [letters("BDCEA")],
   hints=[("Remote Assistance is for quick one-time sessions. Remote Desktop is for connecting to a Windows Pro or Enterprise PC as if you were there.", 0)],
   tags=["CCST 6.1", "Y100200 15.0"], max_attempts=4)

ch("Who Let You In?", 5, 250, """
Open **remote_sessions.log**.

Security is crucial in remote support. The **user must confirm or grant access** before a tech connects to their device.

Which session **connected without the user granting access**? (Example format: `RS-0000`)
""", [exact(A["no_consent_session"]), exact(A["no_consent_session"].replace("RS-", ""))],
   hints=[("Look for a session that has CONNECTED but no USER_ACCESS_GRANTED before it.", 0)],
   files=["remote_sessions.log"], tags=["CCST 6.1", "Y100200 17.0"], max_attempts=4)

ch("Close the Door", 5, 250, """
Using **remote_sessions.log** again:

Step 4 of a remote session is **close the session**: disconnect and **log out to prevent lingering remote access**.

Which session was **left open**?
""", [exact(A["open_session"]), exact(A["open_session"].replace("RS-", ""))],
   hints=[("Every session should end with DISCONNECTED and LOGGED_OUT. Find the one that doesn't.", 0)],
   files=["remote_sessions.log"], tags=["CCST 6.1", "Y100200 17.0"], max_attempts=4)

# ============================================================ 06 Research Desk (2.3)
ch("Stop Code Detective", 6, 200, """
A user reads you a blue screen code: **0x0000009F**.

Including the error code in your search gives much better results. Look it up using a **reputable source** (Microsoft's documentation is best).

What is the **symbolic name** of this bug check? Enter it in ALL_CAPS_WITH_UNDERSCORES the way Microsoft writes it.
""", [("regex", r"^\s*driver[\s_]power[\s_]state[\s_]failure\s*$", CI)],
   hints=[("Search: `bug check 0x9F site:learn.microsoft.com`", 0)],
   tags=["CCST 6.2", "Y100200 03.0"], max_attempts=5)

ch("Trust but Verify", 6, 300, """
Open **ai_chat_export.txt**. A tech asked an AI assistant for DNS troubleshooting commands.

AI responses depend on their input and training data, and **they can be wrong**. Always cross-reference AI answers with a reliable source before acting on them.

One of the listed commands uses an `ipconfig` option that **does not exist**. Enter that option exactly as written (example: `/option`).
""", [("regex", r"^\s*(ipconfig\s+)?/?resetstack\s*$", CI)],
   hints=[("Open Command Prompt and run `ipconfig /?`, or check Microsoft's ipconfig command reference.", 0)],
   files=["ai_chat_export.txt"], tags=["CCST 6.2", "Y100200 03.0"], max_attempts=3)

ch("Prompt Check", 6, 250, """
Open **ai_prompts.txt**. These prompts were typed into a **public** AI chatbot.

Answer two questions:
1. Which prompt number **breaks privacy rules** by entering sensitive data into a public AI tool?
2. Which prompt number is the **best-written** (clear, specific, with context and a desired format)?

Enter both numbers as `privacy,best` (example: `1,5`).
""", [seq(*A["prompts"].split(","))],
   hints=[("Sensitive data includes passwords, IDs, and personal email addresses. A good prompt includes context, details, and the format you want.", 0)],
   files=["ai_prompts.txt"], tags=["CCST 6.2", "Y100200 17.0"], max_attempts=3)

ch("Source Check", 6, 200, """
Open **research_results.txt**. You searched for a fix for an Outlook password loop.

1. Which result should you **try first** (most reputable and current)?
2. Which result should you **avoid entirely** because it's a security risk?

Enter the two letters as `first,avoid` (example: `A,D`).
""", [seq(*A["research"].split(","))],
   hints=[("Prioritize the manufacturer's own site. Be wary of unknown download sites, especially any that tell you to turn off antivirus.", 0)],
   files=["research_results.txt"], tags=["CCST 6.2"], max_attempts=2)

ch("Check the KB First", 6, 200, """
**Ticket:** *"Teams shows error caa70004 after I changed my password."*

Before searching the internet, check whether a teammate has already solved this. Open **internal_kb_index.txt**.

Which **KB article** covers this issue? (Example format: `KB0000`)
""", [exact(A["kb_teams"])],
   files=["internal_kb_index.txt"], tags=["CCST 6.2"], max_attempts=4)

# ============================================================ 07 App Support (2.4)
ch("Where'd You Get That?", 7, 200, """
Open **app_install_audit.log**.

Apps from **untrusted or unknown sources** can carry malware and never get updates. One install this week didn't come from an approved marketplace or the Company Portal.

Enter the **file name** of that installer.
""", [exact(A["untrusted_file"])],
   files=["app_install_audit.log"], tags=["CCST 4.5", "Y100200 05.0"], max_attempts=4)

ch("Why Won't It Install?", 7, 250, """
Open **store_install_errors.txt**. Four users couldn't install apps from an **approved marketplace**.

Classify each one:
- **P** = Permissions denied
- **C** = Compatibility
- **I** = Interrupted download

Enter the four letters for users 1 through 4 in order (example: `PPCI`).
""", [letters(A["store"])],
   files=["store_install_errors.txt"], tags=["CCST 4.5", "Y100200 03.0"], max_attempts=3)

ch("Mail Call", 7, 250, """
Open **email_tickets.txt**. Email and collaboration tools usually fail in one of three ways: **configuration errors**, **connectivity problems**, or **account synchronization failures**.

Classify tickets 1 through 3 using the codes **CFG**, **NET**, or **SYN**.

Enter them in order separated by commas (example: `NET,NET,CFG`).
""", [seq(*A["email"].split(","))],
   files=["email_tickets.txt"], tags=["CCST 4.5", "Y100200 04.0"], max_attempts=3)

# ============================================================ 08 Boss
ch("The CFO's Month-End Meltdown", 8, 500, """
**Ticket priority: P1.** The CFO can't open Excel, and month-end close is due today.

A Tier 1 tech connected remotely and **escalated** the ticket. Tier 2 is swamped and sent you one line:

> *"The fix is already in the internal KB. Find it and put the **resolution code** in the ticket so we can close this."*

Nobody gave you the ticket number, the error, or the article, so you'll have to follow the paper trail:

1. **ticket_queue_export.csv**: find the CFO's ticket.
2. **remote_sessions.log**: find the session for that ticket and read the tech's notes.
3. **internal_kb_index.txt**: find the matching article.

Enter the **resolution code** (example format: `RC-XXXX`).
""", [exact(A["boss_code"])],
   hints=[("The session notes include an error code in parentheses. Search the KB index for that code.", 50)],
   files=["ticket_queue_export.csv", "remote_sessions.log", "internal_kb_index.txt"],
   tags=["CCST 1.1", "CCST 6.1", "CCST 6.2", "CCST 4.5"], max_attempts=3,
   requires=["Queue Jumper", "Close the Door", "Check the KB First"])

if __name__ == "__main__":
    print(len(C), "challenges,", sum(c["value"] for c in C), "points")
    from collections import Counter
    for k, v in sorted(Counter(c["category"] for c in C).items()):
        print(f"  {k}: {v}")
