# Brief — rubric walker 原本

入力: brief-wordfreq-exclude.md、.template.md、.memlog.md、../source-context.md、../open-questions.md。stakes=既存ローカルCLIの小さな変更要求。基準は公式rubric-planningとBrief done when。subagent不可の逐次fallback。

判定: 原文の要求と既存契約を落とさず、需要や効果を発明していない。利用者像とwhy nowは未確認なので、公開/実装判断用のfinalではなくpartialが妥当。

重要な対応: 未決の承認ゲートを先頭でも読めるようにする。背景推定を事実に昇格しない。HTML総数を勝手に変えない。

| Dimension | Rating | Finding / disposition |
| --- | --- | --- |
| Decision-ready | adequate | statusはdraftでOpen questionsに理由があるが、要約だけ読む人にも未承認ゲートを先頭で示す。修正対象。 |
| Earned | strong | 市場規模・人物・効果量なし。依頼のみが需要の根拠。 |
| Testable | adequate | Success criteriaは観測可能。実装と試験は未実施と明記。 |
| Honest scope | strong | 推定はAssumptionsへ分離、未決は共通一覧へ集約。 |
| Usable downstream | adequate | 指定templateと全必須節あり。PRDへ進めるが、製品未決は下流でもゲート。 |

Done when: executive summaryで何/誰/価値/現在の理由が分かる。ただし誰/理由の事業上の実証はないため、Assumptionsを依頼者へ戻すこと。The askとVisionの省略理由はScopeとmemlogにあり。
