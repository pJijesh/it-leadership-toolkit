"""Build 05-it-budget-tracker/it-budget-tracker.xlsx (fictional worked example).

Run from the repository root:  python tools/build_budget_tracker.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import example_data as ex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "05-it-budget-tracker"

NAVY = "1F3A5F"
INPUT_FILL = PatternFill("solid", fgColor="FFF8DC")
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
BAND_FILL = PatternFill("solid", fgColor="F2F4F7")
TOTAL_FILL = PatternFill("solid", fgColor="DCE3EC")
THIN = Side(style="thin", color="C9CED6")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WHITE_BOLD = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
INPUT_FONT = Font(name="Calibri", color="0000FF", size=11)
BASE = Font(name="Calibri", size=11)
BOLD = Font(name="Calibri", bold=True, size=11)
TITLE = Font(name="Calibri", size=16, bold=True, color=NAVY)
NOTE = Font(name="Calibri", italic=True, color="555555", size=10)

GBP = '£#,##0;-£#,##0;£0'
GBP_VAR = '+£#,##0;-£#,##0;£0'
PCT = '0.0%'
PCT_VAR = '+0.0%;-0.0%;0.0%'
MONTH_FMT = "mmm yyyy"

DATA_FIRST = 5
DATA_LAST_RANGE = 1000  # formulas read to this row so new lines can be appended


def header(ws, row, labels, start_col=1, height=32):
    for i, text in enumerate(labels):
        cell = ws.cell(row, start_col + i, text)
        cell.fill = HEADER_FILL
        cell.font = WHITE_BOLD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = height


def page(ws, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def rng(col: str) -> str:
    return f"Data!${col}${DATA_FIRST}:${col}${DATA_LAST_RANGE}"


def rag_formats(ws, ref):
    ws.conditional_formatting.add(ref, CellIsRule(operator="equal", formula=['"Red"'], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE"), font=Font(color="9C0006", bold=True)))
    ws.conditional_formatting.add(ref, CellIsRule(operator="equal", formula=['"Amber"'], fill=PatternFill("solid", bgColor="FFEB9C", fgColor="FFEB9C"), font=Font(color="7F6000", bold=True)))
    ws.conditional_formatting.add(ref, CellIsRule(operator="equal", formula=['"Green"'], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE"), font=Font(color="006100", bold=True)))


def build() -> Path:
    wb = Workbook()
    wb.properties.creator = "Puliyappottammal Jijesh"
    wb.properties.title = "IT budget tracker (fictional example)"

    # ------------------------------------------------------------ Guide
    g = wb.active
    g.title = "Guide"
    g.sheet_view.showGridLines = False
    g.column_dimensions["A"].width = 3
    g.column_dimensions["B"].width = 26
    g.column_dimensions["C"].width = 95
    g["B2"] = "IT budget tracker"
    g["B2"].font = Font(name="Calibri", size=18, bold=True, color=NAVY)
    g["B3"] = f"Worked example for {ex.COMPANY}, {ex.FY_LABEL}. Every figure is invented for illustration."
    g["B3"].font = Font(name="Calibri", italic=True, size=11, color="555555")
    g.page_setup.orientation = "landscape"
    g.page_setup.fitToWidth = 1
    g.page_setup.fitToHeight = 0
    g.sheet_properties.pageSetUpPr.fitToPage = True
    guide_rows = [
        ("Purpose", "Track budget against actual spend and a forecast outturn by cost centre, budget line and month, with the CapEx and OpEx split."),
        ("Sheets", "Settings: reporting month, variance thresholds, cost centres.  By cost centre and By line: year to date and full year position.  Monthly: monthly and cumulative trend.  CapEx vs OpEx: the split.  Data: one row per budget line per month (the only place figures are typed)."),
        ("Monthly routine", "1) On Data, type the month's actuals into the Actual column.  2) Review the Forecast column for the remaining months and update it for known changes.  3) On Settings, move the Reporting month forward.  4) Read By cost centre and write the commentary for the board report."),
        ("Outturn", "Outturn is the latest view of the full year: actual where a month has closed, forecast where it has not. Outturn = Actual if present, otherwise Forecast."),
        ("Variance sign", "Variance = outturn (or actual) minus budget. A positive variance is an overspend. A negative variance is an underspend."),
        ("RAG status", "Green: variance at or below the amber threshold. Amber: above the amber threshold. Red: above the red threshold. Thresholds are on Settings and are examples, so set them to your own policy."),
        ("CapEx and OpEx", "Each budget line is tagged CapEx or OpEx on Data. Apply your own accounting policy and capitalisation threshold when tagging. This workbook does not decide it for you."),
        ("Adding a line", "Add 12 rows at the bottom of Data (one per month) and copy the formulas in columns I to K down. The summary sheets read down to row 1000. Add a new line to By line by copying a row."),
        ("Colour code", "Blue text on a cream background is an input. Everything else is a formula."),
        ("Limits", "This is a management tracker. It is not an accounting system, and it does not replace the finance ledger. Reconcile actuals to finance each month."),
    ]
    r = 5
    for label, text in guide_rows:
        g.cell(r, 2, label).font = BOLD
        g.cell(r, 2).alignment = Alignment(vertical="top")
        g.cell(r, 3, text).font = BASE
        g.cell(r, 3).alignment = Alignment(wrap_text=True, vertical="top")
        g.row_dimensions[r].height = 18 * (1 + len(text) // 95)
        r += 1

    # ------------------------------------------------------------ Settings
    s = wb.create_sheet("Settings")
    s.sheet_view.showGridLines = False
    s["A1"] = "Settings"
    s["A1"].font = TITLE
    s["A2"] = "Cream cells are inputs."
    s["A2"].font = NOTE
    settings = [
        ("Organisation", ex.COMPANY, None),
        ("Financial year", ex.FY_LABEL, None),
        ("Financial year start", ex.FY_START, MONTH_FMT),
        ("Reporting month (last month with actuals)", ex.REPORTING_MONTH, MONTH_FMT),
        ("Amber threshold (variance above, example)", ex.AMBER_THRESHOLD, "0%"),
        ("Red threshold (variance above, example)", ex.RED_THRESHOLD, "0%"),
    ]
    for i, (label, value, fmt) in enumerate(settings):
        row = 4 + i
        s.cell(row, 1, label).font = BOLD
        c = s.cell(row, 2, value)
        c.fill = INPUT_FILL
        c.font = INPUT_FONT
        c.border = BORDER
        c.alignment = Alignment(horizontal="left")
        if fmt:
            c.number_format = fmt
    s["A12"] = "Cost centres"
    s["A12"].font = Font(name="Calibri", bold=True, size=13, color=NAVY)
    header(s, 13, ["Code", "Name"], height=20)
    for i, (code, name) in enumerate(ex.COST_CENTRES):
        for j, v in enumerate((code, name)):
            c = s.cell(14 + i, 1 + j, v)
            c.fill = INPUT_FILL
            c.font = INPUT_FONT
            c.border = BORDER
    cc_first, cc_last = 14, 14 + len(ex.COST_CENTRES) - 1
    s.column_dimensions["A"].width = 44
    s.column_dimensions["B"].width = 34
    page(s)
    wb.defined_names["ReportingMonth"] = DefinedName("ReportingMonth", attr_text="Settings!$B$7")
    wb.defined_names["AmberThreshold"] = DefinedName("AmberThreshold", attr_text="Settings!$B$8")
    wb.defined_names["RedThreshold"] = DefinedName("RedThreshold", attr_text="Settings!$B$9")

    # ------------------------------------------------------------ Data
    d = wb.create_sheet("Data")
    d["A1"] = "Data: one row per budget line per month"
    d["A1"].font = TITLE
    d["A2"] = "Type Actual for closed months and Forecast for open months. Columns I to K are formulas."
    d["A2"].font = NOTE
    header(d, 4, ["Month", "Cost centre", "Line ID", "Description", "Type", "Budget (£)", "Actual (£)", "Forecast (£)", "Outturn (£)", "Variance (£)", "Variance (%)"])
    rows = ex.budget_rows()
    for i, row in enumerate(rows):
        r = DATA_FIRST + i
        d.cell(r, 1, row["month"]).number_format = MONTH_FMT
        d.cell(r, 2, row["cost_centre"])
        d.cell(r, 3, row["line_id"])
        d.cell(r, 4, row["description"])
        d.cell(r, 5, row["type"])
        d.cell(r, 6, row["budget"]).number_format = GBP
        d.cell(r, 7, row["actual"]).number_format = GBP
        d.cell(r, 8, row["forecast"]).number_format = GBP
        d.cell(r, 9, f"=IF(ISNUMBER(G{r}),G{r},N(H{r}))").number_format = GBP
        d.cell(r, 10, f"=I{r}-F{r}").number_format = GBP_VAR
        d.cell(r, 11, f'=IF(F{r}=0,"n/a",J{r}/F{r})').number_format = PCT_VAR
        for col in range(1, 12):
            cell = d.cell(r, col)
            cell.border = BORDER
            if col <= 8:
                cell.fill = INPUT_FILL
                cell.font = INPUT_FONT
            else:
                cell.font = BASE
            if col in (9, 10, 11):
                cell.alignment = Alignment(horizontal="right")
    last_data = DATA_FIRST + len(rows) - 1
    dv_type = DataValidation(type="list", formula1='"CapEx,OpEx"', allow_blank=False, showErrorMessage=True, error="Type must be CapEx or OpEx.")
    dv_cc = DataValidation(type="list", formula1=f"=Settings!$A${cc_first}:$A${cc_last}", allow_blank=False, showErrorMessage=True, error="Choose a cost centre code listed on Settings.")
    dv_amt = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True, showErrorMessage=True, error="Enter a non-negative amount in pounds.")
    for dv in (dv_type, dv_cc, dv_amt):
        d.add_data_validation(dv)
    dv_type.add(f"E{DATA_FIRST}:E{DATA_LAST_RANGE}")
    dv_cc.add(f"B{DATA_FIRST}:B{DATA_LAST_RANGE}")
    dv_amt.add(f"F{DATA_FIRST}:H{DATA_LAST_RANGE}")
    for col, w in zip("ABCDEFGHIJK", [11, 13, 9, 40, 9, 13, 13, 13, 13, 13, 12]):
        d.column_dimensions[col].width = w
    d.freeze_panes = "A5"
    d.auto_filter.ref = f"A4:K{last_data}"
    page(d, landscape=True)

    # ------------------------------------------------------------ By cost centre
    c = wb.create_sheet("By cost centre")
    c.sheet_view.showGridLines = False
    c["A1"] = "Position by cost centre"
    c["A1"].font = TITLE
    c["A2"] = '="Year to date to "&TEXT(ReportingMonth,"mmm yyyy")&". Variance = outturn minus budget; positive is an overspend."'
    c["A2"].font = NOTE
    header(c, 4, ["Code", "Cost centre", "Full-year budget", "YTD budget", "YTD actual", "YTD variance", "YTD variance %", "Full-year outturn", "Full-year variance", "Full-year variance %", "RAG"], height=36)
    n = len(ex.COST_CENTRES)
    first, last = 5, 4 + n
    for i in range(n):
        r = first + i
        c.cell(r, 1, f"=Settings!A{cc_first + i}")
        c.cell(r, 2, f"=Settings!B{cc_first + i}")
        c.cell(r, 3, f"=SUMIFS({rng('F')},{rng('B')},$A{r})")
        c.cell(r, 4, f'=SUMIFS({rng("F")},{rng("B")},$A{r},{rng("A")},"<="&ReportingMonth)')
        c.cell(r, 5, f'=SUMIFS({rng("G")},{rng("B")},$A{r},{rng("A")},"<="&ReportingMonth)')
        c.cell(r, 6, f"=E{r}-D{r}")
        c.cell(r, 7, f"=IF(D{r}=0,0,F{r}/D{r})")
        c.cell(r, 8, f"=SUMIFS({rng('I')},{rng('B')},$A{r})")
        c.cell(r, 9, f"=H{r}-C{r}")
        c.cell(r, 10, f"=IF(C{r}=0,0,I{r}/C{r})")
        c.cell(r, 11, f'=IF(J{r}>RedThreshold,"Red",IF(J{r}>AmberThreshold,"Amber","Green"))')
    t = last + 1
    c.cell(t, 1, "Total")
    c.cell(t, 2, "")
    for col in "CDEFHI":
        c[f"{col}{t}"] = f"=SUM({col}{first}:{col}{last})"
    c[f"G{t}"] = f"=IF(D{t}=0,0,F{t}/D{t})"
    c[f"J{t}"] = f"=IF(C{t}=0,0,I{t}/C{t})"
    c[f"K{t}"] = f'=IF(J{t}>RedThreshold,"Red",IF(J{t}>AmberThreshold,"Amber","Green"))'
    for r in range(first, t + 1):
        for col in range(1, 12):
            cell = c.cell(r, col)
            cell.border = BORDER
            cell.font = BOLD if r == t else BASE
            if r == t:
                cell.fill = TOTAL_FILL
            if col in (3, 4, 5, 8):
                cell.number_format = GBP
            if col in (6, 9):
                cell.number_format = GBP_VAR
            if col in (7, 10):
                cell.number_format = PCT_VAR
            if col == 11:
                cell.alignment = Alignment(horizontal="center")
    rag_formats(c, f"K{first}:K{t}")
    for col, w in zip("ABCDEFGHIJK", [8, 30, 15, 13, 13, 13, 13, 15, 15, 15, 9]):
        c.column_dimensions[col].width = w
    c.freeze_panes = "C5"
    page(c)

    # ------------------------------------------------------------ By line
    ln = wb.create_sheet("By line")
    ln.sheet_view.showGridLines = False
    ln["A1"] = "Position by budget line"
    ln["A1"].font = TITLE
    ln["A2"] = "Same measures as By cost centre, one row per budget line."
    ln["A2"].font = NOTE
    header(ln, 4, ["Line ID", "Description", "Cost centre", "Type", "Full-year budget", "YTD budget", "YTD actual", "YTD variance %", "Full-year outturn", "Full-year variance", "Full-year variance %", "RAG"], height=36)
    line_ids = list(ex.BUDGET_LINES.keys())
    lf, ll = 5, 4 + len(line_ids)
    for i, line_id in enumerate(line_ids):
        r = lf + i
        ln.cell(r, 1, line_id)
        ln.cell(r, 2, f"=INDEX({rng('D')},MATCH($A{r},{rng('C')},0))")
        ln.cell(r, 3, f"=INDEX({rng('B')},MATCH($A{r},{rng('C')},0))")
        ln.cell(r, 4, f"=INDEX({rng('E')},MATCH($A{r},{rng('C')},0))")
        ln.cell(r, 5, f"=SUMIFS({rng('F')},{rng('C')},$A{r})")
        ln.cell(r, 6, f'=SUMIFS({rng("F")},{rng("C")},$A{r},{rng("A")},"<="&ReportingMonth)')
        ln.cell(r, 7, f'=SUMIFS({rng("G")},{rng("C")},$A{r},{rng("A")},"<="&ReportingMonth)')
        ln.cell(r, 8, f"=IF(F{r}=0,0,(G{r}-F{r})/F{r})")
        ln.cell(r, 9, f"=SUMIFS({rng('I')},{rng('C')},$A{r})")
        ln.cell(r, 10, f"=I{r}-E{r}")
        ln.cell(r, 11, f"=IF(E{r}=0,0,J{r}/E{r})")
        ln.cell(r, 12, f'=IF(K{r}>RedThreshold,"Red",IF(K{r}>AmberThreshold,"Amber","Green"))')
    lt = ll + 1
    ln.cell(lt, 1, "Total")
    for col in "EFGIJ":
        ln[f"{col}{lt}"] = f"=SUM({col}{lf}:{col}{ll})"
    ln[f"H{lt}"] = f"=IF(F{lt}=0,0,(G{lt}-F{lt})/F{lt})"
    ln[f"K{lt}"] = f"=IF(E{lt}=0,0,J{lt}/E{lt})"
    ln[f"L{lt}"] = f'=IF(K{lt}>RedThreshold,"Red",IF(K{lt}>AmberThreshold,"Amber","Green"))'
    for r in range(lf, lt + 1):
        for col in range(1, 13):
            cell = ln.cell(r, col)
            cell.border = BORDER
            cell.font = BOLD if r == lt else BASE
            if r == lt:
                cell.fill = TOTAL_FILL
            if col in (5, 6, 7, 9):
                cell.number_format = GBP
            if col == 10:
                cell.number_format = GBP_VAR
            if col in (8, 11):
                cell.number_format = PCT_VAR
            if col in (3, 4, 12):
                cell.alignment = Alignment(horizontal="center")
    rag_formats(ln, f"L{lf}:L{lt}")
    for col, w in zip("ABCDEFGHIJKL", [9, 40, 11, 9, 15, 13, 13, 13, 15, 15, 15, 9]):
        ln.column_dimensions[col].width = w
    ln.freeze_panes = "C5"
    page(ln)

    # ------------------------------------------------------------ Monthly
    m = wb.create_sheet("Monthly")
    m.sheet_view.showGridLines = False
    m["A1"] = "Monthly profile"
    m["A1"].font = TITLE
    m["A2"] = "Actual is shown for closed months; outturn uses forecast for open months."
    m["A2"].font = NOTE
    header(m, 4, ["Month", "Status", "Budget", "Actual", "Forecast", "Outturn", "Variance", "Variance %", "Cumulative budget", "Cumulative outturn", "Cumulative variance"], height=36)
    months = ex.fy_months()
    mf = 5
    for i, month in enumerate(months):
        r = mf + i
        if i == 0:
            m.cell(r, 1, "=Settings!B6")
        else:
            m.cell(r, 1, f"=EDATE(A{r - 1},1)")
        m.cell(r, 2, f'=IF(A{r}<=ReportingMonth,"Actual","Forecast")')
        m.cell(r, 3, f"=SUMIFS({rng('F')},{rng('A')},$A{r})")
        m.cell(r, 4, f'=IF(B{r}="Actual",SUMIFS({rng("G")},{rng("A")},$A{r}),0)')
        m.cell(r, 5, f'=IF(B{r}="Forecast",SUMIFS({rng("H")},{rng("A")},$A{r}),0)')
        m.cell(r, 6, f"=D{r}+E{r}")
        m.cell(r, 7, f"=F{r}-C{r}")
        m.cell(r, 8, f"=IF(C{r}=0,0,G{r}/C{r})")
        m.cell(r, 9, f"=SUM(C${mf}:C{r})")
        m.cell(r, 10, f"=SUM(F${mf}:F{r})")
        m.cell(r, 11, f"=J{r}-I{r}")
    ml = mf + 11
    mt = ml + 1
    m.cell(mt, 1, "Total")
    for col in "CDEFG":
        m[f"{col}{mt}"] = f"=SUM({col}{mf}:{col}{ml})"
    m[f"H{mt}"] = f"=IF(C{mt}=0,0,G{mt}/C{mt})"
    for r in range(mf, mt + 1):
        for col in range(1, 12):
            cell = m.cell(r, col)
            cell.border = BORDER
            cell.font = BOLD if r == mt else BASE
            if r == mt:
                cell.fill = TOTAL_FILL
            if col == 1:
                cell.number_format = MONTH_FMT
                cell.alignment = Alignment(horizontal="left")
            if col in (3, 4, 5, 6, 9, 10):
                cell.number_format = GBP
            if col in (7, 11):
                cell.number_format = GBP_VAR
            if col == 8:
                cell.number_format = PCT_VAR
            if col == 2:
                cell.alignment = Alignment(horizontal="center")
    for col, w in zip("ABCDEFGHIJK", [11, 10, 13, 13, 13, 13, 13, 12, 17, 17, 17]):
        m.column_dimensions[col].width = w
    chart = BarChart()
    chart.type = "col"
    chart.title = "Monthly budget and outturn (£)"
    chart.height = 8.5
    chart.width = 22
    chart.y_axis.number_format = "£#,##0"
    chart.y_axis.delete = False
    chart.x_axis.delete = False
    chart.x_axis.number_format = "mmm"
    chart.add_data(Reference(m, min_col=3, min_row=4, max_row=ml), titles_from_data=True)
    chart.add_data(Reference(m, min_col=6, min_row=4, max_row=ml), titles_from_data=True)
    chart.set_categories(Reference(m, min_col=1, min_row=mf, max_row=ml))
    chart.legend.position = "b"
    m.add_chart(chart, f"A{mt + 3}")
    page(m)

    # ------------------------------------------------------------ CapEx vs OpEx
    x = wb.create_sheet("CapEx vs OpEx")
    x.sheet_view.showGridLines = False
    x["A1"] = "CapEx and OpEx split"
    x["A1"].font = TITLE
    x["A2"] = "Type is set per budget line on Data. Apply your own capitalisation policy."
    x["A2"].font = NOTE
    header(x, 4, ["Type", "Full-year budget", "Share of budget", "YTD budget", "YTD actual", "Full-year outturn", "Share of outturn", "Full-year variance %"], height=36)
    for i, typ in enumerate(["CapEx", "OpEx"]):
        r = 5 + i
        x.cell(r, 1, typ)
        x.cell(r, 2, f"=SUMIFS({rng('F')},{rng('E')},$A{r})")
        x.cell(r, 3, f"=IF(B$7=0,0,B{r}/B$7)")
        x.cell(r, 4, f'=SUMIFS({rng("F")},{rng("E")},$A{r},{rng("A")},"<="&ReportingMonth)')
        x.cell(r, 5, f'=SUMIFS({rng("G")},{rng("E")},$A{r},{rng("A")},"<="&ReportingMonth)')
        x.cell(r, 6, f"=SUMIFS({rng('I')},{rng('E')},$A{r})")
        x.cell(r, 7, f"=IF(F$7=0,0,F{r}/F$7)")
        x.cell(r, 8, f"=IF(B{r}=0,0,(F{r}-B{r})/B{r})")
    x.cell(7, 1, "Total")
    for col in "BDEF":
        x[f"{col}7"] = f"=SUM({col}5:{col}6)"
    x["C7"] = "=SUM(C5:C6)"
    x["G7"] = "=SUM(G5:G6)"
    x["H7"] = "=IF(B7=0,0,(F7-B7)/B7)"
    for r in range(5, 8):
        for col in range(1, 9):
            cell = x.cell(r, col)
            cell.border = BORDER
            cell.font = BOLD if r == 7 else BASE
            if r == 7:
                cell.fill = TOTAL_FILL
            if col in (2, 4, 5, 6):
                cell.number_format = GBP
            if col in (3, 7):
                cell.number_format = PCT
            if col == 8:
                cell.number_format = PCT_VAR
    x["A10"] = "Full-year outturn by cost centre and type"
    x["A10"].font = Font(name="Calibri", bold=True, size=13, color=NAVY)
    header(x, 11, ["Code", "Cost centre", "CapEx outturn", "OpEx outturn", "Total outturn", "CapEx share"], height=24)
    for i in range(n):
        r = 12 + i
        x.cell(r, 1, f"=Settings!A{cc_first + i}")
        x.cell(r, 2, f"=Settings!B{cc_first + i}")
        x.cell(r, 3, f'=SUMIFS({rng("I")},{rng("B")},$A{r},{rng("E")},"CapEx")')
        x.cell(r, 4, f'=SUMIFS({rng("I")},{rng("B")},$A{r},{rng("E")},"OpEx")')
        x.cell(r, 5, f"=C{r}+D{r}")
        x.cell(r, 6, f"=IF(E{r}=0,0,C{r}/E{r})")
    xt = 12 + n
    x.cell(xt, 1, "Total")
    for col in "CDE":
        x[f"{col}{xt}"] = f"=SUM({col}12:{col}{xt - 1})"
    x[f"F{xt}"] = f"=IF(E{xt}=0,0,C{xt}/E{xt})"
    for r in range(12, xt + 1):
        for col in range(1, 7):
            cell = x.cell(r, col)
            cell.border = BORDER
            cell.font = BOLD if r == xt else BASE
            if r == xt:
                cell.fill = TOTAL_FILL
            if col in (3, 4, 5):
                cell.number_format = GBP
            if col == 6:
                cell.number_format = PCT
    x[f"A{xt + 2}"] = "Reconciliation check: total outturn here equals total outturn on By cost centre."
    x[f"A{xt + 2}"].font = NOTE
    x[f"A{xt + 3}"] = f"=IF(ROUND(E{xt}-'By cost centre'!H{t},2)=0,\"OK\",\"ERROR: totals differ\")"
    x[f"A{xt + 3}"].font = BOLD
    x.conditional_formatting.add(f"A{xt + 3}", CellIsRule(operator="equal", formula=['"OK"'], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    x.conditional_formatting.add(f"A{xt + 3}", CellIsRule(operator="notEqual", formula=['"OK"'], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    for col, w in zip("ABCDEFGH", [12, 30, 16, 16, 16, 16, 15, 15]):
        x.column_dimensions[col].width = w
    page(x)

    # sheet order: Guide, Settings, By cost centre, By line, Monthly, CapEx vs OpEx, Data
    order = ["Guide", "Settings", "By cost centre", "By line", "Monthly", "CapEx vs OpEx", "Data"]
    wb._sheets = [wb[name] for name in order]
    wb.active = 0
    wb.calculation.fullCalcOnLoad = True
    path = OUT_DIR / "it-budget-tracker.xlsx"
    wb.save(path)
    return path


# Addresses the tests rely on.
LAYOUT = {
    "cc_sheet": "By cost centre",
    "cc_first": 5,
    "cc_total": 10,
    "data_first": DATA_FIRST,
    "data_rows": 144,
}

if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    print("wrote", build())
