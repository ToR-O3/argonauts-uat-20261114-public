# 独立レビューと対応

対象: Brief・PRD・OpenSpec proposal/specs/design/tasksの6原本。実装や製品ブラウザ合格のレビューではない。
公式bmad-reviewの独立adversarial、edge-case-hunter、structureと、structure結果を渡したproseを通常終了で受領した。verification-gapはcode限定のため対象外。Brief・PRDは別にrubric walker、fresh reader、依頼原文とのreconciliationも実施。各runのreview文書を参照。

## Behavioral lenses
各行は公式のlocation / trigger_condition / guard_snippet / potential_consequenceに対応する。重複指摘を統合せず残す。

| lens | location | trigger_condition | guard_snippet | potential_consequence | 対応 |
|---|---|---|---|---|---|
| adversarial | spec HTML-2 | 「種類数未満なら全件」がtopの比較主体を曖昧にする | 種類数がtop以下なら全種類、超えるなら上位top種類とする | top解釈がシナリオと割れる | 修正済み |
| adversarial | PRD FR-1/design | UTF-8宣言とstdout実バイトの対応が不明 | 保存HTMLの実バイトも検査する | 日本語の文字化けや出力失敗を見逃す | design/tasksへ一致の検査を追加。非UTF-8環境全般への新規対応を製品範囲には追加しない |
| adversarial | PRD FR-5/design | basenameの連続空白・改行・タブが折り畳まれる | 空白表示方針を定める | 異なる名前が同じ表示になる | designで空白保持＋折返し、tasksで検査を追加 |
| adversarial | PRD Glossary/FR-5 | 非Unicodeのファイル名 | surrogateescapeの表示/エラー契約を定める | 例外や不正文書 | 今回の確定要件へ新たな入力契約を加える提案として不採用。現行入力境界の不要な変更はしない |
| adversarial | design Decisions 3–4 | RTL/方向制御文字 | 双方向分離や変換方針を定める | 周辺表示の順序を誤解する | 表示変換の追加は本依頼の要件とせず不採用。既定の可読性条件は維持 |
| adversarial | PRD FR-4/FR-6/tasks | 通常幅・ブラウザが未固定 | UI設計/PLANで固定し版を記録 | 担当ごとの合否が割れる | 後続で固定する前提をdesign/tasksへ明記 |
| adversarial | spec長文/tasks | 長い語/名前の固定入力なし | 320 CSS pxで実際に折返すfixtureを固定 | 長文の不具合を見逃す | design/tasksへ追加 |
| adversarial | design/tasks 3.1 | 数値列が多桁になった幅を未検査 | 複数桁順位・大きい回数/総数を含める | 数値列が重なる | design/tasksへ追加 |
| adversarial | PRD FR-6/tasks 4.1 | headだけでは実行コードを識別できない | 作業状態と製品差分を保存 | 別コードの証拠になる | design/tasksへ追加。未コミット製品変更は対象headの証拠にしない |
| adversarial | Quality/design | 通信観測の範囲が未定義 | 文書を開く前から終了まで、失敗試行と因果関係を記録 | 背景通信の誤判定/漏れ | design/tasksへ追加 |
| edge-case | spec HTML-2 | topと種類数の比較が曖昧 | 比較主体を明記 | PRD/シナリオと矛盾 | adversarialと同じ本文修正で解消 |
| edge-case | design/PRD | 非Unicode basename | surrogateescapeの扱いを定める | 符号化例外 | adversarialと同じ理由で新規契約追加を不採用 |

## Editorial lenses
| Pass | Original Text | Revised Text | Changes / 対応 |
|---|---|---|---|
| structure | PRDの原文取得手続が目的より先 | 目的・読者を先に | 採用済み |
| structure | Briefの画面測定詳細 | PRDへ参照して圧縮 | 不採用。今回明示的に決めた画面判定をBriefにも残す価値を優先。PRDリンク追加済み |
| structure | tasksの長いcheckbox | 実施/確認/証拠の下位箇条書き | 不採用。各タスクに完了確認を含む公式の追跡行を維持し、詳細な分割はGSD PLANへ委ねる |
| prose | 全形式で同じ語の配列と回数 | 語と回数の組が同じ順序で出力 | 採用済み |
| prose | exit 1でstderrにエラー | いずれもstderrにエラーを出す | 採用済み |
| prose | 同じheadの実CLI | 検証対象headの実CLIでHTMLを生成 | 採用済み |
| prose | 実CLIの結果から独立して検査 | 実CLIで再生成し実装担当とは独立して検査 | 採用済み |
| prose | 横収まり・切取り祖先 | 横方向/切取り祖先内の収まり等を列挙 | 採用済み |
| prose | 旧語の昇順 | 旧仕様の語の昇順 | 採用済み |

## BMAD finalize
rubricの仮定タグ・原文参照・FR番号の名前空間を修正。fresh readerは重要不足なし。reconciliationの変更名接頭辞と人へ渡す未決の範囲はPRD Document purposeへ追記済み。未解決の人判断項目はない。
旧OpenSpecシナリオ名の変更は導入版strictで欠落扱いとなったため識別子を保存し、旧期待値を廃して初出順へ変更したことをTHENに明記した。厳格検証は再実行して合格を確認する。
