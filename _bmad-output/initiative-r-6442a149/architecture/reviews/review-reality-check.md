# Configured floor 1 — evidence / reality check

対象: ../architecture.md。設定の第1 lens（全committed decisionの現行根拠確認）。委任不可の公式逐次代替、著者による確認で独立性なし。

判定: この限定範囲の逐次確認ではcritical/highなし。webによる新技術選定は該当なし。親の独立確認待ち。

| Assertion | Reality check |
| --- | --- |
| CLI合成・単方向処理 | wordfreq/__main__.py:7-10,29-48。取得→tokenization→計数→総数→min-count→top→formatter。 |
| 純粋計数・順位 | aggregator.py:6-17。入力取得なし、同数は挿入順を保持する安定sort。 |
| formatterは読取りしない | formatters.py:6-27。text/json/htmlの文字列整形、HTML totalはcaller提供。 |
| 旧本文casefold | tokenizer.py:14-18。新除外時のcasefoldに拡張していない。 |
| 本文失敗exit1 | sources.py:17-22と__main__.py:29-33。除外への自動流用なし。 |
| HTML総数と重複 | PRD RULE-1明示。新規推測や追加受入条件でなく入力要求。 |
| 依存・権限・外部送信を追加しない | PRD RULE-2と依頼の拘束。実装完了や実測証拠とは主張しない。 |

新framework/library/starter/versionを採用・固定しないため外部version検索は不要。現行技術の最新版だという主張もない。現行ファイルの観察をseedとし、永続schemaの新設はなし。

処置: 根拠を維持。独立レビューの不足のみ親へ引継ぎ。
