## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: wordfreq に `--min-length N` を追加し、N文字未満を除外する。既定1の互換、help・試験を対象にし、READMEは変更しないlight計画のための調査。
- **Keywords Used**: wordfreq、CLI、Unicode、casefold、filter、boundary、frequency、top、HTML、pytest、regression、baseline、discrimination、検証、試験。title/tags/module/problem_typeの大文字小文字を区別しない検索と本文検索を並列実施。
- **Search Root**: このrepoの `docs/solutions/` のみ。実在カテゴリは `best-practices/` と `workflow-issues/`。
- **Files Scanned**: 学びMarkdown 5ファイルを検索し、候補5ファイルの先頭30行を確認。関連2ファイルのみ全文読了。`.gitkeep` とディレクトリは件数に含めない。
- **Relevant Matches**: 2ファイル（入力境界・決定論が強関連、判別力・状態基底が中関連）。最小文字数オプションを直接扱った学びは見つからない。
- **Grounding**: repo直下の `CONCEPTS.md` を読了。「既定トークナイザ」「決定論的順位」「試験の判別力」「純粋なHTML整形」を基準にした。
- `docs/solutions/patterns/critical-patterns.md` は探索結果に存在しない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: Unicode語の長さをどの段階で測るか、CJKの境界、フィルタ後の同率順位を変えないことに直結する。
- **Key Insight**: 語の切り出しとcasefoldを混同しない。既定はUnicode単語文字の最長連続で、CJKを文字単位に分解しない。決定論は複数のPYTHONHASHSEEDで実CLIを照合する。
- **Severity**: medium
- **日付・現状との差異**: 2026-11-17の記事。記事34行・55–57行の「同率はコードポイント昇順」は旧契約であり、現在には適用不可。`CONCEPTS.md:49–51` と `wordfreq/aggregator.py:11–17` は頻度降順・正規化後初出順の安定ソートを明示する。この記事のソート例をコピーすると回帰する。トークナイザ境界とcasefoldの記述は現在の `wordfreq/tokenizer.py:6–18` と一致する。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 既定1の互換を「新旧オプション両方が同じ出力だから」で済ませず、除外漏れ・境界の誤り・順序の誤りを検出できる試験にするための指針。Gitのステージ済み基底という話は読み取り専用試験を拡張する場合に限る。
- **Key Insight**: 判別力は失敗の種ごとに独立に示す。変異はcold scratchコピーだけに注入し、通常コードでの成功と、意図したアサーションによる変異検出を対にする。収集エラーや構文エラーを検出成功と数えない。
- **Severity**: medium
- **日付・現状との差異**: 2026-11-17の記事。`tests/test_cli.py:153–182` はcoldコピー、`git add -A` 後の比較、環境変数除去を現在も備える。`test_max_count_read_only` は `.gitignore` を無条件コピーする点が記事の条件付きコピー推奨と異なるため、無視規則欠落の判別力を調べる際は機械的に転用しない。今回、実repoでステージ操作は行わない。

### 現行コードから得た計画上の制約
- `wordfreq/__main__.py:13–29` に現時点で `--min-length` はない。`--min-count` の整数解析と入力取得前の正値チェックが近い既存例。`--max-count` は0・負数も有効という別契約なので、新しい下限オプションの検証にはそのまま流用しない。
- `wordfreq/__main__.py:35–40` は「正規化済み語を全件集計 → 元の総数算出 → min/max-count共通フィルタ → top」の順。最小文字数はこの共通選択部に追加する形が小さく、元Counter・総数を維持しやすい。これは現状に基づく推奨で、過去の学びが最小文字数仕様を決めているわけではない。
- 長さをcasefold後の語に対する `len(word)` とするかは計画で明記する必要がある。推奨は既存集計キーに合わせた正規化後のUnicodeコードポイント数。UTF-8バイト長や見た目の書記素数とは異なり、`ß` のようなcasefoldで長さが変わる入力が判別例となる。既存トークナイザや正規化規則そのものは変更しない。
- 同率順位はフィルタ後も初出順を保持する。長さ判定をtop後に行うと、短い高頻度語に枠を奪われたままになる。
- `format_html` は受け取ったpairsと元のtotalを整形するだけ（`wordfreq/formatters.py:22–27`）。文字数フィルタで全件除外しても元の総出現回数を渡し、既存の空結果表現を維持する。
- `tests/test_cli.py` に3形式共通の `run_cli_bytes` / `assert_output_bytes`、min/max-count選択・help・入力前エラー・保存済み出力baseline・scratch変異検出の既存例がある。現在のファイルを読んだ根拠であり、今回これらを実行して合格を確認したという意味ではない。

### Recommendations
- light計画では主な製品変更を `wordfreq/__main__.py` の引数・入力前検証・共通選択条件に限定し、既存試験ファイルで回帰を追加する。READMEの変更や、トークナイザ・ソート・HTML整形の改変を混ぜない。
- 省略と明示1の一致だけでなく、変更前に保存した実出力とのバイト比較を用意する。現行の保存済みmin/max-count baseline試験も回帰対象に含める。ただし既存baselineだけで今回の全要件を満たしたとは言わない。
- 試験は閾値ちょうど／未満／超過、casefoldで長さが変わる語、CJK・数字・下線、全件除外・空入力、min/max-countとのAND、top前選択、同率初出順、3形式共通、HTML元総数を優先する。helpは実CLIで確認する。Nの許容範囲は明文化し、正整数契約とするなら0・負数・非整数・引数欠落を入力取得前に拒否する。
- 判別力では「長さ条件無視」「境界を排他的にする」「casefold前の長さ」「top後除外」「HTML total再計算」「辞書順へ変更」を区別できる入力を用意する。既存max-countの変異試験には文字列置換による実装箇所への依存があるため、最小変更でも置換対象に当たらなくなる可能性を回帰で確認する。
- 実装前に関連2文書を読み、上記の旧順位契約の訂正を併読する。計画時は未作成の検証コマンドを試さない。PLANには実在を確認した試験ファイルを根拠とするコマンドを記し、Builder・品質が実行結果を取得する。今回GSD状態の判定はしていない。

### 関連なし・条件付きの候補
- `workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`：CI実行結果を受入条件にするときのみ隣接する。今回の最小文字数変更そのものの設計根拠にはしない。ローカル試験だけでCI成功を主張しない、という区別は維持する。
- `workflow-issues/pm-readable-evidence-delivery.md` と `workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md`：証拠配送・添付拒否に関する学びであり、今回のCLI変更・README不変light計画には直接の関連なし。先頭の適用条件を確認して除外し、全文は読んでいない。

### 調査の範囲
この調査はファイル読取り・検索のみで根拠を確認した。試験、未作成コマンド、GSD判定、commit/push/Kanban操作は実行していない。作成する成果物は本ファイルのみ。最小文字数に固有の学びは未収録なので、実装後に確定したUnicode長の契約と検証上の発見は将来の学び候補となる。
