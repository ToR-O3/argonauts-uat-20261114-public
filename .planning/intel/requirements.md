# Requirements (intel)

6件の再分類入力から新規合成。PRD分類のBriefとPRD本体をそれぞれ保持する。詳細化は同時充足可能であり競合variantではない。以下は要件であって実装・試験の成功記録ではない。

DATA_6dfce248_START

## REQ-exclude-brief-ranking
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:57,66
- description: 指定語をランキングから外す。
- acceptance: 指定語がランキングから消え、未指定語の回数と同数初出順、元入力のHTML総数が保たれる。text/json/htmlの結果語を共通に扱い、topとmin-countに除外語が表示枠を占有させない。
- scope: 除外語、全形式、HTML総数、top/min-count

## REQ-exclude-brief-lines
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:58
- description: 除外FILEの行と大小同一視を扱う。
- acceptance: 前後空白除去後の空行と `#` コメントを無視し、LF・CRLF・最終改行なしとUnicode casefold同値語を扱える。
- scope: 除外FILE、行解析、casefold

## REQ-exclude-brief-fullmatch
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:31,59
- description: trim後の残る行全体を既存 `\w+` で検証してからcasefoldする。
- acceptance: `\w+` 全体一致で数字とunderscoreを受理する。複数語・句読点・hyphen・単独結合文字・語の後の#注記・先頭BOMはファイル名と行番号を示してexit2。
- scope: 有効語、不正行診断

## REQ-exclude-brief-errors
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:43,60
- description: 除外FILEを本文より先に読み込み全行検証する。
- acceptance: 既存の引数構文・数値検査後、除外FILEの読込みと全行検証を本文より先に行う。UTF-8で読込み、不在・権限不足・ディレクトリ・不正文字コードなど全読込み失敗は理由stderr/exit2。除外失敗は本文より優先し本文未読、結果stdout空・HTML/Tracebackなし。本文側の既存exit1は維持する。
- scope: 引数→除外全行→本文、終了コード、診断

## REQ-exclude-brief-discovery-tests
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:61
- description: help/READMEと追加試験を届ける。
- acceptance: helpとREADMEで使い方を発見できる。追加試験と既存試験により未指定互換を検証する。
- scope: help、README、回帰試験

## REQ-exclude-brief-change-boundary
- source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:62,68
- description: 既存契約と変更境界を維持する。
- acceptance: 既存出力・既存エラー・依存・CIの意図しない変更がない。新依存、外部通信、CI変更、正規化変更、並び変更、自動stopword辞書、複数ファイルの新しい利用方式、永続設定、HTMLデザイン変更は含まない。
- scope: 既存互換、製品変更境界

## REQ-exclude-prd-fr1
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:66-70,133-135
- description: 任意の `--exclude FILE` を追加する。
- acceptance: 未指定時は従来の結果・終了状態を保つ。指定語の全出現だけをランキングから外し残る語の回数とHTML元総数を変えない。本文 `Zoo apple APPLE zoo banana`、除外appleならtextは `2\tzoo\n1\tbanana\n`、exit0。除外されない語だけにtop適用。値欠落は既存argparseと同じ使い方エラー。
- scope: CLI公開面、指定語除外、互換

## REQ-exclude-prd-fr2
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:72-76
- description: trim後の行を既存Unicode `\w+` 全体一致で検証する。
- acceptance: 空行と `#` 開始行を無視しLF/CRLF/最終改行なしを受理。検証後casefold。空白行、字下げ `#banana`、appleのFILEはappleだけ除外しbananaを残す。123と_word_は有効。foo bar、foo,、foo-bar、単独結合文字、foo # note、先頭BOM付き語は不正。分割・句読点除去・インラインコメント化・BOM自動除去で受理しない。本文分割は不変。
- scope: 除外FILE行形式、有効語、不正語

