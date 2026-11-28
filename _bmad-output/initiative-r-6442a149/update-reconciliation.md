# Update 入力照合・memlog監査

対象：Brief／PRD／設計、intent:update、headless:true。既存原本と各memlogを再開してから公式template merge、入力・現行コードを実読した。任意の既定テンプレートライブラリ2箇所は未配置で、要求テンプレートbrief/prdは解決・merge済み。architectureは公式spine template、headless、reviewer-gateをロード済み。

| 入力・維持条件 | 本文への収容 |
| --- | --- |
| 受付、人default原文、回答日時、PM判断、差戻し | 三原本の冒頭、decisions-oq1-6.md |
| 1 casefoldとSTRASSE／Straße、比較境界の情報損失再確認 | PRD FR-3、設計AD-3、Brief SC-03。tokenizer.py:6-18／aggregator.py:6-17実読 |
| 2 strip、先頭#のみ、各改行 | PRD FR-2、設計AD-3、Brief SC-02 |
| 3 UTF-8先頭BOM、全読込失敗対象原因stderr／exit2／stdout空 | PRD FR-2／FR-4、設計AD-3／AD-4、Brief SC-04 |
| 4 全体一語、文字列例、重複、最後FILEのみ | PRD FR-1／FR-2、設計AD-2〜AD-4、Brief SC-01／SC-02 |
| 5 全語除外の既存空結果・exit0・専用文なし | PRD FR-6、設計AD-2、Brief SC-06。既存HTML案内を消さない |
| 6 既存引数検証→除外→本文、複合失敗のexit | PRD FR-4、設計AD-4、Brief SC-04 |
| 全形式min-count/top前、残存回数・相対初出順、HTML総数境界 | PRD RULE-1、設計AD-1／AD-2、Brief SC-06 |
| OQ7/8のみ、背景不足は停止／追加条件でない | 三原本とopen-questions.md |
| help／README／試験は後続、今回は文書のみ | 三原本のscope／change boundary、FR-5、設計Deferred |

旧memlogの未決判断は当時の状態としてset asideし、明示回答による解決をappend-only追記した。経済効果・利用者の推定A-01〜A-03は確定事実にしない。旧The ask／Visionの除外とPRD optional節採否は既存理由を維持し、新しい製品条件や架空の義務は作らない。手順・過去試験実行の履歴はmemlogに置き、今回の機能合格根拠にはしない。

Finalize順序：監査→入力照合→独立レビューと設計ゲート→背景OQの非阻害保留→structure/proseの明確な修正→ID/TOC再検査→外部handoffなし→Close。機能試験・全件回帰は実行せず、文書のlint/ID検査と独立読解レビューに限る。
