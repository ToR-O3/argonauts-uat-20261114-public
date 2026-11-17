# 構成・文章 polish

この文書は、Johnと仕様承認PMが小さなCLI拡張のPRDを作り、未決をまとめて確認するためにある。モデルはStrategic/Context (Pyramid)。既定style guideはMicrosoft Writing Style Guide、対象読者は人。日本語の簡潔な事実記述・CLI識別子・ACと質問の安定IDを維持する。

公式word_metrics: 全体2897、Executive summary 280、Success criteria 681、Scope 455（CJKを含むスクリプト独自集計）。wc -wは全体210で、日本語の分量を十分表さない。表以下は削減数を捏造せず、実測値がある節を対象にする。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Success criteria（681） | PRESERVE | 詳細に見えるが、依頼が明示したACであり切ると引継ぎ品質を損なう。削減0。 |
| structure | §Scope（455）の末尾 | CONDENSE: 範囲外の理由は日本語1文へ。保存方法のシェル注意は削除。 | Briefでの説明量を減らす。保存上の注意は今回の要求ではないため、仕様を増やさない。削減量は編集後の同CLI再測定で報告。 |
| prose | The askはスポンサー・予算へのpitchでないため対象外。Visionは長期構想が依頼になく、推測で範囲を広げないため省略する。 | スポンサーへの予算依頼と長期構想は今回の対象でないため、The ask・Visionは省略する。 | テンプレート省略理由を保ち、日本語で一読できる形にする。 |

構成パスの後に文章パスを実施し、削除箇所へ文章修正を重ねていない。指摘は上記のみ。採用対象はCONDENSEとprose、PRESERVEは維持判断。その他の重複は、要約・AC・未決の参照関係に必要なので残す。

編集後の公式再測定は全体2829、Scope 387、frontmatter・TOC・Assumptionsを除く本文2485。全体の削減は68（2.35%、jqで算出）。テンプレートは1〜2ページを求めるが、明示されたACを省略せず保持しており、通常印刷で2ページに収まることは未確認。さらなる短縮はACの具体例・安全性/回帰条件をPRDへ移す必要があるため、人不在の本実行では行わない。これは分量に関する残余制約である。
