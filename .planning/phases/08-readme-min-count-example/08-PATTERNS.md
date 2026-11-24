# Phase 8: README min-count example - Pattern Map

**Mapped:** 2026-11-25 (JST)
**Files analyzed:** 4（製品1、工程記録3。工程記録名はPlanner向け候補であり追加要件ではない）
**Analogs found:** 4 / 4（tracked原本3件を再利用）

## Scope and Authority

- 公式 `gsd-pattern-mapper` 本文を全文読み、08-CONTEXT.mdと08-RESEARCH.mdを起点にREADONLY調査した。今回書くのは本PATTERNSだけ。README、製品コード、試験、検証ツールは編集しない。commit/push/Kanban操作なし。
- locked scopeはCONTEXT D-01〜D-07。製品変更は既存使い方フェンスへの `python -m wordfreq input.txt --min-count 3` 1行追加のみ。既存例・説明・末尾を保持する。text/json/htmlの実行確認は対象外であり、未完了条件に戻さない。
- 固定基準branchは **`v112-a`**。研究の `origin/main` 比較は今回の基準に採用しない。調査時のローカル `v112-a^{commit}` は `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`、HEADは `bb8726174f9796493f836ca139e264121186763f`、作業branchは `wt/t_19c23e10`。SHAが参考研究と同値でも基準branchを読み替えない。最終PRでは後続品質が**実際のbase/headとmerge-base**を取得し全一覧を再確認する。
- `gsd_run query init.phase-op 8` はphase_found=true、phase_number=08、has_context=true、has_research=true、has_plans=false、plan_count=0。指定ランチャーを同terminalでsourceして実行した。`query agent-skills gsd-pattern-mapper --skills-only` は空出力。HERMES.md、.hermes/skills/、.agents/skills/は存在しなかった。

## File Classification

静的文書なのでroleはdocumentation / process-recordに拡張する。CRUD、認証、API、DB、runtimeの新規データ経路はない。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `README.md`（変更） | documentation / 利用者向けCLI例 | file-I/O → 静的Markdown閲覧 | `README.md`:5–26,35 | exact |
| `.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md`（工程記録候補） | process-record / Builder自己確認 | Git blob・patch・全一覧 → 文字証拠 → 品質引継ぎ | `.planning/phases/05-readme-verification-a/05-BUILDER-CLI.md`:3–15,58–79,103–108,188–196 | role-match |
| `.planning/phases/08-readme-min-count-example/08-QUALITY-CLI.md`（後続品質の文字原本候補） | process-record / 独立観測 | 対象SHA → Git原本・差分・全一覧 → 文字原本 | `.planning/phases/05-readme-verification-a/05-BUILDER-CLI.md`:58–79,89–108（記録形式のみ） | role-match |
| `.planning/phases/08-readme-min-count-example/08-VERIFICATION.md`（後続品質） | process-record / 要件別判定 | 独立文字原本 → 2条件判定 → 標準添付 → PM読取り | `.planning/phases/05-readme-verification-a/05-VERIFICATION.md`:51–63,73–79,128–134,197–199 | role-match |

CONTEXT D-06がVERIFICATION.mdと文字証拠を要求する。RESEARCH:113–116,186はBuilder工程記録の名前をPlanner裁量とするため、上のCLI名は候補であり不要な別文書を増設する指示ではない。PLAN、SUMMARY、VALIDATIONなどfull工程原本は既存ワークフローとして保持し、製品変更や新規実行ファイルと数えない。CONTEXT/RESEARCH/PRD/OpenSpec/BMAD原本は入力であり、本依頼による書換え対象ではない。過去phaseの製品・工程成果も修復対象外。

## Pattern Assignments

### `README.md` — existing usage fence, not a new section

**Analog:** tracked `README.md`。同一文書内の既存CLI例が最も近い。

**Core pattern** (`README.md`:5–15):

````markdown
## wordfreq の実行

リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。

```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
python -m wordfreq input.txt --format html > result.html
```
````

基本例の直後へ指定行を挿入する。これはBuilder向け期待差分で、今回実施した変更ではない。

```diff
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
```

