# Phase 5: README validation B - Research

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は05-CONTEXT.md:13-22,45-47の原文。指示の新設ではなく、計画対象の制約データとして引用する。

### Locked Decisions
### Locked: 指定の文書状態
- D-01: `検証B: v1.12 の通しの確かめ（2026-11-22）` を引用符なしの独立した最終行として1回だけ追加する。文字列の言い換えは禁止。
- D-02: 既存内容・書式・改行形式を保持する。README差分は上記1行追加のみ、削除・置換・移動・余分な空行や説明なし。
- D-03: コード・試験・他の製品ファイルは変更しない。新しい製品の振る舞い・試験ファイル・自動追記機能や検証スクリプトを追加しない。工程記録は別扱い。
- D-04: 完了時CLIで最終行完全一致・README全体の指定行出現1回・差分1行追加のみ・工程記録を除く製品変更README.mdのみを確認し、文字の工程検証記録へ残す。指定行自体は検証合格の証拠ではない。
- D-05: 人の回答によりskip_specsは使わず、最小specは指定行存在の1要求のみ。機能要件を増やさない。
- D-06: 所定の実装レビュー・phase検証・受入の後に最終化工程でsync/archiveする。この計画工程では実装しない。
### Claude's Discretion
既存CLIで承認条件を確認する具体的なコマンドと、工程記録の構成のみ。範囲の拡張や新規試験は裁量外。

### Deferred Ideas (OUT OF SCOPE)
機能・API・依存・権限・データ・外部送信・費用の変更、既存文書の整形、新しい試験は対象外。過去phaseのstale検証は今回の範囲外。未決事項なし。
</user_constraints>

## Summary

**Domain:** docs-onlyの最小追記と既存CLIによる文書受入確認。
**Confidence:** LOW（公式classify-confidenceのprovider=official結果。ローカル一次資料の事実と、未実行の検証提案を以下で区別する。この分類は要件の不確実性を意味しない）。

**Primary recommendation:** 単一PLAN・単一waveで、既存READMEへの直接1行追記と、その差分・最終行・出現数・変更範囲のCLI証拠化を計画する。試験追加taskやWave 0の検証基盤作成は置かない。根拠は「自動追記機能や新しい試験の実装」をNon-Goalsとし、直接追記・既存CLI確認を選ぶ承認design。 [VERIFIED: openspec/changes/r-215b4390-readme-validation-b/design.md:9-18]

現状のREADMEはwordfreqの実行説明と部品契約で、最後の段落は「自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。」から始まる。読取結果では指定追記はまだない。これは実装前の文書読取りであり、受入検証の合格ではない。改行形式・末尾LFのバイト状態はread_file表示だけから断定しない。 [VERIFIED: README.md:1-34]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| REQ-22 | README.md末尾に `検証B: v1.12 の通しの確かめ（2026-11-22）` が引用符なしの独立した最終行として1回だけ存在する。既存内容を保持し、製品差分は指定行1行追加のみ。コード・試験・他の製品ファイルを変更しない。CLIで最終行完全一致・出現1回・既存内容保持・製品変更限定を確認する。新しい製品の振る舞いや試験ファイルは追加せず、工程記録は別扱い。 | 最小patch、固定した変更前基底とのGit差分、既存grep/tail、文字の受入記録。 |

上記IDと要件は原文。 [VERIFIED: .planning/REQUIREMENTS.md:74-82]
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 指定行の保持 | 静的文書 | — | 製品変更は「README.md」だけ。 |
| 内容・範囲の照合 | 工程のCLI確認 | 手動の文字照合 | 新しい製品機能・試験ではない。 |
| 独立品質と受入 | 工程記録 | PMの原本読取り | head・実コマンド・実結果で判断する。 |

責務境界の根拠：「製品差分は指定1行のみ」「コード・試験・検証機能や試験ファイルの新設なし」。 [VERIFIED: .planning/ROADMAP.md:124-131]

## Project Constraints (from HERMES.md)

