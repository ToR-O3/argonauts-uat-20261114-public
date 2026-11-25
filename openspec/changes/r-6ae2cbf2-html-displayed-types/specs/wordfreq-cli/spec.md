## ADDED Requirements

### Requirement: HTMLの表示語種類数
システムは（SHALL）表より上の既存総出現回数の横に`表示 N 種類`を表示する。Nは正規化・min-count・max-count・top適用後の最終データ行数であり、見出し・入力全体の種類数・回数合計・top指定値ではない。既存の総数・行内容・順位・順序・空状態を維持する。

#### Scenario: 通常の3種類
- **WHEN** PRDの入力`beta beta beta alpha gamma alpha delta`をmax2でHTML出力する
- **THEN** alpha2・gamma1・delta1の3行、総数7の横に`表示 3 種類`を示す

#### Scenario: top1と候補より大きいtop
- **WHEN** 同じ入力をmax2/top1とmax2/top99でHTML出力する
- **THEN** 総数はいずれも7で、前者はalpha2の1行と`表示 1 種類`、後者は3行と`表示 3 種類`を示す

### Requirement: 絞込みと既定top後の種類数
システムは（SHALL）上下限の適用後にtopで制限した件数を表示し、既定top10を維持する。

#### Scenario: 上下限とtopをすべて適用
- **WHEN** beta4回・zoo3回・apple2回・pear2回・single1回の入力をmin2/max3/top1でHTML出力する
- **THEN** zoo3のみの1行、総数12の横に`表示 1 種類`を示す

#### Scenario: 候補12種類で既定top
- **WHEN** 閾値適用後12種類が残る入力をtop省略でHTML出力する
- **THEN** 従来順の上位10行となり、総数の横に`表示 10 種類`を示す

### Requirement: 空結果と正規化後の種類数
システムは（SHALL）空結果でも`表示 0 種類`を示し、表記ゆれを別種類として数えない。抽出・casefold規則は変更しない。

#### Scenario: 空または語なし入力
- **WHEN** 空ファイル・空白のみ・記号のみをHTML出力する
- **THEN** 総数0の横に`表示 0 種類`を示し、既存空状態と0データ行を保つ

#### Scenario: 絞込みで全件除外
- **WHEN** PRDの総数7の入力をmax0でHTML出力する
- **THEN** 総数7の横に`表示 0 種類`を示し、既存空状態と0データ行を保つ

#### Scenario: Unicodeのcasefold合算
- **WHEN** `Straße STRASSE`をmin2/max2でHTML出力する
- **THEN** strasse2の1行、総数2の横に`表示 1 種類`を示す

### Requirement: 小変更の試験と説明
追加と既存のpytestは成功しなければならない（MUST）。新規シナリオを`tests/test_formatters.py`と`tests/test_cli.py`で検証し、READMEの既存HTML説明へ、文言・絞込み/top後の件数・空なら0を説明する1行だけを追加する。

#### Scenario: 受入の確認
- **WHEN** 追加表示の受入を判定する
- **THEN** 全新規ケースの文言・総数・行数とREADMEの追加1行を照合し、通常幅と狭幅の描画で総数の横かつ表の上に読め、既存内容を隠さないことを確認する。未実施を成功としない

### Requirement: 変更範囲と期待値の保全
システムは（SHALL）text/jsonの全バイト・末尾改行、CLI引数・exit・stderrを維持する。入力再読込み、集計・選択変更、依存・CI・権限・外部送信・移行・無関係な機能追加は禁止する。

#### Scenario: 正当なHTML差分だけを整合
- **WHEN** 今回の差分と回帰期待値を確認する
- **THEN** 封印済み過去baselineは上書きせず、今回用期待値か明示的変換で表示種類数追加と必要最小レイアウト差分だけを反映する。text/json期待値・安全性検査・過去scope gateを緩めない

## MODIFIED Requirements

### Requirement: HTMLの入力情報と総出現回数（HTML-2、AC2）
システムは（SHALL）表より上に実行環境のパス規則によるbasenameのみと、min-count・max-count・topを適用する前の入力全体の総出現回数を表示する。総数は種類数や表示行の和ではない。総数の横に最終表示データ行数を`表示 N 種類`として追加する。ディレクトリをtitleや属性を含むHTMLのどこにも埋め込まない。topの既定10・正の整数のみという現行契約を維持し、上下限を満たす種類数がtop以下ならその全種類、topを超えるならその上位top種類を表示する。

