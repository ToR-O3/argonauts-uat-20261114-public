# Constraints (intel)

今回のSPEC分類1文書の6 Requirementを抽出。tasks.mdはDOC分類としてcontext.mdへ格納する。承認済みSPECが機能契約の正。旧シナリオ名を理由に語昇順へ戻さない。

DATA_b2810436_START

## 最小出現回数オプション（MC-1、AC1–AC4）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:5-26
- type: api-contract
- content: --min-count Nは既定1、1以上の整数のみ。不正値0/負数/1.5/abc/値欠落は各形式で入力取得より先にexit2、stderr通知、stdout空、Traceback/エラーHTMLなし（不存在パスでも）。全形式で正規化後回数N未満を除外しNちょうど/超を残してから独立したtopで制限。抽出/casefold/同数初出順/既存エラー契約を維持。beta beta beta alpha gamma alpha deltaをN2/top10ならbeta3,alpha2。Zoo apple APPLE zoo bananaをN2/top1ならzoo2、top10/N2ならzoo2,apple2。Straße STRASSEをN2でstrasse2。有効N2で不存在/ディレクトリ/開けない/不正UTF-8はexit1、stderr、stdout空であり、空結果exit0へ変換しない。

## 空結果と既定互換（MC-2、AC1–AC2、AC7）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:28-41
- type: api-contract
- content: 未指定と明示1は従来出力・並び・各形式構造を維持。同数と10種類超の同一入力・既存引数で変更前/後のstdoutを比較、既定text/top10・回数降順/同数初出順不変。空ファイル/抽出0語/閾値全除外はexit0、text空文字、jsonは[]と末尾改行1つ、htmlは既存メタ情報/3列見出し/0データ行/空状態文言を保持。HTMLの見た目/CSS/静的安全性/basename限定/UTF-8/escapeは変更しない。Zoo apple APPLE zoo bananaをN3なら表示0/総数5、空/空白/句読点のみなら総数0。

## min-countの試験と独立確認（MC-3、AC6–AC7）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:43-52
- type: protocol
- content: pytestは下限未満/ちょうど/超・全形式・空/抽出0語/全除外・既定互換・異常値・Unicode合算・top併用を含み既存全試験とともに成功すること。品質が対象headの実CLI生成HTMLを独立ブラウザ確認。pytest環境/件数/exit、CLI argv/入力/stdout/stderr、head、HTML原本、1280×900と320×900・DPR1の画像/閲覧結果をACに対応付ける。既定は同条件の変更前原本と比較し、絞込み行/元総数/全除外を確認。未実施は合格でない。品質は閾値除外がtopより先の該当ソースを記録し、出力一致だけで内部順序確認済みにしない。CI追加変更/依存追加/見た目変更なし。既存CI未報告/pendingを成功と呼ばず、CI待機処理や新CIを追加しない。READMEは既定・順序・不正値・全除外時の閾値調整を説明。

## 表示件数オプション（FR-2）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:56-70
- type: api-contract
- content: --top Nは既定10、1以上の整数。不正値（非整数/0以下）はstderr、exit2。min-count適用後に上位N件とし、残った種類数がN未満なら残った全件。両値は独立。省略時は条件を満たす10種類以上から上位10件、top3なら条件を満たす上位3件または残った全種類。

## 出力の順序決定論性（FR-4・D-2）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:72-81
- type: nfr
- content: 正規化後回数でmin-count未満を除外→回数降順/同数正規化後初出順→top。text/json/htmlで一致し同じ入力/オプションで決定論的。抽出/casefoldは不変。zooが先で両者5回ならzoo,apple、語昇順へ戻さない。「同回数ワードは単語の昇順」は旧シナリオ識別子であって旧期待値apple,zooは廃止済み。Zoo apple APPLE zoo bananaを既定N1/top1ならzoo2、top2ならzoo2,apple2、後の再出現で初出位置を変更しない。

## HTMLの入力情報と総出現回数（HTML-2、AC2）
- source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:83-100
- type: api-contract
- content: 表より上に実行環境のパス規則のbasenameのみとmin-count/top前の入力全体総出現回数。種類数や表示行回数和で代替しない。title/属性を含む全HTMLにディレクトリ情報なし。top既定10/正整数、閾値を満たす種類数がtop以下なら全件、超えれば上位top。不正topはexit2/stderr/HTMLなし。zoo apple zoo banana apple cherryはN1/top1,2,10すべて総数6、行は1,2,4。beta beta beta alpha gamma alpha deltaはtop2でbeta3,alpha2/総数7、N2/top1でbeta3/総数7、N4なら0行/総数7。順位は残った行の1始まり連番。

DATA_b2810436_END
