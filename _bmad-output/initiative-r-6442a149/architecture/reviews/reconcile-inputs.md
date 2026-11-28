# Input reconciliation — sequential fallback

独立委任ツールなし。著者による公式逐次代替であり、親の独立照合を置換しない。

| 入力 | 照合結果 |
| --- | --- |
| PRD全文 | FR-1〜FR-6・RULE-1〜RULE-2はCapability mapで接続。HTML総数・重複・絞込みをAD-1/2へ反映。FR-4は単独不存在に限定し文言完全一致・出力先を追加しない。FR-5の説明・試験は後続へ。OQ-1〜OQ-8は参照保留、追加受入条件なし。PRD末尾の要求整理・独立レビュー待ちはdiscussionのまま保持。本設計は製品未決の承認ではない。 |
| initiative frontmatterのみ | type/title/parentのみ読み、Requirementsや親spineの存在・承認を推定しない。 |
| wordfreq/__main__.py | 既存の引数、本文取得exit1、count→total→min-count→top→formatを確認。除外未実装。ADは読取り失敗の時間的優先順位を固定しない。 |
| wordfreq/sources.py | FileSourceの本文UTF-8/InputError契約を確認。除外FILEへの流用はOQ-3として保留。 |
| wordfreq/tokenizer.py | 本文Unicode抽出とcasefoldを確認。未指定維持、新除外比較はOQ-1へ。 |
| wordfreq/aggregator.py | I/Oなしの計数、初出順を保存する安定順位、非破壊topを確認。型・シグネチャはseed。 |
| wordfreq/formatters.py | 純粋整形、HTMLのcaller-supplied total、空結果文を確認。除外I/Oを持たず、専用空結果文はOQ-5へ。 |
| wordfreq/__init__.py | package説明のみ。追加の構成制約なし。 |

判定: 逐次照合の範囲で脱落なし。新機能の実装・実CLI試験・既存回帰試験は行っていない。親で上記各入力とspineの独立照合が必要。
