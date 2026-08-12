import json

from plaincheck.reporting import write_reports


def result():
    return {"metrics": {"words": 2, "sentences": 1, "average_sentence_words": 2},
            "findings": [{"rule": "jargon", "sentence": None, "detail": "utilize → use"}],
            "notice": "Automated prompts for human review, not a quality score."}


def test_writes_json_and_accessible_html(tmp_path):
    write_reports(result(), tmp_path)
    assert json.loads((tmp_path / "findings.json").read_text())["metrics"]["words"] == 2
    report = (tmp_path / "report.html").read_text()
    assert '<html lang="en">' in report
    assert 'scope="col"' in report
    assert "Human review required" in report


def test_reports_contain_no_source_text_field(tmp_path):
    write_reports(result(), tmp_path)
    combined = (tmp_path / "findings.json").read_text() + (tmp_path / "report.html").read_text()
    assert '"text"' not in combined
    assert '"source"' not in combined