ルートHERMES.mdと設定の「./.hermes/HERMES.md」を直接read_fileしたが、いずれもnot_foundだった。追加の指示は抽出していない。設定の参照文字列は原文どおり。 [VERIFIED: .planning/config.json:63-68; 本調査のread_file結果]

.hermes/skillsと.agents/skillsの探索結果はPath not found。AGENT_SKILLS_RESEARCHERの公式--skills-only結果が空であることは今回の委任入力による。そこから別phaseのskill・要求を補完しない。 [CITED: 委任入力additional_context; 本調査search_files結果]

## Standard Stack

| Tool | Observed version | Purpose |
|---|---|---|
| Git | 2.52.0 | 基底・対象head、差分、変更ファイル確認 |
| GNU grep | 3.11 | 固定文字列・完全行の照合 |
| GNU tail | coreutils 9.5 | 最終行の抽出 |
| read_file | 提供ツール | 承認文書・工程証拠の読取り |

バージョンは既存CLIの--version出力。追加installは不要とする計画であり、package依存は推奨しない。jqも起動できたがversion表示は「jq-」のみで、版番号を断定しない。 [VERIFIED: 本調査terminal --version出力]

## Architecture Patterns

推奨フロー：承認要件 → 変更前基底の記録 → 末尾の局所patch → 内容と差分の直接照合 → 対象headで独立品質 → 文字証拠による受入。sync/archiveは後続の最終化工程に残す。 [VERIFIED: openspec/changes/r-215b4390-readme-validation-b/tasks.md:3-9]

PLANは「README.md」だけを製品側files_modifiedに置く。工程記録は別に明記し、git全体の変更一覧から個別に分類する。工程記録を理由に任意のMarkdownやdocs配下全体を検査から除外しない。単一taskで追記とBuilderの確認を扱い、独立品質・phase受入を完了条件に含めることを推奨する。これは要件を増やさない計画上の提案。 [VERIFIED: .planning/phases/05-readme-validation-b/05-CONTEXT.md:15-22,39-42]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---|---|---|
| 追記 | shell/Python追記プログラム、自動追記機能 | 既存末尾への局所編集 |
| 検証 | 新規test、validator、検証shell/Pythonファイル | 既存CLIの直接実行と文字照合 |
| 工程確認 | 独自GSD状態parser | 公式GSD CLIの判定 |

禁止・代替の根拠は承認designの「テンプレート生成やスクリプト追加は、1行の変更に不要なため採用しない」「試験ファイルを新設しない」と委任入力。 [VERIFIED: openspec/changes/r-215b4390-readme-validation-b/design.md:15-18] [CITED: 委任入力]

## Common Pitfalls

- **基底を動くHEADのままにする:** commit後のgit diff HEADでは変更が消えて見える。Builderは最初の製品編集前の完全SHAを記録し、品質は同じ基底と対象headの差分を読む。工程記録の報告commitと製品検証headを分ける。 [VERIFIED: .planning/argonauts/r-215b4390-learnings.md:14-19,30-34]
- **statusだけで合格にする:** パス一覧では1行差分や既存保持を示せない。numstatと実patchを両方読む。未追跡ファイルも別途一覧で確認する。 [VERIFIED: .planning/argonauts/r-215b4390-learnings.md:22-27]
- **grepのexit0を「1回」と誤認する:** grepの成功は選択行があることだけ。-cは出現文字列数ではなく選択行数。同一行に複数回含むケースまで区別するには-Foの出力も照合する。 [VERIFIED: 本調査grep --help出力]
- **余分な空行・全角括弧の変更・改行変換:** 最終行の完全一致だけで既存保持を代替しない。差分の削除や全体変更を拒否する。 [VERIFIED: .planning/phases/05-readme-validation-b/05-CONTEXT.md:15-18]
- **過去phaseの要件を移植する:** pytest全件やHTMLブラウザ画像はREQ-22の合格条件ではない。画像閲覧は0枚・UI変更なしと記録する。 [VERIFIED: .planning/phases/05-readme-validation-b/05-CONTEXT.md:39-47; .planning/ROADMAP.md:124-132]

