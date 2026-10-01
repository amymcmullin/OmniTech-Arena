"""Game 4 -- Help Desk: Final Shift (Cisco NetAcad Hardware and Upgrade Support)."""
import csv, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "files"); os.makedirs(OUT, exist_ok=True)
ANS = {}
def w(n, t):
    open(os.path.join(OUT, n), "w", newline="\n").write(t.lstrip("\n"))

# ---------------------------------------------------------------- app compatibility (M1 S61-62)
w("app_compatibility_check.txt", """
Ticket: Marketing wants the new design suite "VectorForge 2027" installed on one of
three available PCs. Check each PC against the published minimum requirements.
=====================================================================
VectorForge 2027 -- MINIMUM REQUIREMENTS
  Processor architecture ... 64-bit (x64)
  RAM ...................... 16 GB
  GPU ...................... dedicated (discrete) GPU with 4 GB VRAM or more
  Free disk space .......... 25 GB

--- PC A: MKT-PC01   (System Information / msinfo32 summary) ---
  System Type ............. x64-based PC
  Installed Physical Memory (RAM) ... 8.00 GB
  Display ................. NVIDIA GeForce RTX 3050 (8 GB VRAM)
  Drive C: free space ..... 212 GB

--- PC B: MKT-PC02 ---
  System Type ............. x64-based PC
  Installed Physical Memory (RAM) ... 32.0 GB
  Display ................. NVIDIA RTX A2000 (6 GB VRAM)
  Drive C: free space ..... 148 GB

--- PC C: MKT-PC03 ---
  System Type ............. x64-based PC
  Installed Physical Memory (RAM) ... 16.0 GB
  Display ................. Intel UHD Graphics 770 (integrated, shared memory)
  Drive C: free space ..... 61 GB
""")
ANS["app_pc"] = "B"

# ---------------------------------------------------------------- mac ifconfig (M1 S42)
w("ifconfig_MKT-MBP04.txt", """
tech@MKT-MBP04 ~ % ifconfig en0
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether a4:83:e7:2b:9c:51
	inet6 fe80::1c8a:3ff2:9e40:7b21%en0 prefixlen 64 secured scopeid 0xb
	inet 10.20.7.88 netmask 0xffffff00 broadcast 10.20.7.255
	inet6 2001:db8:acad:70::58 prefixlen 64 autoconf secured
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
""")
ANS["mac_ether"] = "a4:83:e7:2b:9c:51"

# ---------------------------------------------------------------- Device Manager (M1 S63-64, M2 S62-65)
w("device_manager_ACC-PC11.txt", """
Device Manager -- devices with a problem (exported via Get-PnpDevice / Properties)
Computer: ACC-PC11
=====================================================================
Device                                   Status icon         Device status (Properties > General)
---------------------------------------------------------------------------------------------------
HP LaserJet M404 (USB Printing Support)  yellow triangle !   Windows has stopped this device because it has
                                                             reported problems. (Code 43)
Realtek PCIe GbE Family Controller       down arrow          This device is disabled. (Code 22)
USB Fingerprint Reader                   yellow triangle !   The drivers for this device are not installed.
                                                             (Code 28)
Intel(R) Wi-Fi 6E AX211                  (none)              This device is working properly.

Change log: Windows Update installed a new HP printer driver on 9/29. The printer
worked fine until then.
""")
ANS["disabled_dev"] = "Realtek PCIe GbE Family Controller"

# ---------------------------------------------------------------- Router firmware (M1 S65)
w("router_firmware_notes.txt", """
Branch router BR-TPA-01 -- current firmware: 4.2.1 (installed 9/27 by auto-update)
Ticket: "Internet at the Tampa branch drops every 20-30 minutes since the weekend."
=====================================================================
Manufacturer release notes (support site)
  4.2.1  2026-09-24  New: WPA3 transition improvements.
                     KNOWN ISSUE: WAN connection may drop intermittently on
                     models with DSL/cable failover enabled. Fix planned for 4.2.2.
  4.2.0  2026-08-12  KNOWN ISSUE: DHCP lease table may not clear on reboot.
                     (Affects models with more than 250 clients only.)
  4.1.6  2026-06-30  Stability fixes. No known issues.
  4.1.5  2026-05-02  Security fixes. No known issues.
Branch notes: BR-TPA-01 has DSL/cable failover ENABLED and about 40 clients.
""")
ANS["fw_rollback"] = "4.2.0"

