# CUC-276: Clear Windows Event Logs

| Stage | Code | MITRE |
|---|---|---|
| Delivery | DE-041 | [T1685.005 Clear Windows Event Logs](https://attack.mitre.org/techniques/T1685/005/) (Defense Impairment) |

**What it detects:** attackers clearing Windows event logs to hide activity, using wevtutil, Clear-EventLog / Remove-EventLog, .NET ClearLog() or deleting .evtx files. Seen in BlackCat, LockBit, Ryuk, NotPetya and hands-on-keyboard intrusions.

**Log sources:** Security 1102 (audit log cleared), System 104 (log cleared), Security 4688 with command line, PowerShell 4104. Sysmon 1 optional.

**Detection:** IBM QRadar and Wazuh (rules 102760-102768), plus a Sigma rule. A separate LogRhythm version of the document is included.

**Files:** document (PDF, DOCX), LogRhythm DOCX, `wazuh_rule_276.xml`.
> In ATT&CK v20 this technique moved from T1070.001 (Defense Evasion) to T1685.005 under the new Defense Impairment tactic. The CUC number stays the same; the document still uses the old ID.
