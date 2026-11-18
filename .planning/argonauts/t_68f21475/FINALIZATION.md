# 最終化の記録

依頼: r-e476c11d / t_68f21475 run162
開始head: 421a65cb024c848ec8a0b9ff2ff5aec1538abfde

## 実施と実測
- originは固定入力のToR-O3/argonauts-uat-20261114-public。origin/argonauts/r-e476c11dから開始、origin/mainは既に取込み済み、workflow差分なし。
- 品質添付191/198とPM添付199/220の原本を読取り、tasks2.2に旧製品head afaa56fc022c895ee2243b8f67a239c7c0096086の技術gateとPM承認の参照を記入してチェックした。過去verify191やVERIFICATION197の履歴を改変していない。
- archive前の公式 `openspec instructions apply --change r-e476c11d-wordfreq-min-count --json` はtotal6/complete6/remaining0/state all_done。`openspec validate r-e476c11d-wordfreq-min-count --type change --json` はvalid true/issues空/exit0。
- `openspec archive r-e476c11d-wordfreq-min-count --json` はexit1、archive_confirmation_required（仕様1件の同期のみ）。それを確認して `--yes --json` を実行しexit0、2026-11-18-r-e476c11d-wordfreq-min-countへarchive、specsUpdated true、added3/modified3/removed0/renamed0。
- `openspec validate --specs --json` は1件passed/failed0/exit0。既存要求D-3、FR-5/6、FR-7/8のSHALL/MUST推奨WARNING3件を残す。旧要求の修正を追加しない。
- `gh pr ready argonauts/r-e476c11d` 成功。その後のreadbackでPR8 OPEN/isDraft falseを確認。Ready確認後に最終commit/pushする。
- Builderの実行: `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q`、694 passed in 157.46s、exit0。これはarchive後の作業treeでの回帰試験であり品質の画像実閲覧や新head独立受入ではない。
- 製品コード・見た目・CI・依存は本最終化では変更しない。archive後は変更元ディレクトリが存在せず、archive先tasksと同期specが存在することを確認した。

## 最終品質への必須引継ぎ
新headをPR/originと照合し、runbook `docs/wordfreq-min-count-verification.md` §6のfresh-root全面再検証を行う。旧afaa56fの証拠headの付替え禁止。品質本人の独立CLI、1280×900/320×900 DPR1の全画像実閲覧、source-order、owner exit0、全derived整合と標準添付を新headで確認する。CIは有限回読取り、未報告を成功にしない。smart予約/手動案内と品質印は品質が決める。Builderは直接マージ/Approve/品質印を実行しない。
PM画像未閲覧と人の618件SHA一致採用の境界、VERIFICATION197の古い本文と最新run157/UAT198/PM判断を併読する経緯を保持する。旧phase1/3 staleとadvisoryは対象外。
