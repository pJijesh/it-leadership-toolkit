import csv
import json

import pytest

import score_vendors as sv


def write_csv(path, header, rows):
    with open(path, "w", newline="") as handle:
        w = csv.writer(handle)
        w.writerow(header)
        w.writerows(rows)
    return path


def test_weighted_scores_simple():
    # Two criteria, equal weights: the weighted score is the plain average.
    totals = sv.weighted_scores([50, 50], [[4, 2], [2, 4]])
    assert totals == pytest.approx([3.0, 3.0])


def test_weighted_scores_respects_weights():
    totals = sv.weighted_scores([75, 25], [[5, 1], [1, 5]])
    assert totals == pytest.approx([4.0, 2.0])


def test_competition_ranks_with_ties():
    assert sv.competition_ranks([4.3, 3.55, 3.55, 3.0]) == [1, 2, 2, 4]


def test_example_ranking(root):
    rows = sv.score_scorecard(root / "04-vendor-scorecard" / "vendor-scorecard-example.csv")
    assert [r["vendor"] for r in rows] == ["Vendor B", "Vendor A", "Vendor C", "Vendor D"]
    assert [r["rank"] for r in rows] == [1, 2, 3, 4]
    assert rows[0]["weighted_score"] == pytest.approx(4.30)
    assert rows[1]["weighted_score"] == pytest.approx(3.55)
    assert rows[0]["percent_of_max"] == pytest.approx(0.86)


def test_tied_vendors_share_rank_in_input_order(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X", "Y", "Z"], [["a", 60, 3, 3, 5], ["b", 40, 3, 3, 1]])
    rows = sv.score_scorecard(path)
    assert [(r["vendor"], r["rank"]) for r in rows] == [("Z", 1), ("X", 2), ("Y", 2)]


def test_weights_must_sum_to_100(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X"], [["a", 60, 3], ["b", 30, 3]])
    with pytest.raises(sv.ScorecardError, match="sum to 100"):
        sv.score_scorecard(path)


def test_score_out_of_range_rejected(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X"], [["a", 100, 6]])
    with pytest.raises(sv.ScorecardError, match="outside"):
        sv.score_scorecard(path)


def test_negative_weight_rejected(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X"], [["a", 110, 3], ["b", -10, 3]])
    with pytest.raises(sv.ScorecardError, match="negative"):
        sv.score_scorecard(path)


def test_non_numeric_rejected(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X"], [["a", 100, "high"]])
    with pytest.raises(sv.ScorecardError, match="non-numeric"):
        sv.score_scorecard(path)


def test_bad_header_rejected(tmp_path):
    path = write_csv(tmp_path / "t.csv", ["name", "weight", "X"], [["a", 100, 3]])
    with pytest.raises(sv.ScorecardError, match="Header"):
        sv.score_scorecard(path)


def test_cli_table_and_json(root, capsys):
    csv_path = str(root / "04-vendor-scorecard" / "vendor-scorecard-example.csv")
    assert sv.main([csv_path]) == 0
    out = capsys.readouterr().out
    assert "Vendor B" in out and "4.300" in out
    assert sv.main([csv_path, "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["vendor"] == "Vendor B"


def test_cli_reports_errors(tmp_path, capsys):
    path = write_csv(tmp_path / "t.csv", ["criterion", "weight", "X"], [["a", 50, 3]])
    assert sv.main([str(path)]) == 1
    assert "Error" in capsys.readouterr().err
