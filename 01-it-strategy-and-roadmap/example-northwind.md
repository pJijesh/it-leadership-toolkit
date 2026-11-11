# IT strategy and three-year roadmap: FY2026/27 to FY2028/29

**Northwind Freight (fictional).** A worked example. The company, people and every figure are invented. The Year 1 budget matches the [budget tracker example](../05-it-budget-tracker/).

Prepared by: IT Manager | Approver: Board | Status: draft for discussion

---

## 1. Purpose and scope

This strategy covers technology at all Northwind Freight sites: the core operations platform, end-user services, networks, security, data and the suppliers that support them. It covers the three financial years from April 2026. It does not cover the commercial pricing strategy or the property programme, although both depend on it.

## 2. Business context

Northwind Freight is a fictional regional freight forwarder with five operating sites, a customer base that is moving to digital booking and tracking, and a leadership team that wants to grow without a matching growth in overheads.

| Business goal | What technology must enable | Executive sponsor |
|---|---|---|
| Grow volume without growing back-office headcount at the same rate | Automation of repeatable booking, documentation and invoicing steps | Chief Operating Officer |
| Win and keep larger customers | Reliable, secure service and electronic data exchange with customers | Commercial Director |
| Improve warehouse accuracy and speed | Scanning and real-time stock status at every site | Operations Director |
| Stay resilient to cyber attack and supplier failure | Tested recovery, strong access control, a clear view of supplier dependency | Finance Director |

## 3. Current state

| Area | Strengths | Gaps and risks | Evidence |
|---|---|---|---|
| Services and operations | Stable core platform; clear ticket process | Some tickets miss SLA at month end; no formal problem management | Service review pack, last six months |
| Applications | One main operations platform, well understood | Integrations are custom and held by two people | Integration inventory |
| Infrastructure and cloud | Mostly cloud hosted | Hosting cost rising faster than plan | Budget tracker |
| Security and resilience | Multi-factor authentication on most accounts | Not yet universal; backup restore not tested in the last 12 months | Risk register R-002, R-009 |
| Data | Operational data is complete | Reporting is manual and slow; no single definition of key measures | Finance and operations interviews |
| People and skills | Small, committed team | Key-person dependency | Risk register R-004 |
| Suppliers and contracts | Managed service desk in place | Contract expires in 2027; no renewal calendar | Contract register |
| Cost and value | Budget tracked monthly | No unit-cost view | Budget tracker |

## 4. Guiding principles

1. **Buy before build** unless the capability differentiates us in the market.
2. **Secure by default.** New services launch with multi-factor authentication, logging and a tested recovery path.
3. **One source of truth** for each important data set, with a named owner.
4. **Integrate, do not re-key.** Data is entered once and reused.
5. **Every contract has an owner, a renewal date and an exit plan.**
6. **Measure what we report.** A KPI needs a definition, a source and an owner before it goes on a dashboard.

## 5. Strategic themes and objectives

| Theme | Objective | Measure of success | Owner |
|---|---|---|---|
| 1. Reliable core services | Keep the operations platform and service desk dependable as volume grows | Core availability (AV-01), resolution within SLA (SD-02), change success rate (AV-04) | Service Delivery Manager |
| 2. Secure and resilient | Reduce the chance and impact of cyber attack and failure | MFA coverage (SE-01), critical patches on time (SE-02), backup restore tests passed (AV-06) | Security Lead |
| 3. Data we can trust | Give leaders accurate operational and financial reporting without manual rework | Reports produced automatically (project measure); share of key data sets with a named owner | Applications Lead |
| 4. Connected customers and partners | Exchange booking and status data electronically with the largest customers | Share of bookings received electronically (set baseline in Year 1) | Applications Lead |
| 5. Efficient and well-governed IT | Control cost, manage suppliers and deliver projects predictably | Spend against budget (CO-01), contracts reviewed before notice date (CO-06), milestones on time (PR-02) | IT Manager |

## 6. Three-year roadmap

