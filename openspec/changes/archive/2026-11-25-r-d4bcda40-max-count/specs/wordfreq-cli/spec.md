# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
