"""Single source of truth for the fictional Northwind Freight (fictional) examples.

Every figure here is invented for illustration. Nothing is drawn from a real
organisation. The vendor scorecard, budget tracker and board report examples are
all generated from this module so that they stay consistent with one another.
"""

from __future__ import annotations

from datetime import date

COMPANY = "Northwind Freight (fictional)"

# ---------------------------------------------------------------------------
# Vendor scorecard example: re-tender of a managed service desk (fictional)
# ---------------------------------------------------------------------------

SCORE_MIN = 0
SCORE_MAX = 5

# (criterion, weight in percent). Weights must sum to 100.
VENDOR_CRITERIA = [
    ("Service quality and SLA commitments", 25),
    ("Total cost over three years", 20),
    ("Security and compliance", 15),
    ("Integration with our platforms", 10),
    ("Transition and implementation risk", 10),
    ("References and track record", 10),
    ("Commercial flexibility", 5),
    ("Account management", 5),
]

VENDORS = ["Vendor A", "Vendor B", "Vendor C", "Vendor D"]

# Scores are on a 0 to 5 scale, one list per criterion, in VENDORS order.
VENDOR_SCORES = [
    [4, 5, 3, 4],  # Service quality and SLA commitments
    [3, 4, 5, 2],  # Total cost over three years
    [4, 4, 3, 5],  # Security and compliance
    [3, 5, 2, 4],  # Integration with our platforms
    [3, 4, 4, 2],  # Transition and implementation risk
    [4, 4, 3, 4],  # References and track record
    [3, 3, 5, 2],  # Commercial flexibility
    [4, 4, 3, 4],  # Account management
]

MAX_VENDOR_COLUMNS = 6  # the workbook has room for six vendors

# ---------------------------------------------------------------------------
# Budget tracker example
# ---------------------------------------------------------------------------

FY_LABEL = "FY2026/27"
FY_START = date(2026, 4, 1)
REPORTING_MONTH = date(2026, 9, 1)  # last month with actuals
AMBER_THRESHOLD = 0.05  # example: variance above 5 percent is Amber
RED_THRESHOLD = 0.10  # example: variance above 10 percent is Red

COST_CENTRES = [
    ("IC", "Infrastructure and Cloud"),
    ("AL", "Applications and Licences"),
    ("SD", "Service Desk and End-User"),
    ("SC", "Security and Compliance"),
    ("PC", "Projects and Change"),
]


def fy_months() -> list[date]:
    months = []
    for i in range(12):
        m = 4 + i
        y = 2026 + (m - 1) // 12
        m = (m - 1) % 12 + 1
        months.append(date(y, m, 1))
    return months


