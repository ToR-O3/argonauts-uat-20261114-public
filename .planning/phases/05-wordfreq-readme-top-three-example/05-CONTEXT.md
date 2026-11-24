# Phase 5: wordfreq README top three example - Context

**Gathered:** 2026-11-24
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-864b299c-prd.md)

<domain>
## Phase Boundary

REQ-22 / OpenSpec task 1.1: 既存CLIの `--top 3` の利用例を README に1行追加する。利用者はコマンドを組み立てずに上位3語のJSON表示を試せる。
</domain>

<decisions>
## Implementation Decisions

### README の掲載と検証

- **D-01:** `README.md` の「wordfreq の実行」の既存 `sh` ブロック内、`--top 2` のJSON例の直後に `python -m wordfreq input.txt --top 3 --format json` をちょうど1行追加。
- **D-02:** 実装前後コミットを比較し、製品変更は README の追加1行・削除0行のみ。既存の実行例・説明・フェンス・プログラム・試験・依存・設定・連携は変更しない。
- **D-03:** 掲載行から `input.txt` だけを一時UTF-8入力のパスに置換し、リポジトリ直下で実行。入力は `delta gamma beta alpha beta gamma alpha beta alpha alpha`。終了0、JSONは `alpha:4`、`beta:3`、`gamma:2` の順で3件。既存 `input.txt` は保存・上書きしない。一時入力はコミットしない。

### Claude's Discretion

一時入力と平文検証証拠の作成方法。既存試験は変えず、検証手順の原本は必要なら `.planning/` 内で製品差分と分離する。
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/ROADMAP.md` — Phase 5、REQ-22。
- `.planning/REQUIREMENTS.md` — REQ-22。
- `.planning/argonauts/r-864b299c-prd.md` — 結合済み承認入力。
- `openspec/changes/r-864b299c-readme-top-three/proposal.md` — 対象範囲。
- `openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md` — 掲載要件。
- `openspec/changes/r-864b299c-readme-top-three/tasks.md` — task 1.1 の検証条件。
- `README.md` — 現行の書き方と挿入位置。
</canonical_refs>

<specifics>
## Specific Ideas

頻度が異なる4種類の語を一時入力に置くため、上位3件の絞り込みと順序を同時に確認できる。
</specifics>

<deferred>
## Deferred Ideas

なし。CLIの変更やHTMLの変更は範囲外。
</deferred>

---
*Phase: 05-wordfreq-readme-top-three-example*
*Context gathered: 2026-11-24 via PRD Express Path*
