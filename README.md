# Plain-Language Text Checker

A small, local Python tool that turns transparent writing rules into review
prompts. It flags long sentences, unusually long words, configured jargon,
unexplained acronyms, and simple passive-voice indicators. It does not upload
text, use an AI service, or produce a simplistic quality score.

## Quick start

Python 3.10 or newer is required. The checker itself uses only the standard library.

```bash
git clone https://github.com/phway1/plain-language-text-checker.git
cd plain-language-text-checker
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make demo
```

Open `reports/report.html`; `reports/findings.json` supports further analysis.
The synthetic input is in `data/sample/synthetic_notice.txt`.

```bash
make lint
make test
```

Check another local UTF-8 text file:

```bash
PYTHONPATH=src python -m plaincheck.cli my-draft.txt --output reports
```

## Transparent rules

All thresholds and jargon replacements live in `config/rules.json`. A finding
states the rule, sentence number when relevant, and a short detail—not a hidden
score. The implementation uses documented regular expressions and word counts:

- a sentence is “long” only when it exceeds the configured word threshold;
- a long word exceeds the configured letter threshold;
- jargon matches whole configured phrases, case-insensitively;
- an acronym is two or more capitals and is considered explained when preceded
  by a phrase in parentheses form, such as `application programming interface (API)`;
- passive voice is only a possible indicator matching a form of “be” plus an
  `-ed` word. It is deliberately labeled for review, not asserted as fact.

## Privacy and responsible use

- Processing is local and requires no network. Source text is read into memory
  and is not copied into JSON or HTML reports. Findings may still reveal individual
  words or phrases; treat reports according to the source document's sensitivity.
- Avoid checking confidential, personal, legal, medical, or student records unless
  your organization has authorized the local environment and retention practice.
- This is not a measure of intelligence, literacy, professionalism, truth, or
  writing quality. Never use findings to grade, rank, discipline, or exclude people.
- Plain language depends on audience, purpose, language, culture, disability access,
  and subject matter. Necessary technical terms are not inherently bad.
- Regex sentence splitting, acronym detection, and passive indicators produce false
  positives and negatives. They handle English-like prose only and need human review.
- Shorter is not always clearer. Preserve accuracy, dignity, legal meaning, and the
  author's voice. Test revisions with intended readers and accessibility tools.

## Repository map

```text
config/rules.json                 editable rules and alternatives
data/sample/synthetic_notice.txt synthetic demo input
src/plaincheck/                  analysis, reports, CLI
tests/                           rules, limitations, privacy, CLI tests
.github/workflows/ci.yml         lint, tests, offline demo
```

## Possible next steps

- Add abbreviations, decimals, lists, and heading-aware sentence segmentation.
- Allow a project-specific approved terminology list.
- Add opt-in redacted context around findings.
- Co-design guidance with accessibility experts and multilingual readers.

## License

MIT. See [LICENSE](LICENSE).
