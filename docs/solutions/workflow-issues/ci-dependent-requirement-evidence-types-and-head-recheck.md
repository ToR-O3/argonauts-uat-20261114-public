---
title: "CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する"
date: 2026-11-17
category: workflow-issues
module: "フェーズ検証・要求充足判定（REQ-07 CI pytest job）"
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "要求の充足条件が「CIでテストが成功すること」などCIの実行結果そのものになっている"
  - "CI設定ファイルの存在、過去のheadの人からの成功報告、ローカルテスト成功のうち複数ととのった時点で要求の判定をする"
  - "検証の判定や報告の直前にドキュメント等のcommitが積まれ、検証対象headが動く可能性がある"
tags: [ci-evidence, verification, requirements-gate, head-resolution, independent-verification]
---

# CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する

## Context

wordfreq CLI フェーズ1（カード r-5a3b8a3f、2026-11-17）で、REQ-07「CIでpytestが成功すること」の充足判定が揺れた。実装01-04ではリポジトリのActionsが0件（workflows total_count=0）を実測してPending維持は正しかったが、その後のやりとりで「CI通った」の主張が4種類の別々の証拠で行きかい、gapの解消判定を誤ると要求のCompleteが実体のないものになるリスクが実際に出た（元フェーズ検証 verdict=gaps）。教訓の背景はカードの実記録に基づく。

混同された4種の証拠（同じ「CI通った」に見えて、言える範囲がまったく違う）:

- (a) CI設定ファイルがGitに存在する — 「走る定義がある」だけで、走った事実も、今回のheadで走った事実も言えない
- (b) 過去のheadに対する人からのCI成功報告 — 報告されたheadについての事実であって、現在の検証対象headの証拠ではない
- (c) ローカルでのテスト成功 —REQ-01〜06・08のようなテスト内容の証拠にはなるが、CIの成立そのものの証拠ではない
- (d) 現在の検証対象headに対する検証者の独立したCI成功証跡の読み取り — これだけが要求充足を確定できる

もう一つの摩擦: 検証後〜報告前にドキュメントcommitが積もると検証対象headがずれる。実際の再フェーズ検証では検証対象head=30d9c17 のまま passed となり、検証記録のpush commitは 61421aa（検証対象headと報告commitは別物）だった。チーム運用（E.8.2）でも「確かめていないheadのマージ」が問題になっており、(d)の仕組みがあってもheadの照合をしないと穴になる。

## Guidance

1. **CI依存の要求の充足は (d) だけで確定する。** 検証者自らが、現在の検証対象headに対してCI実行基盤（例: GitHub Actions API）を読み、そのheadのrun/jobの成功（例: pytestステップ success、ランタイム、pass件数）を確認する。読み取りは他人の要約を介さず1回でも独立に行う。
2. **(a)(b)(c)がそろっても要求はPendingのまま維持する。** (a)はworkflowファイルの有無、(b)は人からの報告、(c)はローカル実行。いずれも欠点なくそろっても(d)にはならない。判定コメントに「そろった」ではなく不足の種類を書く。
3. **(b)は歴史的headの話として区別して記録する。** 「run 44017344659/44017344584 の43 passedは歴史的headについての人の報告で、最新headの独立品質証拠ではない」のように、headの帰属を明示して残す。捨てると後続がまた証拠混同する。
4. **判定・報告の直前に検証対象headを再解決して照合する。** 検証に合格したheadが、報告時点でまだ現在のhead（または要求された対象）と一致するかを、commit/pushの直前に再び解決して確認する。検証対象headと報告commitは別のものとして扱い、記録にも両方を別々に残す。
5. **(c)の価値は要求ごとに正しく配分する。** pytest 43件成功・実CLI 17Invocation はREQ-07の証拠にはならないが、REQ-01〜06・08の証拠としては併記して有効。証拠の「量」ではなく「対象」で判定する。

## Why This Matters

