# CUC-037: Scheduled Task

| Stage | Code | MITRE |
|---|---|---|
| Weaponization | WE-002 | [T1053.005 Scheduled Task](https://attack.mitre.org/techniques/T1053/005/) (Persistence, Privilege Escalation, Execution) |

**What it detects:** attackers using Windows Task Scheduler (schtasks.exe, PowerShell ScheduledTasks cmdlets, task XML import) to run code at logon, at startup or on a timer, often as SYSTEM or on remote hosts. Used by Turla, Conti and many commodity loaders.

**Log sources:** Windows Security 4698 (task created, with full task XML) and 4688 (process creation with command line).

**Detection:** IBM QRadar and Wazuh (rules 100370-100379), plus a Sigma rule. Validated in the lab with Atomic Red Team (6 procedures) and native schtasks commands.

**Files:** document (PDF, DOCX), `wazuh_rule_037.xml`.