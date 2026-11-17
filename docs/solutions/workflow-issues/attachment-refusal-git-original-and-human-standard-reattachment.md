---
title: "検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す"
date: 2026-11-17
category: workflow-issues
module: "検証証拠の受け渡し（Argonauts カード添付・検証成果物の原本）"
problem_type: workflow_issue
component: development_workflow
severity: high
resolution_type: workflow_improvement
applies_when:
  - "検証・審査の証拠をカードの添付で依頼者・審査者に渡す必要があり、添付経路がフックやガードに拒否されたとき"
  - "秘密・個人情報の制限でカード本文・metadata に証拠本文を置けず、添付が事実上唯一の受け渡し経路になるとき"
  - "ダッシュボードや UI に表示される添付名が原本名と違う（連番付与など）ため、同一性をどう示すか判断するとき"
  - "metadata の証拠パスに転記誤りが発覚し、後の run が迷う可能性があるとき"
tags: [evidence-handoff, attachment-refusal, git-original, original-identity, sha256-verification, hook-policy, record-distinction]
---

# 検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す

## Context

wordfreq CLI フェーズ1（カード r-5a3b8a3f、2026-11-17）の元フェーズ検証（t_3dc4a405）で、検証結果の gaps 記録（VERIFICATION.md・検証スクリプト・cli-evidence.md）を push 済みなのに、標準添付ツールへのフック拒否が起きた（カード実録: 「フックが添付を拒否: verification document must not embed secret values」）。背景に「秘密・個人情報はカード本文・metadata に置けない（記録が残り続ける）」という運用ルールがあり、その結果として添付が証拠の唯一の受け渡し経路になりやすい。添付が塞がれたとき、Bot は迂回（圧縮・リネーム・URL 化でのこすり付け）や棚上げをせず、「原本は push 済みの Git path にあり、添付は人が標準手段で行う」とコメントに残した（カード実録: 完了コメント・添付不足コメント）。このとき metadata の `cli_evidence_path` を誤った階層に転記するミスも重ね、自らのコメントで「正しい階層は `.planning/argonauts/<カードID>/cli-evidence.md` で push 済み」と訂正した。判定キー（verdict / head_sha / gaps）は元から無傷だった。

受入（t_5154b0f9、verdict=approved）では、元の添付拒否は人が標準添付 18・19 を提供して解消済みと記録し、「元の拒否と今回解消は区別する」を明示した。同一性は sha256sum で標準添付保存ファイルと worktree 原本の一致を検証して確認している。ダッシュボード表示名には標準の連番が付くが、中身が原本なら同一性は成立する。検証対象 head `30d9c17` と報告 push commit `61421aa`（いずれも PR #2 経由で現在の main から到達確認済み）の区別も、証拠の所在を特定する際に効いた。

リポジトリ内の実証拠: `.planning/argonauts/r-5a3b8a3f-fix-1.md:29`（「元のVERIFICATIONとcli証拠の添付はフック拒否のためGitのみ。cli原本は .planning/argonauts/t_3dc4a405/cli-evidence.md（.planning/archive-noneは誤記）」）、`.planning/argonauts/t_0d6af354/ci-handoff.md:57`（「do not bypass hooks… record attachment success (IDs/files) or the exact current inability/refusal reason… excluding secrets, credentials and raw PII」）、`.planning/phases/01-wordfreq-cli/01-VALIDATION.md:78`（「states attachment success or exact refusal reason; never bypasses hooks」）。添付イベントそのものはリポジトリに現れないため、上記の日付・run への言及はカード実録として引用している。

## Guidance

1. **添付がフック・ガードに拒否されたら迂回しない。** 圧縮・リネーム・形式変換・URL 化でガードの目を誤魔化さない。拒否された内容は拒否されるべき理由（秘密・個人情報の埋め込み等）がある合図であり、こすり付けはガードの意図を空にする。
2. **原本は Git 管理下の作業 branch に push して参照パスを残す。** 添付が塞がれても証拠を失わない。原本の所在（リポジトリ内パス）をコメント・metadata に残し、後続 run が Git だけで全証拠に辿れる状態を保つ。
3. **拒否理由は具体的に人へ渡す。** 「添付失敗」では人は動けない。「検証文書が秘密値を埋め込んでいるためフックが拒否」のように、人が対処できる粒度で書く。人はその具体理由を受けて、標準手段（人の UI からの添付）で原本を添付し直せる。Bot にはできない操作であり、ここが人の役割の境界になる。
4. **原本同一性は hash とバイト列で示す。** 添付コピー（ダッシュボード保存ファイル）と worktree 原本の sha256 が一致すれば同一性は成立する。表示名に標準の連番が付くなど、名前の差異は同一性を壊さない。判定は名前の類似ではなく hash 一致で行う。
5. **拒否時点の記録と解消時点の記録を区別して残す。** 「拒否された」という古い記録だけを消さず、「人が標準添付 18・19 を提供して解消済み」という後続記録を別に立てる。後の run が「未添付」と誤読しないためで、判定キー（verdict・head_sha・gaps）が元から無傷であることも添えて、どこが無傷で何が動いたかを明確にする。
6. **metadata の転記誤りは自分でコメント訂正する。** パス名の誤り（今回の `.planning/archive-none` 誤記→正しい階層 `.planning/argonauts/<カードID>/cli-evidence.md`）は、発見者が自らのコメントで正しい階層を明記して修正する。後の run が誤パスを探して迷うのを防ぐ。訂正は元記録の書き換えではなく追記の訂正コメントで行い、何が誤りだったかを残す。

