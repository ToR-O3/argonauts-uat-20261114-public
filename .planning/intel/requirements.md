# Requirements (intel)

MODE: merge。承認manifestのPRD分類2文書をともに全文読取りして抽出した。以下の前半6件はproposal、後半6件はBMAD PRDのFR-1–FR-6。原文の詳細度・出典を失わないよう別IDで保持する。両者の共通要求は整合し、追加の具体化は同時に満たせるため競合variantではない。既存CONTEXTとの初出順衝突はBLOCKERとして残し、destinationへの採用は行わない。

DATA_cd8c01d9_START

## REQ-html-static-output
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:6-7,13-19
- description: 既存wordfreq CLIにhtml出力を追加する。
- acceptance: --format htmlで、順位・単語・回数の3列表を持つ自己完結した静的HTMLをstdoutへ出す。
- scope: wordfreq-cli出力形式、AC1

## REQ-html-input-metadata
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:8
- description: 入力の文脈と全単語の総出現回数をHTMLに表示する。
- acceptance: 表より上にbasenameのみとtop適用前の総出現回数を表示する。
- scope: HTMLメタ情報、AC2

## REQ-first-occurrence-order
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:10,19
- description: 同数語を正規化後単語の昇順ではなく初出順にする意図した互換性変更。
- acceptance: 回数降順を維持し、同数は初出順でtext・json・htmlを一致させ、その後topで制限する。
- scope: 全出力形式の順序、AC3

## REQ-html-responsive-readable
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:9
- description: 明るいHTMLを通常幅と小画面で読めるようにする。
- acceptance: 明るい背景のみで切替なし。順位は1始まりの表示行連番。通常幅と320 CSS pxを含む幅で長い語・名前が読める。
- scope: HTML表示、AC4

## REQ-html-safety-regression
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:11,21-23
- description: HTMLの安全性と、意図した順序変更以外の既存処理を保つ。
- acceptance: エスケープ・空入力・入力とエラー処理・既存形式を回帰検証し、入力取得とトークナイザの境界および標準ライブラリのみの実行を維持する。text/jsonへHTMLメタ情報を加えない。CI追加・変更、生成日時、テーマ切替、対話操作、サーバー、入力元拡張は対象外。
- scope: HTML安全性、既存互換性、変更境界、AC5

## REQ-html-independent-evidence
- source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:11,23
- description: 品質担当の独立ブラウザ確認と証拠を要求する。
- acceptance: 品質担当が実CLIでHTMLを再生成して独立ブラウザ確認を行い、文字範囲の実測原本・画面画像・head等の追跡可能な証拠を残す。提案自体は実装やブラウザ検証の合格を宣言しない。
- scope: 検証証拠、AC6

## REQ-html-static-output-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:46-48,68-74,85-92
- description: ローカル保存して読める静的HTML出力を提供する（PRD FR-1）。
- acceptance: python -m wordfreq <file> --format htmlでstdoutに1枚の文書を出す。順位・単語・回数の見出しと表を持ち、UTF-8で日本語ファイル名を表示する。スタイルは内部に持ち、スクリプト・外部リソース・通信に依存しない。正常時exit 0、説明ログなし。保存の使用例を説明文書へ追記する。生成日時・暗色・テーマ切替・対話操作・Webサーバーは追加しない。
- scope: wordfreq-cli出力形式、AC1、利用説明

## REQ-html-input-metadata-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:39-44,50-52
- description: HTML表より前にbasenameと入力全体の総出現回数を表示する（PRD FR-2）。
- acceptance: 実行環境のパス規則のbasenameだけを表示し、ディレクトリをtitle・属性にも埋め込まない。総数はtop前の全単語の回数の総和で、種類数や表示行の和ではない。topは既定10、正整数Nで表のみ制限。空でもbasename・総数0・見出しを持ちデータ行0件。zoo apple zoo banana apple cherryはtop 1/2/10のいずれも総数6、行はzoo 2のみ／zoo 2とapple 2／4行。beta beta beta alpha gamma alpha deltaは総数7、top 2はbeta 3とalpha 2。
- scope: HTMLメタ情報、top、空入力、AC2

