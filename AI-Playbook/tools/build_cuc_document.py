import sys, copy
sys.path.insert(0, sys.argv[3])
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEMPLATE, OUT, _, RULES = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
NAVY, LIGHT, GREY, NOTE = "E32229", "F2F2F2", "F2F2F2", "F2F2F2"
doc = Document(TEMPLATE)
body = doc.element.body

# ---------- front matter: keep, retitle ----------
def set_p_text(p, new):
    ts = p.findall('.//' + qn('w:t'))
    if not ts: return
    ts[0].text = new
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]: t.text = ''

def retitle(root):
    for p in root.iter(qn('w:p')):
        txt = ''.join(t.text or '' for t in p.findall('.//' + qn('w:t')))
        if not txt.strip(): continue
        new = txt
        if txt.startswith('WE-002-T1047'): new = txt.replace('WE-002-T1047', 'WE-002-T1053.005')
        elif txt.strip() == 'N/A': new = 'Initial release - Wazuh detection logic + Sigma, lab validation with Atomic Red Team'
        elif txt.strip() == 'CUC-045: Windows Management': new = 'CUC-037: Scheduled'
        elif txt.strip() == 'Instrumentation': new = 'Task'
        else:
            for a, b in (('CUC-045: Windows Management Instrumentation', 'CUC-037: Scheduled Logs'),
                         ('CUC-045 Windows Management Instrumentation', 'CUC-037 Scheduled Task'),
                         ('Windows Management Instrumentation', 'Scheduled Task'),
                         ('October 2026', 'November 2026'), ('18-Oct-2026', '15-Nov-2026'),
                         ('CUC \u2013 045', 'CUC \u2013 037'), ('CUC-045', 'CUC-037')):
                new = new.replace(a, b)
        if new != txt: set_p_text(p, new)

children = list(body)
cut = None; numpr = None
for i, el in enumerate(children):
    if el.tag == qn('w:p'):
        st = el.find('.//' + qn('w:pStyle'))
        if st is not None and st.get(qn('w:val')) == 'Heading1' and cut is None: cut = i
        if numpr is None and st is not None and st.get(qn('w:val')) == 'ListParagraph':
            n = el.find('.//' + qn('w:numPr'))
            if n is not None: numpr = copy.deepcopy(n)
for el in children[cut:]:
    if el.tag != qn('w:sectPr'): body.remove(el)
retitle(body)
for sdt in list(body.findall(qn('w:sdt'))):
    p = OxmlElement('w:p')
    def fc(t, dirty=False):
        r = OxmlElement('w:r'); f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), t)
        if dirty: f.set(qn('w:dirty'), 'true')
        r.append(f); return r
    p.append(fc('begin', True))
    r = OxmlElement('w:r'); it = OxmlElement('w:instrText'); it.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); it.text = ' TOC \\o "1-2" \\h \\z \\u '; r.append(it); p.append(r)
    p.append(fc('separate'))
    r = OxmlElement('w:r'); t = OxmlElement('w:t'); t.text = 'Right-click and choose Update Field to refresh the table of contents.'; r.append(t); p.append(r)
    p.append(fc('end'))
    sdt.addprevious(p); body.remove(sdt)
u = OxmlElement('w:updateFields'); u.set(qn('w:val'), 'true'); doc.settings.element.append(u)
for s in doc.sections:
    for part in (s.header, s.footer, s.first_page_header, s.first_page_footer, s.even_page_header, s.even_page_footer):
        try: retitle(part._element)
        except Exception: pass

# ---------- helpers ----------
def _sty(p, sid):
    ps = OxmlElement('w:pStyle'); ps.set(qn('w:val'), sid); p._p.get_or_add_pPr().insert(0, ps); return p
def H1(t): _sty(doc.add_paragraph(t), 'Heading1')
def H2(t): _sty(doc.add_paragraph(t), 'Heading2')
def P(t, size=10, bold=False, italic=False):
    p = doc.add_paragraph(); r = p.add_run(t); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    p.paragraph_format.space_after = Pt(4); return p
