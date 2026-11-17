"""Pure output formatting; callers own writing and exit decisions."""
import json
from html import escape


def format_text(pairs: list[tuple[str, int]]) -> str:
    """Format count-first tab-separated lines, or nothing for no pairs."""
    return "".join(f"{count}\t{word}\n" for word, count in pairs)


def format_json(pairs: list[tuple[str, int]]) -> str:
    """Format ordered word/count objects as one ASCII-safe JSON line."""
    items = [{"word": word, "count": count} for word, count in pairs]
    return json.dumps(items, ensure_ascii=True) + "\n"


def _escape_html_text(value: str) -> str:
    """Escape one text node, preserving CR through HTML newline processing."""
    return escape(value, quote=True).replace("\r", "&#13;")


def format_html(pairs: list[tuple[str, int]], *, filename: str, total_count: int) -> str:
    """Render selected rows, a display basename and pre-top total without I/O.

    Callers select/order pairs and supply metadata; this function neither reads
    nor aggregates input. Save UTF-8 output to a different file from the input.
    Names and words remain in the saved report: check them before sharing.
    """
    rows = "".join(
        f'<tr><td>{rank}</td><td class="word">{_escape_html_text(word)}</td><td>{count}</td></tr>\n'
        for rank, (word, count) in enumerate(pairs, start=1)
    )
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>wordfreq 集計結果</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #FFFFFF; color: #0F172A; font: 400 16px/1.5 system-ui, sans-serif; }}
main {{ width: 100%; max-width: 960px; margin: 0 auto; padding: 24px 16px; }}
h1 {{ margin: 0 0 16px; color: #1E40AF; font-size: 24px; font-weight: 600; line-height: 1.2; overflow-wrap: anywhere; }}
.metadata {{ margin: 0 0 24px; }}
.metadata p {{ margin: 0; }}
.metadata p + p {{ margin-top: 8px; }}
.label {{ display: block; margin-bottom: 4px; color: #475569; font-size: 14px; font-weight: 600; }}
.value {{ display: block; width: 100%; min-width: 0; }}
.value, .word {{ white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal; }}
table {{ width: 100%; table-layout: fixed; border-collapse: collapse; border: 1px solid #CBD5E1; }}
col.rank, col.count {{ width: 20%; }}
col.word {{ width: 60%; }}
thead {{ background: #F1F5F9; }}
th, td {{ padding: 8px; vertical-align: top; text-align: right; border-bottom: 1px solid #CBD5E1; overflow-wrap: anywhere; font-variant-numeric: tabular-nums; }}
th {{ font-size: 14px; font-weight: 600; }}
th:nth-child(2), td:nth-child(2) {{ text-align: left; }}
</style>
</head>
<body>
<main>
<h1>wordfreq 集計結果</h1>
<div class="metadata">
<p><span class="label">入力ファイル:</span><span class="value" id="filename">{_escape_html_text(filename)}</span></p>
<p><span class="label">総出現数:</span><span class="value" id="total-count">{total_count}</span></p>
</div>
<table aria-label="単語の出現頻度">
<colgroup><col class="rank"><col class="word"><col class="count"></colgroup>
<thead><tr><th scope="col">順位</th><th scope="col">単語</th><th scope="col">回数</th></tr></thead>
<tbody>
{rows}</tbody>
</table>
</main>
</body>
</html>
'''
