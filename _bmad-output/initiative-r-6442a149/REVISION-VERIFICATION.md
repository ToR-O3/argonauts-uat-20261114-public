# 要求・仕様の回答反映検証

依頼: r-6442a149 / 対象変更: r-6442a149-exclude-file / revise=1

## 判断の根拠

受付t_c172b029の人defaultの最新判断日時: `2026-11-28T06:59:36.405633+00:00`
原文: 「提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。」
PM判断t_834ece37と差戻しt_14fbf7f0を照合。同じOpenSpec変更を更新し、新規変更は作らない。

## 原本の横断照合

| 回答 | BMAD原本 | OpenSpec差分 | 確認 |
| --- | --- | --- | --- |
| 1 | PRD FR-3、設計AD-3、決定記録OQ-1 | EX-3 Unicode scenario | 既存本文casefold維持、Straße/STRASSEが同一キー。本文tokenizer/aggregatorを実読し、casefold前の元表記は不要と確認。lowerから復元しない |
| 2 | FR-2、AD-3 | EX-2 | strip後空行/先頭#を無視、途中#は文字、LF/CRLF/終端改行なし、先頭BOM除去 |
| 3 | FR-4、AD-4 | EX-4 | UTF-8、不在/権限不足/dir/不正文字コード等は対象・原因をstderr、exit2、stdout空、文言完全一致不要 |
| 4 | FR-1/2、AD-3/4 | EX-1/2 | 行全体一語、分割・記号除去なし、foo bar/foo_bar/123/foo-bar例、重複無影響、最後FILEだけ読込 |
| 5 | FR-6、AD-2 | EX-6 | 全語除外は既存空結果とexit0。既存HTML空結果案内は維持、除外専用案内は追加しない |
| 6 | FR-4、AD-4 | EX-4複合失敗 | 既存引数検証→除外→本文、両ファイル失敗は除外exit2、除外成功後の本文失敗exit1 |

全形式で除外はmin-count/top前、残存語の回数と相対初出順を維持、HTML総数は除外後・selection前で一致。Brief SC-01〜06からPRDへ追跡できる。proposalとdesignは更新原本を参照し、古い製品判断保留を解消した。未決一覧には背景不足OQ-7/8のみ残し、停止理由や追加条件にしない。OQ-1〜6の回答・根拠・日時は `decisions-oq1-6.md` に分離して保存。

## 独立確認

BMAD公式updateのレビューは `reviews/update-independent-review.md`、設計の機械lintと独立reality/adversarialレビューは `architecture/reviews/update-gate.md` とその参照原本。Unicodeの追加行境界定義提案は採用判断の範囲外として非採用に裁定し、全レンズ無指摘とは報告しない。

親の統合後、別の標準delegate_taskによるreconciliation/fresh-readerでBrief・PRD・設計・決定記録・未決一覧とOpenSpec四成果物を全文独立照合した（sa-0-8010ed30、通常終了、truncated=false）。回答1〜6と維持条件に重大矛盾なし。原本整合の確認後にtasks 1.1だけをチェックした。2.1/2.2/3.1は未実施のまま。

## 実行した検証

- 管理下のOpenSpec CLI `status --change r-6442a149-exclude-file --json`: proposal/specs/design/tasksすべてdone、isPlanningComplete=true。原出力 `reviews/revised-openspec-status.json`。
- 同CLI `validate r-6442a149-exclude-file --strict --json`: exit0、valid=true、issues=[]。原出力 `reviews/revised-openspec-validate.json`。
- 公式 `lint_spine.py --workspace _bmad-output/initiative-r-6442a149/architecture`: exit0、ok=true、total_findings=0。最初の位置引数指定はCLI usageで失敗し、公式--workspace指定で再実行して確認。
- `git diff --check`: exit0。

BMAD headlessは背景不足OQ-7/8のためpartial/draftを保持するが、今回の機能仕様未決を示すものではない。

## この工程で行っていないこと

製品コード、README、試験、GSD計画は変更していない。新機能試験・全件回帰は未実施であり、合格を主張しない。後続の仕様再審査t_0d1aa16aへ原本を引き継ぎ、実装へ自動継続しない。
