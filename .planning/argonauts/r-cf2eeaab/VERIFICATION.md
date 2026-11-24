# VERIFICATION — r-cf2eeaab フェーズ検証 7（品質の独立実行）

- カード: t_9dff5b92 ［フェーズ検証 7］ / 実行者: argonauts-uat-quality（run 65。Builderではない）
- 固定起点: c572613dc626160db2eb3bf4a41c95fc8283b828
- 対象head（品質が検証した版。start_sha）: c5d0eb136bf92d6f00c3fc807346e55103917504（PR ToR-O3/argonauts-uat-20261114-public#17）
- 報告head: この文書を保存した後続の .planning だけのcommit。対象headとは別（SHAは完了metadataの head_sha）
- 依頼者の最新判断（2026-11-24T19:13:42.938043+00:00、原文）: 「新しく作ってよい。完成後の説明文は「argonauts-uat public (UAT)」とする。」
- CLI原本: `.planning/argonauts/r-cf2eeaab/quality-cli-evidence.txt`（C1〜C7。コマンド・cwd・exit・生のstdout/stderr・実測時間）
- 画像: 0枚。説明文metadataだけの変更で画面に変化がないため、ブラウザーは使っていない

## 受入条件ごとの判定

| AC | 判定 | 根拠（品質が対象headで実行したもの） |
|---|---|---|
| (1) [project].description を新規追加し、解析値が厳密に `argonauts-uat public (UAT)`。印を足さない | 合格 | C1 `verify_description.py` exit 0（0.094s）: baseline_description_absent / description_type / description_value / single_expected_line が true、description は `argonauts-uat public (UAT)`。pyproject.toml 8行目。ビルドしたPKG-INFOの `Summary: argonauts-uat public (UAT)` も確認 |
| (2) 他の製品ファイルと既存TOML項目・値を変えない | 合格 | C1 other_data_unchanged / existing_bytes_unchanged / head_scope / index_scope / worktree_scope / untracked_scope が true。C5: 工程文書を除く製品の変更は pyproject.toml の1行だけ（numstat 1/0）。工程の文書: 62件（判定の対象外） |
| (3) 変更後の pyproject.toml がTOMLとして正常に解析できる | 合格 | C1 baseline_toml / worktree_toml / baseline_utf8 / worktree_utf8 が true。C6 `git diff --check` exit 0 |

製品の変更: pyproject.toml（description 1行の追加）。工程の文書: 62件（判定の対象外）。危険なパス: pyproject.toml に触れる（smartでも人がマージする）。

## 実行の一覧（cwd はカードのworktree。対象head をcheckout）

| # | コマンド | exit | 実測 | 結果 |
|---|---|---|---|---|
| C1 | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | 0 | 0.094s | 18項目すべて true、stderr 空 |
| C2 | `cd .planning/argonauts/r-cf2eeaab && python3 test_verify_description.py -v` | 0 | 1.500s | Ran 6 tests、OK |
| C3 | `git status --porcelain=v1 --untracked-files=all` | 0 | — | 空（製品dirtyなし） |
| C4 | `git rev-parse HEAD:pyproject.toml` / `git hash-object pyproject.toml` | 0 | — | 両方 eeff26ea…（HEAD blob と作業bytes が一致） |
| C5 | `git diff --name-status --no-renames c572613 HEAD`（工程文書を除外） | 0 | — | `M pyproject.toml` のみ |
| C6 | `git diff --check c572613 HEAD -- pyproject.toml` | 0 | — | 空 |
| C7 | `uv run --with pytest pytest -q`（既存の試験。回帰の確認） | 0 | 196.018s | 702 passed |

## 区別して扱ったこと

- Builderの欠落RED（builder-red-cli.txt）と追加後GREEN（builder-green-cli.txt）はBuilderが実行したもの。品質は原本を読んだだけで、REDは再現していない。上のC1〜C7が品質の独立実行。
- 保存（このcommit）・標準添付・PMの読取りは別の状態。品質は保存と添付の照合までを行った。PMの読取りは後工程（t_f322fb6b）で、まだ行われていない。
- probe未分類3件（REQ-25/26/27）と透明性prohibitions 2件（P1・P2）は flagged のまま保持した。品質の確認では違反を見つけなかったが、解消済みとは扱っていない。

## GSDのフェーズ検証（公式手順）

- 公式 `07-VERIFICATION.md`（gsd-verifier）: status **human_needed**、score 4/5。gapsなし。人の確認項目5件（品質の文書と添付、PMの読取り、P1、P2、probe 3件）
- Nyquist `07-VALIDATION.md`: nyquist_compliant true（gaps 0）／ security `07-SECURITY.md`: threats_open 0（4件すべて closed、ASVS 1）
- コードレビュー: 同じ head の `07-REVIEW.md`（t_35976c4e で作成、status clean）を再利用
- OpenSpec verify: `.planning/argonauts/t_9dff5b92/openspec-verify.md`。CRITICAL・WARNING・SUGGESTION はなし。`openspec validate --strict` exit 0
- phase 7 は完了にしていない（human_needed のため `phase.complete` は呼んでいない）。UAT は `07-UAT.md`