#### Scenario: topを変えても総数は一定
- **WHEN** `zoo apple zoo banana apple cherry`を含む下位ディレクトリのファイルをtop1・2・10でhtml出力する
- **THEN** min-count既定1・上限未指定でbasenameのみと総数6が表より前にあり、行はそれぞれzoo 2のみ、zoo 2とapple 2、zoo 2とapple 2とbanana 1とcherry 1の4行となる。総数の横の表示種類数はそれぞれ1・2・4である

#### Scenario: 異なる頻度の入力とtop
- **WHEN** `beta beta beta alpha gamma alpha delta`をtop2でhtml出力する
- **THEN** 総数は7、行はbeta 3とalpha 2であり、表示回数の和5を総数としない。総数の横に`表示 2 種類`を示す

#### Scenario: top既定と不正値
- **WHEN** html形式で上下限を満たす11種類以上の語を含むファイルにtopを省略する、またはtopに0・負数・非整数を指定する
- **THEN** 省略時は10行、残った種類数より大きい正整数なら残った全種類。不正値ではexit2でstderrにエラーを出し結果HTMLは出さない

#### Scenario: 閾値とtopの両方で表示を絞る
- **WHEN** `beta beta beta alpha gamma alpha delta`を`--min-count 2 --top 1 --format html`で実行し、さらにmin-countを4に変える
- **THEN** 上限未指定の前者はbeta 3の1行と総数7、後者はデータ0行と総数7を示す。表示順位は残った行に1から付け、元集計を総数に用いる。総数の横の表示種類数は前者1、後者0である

#### Scenario: 三条件の除外でも元総数を保つ
- **WHEN** beta4回・zoo3回・apple2回・pear2回・single1回の入力をmin2/max3/top1でhtml出力する
- **THEN** zoo3のみを順位1として表示し、元総数12を示す。各閾値とtopがそれぞれ別の語を除外しても元総数は変わらない。総数の横に`表示 1 種類`を示す

### Requirement: 空結果と既定互換（MC-2、AC1–AC2、AC7）
システムは（SHALL）max-count未指定の場合にmin-count未指定と明示1について従来の出力・並び・各形式の構造を維持する。空ファイル、抽出0語、上下限閾値で全件除外はexit0とし、textは空文字、jsonは`[]`と末尾改行1つ、htmlは既存のメタ情報・3列見出し・0データ行・空状態文言を保持する。HTMLの見た目、CSS、静的安全性、basename限定、UTF-8とescapeは維持し、今回の表示種類数追加と必要最小のレイアウト差分だけを見た目・CSS・HTML出力一致の例外とする。text/jsonの旧バイト列は不変とする。

#### Scenario: 未指定と1と従来の出力
- **WHEN** 同数語と10種類超を含む同一入力・既存引数で、変更前と変更後の未指定および明示`--min-count 1`を各形式で比較する
- **THEN** 上限未指定ではtext/jsonのstdoutバイト列が一致し、htmlは今回の表示種類数追加と必要最小レイアウト差分だけを除いて一致する。変更後の未指定と明示1は全形式で一致し、既定text/top10と回数降順・同数初出順は不変である

#### Scenario: 語のある入力で全件除外
- **WHEN** `Zoo apple APPLE zoo banana`を各形式で`--min-count 3`として実行する
- **THEN** 正常終了し表示語は0件。textは空、jsonは`[]`と改行、htmlは既存空状態とデータ0行、総数5を保持し、総数の横に`表示 0 種類`を示す

#### Scenario: 抽出語0件
- **WHEN** 空ファイル、空白のみ、句読点のみの入力を各形式で有効なmin-countとともに実行する
- **THEN** 正常終了して各形式の空結果となり、HTML総数は0で、その横に`表示 0 種類`を示す

### Requirement: min-countの試験と独立確認（MC-3、AC6–AC7）
pytestは下限未満・ちょうど・超、全形式、空・抽出0語・全除外、既定互換、異常値、Unicode合算、top併用を含め、既存全試験とともに成功しなければならない（MUST）。品質は対象headの実CLI生成HTMLを独立してブラウザ確認する。CIの追加変更、依存追加、今回の表示種類数追加と必要最小レイアウト差分以外の見た目変更は行わない。READMEの既存の既定・順序・不正値・全除外時の閾値調整の説明を維持する。今回追加する説明はHTMLの1行のみとする。

#### Scenario: 試験と実画像の証拠
- **WHEN** 品質が今回の受入を判定する
- **THEN** pytest実行環境・件数・exit結果、CLIのargv/入力/stdout/stderr、検証head、HTML原本、通常幅1280×900と狭幅320×900・DPR1の画像と閲覧結果をACへ対応付ける。既定表示は同条件の変更前原本と比較し、今回の表示種類数追加と必要最小レイアウト差分だけを許容し、絞込み時の行・元総数・全除外も確認する。未実施は合格としない

