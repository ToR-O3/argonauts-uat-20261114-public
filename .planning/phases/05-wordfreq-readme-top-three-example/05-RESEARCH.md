# Phase 5: wordfreq README top three example - Research

**調査日:** 2026-11-24 (JST)  
**領域:** README の CLI 実行例と動作検証  
**確度:** HIGH（承認資料・現行ソース・既存試験の読取り。対象行の実行結果は未採取）

<user_constraints>

## User Constraints (from CONTEXT.md)

[VERIFIED: .planning/phases/05-wordfreq-readme-top-three-example/05-CONTEXT.md:14-22,46-48]
<!-- DATA_80989279_START -->

### Locked Decisions

- D-01: `README.md` の「wordfreq の実行」の既存 `sh` ブロック内、`--top 2` のJSON例の直後に `python -m wordfreq input.txt --top 3 --format json` をちょうど1行追加。
- D-02: 実装前後コミットを比較し、製品変更は README の追加1行・削除0行のみ。既存の実行例・説明・フェンス・プログラム・試験・依存・設定・連携は変更しない。
- D-03: 掲載行から `input.txt` だけを一時UTF-8入力のパスに置換し、リポジトリ直下で実行。入力は `delta gamma beta alpha beta gamma alpha beta alpha alpha`。終了0、JSONは `alpha:4`、`beta:3`、`gamma:2` の順で3件。既存 `input.txt` は保存・上書きしない。一時入力はコミットしない。

### Claude's Discretion

一時入力と平文検証証拠の作成方法。既存試験は変えず、検証手順の原本は必要なら `.planning/` 内で製品差分と分離する。

### Deferred Ideas (OUT OF SCOPE)

なし。CLIの変更やHTMLの変更は範囲外。
<!-- DATA_80989279_END -->

</user_constraints>

## Summary

**推奨:** 「wordfreq の実行」の既存 `sh` ブロックに、`python -m wordfreq input.txt --top 2 --format json` の直後の1行だけを追加する。次行の `python -m wordfreq input.txt --format html` を含め、既存行はそのまま残す。画面・HTML・CLI の変更は不要。 [VERIFIED: README.md:5-15; .planning/ROADMAP.md:122-131; openspec/changes/r-864b299c-readme-top-three/tasks.md:3-5]

受入は**配置・差分**と**掲載行からの実CLI実行**の二つをともに満たすこと。既存 pytest の成功だけでは掲載を検証できない。公式 GSD CLI の `query init.phase-op 5` は `phase_found: true`、`padded_phase: "05"`、`has_plans: false`、`query roadmap.get-phase 5` は `found: true` を返した。`planning.inspect` の `requirement_unmapped` は Traceability 節に行がないとの診断で、Phase 5 のロードマップと要件固有表には `REQ-22` が明記されている。`STATE.md` の `current_phase: 4` は過去の完了位置であり、同ファイルにも Phase 5 追加履歴がある。旧フェーズや Traceability 表をこの調査で変更しない。 [VERIFIED: GSD CLI 上記読み取りクエリの実出力; .planning/ROADMAP.md:122-135; .planning/REQUIREMENTS.md:74-80,106-119; .planning/STATE.md:2-9,89-95; tests/test_cli.py:32-61,194-198,672-682]

## Architectural Responsibility Map

| 対象 | 責任箇所 | 境界 |
|---|---|---|
| 例の掲載と配置 | `README.md` の「wordfreq の実行」 | 既存 `sh` ブロックだけ。 [VERIFIED: README.md:5-15; 05-CONTEXT.md:16-17] |
| 入力・集計・JSON | 既存のローカルCLI、入力・集計・整形部品 | `FileSource` → `count_words(iter_tokens(text))` → `top_words(selected_counts, args.top)` → `format_json(pairs)` → `sys.stdout.write(output)`。この経路は変更しない。 [VERIFIED: wordfreq/__main__.py:29-54] |
| 合否と証拠 | Builder と独立した品質担当 | 実装の前後を比較し、品質は対象 head で再実行。平文証拠を製品差分と分離する。 [VERIFIED: .planning/argonauts/r-864b299c-learnings.md:5-8; 05-CONTEXT.md:17-22] |

<phase_requirements>

## Phase Requirements

| ID | 要件 | 調査の支持 |
|---|---|---|
| REQ-22 | `python -m wordfreq input.txt --top 3 --format json` を既存 `--top 2` JSON 例の直後に1行のみ追加し、掲載行の実行で `alpha:4`、`beta:3`、`gamma:2` の順の3件と終了0を確認。一時入力は既存 `input.txt` と分離する。 | 後述の差分ゲートと実CLIゲート。 [VERIFIED: .planning/REQUIREMENTS.md:74-80; openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md:5-11; openspec/changes/r-864b299c-readme-top-three/tasks.md:5] |

</phase_requirements>

## Standard Stack

