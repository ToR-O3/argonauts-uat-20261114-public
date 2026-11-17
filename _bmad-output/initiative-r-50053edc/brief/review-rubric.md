# Brief — Rubric review

## Verdict

**adequate — 非阻害の改善付きで合格。** 小規模な既存CLIへの機能追加を判断するBriefとして、追加価値、意図した互換性変更、除外範囲、確認条件が揃っており、需要や市場価値を創作していない。

## Three fixes that matter most

1. **low / Usable downstream:** Success criteriaのAC1–AC6の参照先を、同依頼PRDの相対リンクと対応するFRで示す。要求自体をBriefへ再掲して長くしない。
2. **low / Honest scope:** Assumptionsの説明上の仮定を、公式guidanceの`[ASSUMPTION: ...]`表記にし、対象がWho it serves／閲覧場面であることを一行で示す。
3. **low / Decision-ready:** Executive summaryに「既存CLI利用者向け」「今回の依頼に応える局所追加」を短く明記し、本文を読まなくても対象と今回取り組む理由が分かるようにする。架空の緊急性や期限は足さない。

## Findings by dimension

| Dimension | Rating | Severity / location / fix |
|---|---|---|
| Decision-ready | adequate | **low**, 本文L21–24 Executive summary。機能・保存閲覧の流れ・順序の変更は明確だが、対象者はCLI利用者と推測する形になり、why nowは依頼IDに留まる。対象と依頼起点を一文内で明示する。追加の市場調査や投資判断は不要。 |
| Earned | strong | 指摘なし。L26–36で需要の規模・固有人物像・新規性を創作せず、text直接閲覧／JSON整形という代替と局所的な利点を述べる。一般的なNFRや長期Visionで水増ししていない。 |
| Testable | strong | 指摘なし。L38–43は表・総数・初出順・top境界・画面幾何・画像・安全性・独立確認に落ちている。L30の「目指す」はSuccess criteriaの具体条件で補われ、Briefの段階で実装手段を増やす必要はない。 |
| Honest scope | adequate | **low**, L48–49 Assumptions。仮定であることは明示され、memlogの判断とも整合するが、公式guidance-planningの唯一の仮定タグを使っていない。Assumptions節に対象節名付きのタグとして整える。L45–46の除外、The ask／Visionを省いた理由は適切。 |
| Usable downstream | adequate | **low**, L38–42 Success criteria。AC識別子の実体・参照先がこの文書だけでは辿れない。`../prd/prd-wordfreq-html.md`へのリンクと対応FRを添える。小規模変更に対して長さ・用語・技術詳細の量は妥当。 |

Critical: 0 / High: 0 / Medium: 0 / Low: 3。

## Template Done when checks

- **全体:** adequate。Executive summaryだけで追加物と閲覧価値は分かる。対象とwhy nowの明示は上記lowの改善であり、事業上の緊急性を創作する必要はない。
- **Executive summary:** strong。本文にない製品主張はない。二段落で独立して読める。
- **Problem:** adequate。依頼者の要望と現行出力の整形負担を述べ、具体人物・金銭コストの証拠がないことを隠していない。本件の小規模変更で架空の人物や定量コストは要求しない。
- **Solution:** strong。静的HTML、文脈情報、閲覧性がProblemの整形負担に対応する。
- **What makes it different:** strong。既存text／JSONの代替に対して、保存HTMLだけで閲覧できる利点を限定して述べる。
- **Who it serves:** adequate。既存CLI利用者という対象は特定可能で、固有人物の未提供はAssumptionsへ明示されている。
- **Success criteria:** strong。結果・変更境界・品質の合否を確認できる。AC参照の追跡性だけ改善を勧める。
- **Scope:** strong。含む／含めないものと、同数時の意図的変更が明確。
- **The ask / Vision:** 適用外・省略理由確認済み。資金提案でなく、長期構想も本変更の範囲外。

## Review basis and limits

公式rubric-planning全文、guidance-planning、runの`.template.md`・`.memlog.md`・本文、同依頼PRD、initiative定義、現行`openspec/specs/wordfreq-cli/spec.md`を読んで評価した。内部向けの小規模な既存CLI機能追加として判定し、実装・ブラウザ・未作成検証コマンドは実行していない。カードt_db216d64／t_c3d584a1の原文は今回のレビュー入力に含まれないため、カードの全決定との一致は独立に確証できない。本文・memlog・既存仕様間に阻害矛盾は見つからず、同数時順序の差分は明示された変更として扱った。本文・template・memlogは変更していない。
