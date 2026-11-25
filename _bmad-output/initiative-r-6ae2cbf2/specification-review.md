# 要求・仕様の独立レビューと対応

対象: BriefとPRD原本。工程: r-6ae2cbf2 / full / 要求・仕様。

## 実行

BMAD Facilitateのrubric・fresh-reader・入力照合・編集レビューを文書作成時に実施した。ただし作成した子は再委任ツールを持たず順次レビューだったため、親が別の子を起動し、bmad-reviewのadversarial・edge-case-hunter・structureを独立して並行実行し、structure結果を渡した別の子でproseを実行した。いずれも通常終了、truncated:false。verification-gapはコード向けのため適用外。レンズから返った指摘のみを扱い、規定数に合わせて指摘を作らなかった。

## 指摘と判断

### adversarial

- 過去の封印済みHTML baseline原本と今回の期待値を区別する。採用: PRD Change boundary、OpenSpec design/spec/tasksで原本非改変と明示的変換または今回用期待値を指定。
- 過去snapshotを固定するブラウザ検証scope gateが今回の正当差分を拒否する。採用: 今回の合否と区別し、旧gateの無断緩和を禁止。
- DOM順序のみでは総数の「横」の証拠にならない。採用: PRDとdesign/tasksで通常・狭幅の実描画を指定。
- 既定topの誤りを候補10以下では観測できない。採用: PRDに候補12・top省略10とtop99で12の例を追加し、spec/tasksに反映。
- 語なし入力がFR-2で明記されていない。採用: 空白・記号のみを追加し、spec/tasksに反映。

### edge-case-hunter

返却指摘は `[]`。未実施ではなく、対象2文書と既存HTML/CLIを読んだ結果。

### structure

- PRDの結論を冒頭へ移す提案: 今回は見送り。公式テンプレートのDocument purposeの直後にVisionがあり、冒頭だけで目的と変更を読める。
- Brief What makes it different、PRD Stories、Developer experienceを統合する提案: 見送り。明示指定した公式テンプレートの必須節を維持し、各節を小変更に合わせて短くする方を優先した。具体例を保持する提案は維持。
- 文書作成制約を末尾へ集約する提案: 見送り。製品の契約と今回の文書作成のみの境界は既に明示されており、受入の意味を変えない編集のため。

### prose

- 「表示行の和」の合計対象、主語の「親」、列挙条件、略称「総数」、色による「緑」、DOM class/CSS表現の明確化が提案された。
- 受入に直結するFR-2の比較対象と実描画の総出現回数表記を明確化した。残る略称はGlossaryで定義済みの同じ値であり、テンプレート節の全面再編集や長文化は見送った。いずれも機能の不足や未決要求には該当しない。

## 結果と限界

機能上の指摘はPRDとOpenSpecへ反映した。未決事項はなし。Architectureは不要: 最終pairsと元総数が既存整形部品へ渡り、境界・依存・データモデルの新設計判断がない。OpenSpec designは過去期待値との整合と描画確認の局所判断だけを記録する。

この記録は仕様のレビューであり、製品のテスト成功やブラウザ確認を主張するものではない。実装・試験・独立ブラウザ確認は後続工程で実施する。PM向け判定資料は文字で渡し、生成されたBrief参考HTMLの閲覧を要求しない。
