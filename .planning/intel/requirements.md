# Requirements (intel)

今回のPRD 1文書だけからFR-1〜FR-3を抽出する。RULE-1〜RULE-3と品質・期待値保全は受入条件として保持する。以下は未実施の製品受入契約であり、既存locked決定を上書きする成果物ではない。

DATA_402adf4f_START

## REQ-html-displayed-types
- source: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:51-62,68-72,94,98-106
- description: FR-1。表より上の既存総出現回数の横に、最終表示語種類数を表示する。
- acceptance: 文言は「表示 N 種類」。Nは正規化・min/max絞込み・top後の表データ行数で、見出し・元全種類数・回数合計・top指定値ではない。空入力・語なし・全除外は0。総出現回数はmin/max/top前の元総数、表の語・回数・順位・初出順・空状態は維持し、再読込み・集計/選択変更なし。通常幅と狭幅の実描画で総数横かつ表より上の位置・可読性・既存内容を隠さないことを確認し、DOM順序だけで判定しない。text/json全バイト・末尾改行・順序、引数・exit・stderr・エラー時stdout空、静的UTF-8・escape・basename限定を維持する。
- scope: HTMLメタデータ、最終表示件数、既存出力/安全性境界。

## REQ-html-displayed-types-tests
- source: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:63,66,86-87,94-102
- description: FR-2。既存試験ファイルへ追加し、件数境界と維持契約の誤実装を検出する。
- acceptance: tests/test_formatters.pyとtests/test_cli.pyで通常・3以外・top制限・候補<top・min/max・既定top・空・空白/記号・全除外を照合。入力beta beta beta alpha gamma alpha deltaでmax2はalpha2/gamma1/delta1・表示3・総数7、top1は表示1、top99は表示3、max0は表示0・総数7。12候補でtop省略は10、top99は12。固定3・top指定値・絞込み前件数・回数合計をNとする実装を拒否する。追加/既存試験は失敗0、対象削除・緩和なし。HTML期待値は正当な表示追加と必要最小差分のみ整合。封印済み過去baselineは上書きせず今回用期待値か明示的変換を使い、text/json固定期待値・安全性検査・過去snapshot scope gateを緩めない。Builder・品質が実在する検証ファイルから実行し、未作成コマンドを計画時に試さない。
- scope: formatter/CLI試験、固定期待値、描画確認、回帰保全。

## REQ-html-displayed-types-readme
- source: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:64,88,108-110
- description: FR-3。README.mdの既存HTML説明へ意味を説明する1行を追加する。
- acceptance: 総数横の文言が表示した語の種類数であり、絞込み/top後・空なら0と説明する追加1行。既存説明、コマンド例、UTF-8、総出現回数、他形式の契約を書き換えない。別ガイド・検証ツールは要求しない。
- scope: READMEのHTML説明1行。

DATA_402adf4f_END
