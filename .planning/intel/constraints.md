# Constraints (intel)

再分類6件中のSPEC 1件からEX-1〜5を抽出。architectureは対象外であり合成しない。以下は契約であって検証実績ではない。

DATA_631d9043_START

## EX-1: 除外単語ファイル指定
- source: openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:5-15
- type: api-contract
- content: 任意の `--exclude FILE` で1行1語の除外語一覧を受け付け、指定語の全出現を結果語から外す。残った語の回数と初出順を保持する。未指定時は既存出力・終了状態・抽出・正規化・並び・既存エラーを維持しtext/json/htmlのstdoutと終了コードは変更前後一致。本文 `Zoo apple APPLE zoo banana`、除外appleではtext `2\tzoo\n1\tbanana\n`、exit0。

## EX-2: 除外行と大小同一視
- source: openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:17-44
- type: api-contract
- content: UTF-8各行の前後空白除去後、空行と#開始行を無視。LF/CRLF/最終改行なし受理。残る行は既存Unicode `\w+` 全体一致の場合のみ受理し既存casefoldで照合。数字/underscoreは有効。複数語/句読点/hyphen/単独結合文字/語の後の#注記/先頭BOMは不正。本文Unicode抽出/正規化を変更しない。本文apple bananaと `\n#banana\napple\n` ならappleだけ除外。HELLO hello worldとHelloならworldのみ。空白行/字下げコメント/前後空白appleは各改行形式でappleだけ除外、exit0。123/a_bは有効、本文123 a_b appleからappleのみ残す。本文Straße STRASSE helloとSTRASSEならhelloのみ。

## EX-3: 除外FILE不存在の診断
- source: openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:46-84
- type: api-contract
- content: 不存在/権限不足/ディレクトリ/不正文字コード等すべての読込み失敗はFILEと理由のstderr/exit2。不正行はFILEと元行番号のstderr/exit2。stdout空、結果/HTML/Tracebackなし。値欠落も入力取得前exit2。既存引数構文・数値検査→除外FILE全体取得/全行検証→成功時のみ本文取得。各text/json/htmlで同じ契約。2行目の複数語/句読点/hyphen/単独結合文字/#注記または1行目BOMを拒否。本文も取得不可かつ除外不存在/不正行なら本文取得0回で除外診断だけ。空行/字下げコメント/有効語/不正行の4行は4行目を診断、途中の語が本文にあっても本文取得0回。不正数値なら両ファイル取得0回で既存引数診断。除外正常時の本文読込み失敗は既存exit1を維持。

## EX-4: 既存表示選択との併用
- source: openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:86-102
- type: api-contract
- content: 除外後の語に既存min-count→回数降順/同数初出順→topを適用、除外語はtop枠を消費せず全形式の結果語/回数は同じ。全語除外は正常空結果。HTML静的構造/見た目を維持し総数は除外前元入力全体、除外語の回数を引かない。本文Zoo apple APPLE zoo banana、除外zoo、min-count2/top1ならapple2のみ/HTML総数5。全語除外はexit0/text空/json[]+末尾改行/HTML既存見出しと0データ行/元総数。apple除外でもHTML総数5。

## EX-5: 除外指定の説明と試験
- source: openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:104-113
- type: nfr
- content: help/READMEに指定法、1行1語、trim後空行/#開始行無視、大小同一視、除外FILE失敗exit2を説明。READMEには実行例、UTF-8、改行形式、有効条件/不正例、HTML元総数維持、除外FILE優先の検証順を記載。helpはexit0。追加と既存全試験でASCII/Unicode、trim/コメント/改行、有効語/不正行、全読込み失敗、検証順/本文未読、全形式、top/min-count、HTML総数、未指定互換、不存在/値欠落を検査。空本文、空/コメントのみFILE、不一致語、全語除外を区別。依存/外部通信/CI追加変更なし。

DATA_631d9043_END
