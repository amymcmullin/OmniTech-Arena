"""Build the facilitator guide (HTML -> PDF) with answer key."""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import challenges as CH
A = CH.A

WHY = {
 "Clock In": ("first shift", "Teaches the answer box. Everyone should get this in the first minute."),
 "Alphabet Soup": ("Service Level Agreement", "Sets expectations for response and resolution times (1.1)."),
 "Set in Stone": ("ticket number (ticket ID also accepted)", "The unique, auto-generated identifier that never changes."),
 "KPI Speedrun": ("First Contact Resolution (FCR, first call resolution also accepted)", "KPI named in the Module 1 new-terms list."),
 "Queue Jumper": (A["queue_next"], "Two New P1 tickets: INC-10408 (dispatch floor, 07:18) and INC-10417 (warehouse scanners, 08:03). The oldest one wins. INC-10412 is also P1, but it's already In Progress."),
 "Breach!": (str(A["sla_breaches"]), "Breaching tickets: " + ", ".join(A["sla_breach_ids"]) + ". Resolution hours compared with 4/8/24/72."),
 "First Contact": ("64", "16 of 25 resolved tickets have contacts = 1. 16/25 = 64%."),
 "Fast Response": ("12", "P1 first-response minutes: 8, 12, 22, 5, 13. Average 12. Check this against the 15-minute target as a discussion point."),
 "Same Problem, Different People": ("CPY-2F-01", "Tickets " + ", ".join(A["copier_tickets"]) + " describe the same copier four different ways. Group them and work one root cause. KB0142 covers SC-542."),
 "Robot Coworker": (A["ai_miscat"], "Grace Liu's account lockout was AI-categorized as Hardware. It should be Account/Access, and it's arguably P2. This is a good talking point about checking AI output."),
 "Open or Closed?": ("1,3,5,8", "Numbers 2, 4, 6 and 7 can be answered yes/no or by picking one option. Any separator is accepted."),
 "Who's On the Line?": ("DEACB", "Talkative = D (wedding story), Rude = E (insults, wants Marcus), Knowledgeable = A (already flushed DNS), Angry = C (lost work, long hold), Inexperienced = B (\"the blue e\")."),
 "Hold, Please": ("6,13,18", "06 holds without asking or giving a time. 13 transfers without explaining why or to whom. 18 is a cold bounce back to the queue that drops the call. 09 is the model of doing it right, and 20 shows recovery and ownership."),
 "Say It Back": ("C", "C paraphrases accurately in plain language and confirms. A is jargon, B is too vague, and D skips listening. Limited to 2 attempts."),
 "Loose Lips": (A["notes_leak"], "The user's password is written into the ticket note, which breaks confidentiality."),
 "Just the Facts": (A["notes_opinion"], "Personal opinion and a stereotype about the user's department."),
 "Unfinished Business": (A["notes_missing_outcome"], "Steps are listed, but there's no Outcome or Next steps."),
 "Deja Vu": (A["diego_driver"], "Step 4 of INC-09811. This is the course's Diego blue-screen scenario, extended to show why documentation matters."),
 "Eight Steps": ("BEHDGAFC", "Define, Gather, Probable cause, Plan, Implement, Observe, Repeat, Document."),
 "One Thing at a Time": ("6", "Entry 6 makes four changes at once, which is why entry 8 can't explain the fix. Kyle also never documented anything useful (a discussion point)."),
 "What Changed?": (A["room114_driver"], "Installed 9/26 16:22, followed by 'requires further installation' and then 'adapter not present' on Monday. The Defender update came after the failure, and 23.40.0.4 worked for weeks. KB0217 has the fix."),
 "Right Tool, Right Job": ("BDCEA", "1 Remote Assistance, 2 macOS Remote Desktop, 3 Webex, 4 TeamViewer, 5 Microsoft Remote Desktop."),
 "Who Let You In?": (A["no_consent_session"], "VNC session connected with 'admin override - user prompt skipped'. There's no USER_ACCESS_GRANTED."),
 "Close the Door": (A["open_session"], "It never logs DISCONNECTED or LOGGED_OUT, and the tech 'left for break'. RS-4483 also accepted without the prefix."),
 "Stop Code Detective": ("DRIVER_POWER_STATE_FAILURE", "Bug check 0x9F (Microsoft Learn). Needs internet access. Spaces instead of underscores are accepted."),
 "Trust but Verify": ("/resetstack", "Not a real ipconfig switch. The real reset is `netsh int ip reset`. The other five commands are real. Students can check with `ipconfig /?`."),
 "Prompt Check": ("2,4", "2 leaks an email, a password and an employee ID into a public AI. 4 has role, context, the specific error, the format and the ordering."),
 "Source Check": ("C,B", "Try C first (Microsoft, current). Avoid B (unknown .exe that says to disable antivirus). A is outdated (Outlook 2010 / Windows 7) and deletes a whole registry key. D is useful but secondary."),
 "Check the KB First": (A["kb_teams"], "Matches caa70004 after a password change."),
 "Where'd You Get That?": (A["untrusted_file"], "Downloaded from an unknown website rather than the Store or Company Portal."),
 "Why Won't It Install?": ("CIPC", "1 needs Windows 11 (C), 2 corrupt download after a network change (I), 3 blocked by the org (P), 4 device not supported (C)."),
 "Mail Call": ("CFG,SYN,NET", "1 wrong SMTP server and port, 2 desktop not syncing while the network is fine, 3 hotel captive portal not accepted."),
 "The CFO's Month-End Meltdown": (A["boss_code"], "INC-10412 (CFO) leads to session RS-4480, which notes 0xc0000142 and 'look up by error code'. That points to KB0288, resolution code RC-OFC142. It unlocks after Queue Jumper, Close the Door and Check the KB First."),
}
assert set(WHY) == {c["name"] for c in CH.C}, set(WHY) ^ {c["name"] for c in CH.C}

