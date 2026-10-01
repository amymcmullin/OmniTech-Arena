"""Game 4 -- Help Desk: Final Shift (Hardware and Upgrade Support)."""
import json, os, re
A = json.load(open(os.path.join(os.path.dirname(__file__), "answers.json")))
CI = "case_insensitive"
def exact(s): return ("regex", r"^\s*" + re.escape(s) + r"\s*$", CI)
def words(*p): return ("regex", r"^\s*" + r"[\s_-]*".join(re.escape(x) for x in p) + r"s?\s*$", CI)
def letters(s): return ("regex", r"^\s*" + r"[\s,;-]*".join(re.escape(c) for c in s) + r"\s*$", CI)
def number(n, unit=""): return ("regex", r"^\s*" + re.escape(str(n)) + r"(\.0+)?\s*" + unit + r"\s*$", CI)
def seq(*items): return ("regex", r"^\s*" + r"\s*[,;\s]\s*".join(re.escape(str(i)) for i in items) + r"\s*$", CI)

CAT = {
    1: "UP 1A Safety & Device Info (1.1-1.2)",
    2: "UP 1B Ports & Cables (1.3)",
    3: "UP 1C Hardware Issues (1.4)",
    4: "UP 2A Architecture & Compatibility (2.1)",
    5: "UP 2B Core Components (2.2)",
    6: "UP 2C Interfaces & Expansion (2.3)",
    7: "UP 2D Drivers & Device Manager (2.4)",
    8: "UP 2E E-Waste & Disposal (2.5)",
    9: "UP 3 Boss Ticket",
}
NOTE = "\n\n*Answers are not case-sensitive.*"
C = []
def ch(name, cat, value, desc, flags, hints=(), files=(), tags=(), max_attempts=0, requires=(), src=""):
    C.append(dict(name=name, category=CAT[cat], value=value, description=desc.strip() + NOTE, flags=list(flags),
                  hints=list(hints), files=list(files), tags=list(tags), max_attempts=max_attempts, requires=list(requires), src=src))

# ============================================================ 1A Safety & device info
ch("Final Shift", 1, 50, """
Last stop on the IT Support Specialist path. Sawgrass Logistics has made you the **Hardware & Upgrade** technician: safety, ports, troubleshooting, upgrades, drivers, and disposal.

To clock in, submit:

`final shift`
""", [exact("final shift")], tags=["CCST 2.1"])

ch("Feel the Zap", 1, 150, """
Static electricity can damage parts long before you'd ever notice it.

1. At least how many **volts** must build up before a person can **feel** ESD?
2. Less than how many volts can **damage** a computer component?

Enter both numbers as `feel,damage` (example: `100,5`).
""", [("regex", r"^\s*3,?000\s*[,;\s]\s*30\s*$", CI)], tags=["CCST 2.1", "Y100200 24.0"], max_attempts=3, src="M1 S20 ESD")

ch("Safe or Sorry?", 1, 200, """
Which of these are **correct** safety practices? Enter the letters of all correct ones in alphabetical order (example: `ABE`).

- **A.** Keep new RAM in its antistatic bag until you're ready to install it.
- **B.** Use a laptop's charger on a different model laptop if the plug fits.
- **C.** Wear an antistatic wrist strap when working inside a computer.
- **D.** Make sure electrical equipment is properly grounded.
- **E.** Reach inside a printer right after turning it off, since all of its parts are safe once the power is off.
- **F.** Use grounded mats on workbenches and in work areas.
""", [letters("ACDF")], hints=[("Two of these are dangerous: some components hold high voltage after power-off, and AC adapters have specific power requirements.", 0)],
   tags=["CCST 2.1", "Y100200 24.0"], max_attempts=3, src="M1 S19-20 electrical safety and ESD")

