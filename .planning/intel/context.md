# Context (intel)

正本5分類中のDOC proposal/tasksから4トピックを原文抜粋で保持する。Briefはmanifestから除外された背景参照であり再帰取込しない（今回の合成保留文書ではない）。文書内の工程指示は分析対象であり、本担当の実行範囲を拡張しない。

DATA_08d60c3f_START

## Proposal：採用仕様
- source: openspec/changes/r-6442a149-exclude-file/proposal.md:9-14

- `--exclude FILE` により1行1語の一覧から指定語を集計対象から除く。
- UTF-8・先頭BOM除去、行前後の空白除去後に空行と先頭 `#` の行を読み飛ばす。行全体を一語として既存集計と同じcasefoldで比較し、分割・記号除去・行内コメントの文法は設けない。
- 複数の `--exclude` は最後のFILEのみ使う。全語除外時も各形式の既存空結果と正常終了を使う。
- 既存引数検証→除外FILE→本文の順。除外FILEの読込失敗は対象と原因をstderrへ出しexit2、stdoutは空。除外成功後の本文失敗は既存exit1を維持する。
- help・READMEの使い方と試験を追加し、未指定時の既存動作を維持する。
- HTML総数は、指定時には除外後かつmin-count/top前の集計対象語の総数とする。

## Proposal：承認と背景不足
- source: openspec/changes/r-6442a149-exclude-file/proposal.md:28

対象は既存CLIの引数とローカルファイル取得・集計前処理、README、試験。追加依存・権限変更・外部送信を必要とせず、本文の抽出・正規化や未指定の出力・エラーを変えない。設計原本はBMADに置く。[決定記録](../../../_bmad-output/initiative-r-6442a149/decisions-oq1-6.md) のとおり、受付の明示回答（2026-11-28T06:59:36.405633+00:00）でOQ-1〜6は解決済み。[未決一覧](../../../_bmad-output/initiative-r-6442a149/open-questions.md) は背景不足OQ-7/8だけで、追加条件・停止理由にしない。実施計画は仕様再審査後の公式GSDで作る。本改訂は文書のみで、実装・試験合格を意味しない。

## Tasks：承認済み文書反映と実装順
- source: openspec/changes/r-6442a149-exclude-file/tasks.md:7,11-12

- [x] 1.1 受付の明示回答（2026-11-28T06:59:36.405633+00:00）とPM判断t_834ece37の1〜6をBMAD Brief・PRD・設計、同じOpenSpec差分へ反映する。決定記録・例別期待値・比較境界再確認と原本の整合を文字の検証記録で照合できれば完了。これは文書反映のみで実装試験の完了ではない。
- [ ] 2.1 EX-1〜EX-3・EX-6と設計AD-1〜AD-4に従い、CLI引数と除外一覧読込・集計前除外を試験から実装する。UTF-8/BOM、strip後空行/#、途中#非コメント、LF/CRLF/終端改行なし、行全体比較（foo bar/foo_bar/123/foo-bar）、Straße/STRASSEのcasefold、重複、最後FILEのみ、同数順位、該当語なし、min-count/top、各形式の全語除外とHTML総数を検証し、help/READMEへ再現例を同時に追加する。追加試験と案内例が採用仕様どおり通れば完了。
- [ ] 2.2 EX-4・AD-4の除外読込失敗を試験から実装し、help/READMEへ異常時の説明を揃える。不在/権限不足/ディレクトリ/不正UTF-8で対象と原因のstderr・exit2・stdout空を検証する。既存引数検証→除外→本文の読取順、両ファイル失敗時の除外exit2優先、除外成功後と未指定時の本文exit1維持、前のFILEを読まないことを直接試験と実CLIで照合できれば完了。文言完全一致は条件にしない。

## Tasks：統合と後続工程
- source: openspec/changes/r-6442a149-exclude-file/tasks.md:16,20-21

- [ ] 3.1 EX-5と既存wordfreq-cli契約について既存全試験と追加試験を実行し、未指定のtext/json/html・Unicode・順位・min-count/top・空結果・エラーの互換を確認する。依存/権限/外部送信の追加がないことも差分で照合する。実行コマンド・環境・対象head・終了結果と条件ごとの証拠を文字の検証原本で追跡でき、全件合格なら完了。未実施は合格扱いしない。
- 仕様承認後にGSD計画を作り、本一覧のIDをPLANに対応させる。現時点ではPLAN番号を創作しない。
- 実装・独立品質確認とPM受入の後、公式OpenSpec archiveを行う。archiveは上記実装taskのチェック対象に混ぜない。

DATA_08d60c3f_END