# line id: (cost centre code, description, type, {month index: budget GBP})
# Month index 0 = April.
def _flat(total: int) -> dict[int, int]:
    return {i: total // 12 for i in range(12)}


BUDGET_LINES = {
    "IC01": ("IC", "Cloud hosting", "OpEx", _flat(216000)),
    "IC02": ("IC", "Network and connectivity", "OpEx", _flat(96000)),
    "IC03": ("IC", "Server and network hardware refresh", "CapEx", {2: 24000, 5: 30000, 9: 30000}),
    "AL01": ("AL", "Core operations platform subscription", "OpEx", _flat(288000)),
    "AL02": ("AL", "Productivity and collaboration licences", "OpEx", _flat(60000)),
    "AL03": ("AL", "Application development and integration", "CapEx", _flat(120000)),
    "SD01": ("SD", "Managed service desk contract", "OpEx", _flat(108000)),
    "SD02": ("SD", "End-user device replacement", "CapEx", {0: 12000, 2: 12000, 4: 12000, 6: 12000, 8: 12000, 10: 12000}),
    "SC01": ("SC", "Security tooling and monitoring", "OpEx", _flat(84000)),
    "SC02": ("SC", "Penetration testing and audit", "OpEx", {2: 15000, 8: 15000}),
    "PC01": ("PC", "Warehouse scanning rollout", "CapEx", {i: 16000 for i in range(2, 8)}),
    "PC02": ("PC", "Data platform pilot", "CapEx", {i: 10000 for i in range(5, 11)}),
}

# Actuals for April to September, as a multiplier on budget, per line.
# Where a line needs exact amounts, ACTUAL_OVERRIDE wins.
ACTUAL_MULT = {
    "IC01": [1.03, 1.06, 1.09, 1.11, 1.13, 1.15],
    "IC02": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    "IC03": [1.0, 1.0, 1.075, 1.0, 1.0, 0.9633],
    "AL01": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    "AL02": [1.00, 1.00, 1.00, 1.02, 1.02, 1.02],
    "AL03": [0.95, 0.95, 1.00, 1.00, 1.05, 1.05],
    "SD01": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    "SD02": [1.00, 1.0, 0.98, 1.0, 1.02, 1.0],
    "SC01": [1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    "SC02": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "PC01": [1.0, 1.0, 0.5, 0.75, 1.0, 1.0],
    "PC02": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
}

# Forecast for October to March as a multiplier on budget, per line.
FORECAST_MULT = {
    "IC01": 1.15,
    "IC02": 1.00,
    "IC03": 1.00,
    "AL01": 1.00,
    "AL02": 1.02,
    "AL03": 1.03,
    "SD01": 1.00,
    "SD02": 1.00,
    "SC01": 1.00,
    "SC02": 1.00,
    "PC01": 1.00,
    "PC02": 1.00,
}

# Exact forecast overrides: (line, month index) -> GBP. PC01 slipped by one month.
FORECAST_OVERRIDE = {("PC01", 8): 12000}


def budget_rows() -> list[dict]:
    """Return the long-format Data rows used by the workbook and the report."""
    months = fy_months()
    reporting_index = months.index(REPORTING_MONTH)
    rows = []
    for line_id, (cc, desc, typ, profile) in BUDGET_LINES.items():
        for i, month in enumerate(months):
            budget = profile.get(i, 0)
            actual = None
            forecast = None
            if i <= reporting_index:
                actual = round(budget * ACTUAL_MULT[line_id][i])
            else:
                key = (line_id, i)
                if key in FORECAST_OVERRIDE:
                    forecast = FORECAST_OVERRIDE[key]
                else:
                    forecast = round(budget * FORECAST_MULT[line_id])
            rows.append(
                {
                    "month": month,
                    "cost_centre": cc,
                    "line_id": line_id,
                    "description": desc,
                    "type": typ,
                    "budget": budget,
                    "actual": actual,
                    "forecast": forecast,
                }
            )
    return rows


def budget_summary() -> dict:
    """Totals used by the board report example (and cross-checked in tests)."""
    rows = budget_rows()
    ri = fy_months().index(REPORTING_MONTH)
    months = fy_months()
    ytd_budget = sum(r["budget"] for r in rows if months.index(r["month"]) <= ri)
    ytd_actual = sum(r["actual"] for r in rows if r["actual"] is not None)
    fy_budget = sum(r["budget"] for r in rows)
    fy_outturn = sum(r["actual"] if r["actual"] is not None else r["forecast"] for r in rows)
    capex_outturn = sum(
        (r["actual"] if r["actual"] is not None else r["forecast"]) for r in rows if r["type"] == "CapEx"
    )
    opex_outturn = fy_outturn - capex_outturn
    by_cc = {}
    for code, name in COST_CENTRES:
        sub = [r for r in rows if r["cost_centre"] == code]
        by_cc[code] = {
            "name": name,
            "fy_budget": sum(r["budget"] for r in sub),
            "ytd_budget": sum(r["budget"] for r in sub if months.index(r["month"]) <= ri),
            "ytd_actual": sum(r["actual"] for r in sub if r["actual"] is not None),
            "outturn": sum((r["actual"] if r["actual"] is not None else r["forecast"]) for r in sub),
        }
    return {
        "ytd_budget": ytd_budget,
        "ytd_actual": ytd_actual,
        "fy_budget": fy_budget,
        "fy_outturn": fy_outturn,
        "capex_outturn": capex_outturn,
        "opex_outturn": opex_outturn,
        "by_cost_centre": by_cc,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(budget_summary(), indent=2))


# ---------------------------------------------------------------------------
# Risk register example (fictional)
# ---------------------------------------------------------------------------

# Example scoring bands (label them as examples wherever they are shown).
RISK_BANDS = [(1, 4, "Low"), (5, 9, "Medium"), (10, 14, "High"), (15, 25, "Critical")]


def risk_rating(score: int) -> str:
    for low, high, label in RISK_BANDS:
        if low <= score <= high:
            return label
    raise ValueError(f"score out of range: {score}")


# id, title, category, description, likelihood, impact, owner, mitigation, status, next review, trend
RISKS = [
    ("R-001", "Cloud hosting cost grows faster than forecast", "Financial",
     "Usage growth in the core platform raises monthly hosting cost above budget, leading to a full-year overspend.",
     4, 3, "IT Manager",
     "Complete the cost optimisation review; set budget alerts; evaluate reserved capacity; report monthly variance.",
     "Open", "2026-11-15", "Rising"),
    ("R-002", "Ransomware entering through a phishing email", "Security",
     "A user opens a malicious email, malware spreads and operations stop, causing loss of service and data and a possible regulatory notification.",
     3, 5, "Security Lead",
     "Extend multi-factor authentication to 100 percent of accounts; email filtering; immutable backups; quarterly phishing exercises; tested incident plan.",
     "Open", "2026-10-31", "Stable"),
    ("R-003", "Core operations platform outage in a peak period", "Operational",
     "A failure or failed change takes the platform offline during a busy period, delaying shipments and customer service.",
     2, 5, "Applications Lead",
     "Change freeze in peak weeks; tested rollback plans; supplier escalation route; annual disaster recovery test.",
     "Open", "2026-11-30", "Stable"),
    ("R-004", "Key-person dependency for integration knowledge", "People",
     "Two people hold most knowledge of system integrations. Absence or departure would slow fixes and projects.",
     3, 4, "IT Manager",
     "Document integrations; pair a second engineer on each; add a retained support partner option.",
     "Open", "2026-12-15", "Stable"),
    ("R-005", "Supplier delays warehouse scanner delivery again", "Project",
     "A second hardware delay would push the rollout beyond December and into the peak period.",
     3, 2, "Project Manager",
     "Weekly supplier call; agreed delivery date in writing; fallback of phased site go-live.",
     "Open", "2026-10-31", "Falling"),
    ("R-006", "Unsupported operating systems on legacy devices", "Technology",
     "Devices that no longer receive vendor security updates remain in use and become an entry point for attack.",
     3, 3, "Service Desk Lead",
     "Asset review; replace through the device refresh budget; isolate any exception on a restricted network.",
     "Open", "2026-12-01", "Falling"),
    ("R-007", "Service desk contract ends before replacement is live", "Commercial",
     "Re-tender and transition take longer than planned, leaving a gap in service or forcing a poor-value extension.",
     2, 4, "IT Manager",
     "Agree a short extension option in writing; start transition planning before contract award.",
     "Open", "2026-11-15", "Stable"),
    ("R-008", "Personal data shared through misconfigured access", "Compliance",
     "A sharing setting exposes files containing personal data to people who should not see them.",
     2, 4, "Security Lead",
     "Quarterly access review; default-private sharing policy; data loss prevention alerts.",
     "Open", "2026-12-15", "Stable"),
    ("R-009", "Backup restore not tested within the last 12 months", "Resilience",
     "Backups exist but a full restore has not been proven, so recovery time after a major failure is uncertain.",
     3, 4, "Infrastructure Lead",
     "Schedule a restore test in the next disaster recovery exercise; record the measured recovery time.",
     "Open", "2026-11-15", "Stable"),
    ("R-010", "Single-source scanning software supplier fails", "Commercial",
     "The supplier of the scanning application becomes insolvent or withdraws the product.",
     1, 4, "Applications Lead",
     "Escrow or code access arrangement; annual supplier financial check; documented exit plan.",
     "Accepted", "2027-03-31", "Stable"),
]


def top_risks(n: int = 4) -> list[dict]:
    keys = ["id", "title", "category", "description", "likelihood", "impact", "owner", "mitigation", "status", "next_review", "trend"]
    rows = [dict(zip(keys, r)) for r in RISKS]
    for r in rows:
        r["score"] = r["likelihood"] * r["impact"]
        r["rating"] = risk_rating(r["score"])
    return sorted(rows, key=lambda r: (-r["score"], r["id"]))[:n]