ch("Tool Time", 1, 250, """
Match each task to the best **built-in Windows tool**:

- **A.** Task Manager (Performance tab)
- **B.** System Information (msinfo32)
- **C.** Event Viewer (eventvwr)
- **D.** ipconfig /all

1. See a history of what happened on the system before it crashed.
2. Find the network adapter's **Physical Address** (MAC) and the **DHCP server** from the command line.
3. Watch **real-time** CPU and disk activity while the user reproduces a slowdown.
4. Get one master list of host name, processor, RAM, disk space, IP, MAC, and Windows version to plan an upgrade.

Enter the letters for 1 through 4 in order.
""", [letters("CDAB")], tags=["CCST 2.2"], max_attempts=4, src="M1 S25-32 Windows tools")

ch("Run Box Shortcut", 1, 100, """
What do you type into **Windows key + R** to open **System Information**?
""", [("regex", r"^\s*msinfo32(\.exe)?\s*$", CI)], tags=["CCST 2.2"], max_attempts=3, src="M1 S28")

ch("Mac Address on a Mac", 1, 200, """
Open **ifconfig_MKT-MBP04.txt**, output from Terminal on a MacBook.

In `ifconfig`, the line labeled **inet** is the IPv4 address and **inet6** is IPv6. What is this Mac's **MAC address**?
""", [("regex", r"^\s*a4[:-]83[:-]e7[:-]2b[:-]9c[:-]51\s*$", CI)], hints=[("Look for the line labeled `ether`.", 0)],
   files=["ifconfig_MKT-MBP04.txt"], tags=["CCST 2.2"], max_attempts=3, src="M1 S42 ifconfig")

ch("Mac Equivalents", 1, 150, """
Match each Windows tool to its **macOS** equivalent:

- **A.** Activity Monitor
- **B.** Console
- **C.** ifconfig (Terminal)

1. Event Viewer
2. Task Manager
3. ipconfig

Enter three letters in order.
""", [letters("BAC")], tags=["CCST 2.2", "CCST 4.2"], max_attempts=3, src="M1 S36, S40, S42")

ch("Will It Run?", 1, 300, """
Open **app_compatibility_check.txt**. Marketing needs VectorForge 2027 on one of three PCs.

Which PC (**A**, **B**, or **C**) meets **every** minimum requirement?
""", [exact("B"), exact("PC B"), exact("MKT-PC02")],
   hints=[("PC A falls short on RAM. Look closely at PC C's graphics.", 25)],
   files=["app_compatibility_check.txt"], tags=["CCST 2.2", "CCST 4.5"], max_attempts=2, src="M1 S61-62 application compatibility")

# ============================================================ 1B Ports & cables
ch("Name That Port", 2, 250, """
Match each description to the port:

- **A.** VGA
- **B.** DVI
- **C.** HDMI
- **D.** DisplayPort
- **E.** PS/2
- **F.** Parallel

1. 20-pin digital video and audio. Can daisy-chain **multiple monitors** from one cable.
2. **Blue**, analog, 15 pins in three rows.
3. 25-pin receptacle, often called the "printer port."
4. 19-pin digital video **plus audio**, very common on TVs.
5. 6-pin DIN connector for an older keyboard or mouse.
6. Usually **white**, up to 24 digital pins plus up to 4 analog pins and a flat ground bar.

Enter six letters in order.
""", [letters("DAFCEB")], tags=["CCST 2.3"], max_attempts=4, src="M1 S45-50 legacy and video ports")

ch("Adapter or Converter?", 2, 200, """
An **adapter** only connects one physical connector to another. A **converter** also **translates the signal** from one technology to another.

Mark each as **A** (adapter) or **C** (converter):

1. VGA cable to a DVI port
2. USB to Ethernet
3. USB keyboard to a PS/2 port
4. HDMI cable to a DVI port
5. VGA signal to HDMI

Enter five letters in order.
""", [letters("ACAAC")], tags=["CCST 2.3"], max_attempts=3, src="M1 S56-57 adapters and converters")

