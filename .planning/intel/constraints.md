# Constraints (intel)

正本5分類中のSPEC 2件から8制約を抽出。型はapi-contract 8件。今回集合内の参照循環なし。既存locked総数との衝突は保留のまま原意を保持し、宛先へ適用しない。

DATA_ab212ded_START

## EX-1：任意除外と最後のFILE
- source: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:5-26
- type: api-contract
- content: --exclude FILEは1行1語の全出現をmin-count/top前に全形式共通で除く。残存回数・相対初出順・順位規則を維持し、重複は無影響。複数指定は最後のFILEだけ読み、前のFILEは読まない。Zoo apple APPLE zoo bananaからappleを除くとzoo2、banana1。zoo除外/top1はapple2。beta apple alphaからapple除外はbeta1、alpha1の順。該当語なしは未指定と一致する。

## EX-2・EX-3：行全体とcasefold
- source: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:28-56
- type: api-contract
- content: UTF-8先頭BOMを除き、各行strip後、空行と先頭#行を無視する。LF/CRLF/最終改行なしに対応。他は全体一語で、語分割・記号除去・行内コメントを行わない。foo bar/foo-bar/apple#noteを個別語に分けず、foo_bar/123は一致語を除外できる。既存本文抽出とcasefoldを維持し、有効行もcasefoldする。lowerへ変更しない。STRASSE Straße bananaをStraßeまたはSTRASSEで除外するとbanana1のみ。直接読込試験で無視行と有効行を確認する。

## EX-4：失敗の優先順位
- source: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:58-71
- type: api-contract
- content: 既存引数検証→採用除外FILE→本文の順。除外FILEの不存在・権限不足・ディレクトリ・不正UTF-8等は対象と原因をstderr、exit2、stdout空。文言完全一致は不要。引数不正ではファイルを読まず、除外失敗では本文を読まない。両ファイル失敗でも除外exit2優先。除外成功後の本文失敗は既存exit1。

## EX-5・EX-6・HTML-2：空結果、説明、互換と総数
- source: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:73-114
- type: api-contract
- content: 全語除外はexit0、text空、json []と末尾改行、HTML既存空表・空案内と総数0。除外専用メッセージは足さない。help/READMEに構文・行規則・casefold・読込失敗exit2・最後FILE・空結果を説明し、例を再現し追加/既存試験を通す。未指定時の本文読込・抽出・正規化・全形式・min-count/top・順位・エラーを維持し、依存/権限/外部送信を追加しない。HTMLはbasenameのみ、ディレクトリ情報をtitle/属性含む全体へ出さない。指定時総数は除外後min-count/top前の出現数合計で、種類数や表示行和ではない。未指定総数は従来どおり。Zoo apple APPLE zoo bananaからapple除外/min-count2/top1ではzoo2の1行、総数3（5や2でない）。未指定beta beta beta alpha gamma alpha deltaはmin-count4で0行でも総数7。top既定10/正整数、残存種類数以内を表示する。

## AD-1：集計前の共通除外境界
- source: _bmad-output/initiative-r-6442a149/architecture/architecture.md:29-51
- type: api-contract
- content: CLI合成境界が除外集合読取りを統括し、本文casefold済みトークンから一致語を除いて既存集計へ渡す。除外→計数→min-count→top→既存formatter。総数は除外後・選択前。formatterは除外FILEを読まず、集計/formatterから入力取得側へ依存しない。追加依存・権限変更・外部送信なし。未指定時は除外読込みを通らない。

## AD-2：未指定非干渉と残存語保存
- source: _bmad-output/initiative-r-6442a149/architecture/architecture.md:53-57
- type: api-contract
- content: 未指定では除外FILE読取・検証を起動しない。既存本文分割/casefold、回数降順・同数時正規化後初出順、min-count→top、書式とエラーを保持する。指定時も残存回数・相対初出順を変えず、重複は無影響。全語除外の既存空形式/案内と総数0、exit0を使い、専用メッセージを追加しない。

## AD-3：正規化キーと行解釈の分離
- source: _bmad-output/initiative-r-6442a149/architecture/architecture.md:59-65
- type: api-contract
- content: 除外FILEはUTF-8、先頭BOM除去、LF/CRLF/終端改行なし、strip→空無視→先頭#無視→全体一語casefold。途中#を残し分割・記号除去しない。本文既存抽出/casefoldのキーで集計前比較する。StraßeとSTRASSEを同一キーで比較し、lowerへの変更や元表記復元をしない。抽出後に失われたハイフン等を復元・補完しない。

## AD-4：最後のFILEと直列失敗
- source: _bmad-output/initiative-r-6442a149/architecture/architecture.md:67-71
- type: api-contract
- content: 複数指定の最後FILEだけ採用し前は読まない。既存引数検証（help終了含む）→除外FILE→本文。除外読込失敗は対象/原因stderr・exit2・stdout空で本文を読まず、両方失敗でも除外exit2。除外成功後の本文失敗は既存exit1。CLIが読込・終了を統括し、成功までformatter出力を開始しない。

DATA_ab212ded_END