**Validation / preservation:** 既存オプション説明 (`README.md`:19) は次のまま保持する。

```markdown
- `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
```

末尾 (`README.md`:35) も位置・内容を保つ。今回の例を末尾へ足さない。

```text
検証A: v1.12 の通しの確かめ（2026-11-22）
```

imports/auth/error-handling/testコードは非適用。掲載コマンドを実行したという証拠は作らない。README:34の過去ブラウザ試験説明は保存する本文であり、今回の実行範囲ではない。

### Builder文字記録 — retain observations, not old acceptance criteria

**Analog:** tracked `.planning/phases/05-readme-verification-a/05-BUILDER-CLI.md`。

**Identity / gate distinction** (lines 3–4):

```text
指定文字列の掲載は通し検証の実施・合格認定ではない。
独立品質: pending。PM受入: pending。画像0枚: README文字・バイト・Git差分のみで画面やHTML変更なし。画像閲覧も0枚。
```

採用するのは掲載と実行認定、自己確認と独立品質を分ける構造。今回の記録ではREQ-28/REQ-29へ対応を更新し、3形式実行を要求・実施済みとしない。

**Command / output recording** (lines 58–65の形式とpatch行頭):

```markdown
| ID | 完全コマンド | stdout | stderr | raw exit |
|---|---|---|---|---|
```

```diff
# 原本 lines 70–74（過去diffの書式見本、今回の結果ではない）
diff --git a/README.md b/README.md
index 486b319..0961498 100644
--- a/README.md
+++ b/README.md
@@ -32,3 +32,4 @@ HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を
```

固定した編集前SHA・作業場所・入力README、実際のGit patchと全一覧、直接読んだ内容判定を記録する。過去SHA、末尾追加hunk、tail/grep/cmpの旧検証、固定byte数はコピーしない。今回の編集は使い方フェンス内への挿入であり、旧prefix/suffix方式を移植しない。

**Full-list classification** (lines 103–108):

```markdown
### Complete scope classification at H_impl

各行はC5 stdoutのstatusと正確なパス、内容を読んだ分類理由。上流の仕様・計画成果は本Builderが新規作成したと主張しない。フォルダ名で自動許可せず全patch内容を読んだ。

| status / path | 内容分類と理由 |
|---|---|
```

全パスを隠さず文字記録に残すという形式だけ採る。旧phaseの「唯一の製品変更がREADMEならPASS」は今回は不十分。**工程ファイルも含めてREADME以外が残れば整備前REQ-29は未達/暫定**であり、製品だけのguardで最終合格にしない。

### 独立品質の文字原本 / `08-VERIFICATION.md`

**Analog:** tracked `.planning/phases/05-readme-verification-a/05-VERIFICATION.md`。QUALITY-CLI候補には上記Builder原本のstdout/stderr/raw exit・patch書式を使うが、品質自身が取得した結果を書く。

**Scope provenance** (lines 51–54,62–63):

```markdown
## Scope / Head Provenance

