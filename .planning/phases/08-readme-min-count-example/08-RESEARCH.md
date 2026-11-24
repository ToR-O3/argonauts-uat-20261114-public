# Phase 8: README min-count example - Research

**Researched:** 2026-11-25 (JST)
**Domain:** READMEへの1例追記、Git文字差分、最終PRの全変更範囲
**Confidence:** MEDIUM（公式Git資料と原本を照合。最終PRのbase/headは後続で確定）

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は08-CONTEXT.md:12-24,43-45の原文転記。

<!-- DATA_m6Q9w2Kb_START -->
### Locked Decisions

## Implementation Decisions (locked)
- **D-01:** README.mdの使い方へ `python -m wordfreq input.txt --min-count 3` を1例だけ追加する（REQ-28、OpenSpec1.1）。既存例・説明・末尾行を保持する。README原本と文字差分で追加1件を確認する。
- **D-02:** 最終PR base...headの全変更一覧はREADME.mdのみ。工程文書も除外せず確認する（REQ-29、OpenSpec2.1）。途中branchには工程原本があるため、整備前の範囲判定は暫定として残る全ファイルを明示し、条件充足と呼ばない。
- **D-03:** full維持。工程原本は保存・commit・push・標準カード添付する。後続PM/最終化はチームD.5の指定ファイル限定手順で最終PRを整備し、品質が最終全差分を再確認する。full文書を個別削除する代用は禁止。PLANと確認記録はPRから外す前に原本添付して保持する。
- **D-04:** 最新判断日時2026-11-25T06:53+09:00。原文「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」旧3形式実行・入力/出力/終了コードの実行証拠作成は依頼者判断により対象外であり、残件/追加要件にしない。
- **D-05:** 実装・試験・ツール・依存・設定・公開入出力を変えない。検証は既存Git CLIと原本読取りを用い、新しい検証スクリプトや製品テストを追加しない。文字差分と全一覧を直接読んで判定し、diff --check成功だけで例の存在・ファイル限定の合格としない。
- **D-06:** 品質が独立にREADME原本と差分を読み、対象base/head・全一覧・2条件の判定をVERIFICATION.mdと文字証拠へ記録し標準添付。最終PR整備後に再確認することを後続へ渡す。PMはread_fileで判断できる形。画像不要は0枚・理由を記す。PMへ画像/圧縮ファイルを開くよう求めない。Builderの自己確認と品質の独立確認、整備前と最終確認を区別する。
- **D-07:** PLANごと最大3tasks。同じ依頼branch argonauts/r-d78495deへ番号順に直列積上げ。各task終了時点に検証コマンドと入力が実在し、独立PLANは他PLAN成果の有無に依存せず検証可能。phase検証は先行PLAN含む同branch全成果を検証する。fails_whenは対象誤動作を失敗と観測する条件。最終限定確認は最終化側の対象PR base/headで実施し、途中phaseで最終合格を偽らない。

### Claude's Discretion
既存CLIによる読取りコマンドと工程記録の最小構成。README以外の製品・新しい試験/ツール変更、3形式実行は裁量外。

### Deferred Ideas (OUT OF SCOPE)
3形式実行と証拠は対象外（将来残件ではない）。実装・品質・受入・最終化sync/archive・README限定PR整備は該当後続カード。過去phase修復なし。
<!-- DATA_m6Q9w2Kb_END -->
</user_constraints>

## Summary

**Primary recommendation:** Builderは既存の使い方コードフェンス内、基本例の直後に指定行を1行だけ追加する。工程検証プログラム・製品試験は新設せず、編集前README原本、編集後原本、Gitの文字差分と全ファイル一覧を直接読む2-task構成を推奨する。[VERIFIED: 08-CONTEXT.md:14-20; .planning/argonauts/r-d78495de-prd.md:39-50]

合格条件は例1件追加と最終PRのREADME限定だけである。3形式でCLIを実行した証拠を作る必要はなく、実施済みとも主張しない。fullの工程原本を保持した途中branchでREQ-29を最終合格にしてはいけない。後続D.5整備後の別headで独立品質が再確認する。[VERIFIED: .planning/REQUIREMENTS.md:108-111; 08-CONTEXT.md:15-20]

