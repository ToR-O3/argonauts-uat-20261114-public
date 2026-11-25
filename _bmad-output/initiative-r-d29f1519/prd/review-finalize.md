# PRD — Finalizeと実行検査

## 順序と処置

1. memlogを監査し、全項目を本文・前提・OQ・除外理由に対応づけた。
2. ユーザー依頼、README、initiative、入力Briefをreview-reconciliation.mdで個別突合。入力の脱落なし。
3. rubricとfresh-readerを逐次実施。環境に子委任ツールがなく、独立レビュアーの合格とは扱わない。
4. A1-A4とOQ-1〜OQ-5をtriage。文案、省略、基準、5領域を未確認のまま承認せず、PM仕様承認と検証計画へ保留。
5. 公式bmad-review structure→proseで3節の重複を圧縮。216語（総数比6.01%）削減、引用文・境界・OQは保持。前提は最終の専用節にまとめた。
6. 見出しと目次の整合を確認し、check_ids.pyを再実行して全エラー空。
7. headlessのため対話の読了待ちはしない。
8. external_handoffs=[]。設定上の外部操作なし。
9. updatedを設定してdraft／partialでClose。on_completeは空。html_view:offerは承諾のない無人実行なので省略。

## 実行した公式CLI

- resolve_customization.py: pmのagent/workflow、facilitateのworkflow、校正のbmad-review workflowを解決。activation、永続fact、追加reviewer、external_handoffは空。
- resolve_config.py: core.output_folderを解決、core.active_initiative未設定につき明示出力先を採用。
- list_templates.py: --brief一覧を全文確認後、--template prd --mergeで.template.mdを生成し全文読了。任意の標準2フォルダだけmissing。orphaned/unreachable/order_problemsなし。ユーザー指定のprdは利用可能。
- memlog.py init/appendで入力・事実・固定判断・前提・条件節処置・校正・Closeを記録。
- check_ids.py: undefined／unknown_prefix／duplicate／withdrawn／tocはすべて空。FR=1、RULE=4、SM=3、OQ=5を定義。
- word_metrics.py: 初稿3592→最終3376。前文25・目次251・前提132を除く本文2968でinitiativeの約3000語目安内。
- jqで本文だけを抽出しwc -w: 175。日本語の空白区切りでは過少計数になるので公式word_metricsを併記。

## 製品不変と範囲

開始HEAD `69b97f1c9dfa7211367a9bdd0af885d80d8bf380` に対する全tracked差分は空。READMEのdiffは空で、git blobは開始HEAD・作業ファイルとも `3625ed42efa55c9929e47952698c25decd5050b7`。未追跡を含むstatusの追加は指定initiativeのbrief/とprd/内だけ。既存initiative、他の要求、製品ファイルは変更していない。

本カードでは製品テストを作成／実行していない。変更後の文案完全一致・一行単独の意味判別・非対象バイト比較・全差分の検証は、PM承認後の計画・実装担当と品質担当へ残す。指定5領域の具体名は不明で、推測した除外リストは作らない。

## 次の担当

PM仕様承認でOQ-1〜OQ-4を解消し、OQ-5を再確認する。必要ならSofiaがinitiativeのRequirementsを更新して計画・実装へ。Architectureは機能・構造変更がないため不要。実装単位が終わるごとにPRDをUpdateする。これは外部handoffの実行や承認取得の報告ではない。
