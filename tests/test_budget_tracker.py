import openpyxl

import example_data as ex
from conftest import needs_libreoffice


def formula_cells(ws):
    return [c for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("=")]


def test_workbook_contains_formulas(root):
    wb = openpyxl.load_workbook(root / "05-it-budget-tracker" / "it-budget-tracker.xlsx")
    for name in ["By cost centre", "By line", "Monthly", "CapEx vs OpEx"]:
        assert len(formula_cells(wb[name])) >= 30, name
    data = wb["Data"]
    assert len(formula_cells(data)) == 3 * len(ex.budget_rows())
    assert data["I5"].value.startswith("=IF(ISNUMBER(G5)")
    assert "SUMIFS" in wb["By cost centre"]["C5"].value
    assert "ReportingMonth" in wb["By cost centre"]["D5"].value
    assert {"ReportingMonth", "AmberThreshold", "RedThreshold"} <= set(wb.defined_names.keys())


def test_data_rows_match_example_data(root):
    wb = openpyxl.load_workbook(root / "05-it-budget-tracker" / "it-budget-tracker.xlsx")
    data = wb["Data"]
    rows = ex.budget_rows()
    assert data.max_row >= 4 + len(rows)
    for i, row in enumerate(rows):
        r = 5 + i
        assert data.cell(r, 3).value == row["line_id"]
        assert data.cell(r, 6).value == row["budget"]
        assert data.cell(r, 7).value == row["actual"]
        assert data.cell(r, 8).value == row["forecast"]


@needs_libreoffice
def test_recalculated_workbook_has_no_error_values(recalculated):
    wb = openpyxl.load_workbook(recalculated["budget"], data_only=True)
    errors = [(ws.title, c.coordinate, c.value) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("#")]
    assert errors == []


@needs_libreoffice
def test_totals_match_independent_calculation(recalculated):
    s = ex.budget_summary()
    wb = openpyxl.load_workbook(recalculated["budget"], data_only=True)
    cc = wb["By cost centre"]
    total_row = 5 + len(ex.COST_CENTRES)
    assert cc.cell(total_row, 1).value == "Total"
    assert cc.cell(total_row, 3).value == s["fy_budget"]
    assert cc.cell(total_row, 4).value == s["ytd_budget"]
    assert cc.cell(total_row, 5).value == s["ytd_actual"]
    assert cc.cell(total_row, 8).value == s["fy_outturn"]
    for i, code in enumerate(c for c, _ in ex.COST_CENTRES):
        r = 5 + i
        assert cc.cell(r, 1).value == code
        assert cc.cell(r, 3).value == s["by_cost_centre"][code]["fy_budget"]
        assert cc.cell(r, 5).value == s["by_cost_centre"][code]["ytd_actual"]
        assert cc.cell(r, 8).value == s["by_cost_centre"][code]["outturn"]
    cx = wb["CapEx vs OpEx"]
    assert cx["F5"].value == s["capex_outturn"]
    assert cx["F6"].value == s["opex_outturn"]
    assert cx[f"A{12 + len(ex.COST_CENTRES) + 3}"].value == "OK"


@needs_libreoffice
def test_summary_sheets_agree_with_each_other(recalculated):
    wb = openpyxl.load_workbook(recalculated["budget"], data_only=True)
    cc_total = wb["By cost centre"].cell(5 + len(ex.COST_CENTRES), 8).value
    line_total = wb["By line"].cell(5 + len(ex.BUDGET_LINES), 9).value
    month_total = wb["Monthly"]["F17"].value
    assert cc_total == line_total == month_total
    # Cumulative outturn in the last month equals the full-year outturn.
    assert wb["Monthly"]["J16"].value == cc_total


@needs_libreoffice
def test_rag_follows_thresholds(recalculated):
    wb = openpyxl.load_workbook(recalculated["budget"], data_only=True)
    cc = wb["By cost centre"]
    for r in range(5, 5 + len(ex.COST_CENTRES)):
        var_pct = cc.cell(r, 10).value
        expected = "Red" if var_pct > ex.RED_THRESHOLD else "Amber" if var_pct > ex.AMBER_THRESHOLD else "Green"
        assert cc.cell(r, 11).value == expected
    assert cc["K5"].value == "Amber"  # Infrastructure and Cloud in the worked example
