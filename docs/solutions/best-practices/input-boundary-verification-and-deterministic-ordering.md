---
title: "入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す"
date: 2026-11-17
category: best-practices
module: "wordfreq CLI (sources/tokenizer/aggregator/formatters)"
problem_type: best_practice
component: testing_framework
severity: medium
applies_when:
  - "テキスト入力を受け取り、トークン化して頻度を集計・並び替えし出力するCLIやパイプラインで、トークン化方針やその拡張点を扱う"
  - "「同一入力の再実行で同一出力」という決定論を出力に対して主張・検証する"
  - "出力の並び順が dict や set の反復順の影響を受け得る（同率タイbreakなど）"
tags: [determinism, tokenizer, input-boundary, pythonhashseed, total-order, codepoint-order, read-only-io, wordfreq]
---

# 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す

## Context

wordfreq CLI フェーズ1（カード r-5a3b8a3f、2026-11-17）では、入力境界の扱いをめぐる3つの摩擦が実際に出た。

1. **既定トークナイザの境界**: 既定は「Unicode の単語文字の最長列」であり、句読点・記号・空白を除外し casefold で正規化する（`wordfreq/tokenizer.py:6` の `_WORD_RE = re.compile(r"\w+", re.UNICODE)`、`wordfreq/tokenizer.py:14-18`）。仕様の読み方によっては「ASCII 空白・改行で分割」と誤記しやすく、実挙動（`\w+` の最長一致、`_` や数字を語の一部として保持、test_tokenizer.py:24-29）とは境界が違う。
2. **代替トークナイザへの差し替え境界**: 拡張点は `iter_tokens(text, tokenizer=...)` で、差し替えられるのはトークン化方針だけで、casefold 正規化・集計・並び替え・出力は変わらない（`wordfreq/tokenizer.py:14-18`、`tests/test_tokenizer.py:48-60`）。この層を明示しないと、差し替え先が正規化まで握り直して集計契約が崩れる。
3. **空白区切りのない文字列（CJK等）の境界**: CJK のように空白で囲まれていない文字列は既定境界では **語単位ではなく最長1トークン** になる（`tests/test_tokenizer.py:32-38` で「日本語のテキスト」が1トークンと固定）。文字粒度での分解は既定では起こらず、差し替え境界で方針を入れて初めて実現する。セッション側の「CJKは文字単位に分解される」という見立ては既定境界では成り立たず、このズレ自体が3層を分けて検証すべき理由になった。

別軸で、集計・整形層では同一頻度語の並び順が辞書反復順のぶれに飲まれる問題が実際に出た（同カード 実装01-02、t_61fb0c48）。並び順を全順序で確定させ、PYTHONHASHSEED を変えた再実行で決定論を証明する運用で解消した。読み取り層は「読み取り専用」を宣言するだけでなく、バイト不変と改行方針をテストで固定する必要がある。

## Guidance

1. **入力境界は3層に分けて、それぞれに試験を当てる。**
   - (a) 既定トークナイザの境界: 何をもって語とするか（本ツリーでは Unicode 単語文字の最長列 + casefold）を正順・境界例（句読点、記号、`_`、数字、空文字列）で固定する。
   - (b) 差し替え境界: 代替トークナイザを注入しても「返り値がそのまま集計に入り、casefold 正規化だけが残る」ことを試験で固定する（`tests/test_tokenizer.py:48-60`）。差し替えられるのはトークン化方針のみ、という契約を明文化する。
   - (c) 空白区切りのない文字列の境界: CJK 連なりが既定でどう見えるか（1トークンになること、repeat しても同じこと）を固定し、文字粒度が必要なら (b) の方針として提供する。既定挙動への期待と実挙動のズレは、ここでしか露出しない。
