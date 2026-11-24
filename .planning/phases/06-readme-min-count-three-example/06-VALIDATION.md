---
phase: "06"
slug: "readme-min-count-three-example"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-24"
---

# Phase 06 — Validation Strategy

> 計画時の契約。実行未実施。後続の正式validate-phaseがvalidatedを設定するまでdraft。

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | 既存pytest（既存3.12環境の版宣言9.0.3、実行可否は後続で確認） |
| Config file | pyproject.toml（変更禁止） |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k 'min_count_selection or min_count_help_and_readme_example' -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` |
| Estimated runtime | 未測定。後続が実測を記録 |

## Sampling Rate

- 各task終了時: 既存quick試験と、そのtaskのREADME/直接CLI/文字証拠の照合。
- wave終了時: 既存full suite。試験数0、非0exit、skipを隠さない。
- phase検証前: 独立品質の同条件CLI実行、全差分scope、文字原本配送を必須とする。
- Max feedback latency: 未測定（watch-mode無し、有限コマンド）。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 06-01-01 | 01 | 1 | REQ-25, REQ-26 | T-06-01 | READMEのみ編集・無害な入力 | existing integration + direct | quick run commandとPLANの直接3形式・cmp/jq | tests/test_cli.py実在。入力/文字期待は同taskで準備 | pending |
| 06-01-02 | 01 | 1 | REQ-27 | T-06-02 | 別head/別主体の証拠を流用しない | regression + evidence | full suite commandと全git差分・文字原本照合 | 既存testsのみ | pending |

最終task ID/コマンド詳細はPLANで確定。上記は推奨2task構成のsampling map。

## Wave 0 Requirements

新規検証ファイル/fixture/ツール/設定/依存追加は承認範囲外。既存試験を再利用し、直接実行用入力と期待出力は工程文字資料として同taskで準備する。PATHのpytestはimport失敗との調査結果があるため上記既存3.12経路で実測する。使えなければ環境blockを記録し無断installしない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| 新例1つ・既存例/末尾/改行保持 | REQ-25 | 閾値2の既存試験だけでは新例を保証しない | 変更前READMEと全patchを直接読み、指定行以外のbyte保持を確認 |
| 実HTML・語/回数/順序・basename・総数13 | REQ-26 | 検証スクリプト追加禁止 | 3形式stdout全文をread_file、text cmp、JSON jq、HTMLの全行/メタデータを照合 |
| Builder/独立品質の実行と完全原本 | REQ-27 | 主体/実行の事実はpytestで代替不可 | 各自fresh rootのcwd/head/入力/コマンド/exit/stdout/stderrと判定を保存・添付。品質は全git差分を分類しVERIFICATION.mdへ対応付け |

PMは文字原本だけで判定可能にする。画像0枚なら理由を記録、使った画像は品質自身の閲覧枚数/内容/結果を文字で残す。未実行を合格としない。

## Validation Sign-Off

- [ ] 最終PLANの全taskに実在するautomated verifyと対応fails_when
- [ ] 3連続taskで自動検証無しにならない
- [ ] 製品README以外、新規試験/補助スクリプト無し
- [ ] watch-mode無し、実時間記録
- [ ] 独立品質実行とPM可読な原本添付
- [ ] 公式validate-phaseがnyquist_compliantを判定

**Approval:** pending（計画段階）
