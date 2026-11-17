# 公式 bmad-review：structure / prose

本書は、要件・実装・品質担当がmin-countの最小拡張と受入境界を共有するためのBriefである。reader_type=humans、既定Microsoft Writing Style Guideを日本語の技術文書に適用し、structureはStrategic/Context（Pyramid）を採用した。両レンズは公式resolveと各参照指示に従って逐次実施した。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §問題 180語、§解決策253語、§範囲312語ほか。ACと説明が重複 | CONDENSE: 機能の判定詳細をAC表へ集約し、背景は短文化 | 最終は各88/204/250語。総計2629→2141語、488語（18.56%）削減。AC・根拠・未決を落とさない。 |
| structure | §成功基準の7件、§仮定、§未決事項 | PRESERVE: 検証条件と推定の分離を維持 | Briefの信頼性と後工程の判断に必要。詳細な実装案・旧品質手順の展開は追加しない。 |
| prose | 「空状態の説明の適切さは制約として受け入れる」 | 「見た目不変の制約に従い、既存の空状態文言も維持する」 | 適切さについて利用者の未取得の承認を示唆しない。 |

日本語の技術語・確定条件の直接表現は維持した。proseはstructureが圧縮した箇所の旧表現への追加修正を避けた。

全提案は作成者として採用し本文へ反映済み。要件を増やす変更はない。word_metricsの日本語分割込み総計2141語、frontmatter/目次/仮定を除いた本文はjq抽出→wc -wで215語。日本語の空白ベース語数はページ数の指標ではないため、1〜2ページのBriefに向けて圧縮したが印刷ページ数は未測定とする。削除で理解上の契約は失っていない。Q-01/Q-02の未確認は編集で解決せずpartialに保持する。

## 再確認

reconciliationが挙げた承認先取り表現は修正済み。rubricの高い懸念は解消し、残りは明示した利用背景の推定だけ。目次は最終見出し順と一致し、公式check_idsのundefined/duplicate/withdrawn/tocは空。ACの複合IDはツールが認識しないため、7件の一意な定義と参照を別途照合する。A-prefixとUTF-8のunknown_prefixは未定義要件ではない。

文書HTMLは公式render_viewで生成した。公式rendererが既定でCDNをロードすることを確認したため、生成物だけをオフライン化（CSPでscript/外部取得禁止、CDN URL空、ロード呼出し除去）した。日本語の見出しはdata-restのescaped fallbackに保持される。これは文書ビューであって製品HTMLやブラウザ合格証拠ではない。スキル原本・製品の見た目は変更していない。
