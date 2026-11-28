## Conflict Detection Report

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。対象は `.planning/argonauts/r-6442a149-manifest.yaml` と一致する `.planning/intel/classifications/r-6442a149-canonical/` の正本5分類のみ。全件manifest_override=true、precedence=null。今回の承認済み製品判断を取り消さず、公式gateの衝突を親へ返す。宛先PROJECT/REQUIREMENTS/ROADMAP/STATEは未変更。

### BLOCKERS (1)

[BLOCKER] Incoming HTML total decision contradicts existing locked CONTEXT
  Found: 除外指定時のHTML総数は除外後・min-count/top前。Zoo apple APPLE zoo bananaからapple除外で総数3、全語除外では0。これは今回承認済み変更であり、casefold維持・提案1〜6採用を再審査しない。
  Expected: Phase 4 locked D-05は元countsを破壊せず、min-count/top前の元回数和を保持し、語あり全除外でも元正数を保持する。今回の名前指定除外は既存の元総数契約を指定時だけ変更する。incoming locked ADRは0だが、merge pass 2の既存locked CONTEXTとの矛盾として自動上書きしない。
  source: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:73-78,93-114; _bmad-output/initiative-r-6442a149/architecture/architecture.md:29-33,53-57; _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:60,80,84-86; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:13-25; .planning/REQUIREMENTS.md:60; .planning/ROADMAP.md:104; user task（PM approved head=8a2c69b8332e9704377fe680af51767c74e4ab56）。
  → 親のE.7承認済み変更用の追加phase分岐へ渡す。旧locked履歴を消さず標準mergeでは宛先を書かない。製品判断の再質問やOQ-7/8の追加条件化は不要。本担当はphaseを追加しない。

### WARNINGS (0)

競合PRD acceptance variantなし。PRDは1件であり、SPEC/PRD/DOCのcasefold・行全体比較・最後FILE・読込順・失敗コード・空結果・除外後総数は一致する。OQ-7/8は背景不足のみ。旧依頼固有のREADME最終行・description値・固定起点・変更範囲を今回の追加受入条件にしない。
source: 正本5分類と対応原本; _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:58-88,144-151; .planning/phases/05-readme-verification-a/05-CONTEXT.md:8-24; .planning/phases/07-project-description-uat/07-CONTEXT.md:8-24。

### INFO (0)

precedenceによる自動解決なし。ADR 0、locked ADR 0、UNKNOWN 0。今回5ノードのcross_refsに循環なし。前回6件で検出したBrief↔PRD循環は、親がmanifestを正本5件へ縮小しBriefを背景参照に限定したことで今回の取込集合外となった。原本の相互参照は変更しておらず、外部Briefを再帰取込しない。詳細はintel/SYNTHESIS.md。初出順はPhase 3で旧語昇順を置換済みであり、incomingはその現行契約を維持する。承認日時やファイル順を自動勝者選択に使わない。
source: .planning/argonauts/r-6442a149-manifest.yaml; .planning/intel/classifications/r-6442a149-canonical/*.json; 旧 .planning/intel/classifications/r-6442a149/brief-wordfreq-exclude-5016d233.json:18-22; _bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:36; .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:17-18; user task。

GSD > BLOCKED: 1 blockers must be resolved before ingest can proceed.
