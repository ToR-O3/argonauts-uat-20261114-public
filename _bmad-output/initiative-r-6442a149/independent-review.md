# 独立レビューと処置 — r-6442a149

対象：Brief、PRD、Architecture。実装の合格ではなく、仕様承認PMへ渡すための原本レビュー。

## 実施

- 公式bmad-reviewのcustomizationを解決。docsに適用するadversarial・edge-case-hunter・structureを別の独立委任で同時実行し、structureの結果を渡してproseを別委任で実行。通常終了・truncated=falseを確認。
- Architecture公式gateはlintに加え、rubric＋入力照合、reality-check、境界adversaryのfloor全2件を独立委任。原本はarchitecture/reviews/independent-*.md。
- Brief/PRD生成時のreview-*.mdは公式の逐次代替自己レビューであり、独立レビューとは区別する。

## adversarial — 全指摘と処置

| 項目 | 指摘箇所・発現条件 → 結果 | 処置 |
| --- | --- | --- |
| 1 | Brief SC-03とPRD OQ-1のcasefold判断状態が相違 → 期待値が分裂 | BriefにPRDの明示整理を優先する引継ぎ更新を追加。SC-03を未指定互換と新除外Unicode未決に分離。 |
| 2 | BriefのHTML総数・重複等が旧未決のまま → 再質問/誤判断 | PRD RULE-1へ対応付け、Brief Q-04と現行根拠も更新。 |
| 3 | #markerを語として登録してもCLI結果が同じ → 読飛ばし欠落を見逃す | PRD RULE-1とEX-2に読込処理の直接試験を追加。 |
| 4 | 重複試験がappleの同一表記だけ → 正規化重複不具合を逃す | apple/APPLE/aPpLeの重複例を追加。 |
| 5 | 除外後の同数順位例なし → 集合化等で順序が失われる | beta apple alphaからapple除外、残存初出順の例を追加。設計AD-2と一致。 |
| 6 | 全語除外の各形式の境界検証なし → 空結果/総数の不具合を逃す | PRDに空結果・総数0検査を追加。終了状態/専用文言はOQ-5へ。 |
| 7 | 失敗時stdoutと診断先未定義 → JSON等の出力汚染 | OQ-3へ明示追加。stderr/無結果は未承認提案としてPMへ。 |
| 8 | 記号等を不正と呼ぶ → 有効な数字やunderscoreまで拒否しうる | OQ-4を有効性未決と改称しfoo_bar/123/ハイフンの例を追加。 |
| 9 | LF/CRLF/最終改行なしが明示されない → 作成環境で結果が変わる | OQ-2へ追加。PM判断後に期待値を確定。 |
| 10 | 本文に一致しない非空一覧の不変検査なし → 非空経路の誤動作を逃す | PRD RULE-1とEX-1へ各形式の未指定結果一致を追加。 |

## edge-case-hunter — 全指摘

1. 最終改行なしの除外語を読むか判定不能 → OQ-2へ（上表9と重複）。
2. 残存同数語とtop境界の順序が曖昧 → 既存順位維持と具体例をPRD/EX-1へ（上表5と重複）。

## structure — 全提案

| 提案 | 処置 |
| --- | --- |
| PRD冒頭を目的→状態→次の判断、末尾予定の移動 | 大幅構造変更は保留。冒頭でdraft/partialを明示、次工程は末尾記録として保持。 |
| Quality/API/Developer experienceを統合 | 公式templateの採用節を保つ。単一機能には細分化だが、要求欠落防止のため今回は維持。 |
| Decisionsのtemplate採否を工程記録へ | 作成理由の原本を保持するため維持。製品要求と混同しない見出しを保持。 |
| Brief Problem/What makes it different統合 | 必須template節として維持。市場優位の主張をしない点を保持。 |
| Brief Scopeの製品/工程/現行根拠を分離 | 節は維持、HTML総数の状態矛盾は修正。 |
| 要求と検証具体例は保持 | 採用。短縮のため期待値を捨てない。 |

## prose — 全提案

1. Brief SC-03のUnicode留保を該当箇所に明記：採用。
2. Brief Scope/Q-04のHTML総数を現在の整理へ：採用。
3. draft/partialを日本語説明へ：文書の状態を示す標準値として保持。PM引継ぎで説明する。
4. PRD末尾の工程予定の時点明示：PRD作成時点の予定として追記する。
5. 設計のcasefold/strip/UTF-8/汎用exit2の保留対象を具体化：採用。
6. ratify/本高度/schemaの一般的表現化：ratifyは追認へ。残りは設計用語として許容。
7. ステークスを影響度・リスクへ：仮定の文脈を維持し、機能要求に持ち込まない。表現改善は必須でないため保留。

## Architecture gate

reality・adversaryはPASS、rubricはdiscussion用途CONDITIONAL PASS。casefold済み情報だけで新比較を先に固定しないという改善を設計本文へ反映。OQ-1回答後、設計担当による比較境界再確認を明記。製品未決はopen-questions.mdへ引き継ぐ。入力の静的照合と公式lintは実装の合格を意味しない。

## 結論

依頼の六条件と検証方法を保持した仕様承認用の原本を用意した。BMADは未決があるためpartial（文書は草案）、設計のfinalはdiscussion原本の確定状態で、実装承認ではない。仕様・GSD計画・実装の合格をこのレビューで代行しない。
