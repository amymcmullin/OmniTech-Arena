"""Game 2 facilitator guide (HTML -> PDF)."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import challenges as CH
A = CH.A

WHY = {
 "Promoted!": ("second shift", "Warm-up. Teaches where to type answers."),
 "Four Ways to Project": ("BCDA", "1 Duplicate, 2 Extend, 3 Second screen only, 4 PC screen only. Students can try Win+P live."),
 "Battery Health": ("70", "39,203 / 56,004 = 70%. Have students run `powercfg /batteryreport` on their own laptops."),
 "Replace or Keep?": ("yes", "70% is below the 75% policy. Unlocks after Battery Health. One attempt."),
 "Access for Everyone": ("BCFEGDA", "Narrator, Live captions, Color filters, Sticky Keys, Mono audio, On-Screen Keyboard, Magnifier."),
 "Patch Tuesday Problems": (A["failed_kb"], "Failed twice on 9/26 and 9/27. The number alone is accepted. KB numbers are fictional."),
 "Error Code Lookup": ("0x800f0922", "Read straight from the file. 0x800f0922 is a real Windows Update error code, which makes it a good optional research follow-up."),
 "Who's Eating the CPU?": ("Microsoft OneDrive", "61.7% CPU while it syncs the copied share. OneDrive / OneDrive.exe also accepted."),
 "Memory Lane": ("Microsoft Edge", "About 1.4 GB across 14 processes. Teams is the distractor at about 905 MB."),
 "Clean Slate": ("Ctrl+Shift+Delete", "Del or Delete are both accepted, with any spacing."),
 "Fly Offline": ("B,Dock_schedule.docx", "Blue cloud = online-only. Red X = sync error. Fix: right-click > Always keep on this device."),
 "Recycle Bin Rescue": ("93", "OneDrive work/school keeps deleted items 93 days (recycle bin plus second-stage bin), so a 45-day-old folder is still recoverable. Personal accounts keep them 30 days."),
 "Boot Order": ("BDEAC", "POST > UEFI starts Boot Manager > winload.efi > ntoskrnl.exe > Winlogon."),
 "Safe Mode, Please": ("5", "4 = Safe Mode, 5 = with Networking, 6 = with Command Prompt. F5 is also accepted. Only 2 attempts."),
 "USB Won't Boot": ("Enable USB Boot Support", "It's set to Disabled, so USB never appears in the F12 menu. Secure Boot and Fast Boot are the distractors."),
 "Right Tool (Mac Edition)": ("CEADB", "Activity Monitor, Terminal, Time Machine, Spotlight, Disk Utility."),
 "Cron Job Detective": ("5,4", "1-5 = Monday to Friday, so 5 runs a week. */6 = hours 0, 6, 12 and 18, so 4 runs a day."),
 "Hypervisor Sort": ("21122", "VirtualBox 2, ESXi 1, Hyper-V 1, VMware Workstation 2, Parallels 2."),
 "Read the Permissions": ("750,invoices_sept.csv", "rwx r-x --- = 7 5 0. invoices_sept.csv is rw-rw-r--, so the group can write. The archive directory is also group-writable, but the question asks for a file."),
 "Hidden in Plain Sight": (A["flag_hidden"], "[VM] `ls -a` shows .flag_hidden. `FLAG: ...` with the prefix is also accepted."),
 "Count the Errors": (str(A["syslog_errors"]), "[VM] `grep -c ERROR logs/syslog.sample`"),
 "Knock Knock": (A["auth_top_ip"], "[VM] 37 failures from that IP. One-liner: grep \"Failed password\" | grep -oE \"from [0-9.]+\" | sort | uniq -c | sort -rn. A good discussion point about brute-force attacks."),
 "Permission Denied": (A["locked_report"], "[VM] Mode 000 (----------). Extension a student can try: `chmod 644` it and read it."),
 "Make It Run": (A["flag_exec"], "[VM] `chmod +x scripts/fix_printer.sh && cd scripts && ./fix_printer.sh`. Running it with `bash fix_printer.sh` deliberately refuses."),
 "Frozen Mac": ("Command+Option+Esc", "Cmd/Opt/Alt/Esc spellings are all accepted."),
 "Drive Swap": ("NTFS,exFAT", "macOS reads NTFS but can't write to it by default. exFAT is read/write on both and has no 4 GB limit."),
 "Ten Strikes": ("10", "iPhone Erase Data triggers after 10 failed passcode attempts."),
 "Lock, Don't Wipe": (A["bad_wipe"], "'Misplaced somewhere in the office' is lost, not stolen, so it should have been lock and locate."),
 "Pocket Rules": ("D", "MDM can't read a user's passcode. It can clear or reset it on supervised devices. Only 2 attempts."),
 "Battery Vampire": (A["battery_app"], "41% and 6h 48m in the background. Fix: limit Background App Refresh or location to 'While Using'."),
 "Hotspot Not Found": ("2.4 GHz", "The adapter is 2.4 GHz-only and the hotspot broadcasts 5 GHz only. '2.4' is accepted."),
 "Permission Creep": (A["bad_app"], "A flashlight needs only the camera (flash), not contacts, location, the microphone or call logs."),
 "Stuck in the Outbox": ("587", "The user has port 25, which is often blocked. SMTP submission with STARTTLS uses 587."),
 "As a Service": ("SIPSI", "M365 SaaS, EC2 IaaS, App Service PaaS, Gmail SaaS, Compute Engine IaaS."),
 "The Big Three": ("Google", "Google Cloud / GCP also accepted."),
 "Cloud Deployment": ("Hybrid", "On-premises (private) plus public cloud, managed together."),
 "The Board Meeting Lockout": (A["boss_key"], "Match Key ID 9C3E71A4, not just LT-0611 (it has 2 keys), and not LT-0612's look-alike 9C3E7F02. The newer LT-0611 key is a trap. Dashes are optional. Unlocks after Safe Mode, Please; Patch Tuesday Problems; and Lock, Don't Wipe."),
}
assert set(WHY) == {c["name"] for c in CH.C}

rows, cur = [], None
for c in CH.C:
    if c["category"] != cur:
        cur = c["category"]; rows.append(f'<tr class="cat"><td colspan="4">{html.escape(cur)}</td></tr>')
    ans, why = WHY[c["name"]]
    lim = f' <span class="lim">{c["max_attempts"]} tries</span>' if c["max_attempts"] else ""
    req = f'<br><span class="lim">unlocks after: {html.escape(", ".join(c["requires"]))}</span>' if c["requires"] else ""
    rows.append(f"<tr><td><b>{html.escape(c['name'])}</b><br><span class=pts>{c['value']} pts</span>{lim}{req}</td>"
                f"<td class=ans>{html.escape(ans)}</td><td>{html.escape(why)}</td><td class=files>{'<br>'.join(c['files']) or '&ndash;'}</td></tr>")
total = sum(c["value"] for c in CH.C)
nfiles = len(os.listdir(os.path.join(HERE, "..", "files")))
theme_json = '{"challenge_category_order": "function(a, b) { return a.localeCompare(b, undefined, {numeric: true}); }", "challenge_order": "function(a, b) { return a.value - b.value || a.name.localeCompare(b.name); }"}'

doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Help Desk: Second Shift - Facilitator Guide</title>
<style>
body {{ font-family: "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10pt; color:#1b1f24; line-height:1.4; }}
h1 {{ font-size: 22pt; margin: 0 0 2pt; color:#0b3d5c; }}
h2 {{ break-after: avoid; font-size: 13.5pt; color:#0b3d5c; border-bottom: 2px solid #0b3d5c; padding-bottom:2pt; margin-top:16pt; }}
h3 {{ font-size: 11pt; margin: 10pt 0 4pt; }}
.sub {{ color:#555; font-size:11pt; margin-bottom:10pt; }}
.box {{ background:#f2f6f9; border-left:4px solid #0b3d5c; padding:6pt 10pt; margin:8pt 0; }}
.warn {{ background:#fff6e5; border-left:4px solid #c77700; padding:6pt 10pt; margin:8pt 0; }}
code, .ans {{ font-family: Consolas, "Courier New", monospace; }}
code {{ background:#eef1f4; padding:0 3px; border-radius:3px; font-size:8.6pt; word-break: break-all; }}
table {{ border-collapse: collapse; width:100%; font-size:8.8pt; table-layout:fixed; }} tr {{ break-inside: avoid; }}
th, td {{ border:1px solid #c9d1d9; padding:4pt 5pt; vertical-align:top; text-align:left; }}
th {{ background:#0b3d5c; color:#fff; }}
tr.cat td {{ background:#dde8f0; font-weight:700; color:#0b3d5c; }}
td.ans {{ font-weight:700; color:#8a1c1c; word-break:break-word; }}
td.files {{ font-size:7.8pt; color:#444; word-break:break-word; }}
.pts {{ color:#555; font-size:8pt; }} .lim {{ color:#c77700; font-size:8pt; }}
li {{ margin-bottom:3pt; }} .small {{ font-size:8.5pt; color:#555; }}
.grid {{ display:grid; grid-template-columns: 1fr 1fr; gap: 0 18pt; }}
</style></head><body>
<h1>Help Desk: Second Shift</h1>
<div class="sub">A CTF for Cisco NetAcad <b>Operating Systems Support</b> (Modules 1&ndash;3) &middot; Game 2 &middot; Facilitator guide &amp; answer key &middot; <b>Instructor only</b></div>
<div class="box"><b>At a glance:</b> {len(CH.C)} challenges &middot; {total:,} points &middot; 10 categories (all start with "OS") following topics 1.1&ndash;3.7 &middot; {nfiles} evidence files, including a Linux lab pack &middot; works alongside Game 1 on the same server &middot; tested on CTFd 3.8.6 next to Game 1.</div>

<h2>The story</h2>
<p>After their first shift, students are promoted to <b>Desktop &amp; Mobile Support</b> at Sawgrass Logistics. They work Windows tickets (display modes, battery reports, update failures, Task Manager, OneDrive, UEFI), Linux and macOS problems, phone and MDM issues, and cloud models. The boss ticket has them find the CFO's correct <b>BitLocker recovery key</b> among look-alikes before her board meeting.</p>
<div class="warn small"><b>Source note:</b> the Module 1&ndash;3 instructor decks you received contain only slide titles. Their "Best Practices" and "New Terms" slides were carried over from a cybersecurity course. These challenges are built from the official Scope &amp; Sequence topics (1.1&ndash;3.7) using standard CCST IT Support / A+ content. Spot-check the answer key against the NetAcad course pages before first use.</div>

<h2>Setup</h2>
<ol>
<li>Set up CTFd and finish the setup wizard. See <code>docs/platform-setup.md</code> in the OmniTech-Arena repository.</li>
<li>In CTFd as admin: <b>Settings &rarr; Access Tokens &rarr; Generate</b>.</li>
<li>From the repository root: <code>pip install requests</code>, then<br><code>python tools/deploy.py tracks/helpdesk-cisco-it-support/02-second-shift_operating-systems-support --url http://&lt;host&gt;:8000 --token ctfd_...</code></li>
<li>Look for <code>Done: {len(CH.C)} challenges loaded.</code> Run it <b>once</b>. Other games aren't touched. Add <code>--hidden</code> to load the game hidden.</li>
<li>One time per server: paste the two sort functions from <code>docs/platform-setup.md</code> into <b>Admin Panel &rarr; Config &rarr; Theme</b> so each game's categories stay grouped.</li>
</ol>
<h2>The Linux VM challenges [VM]</h2>
<p>The five challenges in <b>OS 2B Linux CLI [VM]</b> use <code>sawgrass_linux_lab.tar.gz</code> and need a Linux terminal. That's the VM students build in topic 2.3. The pack <b>must be extracted inside Linux</b> (<code>tar -xzvf</code>) so the file permissions survive. Extracting it with 7-Zip on Windows loses them, and "Permission Denied" and "Make It Run" stop making sense. Students can download it with the VM's browser straight from the CTF, or copy it in through a shared folder.</p>
<p class="small">If a student has no VM yet, WSL (Ubuntu) on Windows also works. Run the commands from the Linux home folder (<code>~</code>), not from <code>/mnt/c</code>.</p>

<h2>Running it alongside Canvas</h2>
<ul>
<li>Each category maps to a group of NetAcad topics (the numbers in parentheses), so you can tell students "finish OS 1A when you finish 1.1&ndash;1.2."</li>
<li><b>Recycle Bin Rescue</b> needs internet research, and the five <b>[VM]</b> challenges need Linux. Everything else can be solved from the files and the course.</li>
<li>Good discussion debriefs: <i>Lock, Don't Wipe</i> (policy vs. panic), <i>Knock Knock</i> (what brute-force attempts look like), <i>Permission Creep</i> (least privilege on phones), and the boss (why you match Key IDs, not device names).</li>
</ul>

<h2>Answer key</h2>
<p class="small">Every answer below was submitted by a test student on a CTFd 3.8.6 server that already had Game 1 loaded, and all {len(CH.C)} were accepted (full score: {total:,}). Wrong answers were checked and rejected, including the CFO's <i>other</i> LT-0611 key. The VM answers were checked by extracting the pack and running the commands in a real Linux shell.</p>
<table>
<tr><th style="width:19%">Challenge</th><th style="width:17%">Answer</th><th>Why / discussion</th><th style="width:17%">Files</th></tr>
{''.join(rows)}
</table>
</body></html>"""
open(os.path.join(HERE, "guide.html"), "w").write(doc)
print("ok")
