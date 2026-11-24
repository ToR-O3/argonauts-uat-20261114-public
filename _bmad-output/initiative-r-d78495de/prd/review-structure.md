# Editorial structure

> 旧版の履歴。2026-11-25T06:53+09:00 の判断前の本文・計数。実行手順と証拠の保持提案は失効し、現行評価ではない。現行セルフチェックは review-update.md。

本書は Builder／quality の実施と PM の証拠読取りを支える PRD。Strategic/Context (Pyramid) を適用。テンプレート必須節を残し、仕様と実施手順を分離する。

初回 word_metrics 全体3418、目次149、frontmatter26、Assumptions83。Stories193、Glossary173、Developer experience676、Decisions305。同ツールの日本語分割単位で、本文は3000語のinitiative目安を超えるため重複を削る。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Stories — 193語 | CONDENSE: FR／RULE参照の受入条件に縮小 | 同じ条件の反復を避ける。削減は最終metricsで確認。 |
| structure | Glossary — 173語 | CONDENSE: 用語定義のみ維持 | 本文の説明と重複する修飾を削る。 |
| structure | Developer experience — 676語 | PRESERVE | 依頼が要求する再現と証拠を支えるため保持。 |

2件の編集提案を採用。最終 word_metrics は全体3237、本文2891（frontmatter・目次・Assumptionsを除外）。全体は181語・約5.30%削減し、本文はinitiative目安3000語以内。Glossary115語、Stories70語となった。wc -w の空白区切り総数は520で、本文はそれを下回る。受入条件は参照先に残り、理解上の犠牲なし。
