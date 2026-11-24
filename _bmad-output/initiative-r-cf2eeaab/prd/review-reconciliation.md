# Input reconciliation

実施方法: 同一担当による入力別照合。独立したサブエージェント照合ではない。

## Brief全文

- 旧依頼、description不存在、最新判断の時刻・原文・優先関係を保持。
- 完成値と二重追記禁止、AC-1〜AC-3、製品1項目限定、工程文書許容、テスト範囲外を保持。
- full固定、architecture変更不要、smartでも人がマージを保持。
- 差分: Briefの一般BMAD次工程案内は、本カードの明示的なPRD→OpenSpec→仕様承認PMで置き換えた。意図した上書きであり欠落ではない。
- 文体: 小さな確定依頼であり、市場需要・架空利用者・収益目標を持ち込まない。

## 本カードのCONTEXT・TASK

- headless:true / intent:create / template:prd、John、指定libraryと出力先を採用。
- 文書のみ、kanban/commit/push禁止、検証ファイルの置き場許容を保持。
- 親の別委任による独立レビューを明記し、セルフ確認と混同しない。

## initiative全文

題名のみ。旧依頼の題名を完成値の根拠にせず、最新判断を優先した。

## 現物pyproject.toml全文

descriptionなし。name/version/dependenciesおよび他セクションの不変条件に反映。現物に製品変更は行っていない。

## Verdict

重要な欠落なし。入力から解消済みの不存在を未決へ戻さず、後続工程ゲートと依頼の未決事項を区別した。
