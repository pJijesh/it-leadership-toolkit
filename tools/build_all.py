"""Rebuild every generated artefact in the repository.

Run from the repository root:  python tools/build_all.py
Needs openpyxl always; LibreOffice (soffice) to store calculated values in the
workbooks and render sheet images; Playwright with Chromium for the board report PDF.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import build_board_report  # noqa: E402
import build_budget_tracker  # noqa: E402
import build_csvs  # noqa: E402
import build_vendor_scorecard  # noqa: E402
import recalc  # noqa: E402

SHEET_IMAGES = {
    "05-it-budget-tracker/it-budget-tracker.xlsx": [
        ("Position by cost centre", "budget-tracker-by-cost-centre.png"),
        ("Position by budget line", "budget-tracker-by-line.png"),
        ("Monthly profile", "budget-tracker-monthly.png"),
        ("CapEx and OpEx split", "budget-tracker-capex-opex.png"),
    ],
    "04-vendor-scorecard/vendor-scorecard.xlsx": [
        ("Edit the cream cells", "vendor-scorecard-scorecard.png"),
        ("Calculated from the Scorecard sheet", "vendor-scorecard-ranking.png"),
    ],
}


def page_texts(pdf: Path) -> list[str]:
    n = int([l for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages:")][0].split()[1])
    return [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]


def crop(path: Path) -> None:
    from PIL import Image, ImageChops

    img = Image.open(path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    box = ImageChops.difference(img, bg).getbbox()
    if box:
        pad = 24
        box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, img.width), min(box[3] + pad, img.height))
        img.crop(box).save(path)


def main() -> None:
    build_csvs.write_kpi_csv()
    build_csvs.write_kpi_md()
    build_csvs.write_risk_files()
    build_vendor_scorecard.OUT_DIR.mkdir(exist_ok=True)
    build_vendor_scorecard.write_csv()
    build_vendor_scorecard.build_workbook()
    build_budget_tracker.build()
    build_board_report.build(render_pdf=True)

    if recalc.soffice_path() is None:
        print("LibreOffice not found: workbooks left uncalculated and no sheet images produced.")
        return
    for rel, images in SHEET_IMAGES.items():
        book = ROOT / rel
        recalc.recalculate(book, book)  # replace with the recalculated copy (formulas kept, values cached)
        with tempfile.TemporaryDirectory() as tmp:
            pdf = recalc.to_pdf(book, tmp)
            texts = page_texts(pdf)
            for marker, name in images:
                idx = next(i for i, t in enumerate(texts, start=1) if marker in t)
                prefix = Path(tmp) / "p"
                subprocess.run(["pdftoppm", "-r", "110", "-png", "-f", str(idx), "-l", str(idx), str(pdf), str(prefix)], check=True)
                produced = next(Path(tmp).glob("p-*.png"))
                target = ROOT / "docs" / name
                target.write_bytes(produced.read_bytes())
                produced.unlink()
                crop(target)
                print("wrote", target)


if __name__ == "__main__":
    main()
