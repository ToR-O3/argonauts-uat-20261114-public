# 入力照合（順次fallback）

独立subagentではなく同じ担当の照合。親の最終独立レビューが別途必要。

| 入力 | PRDへの反映 | 省略・保留 |
| --- | --- | --- |
| 依頼全文・固定制約 | FR-1〜4、RULE-1〜6、SM-1〜4 | 背景・順位列はOQ-1/2。未承認の総数/basenameはOQ-3/4 |
| Brief | HTML・表前の文脈・簡素UI・全形式順序・安全性・範囲外 | A-1は仮説継承、人物像の追加質問は実装境界を変えないため初回feedbackへ |
| Brief memlog | 未承認仮定、partial、CI/依存制約、実在検証ファイル、独立性の制限 | Brief資料ビューは製品HTMLの証跡にしない。PRDビューはoffer未承諾のため作らない |
| 既存spec | FR-4、RULE-1〜3、SM-4に互換性契約 | 同数語昇順のみ意図的変更。旧IDとPRD IDは別名前空間 |
| wordfreq/全6ファイル | text/count TAB word、JSON配列、UTF-8/FileSource、tokenizer/casefold、部品境界 | 新formatter署名やCSS詳細はdesignへ |
| CONCEPTS | 正規化責務、旧順位からの移行、異なるhashseedの再実行 | CONCEPTS自体はPRD作業で編集しない |
| initiative | 題名・配置 | Requirements未記載を承認扱いにしない |

重要な入力の欠落は見つからない。browser画像・layout/networkは将来受入条件で、実行済み証拠ではない。
