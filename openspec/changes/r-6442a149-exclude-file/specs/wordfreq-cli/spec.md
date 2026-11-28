# Spec Delta

## ADDED Requirements

### Requirement: 除外単語ファイルの指定（EX-1）
システムは（SHALL）任意の `--exclude FILE` を受け取り、1行1語で指定された語の全出現を集計対象から外す。除外はmin-countとtopの適用前に全形式へ共通に反映し、残存語の回数・相対初出順・既存の順位規則を変えない。同一有効除外語の重複で結果を変えない。複数指定は最後のFILEのみ使い、前のFILEを読まない。

#### Scenario: 指定語の全出現を除く
- **WHEN** 本文 `Zoo apple APPLE zoo banana` と、除外行 `apple` を指定してtext・json・htmlで実行する
- **THEN** zoo 2、banana 1の順だけが結果に現れ、appleは現れない

#### Scenario: 集計対象の除外はtopより前
- **WHEN** 本文 `Zoo apple APPLE zoo banana`、除外行 `zoo`、`--top 1` を各形式で指定する
- **THEN** apple 2が表示され、先にtopで選んだzooの削除による空結果にはならない

#### Scenario: 同数順序と重複
- **WHEN** 本文 `beta apple alpha`、除外行 `apple`・`APPLE`・`aPpLe` を各形式で指定する
- **THEN** beta 1、alpha 1の初出順で結果が得られ、除外行 `apple` のみの場合と語・回数・順位・総数が一致する

#### Scenario: 該当語がない一覧
- **WHEN** 本文に存在しない有効語だけの除外一覧を指定する
- **THEN** 未指定時と各形式の語・回数・順位・総数・終了状態が一致する

#### Scenario: 最後のFILEだけ採用する
- **WHEN** 読める本文に `--exclude missing --exclude valid` を指定し、validだけが読める（逆順と、最後が空FILEの場合も確認する）
- **THEN** 前者はmissingを読まずvalidだけ適用し成功する。逆順は最後のmissingでexit2。最後が空FILEなら前の除外一覧は適用しない

### Requirement: 空行とコメント行（EX-2）
システムは（SHALL）UTF-8の除外FILEの先頭BOMを除去し、行前後の空白を除いた後、空行と先頭文字が `#` の行を読み飛ばす。LF・CRLF・最終改行なしを受け付ける。それ以外は行全体を一語とし、語分割・記号除去・行内コメント解釈をしない。

#### Scenario: 空行とコメントは語にならない
- **WHEN** 本文 `apple marker banana` と、空行・`#marker`・`apple` の各行を持つ除外FILEを指定する
- **THEN** marker 1、banana 1が残る。読込処理の直接試験でも空行とコメント行が有効除外項目にならないことを確認する

#### Scenario: 有効項目がない
- **WHEN** 空FILE、または空行と先頭 `#` のコメントだけのFILEを指定する
- **THEN** 各形式の集計結果は未指定時から変わらない

#### Scenario: 前後空白と改行とBOM
- **WHEN** 本文 `apple marker banana` に、先頭BOM・空白のみの行・`  #marker  `・`  APPLE  ` を持つ除外FILEをLF・CRLF・最終改行なしで指定する
- **THEN** marker 1、banana 1のみが残る。直接読込試験でも空白行とコメントが有効項目に入らず、APPLEの前後空白と先頭BOMが比較を妨げない

#### Scenario: 行全体をそのまま比較する
- **WHEN** 本文 `foo bar foo_bar 123 foo-bar apple note` に除外行 `foo bar`・`foo_bar`・`123`・`foo-bar`・`apple#note` を指定する
- **THEN** foo_barと123だけが除外され、foo 2、bar 2、apple 1、note 1が残る。foo barやfoo-barを分割せず、途中#以降もコメントとして切り捨てない

### Requirement: 大文字小文字を区別しない除外比較（EX-3）
システムは（SHALL）有効除外行を既存集計と同じcasefoldで比較する。既存本文の単語抽出・casefoldは維持し、単純lowerへ変更しない。

#### Scenario: 混在表記の同一視
- **WHEN** 本文 `Apple APPLE apple banana` と除外行 `aPpLe` を指定する
- **THEN** banana 1だけが集計に残り、appleの全表記が集計から外れる

#### Scenario: Unicode casefoldで一致する
- **WHEN** 本文 `STRASSE Straße banana` に除外行 `Straße` を指定し、除外行をSTRASSEにした場合も確認する
- **THEN** どちらもbanana 1だけが残り、strasseの全出現が除外される

### Requirement: 除外ファイル読込失敗の通知と優先順位（EX-4）
システムは（SHALL）既存引数検証→除外FILE→本文の順に処理する。除外FILEの不存在・権限不足・ディレクトリ指定・文字コード不正等の読込失敗は、対象と原因が分かる文をstderrへ出しexit2、stdoutは空とする。文言完全一致は要求しない。両ファイル失敗でも除外側を優先し、除外成功後の本文失敗は既存exit1を維持する。