- **製品:** 既存 `python -m wordfreq` と Markdown。`dependencies = []`、開発用は `dev = ["pytest"]`。新規パッケージ・外部調査・インストールは不要。 [VERIFIED: README.md:5-15; pyproject.toml:5-14; openspec/changes/r-864b299c-readme-top-three/proposal.md:7-24]
- **検証案:** `.planning/` 内の短い Python 検証ファイルから stdlib の `tempfile`、`subprocess`、`json` を利用。既存試験も `subprocess.run`、`cwd=ROOT, capture_output=True, text=True, timeout=10` と `json.loads(result.stdout)` を使用している。 [VERIFIED: tests/test_cli.py:1-20,49-61]
- **ローカル環境:** `python --version` は `Python 3.14.9`、同じ `python -m pytest --version` は `No module named pytest`。`/usr/bin/python3` は `Python 3.12.15` で `pytest 9.0.3` が起動するため、回帰試験には後者を使える。`jq -n '1'` は `1` を返し、GSD 応答の抽出に使用できた。いずれも CLI 例そのものや全スイートの実行結果ではない。 [VERIFIED: 各環境確認コマンドの実出力]
- **プロジェクト指示:** ルートの `HERMES.md` と設定先 `./.hermes/HERMES.md` の読取りはどちらも `File not found`。`.hermes/skills` と `.agents/skills` の存在確認および公式 `query agent-skills gsd-phase-researcher --skills-only` に出力なし。 [VERIFIED: read_file の応答、ディレクトリ存在確認と GSD CLI の実出力; .planning/config.json:63-64]

## Architecture Patterns

1. **比較基点**: Builder が製品編集前の基点コミットを記録し、品質が製品変更後の対象コミットと比較する。全変更パス・状態を確認して製品差分が README だけであることを確認し、README 全体を「基点の内容のアンカー直後に指定行だけ挿入した内容」と照合する。削除0・追加1という行数だけでは、位置や行の中身は保証しない。`.planning/` の検証原本は明示的に分離し、他の製品差分を除外指定で隠さない。 [VERIFIED: 05-CONTEXT.md:16-22; .planning/argonauts/r-864b299c-learnings.md:5-8; openspec/changes/r-864b299c-readme-top-three/tasks.md:5]
2. **掲載行を実行**: 対象 head の README から節・フェンス・アンカー・直後の行を確認し、指定行がちょうど1つであることを確認する。読み取った行を argv に分解し、位置引数 `input.txt` だけを一時ファイルの絶対パスに置き換え、リポジトリ直下を cwd に掲載の `python` をシェル経由なしで実行する。期待コマンドを別途ハードコードして実行する方式は不可。入力ファイルはリポジトリ外の一時領域で UTF-8 を明示して作成し、終了時に削除する。 [VERIFIED: README.md:5-15; 05-CONTEXT.md:16-22; tests/test_cli.py:13-20,49-55; wordfreq/sources.py:13-22]
3. **合否と証拠**: 終了コード `0` と、stdout 全体を JSON として解析した後の配列を照合する。`[{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]` は期待値であり、この調査の実測ではない。配列順・件数・キー・文字列/整数型・値を確認し、オブジェクトのキー順や字下げには依存しない。終了コードを JSON 検査で上書きせず、stdout と stderr を別々に保存する。品質は実行した対象 head、基点、差分、抽出した掲載行、実 argv、入力内容、終了値、stdout/stderr、照合結果を平文で残し、証拠コミットと対象 head を区別する。添付工程では PM が読める原本を読み戻す。 [VERIFIED: .planning/REQUIREMENTS.md:74-80; wordfreq/__main__.py:45-54; wordfreq/formatters.py:11-14（`{"word": word, "count": count}`）; .planning/argonauts/r-864b299c-learnings.md:5-8]

## Don't Hand-Roll

集計や JSON 整形を検証側で再実装しない。実 CLI を呼び、固定受入値と JSON を比較する。検証用途のために製品コード・既存 pytest・CI・ブラウザ検証基盤に手を入れない。 [VERIFIED: 05-CONTEXT.md:16-22,46-48; wordfreq/aggregator.py:6-17; wordfreq/formatters.py:11-14]

## Common Pitfalls

