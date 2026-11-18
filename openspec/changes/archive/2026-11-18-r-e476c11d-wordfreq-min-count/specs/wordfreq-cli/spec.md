# Spec Delta

## ADDED Requirements

### Requirement: 最小出現回数オプション（MC-1、AC1–AC4）
システムは（SHALL）`--min-count N`で表示する語の最小出現回数を指定できるようにする。既定は1で、1以上の整数のみ受理する。それ以外と値欠落は入力取得より先に使い方エラーexit2とし、stderrへ通知しstdoutは空にする。全形式で正規化後の回数N未満の語を除き、NちょうどとN超を残した後、独立した`--top`の値で表示件数を制限する。抽出・casefold・同数初出順・既存のエラー契約は維持しなければならない（MUST）。

#### Scenario: 下限未満と境界値と超過
- **WHEN** `beta beta beta alpha gamma alpha delta`を各形式で`--min-count 2 --top 10`として実行する
- **THEN** beta 3、alpha 2の順だけを表示し、gammaとdeltaを表示せずexit0となる

#### Scenario: topとの順序と独立値
- **WHEN** `Zoo apple APPLE zoo banana`を各形式で`--min-count 2 --top 1`および`--top 10 --min-count 2`として実行する
- **THEN** 前者はzoo 2のみ、後者はzoo 2、apple 2の順となる。min-countで除いた後topを適用し、topとmin-countに大小制約は課さない

#### Scenario: Unicode正規化してから閾値を判定
- **WHEN** `Straße STRASSE`を各形式で`--min-count 2`として実行する
- **THEN** strasseを回数2として残す。未正規化の別々の回数で除外しない

#### Scenario: 引数エラーは形式と入力読込みに優先
- **WHEN** 各形式でmin-countに0、負数、1.5、abcを渡す、または値を欠落させる。入力は不存在パスも含める
- **THEN** exit2、stderrに使い方エラー、stdout空となり、TracebackやエラーHTMLを出さない

#### Scenario: 有効な閾値でも入力失敗は失敗
- **WHEN** 各形式で有効な`--min-count 2`を指定し、不存在・ディレクトリ・開けない・不正UTF-8の入力を与える
- **THEN** 既存どおりexit1、stderrへ通知、stdout空となり、空結果のexit0へ変換しない

### Requirement: 空結果と既定互換（MC-2、AC1–AC2、AC7）
システムは（SHALL）min-count未指定と明示1について従来の出力・並び・各形式の構造を維持する。空ファイル、抽出0語、閾値で全件除外はexit0とし、textは空文字、jsonは`[]`と末尾改行1つ、htmlは既存のメタ情報・3列見出し・0データ行・空状態文言を保持する。HTMLの見た目、CSS、静的安全性、basename限定、UTF-8とescapeは変えない。

#### Scenario: 未指定と1と従来の出力
- **WHEN** 同数語と10種類超を含む同一入力・既存引数で、変更前と変更後の未指定および明示`--min-count 1`を各形式で比較する
- **THEN** stdoutが一致し、既定text/top10と回数降順・同数初出順は不変である

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

## MODIFIED Requirements

### Requirement: 表示件数オプション（FR-2）
システムは（SHALL）`--top N`で表示件数を指定できるようにする。既定値は10。Nは1以上の整数でなければならず、それ以外（整数でない、0以下）は使い方エラーexit2とする。min-countで絞った後の結果の種類数がNより少なければ、その結果全件を出力する。両オプションの値は独立である。

#### Scenario: 既定は 10 件
- **WHEN** `--top`を省略して、min-countを満たす10種類以上の語を含むファイルを指定する
- **THEN** 上位10件だけが出力される

#### Scenario: 件数指定と全件出力
- **WHEN** `--top 3`を指定する
- **THEN** min-count適用後の上位3件が出力される
- **AND** 残った種類数が3に満たなければ残った全種類が出力される

#### Scenario: 不正な件数
- **WHEN** `--top 0`または`--top abc`を指定する
- **THEN** 使い方エラーとしてstderrにメッセージが出てexit2となる

### Requirement: 出力の順序決定論性（FR-4・D-2）
システムは（SHALL）正規化後の回数がmin-count未満の語を除外してから、出現回数降順に並べ、同数時は正規化後の同じ語として入力トークン列に最初に出現した順で並べ、その後topで制限する。text・json・htmlで一致し、同じ入力とオプションでは決定論的でなければならない（MUST）。既存の初出順を維持し、過去の単語昇順へ戻さない。抽出・casefold規則は変更しない。

#### Scenario: 同回数ワードは単語の昇順
- **WHEN** zooがappleより先に現れ、両者がともに5回出現するファイルを各形式で実行する
- **THEN** 両者はzoo、appleの順で出力され、語の昇順へ戻らない。このシナリオ名は旧仕様の識別子として保持するが、旧期待値のapple、zooは廃し、初出順を維持する

#### Scenario: 正規化とtop境界
- **WHEN** `Zoo apple APPLE zoo banana`を各形式でtop1およびtop2で実行する
- **THEN** min-count既定1ではtop1はzoo 2だけ、top2はzoo 2、apple 2の順となり、後の再出現で初出位置が変更されない

### Requirement: HTMLの入力情報と総出現回数（HTML-2、AC2）
システムは（SHALL）表より上に実行環境のパス規則によるbasenameのみと、min-countとtopを適用する前の入力全体の総出現回数を表示する。総数は種類数や表示行の和ではない。ディレクトリをtitleや属性を含むHTMLのどこにも埋め込まない。topの既定10・正の整数のみという現行契約を維持し、min-countを満たす種類数がtop以下ならその全種類、topを超えるならその上位top種類を表示する。

#### Scenario: topを変えても総数は一定
- **WHEN** `zoo apple zoo banana apple cherry`を含む下位ディレクトリのファイルをtop1・2・10でhtml出力する
- **THEN** min-count既定1でbasenameのみと総数6が表より前にあり、行はそれぞれzoo 2のみ、zoo 2とapple 2、zoo 2とapple 2とbanana 1とcherry 1の4行となる

#### Scenario: 異なる頻度の入力とtop
- **WHEN** `beta beta beta alpha gamma alpha delta`をtop2でhtml出力する
- **THEN** 総数は7、行はbeta 3とalpha 2であり、表示回数の和5を総数としない

#### Scenario: top既定と不正値
- **WHEN** html形式でmin-countを満たす11種類以上の語を含むファイルにtopを省略する、またはtopに0・負数・非整数を指定する
- **THEN** 省略時は10行、残った種類数より大きい正整数なら残った全種類。不正値ではexit2でstderrにエラーを出し結果HTMLは出さない

#### Scenario: 閾値とtopの両方で表示を絞る
- **WHEN** `beta beta beta alpha gamma alpha delta`を`--min-count 2 --top 1 --format html`で実行し、さらにmin-countを4に変える
- **THEN** 前者はbeta 3の1行と総数7、後者はデータ0行と総数7を示す。表示順位は残った行に1から付け、元集計を総数に用いる
