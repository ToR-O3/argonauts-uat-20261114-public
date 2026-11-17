# 独立レビューと対応

## 回答反映後の独立レビュー（t_a78adc7b）

以下が現在の状態。後方の初回レビューは履歴であり、そこに記された未決/partialは現在には適用しない。

対象はBrief・PRD・open-questions・OpenSpec proposal/spec/design/tasksの回答反映差分。公式customizationを解決し、標準delegate_taskでadversarial・edge-case-hunter・structureを独立並列、structure結果を渡した別委任でproseを実行。全4レンズはexit_reason=completed、truncated=false。実装・ブラウザ検証は行っていない。

### adversarialの指摘一覧と判断

| lens | location | trigger_condition | guard_snippet | potential_consequence | 親の判断 |
|---|---|---|---|---|---|
| adversarial | design D-4 | 背景と文字色の組合せ未定 | UI-SPECで配色対を明記 | 環境依存で読めない | 明るい背景と全文可読性は既に必須。具体色と環境検証は予定済みUI-SPECへ引継ぐ。themeは追加しない。 |
| adversarial | spec HTML-3 | 例が1桁順位のみ | 順位10も狭幅確認 | 既定top10で崩れる | 全内容・3列可読性と既定top10の既存要求に包含。後続試験fixtureへの助言とする。 |
| adversarial | design Risks | 回数例が少桁 | 多桁数をformatterへ直接入力 | 数字がoverflow | 既存の大きな回数リスクと純粋部品検証に包含。後続試験具体化への助言。 |
| adversarial | spec HTML-1 | OS別basename規則がdesignのみ | 指定パスから実行OS規則で取得 | 実装間の差 | design D-2でPath(args.filename).name相当と規定済み。リンク先名への仕様拡張は行わない。 |
| adversarial | spec HTML-1 | 表外へのパス露出検証が不明 | 生成HTML全体も検査 | title等に漏れる | 入力名はbasenameのみ・動的値は名前/語のテキスト境界のみという既存規定を適用。全文に親ディレクトリ識別子がない確認は後続品質への助言。 |
| adversarial | PRD refinements | 空白保持と狭幅を別々に確認し得る | 空白入り名で双方確認 | CSS由来overflow | 全入力名の空白保持/全文可読性は必須。同一fixtureを使う試験具体化への助言。 |
| adversarial | tasks 3.1 | layout測定指標が未定 | 幅・列境界・切捨てを測る | ページ幅のみで誤合格 | 欠落/切捨て/重なり無しの必須条件は維持。具体採取法は既存ブラウザ手段を確認する計画で決める。 |
| adversarial | tasks 3.1/品質証跡 | 証跡の対応が不明 | fixture/command/HTML/viewportを対応付け | 古い証跡との混在 | 実HTMLと画像/DOM/layout/network記録の要求を維持。対応表は品質の記録方法への助言、製品日時表示は不要。 |
| adversarial | PRD refinements | 将来更新対象の記載がBrief/PRDのみ | OpenSpec/UI-SPECも整合 | 将来の文書間drift | 今回は全OpenSpecを更新済み。将来の回答変更は変更受付と同じ文書整合手順の対象。今回の4回答を未決へ戻さない。 |
| adversarial | 再承認gate | 承認対象版の記録先が不明 | commitと承認結果を特定 | finalを承認済みと誤解 | チームC.3のhead_shaと下流仕様承認t_fd2bd806の正常完了metadataが既定記録。finalは製品完了でも再承認済みでもないと本文に明記済み。 |

上記は追加機能や新たな人の判断を要する問いとしては採用しない。既存の受入条件を緩めず、後続UI設計・試験具体化・品質の注意として残す。

### edge-case-hunter

公式結果は `[]`（指摘0件）。他レンズの結果で上書きしない。

### structure

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Brief handoff/PRD Decisionsの親worker分担 | memlogへMOVE | 恒久要求と実行制約を分離する提案。今回は修正対象外の文書再編を避け、履歴として保持する。 |
| structure | PRD Review refinementsの可読性/fixture | RULE-6/SM-3へMOVE | 本文に既にFR/RULE/SMの要求と参照があり、詳細も全て保存済み。章構成は公式テンプレートと既存構造を維持する。 |

### prose

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | spec top後の順位「同じ入力をhtmlでtop1に指定する」 | `Zoo apple zoo APPLE beta` を `--format html --top 1` で集計する | 採用し、通常・同数シナリオも正式CLI表記に統一した。 |

### 現在の引継ぎ

Q-1〜4はt_0c7d0df4のblock後の人defaultコメント1794903097と正常完了run60で解決済み。Brief/PRDはcomplete/final、未解決なし。open-questions.mdは未解決なしのみとし、解決履歴はDecisionsとmemlogに保持する。役割のrevise手順に従い、未決事項の添付は省略する。原本はGitで確認可能。再承認は後続PMが行う。

---

## 初回レビューの履歴


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