研究時点では指定例は未追加。さらにローカルorigin/mainを参考baseにすると、README末尾の過去追記、pyproject.toml、工程文書が全一覧に現れる。これは最終PRの実体を取得した判定ではなく、scopeを隠せないことの事前観測である。研究ではREADMEを編集せず、過去変更も修復しない。[VERIFIED: 本セッションgit diff origin/main...HEAD、git rev-parse、README.md:9-15,35]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 指定例の掲載 | 静的ドキュメント | — | README原本とコードフェンスが責務を持つ |
| 文字差分・範囲確認 | Git / 工程記録 | 独立品質 | 製品ロジックでなく改訂内容を判定する |
| 最終PR限定 | 後続PM/最終化 | 整備後の独立品質 | full原本保存と最終PRからの分離を両立する |

根拠: [VERIFIED: 08-CONTEXT.md:14-20; .planning/argonauts/r-d78495de-prd.md:25-29,41-50]。UI・AI・API・DB・サービス追加の設計は不要。

<phase_requirements>
## Phase Requirements

| ID | Description（REQUIREMENTS.md原文） | Research Support |
|---|---|---|
| REQ-28 | README.mdの使い方へ `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。既存例・説明・末尾行を保持する。原本と文字差分で確認する。 | 既存フェンスの挿入位置、編集前原本、追加1行だけの差分、末尾保持の直接照合 |
| REQ-29 | 最終PR base...headの全変更ファイルがREADME.mdだけである。工程文書をpath除外しない。full工程原本は保存・push・カード添付後、後続D.5指定ファイル限定手順でPRから外す。整備前は暫定として残る工程ファイルを明示し、品質が整備後のbase/head・全一覧・2条件判定をVERIFICATION.md等の文字原本でカード添付する。PMはread_fileで判断する。 | 除外なしの全一覧、固定base/head/merge-base、暫定と最終の判定分離、独立品質への引継ぎ |

[VERIFIED: .planning/REQUIREMENTS.md:108-109]。原文転記であり追加要件ではない。
</phase_requirements>

## Project Constraints (from HERMES.md)

本作業ディレクトリで`HERMES.md`、`.hermes/HERMES.md`、`.hermes/skills/`、`.agents/skills/`をtest -eで確認し、すべてABSENT。プロジェクト固有HERMES指示・skillは読み込む対象がなかった。公式`gsd_run query agent-skills gsd-phase-researcher --skills-only`も空出力だった。[VERIFIED: 本セッションterminal存在確認・公式CLI]

ユーザー指定を適用: ファイル/JSONはread_file、項目抽出は必要ならjq、GSDの判定はsource済みランチャーからgsd_run。インラインPython/Nodeやヒアドキュメントを検証に使わない。研究・計画中は未作成の検証ファイルを試走しない。この研究でcommit/push/Kanban操作はしない。[CITED: 今回の実行依頼]

## Standard Stack

| Tool / material | Observed version | Purpose | Installation |
|---|---|---|---|
| Git | 2.52.0 | 原本blob、文字差分、全変更一覧、対象SHAの読取り | 既存CLIのみ |
| read_file | 現セッション提供 | README・工程文字原本の閲覧 | 不要 |
| GSD公式CLI | バージョン未取得 | Phase8判定・agent-skills・graphify判定 | 指定ランチャーsource後のgsd_runのみ |

Gitバージョンは`git --version`の実出力。公式`query init.phase-op 8`は`phase_found: true`、`phase_number: "08"`、`has_context: true`、`has_research: false`、`has_plans: false`を研究作成前に返した。graphifyは`disabled: true`。有効化や設定変更は行わない。[VERIFIED: 本セッションterminal・公式CLI]

追加ライブラリ、依存インストール、Package Legitimacy Auditは該当なし。jqは既存コマンドが応答したが、この調査に追加JSON処理は不要だった。Step 2.6: SKIPPED (no external service/package dependencies identified); 必要なGitは上記で存在確認済み。[VERIFIED: .planning/argonauts/r-d78495de-prd.md:27; 本セッションterminal]

## Architecture Patterns

### Minimal append inside the existing usage fence

README原本には見出し`## wordfreq の実行`があり、既存の`sh`フェンス内は以下の順序。これらを置換せず基本例の次へ新例を挿入する。[VERIFIED: README.md:5-15]