同じ「CI通った」主張に対してどの証拠種がどこまでを言えるかを混同すると、gapの解消判定を誤る。(a)だけを充足と誤認すると未実行のjobでCompleteになり、(b)だけを信用すると報告されたheadと現在のheadがずれたままCompleteになる。特にドキュメントcommitで検証対象headが検証後に動くのは通常の運用中で起きるため、「確かめていないheadのマージ」は例外ではなく、報告直前のhead再解決という手順でしか防げない。逆に(d)の手順とhead照合があれば、Botにworkflow権限がなく人がworkflowを追加する（今回の 5c9d8fa、CPython 3.12 の pytest job）ような人の介入を挟む流れでも、判定は検証者の独立読み取りに収束する。

## When to Apply

- 要求の充足条件がCIの実行結果そのものになっているとき（REQ-07型）
- 人からの「CI通りました」報告を受けて要求のPending解除を判定するとき
- 検証の合格記録を作ってからの報告・マージまでにcommitが積もりうる工程（ドキュメント同期、サマリ作成、アーカイブ）を含むとき
- CI成功の報告を他カード・他要求の証拠として転用するとき

## Examples

**このカードで実際に通った手順（カード r-5a3b8a3f の実記録、commit 5c9d8fa・30d9c17・61421aa はいずれも PR #2 経由で現在のmainから到達確認済み）:**

1. 実装01-04: Actions total_count=0 を実測 → OpenSpec task 3.3 には「CI job 作成は人の対応が必要」と記録し、REQ-07 は Pending 維持。「SUMMARY作成と requirements.ready-ids 判定はSUMMARY存在判定であってCI成功証跡ではない」と明示。
2. 元フェーズ検証: verdict=gaps、gap=「REQ-07: CI pytest job 無し（workflows total_count=0、.github 空）。対象headのCI成功証跡無し」。pytest 43件成功・実CLI 17Invocation は REQ-01〜06・08 の証拠として併記。
3. 人が workflow commit 5c9d8fa（CPython 3.12 の pytest job）を追加。現在のツリーの `.github/workflows/pytest.yml`（push argonauts/** と pull_request で python 3.12 + pytest）がこの人の対応の残骸。
4. 実装01-05: 「run 44017344659/44017344584 の43 passedは歴史的headについての人の報告で、最新headの独立品質証拠ではない」と明示して ci-handoff.md を作成。Builder run は ci_independently_verified=false・REQ-07 Pending のまま品質へ引き継ぎ。
5. 品質レビューrun (run 36): 最新head 30d9c17 に対してActions APIを1回だけ独立読み取り、push run 44021335880（job pytest、pytest step success、CPython 3.12.16、43/43 passed）と pull_request run 44021344458 の成功を確認 → ci_independently_verified=true、REQ-07 の「最新headのCI成功」証拠を充足。
6. 再フェーズ検証: 検証対象head=30d9c17 のまま passed。検証記録のpush commitは 61421aa（検証対象headと報告commitは別として記録）。REQ-07 Complete、ROADMAP完了。

**NGパターン→修正:**

```text
NG: 「workflow追加済み(5c9d8fa)＋人報告の43 passed＋ローカルpytest 43 passed → REQ-07 OK」
    → (a)+(b)+(c) のそろい踏みを充足と誤認。(b)のheadがどのheadかも不明なまま。
OK: 「REQ-07 Pending (a)(b)(c)あり、(d)無し。最新head X のActions runを独立読み取りして
     job pytest success を確認できるまで解除しない」
```

```text
NG: 検証合格head=30d9c17 → docs commitを積んで報告 → 報告は61421aa、照合なしで「検証済み」
OK: 報告直前に検証対象headを再解決 → 現在のheadが30d9c17か確認（ずれていれば(d)を再実行）
    → 記録には検証対象head=30d9c17、報告commit=61421aa を別々に残す
```

## Related

- `.planning/phases/01-wordfreq-cli/01-CI-GAP.md`・`01-VERIFICATION.md`（このカードのgap→充足の記録）
- `.planning/argonauts/t_0d6af354/ci-handoff.md`（歴史的head報告の区別を明示した引き継ぎ）
- `.github/workflows/pytest.yml`（人の対応で追加されたREQ-07対象のCI job）
