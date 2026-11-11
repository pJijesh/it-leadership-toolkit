"""Build 04-vendor-scorecard/vendor-scorecard.xlsx and the matching CSV.

Run from the repository root:  python tools/build_vendor_scorecard.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import example_data as ex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "04-vendor-scorecard"

NAVY = "1F3A5F"
GREY = "F2F4F7"
INPUT_FILL = PatternFill("solid", fgColor="FFF8DC")
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
BAND_FILL = PatternFill("solid", fgColor=GREY)
THIN = Side(style="thin", color="C9CED6")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WHITE_BOLD = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
INPUT_FONT = Font(name="Calibri", color="0000FF", size=11)
BASE = Font(name="Calibri", size=11)
BOLD = Font(name="Calibri", bold=True, size=11)

FIRST_CRIT_ROW = 5
CRIT_SLOTS = 12
LAST_CRIT_ROW = FIRST_CRIT_ROW + CRIT_SLOTS - 1  # 16
FIRST_VENDOR_COL = 3  # column C
VENDOR_SLOTS = ex.MAX_VENDOR_COLUMNS
LAST_VENDOR_COL = FIRST_VENDOR_COL + VENDOR_SLOTS - 1  # H


def write_csv() -> Path:
    path = OUT_DIR / "vendor-scorecard-example.csv"
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["criterion", "weight", *ex.VENDORS])
        for (criterion, weight), scores in zip(ex.VENDOR_CRITERIA, ex.VENDOR_SCORES):
            writer.writerow([criterion, weight, *scores])
    return path


def build_workbook() -> Path:
    wb = Workbook()
    wb.properties.creator = "Puliyappottammal Jijesh"
    wb.properties.title = "Vendor scorecard (fictional example)"

    # ---------------- Guide ----------------
    guide = wb.active
    guide.title = "Guide"
    guide.sheet_view.showGridLines = False
    guide.column_dimensions["A"].width = 3
    guide.column_dimensions["B"].width = 28
    guide.column_dimensions["C"].width = 90
    guide["B2"] = "Vendor scorecard: weighted criteria model"
    guide["B2"].font = Font(name="Calibri", size=18, bold=True, color=NAVY)
    guide["B3"] = f"Worked example for {ex.COMPANY}: re-tender of a managed service desk. All names and scores are invented."
    guide["B3"].font = Font(name="Calibri", italic=True, size=11, color="555555")
    guide.page_setup.orientation = "landscape"
    guide.page_setup.fitToWidth = 1
    guide.page_setup.fitToHeight = 0
    guide.sheet_properties.pageSetUpPr.fitToPage = True
    rows = [
        ("Purpose", "Compare shortlisted suppliers against criteria that were agreed and weighted before any proposals were read."),
        ("How it works", "Weighted score = SUMPRODUCT(weights, scores) / SUM(weights). Scores run from 0 to 5, so the weighted score does too. Rank 1 is the highest weighted score."),
        ("Step 1", "On the Scorecard sheet, edit the criteria and set the weights (percent). The weights check must read OK, meaning they sum to exactly 100."),
        ("Step 2", "Type the vendor names in the header row (up to six). Leave unused vendor columns blank."),
        ("Step 3", "Score every criterion for every vendor from 0 to 5 using the scale below. Record the evidence for each score in your evaluation notes."),
        ("Step 4", "Read the Ranking sheet. Ties share a rank. Treat close scores as a prompt for a clarification round, not as a decision."),
        ("Colour code", "Blue text on a cream background is an input. Everything else is a formula and should not be overtyped."),
        ("0", "Not offered or fails a mandatory requirement."),
        ("1", "Poor: significant gaps, high risk."),
        ("2", "Weak: partly meets the requirement, material concerns."),
        ("3", "Meets the requirement."),
        ("4", "Exceeds the requirement in some respects."),
        ("5", "Clearly exceptional, evidenced by references or a demonstration."),
        ("Scoring cost", "Score price on a stated rule, agreed in advance. One option: the lowest three-year cost scores 5 and each other bid scores 5 x (lowest cost / bid cost)."),
        ("Cross-check", "score_vendors.py in this folder applies the same arithmetic to the CSV. The two should always agree."),
        ("Limits", "A scorecard supports a decision. It does not replace due diligence, reference calls, security review or legal review."),
    ]
    r = 5
    for label, text in rows:
        guide.cell(r, 2, label).font = BOLD
        guide.cell(r, 3, text).font = BASE
        guide.cell(r, 3).alignment = Alignment(wrap_text=True, vertical="top")
        guide.cell(r, 2).alignment = Alignment(vertical="top")
        guide.row_dimensions[r].height = 32 if len(text) > 90 else 18
        r += 1

    # ---------------- Scorecard ----------------
    sc = wb.create_sheet("Scorecard")
    sc.sheet_view.showGridLines = False
    sc["A1"] = "Scorecard"
    sc["A1"].font = Font(name="Calibri", size=16, bold=True, color=NAVY)
    sc["A2"] = "Edit the cream cells. Weights are percentages and must sum to 100. Scores are 0 to 5."
    sc["A2"].font = Font(name="Calibri", italic=True, color="555555")

    sc.cell(4, 1, "Criterion")
    sc.cell(4, 2, "Weight (%)")
    for i in range(VENDOR_SLOTS):
        col = FIRST_VENDOR_COL + i
        name = ex.VENDORS[i] if i < len(ex.VENDORS) else None
        sc.cell(4, col, name)
    for col in range(1, LAST_VENDOR_COL + 1):
        cell = sc.cell(4, col)
        cell.fill = HEADER_FILL
        cell.font = WHITE_BOLD
        cell.alignment = Alignment(horizontal="center" if col > 1 else "left", vertical="center", wrap_text=True)
        cell.border = BORDER
    sc.row_dimensions[4].height = 22

    for slot in range(CRIT_SLOTS):
        row = FIRST_CRIT_ROW + slot
        if slot < len(ex.VENDOR_CRITERIA):
            criterion, weight = ex.VENDOR_CRITERIA[slot]
            sc.cell(row, 1, criterion)
            sc.cell(row, 2, weight)
            for i in range(len(ex.VENDORS)):
                sc.cell(row, FIRST_VENDOR_COL + i, ex.VENDOR_SCORES[slot][i])
        for col in range(1, LAST_VENDOR_COL + 1):
            cell = sc.cell(row, col)
            cell.fill = INPUT_FILL
            cell.font = INPUT_FONT
            cell.border = BORDER
            cell.alignment = Alignment(horizontal="left" if col == 1 else "center")
    # Vendor name cells are inputs too, but keep the header look.

    dv_score = DataValidation(
        type="decimal", operator="between", formula1="0", formula2="5", allow_blank=True,
        showErrorMessage=True, errorTitle="Score out of range", error="Scores must be between 0 and 5.",
    )
    dv_weight = DataValidation(
        type="decimal", operator="between", formula1="0", formula2="100", allow_blank=True,
        showErrorMessage=True, errorTitle="Weight out of range", error="Weights are percentages between 0 and 100.",
    )
    sc.add_data_validation(dv_score)
    sc.add_data_validation(dv_weight)
    dv_score.add(f"{get_column_letter(FIRST_VENDOR_COL)}{FIRST_CRIT_ROW}:{get_column_letter(LAST_VENDOR_COL)}{LAST_CRIT_ROW}")
    dv_weight.add(f"B{FIRST_CRIT_ROW}:B{LAST_CRIT_ROW}")

    f, l = FIRST_CRIT_ROW, LAST_CRIT_ROW  # 5, 16
    tot_row = l + 1  # 17
    chk_row = l + 2  # 18
    sc.cell(tot_row, 1, "Total weight (%)")
    sc.cell(tot_row, 2, f"=SUM(B{f}:B{l})")
    sc.cell(chk_row, 1, "Weights check")
    sc.cell(chk_row, 2, f'=IF(ROUND(B{tot_row},6)=100,"OK","ERROR: weights must sum to 100")')
    sc.merge_cells(start_row=chk_row, start_column=2, end_row=chk_row, end_column=4)

    res = l + 4  # 20 weighted score
    pct = res + 1
    rank = res + 2
    done = res + 3
    pos = res + 4
    sc.cell(res - 1, 1, "Results").font = Font(name="Calibri", bold=True, size=13, color=NAVY)
    labels = {
        res: "Weighted score (0 to 5)",
        pct: "Percent of maximum",
        rank: "Rank (ties share a rank)",
        done: "Scores entered",
        pos: "Position (ties broken by column order)",
    }
    for rr, text in labels.items():
        sc.cell(rr, 1, text).font = BOLD
    for i in range(VENDOR_SLOTS):
        col = FIRST_VENDOR_COL + i
        c = get_column_letter(col)
        rng = f"${get_column_letter(FIRST_VENDOR_COL)}${res}:${get_column_letter(LAST_VENDOR_COL)}${res}"
        sc.cell(
            res, col,
            f'=IF({c}$4="","",IF(ROUND($B${tot_row},6)<>100,"Check weights",SUMPRODUCT($B${f}:$B${l},{c}{f}:{c}{l})/$B${tot_row}))',
        ).number_format = "0.00"
        sc.cell(pct, col, f'=IF(ISNUMBER({c}{res}),{c}{res}/5,"")').number_format = "0.0%"
        sc.cell(rank, col, f'=IF(ISNUMBER({c}{res}),RANK({c}{res},{rng},0),"")')
        sc.cell(done, col, f'=IF({c}$4="","",COUNT({c}{f}:{c}{l})&" of "&COUNTA($A${f}:$A${l}))')
        first = get_column_letter(FIRST_VENDOR_COL)
        sc.cell(pos, col, f'=IF(ISNUMBER({c}{res}),{c}{rank}+COUNTIF(${first}${res}:{c}{res},{c}{res})-1,"")')
        for rr in (res, pct, rank, done, pos):
            cell = sc.cell(rr, col)
            cell.alignment = Alignment(horizontal="center")
            cell.border = BORDER
            cell.fill = BAND_FILL
            cell.font = BOLD if rr in (res, rank) else BASE
    for rr in (tot_row, chk_row):
        for col in (1, 2):
            sc.cell(rr, col).font = BOLD
    sc.cell(tot_row, 2).alignment = Alignment(horizontal="center")
    sc.cell(chk_row, 2).alignment = Alignment(horizontal="center")

    green = PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")
    red = PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")
    sc.conditional_formatting.add(f"B{chk_row}", CellIsRule(operator="equal", formula=['"OK"'], fill=green))
    sc.conditional_formatting.add(f"B{chk_row}", CellIsRule(operator="notEqual", formula=['"OK"'], fill=red))
    sc.conditional_formatting.add(
        f"{get_column_letter(FIRST_VENDOR_COL)}{rank}:{get_column_letter(LAST_VENDOR_COL)}{rank}",
        CellIsRule(operator="equal", formula=["1"], fill=green),
    )

    sc.column_dimensions["A"].width = 40
    sc.column_dimensions["B"].width = 14
    for col in range(FIRST_VENDOR_COL, LAST_VENDOR_COL + 1):
        sc.column_dimensions[get_column_letter(col)].width = 14
    sc.freeze_panes = "C5"
    sc.page_setup.orientation = "landscape"
    sc.page_setup.fitToWidth = 1
    sc.page_setup.fitToHeight = 1
    sc.sheet_properties.pageSetUpPr.fitToPage = True

    # ---------------- Ranking ----------------
    rk = wb.create_sheet("Ranking")
    rk.sheet_view.showGridLines = False
    rk["A1"] = "Ranking"
    rk["A1"].font = Font(name="Calibri", size=16, bold=True, color=NAVY)
    rk["A2"] = "Calculated from the Scorecard sheet. Nothing to type here."
    rk["A2"].font = Font(name="Calibri", italic=True, color="555555")
    for col, text in enumerate(["Position", "Vendor", "Weighted score (0 to 5)", "Percent of maximum", "Rank"], start=1):
        cell = rk.cell(4, col, text)
        cell.fill = HEADER_FILL
        cell.font = WHITE_BOLD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    rk.row_dimensions[4].height = 32
    v0 = get_column_letter(FIRST_VENDOR_COL)
    v1 = get_column_letter(LAST_VENDOR_COL)
    for n in range(1, VENDOR_SLOTS + 1):
        row = 4 + n
        rk.cell(row, 1, n)
        rk.cell(row, 2, f'=IFERROR(INDEX(Scorecard!${v0}$4:${v1}$4,MATCH($A{row},Scorecard!${v0}${pos}:${v1}${pos},0)),"")')
        rk.cell(row, 3, f'=IFERROR(INDEX(Scorecard!${v0}${res}:${v1}${res},MATCH($A{row},Scorecard!${v0}${pos}:${v1}${pos},0)),"")').number_format = "0.00"
        rk.cell(row, 4, f'=IFERROR(INDEX(Scorecard!${v0}${pct}:${v1}${pct},MATCH($A{row},Scorecard!${v0}${pos}:${v1}${pos},0)),"")').number_format = "0.0%"
        rk.cell(row, 5, f'=IFERROR(INDEX(Scorecard!${v0}${rank}:${v1}${rank},MATCH($A{row},Scorecard!${v0}${pos}:${v1}${pos},0)),"")')
        for col in range(1, 6):
            cell = rk.cell(row, col)
            cell.border = BORDER
            cell.font = BASE
            cell.alignment = Alignment(horizontal="left" if col == 2 else "center")
    rk.conditional_formatting.add(
        f"D5:D{4 + VENDOR_SLOTS}",
        DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="5B8DB8", showValue=True),
    )
    rk.conditional_formatting.add(
        f"A5:E{4 + VENDOR_SLOTS}",
        FormulaRule(formula=["$E5=1"], fill=PatternFill("solid", bgColor="E2F0D9", fgColor="E2F0D9")),
    )
    rk["A12"] = "A scorecard supports the decision. Record the rationale for the final choice in the decision memo."
    rk["A12"].font = Font(name="Calibri", italic=True, color="555555")
    for col, width in zip("ABCDE", [11, 22, 20, 20, 9]):
        rk.column_dimensions[col].width = width
    rk.page_setup.orientation = "landscape"
    rk.page_setup.fitToWidth = 1
    rk.page_setup.fitToHeight = 1
    rk.sheet_properties.pageSetUpPr.fitToPage = True

    wb.calculation.fullCalcOnLoad = True
    path = OUT_DIR / "vendor-scorecard.xlsx"
    wb.save(path)
    return path


# Cell addresses the tests rely on (kept in one place).
LAYOUT = {
    "sheet": "Scorecard",
    "vendor_header_row": 4,
    "first_vendor_col": FIRST_VENDOR_COL,
    "first_row": FIRST_CRIT_ROW,
    "last_row": LAST_CRIT_ROW,
    "total_weight": "B17",
    "weights_check": "B18",
    "weighted_row": 20,
    "rank_row": 22,
}


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    print("wrote", write_csv())
    print("wrote", build_workbook())
