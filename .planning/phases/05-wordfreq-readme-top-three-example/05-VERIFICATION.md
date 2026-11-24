---
phase: 05-wordfreq-readme-top-three-example
verified: 2026-11-24T05:48:38Z
status: gaps_found
score: 2/3 must-haves verified
covered_files: [
    ".planning/argonauts/t_40ba151e/openspec-verify.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/05-01-PLAN.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/05-01-SUMMARY.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/05-CONTEXT.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/05-SECURITY.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/05-VALIDATION.md",
    ".planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py",
    "README.md",
    "openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md",
    "openspec/changes/r-864b299c-readme-top-three/tasks.md",
    "wordfreq/__main__.py",
    "wordfreq/aggregator.py",
    "wordfreq/formatters.py",
    "wordfreq/sources.py"
  ]
covered_digest: "v4:sha256:c32eaabd96dde02e9f48f9550765f7973d1d850c5ded6eb1b4a095b034bb5464"
behavior_unverified: 0
overrides_applied: 0
decision_coverage: {honored: 3, total: 3, not_honored: []}
gaps:
  - truth: "必須報告を含む最新の依頼ツリーでも、品質が PLAN 05-01 の同じコマンドで製品差分と掲載 CLI を独立に再検証し、合格の平文証拠を PM に渡せる。"
    status: failed
    reason: "05-SECURITY.md と openspec-verify.md を置くと、既存の検証が両方を範囲外と判定して終了1となり、実 CLI に到達しない。未追跡で verifier が再現し、ステージ済みでも親の再現で失敗した。"
    artifacts:
      - path: ".planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py"
        issue: "19–43行の完全一致の許容リストに必須原本2件がなく、118–138行で追跡差分・未追跡ファイルを製品範囲違反と誤判定する。"
    missing:
      - "このフェーズの必須原本 .planning/phases/05-wordfreq-readme-top-three-example/05-SECURITY.md と .planning/argonauts/t_40ba151e/openspec-verify.md を限定的に許容する。.planning/ 全体や既存フィクスチャを除外しない。"
      - "必須原本が未追跡の場合と追跡差分に含まれる場合の両方で、同じ検証コマンドが終了0、配置・差分 PASS、実 CLI 終了0、JSON 配列が順に alpha:4、beta:3、gamma:2 の3件となる平文証拠を残す。"
      - "無関係な追跡変更・未追跡ファイル（既存 .planning/ フィクスチャを含む）は従来どおり非0で拒否することを確認する。"
---

# Phase 5: wordfreq README top three example — 検証報告

**Phase Goal:** README の「wordfreq の実行」の既存ブロックで、現行CLIで上位3語をJSON表示する実行例を利用できる。

**Verified:** 2026-11-24T05:48:38Z

**Status:** `gaps_found`

**Re-verification:** いいえ — 初回検証。

**対象:** `start_sha`・クリーンな実装 HEAD ともに `14e6df0700bb19a9e54a0d1b32e0f16f6eced634`。比較基点 `5528aa47cca27a93a6732e914710f2772118a572` はその祖先。報告を置いた状態は同じ HEAD 上の作業ツリーであり、報告コミットの結果ではない。

## Goal Achievement — 目標の達成

利用者向けの目標は達成。未達は製品機能ではなく、必須報告と共存するツリーで PLAN の差分・実行検証を再現できること。

### Observable Truths — 観測可能な条件

| # | 条件 | 判定 | 根拠 |
|---|---|---|---|
| 1 | `--top 2` のJSON例直後に `python -m wordfreq input.txt --top 3 --format json` を1行だけ追加し、それ以外の製品差分がない。 | ✓ VERIFIED | `README.md:5–16` と比較基点からの全差分を照合。README は `+1/-0`、既存フェンス・例・説明、CLI、既存試験、依存、設定、CI に製品差分なし。OpenSpec の `tasks.md` は 1.1 のチェックだけ。実際の製品差分と検証ファイルによる誤判定は別。 |
| 2 | 掲載した行を一時UTF-8入力で実行すると終了コード0、JSON配列が順に `alpha:4`、`beta:3`、`gamma:2` の3件ちょうどとなる。 | ✓ VERIFIED | 親の品質担当がクリーンな実装 HEAD で既存の検証ファイルを独立実行。配置と範囲 PASS、検証と実 CLI ともに終了0、stderr 空。下記に実出力を記載。 |
| 3 | Builder の掲載前 RED・掲載後 GREEN と、品質が同じ検証を最新の依頼ツリーで独立再実行し PM に渡せる平文証拠が揃う。 | ✗ FAILED — BLOCKER | Builder の RED/GREEN は `05-01-SUMMARY.md:57–68` に記録されており、品質によるクリーン HEAD の再実行も確認した。一方で必須報告を含むツリーは終了1で、PLAN の差分検証が実 CLI に到達しない。合格の証拠は報告込みツリーに流用できない。 |

