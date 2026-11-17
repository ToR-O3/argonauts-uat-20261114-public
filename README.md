# argonauts-uat public

Argonauts v1.10 acceptance test repository.

## wordfreq — リポジトリ内で実行

Python 3で、このリポジトリのルートから実行します。ランタイムは標準ライブラリのみで、インストールは不要です。入力はUTF-8のファイル1個です。

```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --format text --top 3
python -m wordfreq input.txt --format json --top 3
```

`--format` は `text|json|html`（既定 `text`）、`--top N` は1以上の整数（既定10）です。語種数を超えるtopは全種類を表示します。Unicodeの単語文字（字母・数字・下線）の連続を抽出してcasefoldします。日本語の形態素解析は行いません。

- text: `回数<TAB>語<改行>`。空入力・記号のみでは出力なし。
- json: `word`と`count`だけを持つ配列。空は `[]`。順位・入力名・総数は追加しません。
- html: 単一の自己完結UTF-8文書。明るい背景の順位/単語/回数3列、表前にbasenameとtop前の総出現数を表示します。順位は選択後1始まりの連番で、同数も別番号です。空は総数0・3見出し・データ0行です。

正常時はexit0・stderr空です。不存在・読取不能・UTF-8不正はexit1、ファイル引数の個数・top・形式が不正ならexit2で、エラーはstderrのみ、stdoutは空です。

### HTMLを別ファイルへ安全に保存

無害な例として、`input.txt`に `Zoo apple zoo APPLE beta 日本語` をUTF-8で保存します。次の例はPOSIX系シェル用です。**入力と出力は別ファイル**にし、成功してCLIが終了した後で `report.html` をローカルのブラウザで開いてください。

```sh
PYTHONIOENCODING=utf-8 python -m wordfreq input.txt --format html > report.html
```

この例ではbasenameは `input.txt`、総出現数は6、表示行は `1/zoo/2, 2/apple/2, 3/beta/1, 4/日本語/1` です。`--top 1` を加えても総数6のままzooの1行だけです。HTMLの出力bytesはUTF-8固定です。text/jsonの出力規則は変更せず、上の環境変数はUTF-8 stdoutを明示する保存例です。

**同じパスへのリダイレクトは禁止です。** シェルはCLIの起動前に出力先を切り詰めるため、入力へ `>` すると、CLIが読み始める前に入力を失います。CLIでは保護できません。別名でも入力と同じ実体を指すリンクは使わず、別の出力ファイルを選んでください。失敗時の出力先は空・途中の場合があるため、正常な完成レポートと扱わないでください。途中stdoutの原子的保存や、同じ出力先への並行書込みは保証しません。

**共有HTMLは匿名化ではありません。** ディレクトリは表示しませんが、basenameと集計語・回数は残ります。共有前に名前と語に秘密・個人情報がないか確認してください。escapeはHTMLとしての解釈を防ぐためで、内容の秘匿ではありません。

### 同数順の互換性変更

**互換性変更:** text/json/htmlのすべてで、回数降順は維持し、同数時は旧来の語昇順から、casefold後の正規化語の**初出順**へ変更しました。sort後にtopを適用するため、top境界で選ばれる語も変わります。`Zoo apple zoo APPLE beta` のtop1はappleではなくzoo（2回）です。casefoldで統合される語の初出は最初の表記の位置です。同じ入力・同じオプションは同じ順になりますが、入力順を変えれば同数順も変わり得ます。text/jsonの構造、Unicode抽出、既定top10、入力境界、終了値は維持しています。

### 検証範囲と未対応

回帰試験は `python -m pytest -q` で実行します（pytestが既に使える開発環境が必要）。保存例の自動試験 `tests/test_cli.py::test_readme_html_save_example` は上のシェル行を実行し、UTF-8文書・総数・行と入力bytes不変を照合します。静的HTML解析の成功は、実ブラウザの表示や外部通信0の受入証拠ではありません。320/375/1280pxでの画像・DOM/layout・通信の実測と独立品質確認は別の受入工程です。

Webサーバ、アップロード・配信、stdin/URL入力、対話sort/graph、テーマ切替、生成日時は未対応です。HTMLは閲覧専用で、製品のJavaScriptや外部assetは使いません。
