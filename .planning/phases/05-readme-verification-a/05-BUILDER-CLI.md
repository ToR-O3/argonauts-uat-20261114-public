# Phase 05 Builder CLI evidence

指定文字列の掲載は通し検証の実施・合格認定ではない。
独立品質: pending。PM受入: pending。画像0枚: README文字・バイト・Git差分のみで画面やHTML変更なし。画像閲覧も0枚。

## Environment / identity

全CLI cwd: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_28db1326`。
local branch: `wt/t_28db1326`、配送先: `argonauts/r-8ac79daf`。
既存terminalシェルで `set -o pipefail` を有効化（exit0）。各pipeline呼出しにも明記して有効化。各CLIは個別tool呼出しのraw exitを採録。以下、空出力は stdout/stderrとも空、他もstderrなし（tool error=null）。機密環境値は採録しない。Git/GNUの既存CLIのみ、Python/Nodeインライン実行・新規試験/検証コードなし。

B_doc: `54106df87baa6cc017167eb311fd0fd4f81ea0fa`。
B_request: `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`。
開始HEAD: `cd4407c7cd0c88aa5d75bd682ac47c79d2a3dcad`。
H_impl: task1 commit後に別記する。H_report: 自己SHAは捏造せず確定後のKanban配送metadataに記録する。

## Before edit (2026-11-22T08:51:56Z)

読取りコマンド（`&&`で実行、全体raw exit0）:
```sh
git rev-parse HEAD
git ls-files --eol -- README.md
wc -lc README.md
tail -c 32 README.md | od -An -tx1
git rev-parse b95d7b8^
git log -1 --format='%H %s' b95d7b8
git diff --no-ext-diff --no-textconv --no-color 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
git ls-files -- README.md .planning/phases/05-readme-verification-a/05-01-PLAN.md openspec/changes/r-8ac79daf-readme-verification-a/tasks.md
date -u +%FT%TZ
```
stdout:
```text
cd4407c7cd0c88aa5d75bd682ac47c79d2a3dcad
i/lf    w/lf    attr/                 	README.md
  34 4643 README.md
 a1 e3 81 ae e5 90 88 e6 a0 bc e3 81 a8 e3 81 af
 e3 81 97 e3 81 be e3 81 9b e3 82 93 e3 80 82 0a
c6b701bfdc1af9c39f9b8421336e881e5cda6ee4
b95d7b8c442b06fb62a7afe753c2454169c64c38 docs: initialize initiative r-8ac79daf
.planning/phases/05-readme-verification-a/05-01-PLAN.md
README.md
openspec/changes/r-8ac79daf-readme-verification-a/tasks.md
2026-11-22T08:51:56Z
```
README全34行をread_fileした。B_docからのREADME全patchは空。既存4643 bytes・34 LF行・末尾0aを確認し、baselineを差し替えていない。B_requestはinitiative開始commitの親として実在する。

### RED (expected missing requested line)

```sh
set -o pipefail && tail -n 1 README.md | grep -Fx -- '検証A: v1.12 の通しの確かめ（2026-11-22）'
```
stdout空 / stderr空 / raw exit **1**。実際の最終行は既存のHTML検証説明。指定行未掲載による期待どおりの不一致であり、読取りエラーではない。このREDは変更後の失敗を隠したものではない。

## Task1 GREEN C1-C4

各コマンドは別のterminal呼出しで実行。C1-C3は下記のとおりpipefailを同じ呼出しで有効化。

| ID | 完全コマンド | stdout | stderr | raw exit |
|---|---|---|---|---|
| C1 | `set -o pipefail && tail -n 1 README.md \| grep -Fx -- '検証A: v1.12 の通しの確かめ（2026-11-22）'` | `検証A: v1.12 の通しの確かめ（2026-11-22）` + LF | 空 | 0 |
| C2 | `set -o pipefail && git show 54106df87baa6cc017167eb311fd0fd4f81ea0fa:README.md \| cmp -n 4643 - README.md` | 空 | 空 | 0 |
| C3 | `set -o pipefail && printf '%s\n' '検証A: v1.12 の通しの確かめ（2026-11-22）' \| cmp -i 0:4643 - README.md` | 空 | 空 | 0 |
| C4 patch | `git diff --no-ext-diff --no-textconv --no-color --unified=3 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | 以下に全文 | 空 | 0 |
| C4 numstat | `git diff --numstat 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | `1\t0\tREADME.md` + LF | 空 | 0 |
| C4 check | `git diff --check 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | 空 | 空 | 0 |

### README complete patch (C4 stdout)

