# wordfreq-cli Specification

## Purpose
wordfreq CLI は、テキストファイルから単語の出現回数を決定論的に数え、上位 N 件を人が読むテキストまたは機械が読む JSON で出力する能力。切り出し・正規化、集計、入力取得、出力整形を分離した部品構成とし、入力元（標準入力・URL）の拡張判断を設計に記録できる状態を提供する。

## Requirements

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

### Requirement: 表示件数オプション（FR-2）
システムは（SHALL）`--top N`で表示件数を指定できるようにする。既定値は10。Nは1以上の整数でなければならず、それ以外（整数でない、0以下）は使い方エラーexit2とする。min-countと指定されたmax-countで絞った後の結果の種類数がNより少なければ、その結果全件を出力する。topと頻度閾値の値は独立である。

#### Scenario: 既定は 10 件
- **WHEN** `--top`を省略して、上下限を満たす10種類以上の語を含むファイルを指定する
- **THEN** 上位10件だけが出力される

#### Scenario: 件数指定と全件出力
- **WHEN** `--top 3`を指定する
- **THEN** 上下限適用後の上位3件が出力される
- **AND** 残った種類数が3に満たなければ残った全種類が出力される

#### Scenario: 不正な件数
- **WHEN** `--top 0`または`--top abc`を指定する
- **THEN** 使い方エラーとしてstderrにメッセージが出てexit2となる

#### Scenario: 上限を適用してから件数を制限
- **WHEN** 通常入力`beta beta beta alpha gamma alpha delta`をmax2/top1で実行する。または上限選択後11種類以上残る入力でtopを省略・十分大きい値として実行する
- **THEN** 前者はalpha2のみ。後者は省略時10件、十分大きいtopでは残った全件となる

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

### Requirement: 単語の切り出しと正規化（D-3）
単語の抽出は Unicode の単語構成文字（Python の `\w`、`re.UNICODE`）の連続する最大長とし、各トークンに `str.casefold()` を適用して正規化する。句読点・記号・空白は単語に含めない。大文字・小文字のみが異なる単語は同じ単語として集計する。トークナイザは差し替え可能な部品として実装する。

#### Scenario: 大文字小文字の同一視
- **WHEN** "Hello hello HELLO world" を含むファイルを text 形式で実行する
- **THEN** `hello` の回数は 3、`world` の回数は 1 として集計される

#### Scenario: 句読点を語に含めない
- **WHEN** "one, two. one" を含むファイルを指定する
- **THEN** `one` は句読点なしの語として 2 回に数えられ、`one,` のような語は現れない

#### Scenario: 空白区切りでない言語は未対応として振る舞いが決定的
- **WHEN** 日本語テキストを指定する
- **THEN** v1 は形態素解析せず、抽出ルール（`\w` 連続）による結果が決定論的に出力される（日本語対応は範囲外。差し替え点の存在は design.md に記録）

### Requirement: 出力の順序決定論性（FR-4・D-2）
システムは（SHALL）正規化後の回数がmin-count未満、または指定されたmax-count超の語を除外してから、出現回数降順に並べ、同数時は正規化後の同じ語として入力トークン列に最初に出現した順で並べ、その後topで制限する。text・json・htmlで一致し、同じ入力とオプションでは決定論的でなければならない（MUST）。既存の初出順を維持し、過去の単語昇順へ戻さない。抽出・casefold規則は変更しない。

#### Scenario: 同回数ワードは単語の昇順
- **WHEN** zooがappleより先に現れ、両者がともに5回出現するファイルを各形式で実行する
- **THEN** 両者はzoo、appleの順で出力され、語の昇順へ戻らない。このシナリオ名は旧仕様の識別子として保持するが、旧期待値のapple、zooは廃し、初出順を維持する

