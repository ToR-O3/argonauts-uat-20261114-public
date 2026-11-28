# Spec Delta

## ADDED Requirements

### Requirement: 除外単語ファイル指定（EX-1）
システムは（SHALL）任意の `--exclude FILE` で1行1語の除外語一覧を受け付け、指定語の全出現を結果語から外す。残った語の回数と初出順は保持する。未指定時は既存の出力・終了状態を維持しなければならない（MUST）。

#### Scenario: 指定語の全出現を外す
- **GIVEN** 本文が `Zoo apple APPLE zoo banana`、除外FILEの内容が `apple` と改行である
- **WHEN** `python -m wordfreq input.txt --exclude excluded.txt` を実行する
- **THEN** text出力は `2\tzoo\n1\tbanana\n`、exit0でありappleは出ない

#### Scenario: 未指定の互換
- **WHEN** 除外指定なしで同じ本文と既存引数を変更前後のCLIへ渡す
- **THEN** text/json/htmlのstdoutと既存終了コードは一致し、抽出・正規化・並び・既存エラーの契約は変わらない

### Requirement: 除外行と大小同一視（EX-2）
システムは（SHALL）UTF-8の各行の前後空白を除去してから、空行と `#` 開始行を無視する。LF・CRLF・最終改行なしを受け付ける。残る行は既存抽出規則 `\w+` に行全体が一致する場合だけ受け付け、既存本文と同じcasefoldで照合する。数字とunderscoreは有効である。複数語・句読点・hyphen・単独の結合文字・語の後の#注記・先頭BOMは不正行とする。本文のUnicode抽出や正規化を変更してはならない（MUST）。

#### Scenario: 空行とコメント行
- **GIVEN** 本文が `apple banana`、除外FILEが `\n#banana\napple\n` である
- **WHEN** 除外FILEを指定する
- **THEN** appleだけを除外しbananaは残り、exit0となる

#### Scenario: ASCIIの大小同一視
- **GIVEN** 本文が `HELLO hello world`、除外行が `Hello` である
- **WHEN** 除外FILEを指定する
- **THEN** helloの全出現を除外しworldだけを残す

#### Scenario: 前後空白と改行形式
- **GIVEN** 除外FILEに空白だけの行、`  # comment  `、` apple `が含まれる
- **WHEN** LF、CRLF、最終改行なしの各形式で本文 `apple banana` を処理する
- **THEN** 空白行とコメントを無視しappleだけを除外してexit0となる

#### Scenario: 数字とunderscoreは有効
- **GIVEN** 除外FILEが `123\na_b\n`、本文が `123 a_b apple` である
- **WHEN** 除外FILEを指定する
- **THEN** appleだけが残りexit0となる


#### Scenario: 既存Unicode正規化の維持
- **GIVEN** 本文が `Straße STRASSE hello`、除外行が `STRASSE` である
- **WHEN** 除外FILEを指定する
- **THEN** casefold同値のstrasseを全て除外しhelloだけを残す

### Requirement: 除外FILE不存在の診断（EX-3）
システムは（SHALL）指定除外FILEの不存在・権限不足・ディレクトリ指定・不正文字コードなどすべての読込み失敗について、FILEと理由の分かるstderrを出してexit2で終了する。不正行はFILEと行番号の分かるstderrとexit2にする。結果stdoutは空で集計結果・HTML・Tracebackを出してはならない（MUST）。値欠落は既存引数エラーと同じexit2とする。既存の引数構文・数値検査を先に行い、除外FILE全体の確認を本文取得より先に完了する。除外側で失敗したら本文を読まず、その説明とexit2を優先する。除外側が正常な場合の本文の既存失敗はexit1を維持する。

#### Scenario: 除外FILEが存在しない
- **WHEN** 有効な本文と不存在の除外FILEを各出力形式で指定する
- **THEN** stderrに除外FILEの診断を出しexit2となり、stdoutは空である

#### Scenario: 値欠落
- **WHEN** `--exclude` の値を欠落させる
- **THEN** 入力取得より先に使い方エラーexit2とstderr診断になりstdoutは空である

#### Scenario: 除外FILEの各読込み失敗
- **WHEN** text/json/htmlの各形式で、権限不足、ディレクトリ、不正UTF-8の除外FILEをそれぞれ指定する
- **THEN** FILEと失敗理由のstderr、exit2、空stdoutとなり、本文を読まずHTMLとTracebackも出さない

