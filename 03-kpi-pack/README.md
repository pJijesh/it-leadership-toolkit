# KPI pack

A catalogue of 36 IT measures across six domains: service desk, availability, security, projects, cost and people.

| File | Use |
|---|---|
| [kpi-catalogue.md](kpi-catalogue.md) | Readable reference, grouped by domain |
| [kpi-catalogue.csv](kpi-catalogue.csv) | The same data for a spreadsheet, BI tool or wiki import |

Each KPI has an ID, a definition, a formula, a data source, an example target, the unit, whether higher or lower is better, an owner role and a reporting cadence.

## How to choose

1. **Start from the audience.** A board needs eight to twelve measures that show whether the business is protected and well served. A service review needs more detail. A team lead needs operational measures.
2. **Choose for decisions.** Keep a KPI only if a poor result would change what someone does. Drop the rest.
3. **Balance the set.** Include at least one measure from each domain so that good service is not bought with overspend, or low cost with weak security.
4. **Agree definitions before you collect data.** Write down what counts as a ticket, an outage, an active user or a CapEx item. Most disputes about KPIs are disputes about definitions.
5. **Name an owner and a source for every KPI.** If the data cannot be produced without manual rework, say so and fix that first.
6. **Set targets from your own context.** The targets here are examples. Use contracts, past performance and risk appetite to set real ones. Do not import a target from another organisation without checking it applies.
7. **Review twice a year.** Retire measures that no longer drive decisions.

## Common traps

- Reporting averages that hide a long tail. Pair an average with a count of the worst cases.
- Targets that reward the wrong behaviour, for example closing tickets quickly rather than correctly. Pair resolution speed with reopen rate and CSAT.
- Counting outputs (tickets closed) instead of outcomes (users able to work).
- Changing a definition mid-year without restating the history.

## Linking to other artefacts

- The [board report template](../02-board-it-report/template.md) uses a small subset of these.
- The [monthly service review pack](../06-monthly-service-review/template.md) uses the service desk and availability measures.
- The [budget tracker](../05-it-budget-tracker/) calculates the cost measures CO-01, CO-02 and CO-03.