#### Scenario: 正規化とtop境界
- **WHEN** `Zoo apple APPLE zoo banana`を各形式でtop1およびtop2で実行する
- **THEN** min-count既定1・上限未指定ではtop1はzoo 2だけ、top2はzoo 2、apple 2の順となり、後の再出現で初出位置が変更されない

#### Scenario: 上限判定も正規化後の回数
- **WHEN** `Straße STRASSE 日本語 日本語`を各形式でmax1およびmin2/max2として実行する
- **THEN** 前者は空、後者はstrasse2、日本語2の順となる

#### Scenario: 上下限と同数初出順
- **WHEN** `Zoo apple APPLE zoo banana`をmin2/max2としてtop1・top2で実行する
- **THEN** top1はzoo2のみ、top2はzoo2、apple2の順となる

### Requirement: 部品分離と入力元拡張の構成（FR-5・FR-6）
切り出し・正規化を行う部品と、集計・出力整形を行う部品を分離する。テキストを得る入力取得は解析・集計から境界として分離し、v1 のファイル入力もその境界の背後で動く。各部品は単体で呼んで検証でき、入力取得を介した集計経路を通過する試験を含むこと。入力元（標準入力・URL）の追加は入力取得境界の実装追加で足りるという構成判断を、変更の design.md に記録する。

#### Scenario: 部品が単体で検証可能
- **WHEN** トークナイザ部品と集計部品を単体で呼び出す単体試験を実行する
- **THEN** 各部品は CLI を経由せずに期待される入力・出力で検証できる

#### Scenario: 入力取得境界越しの検証
- **WHEN** 入力取得境界を介した集計経路の試験を実行する
- **THEN** 解析・集計は入力取得境界を介してのみテキストを受け取ることが確認できる

### Requirement: 試験と実行環境（FR-7・FR-8）
pytest による単体試験を用意し、リポジトリの CI の pytest 実行ジョブで通じる。試験は上記要件のシナリオ（不存在ファイル、空ファイル、引数個数、不正な `--top`・`--format`、同数語の順序、大文字小文字の同一視、UTF-8 デコード失敗、JSON 構造、部品単体・境界越し検証）を含む。対象 Python は当該 CI ジョブの CPython 3 の版とし、バージョン横断互換コードを書かない。ランタイム依存は標準ライブラリのみとする。

#### Scenario: CI で pytest が通る
- **WHEN** CI の pytest ジョブが実行される
- **THEN** 全試験が成功する

#### Scenario: 標準ライブラリのみ
- **WHEN** パッケージのランタイム依存を確かめる
- **THEN** 標準ライブラリ以外の依存が宣言されていない

### Requirement: 自己完結したHTML表（HTML-1、AC1）
html形式は順位・単語・回数の3列の見出しとデータ行を持つ1枚のHTMLをstdoutへ出さなければならない（MUST）。UTF-8を宣言し、必要なCSSは文書内に持つ。スクリプト、外部のスタイル・画像・フォント等の参照、外部通信を生む要素を含めない。正常時はexit 0で、stdoutに説明ログを混ぜない。

#### Scenario: ローカルで静的に開く
- **WHEN** 実CLIのstdoutをHTMLファイルとして保存し、ネットワーク接続のないブラウザで開く
- **THEN** 順位・単語・回数の表が表示され、日本語のファイル名も文字化けしない。外部リソース参照と外部通信の試行はなく、JavaScriptなしで内容を読める

### Requirement: HTMLの入力情報と総出現回数（HTML-2、AC2）
システムは（SHALL）表より上に実行環境のパス規則によるbasenameのみと、min-count・max-count・topを適用する前の入力全体の総出現回数を表示する。総数は種類数や表示行の和ではない。ディレクトリをtitleや属性を含むHTMLのどこにも埋め込まない。topの既定10・正の整数のみという現行契約を維持し、上下限を満たす種類数がtop以下ならその全種類、topを超えるならその上位top種類を表示する。

