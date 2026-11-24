# r-48110017 実装の検証（light）

## 対象と範囲
- 実行日時: 2026-11-24T20:58:36+09:00 時点までの実行。
- repo: ToR-O3/argonauts-uat-20261114-public
- 依頼branch: argonauts/r-48110017 / base: v112-b
- PLAN起点: 681008b5681338987c366cab9bfcc0f6ae4ad439
- 検証した製品変更のhead: c12a8dc36266b9877a22a5fd5892fe7e9c860e70
- この記録のcommitは上記headへ工程文書だけを追加する。
- 受付t_e68130e7の依頼原文に従う。追加の「argonauts: 依頼者の判断」コメントは確認時点で無し。

## 受入条件と結果
1. 「README.md の使い方の説明に、--top 5 を指定した実行例を1つ足す。」: 合格。
   編集前のREADMEと検索結果で対象例の欠落を確認。既存shブロックの `python -m wordfreq input.txt` 直後へ `python -m wordfreq README.md --top 5` を1行追加した。git diffは追加1行・削除0行で、既存例と末尾の検証B行を保持。
2. 「変えるのは README.md だけ。」: 製品差分はREADME.mdのみで合格。
   許可された工程文書は本依頼のPLAN.mdと本VERIFICATION.mdのみ。新規スクリプト・試験・SUMMARY・フレームワーク成果物は作成しない。
3. 「未決事項は無い。」: 新たな判断事項なし。

## 実CLI
コマンド: `python -m wordfreq README.md --top 5`
終了コード: 0。stdoutは以下の5行（区切りはタブ）、stderrは0バイト。

```text
13	html
8	wordfreq
8	top
8	count
7	python
```

別途stdout/stderrを分離して同じコマンドを再実行し、`wc -l`で5行、`wc -c`でstderr 0バイト、`test ! -s`で空を確認（全て終了コード0）。5行とも回数・タブ・単語の形式。pythonの置換は不要。

## 既存試験と差分
- `uv run --with pytest python -m pytest -q tests/test_cli.py`: 終了コード0、358 passed in 13.19s。
  uvのrequires-python未指定警告はあったが試験失敗は無し。生成された未追跡uv.lockとwordfreq.egg-infoは除去し、製品変更に含めない。
- CIの既存workflowはPython 3.12で全pytestを実行する設定と読取り確認。
- `uv run --no-project --with pytest python -m pytest -q`: 終了コード0、702 passed in 166.97s (0:02:46)。全既存試験も実行した。
- `git diff --check`: 終了コード0、出力無し。
- `git diff --name-status origin/v112-b...HEAD`（製品変更commit後）:
  - A .planning/argonauts/r-48110017/PLAN.md
  - M README.md
- 本記録の追加前の `git status --porcelain` はREADME.mdの変更のみ。新規検証スクリプトや試験は無し。

## 引継ぎ
これはBuilderの実行結果であり、品質の独立実行とは区別する。push後の最終headとPRは同じカードのrequest_review metadataに記録する。GitHub CIはpush後に1回読み取り、未完了なら待機せず品質へ引き継ぐ。
