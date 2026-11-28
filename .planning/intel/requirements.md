# Requirements (intel)

PRD 1件からFR-1〜FR-6・RULE-1〜RULE-2を8要件として抽出する。受入条件は後続の検証対象であり実行結果ではない。背景OQ-7/8を追加条件にしない。HTML総数の変更は承認済みだが既存lockedとの衝突を保留し、宛先へ適用しない。

DATA_64a92bd7_START

## REQ-exclude-fr-1
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:58-60
- description: 任意の--exclude FILEで有効行に一致する本文語の全出現を除く。残存回数・相対初出順を保ち重複は無影響。複数指定は最後FILEだけを採用し前は読まない。
- acceptance: Zoo apple APPLE zoo bananaからappleを除き、textは2\tzoo\n1\tbanana\n、JSONはzoo2/banana1の配列と末尾改行、HTMLは同じ語/回数と順位1/2。min-count2/top1はzoo2のみでHTML総数3。zoo除外/top1はapple2。missing→valid指定は前を読まず成功、逆は最後missingでFR-4の失敗。最後が読める空FILEなら前の一覧を適用しない。
- scope: --exclude FILE、全形式、最後FILE、残存語

## REQ-exclude-fr-2
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:62-64
- description: UTF-8先頭BOM除去後、strip→空行/先頭#無視→全体一語。LF/CRLF/最終改行なし対応。分割・記号除去・行内コメントを導入しない。
- acceptance: 空白行と  #apple  は無視、  APPLE  はappleを除外。apple#noteはapple/noteを個別除外せず、foo barもfoo/barを個別除外しない。foo_bar/123は一致語を除外し、foo-barは本文のfoo/barに無影響。空/コメントのみ/該当語なしは未指定と一致。BOM・改行形式・終端改行なし・重複を組合せ、直接読込試験でも無視行と有効行を区別する。
- scope: 除外FILE読込と行解釈

## REQ-exclude-fr-3
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:66-68
- description: 本文の既存抽出/casefoldを維持し、有効除外行もcasefoldで比較。lowerへの変更や元表記復元をしない。
- acceptance: Apple APPLE apple bananaからaPpLe除外はbanana1のみ。STRASSE Straße bananaからStraßeまたはSTRASSE除外もbanana1のみ。casefold済み入力順キーを集計前比較し、非一致語を再変換して順位や表示を変えない。
- scope: Unicode比較、本文tokenizer非変更

## REQ-exclude-fr-4
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:70-72
- description: 既存引数検証→採用除外FILE→本文。除外読込失敗は対象と原因をstderrへ出しexit2、stdout空。文言完全一致は不要。除外成功後の本文失敗は既存exit1。
- acceptance: 不存在/権限不足/ディレクトリ/不正文字コードを読める本文と各形式で確認し、exit2と対象/原因のstderr、stdout空。両ファイル失敗も除外exit2。不正top/min-count/format等ではFILEを読まず既存引数エラーを優先。除外失敗では本文を読まない。除外成功後または未指定の本文失敗はexit1。途中結果なし、helpの既存終了を維持。
- scope: 読取順、診断、終了コード、全形式

## REQ-exclude-fr-5
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:74-76
- description: 実装時にhelp/READMEへ構文・行規則・casefold・読込エラー・最後FILE・空結果を説明し、FR-1〜4/FR-6/RULE-1の試験を加える。
- acceptance: 実CLI helpとREADMEに採用仕様が矛盾なく記載され、一覧例と実行例が再現できる。本合成は製品/help/README/試験を変更せず試験合格を主張しない。
- scope: help、README、追加試験

## REQ-exclude-fr-6
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:78-80
- description: 未指定の本文抽出/casefold、全形式、順位、min-count/top、既存エラーを維持し既存試験を通す。全語除外は既存空結果でexit0、専用メッセージを足さない。
- acceptance: 全語除外はtext空、JSON []と末尾改行、HTML既存空表/既存空案内/総数0でexit0。既存HTML案内を消さない。未指定回帰・空本文・Unicode・同数順・既存異常を検証。新機能/全件試験は後続、現工程では未実施。
- scope: 未指定互換、全語除外、回帰

## REQ-exclude-rule-1
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:84-86
- description: 全形式で除外→計数→min-count→top→formatter。HTML総数は除外後・min-count/top前。残存回数と相対初出順、回数降順/同数時初出順を維持する。
- acceptance: FR-1のHTML総数3はmin-count2/top1でも3。beta apple alphaからapple除外はbeta1/alpha1の順。apple/APPLE/aPpLe重複は単独と同じ。本文にない一覧は語/回数/順位/総数/終了状態を変えない。
- scope: 共通集計境界、HTML総数、順位

## REQ-exclude-rule-2
- source: _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:88,104-106
- description: 追加依存・権限変更・外部送信を必要としない。
- acceptance: 後続実装で依存宣言・変更範囲・通信不要のローカル処理を確認する。性能/可用性の数値目標は追加しない。
- scope: 運用制約、ローカルCLI

DATA_64a92bd7_END
