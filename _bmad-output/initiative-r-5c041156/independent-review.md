# 独立レビューと対応

対象: 本initiativeのBrief・PRD。最終境界条件レビューではOpenSpec `r-5c041156-wordfreq-html` のproposal/spec/design/tasksとopen-questions.mdも全文対象とした。親workerが公式 `bmad-review` のcustomizationを解決し、各レンズを別の標準delegate_taskで実行した。全委任は通常終了、truncated=false。ここは結果と対応の要約であり、製品試験の証拠ではない。

## 反証レンズの指摘と対応

| location | trigger_condition | guard_snippet | potential_consequence |
|---|---|---|---|
| AC-1 / FR-1 | 文字コードと保存の関係がない | UTF-8とcharset、日本語再表示を明記 | 文字化け |
| AC-3 / SM-3 | ウィンドウ縮小だけでmobile扱い | 実mobile viewport/emulationと測定を指定 | 縮小表示で読めない |
| AC-3 / RULE-6 | 横スクロールの可否が曖昧 | ページ/表とも横overflowなし、縦は許す | 回数との対応を失う |
| Solution / FR-1 | 見た目だけの表になり得る | semantic tableとscope=colを指定 | 支援技術が列を追えない |
| SM-2 | casefold例が語昇順と同じ | ZOOから始まる衝突例へ修正 | 統合時の誤sortを見逃す |
| AC-6 / SM-4 | 空ファイルだけで0語を確認 | 非空の記号/空白のみも追加 | 入力長と総数の混同 |
| Solution / RULE-2 | 同一パスへ保存できてしまう | シェル切詰めの境界と禁止を説明 | 入力データ消失 |
| AC-3/5 / SM-3 | browser採取手段が未定 | 計画で既存手段確認、なければ未検証 | 捏造や禁止依存追加 |
| A-2/3 / OQ-3/4 | 否認後も推奨例が残る | 仕様修正・期待値更新・再承認を明記 | 未承認案の実装 |
| AC-5 / RULE-4 | 不実行だけで文字一致を見ない | DOM textContentと原文照合 | 二重escape/欠落 |

これらはPRD Review refinementsとOpenSpecの仕様・design・tasksに反映した。ユーザーの追加要求ではなく、仕様承認対象の受入具体化案として区別した。

## 境界条件レンズ

初回の結果は文字コード整合と名前内空白折畳みの2項目。前者は上記と重複、後者はpre-wrap等による保持とDOM文字列一致を追加した。重複指摘を削除した合格扱いにはしていない。

更新版全成果物の再レビューで1項目:

```json
[{"lens":"edge-case-hunter","location":"design.md D-3/D-4","trigger_condition":"入力名にCRまたはCRLFを含む","guard_snippet":"escape後にCRを&#13;等で保持し、DOM textContent一致を検証する","potential_consequence":"HTML解析の改行正規化で元文字列を失う"}]
```

対応: design D-3へCR参照の方針、specの非ASCII/空白シナリオへLF/CR/CRLF、tasks 2.1とPRDへ検証条件を追加した。追加の製品実行はまだ行っていない。

## 構成・文章レンズ

構成はBriefのAC-6小項目化を適用し、冒頭の互換性警告と定義/仮定/未決の別章を保持。PRD Change boundaryをVision直後へ移す提案は採らず、テンプレート順を維持した（冒頭とFR-3に同じ重要境界がすでにあり、判断情報は後ろだけにない）。

構成結果を渡した別の文章レンズは6項目を返し、すべて反映: 背景/順位列の「未決」を明確化、提供側の構造維持責務、検証の目的語、想定journeyの接続、hashseed比較を形式内と明示、DOM解釈とscript/event実行の区別。

## 未決と検証の区別

現時点の承認質問は背景・順位列（採用時の採番を含む）・総数top前の解釈・basename案。利用者仮説は将来feedback対象。既存の語昇順は今回明示的に置換する契約で、仕様矛盾や未決として扱わない。

OpenSpec厳格検証では旧シナリオ名の削除が拒否されたため、旧名を同期識別子として残し、WHEN/THENを初出順へ明示的に変更した。旧語昇順を残すという意味ではない。文書冒頭の承認注意はarchiveされないためproposal/design/open-questionsへ置き、各条件付き要件にも未承認を明示した。

BMADはpartial/draft。Briefに付随するHTML資料ビューは初回ドラフト時の補助スナップショットであり、承認原本はMarkdown。製品HTMLの動作・安全性・外部通信の証拠には使わない。製品コード・CIの変更と製品ブラウザ試験は本工程で行わない。
