# Spec Delta


## MODIFIED Requirements

### Requirement: 実行方法とファイル読み込み（FR-1）
`python -m wordfreq <file>` は、ファイル引数ちょうど 1 個を受け取り、そのファイルを UTF-8 として読んで頻度集計の結果を出力することを MUST とする。ファイルが存在しない・開けない・UTF-8 としてデコードできない場合は、エラーメッセージを stderr に出して exit 1 で終了する。ファイル引数が 0 個または 2 個以上の場合は使い方エラーとして stderr にメッセージを出して exit 2 で終了する。空ファイルは結果 0 件として exit 0 で正常終了する。エラー時は全形式で結果を stdout に出力しない。

#### Scenario: 通常のファイルで語頻度が出力される
- **WHEN** 英単語を含む UTF-8 テキストファイルを指定して `python -m wordfreq <file>` を実行する
- **THEN** 正規化後単語の出現回数が多い順に上位 10 件が出力され、exit code は 0 である

#### Scenario: 存在しないファイルは非 0 終了
- **WHEN** 存在しないパスを指定して任意の形式で実行する
- **THEN** stderr にエラーメッセージが出て、exit code は 1 であり、stdout に結果が出力されない

#### Scenario: デコード失敗は非 0 終了
- **WHEN** UTF-8 としてデコードできないバイト列のファイルを指定して任意の形式で実行する
- **THEN** stderr にエラーメッセージが出て、exit code は 1 であり、stdout は空である

#### Scenario: 空ファイルは 0 件で正常終了
- **WHEN** 0 バイトのファイルを指定して実行する
- **THEN** 結果 0 件（text では出力なし、json では `[]`、html では総数0・データ行0の完結した文書）で exit code は 0 である

#### Scenario: ファイル引数が 1 個でない
- **WHEN** ファイル引数なし、または 2 個以上で任意の形式を指定して実行する
- **THEN** 使い方エラーとして stderr にメッセージが出て、exit code は 2、stdout は空である

#### Scenario: 読取不能な入力
- **WHEN** 読取不能なファイルを指定して任意の形式で実行する
- **THEN** stderr にエラーメッセージが出て、exit code は 1、stdout は空である

#### Scenario: 非空だが単語がない入力
- **WHEN** 空白と句読点だけの非空UTF-8ファイルを指定する
- **THEN** 空ファイルと同じ0件の結果で exit code は0である

### Requirement: 出力形式オプション（FR-3）
`--format text|json|html` は出力形式を指定し、既定は text とすることを MUST とする。text は `回数<TAB>語<改行>` の1語1行、json は `{"word": <str>, "count": <int>}` の配列とし、「出力の順序決定論性」の順序に従う。html は単語・回数の表を持つ単一の完結HTML文書を stdout に出す。不正な形式は使い方エラー（exit 2）。入力名・総数を既存text/jsonの構造へ追加しない。

#### Scenario: JSON 出力が機械可読
- **WHEN** `--format json` を指定して実行する
- **THEN** stdout が `json.loads` で解析できる配列であり、各要素が `word`（文字列）と `count`（整数）を持つ

#### Scenario: 不正な形式指定
- **WHEN** `--format xml` を指定する
- **THEN** 使い方エラーとして stderr にメッセージが出て、exit code は 2、stdout は空である

#### Scenario: HTML文書の保存と閲覧
- **WHEN** UTF-8 stdoutで `--format html` の結果を入力とは別のHTMLファイルへ保存し、オフラインのブラウザで開く
- **THEN** doctype・html・head・bodyを持つ文書として単語・回数の表を読め、終了値は0、正常時stderrは空であり、stdoutにログや別文書は混ざらない

#### Scenario: 既定形式と表示件数
- **WHEN** 形式・topを省略する、またはtext/json/htmlで正整数のtopを指定する
- **THEN** 既定text・top10および既存の表示件数要件を維持し、語種数より大きいtopなら全種類を出す

### Requirement: 出力の順序決定論性（FR-4・D-2）
出力は常に、出現回数の降順、同数時は正規化後の語が入力トークン列で最初に出現した順に並べ、その後topで切ることを MUST とする。text/json/htmlすべてに適用し、旧仕様の「正規化後単語の昇順」を明示的に置換する。同期用に旧シナリオ名を保持するが、その期待動作は下記のとおり初出順へ変更する。同じ入力と同じオプションでの出力は決定論的とする。casefoldで統合される語は最初の表記の位置を初出位置とする。

#### Scenario: 同回数ワードは単語の昇順
- **WHEN** zooがappleより先に現れ、両者がともに5回出現するファイルを全形式で集計する
- **THEN** 旧名にかかわらず本変更の期待順は `zoo`、`apple` の初出順であり、旧契約の語昇順は適用しない

#### Scenario: 同回数ワードは初出順
- **WHEN** `Zoo apple zoo APPLE beta` を含むファイルを全形式でtop3に指定する
- **THEN** 正規化語と回数は `zoo:2, apple:2, beta:1` の順となり、語昇順のapple先頭にはならない

#### Scenario: top境界も初出順
- **WHEN** 同じ入力を全形式で `--top 1` に指定する
- **THEN** `zoo:2` だけを表示する

#### Scenario: casefold統合後の初出
- **WHEN** `ZOO Straße zoo STRASSE beta` を全形式で集計する
- **THEN** `zoo:2, strasse:2, beta:1` の順となり、top1でもzooを選ぶ

