"""Game 4 facilitator guide."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import challenges as CH
A = CH.A

ANSWER = {
 "Final Shift":"final shift","Feel the Zap":"3000,30","Safe or Sorry?":"ACDF","Tool Time":"CDAB","Run Box Shortcut":"msinfo32",
 "Mac Address on a Mac":"a4:83:e7:2b:9c:51","Mac Equivalents":"BAC","Will It Run?":"B","Name That Port":"DAFCEB",
 "Adapter or Converter?":"ACAAC","Big Iron Power":"C19","Thunder & Type-C":"Thunderbolt","Dead PC Checklist":"BCA",
 "Down Arrow":"Realtek PCIe GbE Family Controller","Firmware Flashback":"4.2.0","Did You Reboot?":"power cycling",
 "Software Layers":"CDAB","Should Have Planned":"BCDA","Tested and Approved":"QVL","Plug It In":"DFABEC","Twelve Volt Club":"12",
 "Socket Match":"2341","Small Box":"Mini-ITX","Wrong Slot":"M2_2","North or South?":"Southbridge","Forget Me Not":"RAM",
 "Lanes for Cards":"PCI_E1,PCI_E2","Speed of a Flash Drive":"500","Size the PSU":"382,550","Wireless, Two Ways":"UIU",
 "Integrated vs Discrete":"integrated","Driver Tab Decisions":"CAEDB","Printer Fix":"Roll Back Driver",
 "WHQL?":"Windows Hardware Quality Labs","Which Law?":"BADCE","Certified Recyclers":"e-Stewards","Paper Trail Gap":"PRN-HR-01",
 "Toxic Trio":"cadmium","The 32 GB Upgrade":"RAM-12",
}
NOTES = {
 "Feel the Zap": "Commas are optional (3000 or 3,000).",
 "Will It Run?": "A fails RAM (8 GB). C has integrated graphics with shared memory, not a 4 GB discrete GPU. Only 2 attempts.",
 "Down Arrow": "Code 22 = disabled. The printer is Code 43 (error), and the fingerprint reader is Code 28 (no driver).",
 "Firmware Flashback": "4.2.1 has the failover bug this router hits. 4.2.0's issue only affects more than 250 clients, so it's the newest safe version. 4.1.6 works but isn't the newest safe one. Only 2 attempts.",
 "Socket Match": "CPU-1 LGA1700 to MB-2, CPU-2 AM5 to MB-3, CPU-3 LGA1151 to MB-4, CPU-4 AM4 to MB-1.",
 "Wrong Slot": "M2_1 is NVMe-only. M2_2 accepts SATA M.2.",
 "Speed of a Flash Drive": "30 x 8,000 / 480 = 500 s (about 8.3 minutes).",
 "Size the PSU": "Sum = 382 W. x 1.3 = 496.6 W, so the smallest PSU that covers it is 550 W.",
 "Paper Trail Gap": "The multifunction printer had a 320 GB HDD and NONE RECORDED. The monitor and keyboard have no storage.",
 "The 32 GB Upgrade": "Board = MSI B760M (DDR4), so DDR5 RAM-11 is out. RAM-13 isn't on the QVL. RAM-14 is only 16 GB. RAM-15 (2x32 GB) isn't tested. That leaves RAM-12. Unlocks after Will It Run?, Socket Match, and Tested and Approved.",
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

doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Help Desk: Final Shift - Facilitator Guide</title>
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
<h1>Help Desk: Final Shift</h1>
<div class="sub">A CTF for Cisco NetAcad <b>Hardware and Upgrade Support</b> (Modules 1&ndash;2) &middot; Game 4 &middot; Facilitator guide &amp; answer key &middot; <b>Instructor only</b></div>
<div class="box"><b>At a glance:</b> {len(CH.C)} challenges &middot; {total:,} points &middot; 9 categories (all start with "UP") following topics 1.1&ndash;2.5 &middot; {nfiles} evidence files &middot; loads next to Games 1&ndash;3 &middot; tested on CTFd 3.8.6 alongside all three.</div>

<h2>The story</h2>
<p>In the last stop on the IT Support Specialist path, students become the <b>Hardware &amp; Upgrade</b> technician. The work covers ESD and electrical safety; finding device information on Windows and Mac; identifying ports, cables, adapters and converters; Device Manager codes; and a firmware rollback decision. Then come compatibility planning, PSU connectors and sizing, CPU sockets, M.2 SATA vs NVMe, PCIe lanes, USB math, driver tools, and e-waste laws and disposal records. In the boss ticket, students pick the one RAM kit that matches the board's memory type, appears on the QVL, and gets the designer to 32 GB.</p>
<div class="box small"><b>Built from your decks:</b> every answer cites its source slide ("Source: M#&nbsp;S##" = Module and slide number in the instructor PPTX).</div>
<h2>Setup</h2>
<ol>
<li>Set up CTFd and finish the setup wizard. See <code>docs/platform-setup.md</code> in the OmniTech-Arena repository.</li>
<li>In CTFd as admin: <b>Settings &rarr; Access Tokens &rarr; Generate</b>.</li>
<li>From the repository root: <code>pip install requests</code>, then<br><code>python tools/deploy.py tracks/helpdesk-cisco-it-support/04-final-shift_hardware-and-upgrade-support --url http://&lt;host&gt;:8000 --token ctfd_...</code></li>
<li>Look for <code>Done: {len(CH.C)} challenges loaded.</code> Run it <b>once</b>. Other games aren't touched. Add <code>--hidden</code> to load the game hidden.</li>
<li>One time per server: paste the two sort functions from <code>docs/platform-setup.md</code> into <b>Admin Panel &rarr; Config &rarr; Theme</b> so each game's categories stay grouped.</li>
</ol>
<h2>Running it alongside Canvas</h2>
<ul>
<li>Each category maps to NetAcad topics, so students can do "UP 2B" right after finishing topic 2.2.</li>
<li>Everything can be solved from the files and the course. Hands-on extension: have students check their answers to <i>Tool Time</i> and <i>Mac Equivalents</i> on real machines, and open a lab PC to physically identify the <i>Plug It In</i> connectors.</li>
<li>Good debriefs: <i>Firmware Flashback</i> (why "newest safe" beats "oldest"), <i>Paper Trail Gap</i> (printers store data too), and the boss (why the QVL matters even when a kit is the right type).</li>
</ul>

<h2>Answer key</h2>
<p class="small">Every answer below was submitted by a test student on a CTFd 3.8.6 server that already had Games 1&ndash;3 loaded, and all {len(CH.C)} were accepted (full score: {total:,}). Common wrong answers were checked and rejected, for example PC C, firmware 4.1.6, a 450 W PSU, and RAM-13 in the boss.</p>
<table>
<tr><th style="width:19%">Challenge</th><th style="width:17%">Answer</th><th>Why / discussion</th><th style="width:17%">Files</th></tr>
{''.join(rows)}
</table>
</body></html>"""
open(os.path.join(HERE, "guide.html"), "w").write(doc)
print("ok")
