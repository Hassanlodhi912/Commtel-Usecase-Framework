# CUC-576: Inhibit System Recovery

| Stage | Code | MITRE |
|---|---|---|
| Actions on Objectives | AO-040 | [T1490 Inhibit System Recovery](https://attack.mitre.org/techniques/T1490/) (Impact) |

**What it detects:** deletion or disabling of Windows recovery features just before ransomware encryption: shadow copy deletion (vssadmin, wmic, PowerShell), backup catalog deletion (wbadmin), boot recovery disabled (bcdedit) and System Restore disabled. Used by Conti, Ryuk, LockBit and BlackCat. A fast alert here is the last chance to isolate before encryption.

**Log sources:** Security 4688 with command line, PowerShell 4104.

**Detection:** IBM QRadar and Wazuh rules, with lab validation.

**Files:** document (PDF, DOCX).