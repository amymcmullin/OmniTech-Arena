"""Game 3 facilitator guide."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import challenges as CH
A = CH.A

ANSWER = {
 "Night Shift":"third shift","Which Directory?":"CDAB","MFA Morning":"1243","Map It Right":"\\\\FS01\\Accounting",
 "Policy Refresh":"gpupdate /force","Built-in Groups":"Guests","Permission Puzzle":"BACD","Locked Out":"wturner,DSP-PC09",
 "Right Console":"dsa.msc","Stuck Spooler":"Print Spooler","Peripheral Triage":"ECFADB","Slow Drive, Fast Port":"blue",
 "Network Sizes":"FADBEC","Cable Choice":"USF","Left Behind":"WH-PRN-02","Power Budget":"Gi1/0/21","Wi-Fi 6":"802.11ax",
 "Private or Public?":"CE","Squeeze the IPv6":"2001:db8::a0:0:0:1","GUA or LLA?":"LGBLG","Gateway Gone Wrong":"10.20.4.1",
 "Local or Remote?":"192.168.10.70","169.254 Means...":"DHCP","DORA":"CDAB","Stale Address":"ipconfig /flushdns",
 "Let It Through":"Windows Defender Firewall","Read the Config":"3C-58-C2-9A-17-E4,10.20.1.5","Where Does It Break?":"192.0.2.200",
 "Who's Listening?":"7316","Modern Linux":"ss","Name That Threat Actor":"ADBEFC","Malware Lineup":"CAEBFD","Attack Category":"RASDR",
 "Hook, Line & Sinker":"m365-verify-login.example","Return to Sender":"sawgrass-logistics-support.example",
 "Social Engineering Bingo":"AECDFBG","Verify, Then Trust":"B","Investigation Order":"CEADB","Who Do You Call?":"EADBC",
 "Sort the Data":"PICFHL","Know, Have, Are":"HKAHA","Can't Deny It":"non-repudiation","The Rulebook":"AUP",
 "Patient Zero":"MailboxRestore_Tool.exe",
}
NOTES = {
 "Map It Right": "User typed 'Acounting' (one c). Trailing backslash and any capitalization are accepted.",
 "Policy Refresh": "gpupdate or gpupdate /force.",
 "Locked Out": "Five 4625s from DSP-PC09, then 4740. gliu and mreyes have failures but were never locked out.",
 "Power Budget": "Ports 1-20 use 10x25.5 + 10x6.5 = 320 W. The 60 W kiosk on port 21 would make it 380 W, over the 370 W budget. The 4 W badge reader on port 22 still fits.",
 "Left Behind": "802.11b/g is 2.4 GHz only. The 2018 laptop is dual-band 802.11n, so it's fine.",
 "Private or Public?": "172.32.0.9 is just outside 172.16-172.31. 169.254 is APIPA.",
 "Squeeze the IPv6": "2001:db8:0:0:a0::1 is also accepted.",
 "Local or Remote?": "/26 = blocks of 64, so .37 is in .0-.63 and .70 is in .64-.127. Only 2 attempts.",
 "Who's Listening?": "Port 4444 to 203.0.113.99. A good discussion lead-in to remote-access Trojans.",
 "Patient Zero": "Proxy: only WH-PC07/ochen got status 200, and it downloaded MailboxRestore_Tool.exe. The email's Received header gives 198.51.100.77; in netstat that's PID 9032, which tasklist shows is MailboxRestore_Tool.exe. Unlocks after Hook Line & Sinker, Who's Listening?, and Investigation Order.",
}
WHY = {c["name"]: (ANSWER[c["name"]], (NOTES.get(c["name"], "") + "  Source: " + c["src"]).strip()) for c in CH.C}
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

doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Help Desk: Third Shift - Facilitator Guide</title>
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
<h1>Help Desk: Third Shift</h1>
<div class="sub">A CTF for Cisco NetAcad <b>Security and Connectivity Support</b> (Modules 1&ndash;3) &middot; Game 3 &middot; Facilitator guide &amp; answer key &middot; <b>Instructor only</b></div>
<div class="box"><b>At a glance:</b> {len(CH.C)} challenges &middot; {total:,} points &middot; 11 categories (all start with "SC") following topics 1.1&ndash;3.7 &middot; {nfiles} evidence files &middot; loads next to Games 1 and 2 &middot; tested on CTFd 3.8.6 alongside both.</div>

<h2>The story</h2>
<p>Students are now <b>Network &amp; Security Support</b> at Sawgrass Logistics. They work through directory services, MFA, mapped drives, lockouts in a domain controller log, NTFS permissions, and peripherals. Then come Wi-Fi standards, a PoE budget, IPv4/IPv6 addressing, gateways, DHCP and DNS, and reading ipconfig, tracert and netstat output. Last are threat actors, malware, social engineering, a real-looking phishing email, incident response and data classification. In the boss ticket, students follow a phishing campaign from the email through the proxy log to the one compromised PC and the malicious process.</p>
<div class="box small"><b>Built from your decks:</b> unlike Game 2, these instructor decks have full slide content. Every answer is tied to a specific slide, cited as "Source: M#&nbsp;S##" in the key (Module and slide number in the instructor PPTX).</div>
<h2>Setup</h2>
<ol>
<li>Set up CTFd and finish the setup wizard. See <code>docs/platform-setup.md</code> in the OmniTech-Arena repository.</li>
<li>In CTFd as admin: <b>Settings &rarr; Access Tokens &rarr; Generate</b>.</li>
<li>From the repository root: <code>pip install requests</code>, then<br><code>python tools/deploy.py tracks/helpdesk-cisco-it-support/03-third-shift_security-and-connectivity-support --url http://&lt;host&gt;:8000 --token ctfd_...</code></li>
<li>Look for <code>Done: {len(CH.C)} challenges loaded.</code> Run it <b>once</b>. Other games aren't touched. Add <code>--hidden</code> to load the game hidden.</li>
<li>One time per server: paste the two sort functions from <code>docs/platform-setup.md</code> into <b>Admin Panel &rarr; Config &rarr; Theme</b> so each game's categories stay grouped.</li>
</ol>
<h2>Running it alongside Canvas</h2>
<ul>
<li>Each category maps to NetAcad topics (the numbers in parentheses), so students can do "SC 2B" right after finishing topics 2.4&ndash;2.5.</li>
<li>Everything can be solved from the files and the course. No internet or VM is needed.</li>
<li>Good debriefs: <i>Verify, Then Trust</i> (one attempt only, so it's worth discussing why), <i>Who's Listening?</i> (what to do when you find a suspicious connection: collect evidence and escalate, don't "fix" it yourself), and <i>Patient Zero</i> (why the proxy bypass on one VLAN mattered).</li>
</ul>

<h2>Answer key</h2>
<p class="small">Every answer below was submitted by a test student on a CTFd 3.8.6 server that already had Games 1 and 2 loaded, and all {len(CH.C)} were accepted (full score: {total:,}). Common wrong answers were checked and rejected, for example the other accounts in the lockout log, port 22 on the PoE switch, and ms-teams.exe in the boss.</p>
<table>
<tr><th style="width:19%">Challenge</th><th style="width:17%">Answer</th><th>Why / discussion</th><th style="width:17%">Files</th></tr>
{''.join(rows)}
</table>
</body></html>"""
open(os.path.join(HERE, "guide.html"), "w").write(doc)
print("ok")