ch("Big Iron Power", 2, 150, """
Most desktops use a **C13 to NEMA 5-15P** power cable. Which **C-number** connector is sometimes used for high-powered servers and large workstations? (Example format: `C7`)
""", [("regex", r"^\s*c\s*19(\s*to\s*nema\s*5-15p)?\s*$", CI)], tags=["CCST 2.3"], max_attempts=3, src="M1 S54 power cables")

ch("Thunder & Type-C", 2, 150, """
**USB Type-C** describes the **shape** of a port. Which technology, also using the Type-C shape, combines USB, DisplayPort, and power delivery in one cable? Give the name without the version number.
""", [exact("Thunderbolt"), ("regex", r"^\s*thunderbolt\s*[34]?\s*$", CI)], tags=["CCST 2.3"], max_attempts=3, src="M1 S51, S53")

# ============================================================ 1C Hardware issues
ch("Dead PC Checklist", 3, 150, """
A user's desktop won't power on at all. Put Amit's checks in order, **simplest first**:

- **A.** Check the switch on the back of the power supply.
- **B.** Check that the power cable is firmly connected at both the PC and the outlet.
- **C.** Test the outlet with another device that you know works.

Enter three letters in order.
""", [letters("BCA")], tags=["CCST 2.5"], max_attempts=2, src="M1 S60 'Troubleshooting Power Issues'")

ch("Down Arrow", 3, 250, """
Open **device_manager_ACC-PC11.txt**.

Which device has been **disabled**? Enter its name exactly as listed.
""", [exact(A["disabled_dev"]), ("regex", r"^\s*realtek.*(gbe|ethernet|nic).*$", CI)],
   hints=[("A down-arrow icon and **Code 22** both mean disabled.", 0)],
   files=["device_manager_ACC-PC11.txt"], tags=["CCST 2.5", "Y100200 03.0"], max_attempts=3, src="M1 S64 / M2 S62 Device Manager status icons")

ch("Firmware Flashback", 3, 300, """
Open **router_firmware_notes.txt**. The Tampa router's Internet connection keeps dropping since the auto-update.

Following Jasmine's approach, you'll **roll back** the firmware. Which version should you roll back to? Choose the **newest** version that has **no known issue affecting this router**.
""", [exact(A["fw_rollback"])],
   hints=[("Read each known issue and check whether it applies to this branch (failover enabled, about 40 clients).", 0)],
   files=["router_firmware_notes.txt"], tags=["CCST 2.5"], max_attempts=2, src="M1 S65 'Firmware Update Issues'")

ch("Did You Reboot?", 3, 100, """
Turning a device off and back on to clear temporary faults is the first, least disruptive step. Amelia used it in the Wi-Fi call. What is this called? (Two words.)
""", [words("power", "cycling"), words("power", "cycle")], tags=["CCST 2.5"], max_attempts=3, src="M1 S59 'Did You Reboot?'")

# ============================================================ 2A Architecture & compatibility
ch("Software Layers", 4, 200, """
Match each description to the type of software:

- **A.** Firmware
- **B.** Operating system
- **C.** Driver software
- **D.** Application software

1. Translates the OS's commands into instructions a specific graphics card understands.
2. A spreadsheet program that a user runs to do their job.
3. Built into the hardware, controls startup, and runs **before** the OS loads.
4. Manages memory, CPU, storage, and I/O, and gives the user an interface.

Enter four letters in order.
""", [letters("CDAB")], tags=["CCST 2.4"], max_attempts=3, src="M2 S23 The Role of Software")