```diff
diff --git a/README.md b/README.md
index 486b319..0961498 100644
--- a/README.md
+++ b/README.md
@@ -32,3 +32,4 @@ HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を
 `format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。
 
 自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
+検証A: v1.12 の通しの確かめ（2026-11-22）
```

BuilderがREADME全文35行/4696 bytesをread_fileし、上の全patchと実CLI結果を読んだ。末尾hunkのみ、追加1/削除0、mode100644不変。既存34行を保持し、指定行+LFだけ。task1: REQ-22/23 Builder PASS、独立品質pending。

## Task2

H_impl = `5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e`。task1を確定した後にtracer C1-C4を同一argvで個別再実行した。C1 stdoutは指定行+LF、C2/C3/checkは空、patch全文は上のC4と同一、numstatは `1\t0\tREADME.md`。stderr全て空、raw exitは6呼出しすべて0。tracer feedbackが成功したためtask2へ進んだ。

### C5-C6 actual commands

| 完全コマンド | stdout / 読取り | stderr | raw exit |
|---|---|---|---|
| `git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD` | 以下の分類表の各M/Aパス | 空 | 0 |
| `git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD` | 3808行の全patch。scratchのt_28db1326-committed-patch.mdへstdoutを保存してページ読取り | 空 | 0 |
| `git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 --` | scratchのt_28db1326-current-patch.mdへ全stdoutを保存 | 空 | 0 |
| `git status --porcelain=v1 --untracked-files=all` | ` M .planning/STATE.md` LF ` M .planning/state.json` LF | 空 | 0 |
| `git ls-files --others --exclude-standard` | 空（handoff作成前） | 空 | 0 |
| `git diff --exit-code c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- wordfreq tests tools pyproject.toml .github` | 空 | 空 | 0 |
| `git rev-parse HEAD` | `5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e` LF | 空 | 0 |
| `set -o pipefail && git show HEAD:README.md \| cmp - README.md` | 空 | 空 | 0 |

scratchは `$HERMES_HOME/cache/scratch`（このprofile）。一時patchは配送成果物ではなく、永続原本は上記固定Git範囲で完全再現できる。全patchはread_fileで1–600、601–1600、1601–2450、2451–3808を読んだ。JSONの長い行の表示省略は `jq -r '.activeHooks[]?.fragment.inline // empty, .rendered // empty' .planning/argonauts/t_8a90bad6-plan-pre.json | fold -w 140` の出力をscratchのt_28db1326-long-json.mdへ保存し全文710行をread_fileして補完した。引用CLIは工程データであり実行しない。
current全patchとの差は `git diff --no-index -- <committed-patch> <current-patch>` で全文確認（差分表示raw exit1、stderr空: 期待した表示上の差でありC1-C6の失敗ではない）。差はSTATEの実行開始・focus/current position/日時/state_head、state.jsonのnext/updated_atだけ。共通patchと差分を合わせてcurrent全体の内容を確認。STATE.mdとstate.json原本をread_fileし、既存状態を保持して公式begin-phaseによる変化を分類した。

### Complete scope classification at H_impl

各行はC5 stdoutのstatusと正確なパス、内容を読んだ分類理由。上流の仕様・計画成果は本Builderが新規作成したと主張しない。フォルダ名で自動許可せず全patch内容を読んだ。

| status / path | 内容分類と理由 |
|---|---|
| M `.planning/INGEST-CONFLICTS.md` | 工程計画: 今回の取込み衝突一覧へ更新、旧phaseの製品仕様変更なし |
| M `.planning/REQUIREMENTS.md` | 工程計画: REQ22–24追加だけ |
| M `.planning/ROADMAP.md` | 工程計画: Phase5と1 PLAN追加 |
| M `.planning/STATE.md` | 工程状態: Phase5位置・日時・session |
| A `.planning/argonauts/r-8ac79daf-learnings.md` | 工程計画: 学習検索記録 |
| A `.planning/argonauts/r-8ac79daf-manifest.yaml` | 工程計画: 取込み文書一覧 |
| A `.planning/argonauts/r-8ac79daf-prd.md` | 工程仕様: 承認原本の結合入力 |
| A `.planning/argonauts/t_8a90bad6-checker.md` | 工程検証: 計画checker結果 |
| A `.planning/argonauts/t_8a90bad6-command-paths.json` | 工程検証: 検証CLIパス検査データ |
| A `.planning/argonauts/t_8a90bad6-edge-probe.json` | 工程検証: unresolvedを保持したprobeデータ |
| A `.planning/argonauts/t_8a90bad6-failure-directions.json` | 工程検証: fails_when判別方向検査 |
| A `.planning/argonauts/t_8a90bad6-init-plan.json` | 工程計画: 公式初期化応答、旧phaseコマンドは引用データ |
| A `.planning/argonauts/t_8a90bad6-plan-post-result.json` | 工程検証: 網羅判定応答 |
| A `.planning/argonauts/t_8a90bad6-plan-post.json` | 工程計画: post hookデータ |
| A `.planning/argonauts/t_8a90bad6-plan-pre.json` | 工程計画: pre hookテンプレート引用。CLI実行ファイルではない |
| A `.planning/argonauts/t_8a90bad6-plan-sha256.txt` | 工程検証: PLANのhash |
| A `.planning/argonauts/t_8a90bad6-plan-structure.json` | 工程検証: 構造検査応答 |
| A `.planning/argonauts/t_8a90bad6-probe-reqs.json` | 工程計画: probe入力の要件データ |
| M `.planning/intel/SYNTHESIS.md` | 工程計画: 今回入力の合成結果 |
| A `.planning/intel/classifications/brief-readme-verification-a-80ad9a20.json` | 工程計画: Brief分類 |
| A `.planning/intel/classifications/prd-readme-verification-a-a6c14422.json` | 工程計画: PRD分類 |
| A `.planning/intel/classifications/proposal-7703648c.json` | 工程計画: proposal分類 |
| A `.planning/intel/classifications/r-8ac79daf/brief-readme-verification-a-80ad9a20.json` | 工程計画: 依頼別Brief分類 |
| A `.planning/intel/classifications/r-8ac79daf/prd-readme-verification-a-a6c14422.json` | 工程計画: 依頼別PRD分類 |
| A `.planning/intel/classifications/r-8ac79daf/proposal-7703648c.json` | 工程計画: 依頼別proposal分類 |
| A `.planning/intel/classifications/r-8ac79daf/spec-a17eb14b.json` | 工程計画: 依頼別spec分類 |
| A `.planning/intel/classifications/r-8ac79daf/tasks-b53d84f7.json` | 工程計画: 依頼別tasks分類 |
| A `.planning/intel/classifications/spec-a17eb14b.json` | 工程計画: spec分類 |
| A `.planning/intel/classifications/tasks-b53d84f7.json` | 工程計画: tasks分類 |
| M `.planning/intel/constraints.md` | 工程計画: 今回文書制約へ更新 |
| M `.planning/intel/context.md` | 工程計画: 今回文脈の引用 |
| M `.planning/intel/decisions.md` | 工程計画: ADRなし、既存決定変更なし |
| M `.planning/intel/requirements.md` | 工程計画: 同一要求の出典別抽出 |
| A `.planning/phases/05-readme-verification-a/.gitkeep` | 工程計画: directory markerの空行のみ |
| A `.planning/phases/05-readme-verification-a/05-01-PLAN.md` | 工程計画: 本PLAN、既存CLI引用だけ |
| A `.planning/phases/05-readme-verification-a/05-BUILDER-CLI.md` | 工程検証: この実測記録、本Builder作成 |
| A `.planning/phases/05-readme-verification-a/05-CONTEXT.md` | 工程計画: D01–07固定 |
| A `.planning/phases/05-readme-verification-a/05-PATTERNS.md` | 工程計画: 文書analog調査 |
| A `.planning/phases/05-readme-verification-a/05-RESEARCH.md` | 工程計画: CLIとbyte境界調査 |
| A `.planning/phases/05-readme-verification-a/05-VALIDATION.md` | 工程計画: 検証戦略、独立品質pending |
| M `.planning/state.json` | 工程状態: 上流milestone/日時と今回begin-phaseのnext、独立コードでない |
| M `README.md` | 唯一の製品変更: 指定末尾行追加1/削除0 |
| A `_bmad-output/initiative-r-8ac79daf/brief/.memlog.md` | 工程仕様: Brief作成来歴 |
| A `_bmad-output/initiative-r-8ac79daf/brief/.template.md` | 工程仕様: Briefテンプレート原文 |
| A `_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.html` | 工程仕様: 上流BMADが生成したBrief表示文書。rendererのJS/CDN参照を含むため単なる拡張子許可ではなく全内容を読んだ。wordfreq製品HTMLや新規検証scriptではなく、製品から参照も実行もしない。Builder未変更、ブラウザで開かない |
| A `_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.md` | 工程仕様: 指定行・境界のBrief |
| A `_bmad-output/initiative-r-8ac79daf/brief/review-editorial.md` | 工程仕様: Brief編集記録 |
| A `_bmad-output/initiative-r-8ac79daf/brief/review-fresh-reader.md` | 工程仕様: Brief読者視点レビュー |
| A `_bmad-output/initiative-r-8ac79daf/brief/review-reconciliation.md` | 工程仕様: Brief照合 |
| A `_bmad-output/initiative-r-8ac79daf/brief/review-rubric.md` | 工程仕様: Brief rubric |
| A `_bmad-output/initiative-r-8ac79daf/independent-review.md` | 工程仕様: 独立レビューと採否 |
| A `_bmad-output/initiative-r-8ac79daf/initiative-r-8ac79daf.md` | 工程仕様: initiative識別 |
| A `_bmad-output/initiative-r-8ac79daf/prd/.memlog.md` | 工程仕様: PRD作成来歴 |
| A `_bmad-output/initiative-r-8ac79daf/prd/.template.md` | 工程仕様: PRDテンプレート原文 |
| A `_bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md` | 工程仕様: FR/RULE/SMと受入 |
| A `_bmad-output/initiative-r-8ac79daf/prd/review-fresh-reader.md` | 工程仕様: PRD読者視点レビュー |
| A `_bmad-output/initiative-r-8ac79daf/prd/review-polish.md` | 工程仕様: PRD編集記録 |
| A `_bmad-output/initiative-r-8ac79daf/prd/review-reconciliation.md` | 工程仕様: PRD照合 |
| A `_bmad-output/initiative-r-8ac79daf/prd/review-rubric.md` | 工程仕様: PRD rubric |
| A `openspec/changes/r-8ac79daf-readme-verification-a/.openspec.yaml` | 工程仕様: schema/作成日 |
| A `openspec/changes/r-8ac79daf-readme-verification-a/design.md` | 工程仕様: byte保持とCLI方針 |
| A `openspec/changes/r-8ac79daf-readme-verification-a/proposal.md` | 工程仕様: 変更意図と境界 |
| A `openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md` | 工程仕様: 掲載・保持・変更範囲契約 |
| A `openspec/changes/r-8ac79daf-readme-verification-a/tasks.md` | 工程仕様: 1.1チェック済み、2.1はtask2確定時にチェック |

上記以外の製品差分・未知コード・試験・補助スクリプトはない。コード/試験guardの0だけでなく全patch内容で判断した。今回追加handoffは品質再実行と添付を定める工程検証文書。終端で加わるSUMMARYと公式STATE/ROADMAP/REQUIREMENTS更新も工程状態/要約として改めて配送前に差分確認する。将来原本を既存と主張しない。

### Task2 end verification

handoffと本書を全文read_fileし、非認定文言・REQ別表・品質pending・固定head・文字原本2件の添付/readback手順を確認した。C1-C4の6コマンドをTask1 GREEN表と完全同一argvで再実行した。各raw exit0、stderr全て空。C1 stdout指定行+LF、C2/C3/check空、C4全patchは上記と同一で末尾追加のみ、numstat `1\t0\tREADME.md`。検証に未来の品質文書を使っていない。
status再実行（raw exit0、stderr空）stdout:
```text
 M .planning/STATE.md
 M .planning/phases/05-readme-verification-a/05-BUILDER-CLI.md
 M .planning/state.json