# ---------------------------------------------------------------- Parts bin / sockets (M2 S40-41)
cpus = [("CPU-1", "Intel Core i5-12400", "LGA 1700"), ("CPU-2", "AMD Ryzen 5 7600", "AM5"),
        ("CPU-3", "Intel Core i7-9700", "LGA 1151"), ("CPU-4", "AMD Ryzen 5 5600", "AM4")]
boards = [("MB-1", "ASRock B550M Pro4", "AM4", "DDR4"), ("MB-2", "MSI B760M (DDR4)", "LGA 1700", "DDR4"),
          ("MB-3", "Gigabyte B650 Gaming X", "AM5", "DDR5"), ("MB-4", "ASUS PRIME H310M-E", "LGA 1151", "DDR4")]
with open(os.path.join(OUT, "parts_bin.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["PartID", "Type", "Model", "Socket", "Memory"])
    for p, m, s in cpus: wr.writerow([p, "CPU", m, s, ""])
    for p, m, s, mem in boards: wr.writerow([p, "Motherboard", m, s, mem])
sock = {s: p for p, m, s, mem in boards}
ANS["socket_map"] = "".join(sock[s][-1] for _, _, s in cpus)   # board digit for CPU-1..4

# ---------------------------------------------------------------- M.2 slots (M2 S45-46)
w("motherboard_manual_storage.txt", """
MSI B760M (DDR4) -- User manual, page 18: Storage
=====================================================================
M2_1 (CPU)      M.2 2280, PCIe 4.0 x4 -- supports **NVMe only** (no SATA M.2)
M2_2 (Chipset)  M.2 2280, PCIe 4.0 x4 / SATA 6Gb/s -- supports NVMe **and** SATA M.2
SATA1-SATA4     SATA 6Gb/s ports for 2.5"/3.5" drives

Ticket: "I installed the Crucial MX500 M.2 SSD (an M.2 **SATA** drive) in the slot
closest to the CPU (M2_1). BIOS doesn't see it at all."
""")
ANS["m2_slot"] = "M2_2"

# ---------------------------------------------------------------- PCIe slots (M2 S49-50)
w("pcie_slot_layout.txt", """
Motherboard MB-2 slot layout (top to bottom)
=====================================================================
PCI_E1   PCIe 4.0 x16 slot   (x16 lanes from CPU)
PCI_E2   PCIe 3.0 x1 slot
PCI_E3   PCIe 3.0 x16-length slot, but wired x4 (x4 lanes from chipset)

Upgrade ticket: install (1) a new discrete graphics card and (2) a PCIe Wi-Fi 6E card.
""")
ANS["slots"] = "PCI_E1,PCI_E2"

# ---------------------------------------------------------------- PSU sizing (M2 S25, S54)
parts = [("CPU (Core i5-12400, max turbo)", 117), ("GPU (RTX 4060 Ti)", 165), ("Motherboard + chipset", 50),
         ("RAM (2 x DIMM)", 10), ("NVMe SSD", 8), ("SATA SSD", 5), ("Case fans (4)", 12), ("USB devices", 15)]
total = sum(v for _, v in parts)
need = total * 1.3
psus = [450, 550, 650, 750, 850]
pick = min(p for p in psus if p >= need)
w("psu_sizing_worksheet.txt", f"""
PSU sizing worksheet -- workstation upgrade for DSN-PC02
Company standard: choose the SMALLEST available PSU whose rating is at least 30% above
the estimated total load (headroom for spikes and future upgrades).
=====================================================================
Component                               Estimated max draw (W)
""" + "\n".join(f"{n:<40}{v:>5}" for n, v in parts) + f"""

PSUs in stock (ATX12V, 80+ Gold): {", ".join(str(p) + " W" for p in psus)}
""")
ANS["psu_total"] = total
ANS["psu_pick"] = pick

# ---------------------------------------------------------------- Disposal log (M2 S69-73)
rows = [
    ("2026-09-02", "LT-0144", "Laptop", "SSD 256 GB", "Certified recycler (R2)", "Wiped - NIST 800-88 purge, cert #W-2231"),
    ("2026-09-02", "LT-0151", "Laptop", "SSD 512 GB", "Certified recycler (R2)", "Wiped - NIST 800-88 purge, cert #W-2232"),
    ("2026-09-09", "PRN-HR-01", "Multifunction printer", "Internal HDD 320 GB", "Certified recycler (e-Stewards)", "NONE RECORDED"),
    ("2026-09-09", "MON-0212", "Monitor", "(no storage)", "Certified recycler (e-Stewards)", "N/A"),
    ("2026-09-16", "PC-ACC-07", "Desktop", "HDD 1 TB", "Certified recycler (R2)", "Physically shredded, cert #D-0981"),
    ("2026-09-16", "KB-0331", "Keyboard", "(no storage)", "Certified recycler (R2)", "N/A"),
]
with open(os.path.join(OUT, "asset_disposal_log.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["Date", "AssetTag", "DeviceType", "Storage", "DisposedVia", "DataSanitization"]); wr.writerows(rows)
ANS["disposal_gap"] = "PRN-HR-01"

# ---------------------------------------------------------------- Boss: RAM upgrade via QVL (M2 S24-26, S43; M1 S61)
w("boss_ticket_INC-30418.txt", """
INC-30418 | P3 | Reported by: Dana K. (Design) | Asset: DSN-PC02
"VectorForge keeps crashing when I open big files. Can IT upgrade my PC?"

Tier 2 note: VectorForge needs 32 GB RAM for large files (vendor KB). Upgrade the
RAM using a kit from our parts inventory. Rules:
  1. The kit must match the motherboard's memory TYPE (check the board model in
     msinfo32, then the parts bin).
  2. The kit must be on the motherboard maker's QVL (Qualified Vendor List).
  3. After the upgrade the PC must have at least 32 GB total. Remove the old
     modules; the board has only 2 DIMM slots.
""")
w("msinfo32_DSN-PC02.txt", """
System Information -- System Summary            (msinfo32 export)
  OS Name ............................ Microsoft Windows 11 Pro
  System Name ........................ DSN-PC02
  System Type ........................ x64-based PC
  Processor .......................... 12th Gen Intel(R) Core(TM) i5-12400, 2500 Mhz, 6 Core(s)
  BaseBoard Manufacturer ............. Micro-Star International Co., Ltd.
  BaseBoard Product .................. MSI B760M (DDR4)    [inventory part MB-2]
  Installed Physical Memory (RAM) .... 16.0 GB  (2 x 8 GB)
  Total Virtual Memory ............... 18.9 GB
""")
kits = [("RAM-11", "Kingston FURY Beast 32GB (2x16GB) DDR5-5600", "DDR5", 32),
        ("RAM-12", "Corsair Vengeance LPX 32GB (2x16GB) DDR4-3200", "DDR4", 32),
        ("RAM-13", "NoName Value 32GB (2x16GB) DDR4-3200", "DDR4", 32),
        ("RAM-14", "Crucial 16GB (2x8GB) DDR4-3200", "DDR4", 16),
        ("RAM-15", "G.Skill Ripjaws V 64GB (2x32GB) DDR4-3600", "DDR4", 64)]
with open(os.path.join(OUT, "ram_inventory.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["PartID", "Kit", "Type", "TotalGB"]); wr.writerows(kits)
w("qvl_MSI_B760M_DDR4.txt", """
MSI B760M (DDR4) -- Memory QVL (excerpt)            Tested / Qualified Vendor List
=====================================================================
Vendor     Part Number            Size        Type        Speed     Tested
Corsair    CMK32GX4M2E3200C16     2x16 GB     DDR4        3200      Yes
Crucial    CT2K8G4DFRA32A         2x8 GB      DDR4        3200      Yes
Kingston   KF432C16BB1K2/32       2x16 GB     DDR4        3200      Yes
G.Skill    F4-3600C16D-32GVKC     2x16 GB     DDR4        3600      Yes
(NoName Value kits: not tested. G.Skill 2x32 GB 3600 kits: not tested.)

Parts-bin cross reference:
  RAM-12 Corsair Vengeance LPX 32GB DDR4-3200  = CMK32GX4M2E3200C16
  RAM-14 Crucial 16GB DDR4-3200                = CT2K8G4DFRA32A
""")
ANS["boss_ram"] = "RAM-12"

json.dump(ANS, open(os.path.join(HERE, "answers.json"), "w"), indent=2)
print(json.dumps(ANS, indent=2))
