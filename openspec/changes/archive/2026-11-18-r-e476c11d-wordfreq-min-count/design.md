# Design

## Context

動機・範囲はproposal.md、観測可能な契約はspecs/wordfreq-cli/spec.mdを参照する。現行CLIはargparse検証→入力取得→count_words→元総数の計算→top_words→formatterの順で、formatterは純粋な表示部品。今回の横断点はCLIと共通の表示対象選択である。新しいサービス・データモデル・依存はなく、別立てのBMAD Architectureは不要と判断し、この文書で最小設計を記録する。

## Goals / Non-Goals

**Goals:** 元集計・総数と表示対象を分離し、全形式が同じ選択結果を受け取る。既存の2引数`top_words(counts, n)`利用とformatter APIを壊さない。

**Non-Goals:** フォーマット別の閾値実装、CSS・HTML文言変更、パーサー独自仕様、広域リファクタリング、既存CIや依存定義変更は行わない。

## Decisions

1. **引数検証を読込みより先に行う。** 既存topと同様argparseのint変換と正数検証を用い、default=1を設定する。独自の桁上限・字句規則・環境制限解除は追加しない。重複指定も通常のargparse単一値と同じ。読込み後の検証や出力別検証はエラー優先度を崩すため採らない。
2. **元のcountsを保持して別の表示対象を選ぶ。** 元総数を先に計算し、元countsを破壊しないフィルタでcount>=min_countだけを取り出してから既存top_wordsで順位付けと制限を行う。フィルタは初出の挿入順を維持する。CLIの合成部分でこの選択を1回行い、全formatterに同じpairsを渡す。既存top_wordsの公開呼出契約を変える必要はない。元countsをin-placeで削る案はHTML総数と既存部品契約を危険にするため採らない。
3. **formatterは変更しないことを基本とする。** HTMLへ従来どおりbasenameと元totalを渡す。空pairsで既存の空状態を使い、text空文字・JSON空配列も既存部品に任せる。閾値専用のHTML表示・新しい空状態文言は加えず、全件除外時の対処はREADMEに記す。
4. **TDDと実CLI、比較元headの証拠を分ける。** 実装着手前head・入力・argv・環境を記録し、従来出力と既定HTML画像を保存する。新試験を先に失敗させ、実装後pytest全件と実CLIの全形式を確認。HTMLは品質が独立再生成し、同じブラウザ/フォント/viewport/DPRで既定表示を比較し、フィルタ・全除外・長い語/名前の可読性と静的安全性を既存契約に従い検証する。出力だけではフィルタとtopの内部順序を区別できないため、品質は該当ソースの行またはdiffも証拠にする。

## Risks / Trade-offs

- 元集計の削除でtotalが減る → 元countsを不変にし、部分表示・全除外のHTML総数を試験する。
- 表示形式ごとの条件差 → 選択は共通経路で1回、三形式の同じ期待pairsをパラメータ化試験。
- 同数初出順やUnicode合算が変わる → 同数境界・casefold合算が閾値に達する試験を追加。
- 抽出0語とフィルタ全除外の混同 → 空/空白/句読点入力のtotal0と、語あり全除外の元total正を別々に試験。
- 既存空状態の案内は閾値全除外に最適でない → 見た目変更の禁止を優先して文言は維持、READMEに閾値を下げる案内を追加する。
- 比較環境差や既存CI未報告 → 環境と対象headを明記し、未実施/pendingを合格扱いしない。CIを待つ仕組みや追加CIで回避しない。

## Migration Plan

データ移行・新依存導入は不要。既定1によって既存コマンドの出力を維持する。ロールバックは当該機能のコード・試験・README差分の通常revertで足り、入力ファイルは変更しない。push/PR/マージは担当カードとチームの既定工程に従う。

## Open Questions

機能・設計の未決判断はない。利用者像・負担、理由・期限の背景確認Q-01/Q-02のみ`_bmad-output/initiative-r-e476c11d/open-questions.md`で仕様承認PMへ渡す。これらは方式・仕様・タスク分割を変える必須入力ではない。
