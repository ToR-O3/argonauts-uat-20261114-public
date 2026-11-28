# 入力原本と照合根拠

## 依頼原文

> wordfreq に --exclude FILE の選択肢を足す。FILE には集計から外す単語を1行に1語で書く（空行と # で始まる行は読み飛ばす）。大文字と小文字は区別しない（今の集計と同じく小文字にそろえて比べる）。FILE が無い時は、分かる文で終了コード 2 にする。--help と README.md の使い方に説明を足し、試験を足す。

受入条件として指定語除外、空行/#行無視、既存正規化で大小同一視、FILE不存在stderrとexit2、help/README説明、試験追加、未指定互換が提示された。新依存・外部通信・CI変更は不要。Unicodeはcasefoldを維持しlowerへ変えない。HTML総数は既存全入力/min-count/top前であり、変更要否は未承認の製品判断。空白trim、コメント先頭、他読込み失敗等は契約の根拠を調べ、根拠のないものを勝手に確定しない。

## 入力ファイル（リポジトリ相対パス）

- `_bmad-output/initiative-r-e0a2598f/initiative-r-e0a2598f.md`: title/type/parentだけでRequirementsなし。依頼原文を補助入力として採用する。チケット自体の編集はしない。
- `openspec/specs/wordfreq-cli/spec.md`: 全文を読取。本文UTF-8/exit1、引数exit2、Unicode抽出/casefold、同数初出順、入力境界、標準ライブラリ、HTML、min-countと既定互換が現契約。
- `wordfreq/__main__.py:13-38`: argparseでtop/min-count/format。引数検査後に本文取得、InputErrorをexit1へ変換。Counter全体からtotalを計算後にmin-count/top。除外指定なし。
- `wordfreq/sources.py:13-22`: UTF-8取得、OSError/UnicodeDecodeErrorをcause保持のInputErrorへ変換。設定行の規則とCLI終了コードは持たない。
- `wordfreq/tokenizer.py:6-18`: Unicode `\w+`、token.casefold()。`lower()`への置換は現契約違反。
- `wordfreq/aggregator.py`: Counterと安定な回数降順ソート。入力Counterの挿入順が同数初出順、ソートは非破壊。
- `wordfreq/formatters.py`: text/json/htmlの純粋整形。HTMLには呼出し側がbasename/totalを渡す。全件除外でも既存空状態・escape・静的CSSを守る。
- `wordfreq/__init__.py`: パッケージの副作用抑制は既存CLI回帰で確認する対象。
- `README.md:5-41`: 既存使い方、casefold、min-count/top、HTML元総数、本文exit1と引数exit2、純粋部品契約。除外FILEの使い方はまだない。
- `pyproject.toml`: runtime dependencies=[]、開発pytest。新規依存・CI変更を要しない。

## 現存する試験の読取り

- `tests/test_cli.py`: 実subprocess、JSON/HTML解析、同数初出順、Unicode、本文異常系、usage異常系、help/READMEのmin-count例、min-countとtop、空結果、既定出力バイト原本、非破壊の共通経路を読む。
- `tests/test_tokenizer.py`: Straße/STRASSE、句読点、数字/underscore、日本語、差替えtokenizerのcasefold。
- `tests/test_aggregator.py`: イテレータ集計、非破壊ソート、同数初出順、空/大きい整数。
- `tests/test_sources.py` と `tests/test_sources_boundary.py`: UTF-8、cause付き読込みエラー、解析のI/O非依存、取得境界越しの試験。
- `tests/test_formatters.py`: text/jsonの形式、純粋HTML、escape、空状態、静的CSS。ブラウザ確認と自動試験を同一視しない。
- `tests/` のその他のHTML/min-count検証器試験とfixtureは一覧を確認。今回の機能は未実装なので、それらを新機能の合格証拠とはしない。

## 契約で確定できるものとできないもの

確定できるのは本文抽出/casefold、既存同数順/形式/未指定互換、本文用のエラー、CLIと取得/集計/整形の境界。FILE不存在exit2は依頼者が明示した除外入力固有の上書き。空行と生の行頭#の無視も明示要求。

既存本文のsplit/tokenizeは設定行のtrim・字下げコメント・インラインコメント・複数語・BOMの規約ではない。既存UTF-8採用は除外FILEの文字コードを推測する材料だが承認ではない。InputErrorをそのまま本文用exceptへ渡すと除外FILE不存在までexit1になるため不適合。HTMLtotalを除外Counterで再計算すると未承認の意味変更になり得る。これらを共通未決一覧へ送った。

## スコープと手順上の制約

headless:true / intent:create、Brief template=brief、PRD template=prdを明示指定。PRDはBriefのdocumentパスを入力とし、architectureはPRDを入力とする。公式merge・memlog・check_ids・lint_spineを使う。公式スクリプトの更新/install、Kanban、git commit/push、実装変更は禁止。GSDの判定は今回の担当範囲にないので行わない。

利用可能なツールにsubagent起動機能はないため、スキルのfallbackに従ってレビューをレンズごと逐次実行して原本を分離保存する。同一モデルの逐次レビューであり、独立プロセス/独立品質担当による承認とは呼ばない。
