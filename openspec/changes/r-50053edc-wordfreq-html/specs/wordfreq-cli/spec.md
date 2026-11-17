# Spec Delta

## MODIFIED Requirements

### Requirement: 実行方法とファイル読み込み（FR-1）
`python -m wordfreq <file>` は、ファイル引数ちょうど 1 個を受け取り、そのファイルを UTF-8 として読んで頻度集計の結果を出力する。ファイルが存在しない・開けない・UTF-8 としてデコードできない場合は、エラーメッセージを stderr に出して exit 1 で終了する。ファイル引数が 0 個または 2 個以上の場合は使い方エラーとして stderr にメッセージを出して exit 2 で終了する。空ファイルは結果 0 件として exit 0 で正常終了する。システムはこれらの動作を全形式で維持しなければならない（MUST）。

#### Scenario: 通常のファイルで語頻度が出力される
- **WHEN** 英単語を含む UTF-8 テキストファイルを指定して `python -m wordfreq <file>` を実行する
- **THEN** 正規化後単語の出現回数が多い順に上位 10 件が出力され、exit code は 0 である

#### Scenario: 存在しないファイルは非 0 終了
- **WHEN** 存在しないパスを指定して実行する
- **THEN** stderr にエラーメッセージが出て、exit code は 1 であり、stdout に結果が出力されない

#### Scenario: デコード失敗は非 0 終了
- **WHEN** UTF-8 としてデコードできないバイト列のファイルを指定して実行する
- **THEN** stderr にエラーメッセージが出て、exit code は 1 である

#### Scenario: 空ファイルは 0 件で正常終了
- **WHEN** 0 バイトのファイルを指定して実行する
- **THEN** 結果0件でexit 0となる。textでは出力なし、jsonでは `[]` と末尾改行、htmlではbasenameと総数0と3列の見出しを持つ文書で、データ行は0件である

#### Scenario: ファイル引数が 1 個でない
- **WHEN** ファイル引数なし、または 2 個以上で実行する
- **THEN** 使い方エラーとして stderr にメッセージが出て、exit code は 2 である

#### Scenario: HTML指定でも読込みエラーを隠さない
- **WHEN** html形式で不存在・開けない・UTF-8デコード不能のファイルを指定する
- **THEN** stderrにエラーを出してexit 1となり、stdoutへ結果HTMLを出さない

### Requirement: 出力形式オプション（FR-3）
`--format text|json|html` は出力形式を指定する。既定はtext。システムは（SHALL）textを `count\tword\n` の行、jsonを `{"word": <str>, "count": <int>}` のオブジェクトの配列と末尾改行、htmlを1枚の静的HTML文書としてstdoutに出す。全形式で「出力の順序決定論性」の順序に一致する。不正な形式指定は使い方エラー（exit 2）とし、htmlのメタ情報をtext/jsonへ追加しない。

#### Scenario: JSON 出力が機械可読
- **WHEN** `--format json` を指定して実行する
- **THEN** stdoutが `json.loads` で解析できる配列であり、各要素が `word`（文字列）と `count`（整数）を持つ

#### Scenario: 不正な形式指定
- **WHEN** `--format xml` を指定する
- **THEN** 使い方エラーとしてstderrにメッセージが出てexit 2となり、stdoutに結果は出ない

#### Scenario: HTML選択と既存形式の保護
- **WHEN** 同じ入力・top指定でtext・json・htmlを実行する
- **THEN** 全形式で同じ語と回数が同じ順序で出る。textはcount先頭のタブ区切り、jsonは既存配列を維持し、順位・ファイル名・総数を追加するのはhtmlだけである

### Requirement: 出力の順序決定論性（FR-4・D-2）
システムは（SHALL）出現回数降順に並べ、同数時は正規化後の同じ語として入力トークン列に最初に出現した順で並べ、その後topで制限する。text・json・htmlで一致し、同じ入力とオプションでは決定論的でなければならない（MUST）。これは従来の正規化後単語の昇順を意図的に置き換える互換性変更である。抽出・casefold規則は変更しない。

#### Scenario: 同回数ワードは単語の昇順
- **WHEN** zooがappleより先に現れ、両者がともに5回出現するファイルを各形式で実行する
- **THEN** 両者はzoo、appleの順で出力され、語の昇順へ戻らない。このシナリオ名は旧仕様の識別子として保持するが、旧期待値のapple、zooは廃し、初出順へ明示的に変更する

#### Scenario: 正規化とtop境界
- **WHEN** `Zoo apple APPLE zoo banana` を各形式でtop 1およびtop 2で実行する
- **THEN** top 1はzoo 2だけ、top 2はzoo 2、apple 2の順となり、後の再出現で初出位置が変更されない

## ADDED Requirements

### Requirement: 自己完結したHTML表（HTML-1、AC1）
html形式は順位・単語・回数の3列の見出しとデータ行を持つ1枚のHTMLをstdoutへ出さなければならない（MUST）。UTF-8を宣言し、必要なCSSは文書内に持つ。スクリプト、外部のスタイル・画像・フォント等の参照、外部通信を生む要素を含めない。正常時はexit 0で、stdoutに説明ログを混ぜない。

#### Scenario: ローカルで静的に開く
- **WHEN** 実CLIのstdoutをHTMLファイルとして保存し、ネットワーク接続のないブラウザで開く
- **THEN** 順位・単語・回数の表が表示され、日本語のファイル名も文字化けしない。外部リソース参照と外部通信の試行はなく、JavaScriptなしで内容を読める

