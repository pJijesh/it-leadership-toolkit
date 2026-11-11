import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "04-vendor-scorecard"))

import recalc  # noqa: E402

needs_libreoffice = pytest.mark.skipif(recalc.soffice_path() is None, reason="LibreOffice (soffice) not installed")


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def recalculated(tmp_path_factory):
    """Recalculate each shipped workbook once in a temporary folder and return the paths."""
    if recalc.soffice_path() is None:
        pytest.skip("LibreOffice (soffice) not installed")
    out = tmp_path_factory.mktemp("recalc")
    books = {
        "vendor": ROOT / "04-vendor-scorecard" / "vendor-scorecard.xlsx",
        "budget": ROOT / "05-it-budget-tracker" / "it-budget-tracker.xlsx",
    }
    return {name: recalc.recalculate(src, out / src.name) for name, src in books.items()}
