---
phase: "05"
slug: "readme-verification-a"
status: verified
threats_open: 0
asvs_level: 1
created: "2026-11-22"
---

# Phase 05 — Security

公式 gsd-secure-phase 5 のState B。PLANに計画時registerあり、SUMMARY全文を確認。ASVS L1 / block_on high、両設定とverify:post security stepを公式CLIで確認。公式gsd-security-auditorの判定を使用。新規脅威探索やコード変更は行わない。

## Trust Boundaries

| Boundary | Description | Data Crossing |
|---|---|---|
| 承認文字列→README | 固定quoteを文字データとして掲載 | 公開文書文字列 |
| Git baseline/head→品質記録/配送 | 不同headや未配送を同一証拠にしない | commit・blob・CLI文字証拠 |

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|---|---|---|---|---|---|---|
| T-05-01 | Tampering | README | medium | mitigate | 独立C1-C4すべてraw0、既存4643byte不変・指定suffix全体・追加1削除0 | closed |
| T-05-02 | Tampering | request-wide scope | medium | mitigate | 公式auditorが全4116行patch・長文JSON710行・全66pathを内容確認。禁止guard0、製品はREADME1行のみ | closed |
| T-05-03 | Repudiation | evidence provenance/delivery | medium | mitigate | H_impl/H_report/C6一致と手順は検証済み。正式2原本の添付SHA/読戻しは親の後処理で完了まで未確認 | open — below high threshold (non-blocking) |
| T-05-SC | Tampering | package installs | low | accept | package導入/依存変更なしを全差分とguardで確認。下記accepted risksへ明記 | closed |

`threats_open`はhigh以上のblocking-open件数で0。mediumの配送gateはphase完了とは別に必須であり、添付未完を合格へ変換しない。VERIFICATIONと文字原本の標準添付・SHA一致・正確な添付readbackが完了するまで親は完了を返さない。これは受入条件の免除や未完のリスク受容ではない。

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---|---|---|---|---|
| R-05-SC | T-05-SC | 実行時package追加はないためpackage audit/checkpointは不要。依存変更を既存C5で拒否する | 承認済み05-01-PLAN.md threat_modelのlow/acceptを品質が記録 | 2026-11-22 |

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|---|---|---|---|---|
| 2026-11-22 | 4 | 3 | 1 medium non-blocking | quality t_df0c2ebc / official gsd-security-auditor sa-0-7e548cdf |

詳細は05-SECURITY-EVIDENCE.md。auditor返答はOPEN_THREATS、blocking 0、当時未作成だったaccepted logは本書で補完。T-05-03は添付後に親が根拠を確認する。設定を弱めず、公式security gateのblocking-open0でverifierへ進める。

## Sign-Off

- [x] All threats have a disposition.
- [x] Accepted risk documented.
- [x] threats_open: 0 (blocking only).
- [x] status: verified for L1 mitigation audit; downstream delivery remains explicitly open.

画像閲覧0枚：README文字・byte・Git差分のみ。工程Brief HTMLはソースの表示rendererでCDN参照を含み、製品UI/HTML変更ではない。ブラウザ無通信は認定していない。指定文字列の掲載は通し検証の実施・合格認定ではない。descriptorless prohibitionはflagged-unverifiedを保持。
