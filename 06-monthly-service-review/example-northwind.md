# Service review: September 2026

**Northwind Freight (fictional).** A worked example with invented figures. Targets are examples.

**Chair:** Service Delivery Manager | **Attendees:** Service Desk Lead, Infrastructure Lead, Applications Lead, Change Manager, Operations Director (business representative) | **Period:** 1 to 30 September 2026

## 1. Summary

- Service was stable. One priority 1 incident, caused by a failed change to a network device, was restored in 3 hours 20 minutes.
- Resolution within SLA improved to 94% but remains below the 95% target. Misses cluster in the last week of the month when volume peaks.
- CSAT is 4.4, above target. The response rate is 26%, so treat the score as indicative.
- A recurring fault with handheld scanner connectivity at two sites has been raised as problem P-031.
- Decision needed: agree a change freeze for the last week of November and the first week of December, ahead of the peak trading period.

## 2. Service level performance

| Measure | Target (example) | This month | Last month | Six-month trend (Apr to Sep) | Status |
|---|---|---|---|---|---|
| Core service availability | 99.9% | 99.93% | 99.91% | 99.95, 99.97, 99.88, 99.99, 99.91, 99.93 | Green |
| Resolution within SLA | 95% | 94% | 93% | 92, 93, 91, 95, 93, 94 | Amber |
| Mean time to restore (P1 and P2) | 4 hours | 2 h 50 min | 3 h 40 min | 3 h 10, 3 h 30, 4 h 20, 2 h 40, 3 h 40, 2 h 50 | Green |
| First contact resolution | 70% | 68% | 66% | 64, 65, 63, 67, 66, 68 | Amber |

**SLA breaches by cause (34 tickets).** Waiting on a supplier: 13. Capacity at month end: 11. Misrouted to the wrong team: 6. Other: 4.

## 3. Incident management

| Month | Logged | P1 | P2 | P3 and P4 | Reopened |
|---|---:|---:|---:|---:|---:|
| Apr 2026 | 560 | 2 | 9 | 549 | 31 |
| May 2026 | 548 | 1 | 7 | 540 | 27 |
| Jun 2026 | 590 | 2 | 11 | 577 | 36 |
| Jul 2026 | 575 | 0 | 8 | 567 | 26 |
| Aug 2026 | 603 | 2 | 10 | 591 | 33 |
| Sep 2026 | 586 | 1 | 8 | 577 | 28 |

- **Major incident.** 9 September, 10:15 to 13:35. A failed firmware change on a core switch interrupted connectivity at the Northern depot. Cause: the change was tested on one switch model but deployed to two. Action recorded in section 8.
- **Top categories by volume.** Access and passwords (22%), handheld scanners (14%), email and collaboration (11%).
- **Backlog older than 30 days.** 9 tickets, against a target of 10 or fewer.

## 4. Problem management

| Problem ID | Description | Linked incidents | Status | Owner | Next step |
|---|---|---:|---|---|---|
| P-031 | Handheld scanners lose connection at two sites | 41 | Root cause analysis | Infrastructure Lead | Wireless survey booked for 14 October |
| P-029 | Month-end report timeouts in the core platform | 17 | Known error, workaround published | Applications Lead | Supplier fix due in the next release |
| P-027 | Password reset requests for one application | 23 | Fix in test | Service Desk Lead | Deploy self-service reset in October |

Three problems were opened and four were closed this month. Fourteen are open.

## 5. Change and release management

| Month | Changes | Standard | Normal | Emergency | Failed or rolled back | Success rate |
|---|---:|---:|---:|---:|---:|---:|
| Apr 2026 | 38 | 20 | 16 | 2 | 2 | 95% |
| May 2026 | 41 | 22 | 17 | 2 | 2 | 95% |
| Jun 2026 | 44 | 21 | 19 | 4 | 4 | 91% |
| Jul 2026 | 36 | 19 | 16 | 1 | 1 | 97% |
| Aug 2026 | 40 | 21 | 17 | 2 | 2 | 95% |
| Sep 2026 | 39 | 20 | 17 | 2 | 2 | 95% |

Emergency changes were 5% of the total in September, on the example limit. The failed switch change on 9 September led to a new rule: every device model in scope must be tested before a change is approved. Forward schedule: scanner firmware update (Oct), disaster recovery test (Nov).

## 6. Customer satisfaction

| Month | Surveys sent | Responses | Response rate | CSAT (1 to 5) |
|---|---:|---:|---:|---:|
| Apr 2026 | 560 | 148 | 26% | 4.2 |
| May 2026 | 548 | 139 | 25% | 4.3 |
| Jun 2026 | 590 | 150 | 25% | 4.2 |
| Jul 2026 | 575 | 160 | 28% | 4.4 |
| Aug 2026 | 603 | 152 | 25% | 4.3 |
| Sep 2026 | 586 | 151 | 26% | 4.4 |

*Positive:* "Fixed while I was still on the phone." *Positive:* "Clear updates throughout the outage." *Negative:* "Took three days to get a new scanner." *Negative:* "Had to explain the problem twice to different people."

Themes: users value speed and clear communication; hand-offs between teams are the main complaint, which matches the misrouting breach cause.

## 7. Suppliers

The managed service desk provider met its response SLA and missed resolution SLA on 13 tickets that were waiting on a third-party supplier. No service credits are due this month. The scanner hardware supplier is under weekly escalation for late delivery of the rollout stock.

## 8. Continual improvement register

| ID | Improvement | Source | Owner | Due | Status |
|---|---|---|---|---|---|
| CI-14 | Test every device model in scope before approving a network change | Major incident, 9 Sep | Change Manager | 30 Sep 2026 | Done |
| CI-15 | Add a routing rule so handheld scanner tickets go straight to the infrastructure queue | Misrouted tickets | Service Desk Lead | 15 Oct 2026 | In progress |
| CI-16 | Publish a self-service password reset for the main application | Problem P-027 | Service Desk Lead | 31 Oct 2026 | In progress |
| CI-17 | Add a temporary resource at month end to protect resolution SLA | SLA breach analysis | Service Desk Lead | 31 Oct 2026 | Proposed |

## 9. Decisions and asks

1. Agree a change freeze from 23 to 30 November and 1 to 7 December.
2. Agree to fund one temporary month-end resource within the current budget (CI-17).

## 10. Next month

Wireless survey (14 October). Scanner firmware update. Cloud optimisation findings to be shared. Reminder: the service desk contract notice date is approaching, see the [renewal checklist example](../10-supplier-contract-renewal/example-northwind.md).