**Score:** 2/3 条件を検証済み（`PRESENT_BEHAVIOR_UNVERIFIED`: 0）。公式 `roadmap.get-phase 5` は Phase 5 を解決したが `success_criteria` は空配列だったため、`ROADMAP.md:128–130` の2条件を原文から採用した。PLAN frontmatter の配置・製品差分を条件1、実 CLI を条件2に統合し、独立検証の条件を条件3に加えた。前回報告・override・prohibition・`human-check` なし。

### Required Artifacts — 必須成果物

| 成果物 | 期待 | 判定 | 詳細 |
|---|---|---|---|
| `README.md` | 正確な掲載行 | ✓ VERIFIED | 存在・実体・利用経路あり。9–16行の既存 `sh` ブロックの13行目で、そのまま実 CLI を使える。 |
| `verify_readme_top_three.py` | 配置・差分・実 CLI の自動検証 | ✓ 実体と接続あり／差分判定にギャップ | 公式 `verify.artifacts` は2/2、終了0。`main()` は配置、Git 差分、CLI 実行、JSON 検査を実装している。必須報告との共存だけが差分段階で失敗する。 |

### Key Link Verification — 接続

| From | To | Via | 判定 | 根拠 |
|---|---|---|---|---|
| `verify_readme_top_three.py` | `README.md` | 掲載行の抽出と比較基点照合 | ✓ WIRED | 62–83、193–208行。公式 `verify.key-links` でも参照を検出。 |
| `verify_readme_top_three.py` | `wordfreq/__main__.py` | 掲載 argv で `python -m wordfreq` を起動 | ✓ WIRED（ソースと実 CLI） | 公式 `verify.key-links` は終了1、1/2。`Target not referenced in source` はファイル名の直接参照がないため。146–166、210–213行のモジュール起動、`wordfreq/__main__.py:57–58` の入口、クリーン HEAD の実出力で結線を確認。報告込みではその手前の範囲チェックで停止する。 |

### Data-Flow Trace (Level 4) — データの流れ

| 出力 | 変数 | 実データ源 | 判定 |
|---|---|---|---|
| CLI stdout の JSON | `pairs` → `output` | 一時 UTF-8 ファイル → `FileSource`（`wordfreq/sources.py:13–22`）→ トークン頻度集計・top（`wordfreq/__main__.py:29–38`、`wordfreq/aggregator.py:6–17`）→ `format_json`（`wordfreq/formatters.py:11–14`）→ stdout（`wordfreq/__main__.py:45–54`）。期待値定数は検証側の比較専用。 | ✓ FLOWING（クリーンな実装 HEAD） |

### Behavioral Spot-Checks — 実行確認

PLAN 指定コマンド: `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`。

| 条件 | 実行主体・対象 | 実測 | 判定 |
|---|---|---|---|
| D-01〜D-03 | 親の品質担当、クリーンな実装 HEAD | 検証終了0、`placement and scope: PASS`、CLI 終了0、stderr 空。掲載行の `input.txt` だけを作業ツリー外の一時ファイルへ置換。 | ✓ PASS |
| 必須報告が未追跡で共存 | verifier、同じ HEAD 上の現作業ツリー（`timeout 10s` で同じ検証ファイルを起動） | 終了1、`CLI: not run`。`out-of-scope untracked paths` に `.planning/argonauts/t_40ba151e/openspec-verify.md` と `.planning/phases/05-wordfreq-readme-top-three-example/05-SECURITY.md`。 | ✗ FAIL |
| 必須報告がステージ済みで共存 | 親の品質担当、同じ HEAD 上で両報告をステージして再現 | 終了1、`CLI: not run`、`out-of-scope change: '.planning/argonauts/t_40ba151e/openspec-verify.md' (b'A')`。最初の違反で停止。ステージは復元済み。 | ✗ FAIL |

