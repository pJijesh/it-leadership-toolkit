"""Recalculate an .xlsx with LibreOffice headless so cached values are stored.

openpyxl writes formulas but no results. Converting through LibreOffice computes
every formula and stores the values, so the workbook previews correctly in
viewers that do not calculate (for example the GitHub file preview).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def soffice_path() -> str | None:
    return shutil.which("soffice") or shutil.which("libreoffice")


def recalculate(src: str | Path, dest: str | Path) -> Path:
    """Write a recalculated copy of src to dest. Raises RuntimeError if LibreOffice is missing."""
    exe = soffice_path()
    if exe is None:
        raise RuntimeError("LibreOffice (soffice) is not available")
    src = Path(src).resolve()
    dest = Path(dest)
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "out"
        out_dir.mkdir()
        profile = Path(tmp) / "profile"
        cmd = [
            exe,
            f"-env:UserInstallation=file://{profile}",
            "--headless",
            "--calc",
            "--convert-to",
            "xlsx:Calc MS Excel 2007 XML",
            "--outdir",
            str(out_dir),
            str(src),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        produced = out_dir / (src.stem + ".xlsx")
        if result.returncode != 0 or not produced.exists():
            raise RuntimeError(f"LibreOffice conversion failed: {result.stdout} {result.stderr}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(produced, dest)
    return dest


def to_pdf(src: str | Path, out_dir: str | Path) -> Path:
    """Render a workbook to PDF with LibreOffice (used for documentation screenshots)."""
    exe = soffice_path()
    if exe is None:
        raise RuntimeError("LibreOffice (soffice) is not available")
    src = Path(src).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            exe,
            f"-env:UserInstallation=file://{tmp}/profile",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(src),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    produced = out_dir / (src.stem + ".pdf")
    if result.returncode != 0 or not produced.exists():
        raise RuntimeError(f"LibreOffice PDF export failed: {result.stdout} {result.stderr}")
    return produced
