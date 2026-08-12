"""Write reports without copying source text into them."""

import html
import json
from pathlib import Path
from typing import Any


def write_reports(result: dict[str, Any], output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "findings.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    rows = "".join(
        f"<tr><td>{html.escape(item['rule'].replace('_', ' ').title())}</td>"
        f"<td>{item['sentence'] or '—'}</td><td>{html.escape(str(item['detail']))}</td></tr>"
        for item in result["findings"]
    ) or "<tr><td colspan='3'>No rule-based findings</td></tr>"
    metrics = result["metrics"]
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>Plain-language review</title>
<style>body{{font:1rem/1.55 system-ui;max-width:60rem;margin:auto;padding:2rem;color:#17324d}}
.notice{{border-left:.4rem solid #ae6100;background:#fff4dd;padding:1rem}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #9dacb8;padding:.5rem;text-align:left}}</style></head><body><main>
<h1>Plain-language review</h1><p class="notice"><strong>Human review required.</strong>
{html.escape(result['notice'])}</p><p>{metrics['words']} words; {metrics['sentences']} sentences;
average {metrics['average_sentence_words']} words per sentence.</p><table><caption>Review prompts</caption>
<thead><tr><th scope="col">Rule</th><th scope="col">Sentence</th><th scope="col">Detail</th></tr></thead>
<tbody>{rows}</tbody></table><h2>Limits</h2><p>Rules can produce false positives and cannot judge
accuracy, tone, audience, disability access, translation quality, or necessary technical language.</p>
</main></body></html>"""
    (output / "report.html").write_text(document, encoding="utf-8")