def B(t):
    p = _sty(doc.add_paragraph(), 'ListParagraph'); r = p.add_run(t); r.font.size = Pt(10)
    if numpr is not None: p._p.get_or_add_pPr().append(copy.deepcopy(numpr))
    p.paragraph_format.space_after = Pt(1); return p
def shade(cell, fill):
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    cell._tc.get_or_add_tcPr().append(shd)
def borders(tbl):
    pr = tbl._tbl.tblPr; b = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        x = OxmlElement('w:' + e); x.set(qn('w:val'), 'single'); x.set(qn('w:sz'), '4'); x.set(qn('w:space'), '0'); x.set(qn('w:color'), 'A6A6A6'); b.append(x)
    pr.append(b)
def cell_text(c, t, size=9, bold=False, color=None, mono=False, align=None):
    c.text = ''; p = c.paragraphs[0]; r = p.add_run(t); r.font.size = Pt(size); r.bold = bold
    if color: r.font.color.rgb = RGBColor.from_string(color)
    if mono: r.font.name = 'Consolas'
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(0)
def T(header, rows, mono_cols=()):
    t = doc.add_table(rows=1, cols=len(header)); borders(t)
    for i, h in enumerate(header):
        cell_text(t.rows[0].cells[i], h, bold=True, color='FFFFFF'); shade(t.rows[0].cells[i], NAVY)
    for row in rows:
        cs = t.add_row().cells
        for i, v in enumerate(row): cell_text(cs[i], v, mono=(i in mono_cols), size=8.5 if i in mono_cols else 9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2); return t
def KV(rows):
    t = doc.add_table(rows=0, cols=2); borders(t)
    for k, v in rows:
        cs = t.add_row().cells; cell_text(cs[0], k, bold=True, color='FFFFFF'); shade(cs[0], NAVY); cell_text(cs[1], v)
    for r in t.rows: r.cells[0].width = Pt(150); r.cells[1].width = Pt(330)
    doc.add_paragraph().paragraph_format.space_after = Pt(2); return t
