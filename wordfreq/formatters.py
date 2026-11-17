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


def _html_text(value: str) -> str:
    """Escape once, protecting CR from HTML's input newline normalization."""
    return escape(value, quote=True).replace("\r", "&#13;")


def format_html(pairs: list[tuple[str, int]], basename: str, total: int) -> str:
    """Render ordered pairs and caller-supplied metadata as escaped text only.

    No I/O, counting or sorting occurs here. The caller supplies a basename
    (never a full path) and the total before limiting the displayed pairs.
    """
    rows = "".join(
        f'<tr><td class="rank">{_html_text(str(rank))}</td>'
        f'<td class="word">{_html_text(word)}</td>'
        f'<td class="count">{_html_text(str(count))}</td></tr>\n'
        for rank, (word, count) in enumerate(pairs, 1)
    )
    empty = (
        '<p class="empty-message">集計対象の単語はありません。'
        '単語を含む UTF-8 ファイルで再実行してください。</p>\n'
        if not pairs else ""
    )
    return '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>単語の出現頻度</title>
<style>
:root { color-scheme: light; }
body {
  margin: 0;
  background: #FFFFFF;
  color: #0F172A;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
}
main {
  width: 100%;
  max-width: 960px;
  box-sizing: border-box;
  margin: 0 auto;
  padding: 32px;
}
h1 {
  margin: 0 0 16px;
  color: #1D4ED8;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.25;
  overflow-wrap: anywhere;
}
.metadata { margin: 0 0 24px; }
.metadata-item + .metadata-item { margin-top: 8px; }
.label, caption, th {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.5;
}
.label { margin-bottom: 4px; color: #475569; }
.filename-value, .word {
  white-space: break-spaces;
  overflow-wrap: anywhere;
  word-break: normal;
  tab-size: 4;
}
.total-value { color: #1D4ED8; }
table { width: 100%; table-layout: fixed; border-collapse: collapse; }
caption { text-align: left; color: #475569; margin-bottom: 8px; }
th, td {
  box-sizing: border-box;
  padding: 8px;
  vertical-align: top;
  text-align: left;
  overflow-wrap: anywhere;
  border-bottom: 1px solid #CBD5E1;
}
th { background: #F1F5F9; }
td { background: #FFFFFF; }
.rank, .count { text-align: right; font-variant-numeric: tabular-nums; }
.rank { width: 56px; }
.count { width: 64px; }
.empty-message { margin: 24px 0 0; color: #475569; overflow-wrap: anywhere; }
@media (max-width: 480px) { main { padding: 16px; } }
</style>
</head>
<body>
<main>
<h1>単語の出現頻度</h1>
<div class="metadata">
<div class="metadata-item">
<div class="label">ファイル名</div>
<div class="filename-value">''' + _html_text(basename) + '''</div>
</div>
<div class="metadata-item">
<div class="label">総出現回数</div>
<div class="total-value">''' + _html_text(str(total)) + '''</div>
</div>
</div>
<table>
<caption>集計結果</caption>
<thead><tr><th class="rank" scope="col">順位</th><th class="word" scope="col">単語</th><th class="count" scope="col">回数</th></tr></thead>
<tbody>
''' + rows + '''</tbody>
</table>
''' + empty + '''</main>
</body>
</html>
'''
