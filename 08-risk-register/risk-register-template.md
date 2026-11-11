# IT risk register: template

## How to use this template

**Purpose.** A living list of the technology risks that could stop the organisation meeting its objectives, each with an owner, a score and actions. It is the evidence that risk is managed, not just discussed.

Files: [risk-register-template.csv](risk-register-template.csv) (blank, with one guidance row to delete) and a worked example in [risk-register-example.md](risk-register-example.md) and [risk-register-example.csv](risk-register-example.csv).

## Writing a good risk

Use this form: **Because of [cause], [event] may happen, leading to [impact].**

- Describe something that could happen, not something that already has. A risk that has happened is an issue and goes in the issue log.
- Be specific enough that the owner knows what to do. "Cyber risk" is a category, not a risk.
- Name one accountable owner, a role or a person, not a team.

## Scoring

Score likelihood and impact from 1 to 5 and multiply. Agree the definitions in advance so scores mean the same thing every time.

| Score | Likelihood | Impact (example descriptors, adapt to your organisation) |
|---|---|---|
| 1 | Rare | Negligible: no visible effect |
| 2 | Unlikely | Minor: short disruption, absorbed within the team |
| 3 | Possible | Moderate: noticeable disruption or cost, management action needed |
| 4 | Likely | Major: significant disruption, financial or regulatory consequence |
| 5 | Almost certain | Severe: sustained loss of service, serious harm or regulatory action |

Scoring matrix (likelihood across, impact down). Bands are examples.

| Impact \ Likelihood | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 Medium | 10 High | 15 Critical | 20 Critical | 25 Critical |
| **4** | 4 Low | 8 Medium | 12 High | 16 Critical | 20 Critical |
| **3** | 3 Low | 6 Medium | 9 Medium | 12 High | 15 Critical |
| **2** | 2 Low | 4 Low | 6 Medium | 8 Medium | 10 High |
| **1** | 1 Low | 2 Low | 3 Low | 4 Low | 5 Medium |

Bands: 1 to 4 Low, 5 to 9 Medium, 10 to 14 High, 15 to 25 Critical.

## Columns

| Column | Meaning |
|---|---|
| id | Unique reference, never reused |
| date_raised | Date first logged |
| title | Short name |
| category | For example Security, Financial, Operational, People, Project, Commercial, Compliance, Technology |
| description | Cause, event and impact in one or two sentences |
| likelihood, impact | 1 to 5, as defined above |
| score | likelihood x impact |
| rating | Band from the score |
| owner | Accountable person or role |
| mitigation | Actions that reduce likelihood or impact, with dates |
| status | Open, Mitigating, Accepted or Closed |
| next_review | Date of next review |
| trend | Rising, Stable or Falling since the last review |

## Responding to a risk

Choose one response and record it: **treat** (reduce likelihood or impact), **tolerate** (accept it, with the owner's and the sponsor's agreement), **transfer** (insurance or contract) or **terminate** (stop the activity). Accepted risks still need a review date.

## Routine

- Review every Critical and High risk monthly and the rest quarterly.
- Report the top risks, with trend, in the [board report](../02-board-it-report/template.md).
- Add risks from incidents, audits, projects and supplier changes as they arise.
- Record residual risk after mitigation if your organisation uses it. Add two columns for residual likelihood and impact.
- Close a risk with a note saying why, rather than deleting it.
