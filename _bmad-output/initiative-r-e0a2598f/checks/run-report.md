# BMAD非対話作成 — 実行記録

## 結果

- intent=create / headless=true / status=partial。Brief/PRD/spineはいずれもdraft。原本はbrief/brief-wordfreq-exclude.md、prd/prd-wordfreq-exclude.md、architecture/architecture.md。
- 出力はこのinitiative配下だけ。既存実装、tests、README、正本、initiative ticket、CIは変更していない。git commit/pushとKanban操作なし。
- 公式チェックは終了コードだけでなくJSON本体をread_fileで確認した。
- 最終check_ids: undefined/duplicate/withdrawn/tocは空。unknown_prefixは文字コード名称UTF-8のみであり要件IDではない。
- 最終lint_spine: ok=true / total_findings=0。
- 公式word_metricsとjqでfrontmatter相当/preamble・ToC・Assumptionsを除いた計数: Brief=1244、PRD=2427。空白単語だけを数えるwc -wと日本語を含む公式計数は異なる。紙面のページ数を実測したとは主張しない。
- git diff --checkはexit0、git statusは今回の出力配下のuntracked追加だけ。追跡済みファイルの改変なし。

## 実行した公式ワークフロー

スキル実体は `/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/skills/`。HERMES_PROFILE_HOMEは使用しない。既存スクリプトの更新/installはしていない。

1. bmad-agent-analyst / bmad-agent-pm / bmad-facilitate / bmad-architecture / bmad-reviewをload。各スキルについて `uv run _bmad/scripts/resolve_customization.py --skill <実体パス> --project-root . --key workflow`（両agentは `--key agent` も指定）。resolve_configでoutput_folderとactive_initiativeを取得。active_initiativeは未設定だが指定output pathを優先。
2. `uv run _bmad/scripts/list_templates.py --libraries-of <facilitate> <agent assets> --project-root . --root <skills> --brief`。カスタムライブラリの既定2フォルダ不在のみで、templateは利用可能。
3. 同じlistingを `--template brief --merge <brief run>/.template.md`、`--template prd --merge <prd run>/.template.md` にして公式merge。両mergedファイルを全文読取。guidance/rubricをloadし文書作成。
4. `uv run _bmad/scripts/memlog.py init/append --workspace <run> ...` を全runで使用。PRDの入力にBrief documentパス、spineの入力にPRD documentパスを渡す。headless.mdとspine-templateを読み、memlogからspineをdistill。
5. reconciliation、rubric、fresh reader、bmad-review edge-case-hunter、structure→proseを実施。spineはgood-spine rubricと設定finalize_reviewersのreality-check/two-unit adversaryを全て実施。subagentツール不可のため逐次fallback。独立プロセスまたは独立品質の承認とは呼ばない。
6. `uv run <facilitate>/scripts/check_ids.py <Brief> <PRD> <spine> <open-questions>` を初回/最終実行。最終原本 `check-ids-final.json`。
7. `uv run <architecture>/scripts/lint_spine.py --workspace <architecture run> --output <checks>/lint-spine-final.json` を初回/最終実行。
8. `uv run <review>/scripts/word_metrics.py <document>` を実行し原本保存。wc -wも実行。jqでJSONの該当項目と本文計数を検査。未作成の機能検証コマンドは実行しない。
9. レビューの明確な編集修正だけ反映し、目次/idsを再チェック。Briefのalways viewは付属brief-view.htmlをstarterにした静的自己完結HTMLで保存。一般render_view.pyはCDNを含むため使わない。ブラウザ品質実行とは呼ばない。
10. memlogを監査しAssumptionsと未決の行先を記録。OQが残るのでfinalにせずpartialで閉じる。外部handoff/on_completeは設定が空で実行対象なし。

## レビュー原本

- `../brief/review-rubric.md`、`../brief/review-fresh-reader.md`、`../brief/review-reconciliation.md`、`../brief/review-editorial.md`
- `../prd/review-rubric.md`、`../prd/review-fresh-reader.md`、`../prd/review-reconciliation.md`、`../prd/review-edge-case-hunter.md`、`../prd/review-edge-case-hunter.json`、`../prd/review-editorial.md`
- `../architecture/reviews/review-rubric.md`、`../architecture/reviews/review-reality-check.md`、`../architecture/reviews/review-divergence.md`、`../architecture/reviews/review-reconciliation.md`
- 採否と監査は `review-triage.md`。

## 残件

共通open-questions.mdのHTML総数、trim/コメント、文字コード/他読込み失敗、不正行、二重失敗優先の回答。背景推定と文書altitude/purposeも未確認。回答後は文書/memlogをUpdateしてからSofiaのRequirements/adoption、Builder実装と品質の独立検証へ進む。今回の成果を機能実装済み・試験成功・製品受入済みと扱わない。
