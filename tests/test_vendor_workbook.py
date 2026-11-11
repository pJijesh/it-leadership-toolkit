import csv

import openpyxl

import score_vendors as sv
from conftest import needs_libreoffice


def formula_cells(ws):
    return [c for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("=")]


def test_workbook_contains_real_formulas(root):
    wb = openpyxl.load_workbook(root / "04-vendor-scorecard" / "vendor-scorecard.xlsx")
    sc = wb["Scorecard"]
    assert len(formula_cells(sc)) >= 25
    assert "SUMPRODUCT" in sc["C20"].value
    assert "RANK" in sc["C22"].value
    assert "SUM(B5:B16)" in sc["B17"].value
    assert 'IF(ROUND(B17,6)=100' in sc["B18"].value
    assert len(formula_cells(wb["Ranking"])) >= 20


def test_csv_matches_workbook_inputs(root):
    wb = openpyxl.load_workbook(root / "04-vendor-scorecard" / "vendor-scorecard.xlsx")
    sc = wb["Scorecard"]
    with open(root / "04-vendor-scorecard" / "vendor-scorecard-example.csv", newline="") as handle:
        rows = list(csv.reader(handle))
    header, body = rows[0], rows[1:]
    vendors = header[2:]
    for j, name in enumerate(vendors):
        assert sc.cell(4, 3 + j).value == name
    for i, row in enumerate(body):
        assert sc.cell(5 + i, 1).value == row[0]
        assert float(sc.cell(5 + i, 2).value) == float(row[1])
        for j, value in enumerate(row[2:]):
            assert float(sc.cell(5 + i, 3 + j).value) == float(value)


@needs_libreoffice
def test_recalculated_workbook_has_no_error_values(recalculated):
    wb = openpyxl.load_workbook(recalculated["vendor"], data_only=True)
    errors = [(ws.title, c.coordinate, c.value) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("#")]
    assert errors == []


@needs_libreoffice
def test_workbook_matches_python_script(root, recalculated):
    expected = sv.score_scorecard(root / "04-vendor-scorecard" / "vendor-scorecard-example.csv")
    wb = openpyxl.load_workbook(recalculated["vendor"], data_only=True)
    sc = wb["Scorecard"]
    assert sc["B18"].value == "OK"
    by_vendor = {}
    for col in range(3, 9):
        name = sc.cell(4, col).value
        if name:
            by_vendor[name] = (sc.cell(20, col).value, sc.cell(22, col).value)
    assert set(by_vendor) == {r["vendor"] for r in expected}
    for r in expected:
        score, rank = by_vendor[r["vendor"]]
        assert abs(score - r["weighted_score"]) < 1e-9
        assert rank == r["rank"]
    # The Ranking sheet lists vendors in the same order as the script.
    rk = wb["Ranking"]
    assert [rk.cell(5 + i, 2).value for i in range(len(expected))] == [r["vendor"] for r in expected]


@needs_libreoffice
def test_bad_weights_are_flagged(root, tmp_path):
    """Change a weight in a copy of the workbook and confirm the check and scores react."""
    import recalc

    wb = openpyxl.load_workbook(root / "04-vendor-scorecard" / "vendor-scorecard.xlsx")
    wb["Scorecard"]["B5"] = 30  # total becomes 105
    src = tmp_path / "broken.xlsx"
    wb.save(src)
    out = recalc.recalculate(src, tmp_path / "broken_recalc.xlsx")
    sc = openpyxl.load_workbook(out, data_only=True)["Scorecard"]
    assert sc["B17"].value == 105
    assert str(sc["B18"].value).startswith("ERROR")
    assert sc["C20"].value == "Check weights"
