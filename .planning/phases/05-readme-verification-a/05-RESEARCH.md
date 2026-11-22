# Phase 05: README verification A - Research

**Researched:** 2026-11-22
**Domain:** README末尾の最小追記・既存CLIによるバイト比較・依頼全差分の分類
**Confidence:** LOW（公式classify-confidenceが本調査のproviderに返した値。一次資料と実環境で確認した事項、未実行の提案コマンドを下記で区別する）

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** README.mdに `検証A: v1.12 の通しの確かめ（2026-11-22）` を独立した最後の1行として追加。かぎ括弧、句点、余分な前後文字なし（REQ-22）。
- **D-02:** 指定行の後に空行・別文言なし。既存行へ連結しない。既存内容・順序・改行形式を保持し、削除・書換え・不要空行を加えない（REQ-23）。変更前の末尾・改行を確認して記録する。
- **D-03:** 既存CLIで文字列完全一致・末尾位置・README全差分を確認し、新旧コード・試験ファイルは一切変更しない。新規検証スクリプトも作らない（OpenSpec1.1）。
- **D-04:** 依頼全体の全ファイル差分を確認し、工程仕様・計画・検証文書を別分類。利用者向け変更がREADME当該1行のみであり、コード・試験不変であることをCLI結果とともに文字の検証記録へ保存する（REQ-24、OpenSpec2.1）。
- **D-05:** 文言掲載は通し検証の実施・合格を認定しない。API・認証・権限・データ・外部送信・費用変更なし。別件の句点追加を混ぜない。
- **D-06:** 品質が対象headで独立に再確認しVERIFICATION.mdとCLI証拠文書を標準添付する。PMはread_fileで判定できる形。画像が不要なら0枚・理由を書く。画像があれば品質自身の実閲覧枚数・確認内容・結果を文字に記録し、PMに画像・圧縮物を開くことを求めない。
- **D-07:** 各PLAN最大3tasks、同じ依頼branch argonauts/r-8ac79dafへ番号順に直列で積む。task終了時の検証入力はその時点で実在し、独立PLANは他PLANの成果の有無に依存しない。phase検証は先行PLAN含む全成果がある同branchで行う。fails_whenは対象の誤動作が既存CLIで失敗として観測される条件にする。

### Claude's Discretion
既存CLIを使う実行可能な確認の組み合わせ、工程文書の詳細とPLAN分割。コード・試験・補助スクリプト追加は裁量に含めない。承認された既存検証方法をそのまま使い、確認のためのインラインコードを作らない。

### Deferred Ideas (OUT OF SCOPE)
コード/試験/CI/依存/画面/新サービス、別件句点追加、過去phase修復。READMEの実装、品質、受入、sync/archiveは該当する後工程。
</user_constraints>

出典: [VERIFIED: .planning/phases/05-readme-verification-a/05-CONTEXT.md:13-45]。追加の実行制約: ファイル・JSONはread_file、項目抽出は利用可能ならjq、GSD判定は公式CLI。計画中に未作成検証ファイルを実行しない。インラインのPython/Node/シェルスクリプト、ヒアドキュメント、新規補助スクリプトは禁止。今回は保存のみでcommit/push/Kanban操作なし。[VERIFIED: 今回の依頼本文]

## Summary

実装はREADMEへの指定1行の追記だけである。承認済みdesignは「既存末尾が改行済みならその直後に指定行と末尾改行を追記」「通常の末尾改行は許容する」を明記している。現在のREADMEはUTF-8、34行・4643バイト、Gitのindex/worktreeともLF、最終バイトは`0a`である。したがって今回は空行も先頭側の追加改行も不要で、既存4643バイトの直後に指定文字列とLFを置く。[VERIFIED: openspec/changes/r-8ac79daf-readme-verification-a/design.md:13-17; README.md:1-34; CLI read-only調査: file / wc / git ls-files --eol / tail -c 32 | od]

検証を「最終行の完全一致」「既存prefixの全バイト一致」「残りのsuffixが指定行+LFだけ」「README全差分」「依頼全体のファイル分類」に分ける。`cmp`のprefix比較とskip比較を組み合わせれば、期待ファイルや試験コードを作らず、既存CLIのパイプだけで誤りを非ゼロ終了として検出する設計にできる。後掲はPLANへ渡す提案であり、この調査では追記・提案検証の試行・成功判定を行っていない。[VERIFIED: CLI cmp --help; CITED: https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html]