<!-- DATA_v8Ny4pR2_START -->
```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
python -m wordfreq input.txt --format html > result.html
```
<!-- DATA_v8Ny4pR2_END -->

指定追加行の原文は`python -m wordfreq input.txt --min-count 3`。[VERIFIED: .planning/REQUIREMENTS.md:108]。新たな説明文・空行・フェンスを増やす必要はない。README.md:19-26の既存オプション説明もそのままにする。

### Preserve the existing final line

末尾の独立行は`検証A: v1.12 の通しの確かめ（2026-11-22）`。[VERIFIED: README.md:35]。新例を末尾へ追加してこの行の位置を変えない。原本末尾を読み、追加差分が使い方の1行だけで、末尾変更・削除・改行形式の一括変更・No newline at end of fileの変更がないことを確認する。diffで空白やCRを無視しない。[VERIFIED: 08-CONTEXT.md:14,40; CITED: https://git-scm.com/docs/git-diff]

### Separate three comparison scopes

1. **編集自己確認:** 編集直前の固定SHAと作業ツリーREADMEを比較する。READMEをまだcommitしていなくても検証できる。
2. **整備前のphase確認:** 対象branchの固定base/headで先行PLANを含む全変更を読む。全一覧の各ファイルを隠さず文字証拠に残し、README以外があれば暫定・REQ-29未達とする。
3. **整備後の最終確認:** 最終PR自身のbase/headを再取得・固定して全一覧とREADME差分・原本を独立品質が読み直す。途中headの証拠を流用して合格にしない。

根拠: [VERIFIED: 08-CONTEXT.md:15-20; .planning/REQUIREMENTS.md:109]。Gitの`A...B`はA/Bのmerge-baseからBへの差分であって、単なるA対Bではない。比較起点を記録する。[CITED: https://git-scm.com/docs/git-diff]

## Recommended Plan Shape

単一PLAN・番号順の2tasksを推奨（最大3tasks制約内）。新しい検証スクリプトを作るWave 0は置かない。[VERIFIED: 08-CONTEXT.md:18,20; .planning/argonauts/r-d78495de-prd.md:39-50]

- **Task 1 / OpenSpec1.1 / REQ-28:** 編集前SHA・原本を記録し、README既存フェンスに1行追加。既存Git CLIと原本で自己確認し、実際のdiffを文字記録に残す。入力は既存READMEとGit blobのみ。
- **Task 2 / OpenSpec2.1の整備前部分 / REQ-29:** 同branchの対象base/headと除外なしの全一覧を保存し、暫定判定、残存全ファイル、独立品質・後続最終化への引継ぎをまとめる。最終D.5整備や独立品質そのものをBuilder実施済みにしない。

この分割は提案であり追加の決定事項ではない。工程記録のファイル名はPlannerが定める。各taskの検証はその時点で存在するREADMEとGit objectだけから実行可能にし、将来のVERIFICATION.md等をコマンド入力に要求しない。最終PRの検証はその対象が成立する後続側の責務と明示する。[VERIFIED: 08-CONTEXT.md:19-20]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| 例が追加されたか | 新規検証スクリプト、正規表現テスト | 原本とGit patchの読取り | D-05の禁止を守り、既存内容の書換えも見える |
| ファイル限定 | 製品pathだけのallowlist検査 | path除外なしのGit全一覧 | 工程文書・設定の混入を隠さない |
| 実行例の保証 | 3形式のCLIハーネス・入力fixture | 指定文字列1行の直接確認 | 実行検証は失効した対象外条件 |
| fullと最終PRの分離 | full文書の個別削除・除外付き一覧 | 後続D.5手順と整備後再確認 | 原本保持と最終限定を区別できる |

根拠: [VERIFIED: 08-CONTEXT.md:15-20; .planning/argonauts/r-d78495de-prd.md:45-50]

## Validation Architecture

### Framework and boundaries

| Property | Value |
|---|---|
| Framework | 既存Git CLI + 原本文字の直接レビュー。新しいテストフレームワークなし |
| Config | `.planning/config.json`の`"nyquist_validation": true` |
| Quick run | `git --no-pager diff --no-ext-diff --no-textconv --unified=40 HEAD -- README.md`（編集中かつHEADが編集前のとき）とread_fileによるREADME全読取り |
| Full phase run | 対象base/headを固定した全一覧・README差分・両原本の読取り。下記手順 |
| Supplement | `git diff --check`は空白エラー確認のみ。これだけでREQ-28/29を合格にしない |

[VERIFIED: .planning/config.json:21-25; 08-CONTEXT.md:18-20; CITED: https://git-scm.com/docs/git-diff]

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Existing command / direct review | Input exists? |
|---|---|---|---|---|
| REQ-28 | 指定例1件の追加・既存本文/末尾保持 | document/manual-assisted | 編集前SHA対作業ツリーの`git diff`、`read_file README.md`。commit後は固定前後SHAで同じ比較 | READMEと編集前blobが既存。新script不要 |
| REQ-29 / 整備前 | 全変更を隠さず列挙・暫定扱い | scope/manual-assisted | `git diff --name-status "${BASE}...${HEAD_SHA}"`と`--name-only`。path指定なし | base/head object存在を事前確認。PR未確定なら参考比較と明記 |
| REQ-29 / 最終 | 最終PRの全変更がREADMEだけ | final scope/manual-assisted | 最終PRの固定base/headで同じ全一覧、README原本と差分を品質が再読取り | 最終PRは後続で確定。今のheadで代替しない |

根拠: [VERIFIED: .planning/REQUIREMENTS.md:108-111; 08-CONTEXT.md:18-20]。Gitの表示コマンドは、内容不適合でも表示自体に成功すればexit 0になり得る。内容の合否は直接読み取って明示する。[CITED: https://git-scm.com/docs/git-diff]

### Concrete command pattern (Builder / quality)

以下のBASE/HEAD_SHAは最終PRで実在する対象SHAに設定する変数であり、現在値の推測ではない。EDIT_BASEはBuilderがREADME編集直前に取得・固定する。Plannerは検証入力と取得段階をタスクに書く。研究段階では将来入力へのコマンドを試走しない。

```sh
# 編集直前（取得したSHAを文字原本へ保存）
EDIT_BASE=$(git rev-parse HEAD)
git --no-pager show "${EDIT_BASE}:README.md"

# 編集後、commit前。read_fileでREADME.mdも全文読む。
git --no-pager diff --no-ext-diff --no-textconv --unified=40 "$EDIT_BASE" -- README.md
git diff --numstat "$EDIT_BASE" -- README.md
git diff --check "$EDIT_BASE" -- README.md

# 整備前/後共通。BASE・HEAD_SHAは対象PR/branchで確認済みの完全SHA。
git rev-parse --verify "${BASE}^{commit}"
git rev-parse --verify "${HEAD_SHA}^{commit}"
git merge-base "$BASE" "$HEAD_SHA"
git --no-pager diff --no-ext-diff --no-textconv --no-relative --name-status "${BASE}...${HEAD_SHA}"
git --no-pager diff --no-ext-diff --no-textconv --no-relative --name-only "${BASE}...${HEAD_SHA}"
git --no-pager diff --no-ext-diff --no-textconv --unified=40 "${BASE}...${HEAD_SHA}" -- README.md
git diff --check "${BASE}...${HEAD_SHA}"
git --no-pager show "${HEAD_SHA}:README.md"
MERGE_BASE=$(git merge-base "$BASE" "$HEAD_SHA")
git --no-pager show "${MERGE_BASE}:README.md"

# 作業ツリーに未記録変更がないかを別途確認（PR差分そのものとは別）
git status --short
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
```

Gitのblob読取りと三点差分は公式資料の書式による。[CITED: https://git-scm.com/docs/git-show; https://git-scm.com/docs/git-diff]。比較文字原本をファイルへ保存する場合はツール出力または既存CLIのリダイレクトで保存しread_fileで開く。存在しない検証スクリプトや他PLANの将来成果を実行しない。原本ファイルの名前・配置はPlannerが決める。

**判定:** 編集直前対編集後のREADME差分は指定行の追加だけ（numstatは1追加/0削除が目安）であること。numstatだけでは内容を証明しない。最終PRには過去の末尾追記などが同じREADME内に含まれる可能性があるので、編集局所の1行追加とPR全体の差分を分け、過去行を消して無理にPRの1追加へ整えない。最終PRでも指定例1件と既存内容保持を原本で確認する。[VERIFIED: README.md:35; 08-CONTEXT.md:14-15,40; 本セッションorigin/main...HEAD差分]

### fails_when: what must be observed as failure

| Check | Failure observation | Result to record |
|---|---|---|
| 指定例 | 指定行がない、複数追加、値/引数違い、フェンス外だけに追加 | REQ-28 fail。表示コマンドexit 0でもfail |
| 既存本文 | 既存例を置換、説明を変更、不要空行・改行形式全体変更、末尾行欠落/後続追記 | REQ-28 fail。原本と全patchを示す |
| 全変更一覧 | README以外が1つでもある。工程文書も含む | 整備前はREQ-29未達/暫定、整備後ならfail |
| 空差分 | 全一覧が空、READMEに今回の例追加がない | 「READMEだけ」と誤認せずfail |
| 比較対象 | SHA不存在、PR対象と異なるbase/head、merge-base取得失敗、出力省略 | 検証不能。合格扱いしない |
| 証拠 | 全一覧から工程pathを除外、途中headを最終と呼ぶ、自己確認を独立品質と呼ぶ | 判定無効・再確認必要 |

根拠: [VERIFIED: 08-CONTEXT.md:14-20,40; .planning/REQUIREMENTS.md:108-109]。意図的に製品を壊すmutationや検証用ファイル新設は計画しない。欠落状態を自然な事前fail観測にできる。

### Actual observations before implementation

研究時のHEADは`bb8726174f9796493f836ca139e264121186763f`、branchは`wt/t_19c23e10`。`git diff --exit-code HEAD -- README.md`はexit 0で差分なし、README.md:9-15に指定例はない。`git diff --check`もexit 0だった。したがって**REQ-28は未実装**であり、diff --check成功は例追加を証明しない。[VERIFIED: 本セッションterminal; README.md:9-15]

参考baseのローカル`origin/main`は`c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`、merge-baseも同じ。`origin/argonauts/r-d78495de`は`7e70a55e424feb94031207ee24f844046d9228da`。fetch/PR照会は行っておらず、いずれも最終PRの新鮮な対象SHAと認定しない。[VERIFIED: 本セッションgit rev-parse・merge-base]

参考`origin/main...HEAD`全一覧には`.planning/`、`_bmad-output/`、`openspec/`配下に加えて`README.md`と`pyproject.toml`が現れた。READMEの参考差分は既存末尾の`検証A: v1.12 の通しの確かめ（2026-11-22）`追加であり、今回の指定例ではない。**この参考比較でREQ-29は未達**。過去設定変更や工程混入を本phaseで修復する権限はない。Builder/品質は自分の確認時点の全一覧を省略せず別文字原本へ保存して後続へ渡す。[VERIFIED: 本セッションgit diff --name-status origin/main...HEAD・README差分; 08-CONTEXT.md:9,15-20]

初期作業ツリーには既存の`.planning/state.json`変更とPhase8の未追跡`.gitkeep`があった。研究はこれらを変更・削除せず引き継ぐ。[VERIFIED: 本セッション初期git status --short]

### Sampling and evidence ownership

- Task 1終了: 編集局所のREADME原本・全patch・既存末尾・追加1件をBuilderが確認。
- Task 2/phase終了: 同branchの全成果を含む固定base/headで全一覧を採取。README以外が残るなら残存全ファイルを文字原本に列挙して暫定と記す。
- 独立品質: Builder出力の転載だけでなく、自身が対象headから原本・差分・全一覧を取得し、VERIFICATION.mdと文字証拠へ2条件を別々に判定する。
- 後続最終化: full原本を保存・push・標準添付後にD.5指定ファイル限定整備。品質が新しい最終PR base/headで再確認し、PMがread_fileで原本を読む。
- 画像は0枚、理由は「README原本と文字差分による文書変更検証でUI変更なし」。CLI3形式の入力/出力/終了コード証拠は作らず、残件にも載せない。

根拠: [VERIFIED: 08-CONTEXT.md:16-20; .planning/argonauts/r-d78495de-prd.md:45-50]

### Wave 0 Gaps

**新規テスト・検証ファイル・フレームワークの整備は不要かつ提案禁止。** 既存GitとREADME原本で今回の2条件を直接観測できる。未確定なのは後続最終PRの対象base/headとD.5整備後の状態であり、検証基盤の不足ではない。[VERIFIED: 08-CONTEXT.md:18-20; .planning/REQUIREMENTS.md:109-111]

## Common Pitfalls

1. **成功exitへの依存:** diff表示やdiff --checkが成功しても、指定例がない・ファイル混入のままになり得る。内容判定を記録する。[CITED: Git diff公式資料; VERIFIED: 上記事前観測]
2. **全一覧のpath絞込み:** `-- README.md`は本文確認だけに使い、ファイル限定確認には使わない。工程文書の除外・grepでの隠蔽もしない。[VERIFIED: 08-CONTEXT.md:15,18]
3. **HEAD相対比較の取り違え:** READMEをcommitした後に`git diff HEAD -- README.md`だけ読むと今回変更が消える。固定EDIT_BASEと実際の対象headに切り替える。[CITED: https://git-scm.com/docs/git-diff]
4. **旧条件復活:** 既存HTML/pytestツールの存在を理由に3形式実行を追加しない。過去phaseの試験ハーネスを再利用しない。[VERIFIED: 08-CONTEXT.md:9,17-18]
5. **過去末尾追記の破壊:** 最終PRのdiff行数を1へ合わせるため既存末尾を削除しない。今回局所差分とPR全体を分けて記録する。[VERIFIED: README.md:35; 08-CONTEXT.md:14,40]
6. **full文書削除での代用:** D.5整備を研究/Builderの個別削除で前倒ししない。REQ-29未達を正直に引き継ぐ。[VERIFIED: 08-CONTEXT.md:15-16,20]

## Code Examples

製品コードの例・実装変更は不要。追加するのは次のREADME差分だけ。これは実施済みdiffではなくPlanner/Builder向けの期待形である。[VERIFIED: README.md:9-11; .planning/REQUIREMENTS.md:108]

```diff
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
```

文字検証の実行例はValidation Architectureに集約した。READMEに実行例を掲載することと、その実CLIを実行して成功を認定することを混同しない。[VERIFIED: .planning/argonauts/r-d78495de-prd.md:10-11,34]

## State of the Art

| Superseded | Current locked approach | Effect |
|---|---|---|
| 3形式実行・入出力/終了コード証拠を要求 | 2026-11-25T06:53+09:00判断の2条件だけ | 旧実行証拠を未完了にしない |
| 工程を除いた製品一覧だけで限定判定 | 最終PR base...headの全変更一覧 | 工程を含めREADME以外は未達 |

[VERIFIED: .planning/argonauts/r-d78495de-prd.md:31-34,45-50; 08-CONTEXT.md:15,17-18]

## Security Domain

`"security_enforcement": true`と`"security_asvs_level": 1`を確認した。設定は変更しない。[VERIFIED: .planning/config.json:49-51]

| ASVS category | Applies to this phase? | Reason / control |
|---|---|---|
| V2 Authentication | no new surface | 文書掲載のみ、認証変更なし |
| V3 Session Management | no new surface | セッション処理なし |
| V4 Access Control | no new surface | 権限制御変更なし |
| V5 Input Validation | no new runtime surface | README以外の公開入出力・検証ロジック変更禁止 |
| V6 Cryptography | no new surface | 暗号処理・依存追加なし |

根拠: [VERIFIED: .planning/argonauts/r-d78495de-prd.md:17-27; 08-CONTEXT.md:9,18]。該当する工程リスクは差分隠蔽/証拠の対象違い（Tampering/Repudiation）で、全一覧・固定SHA・独立品質の文字原本を対策とする。製品セキュリティの再設計や新サービス導入は行わない。

## Assumptions Log

| # | Claim | Risk / disposition |
|---|---|---|
| — | 未確認の技術仕様をlocked decisionとして追加しない | 追加package/実行結果の推測なし |

最終PRのbase/headは未確定値として扱い、架空値やorigin/mainの参考SHAで代用しない。GSDのconfidence seamは`curated --verified`、`official --verified`、`webfetch --verified`にLOW、計画された`jina --verified`にはMEDIUMを返した。jina専用fetchツールはこの環境になく、実取得はweb_extractの公式Git資料。provider由来のHIGHを主張しない。ローカル原本に関する事実は行番号または実CLI出力を出典として区別した。[VERIFIED: 本セッション公式CLI・web_extract]

## Open Questions / Handoff

- 実装方針の未決事項なし。最終PRのbase/head、D.5整備後head、残存全ファイルの消失確認は後続で取得する対象。現時点で最終合格は出せない。[VERIFIED: 08-CONTEXT.md:15-20]
- D.5の破壊的な整備コマンドはこの研究で推測・定義しない。後続が当該公式チーム手順を読み、保存・添付後に適用する。[VERIFIED: 08-CONTEXT.md:16]
- STATEのcurrent focusがPhase7でも過去phaseを修復しない。公式init.phase-op 8とROADMAPのPhase8を今回の対象とする。[VERIFIED: .planning/STATE.md:29,96; .planning/ROADMAP.md:156-169; 本セッション公式CLI]

## Sources

### Local authoritative sources (opened this session)

- `08-CONTEXT.md:12-24,39-45` — locked decisions・裁量・対象外。
- `.planning/REQUIREMENTS.md:104-116` — REQ-28/29原文と対象外。
- `.planning/argonauts/r-d78495de-prd.md:5-34,37-51` — 承認proposal/tasks・最新判断。
- `openspec/changes/r-d78495de-readme-min-count/design.md:7-24` — 文字検証とfull原本保持。
- `README.md:5-26,28-35` — 使い方フェンス・既存説明・末尾行。
- `.planning/config.json:21-25,49-51,63-64` — Nyquist/security・追加skills設定。
- `.planning/STATE.md:29,94-104`、`.planning/ROADMAP.md:156-169` — Phase8登録と過去phaseとの分離。
- 本セッションの公式`query init.phase-op 8`、`query agent-skills ... --skills-only`、`graphify status`、`query research-plan`、`query classify-confidence`とGit出力。

### Official documentation (retrieved this session)

- https://git-scm.com/docs/git-diff — 三点比較、path指定、patch表示、変更状態。取得内容をローカルCLIの読取りと照合。
- https://git-scm.com/docs/git-show — commit内blobの原本取得。

### Metadata

- 研究日: 2026-11-25。最終PRに対する有効期限は日時ではなくbase/head変更時点。対象SHAが変わったら全一覧・原本・差分を再確認する。
- Stack / architecture / pitfalls: MEDIUM。外部資料は公式Git文書、ローカル変更対象は直接読取り。最終PR状態だけは未確認。
- この研究でREADME、製品実装、試験、ツール、依存、設定は編集していない。研究原本のみを新規保存し、commit/push/Kanban操作は行っていない。