rows = []
cur = None
for c in CH.C:
    if c["category"] != cur:
        cur = c["category"]
        rows.append(f'<tr class="cat"><td colspan="4">{html.escape(cur)}</td></tr>')
    ans, why = WHY[c["name"]]
    files = "<br>".join(c["files"]) or "&ndash;"
    lim = f' <span class="lim">{c["max_attempts"]} tries</span>' if c["max_attempts"] else ""
    rows.append(f"<tr><td><b>{html.escape(c['name'])}</b><br><span class=pts>{c['value']} pts</span>{lim}</td>"
                f"<td class=ans>{html.escape(ans)}</td><td>{html.escape(why)}</td><td class=files>{files}</td></tr>")

total = sum(c["value"] for c in CH.C)
doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Help Desk: First Shift - Facilitator Guide</title>
<style>
@page {{ size: letter; margin: 0.6in 0.55in; }}
body {{ font-family: "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10pt; color:#1b1f24; line-height:1.4; }}
h1 {{ font-size: 22pt; margin: 0 0 2pt; color:#0b3d5c; }}
h2 {{ break-after: avoid; font-size: 13.5pt; color:#0b3d5c; border-bottom: 2px solid #0b3d5c; padding-bottom:2pt; margin-top:18pt; }}
h3 {{ font-size: 11pt; margin: 12pt 0 4pt; }}
.sub {{ color:#555; font-size:11pt; margin-bottom:10pt; }}
.box {{ background:#f2f6f9; border-left:4px solid #0b3d5c; padding:6pt 10pt; margin:8pt 0; }}
.warn {{ background:#fff6e5; border-left:4px solid #c77700; padding:6pt 10pt; margin:8pt 0; }}
code, .ans {{ font-family: Consolas, "Courier New", monospace; }}
code {{ background:#eef1f4; padding:0 3px; border-radius:3px; font-size:9pt; }}
table {{ border-collapse: collapse; width:100%; font-size:8.8pt; table-layout:fixed; }} tr {{ break-inside: avoid; }}
th, td {{ border:1px solid #c9d1d9; padding:4pt 5pt; vertical-align:top; text-align:left; }}
th {{ background:#0b3d5c; color:#fff; }}
tr.cat td {{ background:#dde8f0; font-weight:700; color:#0b3d5c; }}
td.ans {{ font-weight:700; color:#8a1c1c; word-break:break-word; }}
td.files {{ font-size:7.8pt; color:#444; }}
.pts {{ color:#555; font-size:8pt; }} .lim {{ color:#c77700; font-size:8pt; }}
ol li, ul li {{ margin-bottom:3pt; }}
.grid {{ display:grid; grid-template-columns: 1fr 1fr; gap: 0 18pt; }}
.pb {{ page-break-before: always; }}
.small {{ font-size:8.5pt; color:#555; }}
</style></head><body>

<h1>Help Desk: First Shift</h1>
<div class="sub">A CTF for Cisco NetAcad <b>IT Customer Support Basics</b> (Modules 1&ndash;2) &middot; Facilitator guide &amp; answer key &middot; <b>Instructor only</b></div>

<div class="box"><b>At a glance:</b> {len(CH.C)} challenges &middot; {total:,} points &middot; 8 categories that follow course topics 1.1&ndash;2.4 &middot; 16 evidence files &middot; tested on CTFd 3.8.6 &middot; about 90&ndash;120 minutes &middot; individual play &middot; students need a spreadsheet app and a text editor, and internet for one challenge (Stop Code Detective).</div>

<h2>The story</h2>
<p>Students are the newest Tier 1 technicians at <b>Sawgrass Logistics</b>, a fictional company. They work a real-looking ticket queue, review call transcripts and ticket notes, read remote-support audit logs, and check AI output and research sources. Most flags come from <b>analyzing evidence</b>, not recalling facts. Only four challenges are straight vocabulary (warm-ups). The locked boss ticket makes students chain three files, which is what a real escalation looks like.</p>

<h2>Setup</h2>
<ol>
<li>Set up CTFd and finish the setup wizard. See <code>docs/platform-setup.md</code> in the OmniTech-Arena repository.</li>
<li>In CTFd as admin: <b>Settings &rarr; Access Tokens &rarr; Generate</b>.</li>
<li>From the repository root: <code>pip install requests</code>, then<br><code>python tools/deploy.py tracks/helpdesk-cisco-it-support/01-first-shift_it-customer-support-basics --url http://&lt;host&gt;:8000 --token ctfd_...</code></li>
<li>Look for <code>Done: {len(CH.C)} challenges loaded.</code> Run it <b>once</b>. Other games aren't touched. Add <code>--hidden</code> to load the game hidden.</li>
<li>One time per server: paste the two sort functions from <code>docs/platform-setup.md</code> into <b>Admin Panel &rarr; Config &rarr; Theme</b> so each game's categories stay grouped.</li>
</ol>
<h2>Running the event</h2>
<table>
<tr><th style="width:17%">Time</th><th>What happens</th></tr>
<tr><td>0:00&ndash;0:10</td><td>Students register (tell them to use first name + last initial). Show the board. Everyone solves <b>Clock In</b>. Remind them that answers aren't case-sensitive and that some challenges have limited attempts, shown under the box.</td></tr>
<tr><td>0:10&ndash;1:30</td><td>Open play. Students choose their path. Beginners do well starting with categories 02, 03 and 04. Your spreadsheet-strong students will go straight for Breach! and First Contact.</td></tr>
<tr><td>~0:45</td><td>Check the scoreboard. If many students are stuck on Breach!, do a two-minute mini-lesson on subtracting timestamps in Excel: <code>=(resolved-created)*24</code>.</td></tr>
<tr><td>1:30&ndash;2:00</td><td>Debrief. The best discussion prompts are in the answer key: <i>Robot Coworker</i> (trusting AI), <i>Hold, Please</i> (role-play lines 06/13/18 the right way), <i>Trust but Verify</i>, and the boss ticket (why good session notes and KB articles saved the day).</td></tr>
</table>
<p class="small"><b>Hints:</b> Free hints (0 points) nudge toward the method. Paid hints cost 20&ndash;50 points and give more away. To make it easier, set all hint costs to 0 in the Admin panel. To make it harder, delete the free hints.</p>

<h2>Curriculum alignment</h2>
<p class="small">Each challenge is tagged in CTFd with its CCST IT Support objective (1.1, 1.2, 1.3, 4.5, 6.1, 6.2) and, where it fits, a Y100200 standard: 02.0 troubleshooting, 03.0 OS &amp; software, 04.0 networking, 05.0 security threats, 07.0 operational procedures, 09.0 math, 13.0 communication, 14.0 problem solving, 15.0 IT tools, 17.0 ethics &amp; legal. Tags show on each challenge card, so students can see what each one practices.</p>

<h2>Answer key</h2>
<p class="small">Flags accept reasonable formatting: <code>INC-10408</code> or <code>10408</code>, <code>1,3,5,8</code> or <code>1 3 5 8</code>, <code>DEACB</code> or <code>D-E-A-C-B</code>. The order still matters. Every answer below was submitted by a test student account on a live CTFd 3.8.6 install and accepted, and several wrong answers were checked and rejected.</p>
<table>
<tr><th style="width:18%">Challenge</th><th style="width:15%">Answer</th><th>Why / discussion</th><th style="width:17%">Files</th></tr>
{''.join(rows)}
</table>

<h2>Extending it</h2>
<ul>
<li><b>Write-up round (not auto-graded):</b> after the boss, have students write the full ticket note for INC-10412 using the Module 1.3 format (issue, steps, outcome, next steps, no sensitive data). Grade it in Canvas.</li>
<li><b>Role-play round:</b> pairs act out calls C and E from <code>call_transcripts.txt</code>, then redo <code>hold_and_transfer_call.txt</code> lines 06, 13 and 18 correctly.</li>
<li><b>Reuse:</b> <code>challenges.json</code> is plain text. Change the answers in the evidence files and flags to make a new version for each semester.</li>
</ul>
</body></html>"""
out = os.path.join(os.path.dirname(__file__), "guide.html")
open(out, "w").write(doc)
print("wrote", out)