#### Scenario: 頻度が初出より優先する
- **WHEN** `early late late` を全形式で集計する
- **THEN** `late:2, early:1` の順となる

#### Scenario: 実行間の決定論性
- **WHEN** 同一入力と同じオプションを異なるハッシュシードで再実行する
- **THEN** 各形式内で出力が一致する（形式間でバイト列を同一にする要求ではない）

## ADDED Requirements

### Requirement: HTMLの入力名と総数（HTML-1）
HTMLは表より前に入力ファイル名と数えた単語の総出現数を表示することを MUST とする。総数は異なり語数ではない。承認案はtop前の全正規化トークン出現数とし、topは表示行だけを制限する。入力名の承認案はディレクトリを含めないbasenameの文字表示（リンクではない）とする。これらの案はQ-3/Q-4の回答で確定する。

#### Scenario: 総数と表示行数の区別（Q-3推奨案の承認後）
- **WHEN** `Zoo apple zoo APPLE beta` を `--format html --top 1` で集計する
- **THEN** 表前の総数は5、データ行はzooの1行で回数2であり、総数を異なり語数3や表示回数2としない

#### Scenario: 入力名のパス露出抑止（Q-4推奨案の承認後）
- **WHEN** ディレクトリ配下の `資料.txt` をhtmlで集計する
- **THEN** 表前に `資料.txt` が文字として現れ、ディレクトリの部分は現れない

### Requirement: HTMLの安全性と自己完結性（HTML-2）
語・入力名はHTML特殊文字を安全に表示し、入力由来のタグ・script・イベントハンドラを解釈/実行しないことを MUST とする。元の表示対象文字列を欠落・二重escapeなく読めるものとする。HTMLはJS・外部CSS/font/image・外部通信を持たずスタイルを内包する。UTF-8保存時のcharset宣言とバイトを一致させる。共有HTMLには語・名前が残る旨を利用説明に示す。

#### Scenario: 特殊文字は文字のまま表示
- **WHEN** `& < > " '` と `&amp;` 相当を含む表示対象の語/名前をHTML整形へ渡す
- **THEN** DOMのtextContentが元の文字列と一致し、要素や属性へ化けず、二重escapeや削除もない

#### Scenario: 悪意あるファイル名のCLIとブラウザ確認
- **WHEN** タグ・script・イベント属性に見える文字列を含む実ファイル名からCLIでHTMLを生成してブラウザで開く
- **THEN** 承認済み表示規則による名前が文字として現れ、入力に由来する要素/script/イベント実行はない

#### Scenario: ネットワーク不要
- **WHEN** 保存済みHTMLを実ブラウザでネットワーク記録を開始して開く
- **THEN** 単語・回数・入力名・総数を読め、外部リクエストは0件である

#### Scenario: 非ASCIIと空白を含む名前
- **WHEN** 日本語の語と日本語・連続スペース・タブ・LF/CR/CRLFを含む入力名をUTF-8で保存して開く
- **THEN** 文字化けせず、名前の空白文字も保持して表示され、表示対象のDOM文字列は元と一致する

### Requirement: モバイルの表の可読性（HTML-3）
HTMLはviewport設定と語/回数の列見出しを持つ意味的tableを備えることを MUST とする。mobile CSS viewport320px/375pxとdesktop1280pxで長い語・入力名を折り返し、省略・欠落・重複・列の重なりなく全内容を読めるものとする。ページ/表の横スクロールは不要、縦スクロールは許す。配色と順位列の有無はQ-1/Q-2の回答まで確定しない。

#### Scenario: 長い語と名前を狭い画面で読む
- **WHEN** 200文字連続の語・長い日本語入力名を持つHTMLをmobile emulationまたは実端末320px/375pxとdesktop1280pxで開く
- **THEN** 語・回数の対応と表前の情報を全文読め、横方向のoverflowや列重なりがないことを画像とDOM/layout測定で確認できる

#### Scenario: 見出しとセルの関連
- **WHEN** 出力HTMLの表をDOMで確認する
- **THEN** thead/tbodyと列見出しがあり、語・回数の見出しがscope=colでデータ列と関連する

### Requirement: HTML追加時の互換性と検証範囲（HTML-4）
HTML追加と同数順置換以外のCLI契約・入力取得境界・語の定義を維持することを MUST とする。試験には全形式の通常/空/記号のみ/top/エラー/Unicode/初出順と入力不変を含める。HTMLは整形部品への直接入力とCLI経由の両方、および実ブラウザで検証する。CIと依存の追加・変更は行わず、既存CI試験は維持する。

#### Scenario: 不正topの回帰
- **WHEN** 全形式で0以下または非整数のtopを指定する
- **THEN** exit2、stderrエラー、stdout空となる

#### Scenario: 入力不変と説明
- **WHEN** 入力と異なる出力先へ保存して集計し、実行前後の入力を比較する
- **THEN** 入力は不変であり、利用説明には同じパスへのシェルリダイレクトは起動前に入力を切り詰めるので使わない旨と、共有前確認の注意がある

#### Scenario: 品質証跡
- **WHEN** 品質がHTMLの受入条件を検証する
- **THEN** 実HTML・ブラウザ名/版・viewport幅・画像・DOM/layout・networkの記録を残し、手段不足は未検証として人へ回し、CI/依存の追加や捏造した結果で代用しない
