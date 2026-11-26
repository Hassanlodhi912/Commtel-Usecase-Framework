# CUC-349: System Binary Proxy Execution - Msiexec

| Stage | Code | MITRE |
|---|---|---|
| Delivery | DE-005 | [T1218.007 Msiexec](https://attack.mitre.org/techniques/T1218/007/) (Stealth, formerly Defense Evasion) |

**What it detects:** attackers using the signed Windows Installer binary msiexec.exe to run malicious MSI packages or DLLs from local or remote paths, bypassing application control. Used by QakBot and IcedID.

**Log sources:** Security 4688 with command line, or Sysmon 1.

**Detection:** Sigma rule and QRadar test definitions, with a reference set of whitelisted MSI packages.

**Files:** document (DOCX).