def CODE(text, size=8):
    t = doc.add_table(rows=1, cols=1); borders(t); c = t.rows[0].cells[0]; shade(c, GREY); c.text = ''
    first = True
    for line in text.strip('\n').split('\n'):
        p = c.paragraphs[0] if first else c.add_paragraph(); first = False
        r = p.add_run(line); r.font.name = 'Consolas'; r.font.size = Pt(size)
        r._r.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Consolas')
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
def SHOTS(pairs, start):
    n = start
    for a, b in pairs:
        t = doc.add_table(rows=2, cols=2); borders(t)
        for i, cap in enumerate((a, b)):
            c = t.rows[0].cells[i]; shade(c, NOTE)
            cell_text(c, '\n\n[ SCREENSHOT %d \u2013 INSERT HERE ]\n\n' % (n + i), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
            cell_text(t.rows[1].cells[i], 'Figure %d: %s' % (n + i, cap), size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        n += 2
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---------- content ----------

import os, tempfile
from PIL import Image
SHOT_DIR = os.environ['SHOT_DIR']; TMP = tempfile.mkdtemp()
def prep(name, box=None):
    p = os.path.join(SHOT_DIR, name + '.png')
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGB')
    if box: im = im.crop(box)
    o = os.path.join(TMP, name + '_c.png'); im.save(o); return o
FIGN = [0]
def fig_row(items):
    items = [x for x in items if x[0]]
    if not items: return
    n = len(items); t = doc.add_table(rows=2, cols=n); borders(t); w = 218 if n == 2 else 446
    for k, (img, cap) in enumerate(items):
        FIGN[0] += 1
        c = t.rows[0].cells[k]; c.text = ''; p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img, width=Pt(w)); p.paragraph_format.space_after = Pt(0)
        cell_text(t.rows[1].cells[k], 'Figure %d: %s' % (FIGN[0], cap), size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
H1('Scope:')
B('To cover MITRE ATT&CK Framework Tactic Persistence (TA0003), with Privilege Escalation (TA0004) and Execution (TA0002), Technique T1053 \u2013 Scheduled Task/Job, Sub-technique T1053.005 \u2013 Scheduled Task.')
B('To cover 1 procedure of the Weaponization phase of the Cyber Kill Chain Framework (as mapped in the Commtel L3 usecase register).')
B('Detection logic for IBM QRadar and Wazuh (Wazuh rule IDs 100370 \u2013 100379) plus a vendor-neutral Sigma rule; role-based investigation steps for L1 and L2 analysts.')
B('Lab validation of the detection logic with Atomic Red Team (6 procedures) and native schtasks commands.')

H1('Context:')
P('Adversaries abuse the Windows Task Scheduler to run code at a chosen time, at logon or at startup. A scheduled task survives reboots (persistence), can run as SYSTEM (privilege escalation) and can be created on a remote host (lateral movement). Tasks are created with schtasks.exe, the PowerShell ScheduledTasks cmdlets, the CIM method PS_ScheduledTask.RegisterByXml, or by importing task XML. Windows records every creation as Security Event ID 4698, which carries the task name and the full task XML (command, arguments, run-as account, hidden flag).')
B('Turla scheduled tasks to run its Topinambour and KopiLuwak implants; both are emulated by Atomic Red Team tests for T1053.005.')
B('Ransomware operators (for example Conti) create scheduled tasks on many hosts to launch the payload at the same time.')
B('Commodity malware and loaders create a logon or startup task to survive a reboot, often hidden or running from a user-writable folder.')

H1('Detection Scope:')
H2('Detection Technologies:')
B('SIEM (IBM QRadar, Wazuh). EDR optional for enrichment and host isolation.')
H2('Log source Type:')
B('Microsoft Windows \u2013 Security log: Event ID 4698 (scheduled task created) and 4688 (process creation with command line).')
B('Microsoft Windows \u2013 Microsoft-Windows-TaskScheduler/Operational: Event ID 106 (task registered). Optional, adds the registering user.')
B('Microsoft Windows \u2013 Microsoft-Windows-PowerShell/Operational: Event ID 4104 (Script Block Logging).')
B('Microsoft Sysmon \u2013 optional: Event ID 1 (process creation).')
H2('Scope:')
B('All Windows assets (workstations and servers); servers and domain controllers at highest priority.')

H1('Prerequisites:')
B('Audit Other Object Access Events (Success) enabled. Without it Event ID 4698 is not generated; this is the key requirement of the usecase.')
B('Audit Process Creation (Success) with "Include command line in process creation events" (Event ID 4688 with the command line).')
B('PowerShell Script Block Logging enabled.')
B('Microsoft-Windows-TaskScheduler/Operational log enabled (it is disabled by default) and collected, if Event ID 106 is wanted.')
B('Log collection agent (Wazuh agent, or WinCollect for QRadar) forwards the Security, PowerShell/Operational and TaskScheduler/Operational channels.')
B('Reference list recommended: "CUC-037: Authorized Task Accounts" (software deployment and management accounts that create tasks, e.g. SCCM/Intune service accounts).')
CODE(r'''auditpol /set /subcategory:"Other Object Access Events" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" /v EnableScriptBlockLogging /t REG_DWORD /d 1 /f
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true''')

H1('Rule Logic:')
P('The core detection is Event ID 4698, which sees a task however it was created. Rules on 4688 and 4104 identify the tool and add context, and catch tasks created while 4698 auditing is off.')
T(['Rule ID', 'Rule Name', 'Event Source', 'Logic', 'Severity', 'Wazuh ID'],
  [['CUC-037-R1', 'Scheduled Task Created', 'Security 4698', 'Event ID = 4698; raised in severity by R2 to R4 when the task XML is hidden, runs as SYSTEM or highest privileges, or runs an interpreter / user-writable path', 'Medium / High', '100373, 100374, 100375, 100376'],
   ['CUC-037-R2', 'Task Created via schtasks', 'Security 4688', 'Process = schtasks.exe AND command line contains /create', 'Medium', '100370'],
   ['CUC-037-R3', 'Persistent or Remote schtasks Task', 'Security 4688', '/create AND (/sc onlogon, onstart or onidle, OR /ru SYSTEM, OR /s <remote host>)', 'High', '100371, 100372'],
   ['CUC-037-R4', 'PowerShell Task Registration', 'PowerShell 4104', 'Script block contains Register-ScheduledTask, Register-ScheduledJob, Set-ScheduledTask, New-ScheduledTaskAction, PS_ScheduledTask or RegisterByXml as a whole command name; PowerShell auto-generated wrapper code and the known Atomic setup module are excluded', 'Medium', '100377, 100378'],
   ['CUC-037-R5', 'Multiple Tasks Created', 'Correlation', '3 or more R1 alerts on the same host within 300 seconds', 'Critical', '100379']])
H2('Sigma Rule:')
CODE(r'''title: CUC-037 Scheduled Task Created
id: 5d3c8f10-037a-4b2e-9c1d-100370100379
status: test
description: Detects creation of Windows scheduled tasks (4698) and the tools used to create them
tags: [attack.persistence, attack.privilege_escalation, attack.execution, attack.t1053.005]
logsource: {product: windows}
detection:
  task_created:
    EventID: 4698
  schtasks:
    EventID: 4688
    NewProcessName|endswith: '\schtasks.exe'
    CommandLine|contains: '/create'
  powershell:
    ScriptBlockText|contains: ['Register-ScheduledTask', 'Register-ScheduledJob', 'PS_ScheduledTask', 'RegisterByXml']
  condition: task_created or schtasks or powershell
falsepositives: [Software deployment (SCCM/Intune), backup and monitoring agents, administrator maintenance]
level: high''')
H2('Wazuh Rules:')
P('Deployed as /var/ossec/etc/rules/cuc_037.xml (same per-CUC file convention as the other CUCs). ID 100378 is a level 0 tuning rule and raises no alert.', size=9, italic=True)
CODE(open(RULES, encoding='utf-8').read(), size=7)
P('Wazuh deployment (manager) and agent configuration', bold=True)
B('Copy cuc_037.xml to /var/ossec/etc/rules/ on the Wazuh manager (owner wazuh:wazuh, mode 660). The rules extend the stock rules 60228 (Security 4698), 67027 (Security 4688) and 91802 (PowerShell script block), which must be present.')
B('Validate: /var/ossec/bin/wazuh-analysisd -t (must exit 0), then restart: systemctl restart wazuh-manager.')
B('Verify in the dashboard: Threat Hunting, Events, query rule.groups: cuc_037.')
B('Chain the rules to the stock parent rules with if_sid, as in this file. Do not use <if_group>windows</if_group> in a CUC rule file: with several CUC files loaded it multiplies the rule tree and exhausts the manager memory.')
B('On every Windows agent, ossec.conf must collect the channels below (add TaskScheduler/Operational for Event ID 106); restart the agent after the change.')
CODE(r"""<localfile><location>Security</location><log_format>eventchannel</log_format></localfile>
<localfile><location>Microsoft-Windows-PowerShell/Operational</location><log_format>eventchannel</log_format></localfile>
<localfile><location>Microsoft-Windows-TaskScheduler/Operational</location><log_format>eventchannel</log_format></localfile>""", size=8)

H2('QRadar Reference:')
P('Reference for SOC analysts to implement this use case on the client IBM QRadar (WinCollect, Microsoft Windows Security Event Log DSM). The detection logic is the one validated in the lab on Wazuh.', size=9, italic=True)
P('1. Prepare (once)', bold=True)
B('Collect the Security and Microsoft-Windows-PowerShell/Operational channels through WinCollect.')
B('Custom event properties (Admin > Custom Event Properties; create only if missing). Regex, capture group 1:')
T(['Property', 'Regex'],
  [['Process Name', r'New Process Name:\s*(.+?)\s+Token Elevation Type:'],
   ['Process Command Line', r'Process Command Line:\s*(.*?)\s+Token Elevation Type indicates'],
   ['Task Name', r'Task Name:\s*(.+?)\s+Task Content:'],
   ['ScriptBlock Text', r'Creating Scriptblock text \(\d+ of \d+\):\s*(.*?)\s*ScriptBlock ID']], mono_cols=(1,))
B('Reference set (AlphaNumeric, Ignore Case, Lives Forever): CUC-037: Authorized Task Accounts (empty at go-live).')
P('2. Create the rules', bold=True)
T(['Rule', 'Name', 'Log source and event', 'Condition', 'Sev.'],
  [['BB', 'BB: CUC-037: Task Created Event', 'Windows Security log, Event ID 4698', r'Event Payload matches EventID=4698\s', '-'],
   ['1', 'Scheduled Task Created', 'Windows Security log, Event ID 4698 (task created)', 'BB: CUC-037: Task Created Event', '5'],
   ['2', 'Task Created via schtasks', 'Windows Security log, Event ID 4688, process created (QID 5000862)', r'Process Name contains schtasks.exe AND Command Line contains /create', '6'],
   ['3', 'Persistent or SYSTEM schtasks Task', 'Windows Security log, Event ID 4688 (QID 5000862)', r'Command Line contains /create AND contains any of: onlogon, onstart, onidle, "/ru system"', '8'],
   ['4', 'Remote schtasks Task', 'Windows Security log, Event ID 4688 (QID 5000862)', r'Command Line contains /create AND contains " /s "', '8'],
   ['5', 'Hidden Task', 'Windows Security log, Event ID 4698', r'BB: CUC-037: Task Created Event AND Event Payload contains Hidden>true', '8'],
   ['6', 'Task as SYSTEM or Highest Privileges', 'Windows Security log, Event ID 4698', r'BB AND Event Payload contains any of: S-1-5-18, HighestAvailable', '7'],
   ['7', 'PowerShell Task Registration', 'PowerShell Operational log, Event ID 4104', r'Event Payload matches EventID=4104\s AND ScriptBlock Text contains any of: Register-ScheduledTask, Register-ScheduledJob, New-ScheduledTaskAction, PS_ScheduledTask, RegisterByXml (whole name) AND NOT __cmdletization', '7'],
   ['8', 'Multiple Tasks Created (correlation)', 'BB: CUC-037: Task Created Event', 'At least 3 events, same Source IP, within 5 minutes', '9']])
B('Rules 1 to 7: log source Microsoft Windows Security Event Log, detected by the LOCAL system, AND NOT Username in CUC-037: Authorized Task Accounts. Name each rule "CUC-037: MITRE T1053.005: <name>".')
B('Conditions are plain text ("contains any of" test in QRadar). Only the Event ID conditions use a regular expression: | means OR, and \\s means one space or tab (backslash then s).')
B('Response: index the offense on Source IP so rules 1 to 8 land in one offense; response limiter once per 30 minutes per Source IP.')
P('3. Hunt (Log Activity > Advanced Search, LAST 24 HOURS)', bold=True)
P('H1: Scheduled tasks created (Rule 1). Run this first to confirm 4698 reaches QRadar.', size=9, bold=True)
CODE(r"""SELECT DATEFORMAT(starttime,'yyyy-MM-dd HH:mm:ss') AS "Time", LOGSOURCENAME(logsourceid) AS "Host", username AS "User", REPLACEFIRST('.*Task Name:\s*(.*?)\s+Task Content:.*', UTF8(payload), '$1') AS "Task" FROM events WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows Security%' AND UTF8(payload) IMATCHES '.*EventID=4698\s.*' ORDER BY starttime DESC LAST 24 HOURS""", size=7.5)
P('H2: schtasks creating tasks (Rules 2 to 4).', size=9, bold=True)
CODE(r"""SELECT DATEFORMAT(starttime,'yyyy-MM-dd HH:mm:ss') AS "Time", LOGSOURCENAME(logsourceid) AS "Host", username AS "User", REPLACEFIRST('.*Process Command Line:\s*(.*?)\s+Token Elevation Type indicates.*', UTF8(payload), '$1') AS "Command Line" FROM events WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows Security%' AND QIDNAME(qid) ILIKE '%new process has been created%' AND UTF8(payload) IMATCHES '.*New Process Name:\s*\S*\\schtasks\.exe\s.*' AND UTF8(payload) IMATCHES '.*Process Command Line:.*/create.*' ORDER BY starttime DESC LAST 24 HOURS""", size=7.5)
P('H3: Baseline, who creates tasks (7 days). Use before any whitelisting decision.', size=9, bold=True)
CODE(r"""SELECT username AS "User", LOGSOURCENAME(logsourceid) AS "Host", COUNT(*) AS "Tasks" FROM events WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Windows Security%' AND UTF8(payload) IMATCHES '.*EventID=4698\s.*' GROUP BY username, logsourceid ORDER BY "Tasks" DESC LAST 7 DAYS""", size=7.5)

H1('Payload Details:')
P('Normalized Wazuh fields observed in the lab alerts (host, account and SID values removed):')
T(['Event', 'Field', 'Value observed'],
  [['Security 4698', 'data.win.system.eventID / channel', '4698 / Security'],
   ['', 'data.win.eventdata.taskName', '\\<task name>'],
   ['', 'data.win.eventdata.subjectUserName', '<account that created the task>'],
   ['', 'data.win.eventdata.taskContent', 'Task XML (escaped): <Command>, <Arguments>, <UserId> or <GroupId>, <RunLevel>, <Hidden>, trigger type'],
   ['Security 4688', 'data.win.eventdata.newProcessName', 'C:\\Windows\\System32\\schtasks.exe'],
   ['', 'data.win.eventdata.commandLine', 'schtasks  /create /tn <name> /sc onlogon /tr "cmd.exe /c calc.exe"'],
   ['', 'data.win.eventdata.parentProcessName', 'C:\\Windows\\System32\\cmd.exe'],
   ['TaskScheduler 106', 'data.win.eventdata.taskName', '\\<task name> (task registered)'],
   ['PowerShell 4104', 'data.win.eventdata.scriptBlockText', '... Register-ScheduledTask <name> -InputObject $object ...']], mono_cols=(1, 2))
P('Note: the task XML in taskContent reaches Wazuh XML-escaped (&lt; for <), so regexes on taskContent must accept both forms.', size=9, italic=True)

H1('SOPs to Tune:')
B('Add approved software-deployment and management accounts to "CUC-037: Authorized Task Accounts" and lower the level for them instead of disabling the rules.')
B('R1: extend the interpreter / user-writable path list with client-specific binaries; exclude exact vendor task names (for example updater tasks) after custodian confirmation, never a whole host.')
B('R5: raise the threshold (3 tasks / 300 s) on hosts where installers create several tasks by design.')
H1('Expected Blindspot:')
B('Event ID 4698 is not generated if Audit Other Object Access Events is off; hosts without it rely on the 4688 and 4104 rules only.')
B('Tasks created by code that does not spawn schtasks.exe or PowerShell (direct COM / Task Scheduler API calls) are visible only in 4698 and in TaskScheduler 106.')
B('Tasks created while the agent is stopped are forwarded when it returns, but 4688 events may be lost.')
B('R4 is tuned to ignore Unregister-ScheduledTask, PowerShell auto-generated wrapper code and the Atomic setup module when it is only loaded. Real task registration still alerts.')

H1('Validation:')
H2('Lab Environment:')
KV([('Victim host', 'Windows 11 VM with Sysmon, command-line auditing (4688), task-create auditing (4698), Script Block Logging, Wazuh agent'),
    ('SIEM', 'Wazuh 4.14 all-in-one (manager, indexer, dashboard)'),
    ('Attack simulation', 'Invoke-AtomicRedTeam 2.3.0 and native schtasks commands, run as local administrator'),
    ('Agent channels verified', 'Application, Security, System, Sysmon/Operational, PowerShell/Operational, TaskScheduler/Operational')])
H2('Validation Procedure:')
CODE(r'''Invoke-AtomicTest T1053.005 -ShowDetailsBrief
Invoke-AtomicTest T1053.005 -TestNumbers 1,2,4,6,8,9          # schtasks, PowerShell cmdlets, CIM RegisterByXml, hidden XML task
schtasks /create /s 127.0.0.1 /tn CUC037remote /sc once /st 23:59 /tr "cmd.exe /c calc.exe"   # remote-style target
Invoke-AtomicTest T1053.005 -TestNumbers 1,2,4,6,8,9 -Cleanup''')
H2('Detection Results:')
T(['Procedure', 'Telemetry', 'Rule', 'Wazuh ID (level)', 'Result'],
  [['Test 1: schtasks onlogon and onstart as SYSTEM', 'Security 4688', 'R3', '100371 (12)', 'Detected'],
   ['Test 1: tasks created (SYSTEM, cmd.exe)', 'Security 4698', 'R1', '100375 (10), 100376 (10)', 'Detected'],
   ['Test 2: schtasks /create /sc once', 'Security 4688', 'R2', '100370 (8)', 'Detected'],
   ['Test 4, 9: Register-ScheduledTask (highest privileges)', 'Security 4698', 'R1', '100375 (10)', 'Detected'],
   ['Tests 4, 6, 9: PowerShell / CIM task registration', 'PowerShell 4104', 'R4', '100377 (10)', 'Detected'],
   ['Test 6: CIM RegisterByXml task', 'Security 4698', 'R1', '100373 (6)', 'Detected (base rule)'],
   ['Test 8: XML task with Hidden attribute', 'Security 4698', 'R1', '100374 (12)', 'Detected'],
   ['schtasks /create /s (remote-style target)', 'Security 4688', 'R3', '100372 (12)', 'Detected'],
   ['Several tasks within 300 s', 'Correlation', 'R5', '100379 (13)', 'Detected']])
H2('Key Observations:')
B('Event ID 4698 is generated for every method (schtasks, PowerShell, CIM, XML import), so R1 is the tool-independent core of the usecase.')
B('A Wazuh frequency rule replaces the alert of the event that completes the threshold; when validating a single-task rule, run it on its own, outside the correlation window.')
B('The task XML in taskContent carries what matters for triage: the command, the run-as account (S-1-5-18 is SYSTEM), the run level and the Hidden flag.')
B('Task Scheduler/Operational logging is disabled by default; Event ID 4698 does not depend on it.')
H2('SIEM Alert Evidence:')
fig_row([(prep('f1'), 'Atomic Red Team console: T1053.005 test list'), (prep('f2'), 'Event Viewer: Security Event ID 4698, scheduled task created')])
fig_row([(prep('f3'), 'Wazuh alerts, rules 100370 / 100371 / 100372 (schtasks)')])
fig_row([(prep('f4'), 'Wazuh alerts, rules 100373 to 100376 (Event ID 4698)')])
fig_row([(prep('f5'), 'Wazuh alerts, rules 100377 (PowerShell) and 100379 (multiple tasks)')])

H1('False Positive scenarios:')
B('Software deployment and endpoint management (SCCM/MECM, Intune, PDQ) creating tasks.')
B('Backup, monitoring and antivirus agents that register their own tasks; vendor updaters (browser, Office, drivers).')
B('Administrators creating maintenance tasks, and installers that create several tasks at once.')

H1('Response:')
H2('Investigation:')
P('L1 Analyst \u2013 Initial Triage (target: within 15 minutes of alert)', bold=True)
B('Identify host, account (subjectUserName), task name and the rule that fired; read the task XML: command, arguments, run-as account, trigger and Hidden flag.')
B('Check the account and task against CUC-037: Authorized Task Accounts, known vendor tasks and change tickets; close as false positive if it is approved.')
B('Escalate to L2 immediately if: the task is hidden, runs as SYSTEM from a user-writable path (%TEMP%, %APPDATA%, Downloads, ProgramData), runs cmd, PowerShell, wscript, mshta or rundll32, was created on a remote host, or R5 fired.')
P('L2 Analyst \u2013 In-Depth Investigation', bold=True)
B('Rebuild the timeline on the host: the process that created the task (4688 parent chain), the logon session, and any file written just before the task was registered.')
B('Collect the task XML and the binary or script it runs; check hash reputation and whether it already executed (TaskScheduler 200/201, Sysmon 1).')
B('Hunt for the same task name, command or account on other hosts (H1 to H3) and for other persistence (services, Run keys).')
H2('Remediation:')
B('Unauthorized task confirmed: delete the task (schtasks /delete), remove the file it runs, isolate the host, disable or reset the account that created it, and treat the host as compromised.')
B('Restrict who can create tasks: remove unneeded local administrators and limit "Log on as a batch job" and remote Task Scheduler access.')
B('Keep Audit Other Object Access Events enabled and collected on every Windows host.')
B('Authorized activity: document it in the ticket and add the account or task to the tuning list.')

H1('Appendix:')
KV([('MITRE Tactic', 'Execution (TA0002), Persistence (TA0003), Privilege Escalation (TA0004)'),
    ('MITRE Technique', 'T1053.005 \u2013 Scheduled Task/Job: Scheduled Task'),
    ('Commtel Usecase Framework Code', 'WE-002-T1053.005'),
    ('Commtel Usecase Identifier', 'CUC-037'),
    ('Cyber Kill Chain Phase', 'Weaponization (as mapped in the Commtel usecase register)'),
    ('Data Source', 'Scheduled Job: Scheduled Job Creation (DS0003), Process: Process Creation (DS0009), Command: Command Execution (DS0017)'),
    ('Windows Security Event ID - 4698', 'A scheduled task was created (needs Audit Other Object Access Events)'),
    ('Windows Security Event ID - 4688', 'Process creation and command-line visibility (schtasks)'),
    ('TaskScheduler Event ID - 106', 'Task registered (Microsoft-Windows-TaskScheduler/Operational)'),
    ('PowerShell Event ID - 4104', 'Script block logging (decoded PowerShell)'),
    ('Atomic Red Team', 'T1053.005 \u2013 14 tests; 6 validated (1, 2, 4, 6, 8, 9)'),
    ('Related', 'T1059.001 \u2013 PowerShell; T1543.003 \u2013 Windows Service (persistence); T1021 \u2013 Remote Services'),
    ('Wazuh Rule IDs', '100370 \u2013 100379'),
    ('Severity', 'High (level 12); Critical for multiple tasks (level 13)'),
    ('Status', 'Use case logic validated in lab (Wazuh). QRadar reference provided for implementation on the client SIEM')])

WIDTHS = {'Rule ID': [58, 78, 72, 150, 48, 54], 'Procedure': [95, 70, 32, 70, 34, 88], 'Event': [62, 200, 190], 'Rule': [28, 110, 105, 155, 32], 'Property': [110, 330], 'Symbol': [50, 150, 240]}
for tb in doc.tables:
    h = tb.rows[0].cells[0].text.strip()
    if h in WIDTHS and len(tb.columns) == len(WIDTHS[h]):
        tb.autofit = False
        for r in tb.rows:
            for c, w in zip(r.cells, WIDTHS[h]): c.width = Pt(w)

for tb in doc.tables:
    rows = {r.cells[0].text.strip(): r for r in tb.rows}
    if 'Prepared By' in rows and 'Supervised By' in rows:
        src = rows['Supervised By'].cells[1].paragraphs[0]; dst = rows['Prepared By'].cells[1].paragraphs[0]
        for x in list(dst.runs): x._r.getparent().remove(x._r)
        run = dst.add_run('Arham')
        if src.runs and src.runs[0]._r.rPr is not None: run._r.insert(0, copy.deepcopy(src.runs[0]._r.rPr))
def _flag(parent, tag):
    if parent.find(qn(tag)) is None: parent.append(OxmlElement(tag))
for tb in doc.tables:
    for ri, r in enumerate(tb.rows):
        if len(tb.rows) > 1: _flag(r._tr.get_or_add_trPr(), 'w:cantSplit')
        if ri == 0 and len(tb.rows) > 1:
            if len(tb.rows) > 2: _flag(r._tr.get_or_add_trPr(), 'w:tblHeader')
            for c in r.cells:
                for q in c.paragraphs: q.paragraph_format.keep_with_next = True
for q in doc.paragraphs:
    if q._p.pPr is not None and q._p.pPr.pStyle is not None and q._p.pPr.pStyle.val.lower().startswith('heading'): q.paragraph_format.keep_with_next = True
for s in doc.styles:
    if s.name and s.name.upper().startswith('TOC ') and s.type == 1:
        s.paragraph_format.space_before = Pt(0); s.paragraph_format.space_after = Pt(0); s.paragraph_format.line_spacing = 1.0
for q in doc.paragraphs:
    if q._p.pPr is not None and q._p.pPr.pStyle is not None and q._p.pPr.pStyle.val.upper().startswith('TOC'):
        q.paragraph_format.space_before = Pt(0); q.paragraph_format.space_after = Pt(0); q.paragraph_format.line_spacing = 1.0
doc.save(OUT)
print('saved', OUT)