#### Scenario: topを変えても総数は一定
- **WHEN** `zoo apple zoo banana apple cherry`を含む下位ディレクトリのファイルをtop1・2・10でhtml出力する
- **THEN** min-count既定1・上限未指定でbasenameのみと総数6が表より前にあり、行はそれぞれzoo 2のみ、zoo 2とapple 2、zoo 2とapple 2とbanana 1とcherry 1の4行となる

#### Scenario: 異なる頻度の入力とtop
- **WHEN** `beta beta beta alpha gamma alpha delta`をtop2でhtml出力する
- **THEN** 総数は7、行はbeta 3とalpha 2であり、表示回数の和5を総数としない

#### Scenario: top既定と不正値
- **WHEN** html形式で上下限を満たす11種類以上の語を含むファイルにtopを省略する、またはtopに0・負数・非整数を指定する
- **THEN** 省略時は10行、残った種類数より大きい正整数なら残った全種類。不正値ではexit2でstderrにエラーを出し結果HTMLは出さない

#### Scenario: 閾値とtopの両方で表示を絞る
- **WHEN** `beta beta beta alpha gamma alpha delta`を`--min-count 2 --top 1 --format html`で実行し、さらにmin-countを4に変える
- **THEN** 上限未指定の前者はbeta 3の1行と総数7、後者はデータ0行と総数7を示す。表示順位は残った行に1から付け、元集計を総数に用いる

#### Scenario: 三条件の除外でも元総数を保つ
- **WHEN** beta4回・zoo3回・apple2回・pear2回・single1回の入力をmin2/max3/top1でhtml出力する
- **THEN** zoo3のみを順位1として表示し、元総数12を示す。各閾値とtopがそれぞれ別の語を除外しても元総数は変わらない

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

### Requirement: 最小出現回数オプション（MC-1、AC1–AC4）
システムは（SHALL）`--min-count N`で表示する語の最小出現回数を指定できるようにする。既定は1で、1以上の整数のみ受理する。それ以外と値欠落は入力取得より先に使い方エラーexit2とし、stderrへ通知しstdoutは空にする。全形式で正規化後の回数N未満の語を除き、NちょうどとN超のうち指定されたmax-count以下の語を残した後、独立した`--top`の値で表示件数を制限する。上限未指定なら従来どおりNちょうどとN超を残す。抽出・casefold・同数初出順・既存のエラー契約は維持しなければならない（MUST）。

#### Scenario: 下限未満と境界値と超過
- **WHEN** `beta beta beta alpha gamma alpha delta`を各形式で`--min-count 2 --top 10`として実行する
- **THEN** 上限未指定ではbeta 3、alpha 2の順だけを表示し、gammaとdeltaを表示せずexit0となる

#### Scenario: topとの順序と独立値
- **WHEN** `Zoo apple APPLE zoo banana`を各形式で`--min-count 2 --top 1`および`--top 10 --min-count 2`として実行する
- **THEN** 上限未指定の前者はzoo 2のみ、後者はzoo 2、apple 2の順となる。min-countで除いた後topを適用し、topとmin-countに大小制約は課さない

#### Scenario: Unicode正規化してから閾値を判定
- **WHEN** `Straße STRASSE`を各形式で`--min-count 2`として実行する
- **THEN** 上限未指定ではstrasseを回数2として残す。未正規化の別々の回数で除外しない

#### Scenario: 引数エラーは形式と入力読込みに優先
- **WHEN** 各形式でmin-countに0、負数、1.5、abcを渡す、または値を欠落させる。入力は不存在パスも含める
- **THEN** exit2、stderrに使い方エラー、stdout空となり、TracebackやエラーHTMLを出さない

#### Scenario: 有効な閾値でも入力失敗は失敗
- **WHEN** 各形式で有効な`--min-count 2`を指定し、不存在・ディレクトリ・開けない・不正UTF-8の入力を与える
- **THEN** 既存どおりexit1、stderrへ通知、stdout空となり、空結果のexit0へ変換しない