## Code Examples

製品コード例は不要。以下はBuilder・品質用の**未実行のCLI提案**であり、本調査ではREADMEの検証として試行していない。新規検証ファイルを参照・作成しない。入力ファイル「README.md」と指定文字列は承認taskの原文。 [VERIFIED: openspec/changes/r-215b4390-readme-validation-b/tasks.md:5]

```text
tail -n 1 README.md | grep -Fx '検証B: v1.12 の通しの確かめ（2026-11-22）'
grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md
grep -Fo '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md
```

期待条件：先頭の照合は指定行を出力しexit0、完全行数は1、-Foの一致出力も指定文字列1件のみ。exit1は不一致、grepのexit2は実行エラーであり、未検証として止める。行数・出力内容は文字で確認し、exit0だけでは合格にしない。tailの読取失敗もstderrと終了状況で確認する。 [VERIFIED: 本調査grep --help、tail --help出力]

Gitは実行段階で記録した完全SHAを用い、次の形を使う。山括弧部分は説明用であり、そのまま実行するコマンドではない。PLANにはSHA取得・記録の手順を明示し、実記録には置換済みのargvを残す。

```text
git rev-parse HEAD
git diff --numstat <変更前基底SHA> -- README.md
git diff --no-ext-diff --no-textconv --unified=0 <変更前基底SHA> -- README.md
git diff --name-status <変更前基底SHA>
git status --short --untracked-files=all
```

