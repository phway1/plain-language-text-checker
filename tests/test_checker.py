import json

import pytest

from plaincheck.checker import analyze, load_rules


RULES = {"long_sentence_words": 5, "long_word_characters": 10,
         "jargon": {"utilize": "use", "in the event that": "if"}}


def test_load_rules(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text(json.dumps(RULES))
    assert load_rules(path) == RULES


@pytest.mark.parametrize("key,value", [("long_sentence_words", 0), ("long_word_characters", "12")])
def test_rejects_invalid_threshold(tmp_path, key, value):
    rules = dict(RULES)
    rules[key] = value
    path = tmp_path / "rules.json"
    path.write_text(json.dumps(rules))
    with pytest.raises(ValueError, match=key):
        load_rules(path)


def test_finds_long_sentence():
    result = analyze("One two three four five six.", RULES)
    assert {item["rule"] for item in result["findings"]} == {"long_sentence"}
    assert result["findings"][0]["sentence"] == 1


def test_finds_jargon_case_insensitively_and_counts():
    result = analyze("Utilize this. Do not utilize that.", RULES)
    jargon = next(item for item in result["findings"] if item["rule"] == "jargon")
    assert jargon["detail"] == "utilize → use"
    assert jargon["occurrences"] == 2


def test_finds_possible_passive_voice():
    result = analyze("The form was reviewed yesterday.", RULES)
    assert "possible_passive_voice" in {item["rule"] for item in result["findings"]}


def test_does_not_call_all_ed_words_passive():
    result = analyze("We reviewed the form.", RULES)
    assert "possible_passive_voice" not in {item["rule"] for item in result["findings"]}


def test_defined_acronym_is_not_flagged():
    result = analyze("An application programming interface (API) connects systems. API helps.", RULES)
    assert "unexplained_acronym" not in {item["rule"] for item in result["findings"]}


def test_unexplained_acronym_is_flagged_once():
    result = analyze("The API changed. API users know.", RULES)
    items = [item for item in result["findings"] if item["rule"] == "unexplained_acronym"]
    assert len(items) == 1 and items[0]["detail"] == "API"


def test_long_words_are_unique_and_normalized():
    result = analyze("Documentation needs DOCUMENTATION.", RULES)
    items = [item for item in result["findings"] if item["rule"] == "long_word"]
    assert len(items) == 1 and items[0]["detail"] == "documentation"


def test_empty_text_has_zero_metrics():
    result = analyze("", RULES)
    assert result["metrics"] == {"words": 0, "sentences": 0, "average_sentence_words": 0}
    assert result["findings"] == []


def test_metrics_are_descriptive_not_score():
    result = analyze("Short sentence. Another clear sentence.", RULES)
    assert result["metrics"]["sentences"] == 2
    assert "score" not in result
    assert "not a quality score" in result["notice"]

