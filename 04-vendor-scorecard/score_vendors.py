#!/usr/bin/env python3
"""Weighted vendor scoring, the Python twin of vendor-scorecard.xlsx.

It reads a CSV with this layout (see vendor-scorecard-example.csv):

    criterion,weight,Vendor A,Vendor B,...
    Service quality and SLA commitments,25,4,5,...

and applies the same arithmetic as the workbook formulas:

    weighted score = SUMPRODUCT(weights, scores) / SUM(weights)     (0 to 5)
    percent of maximum = weighted score / 5
    rank = competition ranking, highest score first (ties share a rank)

Usage:
    python score_vendors.py vendor-scorecard-example.csv
    python score_vendors.py vendor-scorecard-example.csv --json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

SCORE_MIN = 0.0
SCORE_MAX = 5.0
WEIGHT_TOLERANCE = 1e-6


class ScorecardError(ValueError):
    """Raised when the input is not a valid scorecard."""


def load_scorecard(path: str | Path) -> tuple[list[str], list[float], list[str], list[list[float]]]:
    """Return (criteria, weights, vendors, scores[criterion][vendor])."""
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if not header or header[:2] != ["criterion", "weight"] or len(header) < 3:
            raise ScorecardError("Header must start with 'criterion,weight' followed by at least one vendor.")
        vendors = [v.strip() for v in header[2:]]
        criteria: list[str] = []
        weights: list[float] = []
        scores: list[list[float]] = []
        for line_no, row in enumerate(reader, start=2):
            if not any(cell.strip() for cell in row):
                continue
            if len(row) != len(header):
                raise ScorecardError(f"Line {line_no}: expected {len(header)} columns, found {len(row)}.")
            criteria.append(row[0].strip())
            try:
                weights.append(float(row[1]))
                scores.append([float(cell) for cell in row[2:]])
            except ValueError as exc:
                raise ScorecardError(f"Line {line_no}: non-numeric weight or score ({exc}).") from exc
    if not criteria:
        raise ScorecardError("No criteria found.")
    return criteria, weights, vendors, scores


def validate(weights: list[float], scores: list[list[float]]) -> None:
    """Raise ScorecardError if weights do not sum to 100 or a score is out of range."""
    if any(w < 0 for w in weights):
        raise ScorecardError("Weights must not be negative.")
    total = sum(weights)
    if abs(total - 100.0) > WEIGHT_TOLERANCE:
        raise ScorecardError(f"Weights must sum to 100, but they sum to {total:g}.")
    for row in scores:
        for value in row:
            if not SCORE_MIN <= value <= SCORE_MAX:
                raise ScorecardError(f"Score {value:g} is outside {SCORE_MIN:g} to {SCORE_MAX:g}.")


def weighted_scores(weights: list[float], scores: list[list[float]]) -> list[float]:
    """Weighted score per vendor on the 0 to 5 scale."""
    total_weight = sum(weights)
    vendor_count = len(scores[0])
    return [
        sum(weights[i] * scores[i][v] for i in range(len(weights))) / total_weight
        for v in range(vendor_count)
    ]


def competition_ranks(values: list[float]) -> list[int]:
    """Rank 1 is the highest value. Equal values share a rank (1, 2, 2, 4), like Excel RANK."""
    return [1 + sum(1 for other in values if other > value) for value in values]


def score_scorecard(path: str | Path) -> list[dict]:
    """Load, validate and score a scorecard. Returns rows ordered by rank then input order."""
    _criteria, weights, vendors, scores = load_scorecard(path)
    validate(weights, scores)
    totals = weighted_scores(weights, scores)
    ranks = competition_ranks(totals)
    rows = [
        {
            "vendor": vendors[i],
            "weighted_score": totals[i],
            "percent_of_max": totals[i] / SCORE_MAX,
            "rank": ranks[i],
        }
        for i in range(len(vendors))
    ]
    return sorted(rows, key=lambda r: (r["rank"], vendors.index(r["vendor"])))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rank vendors from a weighted scorecard CSV.")
    parser.add_argument("csv_path", help="Path to the scorecard CSV")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a table")
    args = parser.parse_args(argv)
    try:
        rows = score_scorecard(args.csv_path)
    except (ScorecardError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(f"{'Rank':<6}{'Vendor':<20}{'Weighted score (0-5)':<24}{'% of max'}")
        for row in rows:
            print(f"{row['rank']:<6}{row['vendor']:<20}{row['weighted_score']:<24.3f}{row['percent_of_max']:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
