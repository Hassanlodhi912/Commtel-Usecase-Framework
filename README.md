# Commtel Use Case Framework

Commtel SIEM use case library. Each use case is mapped to a Cyber Kill Chain stage and a MITRE ATT&CK technique, with a full document (PDF and DOCX) and, where built, a Wazuh detection rule.

Maintained by **Hassan Kaleem**, Detection Engineer at Commtel.

## Progress

**5 of 713 use cases documented** (`█░░░░░░░░░░░░░░░░░░░ 0.7%`)

| Kill chain stage | Code | Total | Documented | Pending | Progress |
|---|---|---|---|---|---|
| Reconnaissance | RE | 37 | 0 | 37 | `░░░░░░░░░░░░░░░░░░░░ 0.0%` |
| Weaponization | WE | 177 | 2 | 175 | `█░░░░░░░░░░░░░░░░░░░ 1.1%` |
| Delivery | DE | 266 | 2 | 264 | `█░░░░░░░░░░░░░░░░░░░ 0.8%` |
| Exploitation | EX | 102 | 0 | 102 | `░░░░░░░░░░░░░░░░░░░░ 0.0%` |
| Installation | IN | 54 | 0 | 54 | `░░░░░░░░░░░░░░░░░░░░ 0.0%` |
| Command & Control | CC | 36 | 0 | 36 | `░░░░░░░░░░░░░░░░░░░░ 0.0%` |
| Actions on Objectives | AO | 41 | 1 | 40 | `█░░░░░░░░░░░░░░░░░░░ 2.4%` |
| **Total** | | **713** | **5** | **708** | `█░░░░░░░░░░░░░░░░░░░ 0.7%` |

The register is aligned to **MITRE ATT&CK Enterprise v20.1** (14 tactics, including the new Stealth and Defense Impairment tactics). The full list of 713 use cases is in [Framework/Commtel_Usecase_Framework.xlsx](Framework/Commtel_Usecase_Framework.xlsx); the ATT&CK Changes sheet lists what changed.

## Structure

```
Commtel-Usecase-Framework/
â”œâ”€â”€ Framework/          Commtel use case framework (Excel)
â”œâ”€â”€ Use-Cases/
â”‚   â”œâ”€â”€ Weaponization/
â”‚   â”œâ”€â”€ Defense-Evasion/
â”‚   â””â”€â”€ Actions-on-Objectives/
â””â”€â”€ Advisories/         Regulator and threat advisories
```

Each use case folder holds the document as PDF and DOCX, plus `wazuh_rule_NNN.xml` when a Wazuh rule exists.

## Use cases

| CUC | Stage | Code | MITRE technique | Use case | Rules |
|---|---|---|---|---|---|
| [CUC-037](Use-Cases/Weaponization/CUC-037_WE-002-T1053.005_Scheduled_Task) | Weaponization | WE-002 | [T1053.005](https://attack.mitre.org/techniques/T1053/005/) | Scheduled Task | QRadar, Wazuh, Sigma |
| [CUC-045](Use-Cases/Weaponization/CUC-045_WE-002-T1047_Windows_Management_Instrumentation) | Weaponization | WE-002 | [T1047](https://attack.mitre.org/techniques/T1047/) | Windows Management Instrumentation | QRadar, Wazuh, Hayabusa |
| [CUC-276](Use-Cases/Delivery/CUC-276_DE-005-T1070.001_Clear_Windows_Event_Logs) | Delivery | DE-041 | [T1685.005](https://attack.mitre.org/techniques/T1685/005/) (was T1070.001) | Clear Windows Event Logs | QRadar, Wazuh, LogRhythm, Sigma |
| [CUC-349](Use-Cases/Delivery/CUC-349_DE-005-T1218.007_System_Binary_Proxy_Execution_Msiexec) | Delivery | DE-005 | [T1218.007](https://attack.mitre.org/techniques/T1218/007/) | System Binary Proxy Execution: Msiexec | QRadar, Sigma |
| [CUC-576](Use-Cases/Actions-on-Objectives/CUC-576_AO-040-T1490_Inhibit_System_Recovery) | Actions on Objectives | AO-040 | [T1490](https://attack.mitre.org/techniques/T1490/) | Inhibit System Recovery | QRadar, Wazuh |

Open a use case folder for its description and documents.

## Adding a use case

1. Create `Use-Cases/<Stage>/CUC-NNN_<Code>-<Technique>_<Name>/`.
2. Add the PDF, the DOCX and the Wazuh rule if there is one.
3. Add a row to the table above, update the Progress table, and set the status to Documented in the register.

## Related

- [Commtel Firewall Log Simulator](https://github.com/Hassanlodhi912/commtel_log_simulator): generates firewall logs to test these use cases.