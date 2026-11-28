# Revision review — PRD / rubric-planning

## Verdict

**PASS（軽微な明確化提案のみ、実装前の製品ブロッカーなし）**。承認済み5決定が安定したFRと受入例・説明要求・検証要求へ展開され、既存互換を壊さずにBuilderと品質担当が使えるfeature-level要件になっている。

これは文書rubricの判定であり、後続仕様承認・実装・試験合格・受入の承認ではない。

## 優先する修正（最大3件）

必須修正はない。任意の改善は1件のみで、指摘数を埋めるための追加要求はしない。

1. **Low / Success metricsの判定語**: SM-1 / SM-2の「検査できる」を「対象シナリオの検査がすべて合格する」に置き換えると、試験の存在と製品の受入結果をさらに区別しやすい。新たな数値目標や機能の追加は不要。

## 評価範囲・根拠

公式 `bmad-facilitate/references/rubric-planning.md` 全文、および `guidance-planning.md` に基づく。対象本文、同runの `.template.md` / `.memlog.md` 全文、更新Brief、`../decision-update.md`、`../source-context.md`、`../open-questions.md`、architectureを読んだ。過去のreviewは今回の合格根拠にしていない。原本を編集せず、実装やgit操作も行っていない。

想定stakesは非規制・非契約の小規模ローカルCLI変更。本文のfeature altitudeを受け入れ、架空人物や大規模リリース計画の不足を指摘しない。実際の実装挙動や試験合格は今回検証していない。

## Dimensions

| Dimension | Rating | Findings（severity / location / fix） |
| --- | --- | --- |
| 1. Decision-ready | strong | FR-1〜FR-7が機能、行解釈、同一視、失敗と優先、出力、説明、互換証拠を分担する。5決定の出典・時刻・採用内容と後続承認の境界が明示される。阻害指摘なし。 |
| 2. Earned | strong | 架空の人物や事業成果、generic NFRを置かず、単一CLIのcapability specに絞る。Qualityの統合と非該当節の省略には理由がある。CLI契約の細部はこのfeature altitudeで誤実装を防ぐため必要。阻害指摘なし。 |
| 3. Testable | adequate | FRの入力・結果・失敗・順序は検査可能。**Low: Success metrics、125–126行。** 「検査できる」は試験可能性とも読めるため、任意修正として対象検査の全合格を成功と表す。FRの受入例、FR-7、Storiesに合格対象が既にあるためブロッカーではない。 |
| 4. Honest scope | strong | Non-goals / MVP / Change boundaryで増やさない範囲を固定。背景と文書構成の推定はAssumptionsにタグ付きで分離する。5決定は承認入力由来であり、現在未決なしとの記述も共通正本に一致。阻害指摘なし。 |
| 5. Usable downstream | strong | 用語定義、安定ID、FR別受入例、既存版を用いた互換検証方針がある。architectureのAD-1〜AD-4とも整合する。提供された `../checks/revision-check-ids.json` はundefined / duplicate / withdrawn / ToC問題なし（UTF-8は符号化名であり要求IDではない）。阻害指摘なし。 |

## Template Done when

- **Every FR can be checked: 適合。** FR-1は基本除外と未指定互換、FR-2は処理順と行文法、FR-3はcasefold、FR-4は診断・終了コード・本文未読、FR-5は全形式と選択規則、FR-6はhelp / README、FR-7は検証対象と互換原本を指定する。
- **FR traces to a journey or need: 適合。** 単一CLIなのでUJ-IDや架空人物を増やさず、Users and journeysと原依頼の必要性で根拠を示す。準備→実行→結果または失敗認知の各beatはFR-1 / FR-2 / FR-3 / FR-5、FR-6、FR-4により支えられ、検証をFR-7が担う。
- **Non-goals / out-of-scope: 適合。** Non-goals、MVP scope、Change boundary、Rulesで明示。複数FILEの新仕様や正規化変更等を持ち込まない。
- **Success metrics / counter-metrics: 適合（上記Lowの表現改善余地）。** 各SMが対象FRと互換・既存エラー・依存等の対抗指標を示し、未実装という現状も隠さない。
- **Shape fits product: 適合。** 単一ローカルCLI向けのcapability-first構成で、対象外のconsumer UX、運用SLO、規制などを膨らませない。
- **User owns decisions / no invention: 入力照合上適合。** 5件はdecision-updateの明示採用に一致する。既存casefold等は継承契約に分離され、利用背景・構成判断はAssumptionsに残る。依頼者の記憶そのものは無人レビューでは確認不能だが、ユーザーの新規発言や承認は捏造していない。

## 採用決定との照合

| 決定 | 反映先と評価 |
| --- | --- |
| 1. HTML元入力総数維持 | Glossary、FR-1 / FR-5、Change boundaryに整合。全件除外・閾値・空本文の例もあり。 |
| 2. trim後判定 / LF・CRLF・最終改行なし | FR-2に処理順と具体例、FR-6に説明、FR-7に検査要求。 |
| 3. UTF-8 / 全読込み失敗exit2 / 出力抑制 / 本文exit1維持 | FR-4でファイル名と理由を示す診断、stdout空、HTML / Tracebackなし、本文契約維持を規定。FR-6 / FR-7も一致。 |
| 4. 既存 `\w+` 全体一致 / 不正行診断 | FR-2で検証後casefoldを明記し、数字・underscoreと全不正行例を区別。FR-4でファイル名・行番号・exit2を規定。 |
| 5. 引数→除外→本文 / 本文未読 | FR-4で順序と複合失敗の受入例、FR-7で本文未読を含む検査、CLI契約で既存引数エラー維持を明示。 |

Critical / High / Mediumの指摘はない。本文はそのまま親の残りのレビュー工程へ渡せる。追加機能の実行結果を未実施と明示しているため、この文書PASSを実装PASSとして扱わない。
