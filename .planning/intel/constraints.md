# Constraints (intel)

承認manifestのSPEC分類2文書（spec.md / tasks.md）から抽出。取込み対象4文書の参照グラフに循環はない。全件staging。初出順は承認済み入力の要求として保持するが、既存CONTEXT D-10との矛盾を自動解決しない。詳細なWHEN/THEN・チェック項目は各sourceの該当節を参照。

DATA_5df1e033_START

## 実行方法とファイル読み込み（FR-1）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:5-30
- type: api-contract
- content: ファイル引数はちょうど1個、UTF-8入力。正常・空入力はexit 0。不在・開けない・デコード不能はstderrとexit 1、個数不正はstderrとexit 2。HTMLを含む全形式で維持し、エラー時に結果HTMLをstdoutへ出さない。空ではtextは空、jsonは空配列と改行、htmlはbasename・総数0・3列見出しを持ちデータ行0件。

## 出力形式オプション（FR-3）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:32-45
- type: api-contract
- content: --formatはtext/json/html、既定text。textはcount先頭のタブ区切りと末尾改行、jsonはword文字列/count整数オブジェクトの配列と末尾改行、htmlは静的1文書。不正形式はexit 2とstderr、結果なし。全形式で語と回数の順序が一致する。順位・ファイル名・総数はhtmlのみに追加する。

## 出力の順序決定論性（FR-4・D-2）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:47-56
- type: nfr
- content: 回数降順、同数は正規化後の同一語が入力トークン列に初めて現れた順、その後top適用。抽出とcasefoldは変えず、後の再出現で初出位置を更新しない。text/json/htmlで同じ順序。同じ入力とオプションで決定論的。旧語昇順を意図して置き換える。旧シナリオ名は識別子として残るが期待値は初出順へ変更済み。これは既存CONTEXT D-10とのBLOCKERであり自動採用しない。

## 自己完結したHTML表（HTML-1、AC1）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:60-65
- type: schema
- content: 順位・単語・回数の3列表を持つHTML1文書をstdoutへ出す。UTF-8宣言と内部CSSを持つ。スクリプト、外部スタイル・画像・フォント、外部通信を生む要素を含めない。正常時exit 0、stdoutに説明ログなし。保存HTMLをオフラインで読み、日本語basenameが文字化けせず、外部参照・通信試行がなくJavaScript不要であることを確認する。

## HTMLの入力情報と総出現回数（HTML-2、AC2）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:67-80
- type: api-contract
- content: 実行環境のパス規則に基づくbasenameのみと、top適用前の全単語の総出現回数を表より上に出す。種類数や表示行の回数の和で代替しない。ディレクトリはtitleや属性を含めHTMLのどこにも埋め込まない。top既定10、正整数のみ、種類数超過なら全種類。不正topはexit 2とstderr、HTMLなし。sourceのtop 1/2/10・異なる頻度のシナリオで総数不変を検証する。

## 明るい背景と表示行順位（HTML-3、AC4）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:82-87
- type: schema
- content: 明るい背景のみ、切替なし。top後の表示行へ1始まりの連番を付け、同数でも同順位や欠番にしない。

## 小画面での全文可読性（HTML-4、AC4）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:89-98
- type: nfr
- content: 通常幅と320 CSS pxを含む幅で長い連続語・長いbasenameの全文を読めること。折返しを許し、省略・切取りによる情報欠落を認めない。viewport・要素・文字Range行断片・切取り祖先の矩形を原本保存する。横収まり、切取り祖先内収まり、隣接内容との非重複、実画像での可読性で判定する。要素自身への厳格な縦包含だけを必須にせず、縦にはみ出す場合も実測値を保存し、欠け・重なり・可読性で判断する。

