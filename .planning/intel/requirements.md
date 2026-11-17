# Requirements (intel)

Extracted from the two PRD-classified sources. Where both PRDs state the same requirement, both source paths are cited. No competing acceptance variants detected between the two PRDs (consistent on options, defaults, exit behavior, packaging, dependency constraints).

## REQ-wordfreq-cli-execution
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-1 — user runs `python -m wordfreq <file>` with exactly one file argument, the file is read as UTF-8, and word frequency aggregation results are produced (new capability `wordfreq-cli` in the proposal).
- acceptance: 「ファイルが存在しない・開けない・UTF-8 としてデコードできない場合は、エラーメッセージを stderr に出して exit 1 で終了する。ファイル引数が 0 個・2 個以上の場合は使い方エラー（exit 2）。空ファイルは結果 0 件として exit 0 する。」
- scope: wordfreq CLI invocation, file input, error/exit behavior (exit codes per PRD D-4)

## REQ-top-count-option
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-2 — `--top N` selects the number of displayed results.
- acceptance: 「既定は 10。N は 1 以上の整数で、それ以外の値（整数でない、0 以下）は使い方エラー（exit 2）。結果の種類数が N より少ない場合は全件を出す。」
- scope: CLI option --top, validation, usage-error exit

## REQ-output-format-option
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-3 — `--format text|json` selects human-readable text or machine-readable JSON output.
- acceptance: 「既定は text。不正な形式指定は使い方エラー（exit 2）。text は 1 語 1 行で単語と回数を読むことのできる形式、json は `{"word": <str>, "count": <int>}` のオブジェクト配列（FR-4 の並び順どおり）で、`json.loads` で機械可読であること。結果 0 件のとき json は `[]`、text は出力なし。text の正確な列書式は design.md で決める。」
- scope: CLI option --format, text/JSON output structure; exact text column format delegated to design.md (outside the current ingest set)

## REQ-deterministic-ordering
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-4 (decision D-2) — output ordering is always deterministic; the proposal lists deterministic ordering (並び順) among the fixed-by-test behaviors.
- acceptance: 「出力は常に同じ順序である: 出現回数の降順、同数の単語は正規化後単語の昇順（D-2）。同じ入力・同じオプションでの出力は決定的（識別子とする）。」
- scope: sort rule, determinism identifier for acceptance cards

## REQ-component-separation
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-5 — tokenization/normalization component is separated from aggregation/output-formatting components (proposal: 切り出し・正規化 / 集計 / 入力取得 / 出力整形 separation).
- acceptance: 「各部品はそれ単体で呼んで検証でき、対応する単体試験を持つ（分離の機械的確認はこの試験とする）。」
- scope: module architecture, unit-testability of isolated components

## REQ-input-source-boundary
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-6 — text acquisition ("入力取得") is a boundary separated from parsing/aggregation; v1 file input also runs behind that boundary; future sources (stdin/URL) need only a boundary implementation addition.
- acceptance: 「解析・集計が入力取得境界を介してのみテキストを受け取ることを通す試験（境界越し試験）を持ち、標準入力などの将来の入力元がその境界の実装追加で足りることを design.md（OpenSpec 変更。ADR に相当）に構成判断として記録する。標準入力・URL 入力の実装自体は v1 の作業範囲ではない。」
- scope: input-fetch extension seam; design-record target design.md sits outside the current ingest set

## REQ-pytest-ci
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-7 — pytest unit tests exist and pass in the repository CI's pytest job.
- acceptance: 「FR-1〜FR-5・FR-6 のエッジ（不存在ファイル、空ファイル、ファイル引数個数、不正な `--top`・`--format`、同数語の順序、大文字小文字の同一視、UTF-8 失敗、JSON 構造、境界越し試験）をテストケースに含む。対象 Python は当該 CI ジョブの CPython 3 の版とし（版番号は CI 設定が持つ。本では固定しない）、バージョン横断互換コードは書かない。」
- scope: pytest test suite, CI pytest job, Python version policy

## REQ-stdlib-only-runtime
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md, /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- description: FR-8 — runtime dependencies are standard library only; PM policy "stdlib-first" elevated to a binding decision (proposal: ランタイム依存は標準ライブラリのみ).
- acceptance: 「依存追加が必要になる場合は人の承認を要する範囲変更として扱う。パッケージ化に最低限必要な設定ファイル（`pyproject.toml` 等）の変更は許容するが、smart マージ方針で人の承認対象になり得ることを前提に必要最小限に留める。ローカルパッケージ名 `wordfreq` と同名 PyPI パッケージの取り違えは、依存を増やさず repository 内で `python -m` 実行する範囲では問題にならない前提（Brief A-5）。」
- scope: dependency policy, packaging config, human-approval boundary
