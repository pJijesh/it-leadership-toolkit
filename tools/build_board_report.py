"""Build the one-page board IT report example (Markdown, HTML and PDF) from example data.

Run from the repository root:  python tools/build_board_report.py
The figures for spend come from example_data.py, the same source as the budget
tracker workbook, so the two always agree.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import example_data as ex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02-board-it-report"
DOCS = ROOT / "docs"

PERIOD = "September 2026"


def gbp(value: float) -> str:
    return f"£{value:,.0f}"


def gbp_k(value: float) -> str:
    return f"£{value / 1000:,.0f}k"


def pct(value: float) -> str:
    text = f"{value:+.1%}"
    return "0.0%" if text in ("+0.0%", "-0.0%") else text


def rag_for(var_pct: float) -> str:
    if var_pct > ex.RED_THRESHOLD:
        return "Red"
    if var_pct > ex.AMBER_THRESHOLD:
        return "Amber"
    return "Green"


def vendor_top_two() -> tuple[str, float, float]:
    weights = [w for _c, w in ex.VENDOR_CRITERIA]
    totals = [
        sum(weights[i] * ex.VENDOR_SCORES[i][v] for i in range(len(weights))) / sum(weights)
        for v in range(len(ex.VENDORS))
    ]
    order = sorted(range(len(totals)), key=lambda v: -totals[v])
    return ex.VENDORS[order[0]], totals[order[0]], totals[order[1]]


def cloud_overspend() -> int:
    rows = [r for r in ex.budget_rows() if r["line_id"] == "IC01"]
    return sum(r["actual"] if r["actual"] is not None else r["forecast"] for r in rows) - sum(r["budget"] for r in rows)


def collect() -> dict:
    s = ex.budget_summary()
    cc_rows = []
    for code, info in s["by_cost_centre"].items():
        var = info["outturn"] - info["fy_budget"]
        vp = var / info["fy_budget"] if info["fy_budget"] else 0.0
        cc_rows.append(
            {
                "name": info["name"],
                "fy_budget": info["fy_budget"],
                "ytd_budget": info["ytd_budget"],
                "ytd_actual": info["ytd_actual"],
                "outturn": info["outturn"],
                "var": var,
                "var_pct": vp,
                "rag": rag_for(vp),
            }
        )
    fy_var = s["fy_outturn"] - s["fy_budget"]
    fy_var_pct = fy_var / s["fy_budget"]
    ytd_var = s["ytd_actual"] - s["ytd_budget"]
    ytd_var_pct = ytd_var / s["ytd_budget"]
    return {
        "summary": s,
        "cc_rows": cc_rows,
        "fy_var": fy_var,
        "fy_var_pct": fy_var_pct,
        "ytd_var": ytd_var,
        "ytd_var_pct": ytd_var_pct,
    }


# Narrative content (invented for the fictional company).
HEADLINE = (
    "Services were stable this month and spend is on plan year to date. Cloud hosting is the main pressure on the "
    "full-year forecast, one project has slipped by a month, and two critical vulnerabilities remain open. "
    "Overall status is Amber."
)

SERVICE_TILES = [
    ("Core platform availability", "99.93%", "Target 99.9% (example)", "Green"),
    ("Priority 1 incidents", "1", "Target 2 or fewer (example)", "Green"),
    ("Tickets resolved within SLA", "94%", "Target 95% (example)", "Amber"),
    ("User satisfaction (CSAT)", "4.4 / 5", "Target 4.3 (example)", "Green"),
]

PROJECTS = [
    ("Warehouse scanning rollout", "Amber", "£96,000", "Hardware delivery arrived a month late. Go-live moves from November to December. Budget unchanged.", "Go-live, Dec 2026"),
    ("Data platform pilot", "Green", "£60,000", "Pilot environment built and first data sets loaded. Spend on plan.", "Pilot review, Jan 2027"),
    ("Cloud cost optimisation review", "Green", "Within run cost", "Usage analysis under way. Findings and options due in October.", "Findings, Oct 2026"),
    ("Annual disaster recovery test", "Green", "Within run cost", "Test plan agreed with the business. Includes a measured restore test.", "Test, Nov 2026"),
]

SECURITY = [
    ("Accounts protected by multi-factor authentication", "96%", "Target 100% (example)", "Amber"),
    ("Critical patches applied within 14 days", "91%", "Target 95% (example)", "Amber"),
    ("Open critical vulnerabilities", "2", "Target 0 (example)", "Amber"),
    ("Phishing exercise click rate", "4.1%", "Target under 5% (example)", "Green"),
    ("Major security incidents", "0", "Target 0 (example)", "Green"),
]

PROGRESS_NOTE = "All figures in this example are invented for a fictional company."


def decisions(c: dict) -> list[tuple[str, str]]:
    return [
        (
            "Note the forecast overspend and agree the response",
            f"Full-year outturn is {gbp(c['summary']['fy_outturn'])} against a budget of {gbp(c['summary']['fy_budget'])} "
            f"({pct(c['fy_var_pct'])}), driven by cloud hosting. Agree that IT completes the optimisation review and returns with options in November before any budget change is requested.",
        ),
        (
            "Approve the preferred managed service desk supplier",
            f"{vendor_top_two()[0]} ranked first on the weighted scorecard ({vendor_top_two()[1]:.2f} out of 5; next best {vendor_top_two()[2]:.2f}). Approve moving to contract and security review. The decision memo is attached.",
        ),
        (
            "Agree the new warehouse scanning go-live date",
            "Approve a December 2026 go-live outside the peak trading weeks, with a phased site rollout as the fallback.",
        ),
    ]


# ------------------------------------------------------------------ Markdown

def render_markdown(c: dict) -> str:
    s = c["summary"]
    lines: list[str] = []
    a = lines.append
    a(f"# IT board report: {PERIOD}")
    a("")
    a(f"**{ex.COMPANY}** | Prepared by the IT Manager | Financial year {ex.FY_LABEL}, month 6 | Overall status: **AMBER**")
    a("")
    a(f"> {PROGRESS_NOTE} Targets shown are examples, not benchmarks.")
    a("")
    a("## 1. Headline")
    a("")
    a(HEADLINE)
    a("")
    a("## 2. Service performance")
    a("")
    a("| Measure | Result | Target | Status |")
    a("|---|---|---|---|")
    for name, value, target, rag in SERVICE_TILES:
        a(f"| {name} | {value} | {target.replace('Target ', '')} | {rag} |")
    a("")
    a("## 3. Spend against budget")
    a("")
    a(
        f"Year to date: {gbp(s['ytd_actual'])} against a budget of {gbp(s['ytd_budget'])} ({pct(c['ytd_var_pct'])}). "
        f"Full-year outturn (actuals plus forecast): {gbp(s['fy_outturn'])} against {gbp(s['fy_budget'])} ({pct(c['fy_var_pct'])}). "
        f"Outturn split: CapEx {gbp(s['capex_outturn'])}, OpEx {gbp(s['opex_outturn'])}."
    )
    a("")
    a("| Cost centre | Full-year budget | YTD budget | YTD actual | Full-year outturn | Variance | Status |")
    a("|---|---:|---:|---:|---:|---:|---|")
    for r in c["cc_rows"]:
        a(f"| {r['name']} | {gbp(r['fy_budget'])} | {gbp(r['ytd_budget'])} | {gbp(r['ytd_actual'])} | {gbp(r['outturn'])} | {pct(r['var_pct'])} | {r['rag']} |")
    a(
        f"| **Total** | **{gbp(s['fy_budget'])}** | **{gbp(s['ytd_budget'])}** | **{gbp(s['ytd_actual'])}** | **{gbp(s['fy_outturn'])}** | **{pct(c['fy_var_pct'])}** | **{rag_for(c['fy_var_pct'])}** |"
    )
    a("")
    a(
        f"Variance is full-year outturn against budget; positive is an overspend. Amber above {ex.AMBER_THRESHOLD:.0%} and red above {ex.RED_THRESHOLD:.0%} (example thresholds). "
        f"Cloud hosting alone is forecast to be {gbp(cloud_overspend())} (about 12 percent) over its line budget. Warehouse scanning spend is behind plan year to date because of the delivery delay, and is forecast to catch up by December."
    )
    a("")
    a("## 4. Major projects")
    a("")
    a("| Project | Status | Budget | Update | Next milestone |")
    a("|---|---|---|---|---|")
    for name, rag, budget, note, ms in PROJECTS:
        a(f"| {name} | {rag} | {budget} | {note} | {ms} |")
    a("")
    a("## 5. Top risks")
    a("")
    a("| ID | Risk | Score | Rating | Owner | Trend |")
    a("|---|---|---:|---|---|---|")
    for r in ex.top_risks(4):
        a(f"| {r['id']} | {r['title']} | {r['score']} | {r['rating']} | {r['owner']} | {r['trend']} |")
    a("")
    a("Score is likelihood (1 to 5) times impact (1 to 5). Full register: [risk register example](../08-risk-register/risk-register-example.md).")
    a("")
    a("## 6. Security posture")
    a("")
    a("| Measure | Result | Target | Status |")
    a("|---|---|---|---|")
    for name, value, target, rag in SECURITY:
        a(f"| {name} | {value} | {target.replace('Target ', '')} | {rag} |")
    a("")
    a("## 7. Decisions requested")
    a("")
    for i, (title, text) in enumerate(decisions(c), start=1):
        a(f"{i}. **{title}.** {text}")
    a("")
    return "\n".join(lines)


# ------------------------------------------------------------------ HTML

CSS = """
:root { --navy:#1f3a5f; --ink:#1d2733; --muted:#5b6674; --line:#d5dae1; --band:#f3f5f8;
        --green:#2e7d32; --amber:#c77700; --red:#c62828; --greenbg:#e6f2e7; --amberbg:#fdf0d9; --redbg:#fbe4e4; }
* { box-sizing:border-box; }
@page { size: A4; margin: 0; }
html, body { margin:0; padding:0; background:#fff; }
body { font-family: "Liberation Sans", Arial, Helvetica, sans-serif; color:var(--ink); font-size:8.6pt; line-height:1.3; }
.page { width:210mm; height:297mm; padding:10mm 11mm 8mm 11mm; position:relative; overflow:hidden; }
header { background:var(--navy); color:#fff; padding:9px 14px; border-radius:4px; display:flex; justify-content:space-between; align-items:center; }
header h1 { font-size:15pt; margin:0; letter-spacing:.2px; }
header .sub { font-size:8.4pt; opacity:.9; margin-top:2px; }
.status { text-align:center; background:#fff; color:var(--amber); border-radius:4px; padding:4px 12px; font-weight:700; font-size:9pt; }
.status small { display:block; color:var(--muted); font-weight:400; font-size:7pt; }
.note { color:var(--muted); font-size:7.4pt; margin:4px 0 0 0; }
h2 { font-size:9.6pt; color:var(--navy); margin:8px 0 3px 0; padding-bottom:2px; border-bottom:1.5px solid var(--navy); text-transform:none; }
p { margin:2px 0; }
.tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; margin-top:6px; }
.tile { background:var(--band); border-left:4px solid var(--line); padding:4px 7px; border-radius:3px; }
.tile .v { font-size:12.5pt; font-weight:700; }
.tile .l { font-size:7.6pt; color:var(--ink); }
.tile .t { font-size:6.8pt; color:var(--muted); }
.Green { border-left-color:var(--green); } .Amber { border-left-color:var(--amber); } .Red { border-left-color:var(--red); }
table { width:100%; border-collapse:collapse; margin-top:3px; }
th { background:var(--band); text-align:left; font-size:7.4pt; color:var(--muted); font-weight:700; padding:2.5px 5px; border-bottom:1px solid var(--line); }
td { padding:2.5px 5px; border-bottom:1px solid var(--line); vertical-align:top; font-size:8pt; }
td.n, th.n { text-align:right; white-space:nowrap; }
tr.total td { font-weight:700; background:var(--band); }
.pill { display:inline-block; min-width:42px; text-align:center; padding:0 6px; border-radius:9px; font-weight:700; font-size:7.4pt; }
.pill.Green { background:var(--greenbg); color:var(--green); } .pill.Amber { background:var(--amberbg); color:var(--amber); } .pill.Red { background:var(--redbg); color:var(--red); }
.two { display:grid; grid-template-columns: 1.08fr 1fr; gap:10px; }
.bars { margin-top:4px; }
.bar-row { display:grid; grid-template-columns:104px 1fr 62px; gap:6px; align-items:center; margin:2px 0; font-size:7.6pt; }
.bar-track { position:relative; height:9px; background:var(--band); border-radius:2px; }
.bar-budget { position:absolute; left:0; top:0; height:9px; background:#b8c4d4; border-radius:2px; }
.bar-out { position:absolute; left:0; top:3px; height:3px; background:var(--navy); }
.legend { font-size:6.8pt; color:var(--muted); margin-top:2px; }
.sw { display:inline-block; width:9px; height:6px; margin-right:3px; vertical-align:middle; }
ol.dec { margin:3px 0 0 0; padding-left:15px; }
ol.dec li { margin-bottom:3px; }
footer { position:absolute; bottom:6mm; left:11mm; right:11mm; font-size:6.8pt; color:var(--muted); border-top:1px solid var(--line); padding-top:3px; display:flex; justify-content:space-between; }
"""


def pill(rag: str) -> str:
    return f'<span class="pill {rag}">{rag}</span>'


def tile(name: str, value: str, target: str, rag: str) -> str:
    return (
        f'<div class="tile {rag}"><div class="v">{html.escape(value)}</div>'
        f'<div class="l">{html.escape(name)}</div><div class="t">{html.escape(target)}</div></div>'
    )


def render_html(c: dict) -> str:
    s = c["summary"]
    max_val = max(max(r["fy_budget"], r["outturn"]) for r in c["cc_rows"])
    bars = []
    for r in c["cc_rows"]:
        bw = r["fy_budget"] / max_val * 100
        ow = r["outturn"] / max_val * 100
        bars.append(
            f'<div class="bar-row"><div>{html.escape(r["name"])}</div>'
            f'<div class="bar-track"><div class="bar-budget" style="width:{bw:.1f}%"></div><div class="bar-out" style="width:{ow:.1f}%"></div></div>'
            f'<div style="text-align:right">{pill(r["rag"])}</div></div>'
        )
    cc_table = "".join(
        f'<tr><td>{html.escape(r["name"])}</td><td class="n">{gbp_k(r["fy_budget"])}</td><td class="n">{gbp_k(r["ytd_actual"])}</td>'
        f'<td class="n">{gbp_k(r["outturn"])}</td><td class="n">{pct(r["var_pct"])}</td></tr>'
        for r in c["cc_rows"]
    )
    total_row = (
        f'<tr class="total"><td>Total</td><td class="n">{gbp_k(s["fy_budget"])}</td><td class="n">{gbp_k(s["ytd_actual"])}</td>'
        f'<td class="n">{gbp_k(s["fy_outturn"])}</td><td class="n">{pct(c["fy_var_pct"])}</td></tr>'
    )
    proj_rows = "".join(
        f"<tr><td><b>{html.escape(n)}</b></td><td>{pill(r)}</td><td class='n'>{html.escape(b)}</td><td>{html.escape(note)}</td><td>{html.escape(ms)}</td></tr>"
        for n, r, b, note, ms in PROJECTS
    )
    # Show the rating word in the pill, coloured by severity.
    risk_rows = ""
    colour = {"Critical": "Red", "High": "Amber", "Medium": "Green", "Low": "Green"}
    for r in ex.top_risks(4):
        risk_rows += (
            f"<tr><td style='white-space:nowrap'>{r['id']}</td><td>{html.escape(r['title'])}</td><td class='n'>{r['score']}</td>"
            f"<td><span class='pill {colour[r['rating']]}'>{r['rating']}</span></td></tr>"
        )
    sec_rows = "".join(
        f"<tr><td>{html.escape(n)}</td><td class='n'><b>{html.escape(v)}</b></td><td class='n' style='color:var(--muted)'>{html.escape(t.replace('Target ', ''))}</td><td>{pill(r)}</td></tr>"
        for n, v, t, r in SECURITY
    )
    dec = "".join(f"<li><b>{html.escape(t)}.</b> {html.escape(x)}</li>" for t, x in decisions(c))
    service_tiles = "".join(tile(*t) for t in SERVICE_TILES)

    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><title>IT board report, {PERIOD} (fictional example)</title>
<style>{CSS}</style></head>
<body><div class="page">
<header>
  <div><h1>IT board report: {PERIOD}</h1>
  <div class="sub">{html.escape(ex.COMPANY)} &nbsp;|&nbsp; Prepared by the IT Manager &nbsp;|&nbsp; {ex.FY_LABEL}, month 6</div></div>
  <div class="status">AMBER<small>Overall status</small></div>
</header>
<p class="note">{PROGRESS_NOTE} Targets shown are examples, not benchmarks.</p>

<h2>1. Headline</h2>
<p>{html.escape(HEADLINE)}</p>

<h2>2. Service performance</h2>
<div class="tiles">{service_tiles}</div>

<h2>3. Spend against budget</h2>
<p>Year to date <b>{gbp(s['ytd_actual'])}</b> against <b>{gbp(s['ytd_budget'])}</b> budget ({pct(c['ytd_var_pct'])}). Full-year outturn <b>{gbp(s['fy_outturn'])}</b> against <b>{gbp(s['fy_budget'])}</b> ({pct(c['fy_var_pct'])}). Outturn split: CapEx {gbp(s['capex_outturn'])}, OpEx {gbp(s['opex_outturn'])}.</p>
<div class="two">
<div><table><tr><th>Cost centre</th><th class="n">FY budget</th><th class="n">YTD actual</th><th class="n">FY outturn</th><th class="n">Variance</th></tr>{cc_table}{total_row}</table></div>
<div><div class="bars">{''.join(bars)}</div>
<div class="legend"><span class="sw" style="background:#b8c4d4"></span>Budget &nbsp; <span class="sw" style="background:var(--navy)"></span>Outturn &nbsp; Status: amber above {ex.AMBER_THRESHOLD:.0%}, red above {ex.RED_THRESHOLD:.0%} (example)</div></div>
</div>
<p class="note">Positive variance is an overspend. Cloud hosting alone is forecast {gbp(cloud_overspend())} (about 12 percent) over its line budget. Scanning spend is behind plan year to date because of the delivery delay and is forecast to catch up by December.</p>

<h2>4. Major projects</h2>
<table><tr><th>Project</th><th>Status</th><th class="n">Budget</th><th>Update</th><th>Next milestone</th></tr>{proj_rows}</table>

<div class="two">
<div><h2>5. Top risks</h2>
<table><tr><th>ID</th><th>Risk</th><th class="n">Score</th><th>Rating</th></tr>{risk_rows}</table>
<p class="note">Score = likelihood (1 to 5) x impact (1 to 5).</p></div>
<div><h2>6. Security posture</h2>
<table><tr><th>Measure</th><th class="n">Result</th><th class="n">Target</th><th>Status</th></tr>{sec_rows}</table></div>
</div>

<h2>7. Decisions requested</h2>
<ol class="dec">{dec}</ol>

<footer><span>{html.escape(ex.COMPANY)}: fictional worked example from the IT Leadership Toolkit. Not real data.</span><span>Page 1 of 1</span></footer>
</div></body></html>
"""


def build(render_pdf: bool = True) -> None:
    c = collect()
    OUT.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    (OUT / "example-northwind-board-report.md").write_text(render_markdown(c), encoding="utf-8")
    html_path = OUT / "example-northwind-board-report.html"
    html_path.write_text(render_html(c), encoding="utf-8")
    if render_pdf:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
            page.goto(html_path.resolve().as_uri())
            page.pdf(path=str(DOCS / "board-report-example.pdf"), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            page.screenshot(path=str(DOCS / "board-report-example.png"), full_page=False)
            overflow = page.evaluate("document.querySelector('.page').scrollHeight - document.querySelector('.page').clientHeight")
            browser.close()
        print("overflow px (should be 0 or less):", overflow)


if __name__ == "__main__":
    build()
