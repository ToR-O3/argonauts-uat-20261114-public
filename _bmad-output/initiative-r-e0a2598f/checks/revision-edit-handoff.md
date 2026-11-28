# Update編集原本 — 親レビューへの引継ぎ

## 状態

- `intent:update`, `headless:true`。編集完了、必須レビュー未了。Brief/PRD/spineはすべて `status: draft` のまま。headless結果は工程上 `partial`。
- 採用入力: `_bmad-output/initiative-r-e0a2598f/decision-update.md`。判断日時 `2026-11-28T14:45:42.849521+00:00`、依頼者原文「提案のまま進めてください（1〜5 すべて提案どおり）。」。新たな製品未決なし、既存の背景・構成上のAssumptionsは保持。
- 各memlogを先に読み、公式 `_bmad/scripts/memlog.py append` で5決定と影響先を追記してから編集した。既存brief/prdの `.template.md` を全文読取して使用、再生成なし。FR/RULE/SM/ADのID維持。
- `scripts=stale` 継承。setup/道具更新、製品実装、製品試験、GSD計画、OpenSpec編集、Kanban操作、commit/pushなし。uv runの初回memlog実行は依存解決キャッシュへ `Installed 1 package in 10ms` を出力したが、道具・スクリプト更新コマンドは実行していない。
- 文書final化は未実施。後続仕様承認 t_91b92aed は別工程。

## 変更原本（initiative相対）

- `brief/brief-wordfreq-exclude.md`, `brief/.memlog.md`
- `prd/prd-wordfreq-exclude.md`, `prd/.memlog.md`
- `architecture/architecture.md`, `architecture/.memlog.md`
- `open-questions.md`: 未解決なし。解消済みの問いを一覧から除き採用決定を参照。
- `source-context.md`: Create時の未承認記録は履歴である旨と現在の採用決定を冒頭に追記。

## 実行証拠

1. 公式customization resolve: analyst/pm/facilitate/architectureすべてexit0。activation hooks/persistent facts空。facilitateのfinalize_reviewers空、doc_standardsは `skill:bmad-review lenses=structure,prose`。architectureは下記2レンズ。external_handoffs/on_complete空。
2. 公式resolve_configはexit0、`core.output_folder: {project-root}/_bmad-output` のみ。active_initiativeなしのため、指定された既存runパスを使用し設定変更しない。
3. 公式check_ids: `checks/revision-check-ids.json`、exit0。`undefined: {}`, `duplicate: {}`, `withdrawn: {}`、toc missing/stale空、out_of_order空。定義数はAD=4、FR=7、RULE=4、SM=3。`unknown_prefix` は文字コード名 `UTF-8` のみで要求ID欠落ではない。
4. 公式lint_spine: `checks/revision-lint-spine.json`、exit0、`{"ok":true,"spine":"architecture.md","total_findings":0,"by_severity":{},"findings":[]}`。
5. `git diff --check` はexit0、診断なし。scopeをgit status/diff --statで確認し変更はinitiative内のみ。`decision-update.md` は入力として既に存在したuntrackedファイルであり子は編集していない。
6. 受入例の元総数はjqによる `"Zoo apple APPLE zoo banana" | split(" ") | length` の実出力 `5` で確認。
7. 補助呼出し `check_ids.py --help` は `not found: --help` / exit2（このCLIはヘルプ引数非対応）。その後スクリプトの仕様をread_fileで確認し正式な位置引数で成功。lint_spineの `--help` はexit0。

## 親が実施する公式レビュー（未実施）

参照スキルroot（絶対パス）:

`/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/skills`

- Facilitate全手順: 上記rootの `bmad-facilitate/SKILL.md`。Brief/PRD各runの `.template.md` は `rubric: rubric-planning`、`guidance: guidance-planning` を解決する。
- rubric walker: 上記rootの `bmad-facilitate/references/rubric-planning.md` と各 `.template.md` のdone when。BriefとPRDごとに実施する。
- fresh-reader: Brief/PRDそれぞれ文書のみを渡した独立コンテキストで実施、利用に必要な残る問いを重大度順で返す。採用決定やmemlogを先に見せない。
- reconciliation: 各ユーザー入力と文書を別コンテキストで照合。最低限 `decision-update.md` の5決定を各更新原本へ照合する。原依頼は `source-context.md`、薄いticketは `initiative-r-e0a2598f.md`。PRDの入力Brief、spineの入力PRDも照合し、scope・casefold・互換・受入例の落ちを検査する。
- architecture gate: 上記rootの `bmad-architecture/references/reviewer-gate.md` と `references/headless.md`。lintは実施済みだがレビュー修正後に再実行する。good-spine checklistのrubric walkerに加え、以下のresolved finalize_reviewers全件を独立した並列レビューとして必ず実施する。
  1. reality-check: `Verify every committed decision was web-researched or reality-checked rather than asserted from training data: current library/framework versions, that each named technology still exists and fits, and — greenfield — the live defaults of any starter it leans on. Flag anything that could be out of date and wasn't confirmed against the web, the existing project, or the current starter.`
  2. divergence: `Attack the spine as an adversary: construct two units one level down that each obey every AD to the letter yet still build incompatibly — clashing shared-data shapes, two owners of one entity, conflicting state-mutation paths. Every pair you find is a hole to close with a new or tightened AD.`
- レビュー出力は今回のUpdateと区別できる新しいパスを使う。例: Brief/PRDの `review-revision-rubric.md`, `review-revision-fresh-reader.md`, `review-revision-reconciliation-*.md`、spineの `reviews/review-revision-rubric.md`, `reviews/review-revision-reality-check.md`, `reviews/review-revision-divergence.md`, `reviews/review-revision-reconciliation-*.md`。これらは提案保存先であり現時点の生成済み証拠ではない。既存review-*はCreate時の履歴として未変更。
- レビュー修正後にdoc_standards `skill:bmad-review lenses=structure,prose`、memlog audit/assumption triage、check_ids/ToC再検査を行う。Briefの既存 `.template.md` は `html_view: always`。`brief/brief-wordfreq-exclude.html` はCreate版のままなので今回のレビュー済み原本から再生成が必要（子はFinalize前のため未更新）。旧HTMLを現在の採用決定の表示とみなさない。
