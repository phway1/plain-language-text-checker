import json

from plaincheck.cli import main


def test_cli_runs_locally(tmp_path, capsys):
    source = tmp_path / "private.txt"
    source.write_text("Please utilize the confidential banana.")
    rules = tmp_path / "rules.json"
    rules.write_text(json.dumps({"long_sentence_words": 20, "long_word_characters": 20,
                                 "jargon": {"utilize": "use"}}))
    output = tmp_path / "reports"
    assert main([str(source), "--rules", str(rules), "--output", str(output)]) == 0
    assert "not copied" in capsys.readouterr().out
    reports = (output / "findings.json").read_text() + (output / "report.html").read_text()
    assert "confidential banana" not in reports