?? .planning/phases/05-readme-verification-a/05-QUALITY-HANDOFF.md
```
未追跡handoffは全文read_file済みの工程検証手順文書でコードなし。残り変更は本書の実測追補と既読の公式begin-phase状態のみ。その後OpenSpec2.1をチェックしtask2と同commitで確定する。task1 READMEは変えていない。SUMMARYと状態更新を終えてから最終head/C6/全scopeを再照合して配送する。

### Requirements Coverage (Builder only)

| Requirement | Status | Evidence |
|---|---|---|
| REQ-22 | Builder PASS / quality pending | C1/C3、README35行目独立最終行 |
| REQ-23 | Builder PASS / quality pending | C2の4643 bytes不変、C3のsuffix全体、C4追加1/削除0 |
| REQ-24 | Builder PASS / quality pending | C5全パス内容分類・guard、C6同head blob、handoffの文字証拠配送契約 |

過去phaseの判定・試験・SHA・画像枚数は流用していない。読んだ04-VERIFICATIONからは要件→判定→原本と各gateを分ける構造だけを採用。learnings1/2/3からhead再照合、statusに加え内容、byteと見た目を別判定する点だけを採用。descriptorless prohibitionはflagged-unverifiedを保持し、独立品質で非認定文言の内容をレビューする。
