# CUC-276: Clear Windows Event Logs

| Stage | Code | MITRE |
|---|---|---|
| Delivery | DE-005 | [T1070.001 Clear Windows Event Logs](https://attack.mitre.org/techniques/T1070/001/) (Defense Evasion) |

**What it detects:** attackers clearing Windows event logs to hide activity, using wevtutil, Clear-EventLog / Remove-EventLog, .NET ClearLog() or deleting .evtx files. Seen in BlackCat, LockBit, Ryuk, NotPetya and hands-on-keyboard intrusions.

**Log sources:** Security 1102 (audit log cleared), System 104 (log cleared), Security 4688 with command line, PowerShell 4104. Sysmon 1 optional.

**Detection:** IBM QRadar and Wazuh (rules 102760-102768), plus a Sigma rule. A separate LogRhythm version of the document is included.

**Files:** document (PDF, DOCX), LogRhythm DOCX, `wazuh_rule_276.xml`.