2. **並び順は全順序で確定させる。** 比較キーを `(頻度降順, 語のコードポイント昇順)` のように全順序にし、ソートで確定する。dict/set の反復順や stable ソートの元順に依存した「たまたま同じ」を排除する（`wordfreq/aggregator.py:13` の `sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))`、`tests/test_aggregator.py:17-23` で同率5の apple→zoo を固定）。
3. **決定論の主張は「PYTHONHASHSEED を変えた再実行」で証明する。** 単一シードの再実行はハッシュ順が同一の範囲でしか無い。少なくとも 1 / 42 / 99 など複数シードで pytest と実CLI出力の一致まで示す。フェーズ検証の実測記録（`.planning/argonauts/t_3dc4a405/cli-evidence.md:79-80`: PYTHONHASHSEED 1/99 で text 出力 md5 一致、PYTHONHASHSEED=42 でも 43 passed）に加え、本キャプチャ実施時（2026-11-17、HEAD マージ後ツリー）でも PYTHONHASHSEED を 1/42/99 で変えた実CLI出力の md5 一致と、seed 1・99 での 43 passed を再実測した。
4. **読み取り層は「読み取り専用」と「改行方針」を明示して固定する。** `FileSource.read_text` は入力ファイルのバイト列を変えないことをテストで固定する（`tests/test_sources.py:16-17` の read前後の `read_bytes()` 一致、`tests/test_cli.py:152` の CLI 実行後も worktree・入力不変）。改行変換の可否は境界仕様として決める必要がある: 現行実装は `open(..., "r", encoding="utf-8")`（`wordfreq/sources.py:19`）でユニバーサル改行が有効なので、CRLF・CR はトークナイザに届く前に LF 正規化される。本キャプチャ時点のテストは `\n` のみで CRLF を固定していないため、改行方針を変更・確定させるときはそこにテストを足す。

## Why This Matters

- 並び順が反復順に依存すると、出力は PYTHONHASHSEED のたびに変わり得る。「2回実行して同じだった」は構造的不変の証明ではなく、シードを変えた再実行だけが「再現」を「不変」に格上げする。品質レビューでも実フェーズ検証でも、この証明手順が合格判定の根拠になった。
- 3層を分けないと、既定トークナイザの副作用として CJK が1トークンになる事実が仕様と認識の両方で見逃される。CJK の粒度は既定境界の属性ではなく差し替え境界で選べる方針であり、この区別がないと「CJKが文字単位で数えられるはず」という誤った前提で仕様・試験が組まれる。
- 読み取り専用性は宣言ではなく検証対象で、バイト不変と改行方針の両方をテストで初めて他者が信用できる。

## When to Apply

- テキストやレコード集を入力に取って集計・順位付けして出力するツールを作り、トークナイズ方針の既定値と拡張点を決めるとき。
- 出力の決定論を要求・主張・検証するとき、または同じはずの出力が環境差でぶれたと報告されたとき。
- 非ASCII（CJK 等）を扱う入力で、粒度の期待を仕様側と実装側がそれぞれの認識で書いているとき。

## Examples

順序の全順序化（本ツリーの実装）:

```python
# wordfreq/aggregator.py:13 — 頻度降順、同一頻度は語のコードポイント昇順
def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]
```

差し替え境界（方針だけを差し替え、正規化・集計・出力は変わらない）:

```python
# wordfreq/tokenizer.py:14-18
def iter_tokens(
    text: str, tokenizer: Callable[[str], list[str]] = default_tokenizer
) -> Iterator[str]:
    return (token.casefold() for token in tokenizer(text))
```

決定論の証明（単一再実行ではなくシードを振る）:

```bash
for seed in 1 42 99; do PYTHONHASHSEED=$seed python3 -m wordfreq input.txt | md5sum; done
# 2026-11-17 実測: 3 seed で md5 一致（828dba48f33178eceda8718042c778bf）
```

CJK の既定挙動の固定（1トークンであることを試験で宣言する）:

```python
# tests/test_tokenizer.py:32-38
text = "日本語のテキスト。東京、ひらがな"
expected = ["日本語のテキスト", "東京", "ひらがな"]  # 文字単位分解ではない
assert list(iter_tokens(text)) == expected
```

## Related

- [docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md](../workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md) — 同じフェーズ1（カード r-5a3b8a3f）からの別教訓。証拠の種類と検証対象headの区別がテーマで、本記事の「シードを変えた再実行で証明」という証拠手順の要求とも整合する。
- `.planning/argonauts/t_3dc4a405/cli-evidence.md` — 実CLI 17 Invocation と PYTHONHASHSEED 1/99 md5 一致の実測記録（カード実記録）。
