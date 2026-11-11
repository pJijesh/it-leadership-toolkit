"""Build the KPI catalogue (CSV and Markdown) and the risk register files.

Run from the repository root:  python tools/build_csvs.py
All targets are examples. They are starting points to be replaced with your own.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import example_data as ex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

KPI_COLUMNS = ["id", "domain", "name", "definition", "formula", "data_source", "target_example", "unit", "better_when", "owner", "cadence"]

# id, domain, name, definition, formula, source, target (example), unit, better when, owner, cadence
KPIS = [
    # ---- Service desk
    ("SD-01", "Service desk", "First response within SLA", "Share of tickets where the first human response was sent within the agreed response time.", "Tickets with first response within SLA / all tickets raised in the period x 100", "ITSM tool", "95% or more", "%", "Higher", "Service Desk Lead", "Monthly"),
    ("SD-02", "Service desk", "Resolution within SLA", "Share of resolved tickets closed within the agreed resolution time for their priority.", "Tickets resolved within SLA / all tickets resolved in the period x 100", "ITSM tool", "95% or more", "%", "Higher", "Service Desk Lead", "Monthly"),
    ("SD-03", "Service desk", "First contact resolution", "Share of tickets resolved on first contact without hand-off or callback.", "Tickets resolved at first contact / all tickets resolved x 100", "ITSM tool", "70% or more", "%", "Higher", "Service Desk Lead", "Monthly"),
    ("SD-04", "Service desk", "Aged ticket backlog", "Number of open tickets older than 30 days at period end, excluding tickets waiting on a supplier or the customer.", "Count of open tickets with age over 30 days", "ITSM tool", "10 or fewer", "count", "Lower", "Service Desk Lead", "Monthly"),
    ("SD-05", "Service desk", "Customer satisfaction (CSAT)", "Average score from the post-resolution survey on a 1 to 5 scale. Report the response rate alongside it.", "Sum of survey scores / number of responses", "ITSM survey", "4.3 or more", "score (1 to 5)", "Higher", "Service Desk Lead", "Monthly"),
    ("SD-06", "Service desk", "Ticket reopen rate", "Share of resolved tickets that were reopened within seven days, a signal of poor fixes or premature closure.", "Tickets reopened within 7 days / tickets resolved x 100", "ITSM tool", "5% or less", "%", "Lower", "Service Desk Lead", "Monthly"),
    # ---- Availability and change
    ("AV-01", "Availability", "Core service availability", "Time a named business-critical service was available during its agreed service hours.", "(Agreed service minutes - downtime minutes) / agreed service minutes x 100", "Monitoring tool, incident records", "99.9% or more", "%", "Higher", "Infrastructure Lead", "Monthly"),
    ("AV-02", "Availability", "Priority 1 incidents", "Number of incidents that stopped a critical service or affected a large share of users.", "Count of incidents logged at priority 1 in the period", "ITSM tool", "2 or fewer per month", "count", "Lower", "Service Delivery Manager", "Monthly"),
    ("AV-03", "Availability", "Mean time to restore (priority 1 and 2)", "Average time from incident start to service restored for the highest priority incidents.", "Sum of restore durations / number of incidents", "ITSM tool", "4 hours or less", "hours", "Lower", "Service Delivery Manager", "Monthly"),
    ("AV-04", "Availability", "Change success rate", "Share of changes implemented without causing an incident, rollback or unplanned outage.", "Successful changes / all changes implemented x 100", "ITSM change records", "95% or more", "%", "Higher", "Change Manager", "Monthly"),
    ("AV-05", "Availability", "Emergency change ratio", "Share of changes raised as emergencies, a signal of weak planning.", "Emergency changes / all changes x 100", "ITSM change records", "5% or less", "%", "Lower", "Change Manager", "Monthly"),
    ("AV-06", "Availability", "Backup restore tests passed", "Share of scheduled restore tests that recovered data within the target time.", "Restore tests passed / restore tests performed x 100", "Backup tool, test records", "100% of scheduled tests", "%", "Higher", "Infrastructure Lead", "Quarterly"),
    # ---- Security
    ("SE-01", "Security", "Multi-factor authentication coverage", "Share of active user accounts protected by multi-factor authentication.", "Accounts with MFA enforced / active accounts x 100", "Identity platform", "100%", "%", "Higher", "Security Lead", "Monthly"),
    ("SE-02", "Security", "Critical patches applied on time", "Share of critical security patches applied within the agreed window.", "Critical patches applied within 14 days / critical patches released x 100", "Patch management tool", "95% or more (14-day window is an example)", "%", "Higher", "Infrastructure Lead", "Monthly"),
    ("SE-03", "Security", "Open critical vulnerabilities", "Number of critical vulnerabilities open beyond the agreed remediation window at period end.", "Count of critical findings past due", "Vulnerability scanner", "0", "count", "Lower", "Security Lead", "Monthly"),
    ("SE-04", "Security", "Phishing exercise click rate", "Share of staff who clicked a link in a simulated phishing email.", "Staff who clicked / staff who received x 100", "Awareness platform", "Under 5%", "%", "Lower", "Security Lead", "Quarterly"),
    ("SE-05", "Security", "Security incidents by severity", "Number of confirmed security incidents, reported by severity band, with time to contain.", "Count of confirmed incidents per severity band", "Security incident log", "0 major incidents", "count", "Lower", "Security Lead", "Monthly"),
    ("SE-06", "Security", "Privileged access reviews completed", "Share of scheduled reviews of administrator and other privileged accounts completed on time.", "Reviews completed on time / reviews due x 100", "Identity platform, review records", "100%", "%", "Higher", "Security Lead", "Quarterly"),
    # ---- Projects
    ("PR-01", "Projects", "Projects reporting Green", "Share of active projects with an overall Green status at period end.", "Projects at Green / active projects x 100", "Project portfolio tracker", "Track trend; set a floor locally", "%", "Higher", "Head of PMO or IT Manager", "Monthly"),
    ("PR-02", "Projects", "Milestones delivered on time", "Share of milestones due in the period that were completed by their baseline date.", "Milestones met on time / milestones due x 100", "Project plans", "85% or more", "%", "Higher", "Project Manager", "Monthly"),
    ("PR-03", "Projects", "Schedule slippage", "Average days late against baseline for projects in delivery.", "Sum of (forecast finish - baseline finish) / number of projects", "Project plans", "10 days or fewer", "days", "Lower", "Project Manager", "Monthly"),
    ("PR-04", "Projects", "Project budget variance", "Forecast final cost against approved budget for projects in delivery.", "(Forecast final cost - approved budget) / approved budget x 100", "Project cost tracker, finance ledger", "Within plus or minus 5%", "%", "Closer to zero", "Project Manager", "Monthly"),
    ("PR-05", "Projects", "Benefits realised", "Value of benefits confirmed by the business owner against the benefits in the business case.", "Benefits confirmed / benefits planned for the period x 100", "Benefits register", "90% or more", "%", "Higher", "Project Sponsor", "Quarterly"),
    ("PR-06", "Projects", "High and critical project risks open", "Number of open project risks rated High or Critical.", "Count of open project risks with rating High or Critical", "Risk register", "Track trend", "count", "Lower", "Project Manager", "Monthly"),
    # ---- Cost
    ("CO-01", "Cost", "Spend against budget, year to date", "Actual IT spend against budget for the year to date.", "(YTD actual - YTD budget) / YTD budget x 100", "Finance ledger, budget tracker", "Within plus or minus 3%", "%", "Closer to zero", "IT Manager", "Monthly"),
    ("CO-02", "Cost", "Forecast accuracy", "How close last month's full-year forecast was to the latest outturn, as an absolute percentage.", "Absolute value of (latest outturn - prior forecast) / latest outturn x 100", "Budget tracker", "Within 3%", "%", "Lower", "IT Manager", "Monthly"),
    ("CO-03", "Cost", "CapEx share of IT spend", "Share of full-year outturn classed as CapEx under the organisation's accounting policy.", "CapEx outturn / total outturn x 100", "Budget tracker, finance policy", "Track against plan", "%", "Closer to plan", "IT Manager", "Quarterly"),
    ("CO-04", "Cost", "IT run cost per user", "Annual IT operating cost divided by the number of active users, used for trend and internal comparison.", "IT OpEx for the period / average active users", "Finance ledger, identity platform", "Track trend; no external benchmark assumed", "GBP per user", "Lower", "IT Manager", "Quarterly"),
    ("CO-05", "Cost", "Licence utilisation", "Share of purchased licences that were actively used in the last 30 days.", "Active licences / purchased licences x 100", "Licence portal, identity platform", "85% or more", "%", "Higher", "Applications Lead", "Quarterly"),
    ("CO-06", "Cost", "Contracts reviewed before notice date", "Share of contracts reaching their notice date in the period that had a documented renewal decision beforehand.", "Contracts with decision recorded before notice date / contracts reaching notice date x 100", "Contract register", "100%", "%", "Higher", "IT Manager", "Monthly"),
    # ---- People
    ("PE-01", "People", "IT staff turnover", "Leavers over the last 12 months as a share of average headcount.", "Leavers in last 12 months / average headcount x 100", "HR system", "Track trend; set locally", "%", "Lower", "IT Manager", "Quarterly"),
    ("PE-02", "People", "Time to fill vacancies", "Average working days from approval of a vacancy to the accepted offer.", "Sum of days to accepted offer / number of roles filled", "HR system", "Set locally", "days", "Lower", "IT Manager", "Quarterly"),
    ("PE-03", "People", "Mandatory training completion", "Share of IT staff who completed required training by the due date.", "Staff completed / staff assigned x 100", "Learning platform", "100%", "%", "Higher", "IT Manager", "Quarterly"),
    ("PE-04", "People", "Team engagement score", "Average score from a short pulse survey of the IT team.", "Sum of responses / number of responses", "Pulse survey", "Track trend", "score (1 to 5)", "Higher", "IT Manager", "Quarterly"),
    ("PE-05", "People", "Critical systems with a named deputy", "Share of critical systems with a named primary and a trained deputy, reducing key-person risk.", "Critical systems with primary and deputy / critical systems x 100", "Service catalogue", "100%", "%", "Higher", "IT Manager", "Quarterly"),
    ("PE-06", "People", "Skills coverage against plan", "Share of skills in the team skills matrix where the planned minimum number of competent people is met.", "Skills meeting minimum cover / skills in matrix x 100", "Skills matrix", "90% or more", "%", "Higher", "IT Manager", "Half-yearly"),
]

DOMAIN_ORDER = ["Service desk", "Availability", "Security", "Projects", "Cost", "People"]
DOMAIN_NOTES = {
    "Service desk": "How quickly and how well users get help.",
    "Availability": "Whether services stay up, and whether change is safe.",
    "Security": "Whether the controls that reduce the likelihood and impact of an attack are working.",
    "Projects": "Whether change is delivered on time, on budget and with the promised benefit.",
    "Cost": "Whether money is controlled and well spent.",
    "People": "Whether the team has the capacity, skills and resilience to deliver.",
}


def write_kpi_csv() -> Path:
    path = ROOT / "03-kpi-pack" / "kpi-catalogue.csv"
    with open(path, "w", newline="", encoding="utf-8") as handle:
        w = csv.writer(handle, lineterminator="\n")
        w.writerow(KPI_COLUMNS)
        w.writerows(KPIS)
    return path


def md_cell(text: str) -> str:
    return text.replace("|", "/")


def write_kpi_md() -> Path:
    lines = [
        "# KPI catalogue",
        "",
        "Thirty-six measures across six domains, each with a definition, formula, data source, example target, owner and reporting cadence. "
        "The same content is in [kpi-catalogue.csv](kpi-catalogue.csv) so it can be loaded into a spreadsheet or reporting tool.",
        "",
        "**Targets are examples only.** They show the form a target takes. Replace them with targets that reflect your own service levels, contracts and risk appetite. No external benchmark is implied.",
        "",
        f"This file is generated from `tools/build_csvs.py`. Edit the source and rebuild rather than editing the tables by hand.",
        "",
    ]
    for domain in DOMAIN_ORDER:
        rows = [k for k in KPIS if k[1].startswith(domain)]
        lines += [f"## {domain}", "", DOMAIN_NOTES[domain], "", "| ID | KPI | Definition | Formula | Data source | Target (example) | Better when | Owner | Cadence |", "|---|---|---|---|---|---|---|---|---|"]
        for k in rows:
            kid, _d, name, definition, formula, source, target, unit, better, owner, cadence = k
            lines.append(
                f"| {kid} | {md_cell(name)} | {md_cell(definition)} | {md_cell(formula)} | {md_cell(source)} | {md_cell(target)} ({unit}) | {better} | {owner} | {cadence} |"
            )
        lines.append("")
    path = ROOT / "03-kpi-pack" / "kpi-catalogue.md"
    # Guidance is kept in README.md; the catalogue file stays a pure reference.
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


RISK_COLUMNS = ["id", "date_raised", "title", "category", "description", "likelihood", "impact", "score", "rating", "owner", "mitigation", "status", "next_review", "trend"]
RAISED = {
    "R-001": "2026-04-20", "R-002": "2026-04-20", "R-003": "2026-04-20", "R-004": "2026-05-18", "R-005": "2026-08-10",
    "R-006": "2026-05-18", "R-007": "2026-07-06", "R-008": "2026-06-15", "R-009": "2026-06-15", "R-010": "2026-04-20",
}


def write_risk_files() -> list[Path]:
    out = ROOT / "08-risk-register"
    out.mkdir(exist_ok=True)
    rows = ex.top_risks(len(ex.RISKS))
    rows_by_id = sorted(rows, key=lambda r: r["id"])
    example = out / "risk-register-example.csv"
    with open(example, "w", newline="", encoding="utf-8") as handle:
        w = csv.writer(handle, lineterminator="\n")
        w.writerow(RISK_COLUMNS)
        for r in rows_by_id:
            w.writerow([r["id"], RAISED[r["id"]], r["title"], r["category"], r["description"], r["likelihood"], r["impact"], r["score"], r["rating"], r["owner"], r["mitigation"], r["status"], r["next_review"], r["trend"]])
    template = out / "risk-register-template.csv"
    with open(template, "w", newline="", encoding="utf-8") as handle:
        w = csv.writer(handle, lineterminator="\n")
        w.writerow(RISK_COLUMNS)
        w.writerow(["R-000", "YYYY-MM-DD", "Short title (delete this guidance row)", "Security / Financial / Operational / People / Project / Commercial / Compliance / Technology", "Because of [cause], [event] may happen, leading to [impact].", 3, 3, "=likelihood x impact (9)", "Low / Medium / High / Critical", "Named role or person", "Actions that reduce likelihood or impact, with dates", "Open / Mitigating / Accepted / Closed", "YYYY-MM-DD", "Rising / Stable / Falling"])

    md = [
        "# Risk register: worked example",
        "",
        f"A fictional register for {ex.COMPANY}. The IDs and scores match the top risks shown in the [example board report](../02-board-it-report/example-northwind-board-report.md). Data file: [risk-register-example.csv](risk-register-example.csv).",
        "",
        "Scoring bands used here are examples: " + ", ".join(f"{lo} to {hi} {label}" for lo, hi, label in ex.RISK_BANDS) + ".",
        "",
        "| ID | Risk | Category | L | I | Score | Rating | Owner | Status | Next review | Trend |",
        "|---|---|---|---:|---:|---:|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (-r["score"], r["id"])):
        md.append(f"| {r['id']} | {r['title']} | {r['category']} | {r['likelihood']} | {r['impact']} | {r['score']} | {r['rating']} | {r['owner']} | {r['status']} | {r['next_review']} | {r['trend']} |")
    md += ["", "## Mitigation actions", ""]
    for r in sorted(rows, key=lambda r: (-r["score"], r["id"])):
        md.append(f"- **{r['id']} {r['title']}.** {r['description']} *Mitigation:* {r['mitigation']}")
    md.append("")
    md_path = out / "risk-register-example.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    return [example, template, md_path]


if __name__ == "__main__":
    print("wrote", write_kpi_csv())
    print("wrote", write_kpi_md())
    for p in write_risk_files():
        print("wrote", p)
