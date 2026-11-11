# Asset lifecycle plan: FY2026/27 to FY2028/29

**Northwind Freight (fictional).** A worked example. Quantities, lives and costs are invented, and the target lives are illustrations, not recommendations.

**Owner:** Service Desk Lead | **Version:** 1.0, November 2026 | **Review date:** April 2027

## 1. Scope and asset classes

Laptops, handheld scanners, mobile phones, network switches and wireless access points, servers and on-premises storage, and printers across five sites. Software licences are covered by the contract register and are out of scope here.

## 2. Lifecycle stages and responsibilities

| Stage | What happens | Responsible |
|---|---|---|
| Plan | Annual refresh list agreed with finance in February | IT Manager |
| Procure | Purchase from approved suppliers with three-year warranty on laptops | Service Desk Lead |
| Deploy | Standard image, asset tag, inventory entry, user sign-off | Service Desk team |
| Operate | Monitoring and monthly patching | Infrastructure Lead |
| Maintain | Repairs logged; warranty claims tracked | Service Desk team |
| Refresh | Replace when a trigger is met | Service Desk Lead |
| Retire | Access removed, data wiped, certificate retained, device recycled or reused | Service Desk Lead |

## 3. Policy by asset class

| Asset class | Units | Target life (years, example) | Refresh triggers | Warranty / support | Disposal route |
|---|---:|---:|---|---|---|
| Laptops | 320 | 4 | Age, vendor support end, battery or repair cost, failed security baseline | 3-year warranty, extend to 4 | Wipe, certificate, authorised recycler |
| Handheld scanners | 60 | 4 | Age, repair rate, vendor support end | Supplier warranty plus support contract | Return to supplier or authorised recycler |
| Mobile phones | 90 | 3 | Vendor security update end, damage | Insurance | Wipe, trade-in or recycle |
| Network switches and access points | 70 | 6 | Vendor support end, capacity | Support contract | Authorised recycler |
| Servers and storage | 12 | 5 | Vendor support end, capacity, failure history | Support contract | Wipe media, destroy drives, certificate |
| Printers | 14 | 6 | Repair cost, supplier end of service | Supplier contract | Supplier take-back |

## 4. Inventory and data quality

The inventory is held in the service management tool and reconciled to the endpoint management and network discovery lists each quarter. Required fields: asset ID, class, model, serial number, user or location, purchase date, warranty end, vendor support end, cost, status. An annual physical audit of 10 percent of assets checks accuracy.

## 5. Refresh schedule and budget profile

Laptops are the largest recurring item. A fleet of 320 on a four-year life means 80 replaced a year. At an example unit cost of £900, that is £72,000 a year, which matches the end-user device replacement line in the [budget tracker](../05-it-budget-tracker/).

| Asset class | Units to refresh (3 years) | Unit cost (£, example) | Cost (£) | FY2026/27 | FY2027/28 | FY2028/29 |
|---|---:|---:|---:|---:|---:|---:|
| Laptops | 240 | 900 | 216,000 | 72,000 | 72,000 | 72,000 |
| Network switches and access points | 35 | 2,400 | 84,000 | 84,000 | 0 | 0 |
| Mobile phones | 90 | 500 | 45,000 | 0 | 22,500 | 22,500 |
| **Total** | **365** | | **345,000** | **156,000** | **94,500** | **94,500** |

The FY2026/27 network figure of £84,000 matches the server and network hardware line in the budget. Handheld scanners are being replaced as part of the warehouse scanning project and are funded there. Servers and printers have no scheduled refresh in the period. The costs are CapEx where they exceed the company's capitalisation threshold, and otherwise OpEx.

## 6. Security requirements

Devices must run an operating system and firmware that the vendor still supports with security updates, use full-disk encryption and be managed by endpoint tooling. Assets past vendor support are listed as exceptions, isolated on a restricted network and replaced within six months. See risk R-006.

## 7. Secure disposal and environmental duties

Storage media are wiped to an agreed standard, or destroyed where wiping is not possible, and the evidence is kept with the asset record. Disposal goes only to an authorised provider that issues a certificate. Electrical waste is handled under the regulations that apply to the company. Devices in good condition may be reused internally before disposal.

## 8. Measures

| Measure | Definition | Target (example) |
|---|---|---|
| Fleet within target life | Assets younger than target life / all assets | 90% or more |
| Assets past vendor support | Count of assets no longer supported | 0 |
| Inventory accuracy | Assets found at audit that match the record / assets audited | 98% or more |
| Disposals with certificate | Disposals with sanitisation evidence / all disposals | 100% |

## 9. Risks and exceptions

| Exception | Reason | Risk | Owner | Review |
|---|---|---|---|---|
| 21 laptops past target life | Delayed by project priorities | Unsupported operating system on some | Service Desk Lead | Monthly until replaced |
| Two older switches at the Southern depot | Replacement scheduled with depot refit | Out of vendor support | Infrastructure Lead | Quarterly |

## 10. Review

Reviewed each April with finance. The review reports units replaced, spend against plan, exceptions closed and any change to target lives based on failure and repair history.