## Why This Matters

秘密・個人情報をカード本文・metadata に置けないルールがある限り、証拠本文を審査者に渡す実質唯一の経路は添付であり、添付経路が塞がれたときの扱いがそのまま品質受け渡しボトルネックになる。迂回（リネーム・圧縮での再試行）を許すと、秘密ガードは名前と形式を変えるだけのイタチごっこになり、ガードが守っていたものが何か分からなくなる。逆に「原本は Git・添付は人の標準手段」と境界を固定すると、Bot は権限の外で無理をせず、人は具体理由があれば 1 操作で解消できる。

区別記録がない場合、後の run は「添付拒否」だけを読んで未添付と誤判し、解消済みの受け渡しをもう一度やり直すか、判定を保留し続ける。検証対象 head と報告 push commit を区別しておくのと同じ原則（証拠の主張はその帰属先に対してのみ成立つ）が、添付イベントにもそのまま適用される: 「拒否された」は拒否時点の fact、「解消済み」は解消時点の fact で、1 行に圧縮するとどちらか一方で必ず嘘になる。

## When to Apply

- カード・ワークフローシステムの添付に検証成果物を載せる必要があり、標準添付ツールがフックで拒否したとき
- 審査者が「添付が見当たらない／どのファイルが原本か分からない」と指摘したとき
- 添付のコピーとリポジトリ原本のどちらが正か判断する必要があるとき（判定は sha256 一致）
- 自分が書いた metadata の参照パスに誤りがあると後から分かったとき
- 過去の拒否・失敗記録を持つカードの受け渡しを、時間を置かずに続ける/run させるとき

## Examples

```text
NG: 添付拒否 → ファイル名を evidence.txt に変えて再試行 → 通ったので秘密はそのままで受理された
    → ガードの意図（秘密値の非埋め込み）を形式変更で無効化。次以降のrunはガードが効いていると誤信する。
OK: 添付拒否 → 「verification document must not embed secret values とフックが拒否。
    原本は push 済み: .planning/argonauts/<カードID>/cli-evidence.md。添付は人の標準手段で」とコメントし、人は待たせず返す
```

```text
NG: 「元検証で添付がフックに拒否された」だけを残してクローズ → 後続 run が未添付と誤読し差し戻し
OK: 拒否記録（元検証: フック拒否・Git のみ）と解消記録（受入: 人が標準添付 18・19 を提供、
    sha256sum で保存ファイルと worktree 原本の一致確認済み、判定キーは無傷）を別々に残す
```

```bash
# 原本同一性の確認手順（名前の連番は無視して中身を見る）
sha256sum "<標準添付の保存ファイル>" "<worktree 内の原本（例: .planning/argonauts/<カードID>/cli-evidence.md)>"
# ハッシュ一致で同一性成立。表示名の連番付与は同一性を壊さない
```

## Related

- [docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md](../workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md) — 同じカード r-5a3b8a3f からの別教訓。あちらは「どの証拠種が要求充足を言えるか」と検証対象 head の区別、本記事は「その証拠の原本を審査者へどう届けるか」の経路と記録の扱い。
- `.planning/argonauts/r-5a3b8a3f-fix-1.md` — フック拒否で Git のみとなった経緯と cli-evidence 正しい階層の記録
- `.planning/argonauts/t_0d6af354/ci-handoff.md` — 「添付成功または具体的な不能理由を記録し、hooks を迂回しない」を成果物出力として契約化した箇所
- `.planning/phases/01-wordfreq-cli/01-VALIDATION.md`・`01-05-PLAN.md`・`01-05-SUMMARY.md` — 添付可否・拒否理由の記録を必須出力とした検証/計画/サマリ