クリーン実行の入力: `delta gamma beta alpha beta gamma alpha beta alpha alpha`。stdout は次の JSON と末尾改行。

```json
[{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]
```

### Probe Execution — PLAN の実ファイル

| Probe | コマンド | 結果 | 判定 |
|---|---|---|---|
| `verify_readme_top_three.py` | `gsd-tools.cjs run-with-timeout 30 -- python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`（指定の公式 CLI を `node` で起動） | 必須報告入り作業ツリーで終了1、上記2件を `out-of-scope untracked paths` として列挙、`CLI: not run`。 | FAILED |

### Requirements Coverage — 要件の充足

| 要件 | PLAN | 判定 | 根拠 |
|---|---|---|---|
| REQ-22 | 05-01 | ✓ SATISFIED（製品）／フェーズ検証は BLOCKED | `.planning/REQUIREMENTS.md:74–80` の配置・差分・実 CLI はクリーンな製品で確認。一時入力は既存 `input.txt` と分離。報告込みでの同一検証は未達。Phase 5 に PLAN 未割当ての要件なし。 |
| OpenSpec 1.1 | 05-01 | ✓ SATISFIED（対象実装） | `tasks.md:5` のチェックと `specs/wordfreq-cli/spec.md:5–11` を差分・出力と照合。`openspec-verify.md` の完全性・正しさ・整合性に指摘なし。OpenSpec の判定をフェーズ全体の合格とみなさない。 |

### Decision Coverage — 決定事項

公式結果: `All trackable CONTEXT.md decisions are honored by shipped artifacts.`（D-01〜D-03、3/3、非ブロッキング）。これは報告共存時の実行検証を代替しない。

### Test Quality Audit — 試験の質

| 検証ファイル | 要件 | 有効 | スキップ | 循環 | 検査の強さ | 判定 |
|---|---|---|---|---|---|---|
| `verify_readme_top_three.py` | REQ-22 / OpenSpec 1.1 | 有効 | なし | なし | 配置とバイト差分、実プロセス終了、JSON 配列の順序・件数・値・整数型 | 期待値は仕様由来で CLI から生成しない。必須報告に対する差分分類にギャップ。 |

### Anti-Patterns Found — 問題箇所

| ファイル | 行 | 問題 | 重大度 | 影響 |
|---|---|---|---|---|
| `verify_readme_top_three.py` | 19–43、118–138 | 許容リストに必須の工程報告が2件不足 | 🛑 BLOCKER | 製品差分が正しくても検証が非0で停止し、PLAN の独立検証を報告と同じツリーで再現できない。 |

対象差分に未解決の負債マーカーやスタブは見つからなかった。Nyquist は `05-VALIDATION.md` のとおり PARTIAL（`nyquist_compliant: false`）。Security は `05-SECURITY.md` のとおり `verified`、`threats_open: 0`。PLAN の edge-probe fallback の未分類を合格根拠にしていない。既存回帰試験の今回の終了結果と CI は未確認。

### Human Verification Required — 人手確認

なし。配置・差分・CLI 出力は機械判定可能。画像確認0枚（非画面、閲覧対象なし）。

### Gaps Summary — 未達事項

1. **必須報告を含むツリーでの差分検証と実 CLI の再現性。** 対象原本だけを工程資料として許容し、同じ既存コマンドで報告共存時の終了0と期待3件を確認する。同時に無関係な差分の拒否を維持する。後続フェーズに該当項目がないため延期しない。フェーズは閉じない。

### Recommended Fix Plans — 修正計画への引継ぎ

`/gsd-plan-phase --gaps` 向けの1件。範囲は検証ファイルと回帰確認に限定し、README・製品 CLI・既存フィクスチャの仕様は変更しない。必須報告が未追跡・追跡差分のどちらでも成功し、無関係な差分は失敗することを同じ検証ファイルで確かめる。

---
_Verified: 2026-11-24T05:48:38Z_

_Verifier: Hermes Agent (gsd-verifier)_
