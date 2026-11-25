# Tasks

## 1. 上限指定・共通選択・使用例の一体実装

- [x] 1.1 既存の保存済み期待出力を確認し、不足する省略互換の期待バイト列・入力・実行条件を変更前に固定する。tests/test_cli.pyにMAX-1/MAX-2と変更されたFR-2/FR-4/HTML-2/MC-1/MC-2の追加pytestを先に書き、新オプション未実装で狙いどおり失敗することを確認する。整数表記・欠落/非整数・読込み前検証、0/負数/逆転、全形式、min/max境界、max1、Unicode、同数初出順、top既定/明示、空入力/抽出0語、有効上限でも入力失敗を含める。検証は追加ケースのRED出力を残し、既存試験の期待値を新コードで作り直さないこと。
- [x] 1.2 wordfreq/__main__.pyにtype=int・省略Noneの--max-countを追加し、共通選択で下限AND任意上限を適用してから既存topへ渡す。正値制約・min/max関係エラー・空集合による入力取得の短絡を加えない。元Counterと全フィルタ前総数、全formatterのAPIを保つ。1.1の追加pytestのGREENと、top入力のspyによる選択順序・元Counter不変・formatter共有pairsの確認で検証する。
- [ ] 1.3 README.mdに`python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`の例を1つ追加する。入力`beta beta beta alpha gamma alpha delta`と期待JSON（beta3、alpha2）を同じ例に併記し、整数・省略上限なし・包含・min併用・0/負数/逆転は正常空結果・全除外時の上限調整・max前のHTML元総数を説明する。同じ掲載コマンドを実CLIで走らせるpytestを追加し、例のexit0/stdout/stderrとREADMEの内容を検証する。

## 2. 全体の互換性と独立検証

- [ ] 2.1 追加と全既存pytestを実行し、件数・環境・コマンド・exitを記録する。元総数の三条件ケース（beta4/zoo3/apple2/pear2/single1、min2/max3/top1→zoo3・総数12）、選択後11種類以上でのtop10、既存不正min/topとmax0/負数の組合せも確認する。全試験成功、既存試験の削除/回避なし、製品差分にCI・依存・見た目・無関係変更がないことをgit差分で検証する。
- [ ] 2.2 品質が対象headから実CLIを独立実行し、省略互換・包含境界・min併用・全除外・元総数を確認する。HTMLは既存の独立ブラウザ検証を通常幅と狭幅で行い、入力・argv・exit/stdout/stderr・HTML原本・実測/画像/通信検査を追跡可能に残す。PM向けにはVERIFICATION.mdとCLI/CIの文字の証拠文書を添付し、受入条件ごとの結果、閲覧画像の枚数・確認内容・結果を記す。PMに画像や圧縮ファイルの閲覧を求めず、未実施・未報告CIを成功扱いしないことを検証する。

## Workflow follow-up

- 仕様承認後の計画工程で本tasksに対応するPLANを作る。このカードでは製品実装・GSD取込み・PR作成・archiveを行わない。
- 受入後の最終化でOpenSpecをsync/archiveし、最終headを品質が確認する。Bot自身はPRをマージしない。