#### Scenario: 除外FILEが存在しない
- **WHEN** 読める本文と不存在の除外パスを `--exclude FILE` で指定する
- **THEN** 終了コードは2で、対象パスと不存在が原因と分かる文をstderrへ出しstdoutは空

#### Scenario: 不存在以外の除外読込失敗
- **WHEN** 権限不足・ディレクトリ指定・不正UTF-8の除外FILEをそれぞれ読める本文と各形式で指定する
- **THEN** 各失敗がexit2、対象と原因を示すstderr、stdout空となり、集計結果を出さない

#### Scenario: 複合失敗の順序
- **WHEN** 不正な既存引数と読めない除外FILE・本文を併用する、両ファイルだけが読めない、または除外FILEだけ正常に読める場合を実行する
- **THEN** 順に既存引数エラー（ファイルを読まない）、除外FILEのexit2（本文を読まない）、既存本文エラーexit1となり、いずれもstdoutに結果を出さない

### Requirement: 全語除外の空結果（EX-6）
システムは（SHALL）全語が除外された場合、各出力形式の既存空結果で正常終了exit0とし、除外専用メッセージを追加しない。

#### Scenario: 全語除外の各形式
- **WHEN** 本文 `Apple apple` に除外行appleを指定しtext・json・htmlで実行する
- **THEN** textは空、jsonは `[]` と末尾改行、htmlは既存空表・既存空結果案内と総数0を示し、全形式でexit0となる

### Requirement: 除外指定の説明・試験・未指定互換（EX-5）
システムは（MUST）`--help` とREADMEの使い方に除外FILEの構文・行規則・casefold比較・読込失敗時exit2・最後のFILEのみ採用・空結果を説明し、対応試験を追加する。既存試験を通し、未指定時の本文読込、抽出・正規化、text/json/html、min-count/top、順位とエラー契約を維持する。追加依存・権限変更・外部送信を必要としない。

#### Scenario: 案内を読む
- **WHEN** `python -m wordfreq --help` とREADMEの使い方を確認する
- **THEN** `--exclude FILE` の使用方法と一覧形式・不存在時の扱いが分かり、READMEの例を再現できる

#### Scenario: 追加試験と既存回帰
- **WHEN** 除外正常系、空行、コメント、大小文字、不存在と既存全試験を実行する
- **THEN** 全試験が成功し、未指定の各形式と本文エラーexit1を含む従来動作が維持される

## MODIFIED Requirements

### Requirement: HTMLの入力情報と総出現回数（HTML-2、AC2）
システムは（SHALL）表より上に実行環境のパス規則によるbasenameのみと、除外指定時は指定語を集計対象から外した後、min-countとtopを適用する前の総出現回数を表示する。除外未指定時は従来どおり入力全体の総出現回数とする。総数は種類数や表示行の和ではない。ディレクトリをtitleや属性を含むHTMLのどこにも埋め込まない。topの既定10・正の整数のみという現行契約を維持し、min-countを満たす種類数がtop以下ならその全種類、topを超えるならその上位top種類を表示する。

#### Scenario: topを変えても総数は一定
- **WHEN** `zoo apple zoo banana apple cherry`を含む下位ディレクトリのファイルをtop1・2・10でhtml出力する
- **THEN** min-count既定1でbasenameのみと総数6が表より前にあり、行はそれぞれzoo 2のみ、zoo 2とapple 2、zoo 2とapple 2とbanana 1とcherry 1の4行となる

#### Scenario: 異なる頻度の入力とtop
- **WHEN** `beta beta beta alpha gamma alpha delta`をtop2でhtml出力する
- **THEN** 総数は7、行はbeta 3とalpha 2であり、表示回数の和5を総数としない

#### Scenario: top既定と不正値
- **WHEN** html形式でmin-countを満たす11種類以上の語を含むファイルにtopを省略する、またはtopに0・負数・非整数を指定する
- **THEN** 省略時は10行、残った種類数より大きい正整数なら残った全種類。不正値ではexit2でstderrにエラーを出し結果HTMLは出さない

#### Scenario: 閾値とtopの両方で表示を絞る
- **WHEN** `beta beta beta alpha gamma alpha delta`を`--min-count 2 --top 1 --format html`で実行し、さらにmin-countを4に変える
- **THEN** 前者はbeta 3の1行と総数7、後者はデータ0行と総数7を示す。表示順位は残った行に1から付け、元集計を総数に用いる

#### Scenario: 除外後の総数を保って表示を絞る
- **WHEN** 本文 `Zoo apple APPLE zoo banana`、除外行 `apple` を指定し、htmlで `--min-count 2 --top 1` を実行する
- **THEN** 表示行はzoo 2だけで総数は3となり、除外前総数5や表示回数の和2を総数にしない