#### Scenario: 内部順序と範囲の確認
- **WHEN** 品質が差分と既存CI状態を確認する
- **THEN** 閾値除外がtop制限より先である該当箇所を記録し、CI・依存の追加変更と今回の表示種類数追加に必要最小の差分以外の見た目変更がないことを確認する。出力一致だけで内部順序を確認済みにしない。既存CIの未報告・pendingを成功と呼ばず、CIを待つ処理や新CIを追加しない

### Requirement: 上限選択の空結果と互換性（MAX-2）
システムは（SHALL）正常に読み込めた入力で上限0・負数・下限>上限・全件除外・空入力・抽出0語を正常な空結果としてexit0・stderr空で返す。textは空、jsonは`[]`と末尾改行1つ、htmlは既存の見出し3列・データ0行・空状態・basename・元総数を保ち、総数の横に`表示 0 種類`を追加する。有効な上限でも入力失敗を隠してはならない（MUST）。上限未指定では旧出力のバイト列・終了コード・構造・UTF-8・安全性を維持し、HTMLの表示種類数追加と必要最小レイアウト差分だけを旧HTMLバイト列・構造の一致から除外する。text/jsonの旧バイト列は不変とする。

#### Scenario: 全除外と不一致区間
- **WHEN** 総数7の通常入力を各形式でmax0、max-1、min3/max2として実行する
- **THEN** それぞれ既存の空形式でexit0となり、HTML総数は7のままで、その横に`表示 0 種類`を示す

#### Scenario: 空または抽出0語
- **WHEN** 空・空白のみ・記号のみの入力を各形式で有効な上限とともに実行する
- **THEN** 各形式の既存空結果でexit0、HTMLの場合のみ総数0とその横の`表示 0 種類`を示す

#### Scenario: 有効な上限でも入力失敗は失敗
- **WHEN** max0・負数など有効整数を指定し、不存在・ディレクトリ・権限による読込み失敗・不正UTF-8を与える
- **THEN** exit1・stderrへ通知・stdout空となり、選択集合が空でも入力取得を省略しない

#### Scenario: 空集合でも既存引数の検証は必要
- **WHEN** max0または負数と、不正なmin-count0またはtop0をそれぞれ併用する
- **THEN** 入力取得前にexit2・stderrへ通知・stdout空となる

#### Scenario: 省略互換と大きな上限
- **WHEN** 全形式で上限省略と十分大きい上限を用いて既存の呼出しを行う
- **THEN** 両者のstdoutバイト列・exit・stderrは既存の保存済み出力または変更前の固定期待値と一致する。ただしHTMLは今回の表示種類数追加と必要最小レイアウト差分だけを例外とし、過去baseline原本を保存して今回用期待値または明示的変換で照合する。text/jsonは旧バイト一致を厳守する。変更後の2呼出し同士の比較だけでは互換確認済みとしない

### Requirement: 上限の試験と使用例（MAX-3）
追加pytestと既存全試験は成功しなければならない（MUST）。上限境界・min併用・top・Unicode・全形式・空結果・エラー・省略互換を含む。READMEの既存の使用例1つと、整数（0・負数含む）、省略時上限なし、包含、min併用、逆転は空、上限による全除外の調整の説明を維持しなければならない（MUST）。これらは今回の新規追加要求ではなく、今回追加するREADME説明はHTMLの1行のみとする。依存・CI・無関係な機能を追加変更せず、HTMLの見た目変更は今回の表示種類数追加と必要最小レイアウト差分だけに限る。

#### Scenario: 使用例を再現できる
- **WHEN** READMEの既存の1例として`beta beta beta alpha gamma alpha delta`をinput.txtに用意し、`python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`を実行する
- **THEN** `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]`と末尾改行、exit0・stderr空となる。READMEの同じ例に入力と期待結果の併記を維持する

#### Scenario: 試験と独立した結果の記録
- **WHEN** 実装後に品質が受入の証拠を確認する
- **THEN** 追加と全既存pytestの環境・コマンド・件数・exit、対象head、実CLIの入力・argv・exit/stdout/stderrを受入条件ごとに文字の検証記録へ対応付ける。HTMLは既存の独立ブラウザ確認義務を保ち、未指定互換・絞込み・全除外・元総数を確認する。互換比較は今回の表示種類数追加と必要最小レイアウト差分だけを例外とし、封印済み過去baselineを上書きしない。未実施を成功と呼ばない