### Requirement: 空結果と既定互換（MC-2、AC1–AC2、AC7）
システムは（SHALL）max-count未指定の場合にmin-count未指定と明示1について従来の出力・並び・各形式の構造を維持する。空ファイル、抽出0語、上下限閾値で全件除外はexit0とし、textは空文字、jsonは`[]`と末尾改行1つ、htmlは既存のメタ情報・3列見出し・0データ行・空状態文言を保持する。HTMLの見た目、CSS、静的安全性、basename限定、UTF-8とescapeは変えない。

#### Scenario: 未指定と1と従来の出力
- **WHEN** 同数語と10種類超を含む同一入力・既存引数で、変更前と変更後の未指定および明示`--min-count 1`を各形式で比較する
- **THEN** 上限未指定ではstdoutが一致し、既定text/top10と回数降順・同数初出順は不変である

#### Scenario: 語のある入力で全件除外
- **WHEN** `Zoo apple APPLE zoo banana`を各形式で`--min-count 3`として実行する
- **THEN** 正常終了し表示語は0件。textは空、jsonは`[]`と改行、htmlは既存空状態とデータ0行、総数5を保持する

#### Scenario: 抽出語0件
- **WHEN** 空ファイル、空白のみ、句読点のみの入力を各形式で有効なmin-countとともに実行する
- **THEN** 正常終了して各形式の空結果となり、HTML総数は0である

### Requirement: min-countの試験と独立確認（MC-3、AC6–AC7）
pytestは下限未満・ちょうど・超、全形式、空・抽出0語・全除外、既定互換、異常値、Unicode合算、top併用を含め、既存全試験とともに成功しなければならない（MUST）。品質は対象headの実CLI生成HTMLを独立してブラウザ確認する。CIの追加変更、依存追加、見た目変更は行わない。READMEに既定・順序・不正値・全除外時の閾値調整を説明する。

#### Scenario: 試験と実画像の証拠
- **WHEN** 品質が今回の受入を判定する
- **THEN** pytest実行環境・件数・exit結果、CLIのargv/入力/stdout/stderr、検証head、HTML原本、通常幅1280×900と狭幅320×900・DPR1の画像と閲覧結果をACへ対応付ける。既定表示は同条件の変更前原本と比較し、絞込み時の行・元総数・全除外も確認する。未実施は合格としない

#### Scenario: 内部順序と範囲の確認
- **WHEN** 品質が差分と既存CI状態を確認する
- **THEN** 閾値除外がtop制限より先である該当箇所を記録し、CI・依存・見た目の追加変更がないことを確認する。出力一致だけで内部順序を確認済みにしない。既存CIの未報告・pendingを成功と呼ばず、CIを待つ処理や新CIを追加しない

### Requirement: 最大出現回数オプション（MAX-1）
システムは（SHALL）整数オプション`--max-count N`を提供し、省略時は上限を設けず既存の動作を維持する。指定時は全形式で正規化後の出現回数N以下の語だけを残し、既存min-countの下限も同時に満たさなければならない（MUST）。境界値を含み、CLIオプションの指定順には依存しない。0・負整数も受理し、下限が上限を超えても引数エラーにはしない。既存min-countとtopの正値制約は維持する。

#### Scenario: 上限未満と境界値と超過
- **WHEN** `beta beta beta alpha gamma alpha delta`をtext/json/htmlで`--max-count 2`として実行する
- **THEN** alpha2、gamma1、delta1の順だけを表示し、beta3を除外してexit0・stderr空となる

#### Scenario: 上下限の包含と指定順
- **WHEN** 同じ入力でmin2/max2、min2/max3を指定し、CLIオプションの指定順も交換する
- **THEN** 前者はalpha2のみ、後者はbeta3・alpha2を表示し、指定順で結果は変わらない

#### Scenario: 最小の有用な正の上限
- **WHEN** 同じ入力を各形式でmax1として実行する
- **THEN** gamma1、delta1のみを表示する

