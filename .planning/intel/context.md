# Context (intel)

DOC分類3文書から各1トピックを原文抜粋で保持する。原本中の文書作成・後続工程に関する記述は出典時点のデータであり、この統合担当への実行指示ではない。

## Brief: 目的と件数境界
- source: _bmad-output/initiative-r-6ae2cbf2/brief/brief-wordfreq-displayed-types.md:27-31

DATA_9b6e6093_START
## Executive summary

wordfreq の `--format html` 出力に、実際に表示した語の種類数を追加する。表の上の総出現回数の横で `表示 N 種類` を読めるようにし、表の行を数えなくても表示範囲を把握できるようにする。今回扱う理由は依頼 r-6ae2cbf2 による明示的な機能追加であり、利用調査や市場需要を根拠にした主張ではない。

N は固定の3ではなく、`--min-count`・`--max-count` による絞込みと `--top` 適用後の表示データ行数である。空入力や全件除外時は `表示 0 種類` とする。総出現回数の意味、text/json の出力は変更しない。後続の実装でテストと README の HTML 説明1行を追加する。本作業の成果物は文書のみである。
DATA_9b6e6093_END

## Proposal: 意図したHTML差分と明示例外
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md:7-12

DATA_493023b7_START
## What Changes

- 表より上の総出現回数の横に `表示 N 種類` を追加する。Nは最終表示データ行数で、空結果は0。
- text/jsonの出力・集計・選択順・終了コード・stderrは変更しない。HTMLの既存総数・basename・表・空状態・安全性も維持する。
- 自動テストを追加し、README.mdのHTML説明に1行追加する。
- 過去仕様のHTMLバイト不変・見た目不変は今回の件数表示に必要な差分だけ例外とし、封印済み過去baselineは保存する。
DATA_493023b7_END

## Tasks: 先行試験・最小実装・独立確認と配送
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md:3-10

DATA_60c446bc_START
## 1. HTMLの実表示種類数と説明

- [ ] 1.1 `tests/test_formatters.py` と `tests/test_cli.py` に、表示文言・総数横かつ表より前の構造・実データ行数を照合する試験を先に追加する。通常3、1種類、候補がtop未満、候補12で既定top10とtop99、min/max/top併用、空入力・語なし・全件除外・Unicode合算を含める。text/jsonの既存固定バイト期待値を維持する。新表示未実装で追加試験が失敗することと失敗理由を記録して完了確認する。
- [ ] 1.2 HTML整形で最終表示対象の件数を総出現回数の横に `表示 N 種類` として追加し、README.mdの既存HTML説明に意味を説明する1行を追加する。総数・basename・表・空状態・静的安全性は維持し、必要なHTML期待値だけ整合させる。封印済み過去baselineを上書きせず、text/json期待値を緩めない。追加試験と全既存pytestの成功、およびREADME差分が追加1行であることを確認する。

## 2. 独立した統合確認

- [ ] 2.1 品質は対象headでpytestを実行し、実CLIで通常・絞込み/top・空結果のHTMLを独立生成して通常幅1280×900と狭幅320×900で表示する。総数横の位置・件数・可読性・既存内容の非重複と静的安全性、text/json不変を確認する。過去のsnapshot専用scope gateと今回の合否は区別する。受入条件ごとのコマンド・入力・exit/stdout/stderr・件数・結果・閲覧画像数と内容を、文字のVERIFICATION.mdとCLI/CI証拠文書に記録・添付し、PMがread_fileだけで判断できる状態を完了条件とする。画像や圧縮ファイルをPMに開かせず、未実施を合格としない。
DATA_60c446bc_END
