# PRD — Rubric review

## Verdict

**adequate — 非阻害の改善付きで合格。** 既存CLIの局所的な機能追加に必要な動作・境界・互換性変更・独立検証が確認可能な粒度で示され、実装計画を作るための製品判断に阻害的な空白は見当たらない。

## Three fixes that matter most

1. **low / Honest scope:** Assumptionsを公式guidanceの`[ASSUMPTION: ...]`表記にし、Users and journeys／Visionの閲覧者像に関する説明上の仮定だと一行で明示する。
2. **low / Usable downstream:** Document purposeのカードt_db216d64とAC1–AC6について、後続担当が原文へ到達できる保存先またはリンクを示す。取得できない場合は原文との独立照合が未実施である旨を残す。
3. **low / Usable downstream:** 本書のFR番号は「今回のPRD内」の識別子で、現行OpenSpecの同番号とは別の要求を指すと短く明記する。全件の再採番やtraceability matrixは不要。

## Findings by dimension

| Dimension | Rating | Severity / location / fix |
|---|---|---|
| Decision-ready | strong | 指摘なし。L29–36に目的・読者・利用フロー、L67–95に制約・変更境界・代替を退けた決定がある。全形式での初出順変更と移行フラグなしを明示し、実装・検証未実施を合格と混同していない。 |
| Earned | strong | 指摘なし。単独CLI向けcapability specとして架空のpersona／詳細journeyを省略し、事業数値や汎用NFRで埋めていない。FR-4／FR-6の詳細はmemlogとBriefにある明示的な画面判定・証拠要件に対応するため、本件では過剰な一般論として削らない。 |
| Testable | strong | 指摘なし。L45–65のFR-1–FR-6に正常・空・top・同数・正規化・特殊文字・エラー・独立ブラウザ検査がある。長文の収まりをRange、切取り祖先、重複、画像の複合で判定し、要素自身への縦包含を誤って追加していない。通常幅の具体値や検証コマンドは計画・実装側の選択であり、ここで製品の未決事項にはしない。 |
| Honest scope | adequate | **low**, L100–101 Assumptions。説明上の仮定と明示しているが、guidance-planning指定の仮定タグと影響節名がない。Assumptions節内で整える。Non-goals、Change boundary、未実施の明示は適切。 |
| Usable downstream | adequate | **low**, L29–30 Document purpose。カードIDとAC番号がリンクや保存先なしで、独立した読者が根拠を取り出せない。原文参照先を追加する。**low**, L45–65およびL29–30。現行OpenSpecにもFR-1等があり、本書のFR-1「静的HTML」と既存FR-1「実行方法とファイル読み込み」は別物。本書内の定義・参照は整合するが、後続仕様や試験の引用を曖昧にしないよう文書名で修飾する方針を一文追加する。 |

Critical: 0 / High: 0 / Medium: 0 / Low: 3。

## Template Done when checks

- **Every FR can be checked at its altitude:** strong。機能追加／epic相当の粒度で挙動と失敗状態を確認可能。具体的な試験コマンドや未作成の検証ファイルを要求文書に置く必要はない。
- **Every FR traces to a journey or need:** strong。FR-1／2／4は保存閲覧フロー、FR-3は全形式の意図的な順序変更、FR-5は安全性と既存動作の保護、FR-6は品質担当の独立確認に対応する。AC番号は付くが、原文の追跡性は上記lowの改善対象。
- **Every product-dependent journey beat has an FR:** strong。ファイル指定・HTML保存・ブラウザ閲覧をFR-1／2／4、既存入力挙動をFR-5、品質確認をFR-6で扱う。人物を創作しない縮小はテンプレートの単独CLI向け例外に適合する。
- **Non-goals and out-of-scope explicit:** strong。L72–76に非目標と同時提供範囲、L84–88に不変部分と破壊的期待値変更を明記。
- **Success metrics and counter-metrics:** strong。SM-1は条件別試験・独立確認・証拠追跡を成果とし、既存回帰・書式維持・外部通信0・CI差分なしを保護指標にする。利用規模の数値を創作しない。
- **Shape fits the product:** strong。capability specで構成し、不適用のAI／法規制／SLO／運用等を理由付きで省く。Consumer migrationはAPI contract、Storiesは重複生成しない扱いを明記する。
- **Nothing invented to fill a section / user remembers every decision:** adequate。読んだBriefとmemlogに主要決定が対応し、説明上の仮定も明示される。ただしカード原文未読のため、すべての決定が依頼者の明示承認に由来するかの独立確証まではできない。創作を確認したという指摘ではない。

## Review basis and limits

公式rubric-planning全文、guidance-planning、runの`.template.md`・`.memlog.md`・本文、同依頼Brief、initiative定義、現行`openspec/specs/wordfreq-cli/spec.md`を読んで評価した。小規模な既存CLI機能追加として判定し、コード動作やブラウザ合格を判定したものではない。カード原文、実行結果、実画像は今回のレビュー入力に含まれない。現行OpenSpecの同数時語順は語の昇順だが、PRDは明示的に置換すると述べるため、それ自体を矛盾として扱わない。本文・template・memlogは変更せず、検証コマンド実行・commit・Kanban操作は行っていない。