**Primary recommendation:** 1 PLAN・最大3 tasksに、事前末尾記録→最小追記と内容検証→全差分分類・文字証拠の保存を置く。新規検証ファイル、pytest、browser、依存導入は使わない。品質の対象head独立再確認は後工程として明示する。[VERIFIED: 05-CONTEXT.md:15-24; openspec/changes/r-8ac79daf-readme-verification-a/tasks.md:3-13]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 指定文言の掲載 | 静的文書 | — | 実行時のwordfreq機能を変更しない |
| 完全一致・既存バイト保持 | ローカル既存CLI | Git baseline | 既存文書と指定suffixを別々に比較する |
| 全差分分類と受入証拠 | 工程文書 / 独立品質 | Git対象head | 利用者向け差分と工程成果物を区別する |

[VERIFIED: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:3-32; 05-CONTEXT.md:17-21]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| REQ-22 | README.mdの独立した最終行に `検証A: v1.12 の通しの確かめ（2026-11-22）` を完全一致で追加する。かぎ括弧・追加句点・余分な前後文字・後続空行や別文言なし。 | 最終行の固定文字列全行一致とsuffix全バイト一致 |
| REQ-23 | 既存README内容・順序・改行形式を保持し、差分は指定行の末尾追記のみ。削除・書換え・不要空行追加なし。 | LF/末尾LFの実測、prefixのcmp、README全patch確認 |
| REQ-24 | 利用者向け変更はREADMEの当該1行のみ。コードと試験ファイルを変更せず、工程の仕様・計画・検証文書を全差分から別分類し、既存CLIの結果を検証記録に残す。指定文字列の掲載を通し検証の実施・合格認定と混同しない。 | 依頼開始前baselineからの全差分、未追跡一覧、工程文書の個別読取り、対象head独立再確認 |

[VERIFIED: .planning/REQUIREMENTS.md:74-86]
</phase_requirements>

## Project Constraints and Current State

- rootの`HERMES.md`はファイル探索で発見されず、`.hermes/`と`.agents/`の探索もPath not found。公式`query agent-skills gsd-phase-researcher --skills-only`は空出力で、追加skill指示は得られなかった。設定の`"claude_md_path": "./.hermes/HERMES.md"`は存在証明ではない。[VERIFIED: discovery結果; .planning/config.json:63-68]
- 公式`query init.phase-op 5`は`phase_found: true`、`phase_number: "05"`、`has_context: true`、`has_research: false`、`has_plans: false`を返した。graphifyはdisabled。設定の`"nyquist_validation": true`と`"security_enforcement": true`に従い対応sectionを含める。[VERIFIED: official CLI outputs; .planning/config.json:21-53]
- STATE.mdの`current_phase: 4`、`status: completed`はPhase 5不存在の根拠にしない。ROADMAPの`Phase 5: README verification A`、`REQ-22, REQ-23, REQ-24`と公式initが今回の対象を示す。過去phaseのstale検証・CI・browser要件を今回へ転用しない。[VERIFIED: .planning/STATE.md:1-16,89-95; .planning/ROADMAP.md:122-136]
- 調査時HEADは`54106df87baa6cc017167eb311fd0fd4f81ea0fa`、作業branchは`wt/t_8a90bad6`。要求された積み先は`argonauts/r-8ac79daf`であり、worktree名をそのまま依頼branchと報告しない。本調査でbranch操作は行わない。[VERIFIED: git rev-parse HEAD / git branch --show-current; 05-CONTEXT.md:21]
- 調査開始時点で`.planning/state.json`の変更、`.planning/argonauts/t_8a90bad6-init-plan.json`、`.planning/argonauts/t_8a90bad6-plan-pre.json`、phase `.gitkeep`が既に存在した。既存作業を自分の変更と報告したり、削除・巻戻し・自動stageしたりしない。[VERIFIED: git status --porcelain=v1 --untracked-files=all]

## Standard Stack

| Existing tool | Observed version | Purpose |
|---|---|---|
| Git | 2.52.0 | baseline、対象head、全patch、パス一覧、改行属性 |
| GNU cmp | diffutils 3.10 | prefixとsuffixのバイト一致・不一致終了値 |
| tail / head / od | coreutils 9.5 | 最終行、末尾バイト、改行の観測。headは必須ではない |
| GNU grep | 3.11 | `-F`固定文字列・`-x`全行一致 |
| wc / printf | インストール済み（個別version未採取） | バイト/行数の観測・指定suffixを標準入力へ供給 |
| jq | PATH上にあり、version出力は`jq-` | 必要なJSON項目抽出のみ。README検証には不要 |
| 公式gsd-tools.cjs | 本profileの既存CLI | phase init / agent skills / confidence / graph status |