## REQ-first-occurrence-order-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:39-41,54-55,68-70,85-89
- description: 全形式の同数語順を初出順へ意図して変更する（PRD FR-3）。
- acceptance: 回数降順、正規化後同一語が入力トークン列に最初に現れた位置の昇順、その後topの順で処理し、後の再出現で初出位置を更新しない。text/json/htmlで語と回数が同順。Zoo apple APPLE zoo bananaはzoo 2、apple 2、banana 1でtop 1はzoo。旧語昇順の期待値・利用説明・試験を初出順へ更新し、移行フラグは追加しない。
- scope: 全出力形式の順序、互換性変更、AC3

## REQ-html-responsive-readable-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:44,57-59,82-83,94-95
- description: 通常幅と小画面で全文を読める明るい表を提供する（PRD FR-4）。
- acceptance: 明るい背景のみ、テーマ切替なし、3列表、順位は1始まりの表示行連番。同数でも同順位にしない。通常幅と少なくとも320 CSS pxで空・通常・長い連続語・長いbasenameの全内容が読める。折返しを許し、省略や切取りによる欠落を合格としない。viewport・要素・文字Rangeの矩形と行断片・切取り祖先の実測原本を保存し、横収まり、切取り祖先内の収まり、隣接内容との非重複、実画像の可読性で判定する。要素自身への厳格な縦包含を必須にせず、縦のはみ出し値を隠さず欠け・重なり・可読性で判断する。
- scope: HTML表示、幾何測定、AC4

## REQ-html-safety-regression-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:61-63,68-74,82-89
- description: データを安全に表示し、同数時語順以外の既存契約を維持する（PRD FR-5）。
- acceptance: 単語とbasenameのHTML特殊文字をエスケープし、&・<・>・二重引用符・単一引用符の表示を保持してタグ・イベント・スクリプトを生成しない。整形部品へ特殊文字の語を直接与え、実CLIは特殊文字を含む有効なbasenameで検証する。パス区切りをbasenameへ含めず認識規則を緩めない。入力取得境界・UTF-8読込み・Unicodeの単語構成文字の最大連続抽出・casefoldを維持する。引数個数/top/format不正はstderrとexit 2、読込み/デコード失敗はstderrとexit 1で結果HTMLなし。textはcount先頭のタブ区切り行、jsonはword/count配列と末尾改行、空ではtext空・json空配列と改行。HTMLメタ情報はtext/jsonへ追加しない。標準ライブラリのみ、CI追加・変更なし。入力元拡張・形態素解析・認識変更・依存追加は対象外。外部参照なしと通信試行なしを別々に確認する。
- scope: HTML安全性、入力・エラー・出力回帰、変更境界、AC5

## REQ-html-independent-evidence-prd
- source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:65-66,76-83,98-99
- description: 自動試験と品質の独立ブラウザ確認を条件別証拠へ対応付ける（PRD FR-6）。
- acceptance: FR-1–FR-5の通常・空・top既定/1/境界/種類数超過・不正値・Unicode・注入・エラー回帰を自動検査する。品質担当は対象headの実CLIから独立生成し通常幅と320 CSS pxを含む画面を確認する。head、入力原本、コマンド、exit/stdout/stderrと期待値、生成HTML、ブラウザ/viewport、文字範囲の測定原本、実画面画像、外部通信検査を保存・添付しACごとの合否と対応付ける。Builder画像や自動判定だけで代用せず未実施を合格扱いしない。幾何条件と実画像の両方を用い、外部参照・通信試行を確認し、ローカル文書読込みと外部通信を区別する。FR-1–FR-6を同じ変更で提供し、UI・安全性・証拠を後回しにしない。製品試験と独立確認の現状は未実施。
- scope: 検証証拠、独立品質確認、AC6

DATA_cd8c01d9_END