ch("Should Have Planned", 4, 250, """
Match each failed upgrade to the planning step that would have prevented it:

- **A.** Check part specifications
- **B.** Check dimensions and clearance
- **C.** Calculate power needs
- **D.** Check for BIOS updates

1. The new graphics card is 2 cm too long to close the case.
2. The PC shuts down whenever a game starts after the new GPU went in.
3. The new CPU fits the socket, but the board won't POST until the firmware is newer.
4. The DDR5 RAM that was ordered won't go into the board's DDR4 slots.

Enter four letters in order.
""", [letters("BCDA")], tags=["CCST 2.4"], max_attempts=3, src="M2 S24-25 planning the installation or upgrade")

ch("Tested and Approved", 4, 100, """
Motherboard makers publish a list of memory modules they've **tested** with each board. What is this list usually called? Enter the three-letter abbreviation.
""", [exact("QVL"), ("regex", r"^\s*qualified\s+vendor\s+list\s*$", CI)], hints=[("Q _ _", 0)],
   tags=["CCST 2.4"], max_attempts=3, src="M2 S26 HCL/QVL")

# ============================================================ 2B Core components
ch("Plug It In", 5, 250, """
Match each power supply connector to what it powers:

- **A.** 24-pin slotted connector
- **B.** SATA keyed connector
- **C.** Molex keyed connector
- **D.** Berg keyed connector
- **E.** 4-pin to 8-pin auxiliary connector
- **F.** 6/8-pin PCIe connector

1. A legacy floppy drive
2. A discrete graphics card
3. The main motherboard power
4. A modern SATA SSD
5. Extra dedicated power to the CPU area of the motherboard
6. An older optical drive or legacy hard drive

Enter six letters in order.
""", [letters("DFABEC")], tags=["CCST 2.4"], max_attempts=4, src="M2 S32-33 power supply connectors")

ch("Twelve Volt Club", 5, 100, """
Of the three common PSU voltages (3.3 V, 5 V, 12 V), which one runs the **motors** in disk drives and fans? Enter just the number.
""", [("regex", r"^\s*12\s*(v|volts?)?\s*$", CI)], tags=["CCST 2.4"], max_attempts=2, src="M2 S34 power supply voltage")

ch("Socket Match", 5, 300, """
Open **parts_bin.csv**. Each CPU fits exactly one of the motherboards.

For **CPU-1, CPU-2, CPU-3, and CPU-4** in that order, enter the **number** of the motherboard each one fits (MB-1 through MB-4). Example format: `4321`.
""", [letters(A["socket_map"])], hints=[("Match the Socket column. Remember that AM5 is not AM4, and LGA 1700 is not LGA 1151.", 0)],
   files=["parts_bin.csv"], tags=["CCST 2.4", "Y100200 10.0"], max_attempts=3, src="M2 S40-41 CPU socket types")

ch("Small Box", 5, 150, """
A thin client needs the smallest motherboard form factor in the course, about **17 cm x 17 cm** with only **one** expansion slot. Which form factor is it?
""", [("regex", r"^\s*mini[\s-]?itx\s*$", CI)], tags=["CCST 2.4"], max_attempts=3, src="M2 S38 motherboard form factors")

ch("Wrong Slot", 5, 250, """
Open **motherboard_manual_storage.txt**.

**M.2** is a physical form factor, and drives in that shape can use the **SATA** or **NVMe** protocol. The user's M.2 SATA SSD isn't detected. Which **slot** should it go in instead?
""", [("regex", r"^\s*m\.?2[_\s-]?2\s*$", CI)], files=["motherboard_manual_storage.txt"], tags=["CCST 2.4", "Y100200 10.0"],
   max_attempts=2, src="M2 S45-46 SATA, NVMe, M.2")

ch("North or South?", 5, 150, """
Which part of the chipset lets the CPU talk to **slower** devices like hard drives, USB ports, and expansion slots? (One word.)
""", [exact("southbridge"), words("south", "bridge")], tags=["CCST 2.4"], max_attempts=2, src="M2 S37 motherboard chipset")