[VERIFIED: command -v / 各--version / CLI調査結果]

**Installation:** なし。外部package追加なしのためPackage Legitimacy Auditは対象外。既存CLIオプションはローカル`--help`とGNU/Git公式資料で照合した。フレームワーク/API採用調査ではなく、新しい依存・研究用基盤を導入しない。[VERIFIED: 05-CONTEXT.md:10,17,24; CLI help; CITED: https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html]

## Architecture Patterns

### Flow

承認文字列 + 変更前README → 末尾/LFを記録 → 既存バイトへ指定行+LFだけ追記 → 最終行/prefix/suffixを照合 → README全patch + 依頼全patchを確認 → 製品/工程を分類 → 対象headの独立品質 → PMが文字証拠を読む。

[VERIFIED: approved tasks.md:3-13; 05-CONTEXT.md:15-21]

### Baselineを二つ区別する

1. **製品変更前README baseline:** 今回調査時HEAD `54106df87baa6cc017167eb311fd0fd4f81ea0fa`。READMEはこのHEADに対して未変更。既存prefixは4643バイト、34 LF行。
2. **依頼全体baseline:** initiative開始commit `b95d7b8`の親としてGitが解決した`c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`。この範囲の差分には既にBrief/PRD/OpenSpec/GSD工程文書が含まれる。今回のHEADだけから比較するとそれらが漏れる。

上記二点はgit log / git show --stat / git rev-parse / git diff --name-statusの読取り結果に基づく候補である。調査時に依頼全体baselineからHEADへのREADME差分はなかった。Builderは開始時に同一履歴・READMEサイズ・未変更状態を再確認し、別内容へ進んでいたら数値を無条件に流用せず停止して計画を補正する。品質も同じ固定baselineを使い、可動なHEADを比較元にしない。[VERIFIED: CLI git log -8 / git show --stat b95d7b8 / git rev-parse b95d7b8^ / git diff --quiet / wc]

### Planner向け分割

1 PLANに3 tasks以下を推奨する。task 1は変更前の文書/改行/HEAD記録、task 2は追記とREQ-22/23検証、task 3はREQ-24の全差分分類と文字証拠保存。task 1で未来の証拠文書の存在を検証しない。task 2のCLIは既存READMEとGit blobのみを入力にする。task 3はそのtask内で作成済みの検証文書をread_fileで読む。分割するなら後続依存を明示し、独立PLANを装わない。[VERIFIED: 05-CONTEXT.md:21-24; approved tasks.md:3-9]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---|---|---|
| 指定行完全一致 | Python/Nodeのインラインassert、新しい試験 | `tail` + `grep -Fx` / `cmp` |
| 既存内容保持 | Markdown再生成、全体置換、改行正規化 | 既存byteのprefix比較 |
| suffixの検証 | 新規期待ファイル・検証スクリプト | `printf`の標準出力と`cmp`のskip比較 |
| 全差分判定 | statusだけの合格、pytest/browser流用 | Git全patch・未追跡一覧と工程文書の読取り |

[VERIFIED: 05-CONTEXT.md:15-24,40-45; approved design.md:13-23; CLI help]

## Code Examples — PLAN用の既存CLI候補

**実行境界:** 以下は新規コード/スクリプトではなく既存CLIのコマンド列。調査では実行していない。実装・品質で実在するREADMEと既存Git blobに対して実行し、各コマンドのstdout/stderr/exitを保存する。パイプは実行環境のpipefailを有効にして上流エラーも拒否し、最後の成功コマンドで前の失敗を上書きしない。`python3 -c`、`node -e`、`sh -c`、`bash -lc`、ヒアドキュメント、補助ファイルは不要。[VERIFIED: 今回の依頼; CLI grep/tail/cmp help]

### C1: 独立した最終行の完全一致（追記後）

```text
tail -n 1 README.md | grep -Fx -- '検証A: v1.12 の通しの確かめ（2026-11-22）'
```

`grep -F`は正規表現ではなく固定文字列、`-x`は全行一致。句点・前後文字・既存行への連結・後続空行/文言では一致せずexit 1となる。入力エラーも不合格とする。最終LF自体の有無はこの検査単独では保証しないためC3を併用する。[VERIFIED: grep --help; tail --help; CITED: https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html]

