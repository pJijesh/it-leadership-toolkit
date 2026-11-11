# Risk register: worked example

A fictional register for Northwind Freight (fictional). The IDs and scores match the top risks shown in the [example board report](../02-board-it-report/example-northwind-board-report.md). Data file: [risk-register-example.csv](risk-register-example.csv).

Scoring bands used here are examples: 1 to 4 Low, 5 to 9 Medium, 10 to 14 High, 15 to 25 Critical.

| ID | Risk | Category | L | I | Score | Rating | Owner | Status | Next review | Trend |
|---|---|---|---:|---:|---:|---|---|---|---|---|
| R-002 | Ransomware entering through a phishing email | Security | 3 | 5 | 15 | Critical | Security Lead | Open | 2026-10-31 | Stable |
| R-001 | Cloud hosting cost grows faster than forecast | Financial | 4 | 3 | 12 | High | IT Manager | Open | 2026-11-15 | Rising |
| R-004 | Key-person dependency for integration knowledge | People | 3 | 4 | 12 | High | IT Manager | Open | 2026-12-15 | Stable |
| R-009 | Backup restore not tested within the last 12 months | Resilience | 3 | 4 | 12 | High | Infrastructure Lead | Open | 2026-11-15 | Stable |
| R-003 | Core operations platform outage in a peak period | Operational | 2 | 5 | 10 | High | Applications Lead | Open | 2026-11-30 | Stable |
| R-006 | Unsupported operating systems on legacy devices | Technology | 3 | 3 | 9 | Medium | Service Desk Lead | Open | 2026-12-01 | Falling |
| R-007 | Service desk contract ends before replacement is live | Commercial | 2 | 4 | 8 | Medium | IT Manager | Open | 2026-11-15 | Stable |
| R-008 | Personal data shared through misconfigured access | Compliance | 2 | 4 | 8 | Medium | Security Lead | Open | 2026-12-15 | Stable |
| R-005 | Supplier delays warehouse scanner delivery again | Project | 3 | 2 | 6 | Medium | Project Manager | Open | 2026-10-31 | Falling |
| R-010 | Single-source scanning software supplier fails | Commercial | 1 | 4 | 4 | Low | Applications Lead | Accepted | 2027-03-31 | Stable |

## Mitigation actions

- **R-002 Ransomware entering through a phishing email.** A user opens a malicious email, malware spreads and operations stop, causing loss of service and data and a possible regulatory notification. *Mitigation:* Extend multi-factor authentication to 100 percent of accounts; email filtering; immutable backups; quarterly phishing exercises; tested incident plan.
- **R-001 Cloud hosting cost grows faster than forecast.** Usage growth in the core platform raises monthly hosting cost above budget, leading to a full-year overspend. *Mitigation:* Complete the cost optimisation review; set budget alerts; evaluate reserved capacity; report monthly variance.
- **R-004 Key-person dependency for integration knowledge.** Two people hold most knowledge of system integrations. Absence or departure would slow fixes and projects. *Mitigation:* Document integrations; pair a second engineer on each; add a retained support partner option.
- **R-009 Backup restore not tested within the last 12 months.** Backups exist but a full restore has not been proven, so recovery time after a major failure is uncertain. *Mitigation:* Schedule a restore test in the next disaster recovery exercise; record the measured recovery time.
- **R-003 Core operations platform outage in a peak period.** A failure or failed change takes the platform offline during a busy period, delaying shipments and customer service. *Mitigation:* Change freeze in peak weeks; tested rollback plans; supplier escalation route; annual disaster recovery test.
- **R-006 Unsupported operating systems on legacy devices.** Devices that no longer receive vendor security updates remain in use and become an entry point for attack. *Mitigation:* Asset review; replace through the device refresh budget; isolate any exception on a restricted network.
- **R-007 Service desk contract ends before replacement is live.** Re-tender and transition take longer than planned, leaving a gap in service or forcing a poor-value extension. *Mitigation:* Agree a short extension option in writing; start transition planning before contract award.
- **R-008 Personal data shared through misconfigured access.** A sharing setting exposes files containing personal data to people who should not see them. *Mitigation:* Quarterly access review; default-private sharing policy; data loss prevention alerts.
- **R-005 Supplier delays warehouse scanner delivery again.** A second hardware delay would push the rollout beyond December and into the peak period. *Mitigation:* Weekly supplier call; agreed delivery date in writing; fallback of phased site go-live.
- **R-010 Single-source scanning software supplier fails.** The supplier of the scanning application becomes insolvent or withdraws the product. *Mitigation:* Escrow or code access arrangement; annual supplier financial check; documented exit plan.