#### Scenario: 整数の表記とヘルプ
- **WHEN** 0・負整数・`+2`・`02`・大きい整数・`--max-count=-1`を指定する。またはファイル引数なしで`--help`を実行する
- **THEN** 整数指定は既存整数引数と同じ解釈で受理する。helpはexit0・stderr空でstdoutに`--max-count MAX_COUNT`を示す

#### Scenario: 上限の引数エラーは入力取得より先
- **WHEN** 各形式でmaxに`abc`・`1.5`を渡す、または値を欠落させる。入力には不存在パスも含める
- **THEN** 入力を読まずexit2・stderrへ使い方エラー・stdout空となり、TracebackやエラーHTMLを出さない

### Requirement: 上限選択の空結果と互換性（MAX-2）
システムは（SHALL）正常に読み込めた入力で上限0・負数・下限>上限・全件除外・空入力・抽出0語を正常な空結果としてexit0・stderr空で返す。textは空、jsonは`[]`と末尾改行1つ、htmlは既存の見出し3列・データ0行・空状態・basename・元総数を保つ。有効な上限でも入力失敗を隠してはならない（MUST）。上限未指定では旧出力のバイト列・終了コード・構造・UTF-8・安全性を維持する。

#### Scenario: 全除外と不一致区間
- **WHEN** 総数7の通常入力を各形式でmax0、max-1、min3/max2として実行する
- **THEN** それぞれ既存の空形式でexit0となり、HTML総数は7のままである

#### Scenario: 空または抽出0語
- **WHEN** 空・空白のみ・記号のみの入力を各形式で有効な上限とともに実行する
- **THEN** 各形式の既存空結果でexit0、HTMLの場合のみ総数0を表示する

#### Scenario: 有効な上限でも入力失敗は失敗
- **WHEN** max0・負数など有効整数を指定し、不存在・ディレクトリ・権限による読込み失敗・不正UTF-8を与える
- **THEN** exit1・stderrへ通知・stdout空となり、選択集合が空でも入力取得を省略しない

#### Scenario: 空集合でも既存引数の検証は必要
- **WHEN** max0または負数と、不正なmin-count0またはtop0をそれぞれ併用する
- **THEN** 入力取得前にexit2・stderrへ通知・stdout空となる

#### Scenario: 省略互換と大きな上限
- **WHEN** 全形式で上限省略と十分大きい上限を用いて既存の呼出しを行う
- **THEN** 両者のstdoutバイト列・exit・stderrは既存の保存済み出力または変更前の固定期待値と一致する。変更後の2呼出し同士の比較だけでは互換確認済みとしない

### Requirement: 上限の試験と使用例（MAX-3）
追加pytestと既存全試験は成功しなければならない（MUST）。上限境界・min併用・top・Unicode・全形式・空結果・エラー・省略互換を含む。READMEに使用例を1つ追加し、整数（0・負数含む）、省略時上限なし、包含、min併用、逆転は空、上限による全除外の調整を説明しなければならない（MUST）。依存・CI・HTML見た目・無関係な機能を追加変更しない。

#### Scenario: 使用例を再現できる
- **WHEN** READMEの新しい1例として`beta beta beta alpha gamma alpha delta`をinput.txtに用意し、`python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`を実行する
- **THEN** `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]`と末尾改行、exit0・stderr空となる。READMEの同じ例に入力と期待結果も併記する

#### Scenario: 試験と独立した結果の記録
- **WHEN** 実装後に品質が受入の証拠を確認する
- **THEN** 追加と全既存pytestの環境・コマンド・件数・exit、対象head、実CLIの入力・argv・exit/stdout/stderrを受入条件ごとに文字の検証記録へ対応付ける。HTMLは既存の独立ブラウザ確認義務を保ち、未指定互換・絞込み・全除外・元総数を確認する。未実施を成功と呼ばない