指定literalの出典: `検証A: v1.12 の通しの確かめ（2026-11-22）`。[VERIFIED: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:11-16]

### C2: 既存prefixの全バイト不変

```text
git show 54106df87baa6cc017167eb311fd0fd4f81ea0fa:README.md | cmp -n 4643 - README.md
```

4643バイトまでを比較する。既存部分の削除・改変・並替え・LF/CRLF変換は非ゼロとなる。prefixだけなら余計な追記を拒否できないためC3も必須。[VERIFIED: CLI wc / git status / cmp --help; CITED: https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html]

### C3: 既存prefix後が指定行+LFだけ

```text
printf '%s\n' '検証A: v1.12 の通しの確かめ（2026-11-22）' | cmp -i 0:4643 - README.md
```

`-i 0:4643`で標準入力はskipなし、READMEは既存4643バイトをskipして、残り全体を比較する。空行追加、重複行、句点、余分な末尾バイト、末尾LF欠落、CRLF化はいずれも不一致になる設計。cmpは一致0・差分1・エラー2であり、1と2はどちらも不合格と記録する。C2+C3で全体を分割して検証する。[VERIFIED: cmp --help; approved design.md:15-17; CITED: https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html]

### C4: README全patchと行数差分

```text
git diff --no-ext-diff --no-textconv --no-color --unified=3 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
git diff --numstat 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
git diff --check 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
```

