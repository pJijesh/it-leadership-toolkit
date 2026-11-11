# Contributing

Thank you for considering a contribution. This is a small, practical toolkit, so the bar is simple: changes should make a template clearer, more correct or more useful to a working IT manager.

## What is welcome

- Corrections to formulas, definitions or wording
- Clearer guidance notes, or a missing step in a checklist
- Additional KPIs, with a definition, formula, data source and owner
- Tests that make the checks stronger
- Accessibility improvements to the HTML report

## Ground rules

1. **Fictional data only.** Examples use the invented company "Northwind Freight (fictional)". Do not add real company names, people, contracts or figures, and do not add anything taken from an employer or client.
2. **No invented statistics or benchmarks.** Targets in examples must be labelled "example". Do not present a number as an industry norm unless you can cite a public source in the same change.
3. **British English, plain style.** Professional tone, no hype, no em-dashes. Currency in pounds sterling.
4. **Generated files come from the build scripts.** The workbooks, KPI and risk files, and the board report example are produced by `tools/`. Change the source (`tools/example_data.py` and the `build_*.py` scripts) and run `python tools/build_all.py` rather than editing the output by hand.
5. **Keep the checks green.** Run `pytest` before opening a pull request.

## Setting up

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt          # tests and workbook builders
pip install -r requirements-dev.txt      # also needed to render the PDF and images
playwright install chromium              # for the board report PDF
```

LibreOffice is optional. Without it the workbook recalculation tests are skipped, and workbooks are written without cached values.

## Pull requests

Keep each pull request focused, describe what changed and why, and mention which artefact it touches. If you change a figure in the example data, rebuild so the workbook, report and documents stay consistent.