ch("Forget Me Not", 5, 100, """
Which type of memory is **volatile**, meaning its contents are erased every time the computer powers off? Enter **RAM** or **ROM**.
""", [exact("RAM")], tags=["CCST 2.4"], max_attempts=1, src="M2 S43 types of memory")

# ============================================================ 2C Interfaces & expansion
ch("Lanes for Cards", 6, 200, """
Open **pcie_slot_layout.txt**. You're installing a **discrete GPU** and a **PCIe Wi-Fi card**.

Which slot gets the GPU, and which gets the Wi-Fi card? Enter `GPUslot,WiFislot` (example: `PCI_E3,PCI_E1`).
""", [seq("PCI_E1", "PCI_E2")], hints=[("GPUs need the full x16 lanes. Wi-Fi cards use x1.", 0)],
   files=["pcie_slot_layout.txt"], tags=["CCST 2.4"], max_attempts=3, src="M2 S49-50 PCIe lane sizes")

ch("Speed of a Flash Drive", 6, 250, """
A user is copying **30 GB** to a flash drive in a **USB 2.0** port (480 Mbps from the course's USB table).

Ignoring overhead, how many **seconds** would that take at the full theoretical speed? Use 1 GB = 8,000 megabits.
""", [number(500, r"(s|sec|seconds?)?")], hints=[("30 x 8,000 megabits / 480 megabits per second", 25)],
   tags=["CCST 2.3", "Y100200 09.0"], max_attempts=4, src="M2 S52 USB versions table")

ch("Size the PSU", 6, 300, """
Open **psu_sizing_worksheet.txt**.

1. What is the **total** estimated load in watts?
2. Following the company standard, which **PSU wattage** do you pick?

Enter `total,PSU` (example: `300,450`).
""", [seq(A["psu_total"], A["psu_pick"])], hints=[("Add up the column, multiply by 1.3, then pick the smallest PSU at or above that number.", 0)],
   files=["psu_sizing_worksheet.txt"], tags=["CCST 2.4", "Y100200 09.0"], max_attempts=4, src="M2 S25 calculate power needs, S54 GPU power")

ch("Wireless, Two Ways", 6, 150, """
Choose **U** (external USB adapter) or **I** (internal PCIe card) for each case:

1. A loaner laptop's built-in Wi-Fi died and the user needs to be online in 5 minutes.
2. A permanent desktop video-editing workstation that needs the best Wi-Fi performance and bigger antennas.
3. A trainer who moves one Wi-Fi adapter between several classroom PCs.

Enter three letters in order.
""", [letters("UIU")], tags=["CCST 2.4"], max_attempts=2, src="M2 S55-56 wireless and Bluetooth cards")

ch("Integrated vs Discrete", 6, 150, """
A GPU that is **built into the CPU** and **shares system RAM** is called what kind of graphics? (One word.)
""", [exact("integrated")], tags=["CCST 2.4"], max_attempts=2, src="M2 S53-54 GPUs")

# ============================================================ 2D Drivers
ch("Driver Tab Decisions", 7, 250, """
Match each situation to the **Driver tab** option in Device Manager:

- **A.** Driver Details
- **B.** Update Driver
- **C.** Roll Back Driver
- **D.** Uninstall Device
- **E.** Scan for hardware changes

1. The printer stopped working right after Windows Update installed a new driver.
2. You need the driver's file names, versions, and digital signature for a ticket.
3. You reconnected a USB scanner but it doesn't show up in the list.
4. You want to remove a device and its settings completely before reinstalling cleanly.
5. Routine maintenance: check for a newer, compatible driver without removing anything.

Enter five letters in order.
""", [letters("CAEDB")], tags=["CCST 2.4", "Y100200 03.0"], max_attempts=4, src="M2 S65 Driver tab options")

ch("Printer Fix", 7, 150, """
Using **device_manager_ACC-PC11.txt** and its change log: the HP LaserJet worked until Windows Update installed a new driver. Which **Driver tab** button do you try first? (Three words.)
""", [words("roll", "back", "driver"), words("rollback", "driver")], files=["device_manager_ACC-PC11.txt"],
   tags=["CCST 2.4", "CCST 2.5"], max_attempts=2, src="M1 S63, M2 S65")