## HTMLデータの安全な表示（HTML-5、AC5）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:100-105
- type: nfr
- content: 単語とbasenameを表示テキストとして安全にHTMLエスケープし、データからタグ・イベント・スクリプト・外部通信を生まない。CLIでは特殊文字やタグに似た文字列を持つ有効なbasenameを検査し、整形部品単体では特殊文字の単語を検査する。検査のためにUnicode抽出・casefold・入力仕様を変更しない。

## HTML検証の独立した証拠（HTML-6、AC6）
- source: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:107-116
- type: protocol
- content: 自動試験と品質担当による対象headの実CLI再生成・独立ブラウザ確認を行う。head、入力原本、コマンド、exit/stdout/stderrと期待値、生成HTML、ブラウザ/viewport、文字範囲実測原本、画面画像、外部通信検査をAC1–AC6に対応付け保存・添付する。空・通常・top・長文・安全性・通常幅と320 CSS pxを含める。Builder画像だけで代用せず、未実施を合格にしない。入力境界・抽出・casefold・既存エラー・text/json構造を意図した順序以外は維持する。CI追加・変更、生成日時、テーマ切替、対話操作、サーバーは追加しない。

## 初出順実装タスク（1.1）
- source: openspec/changes/r-50053edc-wordfreq-html/tasks.md:3-4
- type: protocol
- content: 正規化後初出順を集計で保持し、回数降順の安定ソート後にtop適用。集計単体とtext/json実CLIで大文字小文字、top 1/2、後の再出現、異なる回数を検証し、旧語昇順なら失敗する試験を残す。部品順序契約と互換性変更を文書化する。

## 安全なHTMLと接続のタスク（2.1–2.3）
- source: openspec/changes/r-50053edc-wordfreq-html/tasks.md:6-9
- type: protocol
- content: 安全な単語・basename、UTF-8宣言、内部CSS、空pairs・特殊文字・注入候補の整形単体試験を用意する。CLIはtop前countsから総数を計算しbasenameと渡す。HTML全体に入力ディレクトリを出さない。総数不変・異なる頻度・表示位置・top既定/超過/空を実CLIで検証し保存例を説明文書へ追記する。全形式の語・回数・順序、入力境界・Unicode/casefold、不正top/format/個数/読込み/デコードのexit・stderr・空stdoutを回帰検証し、text/json構造を順序以外は変えない。

## レスポンシブ表示と測定タスク（3.1–3.2）
- source: openspec/changes/r-50053edc-wordfreq-html/tasks.md:11-14
- type: protocol
- content: UI設計・PLANで通常幅、対象ブラウザ、320 CSS pxで実際に折返す長い語と有効なbasenameの固定入力を確定する。名前の連続空白・改行・タブ、保存実体と宣言のUTF-8一致、複数桁数値も検証する。明るい背景・切替なし・連番順位と空/通常/長文/同数top表示を実CLI生成HTMLで確認する。ブラウザ手順とローカル補助を用意し、文字Range行断片・切取り祖先・隣接内容を含む矩形原本と全文画像を保存し、値を補正せず判定する。厳格な自己要素内縦包含を必須にしない。

## 独立統合検証と後続工程（4.1–4.2）
- source: openspec/changes/r-50053edc-wordfreq-html/tasks.md:16-23
- type: protocol
- content: 検証開始時の作業状態と製品差分を保存しheadと実行コードの対応を確かめる。品質が入力原本からCLIを独立再実行し全形式を照合、空/通常/top/長文/注入を通常幅と320 CSS pxで確認する。文書を開く前から終了まで通信を記録し、失敗試行・文書由来遷移とブラウザ背景通信を区別する根拠を残す。静的外部参照検査と通信試行記録を併用し遮断だけで無通信としない。全画像を実際に読み幾何原本と合わせACごとに判定する。未実施は未検証。全自動試験と差分を確認しCI/依存追加等の範囲逸脱がないことを示す。承認後GSD計画で検証可能PLANへ対応付け、実装・品質・受入後に別工程でsync/archiveする。現タスクは全て未実施。

DATA_5df1e033_END