| Horizon | Initiative | Theme | Outcome | Indicative cost | Dependencies | Owner |
|---|---|---|---|---|---|---|
| Now | Warehouse scanning rollout | 1, 4 | Real-time stock status at all five sites | £96,000 (budgeted) | Hardware delivery | Project Manager |
| Now | Cloud cost optimisation review | 5 | Hosting cost matched to need; options for reserved capacity | Within run cost | Usage data | Infrastructure Lead |
| Now | Extend multi-factor authentication to all accounts | 2 | Full coverage | Within security tooling budget | Exceptions list | Security Lead |
| Now | Managed service desk re-tender | 1, 5 | Better service at equal or lower cost | Transition £10,000 to £15,000 | Contract end date | IT Manager |
| Now | Disaster recovery and restore test | 2 | Proven recovery time for the core platform | Within run cost | Business agreement on test window | Infrastructure Lead |
| Now | Data platform pilot | 3 | Automated operational and financial reports from one source | £60,000 (budgeted) | Data owners named | Applications Lead |
| Next | Customer data exchange for the largest customers | 4 | Electronic booking and status messages | £80,000 to £120,000 | Pilot results, customer readiness | Applications Lead |
| Next | Server and storage review and refresh plan | 1, 2 | Supported, resilient platform for the next five years | To be scoped | Asset lifecycle plan | Infrastructure Lead |
| Next | Workflow automation of invoicing steps | 1, 3 | Fewer manual touches per shipment | £50,000 to £80,000 | Data platform | Applications Lead |
| Later | Extend data platform to forecasting | 3 | Demand and capacity views | To be scoped | Data quality baseline | Applications Lead |
| Later | Review core platform contract and alternatives | 5 | Informed renewal decision | Review cost only | Contract end date | IT Manager |

**Not doing.** Building a custom operations platform; moving all workloads to a different cloud provider in this period; running a private data centre. Each was considered and rejected as poor value or poor risk for a company of this size.

## 7. Investment summary

| | FY2026/27 | FY2027/28 | FY2028/29 |
|---|---:|---:|---:|
| Run cost (OpEx) | £882,000 | £920,000 | £955,000 |
| Change and capital (CapEx) | £432,000 | £410,000 | £380,000 |
| **Total** | **£1,314,000** | **£1,330,000** | **£1,335,000** |
| Status | Approved budget | Indicative | Indicative |

Year 2 and Year 3 are planning assumptions, not forecasts. They assume volume growth is absorbed by automation, contract renewals rise with the supplier's stated indexation, and cloud cost is brought under control by the optimisation review. They will be re-based each year.

## 8. Risks and dependencies

| Risk | Owner | Mitigation |
|---|---|---|
| R-001 Cloud hosting cost grows faster than forecast | IT Manager | Optimisation review; budget alerts; reserved capacity options |
| R-002 Ransomware entering through a phishing email | Security Lead | Universal multi-factor authentication; email filtering; immutable backups; tested response plan |
| R-004 Key-person dependency for integration knowledge | IT Manager | Document integrations; second engineer on each; retained support option |
| R-009 Backup restore not tested within 12 months | Infrastructure Lead | Restore test in the next recovery exercise |

## 9. Governance and review

The IT Manager reports progress monthly in the board IT report and reviews the roadmap quarterly with the executive team. Any change to a Now initiative with a cost impact above £10,000 or a delay of more than one month goes to the board as a decision. The strategy is re-issued each April.

## 10. Decisions requested

1. Approve the five strategic themes and guiding principles.
2. Endorse the Now initiatives and the FY2026/27 budget as the committed scope.
3. Note the Next and Later horizons as intent, to be confirmed through business cases.

## Appendix: prioritisation method

Each candidate initiative was scored 1 to 5 for business value, risk reduction, effort (5 is least effort) and urgency, and the four scores were summed. Ties were resolved by dependency order. The scoring table is kept with the working papers so that it can be challenged.
