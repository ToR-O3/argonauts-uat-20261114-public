# Brief・PRDの独立レビュー

対象: brief/brief-wordfreq-max-count.md と prd/prd-wordfreq-max-count.md（双方全文）。製品実装のレビューではない。

bmad-reviewの公式resolve_customizationで選ばれたdocs向けレンズを独立したdelegate_taskで実行。adversarial・edge-case-hunter・structureを同時実行し、structure結果を渡してproseを別に実行した。全4件ともexit_reason=completed、truncated=false。verification-gapはapplies_to=codeのため対象外。

## Findingsと扱い

### adversarial

|番号|指摘|処置|
|---|---|---|
|1|全除外時にmin-countを下げるだけのREADME案内では上限除外を解消できない|採用: FR-6にmax-countを上げる・省略する案内の修正を明記|
|2|0・負数・逆転の正常空結果をREADMEでも説明すべき|採用: FR-6に明記|
|3|試験表の総数期待をtext/jsonへ誤適用し得る|採用: HTMLのみの期待と明記|
|4|max1で単発語が残る直接試験がない|採用: gamma1・delta1のケースを追加|
|5|max指定時に既定top10を直接試験しない|採用: 選択後11種類以上のケースを追加|
|6|min/max/topがそれぞれ除外する時の総数確認がない|採用: 三条件と元総数を区別するケースを追加|
|7|空集合経路と不正min/topの組合せがない|採用: 入力読込み前exit2のケースを追加|
|8|helpのexit・出力先・入力不要の確認がない|採用: ファイル引数なしhelp試験を明記|
|9|未指定互換の期待バイト列の出所が曖昧|採用: 既存原本または変更前固定期待値を使いexit/stderrも照合|
|10|README例に入力と期待結果を添える保証がない|採用: 1つの例に入力本文・期待JSONを併記|

### edge-case-hunter

公式結果: `[]`。追跡可能な挙動の欠陥の指摘なし。

### structure

|指摘|処置|
|---|---|
|FR-6が長い試験表で分断される|採用: FR-5直後へ移し、検証設計を小見出しに分離|
|Briefの導出を短縮してPRDへ集約|不採用: 今回はPMがBriefだけでも原文と導出を区別できることを優先。要件の矛盾はない|
|RulesとQualityの共通制約を統合|不採用: 指定テンプレートの節とIDの安定を優先し、小規模な重複を許容|

### prose

正常入力の意味、今回の文書作業と製品変更の区別、CLIオプション指定順、top1/top2別の期待結果、未指定互換の修飾、README例の入力、境界比較、包含の説明、逆転の対象の9点を採用した。

## 結論と残り

挙動の未決事項なし。利用者像の非阻害推定は各文書のAssumptionsに残す。新Architectureは既存共通filterの局所変更で境界/API/依存を変えないため不要。最初の作成子が残したreview-*はセルフレビューであり、この独立レビューとは区別する。新機能の実装・pytest・品質のブラウザ確認は未実施で、実装工程以降に残す。
