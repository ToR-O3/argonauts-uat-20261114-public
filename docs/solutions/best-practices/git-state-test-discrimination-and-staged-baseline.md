---
title: "状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する"
date: 2026-11-17
category: best-practices
module: "wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）"
problem_type: best_practice
component: testing_framework
severity: medium
root_cause: test_isolation
resolution_type: test_fix
applies_when:
  - "git status など作業ツリー・リポジトリ状態の before/after 一致を主張する回帰試験を作り、または品質レビューで『その試験は失敗を検出できるか』を問われる"
  - "試験が一時リポジトリ（git init した scratch のリポジトリ）を作り、その状態を比較基準にする"
  - "『CLIはリポジトリに書き込まない』『生成物が作業ツリーを汚さない』類の読み取り専用性の主張を試験で固定する"
  - "試験の失敗が本物の検出なのか、試験設計側の欠陥による偽陽性なのかが判別できない状態で request_changes が来た"
tags: [git-status, mutation-injection, test-discrimination, staged-baseline, untracked-files, false-positive, read-only-claim]
---

# 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する

## Context

wordfreq CLI フェーズ1（カード r-5a3b8a3f、2026-11-17）の実装01-03（t_4b01f783）では、`python -m wordfreq` の実行が Git 作業ツリーを変えないことを `git status --porcelain --untracked-files=all` の before/after 一致で主張する回帰試験を PLAN に含んだ。初版は品質レビューから request_changes を受け、原因は2点だった（カード実記録）。

1. **偽陽性**: 状態比較の基底リポジトリに未追跡ファイルが残ったままスナップショットを取っており、変異を注入しなくても差分が出て失敗していた。失敗の原因が試験設計側にあり、本物の検出と混同される。
2. **検出範囲の未証明**: 注入した変異が1種類（既存ファイル変更）だけで、無視規則の欠落による想定外の未追跡ファイル（実行が生成する `wordfreq/__pycache__/*.pyc`）を検出できることが示せていなかった。

やり直し後の記録（`.planning/phases/01-wordfreq-cli/01-03-SUMMARY.md` の "Review rework: WR-02"・"Review rework: tracked-baseline discrimination"、いずれも現在の main から到達可能な PR #2 経由）が示したのは、同じ状態比較試験が2回、別々の欠陥で判別力を欠いていた事実である。

- WR-02: 初版の合格は継承された `PYTHONDONTWRITEBYTECODE=1` や先行試験で温まったキャッシュに依存しており、既定環境の git クリーン性は立証されていなかった。修正は `.gitignore` に `__pycache__` ディレクトリ・`*.pyc`・`.pytest_cache` ディレクトリを無視する3規則を追加する最小修正（commit `4fa6d98`、PR #2 経由で現 head から到達確認済み）。
- tracked-baseline discrimination: WR-02 修正後もコピーしたソースは未追跡のままだった。未追跡ファイルは `git status` がパス名だけを報告するため内容変更が不可視で、レビューアの注入変異（`__main__.py` に兄弟 `__init__.py` へ `# tampered\n` を追記するコードを先頭に足す）に対し、修正前の試験は **1 passed・exit 0 の偽合格**をした（01-03-SUMMARY.md:139-141）。`git init` 直後の `git add -A` を最初のスナップショット前に足したところ、同じ変異で **1 failed・exit 1、失敗箇所は `assert after == before`（status が `AM` に変化）** となり、変更の検出を証明した（同:142-143）。

現行ツリーの固定済み試験は `tests/test_cli.py:152-180` にあり、cold copy（`__pycache__`/`*.pyc` を除外した copytree、test_cli.py:156-157）、`.gitignore` の明示的コピー（test_cli.py:158-159）、`git init` → `git add -A`（test_cli.py:160-162）、subprocess env からの `PYTHONDONTWRITEBYTECODE` 除去（test_cli.py:168-169）、`--untracked-files=all` の before/after 比較（test_cli.py:170,175,180）をすべて含んでいる。

## Guidance

1. **状態検証試験は『パスすること』だけでは検証にならない。判別力を変異注入で示す。** 使い捨ての scratch コピーで意図的な失敗を注入し、実際の試験をそのまま実行して、期待どおりの主張で失敗すること（失敗箇所が特定のアサーションであることまで）を確認する。scratch コピーでのみ実行し、作業ツリーと product code は一瞬たりとも変異状態で持たせない。
2. **検出すべき失敗の種ごとに、別々の scratch コピーで別々に注入する。** 本ツリーで確定した最低2種は:
   - (a) 追跡内容の変更: CLI 実行がリポジトリ内の既存ファイルを書き換える変異 → status が `AM` になり `assert after == before` で失敗すること。
   - (b) 無視規則の欠落による想定外の未追跡ファイル: 実行が生成する `.pyc` 相当を無視できなくなる状態（`.gitignore` を置かない scratch コピー）→ 新規 `wordfreq/__pycache__/*.pyc` パスが status 差分になり同じアサーションで失敗すること。
   片方の注入だけでは、もう一方の検出は証明できない（01-03 が実際に失敗した点）。
