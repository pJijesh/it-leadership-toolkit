import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".csv", ".html", ".py", ".yml", ".yaml", ".txt", ".ini"}
SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "venv"}
BAD_DASHES = [chr(0x2014), chr(0x2013)]  # em dash and en dash


def text_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and not (set(path.parts) & SKIP_DIRS):
            yield path


def test_no_em_or_en_dashes(root):
    offenders = []
    for path in text_files(root):
        text = path.read_text(encoding="utf-8")
        if any(d in text for d in BAD_DASHES):
            offenders.append(str(path.relative_to(root)))
    assert offenders == []


def test_relative_markdown_links_resolve(root):
    link = re.compile(r"\]\(([^)\s]+)\)")
    broken = []
    for path in root.rglob("*.md"):
        if set(path.parts) & SKIP_DIRS:
            continue
        for target in link.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#")[0]
            if target_path and not (path.parent / target_path).exists():
                broken.append(f"{path.relative_to(root)} -> {target}")
    assert broken == []


def test_every_template_has_a_worked_example(root):
    # The KPI pack is a populated catalogue (with example targets) rather than a template and example pair.
    for folder in sorted(root.glob("[0-9][0-9]-*")):
        if folder.name == "03-kpi-pack":
            continue
        names = {p.name for p in folder.iterdir()}
        # The two workbooks are both the model and the worked example: inputs are cream cells to overwrite.
        assert any("example" in n or n.endswith(".xlsx") for n in names), f"{folder.name} has no example"


def test_examples_are_labelled_fictional(root):
    for path in root.glob("[0-9][0-9]-*/example-northwind*.md"):
        assert "fictional" in path.read_text(encoding="utf-8").lower(), path.name
