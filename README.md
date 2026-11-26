# Commtel Use Case Framework

Commtel SIEM use case library. Each use case is mapped to a kill chain stage and a MITRE ATT&CK technique, with a full document (PDF and DOCX) and, where built, a Wazuh detection rule.

Maintained by **Hassan Kaleem**, Detection Engineer at Commtel.

## Structure

```
Commtel-Usecase-Framework/
├── Framework/          Commtel use case framework (Excel)
├── Use-Cases/
│   ├── Weaponization/
│   ├── Defense-Evasion/
│   └── Actions-on-Objectives/
└── Advisories/         Regulator and threat advisories
```

Each use case folder holds the document as PDF and DOCX, plus `wazuh_rule_NNN.xml` when a Wazuh rule exists.

## Use cases

| CUC | Stage | Code | MITRE technique | Use case | Files |
|---|---|---|---|---|---|
| CUC-037 | Weaponization | WE-002 | [T1053.005](https://attack.mitre.org/techniques/T1053/005/) | Scheduled Task | [Folder](Use-Cases/Weaponization/CUC-037_WE-002-T1053.005_Scheduled_Task) |
| CUC-276 | Defense Evasion | DE-005 | [T1070.001](https://attack.mitre.org/techniques/T1070/001/) | Clear Windows Event Logs | [Folder](Use-Cases/Defense-Evasion/CUC-276_DE-005-T1070.001_Clear_Windows_Event_Logs) |
| CUC-576 | Actions on Objectives | AO-040 | [T1490](https://attack.mitre.org/techniques/T1490/) | Inhibit System Recovery | [Folder](Use-Cases/Actions-on-Objectives/CUC-576_AO-040-T1490_Inhibit_System_Recovery) |

## Adding a use case

1. Create `Use-Cases/<Stage>/CUC-NNN_<Code>-<Technique>_<Name>/`.
2. Add the PDF, the DOCX and the Wazuh rule if there is one.
3. Add a row to the table above.

## Related

- [Commtel Firewall Log Simulator](https://github.com/Hassanlodhi912/commtel_log_simulator): generates firewall logs to test these use cases.