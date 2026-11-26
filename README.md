# Commtel Use Case Framework

Commtel SIEM use case library. Each use case is mapped to a Cyber Kill Chain stage and a MITRE ATT&CK technique, with a full document (PDF and DOCX) and, where built, a Wazuh detection rule.

Maintained by **Hassan Kaleem**, Detection Engineer at Commtel.

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
| [CUC-276](Use-Cases/Delivery/CUC-276_DE-005-T1070.001_Clear_Windows_Event_Logs) | Delivery | DE-005 | [T1070.001](https://attack.mitre.org/techniques/T1070/001/) | Clear Windows Event Logs | QRadar, Wazuh, LogRhythm, Sigma |
| [CUC-349](Use-Cases/Delivery/CUC-349_DE-005-T1218.007_System_Binary_Proxy_Execution_Msiexec) | Delivery | DE-005 | [T1218.007](https://attack.mitre.org/techniques/T1218/007/) | System Binary Proxy Execution: Msiexec | QRadar, Sigma |
| [CUC-576](Use-Cases/Actions-on-Objectives/CUC-576_AO-040-T1490_Inhibit_System_Recovery) | Actions on Objectives | AO-040 | [T1490](https://attack.mitre.org/techniques/T1490/) | Inhibit System Recovery | QRadar, Wazuh |

Open a use case folder for its description and documents.

## Adding a use case

1. Create `Use-Cases/<Stage>/CUC-NNN_<Code>-<Technique>_<Name>/`.
2. Add the PDF, the DOCX and the Wazuh rule if there is one.
3. Add a row to the table above.

## Related

- [Commtel Firewall Log Simulator](https://github.com/Hassanlodhi912/commtel_log_simulator): generates firewall logs to test these use cases.