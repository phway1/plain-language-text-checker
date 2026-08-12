"""Rule-based text checks; findings are prompts for human review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

WORD_RE = re.compile(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)*\b")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?", re.MULTILINE)
ACRONYM_RE = re.compile(r"\b[A-Z]{2,}\b")
PASSIVE_RE = re.compile(r"\b(?:am|is|are|was|were|be|been|being)\s+([a-z]+ed)\b", re.I)


def load_rules(path: str | Path) -> dict[str, Any]:
    rules = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("long_sentence_words", "long_word_characters"):
        if not isinstance(rules.get(key), int) or rules[key] < 1:
            raise ValueError(f"{key} must be a positive integer")
    jargon = rules.get("jargon")
    if not isinstance(jargon, dict) or any(not k.strip() or not v.strip() for k, v in jargon.items()):
        raise ValueError("jargon must map non-empty phrases to alternatives")
    return rules


def _sentences(text: str) -> list[str]:
    return [match.group().strip() for match in SENTENCE_RE.finditer(text) if match.group().strip()]


def analyze(text: str, rules: dict[str, Any]) -> dict[str, Any]:
    sentences = _sentences(text)
    words = WORD_RE.findall(text)
    findings: list[dict[str, Any]] = []
    for number, sentence in enumerate(sentences, start=1):
        count = len(WORD_RE.findall(sentence))
        if count > rules["long_sentence_words"]:
            findings.append({"rule": "long_sentence", "sentence": number, "detail": f"{count} words"})
        if PASSIVE_RE.search(sentence):
            findings.append({"rule": "possible_passive_voice", "sentence": number,
                             "detail": "Review the be + -ed construction"})
    lowered = text.lower()
    for phrase, alternative in sorted(rules["jargon"].items()):
        occurrences = len(re.findall(rf"\b{re.escape(phrase.lower())}\b", lowered))
        if occurrences:
            findings.append({"rule": "jargon", "sentence": None,
                             "detail": f"{phrase} → {alternative}", "occurrences": occurrences})
    long_words = sorted({word.lower() for word in words if len(word.replace("-", "")) > rules["long_word_characters"]})
    for word in long_words:
        findings.append({"rule": "long_word", "sentence": None, "detail": word})

    definitions = {match.group(2) for match in re.finditer(r"\b([A-Za-z][A-Za-z ]{2,})\s+\(([A-Z]{2,})\)", text)}
    acronyms = sorted(set(ACRONYM_RE.findall(text)) - definitions)
    for acronym in acronyms:
        findings.append({"rule": "unexplained_acronym", "sentence": None, "detail": acronym})
    sentence_lengths = [len(WORD_RE.findall(sentence)) for sentence in sentences]
    return {
        "metrics": {"words": len(words), "sentences": len(sentences),
                    "average_sentence_words": round(sum(sentence_lengths) / len(sentences), 1) if sentences else 0},
        "findings": findings,
        "notice": "Automated prompts for human review, not a quality score.",
    }