## REQ-exclude-prd-fr3
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:78-82
- description: 既存casefoldでUnicode同一視する。
- acceptance: lowerへ変更しない。本文 `Straße STRASSE hello` と除外STRASSEはhelloのみ。本文HELLO helloと除外Helloは全出現を外す。
- scope: 除外語照合、Unicode正規化

## REQ-exclude-prd-fr4
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:84-90
- description: 除外FILEの全読込み・全行検証を本文取得前に完了する。
- acceptance: UTF-8読込み。不在・権限不足・ディレクトリ・不正文字コード等すべての読込み失敗はFILEと理由のstderr/exit2。不正行はFILEと元行番号のstderr/exit2。全文メッセージ固定なし。stdout空、結果/HTML/Tracebackなし。既存引数構文・top/min-count数値検査→除外取得/全行検証→成功時のみ本文取得。双方不存在でも除外診断/exit2。本文不正UTF-8と除外不正行でも本文未読。空行/字下げコメント/有効語/不正行なら4行目を診断し途中の有効語が本文に一致しても本文取得0回。有効除外と本文不存在はexit1。top0またはmin-count0と除外不存在なら既存数値診断が先で両ファイル取得0回。
- scope: 入力境界、検証優先順位、終了コード

## REQ-exclude-prd-fr5
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:92-96,129-131
- description: 除外→min-count→回数降順/同数初出順→topを共通結果語へ適用する。
- acceptance: text/json/htmlの語/回数/順序一致。除外語はtop枠を消費しない。不一致語なら結果不変。本文 `Zoo apple APPLE zoo banana`、除外zoo、min-count2/top1ならapple2のみ、HTML総数5。除外と閾値で全件消えてもexit0、text空、json `[]\n`、HTML既存見出し/0データ行/元総数5。空本文は総数0。空/コメントのみFILE/不一致語では既存結果を保持。全文Counterと候補を区別し総数は除外/min-count/top前の全文Counterから取得。入力本文・除外FILEを書き換えない。
- scope: 全出力形式、元総数、選別順序

## REQ-exclude-prd-fr6
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:98-100,137-139
- description: helpとREADMEで使用法を説明する。
- acceptance: helpは目的とファイル形式を説明してexit0。READMEに実行例、UTF-8の1行1語、trim後空行/#開始行無視、LF/CRLF/最終改行なし、既存w+全体一致/不正行、casefold、読込み失敗/不正行のstderr/exit2、除外先行、HTML元総数、未指定互換を追記。README実行例は追加試験で実行する。
- scope: help、README、説明と受入の一致

## REQ-exclude-prd-fr7
- source: _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:102-117,129-143
- description: 既存版との互換、追加/既存全試験、独立品質の証拠を残す。
- acceptance: 比較元 `79d83ba14dd59d289d2ecd3e33c85e8de437972e` と変更後を同一入力/argvで実行するか比較元の固定期待値を使用し、変更後自身を根拠なく期待値にしない。同数語/Unicode/10種類超/空本文、空FILE/コメントのみ/不一致/全語除外を区別。pytestでFR-1〜6の全行規則・全不正例・全読込み失敗・優先順/本文未読・全形式・HTML元総数・top/min-count・同数順・空/全除外・既存本文エラーを検査、既存全試験維持、未指定stdoutバイト一致。品質が対象版で独立CLIと回帰確認。既存count_words/top_words/formatters公開契約を不必要に変えず、取得境界と純粋解析/集計/整形を分離、終了コードはCLI、formatterに除外I/Oなし。Unicode抽出/casefold/Counter初出順/既定値を維持。新依存/外部通信/CI変更なし、HTML静的安全性/UTF-8/basename/escape/見た目を維持。自動辞書/regex除外/外部入力元/FILE `-` stdin追加/複数FILE新仕様/永続設定/lower化/形態素解析/全面再設計なし。仮実装・期待値・READMEを承認代用にしない。新未決は推測しない。
- scope: 回帰証拠、独立確認、既存公開境界、非目標

DATA_6dfce248_END