Builderは基底→working tree（stage済みも含む）の内容を確認する。品質は上記diffへ対象head SHAを第2のcommitとして明記し、基底→対象headを比較する。同時に品質の作業ツリーに差分がないことを確認してから、対象headのREADMEへgrep/tailを実行する。期待はnumstatが追加1・削除0・README.md、patchの追加本文が指定行だけ、製品変更がREADME.mdのみ。差分コマンドのexit0は一致のassertではないため、実出力の読み合わせが必要。 [CITED: https://git-scm.com/docs/git-diff] [VERIFIED: 本調査git diff -h出力]

## Validation Architecture

設定は「nyquist_validation": true」と「security_enforcement": true」。試験新設で満たすのではなく、直接CLIと手動判定を組み合わせた文書受入として計画する。 [VERIFIED: .planning/config.json:21-25,49-51]

### Test Framework

| Property | Value |
|---|---|
| Framework | 文書受入の既存Git・grep・tail。専用test frameworkは導入しない |
| Config file | 新設なし |
| Quick run command | 上記tail→grep完全一致とgrep -Fxc / -Fo |
| Full suite command | 同CLIに固定基底のnumstat・patch・全変更一覧・status確認を加える |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command / Evidence | File Exists? |
|---|---|---|---|---|
| REQ-22 | 独立した最終行・指定行1回 | CLI + manual output check | 上記tail/grep。完全行数1・一致出力1件を照合 | README.mdをread_file済み。test追加なし |
| REQ-22 | 既存保持・指定1行追加 | manual diff acceptance | 固定基底のgit diff --numstatと実patch | README.mdをread_file済み。test追加なし |
| REQ-22 | 製品変更限定 | manual scope acceptance | 全変更一覧と未追跡を含むstatus、工程記録の個別分類 | 新規検証ファイル不要 |

### Sampling Rate

- **各task終了時:** Builderが上記の全確認を実行し、コマンド・stdout/stderr・終了コード・判定を工程記録へ残す。
- **各wave完了時:** 同じ確認をその時点の基底・対象状態で実行する。単一waveを推奨する。
- **Phase gate:** 品質が対象headから独立して同じ受入確認を行い、VERIFICATION.mdとCLI証拠文書に対象head・基底SHA・実argv・実結果・REQ-22対応・手動判定・未検証事項を記録し標準添付する。画像閲覧0枚と理由を明記する。 [VERIFIED: .planning/ROADMAP.md:127-131; .planning/phases/05-readme-validation-b/05-CONTEXT.md:39-42]

### Manual Verification

PM/品質は文字証拠とpatchをread_fileで読み、文字列、末尾位置、出現数、既存本文、改行保持、製品変更範囲を判断する。CLIだけで期待値全体をassertするプログラムは作らない。実装時の改行形式と差分が要件を満たさなければ合格にせず、最小の追記を修正して再確認する。 [VERIFIED: openspec/changes/r-215b4390-readme-validation-b/design.md:15-23]

### Wave 0 Gaps

**なし（今回の受入は既存CLIと手動照合で実施）。** 専用自動試験がないことを埋めるためのtest/config/fixture/script作成を計画しない。これは過去試験がREQ-22を網羅するという主張ではない。 [VERIFIED: .planning/REQUIREMENTS.md:78]

## Security Domain

今回の変更境界には認証・セッション・アクセス制御・入力処理・暗号機能の追加はない。ASVS V2/V3/V4/V5/V6はいずれも本差分への追加実装は非該当とする。新しい入力検証libraryやsecurity testを追加しない。主な工程リスクは、文書の誤記、範囲外変更、証拠対象headの取り違えであり、固定基底・直接diff・原本の読取りで抑える。 [VERIFIED: .planning/phases/05-readme-validation-b/05-CONTEXT.md:15-22,45-47; .planning/argonauts/r-215b4390-learnings.md:18-19]

## Environment Availability

Step 2.6: SKIPPED（外部サービス・新規packageの依存なし）。既存CLIの版とhelpのみ取得した。検証CLIの実試行、製品編集、試験実行はしていない。grepのWebマニュアル取得はSOURCE_NOT_AVAILABLEだったため、利用中GNU grep自身の--helpで構文と終了コードを調べた。git diff -hのexit129はhelp呼出しの結果であり、README検証の失敗ではない。 [VERIFIED: 本調査tool出力]

## Open Questions

- 製品仕様の未決事項なし。改行形式・末尾LFの実バイト確認と最終SHAは実装・品質段階の対象状態に依存するため、ここでは未確認として残す。推測した改行形式や未来のcommit SHAをPLANへ固定しない。 [VERIFIED: .planning/phases/05-readme-validation-b/05-CONTEXT.md:47; README.mdのread_file表示]
- STATEのcurrent_phaseは「4」だが、Roadmapには「Phase 5: README validation B」があり、公式init.phase-op 5がphase_found=true、phase_number="05"、has_plans=falseを返した。過去phaseを再開する根拠にしない。graphifyはdisabled=trueを返したため有効化していない。 [VERIFIED: .planning/STATE.md:3-6,89-95; .planning/ROADMAP.md:122-137; 本調査公式CLI出力]

## Assumptions Log

未確認の実装結果を前提にした事実主張は置いていない。CLI例は未実行の提案として明示した。Confidence分類の公式seamはprovider=officialをLOWとした。追加でcontext7分類を照会するとMEDIUMだったが、Context7取得はしていないため、この値を本調査の取得経路として転用しない。 [VERIFIED: 本調査classify-confidence出力]

## Sources

- 一次資料：05-CONTEXT.md、REQUIREMENTS.mdのREQ-22、ROADMAP.mdのPhase 5、承認OpenSpec design/spec/tasks。各事実の参照箇所は本文に併記。
- 計画参考：.planning/argonauts/r-215b4390-learnings.md（過去要求・過去成功の転用なし）。
- 既存CLI：git --version / diff -h、grep --version / --help、tail --version / --help。
- Git公式説明：https://git-scm.com/docs/git-diff （差分の比較対象と構文）。
- GSD公式CLI：query init.phase-op 5、graphify status、query classify-confidence。製品検証の代替には用いない。

## Metadata

調査は承認文書・README読取り、公式GSD照会、既存CLIの版/help確認と本ファイル作成のみ。README・コード・試験の変更、新規検証プログラム、commit/push/kanban操作は実施していない。再利用のための新規skill保存も本依頼の成果範囲に含めない。