ch("WHQL?", 7, 150, """
Windows Update drivers come from Microsoft's catalog and are tested through **WHQL**. What does WHQL stand for?
""", [("regex", r"^\s*windows\s+hardware\s+quality\s+lab(s|oratories)?\s*$", CI)], tags=["CCST 2.4"], max_attempts=3, src="M2 S59")

# ============================================================ 2E E-waste
ch("Which Law?", 8, 250, """
Match each situation to the regulation:

- **A.** HIPAA
- **B.** FERPA
- **C.** GDPR
- **D.** RCRA
- **E.** WEEE Directive

1. Old lab PCs at iTECH stored **student records**.
2. A clinic's retired laptops held **patient** information.
3. A US company's monitors may be **hazardous waste** and need certified recycling.
4. A European customer's **personal data** was on a returned drive.
5. In the **EU**, the **manufacturer** must handle recycling and recovery of electronics.

Enter five letters in order.
""", [letters("BADCE")], tags=["CCST 2.1", "Y100200 17.0"], max_attempts=3, src="M2 S69-71 data security and regulations")

ch("Certified Recyclers", 8, 150, """
The course names two e-waste recycler certifications. One is **R2 (Responsible Recycling)**. What is the other?
""", [("regex", r"^\s*e[\s-]?stewards?\s*$", CI)], tags=["CCST 2.1"], max_attempts=3, src="M2 S72")

ch("Paper Trail Gap", 8, 300, """
Open **asset_disposal_log.csv**. Every device that **stores data** needs a documented wipe or destruction before it leaves the building.

Which **asset tag** went to the recycler with **no** data sanitization on record, even though it had storage?
""", [exact(A["disposal_gap"])], hints=[("Printers can store data too.", 0)],
   files=["asset_disposal_log.csv"], tags=["CCST 2.1", "Y100200 17.0", "Y100200 46.0"], max_attempts=3, src="M2 S69, S73")

ch("Toxic Trio", 8, 100, """
The course lists three toxic materials found in motherboards, batteries, and cables: **lead**, **mercury**, and one more starting with **C**. What is it?
""", [exact("cadmium")], tags=["CCST 2.1"], max_attempts=2, src="M2 S70")

# ============================================================ Boss
ch("The 32 GB Upgrade", 9, 500, """
**Ticket INC-30418.** A designer's VectorForge keeps crashing on large files. Tier 2 approved a RAM upgrade to **at least 32 GB**, but you must pick the right kit from inventory.

Files:
1. **boss_ticket_INC-30418.txt**: the rules
2. **msinfo32_DSN-PC02.txt**: what's in the PC now
3. **ram_inventory.csv**: the kits on the shelf
4. **qvl_MSI_B760M_DDR4.txt**: the motherboard's Qualified Vendor List

Enter the **PartID** of the only kit that meets every rule (example format: `RAM-00`).
""", [exact(A["boss_ram"])],
   hints=[("The board model's name tells you the memory type.", 0),
          ("Two DDR4 32 GB kits are in stock, but only one is on the QVL. The 64 GB kit isn't tested.", 100)],
   files=["boss_ticket_INC-30418.txt", "msinfo32_DSN-PC02.txt", "ram_inventory.csv", "qvl_MSI_B760M_DDR4.txt"],
   tags=["CCST 2.2", "CCST 2.4", "Y100200 10.0"], max_attempts=3,
   requires=["Will It Run?", "Socket Match", "Tested and Approved"],
   src="M1 S61-62 compatibility, M2 S24-26 compatibility/QVL, S43 RAM")

if __name__ == "__main__":
    print(len(C), "challenges,", sum(c["value"] for c in C), "points")
