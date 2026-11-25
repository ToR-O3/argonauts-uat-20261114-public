# Constraints (intel)

今回のSPEC 1文書のADDED 5要求とMODIFIED 5要求を保持する。以下は要求の抽出であり実装/検証済みの宣言ではない。既存locked決定との衝突は報告し、解消したことにしない。

DATA_fd245eb5_START

## HTMLの表示語種類数
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:3-12
- type: api-contract
- content: 表より上の総出現回数の横に表示 N 種類。Nは正規化・min/max・top後の最終データ行数で、見出し・入力全体の種類数・回数合計・top値ではない。総数・行・順位・順序・空状態を維持。beta beta beta alpha gamma alpha deltaのmax2はalpha2/gamma1/delta1・総数7・表示3、top1はalpha2・表示1、top99は3行・表示3。

## 絞込みと既定top後の種類数
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:14-23
- type: api-contract
- content: 上下限後にtop、既定10を維持。beta4/zoo3/apple2/pear2/single1のmin2/max3/top1はzoo3の1行・元総数12・表示1。閾値後12種類でtop省略は従来順の10行・表示10。

## 空結果と正規化後の種類数
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:25-38
- type: api-contract
- content: 空・空白・記号のみは0行・総数0・表示0。総数7の入力でmax0は0行・総数7・表示0。既存空状態を保持。Straße STRASSEのmin2/max2はstrasse2の1行・総数2・表示1。抽出/casefoldを変えず表記ゆれを別種類にしない。

## 小変更の試験と説明
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:40-45
- type: protocol
- content: 追加と全既存pytest成功を要求。tests/test_formatters.pyとtests/test_cli.pyで新規シナリオ、文言・総数・行数を検証。READMEの既存HTML説明に文言・絞込み/top後・空0の説明1行だけ追加。通常幅/狭幅の描画で総数横・表より上の位置と可読性、既存内容を隠さないことを確認し未実施を成功にしない。

## 変更範囲と期待値の保全
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:47-52
- type: nfr
- content: text/json全バイト・末尾改行、CLI引数・exit・stderrを維持。入力再読込み・集計/選択変更・依存/CI/権限/外部送信/移行/無関係機能追加は禁止。封印済み過去baselineは上書きせず今回用期待値か明示的変換で表示追加と必要最小レイアウト差分だけ反映。text/json期待値・安全性検査・過去scope gateは緩めない。

## HTMLの入力情報と総出現回数（HTML-2、AC2）
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:56-77
- type: api-contract
- content: basenameのみとmin/max/top前の元総数を表より上に出し、総数横に表示種類数を追加。title/属性を含めディレクトリ情報なし。top既定10・正整数、不正0/負数/非整数はexit2・stderr・HTMLなし。zoo apple zoo banana apple cherryのtop1/2/10は総数6・行数/表示1/2/4（初出zooがappleより前）。beta beta beta alpha gamma alpha deltaのtop2はbeta3/alpha2・元総数7・表示2、min2/top1はbeta3・表示1、min4は0行・表示0で元総数7。三条件min2/max3/top1のzoo3も元総数12・順位1・表示1。

## 空結果と既定互換（MC-2、AC1–AC2、AC7）
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:79-92
- type: api-contract
- content: max未指定のmin未指定/明示1は従来の順序・構造を維持。空/抽出0語/全除外はexit0、text空・json[]+末尾改行1つ・HTML既存メタ/3列/0行/空文言。HTML CSS/見た目/バイト一致の例外は表示追加と必要最小レイアウトだけ。UTF-8/escape/静的安全性/basename限定とtext/json旧バイトを維持。変更前固定値と比較し、変更後の未指定と明示1も全形式一致。Zoo apple APPLE zoo bananaのmin3は表示0・元総数5、抽出0語は表示0・総数0。

## min-countの試験と独立確認（MC-3、AC6–AC7）
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:94-103
- type: protocol
- content: 下限未満/ちょうど/超・全形式・空/全除外・既定互換・異常・Unicode・topと既存全pytestを成功させる。品質が対象headの実CLI HTMLを独立生成/ブラウザ確認し、1280×900と320×900 DPR1の画像と閲覧結果、同条件変更前比較、環境/件数/exit/head/argv/入力/stdout/stderr/HTML原本をAC別記録。表示追加と必要最小差分以外の見た目変更なし。閾値除外がtopより先のソース箇所を記録。CI未報告/pendingを成功扱いせずCI待機処理/新CI/依存を追加しない。既存README説明維持、追加はHTMLの1行のみ。

## 上限選択の空結果と互換性（MAX-2）
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:105-126
- type: api-contract
- content: 正常読込みのmax0/負数/min>max/全除外/空/抽出0語はexit0・stderr空、text空・json[]+改行・HTML既存3列/0行/空状態/basename/元総数と表示0。語あり全除外は元総数7、抽出0語は0。有効max0/負数でも入力を短絡せず不存在/ディレクトリ/読込拒否/不正UTF-8はexit1・stderr・stdout空。不正min0/top0併用は入力取得前exit2。上限省略/大上限を保存済み出力か変更前固定期待値と照合し、新コード同士だけの比較で代用しない。HTML表示追加/最小レイアウトだけ例外、封印baseline保全、text/json旧バイト厳守。

## 上限の試験と使用例（MAX-3）
- source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:128-137
- type: protocol
- content: 上限境界/min/top/Unicode/全形式/空/エラー/省略互換と全既存pytest成功。既存README例python -m wordfreq input.txt --min-count 2 --max-count 3 --format json、入力beta beta beta alpha gamma alpha delta、期待beta3/alpha2のJSON+改行・exit0・stderr空を維持。整数全域/省略上限なし/包含/min併用/逆転空/上限全除外調整説明も維持し、新規README要求はHTMLの1行のみ。品質は対象headの独立CLIとブラウザ、未指定/絞込み/全除外/元総数を確認し環境/コマンド/件数/exit/入力/argv/stdout/stderrをAC別文字証拠にする。baseline上書きなし、差分例外限定、未実施を成功と呼ばない。

DATA_fd245eb5_END
