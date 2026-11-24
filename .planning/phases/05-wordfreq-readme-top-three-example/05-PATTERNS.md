# Phase 05: wordfreq README top three example - Pattern Map

**Mapped:** 2026-11-24

**Files analyzed:** 対象2件（製品1件、検証ファイル案1件）
**Analogs found:** 2 / 2（完全一致1、役割一致1）

## File Classification

| 対象 | 役割 | データフロー | 最も近い既存例 | 一致度 |
|---|---|---|---|---|
| `README.md`（変更） | 利用者向けドキュメント | 静的なコマンド掲載 → ローカルファイル入力の CLI → JSON stdout | `README.md:5-15` の同じ `sh` ブロック | 完全一致 |
| `.planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`（未作成の提案） | 受入検証ユーティリティ | 前後コミット・README 読取り（file-I/O）→ 一時 UTF-8 入力 → 実サブプロセス（batch）→ JSON と終了値の照合・平文証拠 | `tools/verify_wordfreq_min_count.py:85-113,122-157`、補助 `tests/test_cli.py:13-20,49-59,672-682` | 役割一致。掲載行を抽出して実行する部分は新規 |

## Pattern Assignments

### `README.md`

`README.md:9-15` の既存例と同じ記法を使う。以下の2行の間に `python -m wordfreq input.txt --top 3 --format json` を1行だけ挿入する。

```sh
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
```

見出し・フェンス・既存行はそのまま。製品差分は `README.md` の追加1行・削除0行のみ。

### `verify_readme_top_three.py`（提案）

- **比較と出力の採取:** `tools/verify_wordfreq_min_count.py:88-104` は `subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)` で実 CLI を呼び、`result.stdout`・`result.stderr`・`result.returncode` を分けて記録する。同ファイルの `122-135,149-157` は `base_tree, head_tree = tree(BASE), tree(head)` で全体を比較して許可外のパスを拒否する。Phase 05 では固定した前後コミットの全変更パス・状態を確認し、検証原本などの `.planning/` の変更を製品差分と分離する。README 全体が基点に指定行を挿入しただけであることを照合する。旧フェーズの定数・対象パス・証拠基盤は流用しない。
- **掲載行と実行の結合:** `tests/test_cli.py:676-682` の `readme = (ROOT / "README.md").read_text(encoding="utf-8")` と UTF-8 の一時入力・実 CLI 呼出しが近い。ただし既存試験は掲載文字列を確認した後に別の argv を組み立てる。今回は対象 head の README から該当節・`sh` フェンス・アンカー直後の一意な掲載行を検証して抽出し、その行の `input.txt` だけをリポジトリ外の一時ファイルの絶対パスに差し替える。入力は `delta gamma beta alpha beta gamma alpha beta alpha alpha`。掲載の `python` をリポジトリ直下から argv で直接実行し、シェル評価せず、既存 `input.txt` は触らない。
- **終了値と JSON の照合:** `tests/test_cli.py:16-20,49-59` の `assert result.returncode == 0, result.stderr` と `assert json.loads(result.stdout) == [...]` を参考にする。期待値は `[{"word":"alpha","count":4},{"word":"beta","count":3},{"word":"gamma","count":2}]`。配列順・件数・キー・値・型（`count` は整数）を確認し、字下げやキー順には依存しない。掲載・差分・起動・終了・JSON のいずれかが不成立なら非ゼロにする。

## Shared Patterns

- **現行 CLI が唯一の出力元:** `wordfreq/__main__.py:29-38,45-54` の `FileSource` → 集計 → `top_words` → `format_json` → stdout。`wordfreq/formatters.py:11-14` は `word` と `count` のオブジェクトを入力順の配列にする。集計や整形を検証側で再実装しない。
- **平文証拠:** `.planning/argonauts/r-864b299c-learnings.md:5-8` に従い、基点・対象 head・差分・抽出行・実 argv・入力・終了値・stdout/stderr・照合結果を残す。Builder と品質は検証ファイルの作成後に実ファイルから実行し、品質は対象 head で独立再実行する。対象 head と証拠コミットは区別する。

## No Analog Found

対象ファイル単位では該当なし。README の配置・1行差分検査から掲載 argv の実行までを一体化した既存例は、上記参照範囲では確認していない。この結合部分は `05-RESEARCH.md:62-66` を参照する。

## Metadata

- **Analog search scope:** ルート README、`tests/`、`tools/`。現行契約と証拠方針は `wordfreq/` と `.planning/argonauts/` を参照。
- **Files scanned:** 上記範囲の本文参照7件（抜粋を含む）。採用した既存例は `git ls-files` で追跡を確認。
- **Pattern extraction date:** 2026-11-24。製品・Git は未変更。CLI スモークと専用検証は未実行。