#### Scenario: 不正行を拒否する
- **GIVEN** 除外FILEの2行目が複数語、句読点付き語、hyphen付き語、単独の結合文字、語の後の#注記のいずれか、または1行目に先頭BOMがある
- **WHEN** 各出力形式で実行する
- **THEN** FILEと該当行番号のstderr、exit2、空stdoutとなり、本文を読まずHTMLとTracebackも出さない

#### Scenario: 除外側を本文より先に検証する
- **GIVEN** 本文も取得できず、除外FILEが不存在または不正行を含む
- **WHEN** 引数構文・数値検査に通るargvで実行する
- **THEN** 本文取得を一度も呼ばず、除外FILEの診断とexit2だけを返す

#### Scenario: 元の行番号と後方の不正行
- **GIVEN** 除外FILEが空行、字下げコメント、有効語、不正行の順に4行あり、有効語は本文にも存在する
- **WHEN** 各出力形式で実行する
- **THEN** 元ファイルの4行目とFILE名をstderrに示してexit2となり、本文取得を一度も呼ばずstdoutは空でHTMLとTracebackも出さない

#### Scenario: 引数検査が最優先
- **GIVEN** 除外FILEが読めず本文も読めない
- **WHEN** 不正な数値引数を指定する
- **THEN** ファイル取得を呼ばず既存の引数診断とexit2を返す

#### Scenario: 本文の既存失敗を維持
- **GIVEN** 除外FILEは正常で本文が読めない
- **WHEN** 実行する
- **THEN** 本文の既存診断とexit1を維持する

### Requirement: 既存表示選択との併用（EX-4）
システムは（SHALL）除外語がtop枠を占有しないよう、残った語へ既存min-count、回数降順・同数初出順、top制限を適用し、全形式へ同じ結果語と回数を出す。全語が除外された場合は正常な空結果とする。HTMLの静的構造と見た目を維持し、総単語数は除外前の入力全体の総数を維持する。除外語の回数を総数から引いてはならない（MUST）。

#### Scenario: topとmin-countの併用
- **GIVEN** 本文が `Zoo apple APPLE zoo banana`、除外行が `zoo` である
- **WHEN** 各形式で `--exclude excluded.txt --min-count 2 --top 1` を指定する
- **THEN** 結果語はapple2のみであり、除外語がtop枠を消費しない。HTML総数は元入力の5を維持する

#### Scenario: 全件除外
- **GIVEN** 本文の全語を除外FILEに1行1語で指定する
- **WHEN** 各形式で実行する
- **THEN** exit0でtextは空、jsonは `[]` と末尾改行、htmlは既存見出しと0データ行の空状態を保つ。総数は元の入力全体の単語数を維持する

#### Scenario: HTML総単語数は除外前
- **GIVEN** 本文が `Zoo apple APPLE zoo banana`、除外行が `apple` である
- **WHEN** html形式で実行する
- **THEN** ランキングにappleはなく、総単語数は元の5のままである

### Requirement: 除外指定の説明と試験（EX-5）
システムは（SHALL）helpとREADMEの使い方に指定方法、1行1語、前後空白除去後の空行/#開始行の無視、大小同一視、除外FILE失敗exit2を説明する。READMEにはUTF-8、改行形式、単語の有効条件と不正例、HTML総数の維持、除外FILE優先の検証順を記載する。追加試験と既存全試験で除外動作と未指定互換を検証しなければならない（MUST）。依存・外部通信・CIを追加変更しない。

#### Scenario: 利用方法を発見できる
- **WHEN** `--help` とREADMEの使い方を読む
- **THEN** `--exclude FILE` の説明とREADME実行例があり、上記の採用済み契約を説明する。helpはexit0である

#### Scenario: 回帰を含む検証
- **WHEN** 追加試験と既存全試験を実行する
- **THEN** ASCII/Unicode照合、空白除去/コメント/改行、有効語と不正行、全読込み失敗、検証順序と本文未読、全形式、top/min-count併用、HTML総数、未指定互換、不存在と値欠落を確認できる。空本文、空/コメントのみ除外FILE、不一致語、全語除外を区別する
