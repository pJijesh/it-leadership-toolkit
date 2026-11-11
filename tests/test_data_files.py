import csv
import re

import example_data as ex


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_kpi_catalogue(root):
    rows = read_csv(root / "03-kpi-pack" / "kpi-catalogue.csv")
    assert len(rows) == 36
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert {r["domain"] for r in rows} == {"Service desk", "Availability", "Security", "Projects", "Cost", "People"}
    required = ["id", "domain", "name", "definition", "formula", "data_source", "target_example", "owner", "cadence"]
    for r in rows:
        for col in required:
            assert r[col].strip(), f"{r['id']} is missing {col}"
        assert r["cadence"] in {"Monthly", "Quarterly", "Half-yearly"}
    md = (root / "03-kpi-pack" / "kpi-catalogue.md").read_text(encoding="utf-8")
    for kid in ids:
        assert f"| {kid} |" in md
    assert "example" in md.lower()


def test_risk_register_example(root):
    rows = read_csv(root / "08-risk-register" / "risk-register-example.csv")
    assert len(rows) == len(ex.RISKS)
    for r in rows:
        score = int(r["likelihood"]) * int(r["impact"])
        assert int(r["score"]) == score
        assert r["rating"] == ex.risk_rating(score)
        assert 1 <= int(r["likelihood"]) <= 5 and 1 <= int(r["impact"]) <= 5
        assert r["owner"].strip() and r["mitigation"].strip() and r["next_review"].strip()


def test_risk_template_has_same_columns(root):
    template = read_csv(root / "08-risk-register" / "risk-register-template.csv")
    example = read_csv(root / "08-risk-register" / "risk-register-example.csv")
    assert list(template[0].keys()) == list(example[0].keys())


def test_board_report_matches_example_data(root):
    s = ex.budget_summary()
    md = (root / "02-board-it-report" / "example-northwind-board-report.md").read_text(encoding="utf-8")
    html = (root / "02-board-it-report" / "example-northwind-board-report.html").read_text(encoding="utf-8")
    for text in (md, html):
        assert f"£{s['ytd_actual']:,}" in text
        assert f"£{s['fy_outturn']:,}" in text
        assert f"£{s['fy_budget']:,}" in text
        assert "fictional" in text
    top = ex.top_risks(4)
    for r in top:
        assert r["id"] in md and r["title"] in md


def test_decision_memo_names_top_scored_vendor(root):
    weights = [w for _c, w in ex.VENDOR_CRITERIA]
    totals = {
        v: sum(weights[i] * ex.VENDOR_SCORES[i][j] for i in range(len(weights))) / sum(weights)
        for j, v in enumerate(ex.VENDORS)
    }
    best = max(totals, key=totals.get)
    memo = (root / "07-technology-decision-memo" / "example-northwind.md").read_text(encoding="utf-8")
    assert f"Vendor B" in memo and best == "Vendor B"
    assert f"{totals[best]:.2f}" in memo


def test_board_pdf_is_single_page(root):
    pdf = (root / "docs" / "board-report-example.pdf").read_bytes()
    assert len(re.findall(rb"/Type\s*/Page[^s]", pdf)) == 1
