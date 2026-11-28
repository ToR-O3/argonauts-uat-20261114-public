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
システムは（SHALL）空行と生の行頭が `#` の行を無視し、通常の1行1語を既存本文と同じcasefoldで照合する。本文のUnicode抽出や正規化をlowerへ置き換えてはならない（MUST）。前後空白、字下げコメント、不正行、文字コード等の未決は共通一覧の回答まで固定しない。

#### Scenario: 空行とコメント行
- **GIVEN** 本文が `apple banana`、除外FILEが `\n#banana\napple\n` である
- **WHEN** 除外FILEを指定する
- **THEN** appleだけを除外しbananaは残り、exit0となる

#### Scenario: ASCIIの大小同一視
- **GIVEN** 本文が `HELLO hello world`、除外行が `Hello` である
- **WHEN** 除外FILEを指定する
- **THEN** helloの全出現を除外しworldだけを残す

#### Scenario: 既存Unicode正規化の維持
- **GIVEN** 本文が `Straße STRASSE hello`、除外行が `STRASSE` である
- **WHEN** 除外FILEを指定する
- **THEN** casefold同値のstrasseを全て除外しhelloだけを残す

### Requirement: 除外FILE不存在の診断（EX-3）
システムは（SHALL）本文が有効で指定除外FILEが存在しない場合、FILEと原因を認識できる説明をstderrへ出しexit2で終了する。結果stdoutは空でTracebackやエラーHTMLを出してはならない（MUST）。値欠落は既存引数エラーと同じexit2とする。本文の既存失敗はexit1を維持し、他の除外読込み失敗と同時失敗の優先は未決として扱う。

#### Scenario: 除外FILEが存在しない
- **WHEN** 有効な本文と不存在の除外FILEを各出力形式で指定する
- **THEN** stderrに除外FILEの診断を出しexit2となり、stdoutは空である

#### Scenario: 値欠落
- **WHEN** `--exclude` の値を欠落させる
- **THEN** 入力取得より先に使い方エラーexit2とstderr診断になりstdoutは空である

### Requirement: 既存表示選択との併用（EX-4）
システムは（SHALL）除外語がtop枠を占有しないよう、残った語へ既存min-count、回数降順・同数初出順、top制限を適用し、全形式へ同じ結果語と回数を出す。全語が除外された場合は正常な空結果とする。HTMLの静的構造と見た目を維持する。除外指定時のHTML総数は未決であり、この要求はその値を決定しない。

#### Scenario: topとmin-countの併用
- **GIVEN** 本文が `Zoo apple APPLE zoo banana`、除外行が `zoo` である
- **WHEN** 各形式で `--exclude excluded.txt --min-count 2 --top 1` を指定する
- **THEN** 結果語はapple2のみであり、除外語がtop枠を消費しない

#### Scenario: 全件除外
- **GIVEN** 本文の全語を除外FILEに1行1語で指定する
- **WHEN** 各形式で実行する
- **THEN** exit0でtextは空、jsonは `[]` と末尾改行、htmlは既存見出しと0データ行の空状態を保つ。総数の期待値はOQ-1の回答後に追加する

### Requirement: 除外指定の説明と試験（EX-5）
システムは（SHALL）helpとREADMEの使い方に指定方法、1行1語、空行/#開始行の無視、大小同一視、不存在exit2を説明する。追加試験と既存全試験で除外動作と未指定互換を検証しなければならない（MUST）。依存・外部通信・CIを追加変更しない。

#### Scenario: 利用方法を発見できる
- **WHEN** `--help` とREADMEの使い方を読む
- **THEN** `--exclude FILE` の説明とREADME実行例があり、未決の構文を利用可能と記載しない。helpはexit0である

#### Scenario: 回帰を含む検証
- **WHEN** 追加試験と既存全試験を実行する
- **THEN** ASCII/Unicode照合、空行/コメント、全形式、top/min-count併用、未指定互換、不存在と値欠落を確認できる。空本文、空/コメントのみ除外FILE、不一致語、全語除外を区別し、未決由来の期待値は承認後に確定する