| 誤り | 検証で落とす条件 |
|---|---|
| 掲載行がない、重複、別ブロック、順番違い、`--top 3` や `--format json` の誤記、他の行・ファイルを変更 | 配置・基点比較を非ゼロで失敗させる。旧 README を負例にすれば、CLI 自体が既に動く場合も掲載検証が落ちることを示せる。 [VERIFIED: README.md:5-15; 05-CONTEXT.md:16-17] |
| `--top` を無視する、ソートしない、`--top 2` になる | 相異なる頻度の4語を使う。制限なしでは4件目 `delta` が残り、2件なら `gamma` が欠け、初出順のままなら `delta` から始まるため、すべて不一致。今回の入力で同数時の順序は主張しない。 [VERIFIED: 05-CONTEXT.md:18,39-42; wordfreq/aggregator.py:11-17（`return sorted(counts.items(), key=lambda wc: -wc[1])[:n]`）; .planning/argonauts/r-864b299c-learnings.md:5] |
| プロセス起動不能・タイムアウト・非ゼロでも通す、空/非JSON/余計な出力、順序逆転・値や型違い | 起動・終了・解析・構造・配列のいずれかが不成立なら非ゼロ。例外や出力を隠さず、失敗箇所を記録する。既存試験も不足入力は `1`、不正 `--top`/`--format` は `2`、正常 JSON は `0` と分けている。 [VERIFIED: tests/test_cli.py:41-70,87-101,120-127; wordfreq/__main__.py:25-33,45-54] |
| 既存 pytest が通ったので追加行も正しいとみなす | `test_top_three_selects_three_sorted_words` は text、`test_json_is_machine_readable_in_frequency_then_initial_order` は個別に組み立てた argv、`test_readme_runs_as_json_from_repository_without_installation` は README 自体を入力扱い、`test_min_count_help_and_readme_example` は別の例が対象。これらを回帰とし、掲載行の受入は独立に実施する。 [VERIFIED: tests/test_cli.py:32-38,49-61,194-198,672-682] |

## Code Examples

掲載する行（実行結果ではない）: `python -m wordfreq input.txt --top 3 --format json`。既存行 `python -m wordfreq input.txt --top 2 --format json` の直後。 [VERIFIED: README.md:9-15; openspec/changes/r-864b299c-readme-top-three/tasks.md:5]

## Validation Architecture

`"nyquist_validation": true` のため省略しない。 [VERIFIED: .planning/config.json:21-25]

### Test Framework

| 項目 | 採用 |
|---|---|
| REQ-22 専用 | stdlib の実ファイル型検証。追加の製品試験や新規フレームワーク設定は不要。 |
| Wave 0 提案 | `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`（**未作成の提案パス**。PLAN で前後コミットの引数と平文証拠の出力方法を確定し、Builder が実ファイルを作成した後だけ実行）。 |
| 既存回帰（任意の補助） | `/usr/bin/python3 -m pytest tests/test_cli.py -q`、全件確認が必要なら `/usr/bin/python3 -m pytest -q`。pytest `9.0.3` の起動のみ確認。REQ-22 合格の代用ではない。 [VERIFIED: tests/test_cli.py:11-20,32-61,194-198,672-682; pytest バージョン確認の実出力] |

### Phase Requirements → Test Map

| 要件 | 振る舞い | 種別 | 自動検証・ファイルの状態 |
|---|---|---|---|
| REQ-22 / 配置・差分 | 既存 `sh` 内の直後に指定行1つ、全製品差分で README 追加1・削除0 | 静的差分 | 上記 Wave 0 検証ファイルで前後コミット全体を比較。未作成。 |
| REQ-22 / 実行 | 掲載 argv の入力だけを交換し、終了 `0` とJSONの正確な3件を検証 | 実CLIスモーク | 同ファイルで実プロセスを起動。短時間の上限を設定。未作成。 |

### Sampling Rate / Wave 0 Gaps

- Wave 0 で専用検証ファイルを実在化する。先に変更前 README で「掲載なし」が検出されることを確認し、変更後に正例を通す。誤った JSON の負例を試す場合は一時データで行い、製品・既存試験を変更しない。
- Builder は README 編集後に専用検証を実行し、最終製品コミットで配置・差分と実行の両方を確定する。品質は対象 head で同じ実ファイルから独立に再実行する。未実施・証拠なし・不一致は合格にしない。補助の pytest は別記し、ローカル成功を CI 成功と呼ばない。 [VERIFIED: .planning/argonauts/r-864b299c-learnings.md:5-8]
- 調査・計画中は未作成コマンドを試さない。PLAN の検証は実在するファイルを起点とし、インライン実行やヒアドキュメントのスクリプトに置き換えない。

## Security Domain

`"security_enforcement": true`。今回の主な確認は V5（入力検証）相当で、README から抽出した行は固定形を検証して argv で渡し、シェル評価しない。一時ファイルには固定の非機密テキストだけを書き、既存データに書き込まない。V2（認証）、V3（セッション）、V4（アクセス制御）、V6（暗号）は今回のローカル JSON 実行例で新設・変更する対象なし。HTML の安全性をこの例で検証したとは扱わない。 [VERIFIED: .planning/config.json:49-51; 05-CONTEXT.md:16-22,46-48; openspec/changes/r-864b299c-readme-top-three/proposal.md:14-24]

## Sources / Assumptions

一次資料は `05-CONTEXT.md`、承認済み `.planning/argonauts/r-864b299c-prd.md`、`REQ-22`、OpenSpec task `1.1`、`README.md`、CLI と試験の各ソース。差分・独立再実行・原本配送は `.planning/argonauts/r-864b299c-learnings.md:5-8` を参照。追加の依存・UI がないため外部資料は不要。未確認の動作を結果として主張していない。検証ファイルの仕様確定と実行、証拠採取は後工程。調査上のブロッカーなし。