期待は指定行の追加1・削除0で、末尾以外のhunkやmode変更がないことを全patchで読む。普通のdiff表示は差分があっても成功し得るため、表示コマンドのexit 0を内容の合格にしない。`--check`も単独では文字列・変更範囲を判定しない。[CITED: https://git-scm.com/docs/git-diff; VERIFIED: approved tasks.md:5]

### C5: 依頼全体と禁止範囲

```text
git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD
git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD
git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 --
git status --porcelain=v1 --untracked-files=all
git ls-files --others --exclude-standard
git diff --exit-code c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- wordfreq tests tools pyproject.toml .github
```

commit済み依頼差分と、index/作業木を含む現在差分を分けて記録する。最後のコマンドは既知のコード・試験・ツール・依存・CI範囲への変更をexit 1で拒否するが、全パスの証明ではない。未追跡ファイルはgit diffに含まれないので一覧の各ファイルもread_fileで分類し、未知の製品ファイル・新しい検証コードは不合格とする。工程ディレクトリ配下だから自動許可、という扱いにしない。[CITED: https://git-scm.com/docs/git-diff; VERIFIED: 05-CONTEXT.md:18,24,40-45; CLI git status]

確認対象の既存コードパス`wordfreq`、`tests`、`tools`、`pyproject.toml`は今回のファイル探索で実在を観測した。`.github`は予防的な禁止範囲であり、存在確認した検証入力ではない。これらをpytest等の実行パスに転用しない。[VERIFIED: repository file discovery; ASSUMED: .githubはCI一般の監視候補であり存在未確認]

### C6: 品質対象headとREADME入力の一致

```text
git rev-parse HEAD
git show HEAD:README.md | cmp - README.md
```

対象headを文字証拠へ固定し、作業木のREADMEで別headの合格を主張しない。品質はC1〜C5を自身で再実行し、報告直前に対象headを再照合する。工程文書を後から追加する場合、製品検証headと証拠文書headを区別して記録する。[VERIFIED: 05-CONTEXT.md:20; .planning/argonauts/r-8ac79daf-learnings.md:18-31; CITED: GNU cmp manual]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | 既存Git/GNU CLI。新規試験frameworkなし |
| Config file | 新設なし。workflow.nyquist_validation=true |
| Quick run command | C1 + C2 + C3の各終了値を確認 |
| Full suite command | C1〜C6と全変更ファイルの内容分類・文字証拠読取り |
| Execution status | このresearchでは未実行。Builder・品質で実行する |

[VERIFIED: .planning/config.json:21-25; 05-CONTEXT.md:17-24]

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|---|---|---|---|---|
| REQ-22 | 指定最終行完全一致 | CLI content | C1、C3 | README.mdと既存CLIあり。追記前なので合格は未検証 |
| REQ-23 | 既存全バイト・改行不変、追記1行のみ | byte comparison + patch review | C2、C3、C4 | README.mdと固定Git blobあり |
| REQ-24 | README以外の製品不変・工程別分類 | scope review + CLI guard | C5、C6、全パス内容をread_file | Git履歴とREADMEあり。証拠文書は後続taskで作成 |

fails_whenは「grepが一致を選べずexit 1」「cmpで差分exit 1/読取等エラーexit 2」「禁止範囲git diff --exit-codeが非ゼロ」「全差分に許可外の製品ファイルがある」とする。レビューが必要な分類を単なる表示コマンドの成功で自動合格にしない。[VERIFIED: CLI help; 05-CONTEXT.md:21,40-41]

### Sampling Rate

- 追記task完了時: C1〜C4。基底とバイト数をその場で再確認し、誤った前提なら停止する。
- 工程文書作成task完了時: C5で工程成果を含む全変更を分類して、保存済み証拠をread_fileで読む。
- Phase gate: 同一依頼branch上の全成果を対象に品質がC1〜C6を独立再実行し、VERIFICATION.mdとCLI証拠文書を標準添付する。

[VERIFIED: 05-CONTEXT.md:18-24]

### Wave 0 Gaps

新規テスト、fixture、framework、スクリプトは作らない。承認仕様が既存CLI検証を要求しているため、検証ファイル不足を新規コード追加で埋めるWave 0は不要。必要なのは後続taskが作る文字の証拠文書だけであり、それを実行可能スクリプトとして扱わない。[VERIFIED: approved design.md:9-17; 05-CONTEXT.md:17-24]

### Evidence Contract

Plannerが証拠名を確定した: Builderは .planning/phases/05-readme-verification-a/05-BUILDER-CLI.md と 05-QUALITY-HANDOFF.md、後工程の品質は同directoryの 05-VERIFICATION.md と 05-QUALITY-CLI.md を作る。未作成パスを既存と主張しない。最低限、変更前HEAD/依頼baseline、README byte/line/EOL/末尾記録、対象head、各CLIの完全なargv・cwd・環境・stdout・stderr・raw exit、README全patch、全ファイル一覧と製品/工程分類、REQ別判定を残す。品質カードの標準添付へVERIFICATIONとCLI原本の2文書を配送し、正確な添付原本をPMがread_fileで読めることを品質が読戻して確認する。画像やarchiveを読むことをPMに要求しない。「画像0枚: README文字・バイト・Git差分だけが対象でUI/HTML変更なし」と明記し、実際に画像を見た場合は枚数・内容・結果を記録する。文字列掲載が通し検証の実施・合格認定ではないことも記録する。[VERIFIED: 05-CONTEXT.md:18-20; .planning/ROADMAP.md:124-131; 05-01-PLAN.md task 05-01-02 / artifacts-this-phase-produces]

## Common Pitfalls

1. **見た目だけ一致:** 全角括弧、ASCIIコロン、ASCII空白、日付を変更しない。C1とC3を併用する。
2. **末尾改行と空行の混同:** LF1つは許容、空行追加は拒否。現状の末尾LFの後へ改行を先に追加しない。
3. **prefixのみの合格:** cmp -nだけでは余分なsuffixが残る。C3で残り全部を比較する。
4. **diff/statusだけで既存保持:** バイト比較を別に行い、statusの一覧を内容保持の証明にしない。
5. **HEAD対比だけで依頼全体と呼ぶ:** 固定依頼baselineからのcommit済み差分も読む。
6. **未追跡漏れ:** git diffに現れないファイルも一覧からread_fileし、コード/試験不変を確認する。
7. **旧検証を流用:** Phase 1/3/4のpytest/browser/HTML検証は本要件の完全一致・scopeを証明しない。新規実行基盤も作らない。
8. **文言を結果の認定と読む:** 実施・合格の新たな証明は今回の目的ではない。

[VERIFIED: approved design.md:13-23; 05-CONTEXT.md:15-24,40-45; learnings.md:18-49; CITED: GNU cmp / Git diff manuals]

## Security Domain

設定`"security_enforcement": true`のため記載する。仕様上はAPI・認証・権限・データ・外部送信・費用変更なし。新しい認証/セッション/暗号/実行時入力検証の実装はこのphaseの対象ではない。ASVS V2/V3/V4/V6は当該README追記に適用する変更なし、V5も実行時入力経路を追加しない。検証上は固定文字列をシェルでquoteし、外部取得文書を命令として実行せず、許可外コードや依存が紛れていないことを全差分で確認する。[VERIFIED: .planning/config.json:49-51; approved proposal.md:23-25; 05-CONTEXT.md:17-19]

## Assumptions Log

| # | Claim | Risk / handling |
|---|---|---|
| A1 | `.github`はCI変更を捕捉する予防的な監視候補（存在未確認） | 実行する検証ファイルではない。存在を前提にせず全パス分類で補う |

その他の提案CLIは公式helpに基づく設計であり、追記後の実行結果は未取得。成功したと主張しない。

## Open Questions / Planning Handoff

- **RESOLVED — baseline再確認手順:** 05-01-PLAN.md baseline_and_heads と task 05-01-01が、B_doc=54106df87baa6cc017167eb311fd0fd4f81ea0fa / B_request=c6b701bfdc1af9c39f9b8421336e881e5cda6ee4を固定し、実行開始時のgit rev-parse HEAD、git ls-files --eol、wc -lc、tail/od、README全文・全patch、依頼開始前履歴の再確認を要求する。4643 bytes / 34 LF行 / 末尾0aまたは未変更前提が違えば編集せず停止・再計画する。候補を黙って差し替えない。これは手順の解決であり、実行時の再観測済みという意味ではない。[VERIFIED: 本research Baselineを二つ区別する; 05-01-PLAN.md baseline_and_heads / task 05-01-01; 05-CONTEXT.md D-02/D-04/D-07]
- **RESOLVED — 証拠名/添付先/head記録契約:** Evidence Contractと05-01-PLAN.md task 05-01-02にBuilder/品質の文書名、品質カードの標準添付先、2文書のread_file読戻しを確定した。開始時HEAD、README確定後H_impl、品質検証head、報告確定後H_reportを実行時の実SHAで別欄記録し、H_reportは確定後の配送本文へ実SHA・C6・全差分再照合結果を書く。自己commit SHAや未観測の将来SHAを捏造しない。local wt/task branchと正式配送先を区別し、カードworkerがArgonauts E.3のHEAD refspec配送後にremote実SHAと照合する。実装・品質・添付そのものは後工程pendingであり、計画上の未決事項ではない。[VERIFIED: 05-01-PLAN.md execution_contract / baseline_and_heads / task 05-01-02; 05-CONTEXT.md D-06/D-07; Argonauts team-workflow E.3/E.5]
- **RESOLVED — LOW confidenceの扱い:** 公式classify-confidenceがprovider `local` / `official` / `webfetch`（いずれも`--verified`）へ返したLOWを保持する。HIGHに格上げせず、承認一次文書・既存CLI help・GNU/Git公式資料による設計根拠と、未実行C1-C6を区別する。Builder/品質の独立実測・前提不一致時停止で扱う。LOWという分類値自体は未解決の製品質問ではなく、edge/prohibitionのunresolvedも別欄のまま解除しない。[VERIFIED: CLI調査結果; 本research Confidence / Code Examples; 05-01-PLAN.md execution_contract / probe_status; 05-CONTEXT.md D-03/D-06]

[VERIFIED: CLI調査結果; 05-CONTEXT.md:20-24]

## Sources

### Primary
- `.planning/phases/05-readme-verification-a/05-CONTEXT.md:9-45` — locked decisions・範囲。
- `.planning/REQUIREMENTS.md:74-86` / `.planning/ROADMAP.md:122-136` — REQ-22/23/24とPhase 5。
- `.planning/argonauts/r-8ac79daf-prd.md:1-70` — 承認済みproposal/spec/tasksの結合入力。
- `openspec/changes/r-8ac79daf-readme-verification-a/{proposal.md,design.md,tasks.md}` / `specs/readme-verification-note/spec.md` — 原本全文をread_fileで確認。
- `README.md:1-34` — 現行全文。
- `.planning/config.json:21-53,63-68` / `.planning/STATE.md:1-16,89-95` — 設定と過去状態の区別。
- 既存CLIのhelp/version/read-only Git結果 — ツール存在、改行、サイズ、履歴、比較オプション。

### Official CLI Documentation
- https://www.gnu.org/software/diffutils/manual/html_node/Invoking-cmp.html — バイト比較、標準入力、exit 0/1/2。
- https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html — 末尾行/バイト。
- https://git-scm.com/docs/git-diff — baseline対比、patch、exit-code、check。

### Supporting
- `.planning/argonauts/r-8ac79daf-learnings.md:18-49` — 対象head、statusだけでは不足、改行確認、旧試験の非流用。

## Metadata

**Research date:** 2026-11-22（date CLIで確認）
**Validity:** baseline/README状態が変わるまで。実行前に再確認する。
**Execution boundary:** research文書保存のみ。README・コード・試験・補助スクリプト変更なし。commit/push/Kanban操作なし。提案検証は未実行。