### Requirement: HTMLの入力情報と総出現回数（HTML-2、AC2）
システムは（SHALL）表より上に実行環境のパス規則によるbasenameのみと、topを適用する前の入力全体の総出現回数を表示する。総数は種類数や表示行の和ではない。ディレクトリをtitleや属性を含むHTMLのどこにも埋め込まない。topの既定10・正の整数のみという現行契約を維持し、単語の種類数がtop以下なら全種類、topを超えるなら上位top種類を表示する。

#### Scenario: topを変えても総数は一定
- **WHEN** `zoo apple zoo banana apple cherry` を含む下位ディレクトリのファイルをtop 1・2・10でhtml出力する
- **THEN** basenameのみと総数6が表より前にあり、行はそれぞれzoo 2のみ、zoo 2とapple 2、zoo 2とapple 2とbanana 1とcherry 1の4行となる

#### Scenario: 異なる頻度の入力とtop
- **WHEN** `beta beta beta alpha gamma alpha delta` をtop 2でhtml出力する
- **THEN** 総数は7、行はbeta 3とalpha 2であり、表示回数の和5を総数としない

#### Scenario: top既定と不正値
- **WHEN** html形式で11種類以上の語を含むファイルにtopを省略する、またはtopに0・負数・非整数を指定する
- **THEN** 省略時は10行、種類数より大きい正整数なら全種類。不正値ではexit 2でstderrにエラーを出し、結果HTMLは出さない

### Requirement: 明るい背景と表示行順位（HTML-3、AC4）
システムは（SHALL）明るい背景だけを用い、切替を設けない。順位はtop適用後の表示行に1から順に付ける。同数でも同順位や欠番にしない。

#### Scenario: 同数の行と順位
- **WHEN** zooとappleが同数の入力をtop 2でhtml出力する
- **THEN** 表示順に順位1、2を付け、背景は明るく、テーマ切替はない

### Requirement: 小画面での全文可読性（HTML-4、AC4）
システムは（SHALL）通常幅および320 CSS pxを含むスマートフォン幅で、長い連続語・長いbasenameを含め全文を読める表を提供する。折返しを許し、省略・切取りで内容を失わせない。文字範囲の実測原本を残し、横方向の収まり、切取り祖先内の収まり、隣接内容との非重複、実画像での可読性で合否を判定する。要素自身への厳格な縦包含は必須にしない。

#### Scenario: 長い内容を狭い幅で読む
- **WHEN** 長い連続語・長いbasenameを持つ実CLI生成HTMLを、通常幅と320 CSS pxで表示する
- **THEN** ページと文字が横方向にはみ出さず、切取り祖先により欠けず、隣接内容と重ならず、実画像で全文を読める。viewport・要素・文字Rangeの行断片・切取り祖先の矩形を原本のまま保存する

#### Scenario: 文字の縦範囲を隠さず評価する
- **WHEN** 文字Rangeが要素自身の縦の矩形をわずかに越えるが、切取り祖先から欠けず、横収まり・非重複・画像可読性を満たす
- **THEN** その実測値を保存し、要素自身の厳格な縦包含だけを理由に不合格としない。逆に切取り・重なり・読めない画像があれば合格にしない

### Requirement: HTMLデータの安全な表示（HTML-5、AC5）
システムは（SHALL）単語とbasenameを実行可能なマークアップでなく表示テキストとして扱い、HTML特殊文字を安全にエスケープする。データからタグ・イベント・スクリプト・外部通信を生じさせない。特殊文字の検査のために単語認識規則や入力仕様を変更しない。

#### Scenario: 特殊文字と注入候補
- **WHEN** 有効なbasenameに `& < > " '` やタグに似た文字列を含むファイルをCLIでhtml出力し、整形の部品単体では同様の特殊文字を持つ単語を与える
- **THEN** 表示文字は元のデータと一致し、追加のタグ・イベント・スクリプト・外部通信は生じない。通常CLIでは従来のUnicode抽出とcasefoldを維持する

### Requirement: HTML検証の独立した証拠（HTML-6、AC6）
自動試験と品質担当の実CLI再生成による独立ブラウザ確認を行わなければならない（MUST）。証拠は検証head、入力原本、コマンド、exit/stdout/stderrと期待値、生成HTML、ブラウザとviewport、文字範囲の実測原本、画面画像、外部通信検査結果をACごとに追跡可能に保存・添付する。未実施の条件を合格扱いせず、CIは追加・変更しない。

#### Scenario: 条件ごとに証拠を辿る
- **WHEN** 品質担当が受入判定のためHTMLを検査する
- **THEN** 対象headで自らCLIを実行し、空・通常・top・長文・安全性・320 CSS pxと通常幅の結果を検査して、文字範囲原本と実画像を含む証拠をAC1–AC6に対応付ける。Builderの画像だけでは独立確認の代用にしない

#### Scenario: 既存処理とCIの範囲を保つ
- **WHEN** 全自動試験と今回の差分を確認する
- **THEN** 入力取得境界、抽出・casefold、既存エラー、text/json構造が同数時順序以外は維持され、CIの追加・変更はない。生成日時・テーマ切替・対話操作・サーバーは追加しない
