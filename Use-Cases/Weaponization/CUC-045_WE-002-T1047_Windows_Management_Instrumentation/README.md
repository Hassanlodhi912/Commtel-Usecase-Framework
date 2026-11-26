# CUC-045: Windows Management Instrumentation

| Stage | Code | MITRE |
|---|---|---|
| Weaponization | WE-002 | [T1047 Windows Management Instrumentation](https://attack.mitre.org/techniques/T1047/) (Execution) |

**What it detects:** abuse of WMI (wmic.exe, Invoke-WmiMethod, CIM cmdlets) for reconnaissance, process creation and lateral movement. Processes started through WMI run under WmiPrvSE.exe, which breaks the normal parent-child chain; this use case alerts on the WMI command, on children of WmiPrvSE.exe and on the decoded PowerShell script block.

**Log sources:** Security 4688 with command line, PowerShell 4104. Sysmon 1 optional.

**Detection:** IBM QRadar and Wazuh (rules 100450-100455), plus Hayabusa rules for offline hunting on .evtx files.

**Files:** document (PDF), `hayabusa_rules/` (4 rules and a run script).