| Role | Exact value / status |
|---|---|
| quality report commit | 未確定。自己SHAを捏造しない。親が確定後に記録・再照合する |
| images / browser | 画像閲覧0枚。README文字/byte/Git差分だけの製品変更、UI hint=no、UI-SPECなし。browser/E2E認定なし |
```

今回の欄には固定基準branch `v112-a`、実際の対象base/head/merge-base、整備前か最終PR整備後かを明記する。未確定SHAを捏造しない。

**Requirement → result → evidence** (lines 128–131):

```markdown
### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
```

今回は2行だけを内容判定の軸にする。

- REQ-28: 原本と文字差分に指定例1件が追加され、既存本文・末尾が保持される。
- REQ-29: **最終PRの実際のbase...head全一覧がREADME.mdのみ**。空一覧、工程文書残存、別head、出力省略なら合格にしない。整備前は残る全ファイルを列挙して暫定と記す。

旧reportのstatus、score、REQ番号、回帰実績、UAT、prohibition、過去gateは引き継がない。画像は0枚、理由はREADME原本と文字差分の文書検証でUI変更なし。

**Attachment boundary** (line 199からの具体抜粋):

```text
正確なstored_pathのread_file全文読戻し、原本/添付SHA-256一致、対象head/C6終端照合を行い、未完ならpendingのまま。
```

これは後続配送の原本/添付照合パターン。今回mapperは添付を実施しない。今回の正式手順はCONTEXT D-03/D-06と後続の公式チームD.5を優先する。

## Shared Patterns

### 1. Three scopes stay separate

CONTEXT:14–20とRESEARCH:101–107を適用する。

1. **Builder局所確認:** 編集直前の固定SHA対編集後README。使い方への追加1行と全既存内容保持を原本・patchで確認。
2. **整備前phase確認:** `v112-a`を固定基準branchとして対象base/headを記録し、先行PLAN含む全一覧を除外なしで文字化。工程が残ればREQ-29未達/暫定。作業ツリー未記録変更も別途明示。
3. **最終PR確認:** 後続D.5整備後、品質が実際のPR base/headを再取得して全一覧・README原本・patchを独立確認。途中headの証拠を最終証拠として流用しない。

### 2. Existing Git + direct reading, not a new verifier

RESEARCH:153–186の既存Git読取り形式をPlannerが参照できる。`git diff --name-status` / `--name-only` の全一覧にはpath制限を付けず、本文patchにだけ `-- README.md` を付ける。`--check`の成功は空白確認であり2条件の合格ではない。確認の入力は実在するREADMEとGit object。計画中に将来の検証を試走しない。

PLANの検証はBuilder/品質がその時点で実在する検証対象・検証ファイルから実施する。ここで新規script、test、fixture、ツールやWave 0を作らない。インラインPython/Nodeやヒアドキュメントを検証に使わない。Git結果を文字証拠へ保存することと新しい検証プログラム追加を混同しない。

### 3. Full originals and D.5 are different operations

tracked `.planning/argonauts/r-d78495de-prd.md`:45,50が今回の正本であり、旧phaseの製品限定判定より優先する。

```markdown
- full工程を維持し、工程原本はGit保存・push・カード添付する。後続がチームD.5の指定ファイル限定手順で最終PRから工程文書を外し、最終全差分を品質が再確認する。本仕様工程ではREADME未編集。
```

工程原本の保存・標準添付は原本保持の工程。後続D.5は最終PRの指定ファイル限定整備。後続品質の再確認は別headに対する最終判定。この3つを個別に扱い、full文書の個別削除、一覧の工程除外、未添付を添付済みと書くことでは代用しない。本mapperはD.5を実行・コマンド推測しない。

## No Analog Found

分類した4ファイルには文書構造のanalogがある。ただし**今回の最終PR整備済み結果**と**D.5実行方法**を証明するanalogは採用していない。旧Phase5はREADME以外の工程変更を許容する別契約だったため、その合格判定を流用できない。後続が公式D.5本文を読み、実際のPR base/headで独立確認する。これは検証基盤不足や新規コード追加の理由ではない。

## Metadata

- Analog search scope: README、tracked Phase5文書、今回のtracked PRD。強い一致が得られた3原本でanalog探索を停止。
- Tracked-source gate: `git ls-files -- README.md .planning/phases/05-readme-verification-a/05-BUILDER-CLI.md .planning/phases/05-readme-verification-a/05-VERIFICATION.md .planning/argonauts/r-d78495de-prd.md` は4pathとも出力。runtime/install mirrorをanalogにしていない。
- Files read for mapping: 必須役割全文、Phase8 CONTEXT/RESEARCH、README、Phase5 BUILDER-CLI/VERIFICATION、今回PRD、指定runtime launcher。analog全文は各1回のみ読取り。
- 初期状態: `.planning/state.json`に既存変更、Phase8の`.gitkeep`・RESEARCH・VALIDATIONは未追跡。これらをmapperの変更とせず、触らない。
- Verification performed here: 公式Phase8判定、tracked gate、基準branch/HEAD存在確認、原本からの抜粋。製品実行・将来PLAN検証・最終PR合格判定は未実施。
- File written by this mapper: `.planning/phases/08-readme-min-count-example/08-PATTERNS.md` のみ。