3. **比較基底は `git init` 直後の `git add -A` 後に作る。** 未追跡のままスナップショットした基底は、(i) 未追跡ファイルの内容変更が `git status` に不可視で偽合格し、(ii) 注入なしでも生成物が差分に出て偽陽性する、という二方向の誤作動を起こす。ステージ済み同一内容から検証を始めることで、差分は注入された変異からのみに帰属する。コミットも Git identity も不要（ステージだけで `AM` 遷移は機能する）。
4. **基底リポジトリの外側からの汚染も断つ。** ソースは `__pycache__`/`*.pyc` を除外した cold copy で置き、CLI subprocess の env からは `PYTHONDONTWRITEBYTECODE` を明示的に除去する。継承環境や先行試験で温まったキャッシュに依存した合格は、既定環境の主張にならない。
5. **修正側のガードは条件付きコピーにする。** `.gitignore` は「存在すればコピー」する（test_cli.py:158-159）。これにより (b) の注入プロウブは「ファイルが存在しない設定エラー」ではなく無視規則の有無という状態検出を行使する（01-03-SUMMARY.md:144 の copy guard 維持の理由）。

## Why This Matters

状態比較試験の失敗は「本物の検出」と「試験設計側の欠陥（偽陽性）」が見た目が同じで、基底が汚れている限り両者を区別できない。偽陽性を抱えたまま試験を回すと、原因調査が request_changes のコストとしてレビュー往復に転嫁される（本カードで実際に出た調査コスト）。逆に偽合格のほうがたちが悪い: 未追跡基底の試験は既存ファイルを書き換えられても `1 passed` を返すため、「読み取り専用である」という主張が根拠なしに合格ラインを通過してしまう。判別力は種ごとに別々証明されるもので、1種の注入成功から他種の検出を推論できないのは、Git の status 表示が未追跡ファイルについてパス名しか持たないという挙動そのものに由来する。

## When to Apply

- `git status`、ハッシュツリー、ディレクトリ listings など、状態の before/after 一致を主張する回帰試験を新設・改修するとき。
- 試験が `git init` した一時リポジトリを fixtures として作り、そこに product code をコピーして実行するとき。
- 品質レビューから「その試験は何を検出できるのか」「注入なしでも失敗しないか」と問われたとき。
- 実行時にキャッシュ・生成物を書く可能性がある処理（Python の bytecode 生成など）の読み取り専用性を固定するとき。

## Examples

基底固定の実装（本ツリー、`tests/test_cli.py:156-170` より要点）:

```python
shutil.copytree(ROOT / "wordfreq", repo / "wordfreq",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
if (ROOT / ".gitignore").exists():          # 条件付きコピーが無視規則の検出を行使させる
    shutil.copy2(ROOT / ".gitignore", repo / ".gitignore")
subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
# Track the baseline so content changes show up, not just new paths.
subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
```

判別力の実測記録（scratch コピー、`.planning/phases/01-wordfreq-cli/01-03-SUMMARY.md:141-144`）:

```text
(a) 既存ファイル変更の変異（__main__.py が __init__.py へ "# tampered\n" 追記）
    基底=未追跡のまま: 1 passed, exit 0   ← 偽合格。内容変更が status に不可視
    基底=git add -A 後: 1 failed, exit 1  ← assert after == before（status が AM）

(b) 無視規則の欠落（実アプリは無変異、.gitignore をコピーしない scratch）
    基底=git add -A 後: 1 failed, exit 1  ← 新規 wordfreq/__pycache__/*.pyc が status 差分
```

```text
NG: 注入なしで 1 回流して passed →「読み取り専用を立証」
    → 未追跡基底なら既存ファイル書き換えにも気づかず、キャッシュ生成でも元から落ちる。
OK: 検出したい失敗の種ごとに scratch を作り、種ごとに期待アサーションの失敗を確認してから
    本ツリーで 1 passed を並べて記録する（作業ツリーは変異状態を一切通さない）。
```

## Related

- [docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md](../best-practices/input-boundary-verification-and-deterministic-ordering.md) — 同じカード r-5a3b8a3f からの別教訓。「単一シードの再実行一致は決定論の証明にならない」と「単一実行の合格は判別力の証明にならない」は同一原則（単一の成功実行は証明にならない）の別適用で、あちらが引用する `tests/test_cli.py:152` の読み取り専用アサーションの設計教訓が本記事。
- `.planning/phases/01-wordfreq-cli/01-03-SUMMARY.md` — WR-02 と tracked-baseline discrimination の rework 全記録（注入手順・before/after の pass/fail・commit `4fa6d98`）。
- `tests/test_cli.py:152-180` — 教訓が実装された試験本体。
