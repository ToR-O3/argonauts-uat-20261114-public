# Phase 06: pyproject description UAT - Research

**Researched:** 2026-11-24（`date -I`で確認）
**Domain:** Pythonパッケージメタデータの最小変更、構造/生バイト/Git境界検証、独立品質の証拠帰属
**Confidence:** MEDIUM — 要件・現物テキストは直接読了。基準blob/Git状態・検証CLIの実動は実装工程に留保。

<user_constraints>
## User Constraints (from CONTEXT.md)

以下のLocked Decisions、discretion、deferredは06-CONTEXT.md:15–36,59–61の原文。

### Locked Decisions

### 承認と固定入力
- D-01: 受付t_78c8849eの依頼者判断日時2026-11-24T13:00:38.567271+00:00、原文「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」が正本。OQ-1は回答済み、再質問不要。
- D-02: 改訂仕様head56b70bdca4349c6d2f9eaeb62be2e340a3e04b49はPM t_b8e9c36c run37 approved。元の未改訂仕様承認と新設回答を組み合わせず、この改訂承認を照合する。
- D-03: 完成値は正確に `argonauts-uat public (UAT)`。ASCII ` (UAT)` の連結1回。指定連結元 `argonauts-uat public` は現物の旧値ではない。正規化、重複、空文字補完は禁止。
- D-04: 不変比較元treeは `b34cba0d008923e7f5267ce52d5403492ea53925`。基準/現物のdescription欠落、repo ToR-O3/argonauts-uat-20261114-public、依頼branch argonauts/r-774f3cd6、対象パス/全内容を実装直前にも再照合。不一致・description既存・解析不能なら製品を編集せずPMへ返す。

### 変更の境界
- D-05: 製品変更はdescription新設1行のみ。全体再シリアライズせず既存バイトを保持。他TOML項目、依存、他製品ファイル、無関係な書式、空白/改行/末尾改行は不変。製品試験・CIの追加変更禁止。検証スクリプト/負例/証拠は工程管理領域に限定する。
- D-06: 比較先は製品commitに固定。基準→製品commitの全追跡差分（追加/削除/改名/mode含む）、index、作業ツリー、未追跡一覧を確認。工程成果物の除外パスと用途を全件列挙し、任意コードを工程ディレクトリというだけで除外しない。

### 試験と直接観測
- D-07: OpenSpec1.1で承認・対象・基準と欠落を証拠に固定。1.2で工程領域の検証スクリプトを先に作り具体的コマンドと基準取得方法を確定。編集前は正常解析/基準取得が成功し、固定完成値条件だけ不一致の期待失敗を記録。欠落キーへの無条件参照の異常終了は期待失敗ではない。
- D-08: スクリプトの正しい完成値成功と、工程領域内負例（欠落、suffix重複、異なる値、他項目変更、不正TOML）拒否を確認。要件不一致と実行エラーを区別。製品へ負例を書かない。
- D-09: OpenSpec1.3は(a)直前照合/1行新設、(b)条件別検証、(c)証拠記録のsubstepとして進捗表示。tomllib全体解析、固定完成値完全一致、編集後からdescriptionだけ除いた構造と基準の完全一致、追加1行を除いた生バイトと基準の完全一致、生テキストgit差分/未追跡で他製品不変を検証。必須失敗・実行不能は未完了停止し残存差分を記録、無関係な修復/他者差分一括復元は禁止。
- D-10: 基準commit、製品commit、検証対象head、ファイルSHA-256、コマンド、終了コード、条件別結果を文字の証拠に残す。品質は同一製品commit blobのSHA-256と検証ファイルの一致を独立再確認し、VERIFICATION.mdとCLI証拠を標準添付、PMはread_fileだけで判断可能とする。画像/圧縮ファイルを求めない。

### 工程境界
- D-11: 全タスク完了・同一製品commitの独立品質合格・全受入条件成立・PM受入の後だけ、最終化でsync/archive。文書final/OQ解消だけでは実行しない。
- D-12: pyproject.tomlは危険なパスのため受付lightよりfullを優先した理由を最終報告まで引継ぐ。既存閉じたphase/過去の決定を書き換えない。既存phase1/3/4/5のstale検証は今回対象外。

### Claude's Discretion
工程領域のファイル名、標準ライブラリだけの検証CLI詳細、PLAN分割（各3task以内）、証拠文書の配置。順序は同じ依頼branch上へ直列に積み、各task終了時点で検証コマンドと入力が存在するようにする。品質はBuilderと別主体で同じ対象を確認する。

### Deferred Ideas (OUT OF SCOPE)
CLI/API/画面/依存/CI/Architecture変更、製品試験追加、他製品編集、過去phase修復は対象外。sync/archiveは最終化工程のみ。
</user_constraints>

## Summary

最小変更の受入を、値・構造・バイト・リポジトリ境界・証拠帰属に分ける。現物には `[project]`、`name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` があり、その間にdescription行はない。これは本調査のread_fileによるテキスト観測であり、基準commit blobの解析成功・現物とのバイト一致を実測した主張ではない。[VERIFIED: pyproject.toml:5–11]

固定値と試験先行は承認入力で決定済み。外部TOML編集器や製品pytest追加を導入せず、工程領域に専用CLIとstdlib unittestを後続Builderが作成する。未編集現物で値だけが不一致になるRED、隔離正例のGREEN、負例拒否、実製品commitのGREEN、別主体の同一commit検証を直列にする。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:22–36; openspec/changes/r-774f3cd6-pyproject-uat/design.md:22–28]

**Primary recommendation:** PLANは「承認/入力固定→工程検証器・自己テスト・RED→直前再照合・1行新設・GREEN→独立品質への文字証拠引継ぎ」の順とし、1.3の(a)(b)(c)を明示する。以下のCLI名・オプション・終了コードはすべて**設計提案であり未実装**。本調査は製品編集、Git/Kanban操作、検証スクリプト実装・実行をしていない。

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 静的descriptionの1行追加 | パッケージ設定 | — | 実行時CLI/APIの機能変更ではない |
| 値・構造・バイトの照合 | 工程ローカル検証CLI | Git blob読取り | 基準と候補の入力を明示して検証する |
| 全追跡差分/index/作業ツリー/未追跡 | 工程検証CLIの境界層 | 用途付き個別許可一覧 | 内容検証とは別の範囲判定 |
| 同一製品commit確認と受入原本 | 独立品質 | PMのread_file照合 | Builderの自己申告だけで完了しない |

上表はD-05〜D-10の責任を配置した設計推奨であり、サービス追加の提案ではない。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:22–29]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| REQ-23 | `[project].description` を新設し `argonauts-uat public (UAT)` に完全一致。他TOML項目・依存・他製品ファイル・無関係な書式を保持、有効TOML。基準 `b34cba0d008923e7f5267ce52d5403492ea53925` はdescription欠落の不変比較元。承認/対象/欠落の直前照合、試験先行、正負例、構造/バイト/全Git状態、同一製品commitとblob SHA-256の独立品質、文字証拠とVERIFICATION.mdが必要。 | 入力固定、二層検証器、RED専用oracle、差分全件分類、製品commit固定の証拠スキーマ、Validation Architectureで全条件を対応付ける。 |

要件の原文正本は `.planning/REQUIREMENTS.md:84–92`。上表は計画索引用要約であり要件を置換しない。[VERIFIED: .planning/REQUIREMENTS.md:88–92]
</phase_requirements>

## Project Constraints and GSD Discovery

- 公式launcherをsourceした同じterminal内で `gsd_run query init.phase-op 6` を実施。`phase_found: true`、`phase_number: "06"`、`has_context: true`、`has_plans: false`、`has_research: false`、`plan_count: 0`。この結果は作成前の観測。STATEの旧現在位置を根拠にPhase5へ戻らない。[VERIFIED: 本調査GSD init出力; .planning/STATE.md:3–10,91–99; .planning/ROADMAP.md:140–155]
- 開始設定は `"security_enforcement": true`、`"nyquist_validation": true`、`"plan_check": true`、`"pattern_mapper": true`。`"agent_skills": {}`。read_fileとjqで照合。設定を変更しない。[VERIFIED: .planning/config.json:21–53,63]
- `gsd_run query agent-skills gsd-phase-researcher --skills-only` は空出力、`gsd_run graphify status` は `disabled: true`。有効化はしない。[VERIFIED: 本調査公式CLI出力]
- rootでHERMES.mdを検索し一致なし。`.hermes/` と `.agents/` の探索はPath not found。追加project skillは本調査では発見していない。隠れた別scopeの存在を一般否定するものではない。[VERIFIED: 本調査search_files結果]
- ユーザーの実行制約を維持する。ファイル/JSONはread_file、項目抽出はjq、GSD判定は公式CLI。inline実行とheredocを用いない。未作成検証コマンドは研究/計画中には試さない。以下のコマンドはBuilder・品質がファイル作成後に実行するための契約案。

## Standard Stack

| Library / Tool | Version / Availability | Purpose | Why |
|---|---|---|---|
| Python | ローカル `python3 --version`: `Python 3.14.9` | 工程CLIと自己テスト | ランタイムのみ確認済み、モジュール実動はWave 0で確認 |
| `tomllib` | Python標準、3.11で追加 | 基準/候補の全体解析 | 読取り専用。書込みAPIはない |
| `hashlib.sha256` | Python標準 | blob/実検証入力/検証器の指紋 | 生バイトに対するSHA-256 |
| `unittest` | Python標準 | 工程検証器の自己テスト | 外部依存不要、製品testsを変更しない |
| `pathlib`, `copy`, `subprocess`, `argparse`, `json`, `tempfile` | Python標準（API設計候補） | 入力読取り、構造複製、Git呼出し、CLI、文字結果、隔離負例 | subprocessはargv配列、shell=False、blobはbinary |
| GSD | launcher経由の公式CLIが応答 | phase/設定/研究判定 | gsd-tools.cjs直接実行禁止 |
| jq | `/usr/bin/jq`、設定抽出成功 | JSON項目確認 | Python/Node inlineで代用しない |

[VERIFIED: 本調査terminal出力（Python、GSD、jq）] [CITED: https://docs.python.org/3.14/library/tomllib.html] [CITED: https://docs.python.org/3.14/library/hashlib.html] [CITED: https://docs.python.org/3.14/library/unittest.html] [CITED: https://docs.python.org/3.14/library/subprocess.html]

**Installation:** なし。製品の既存 `requires = ["setuptools>=61"]`、`dev = ["pytest"]` は変更しない。新しい検証器はこれらのinstall/buildを要求しない設計とする。[VERIFIED: pyproject.toml:1–14; openspec/changes/r-774f3cd6-pyproject-uat/design.md:11,17–19]

## Package Legitimacy Audit

外部packageの新規導入はゼロ。registry照会/インストールは対象外。TOML writerや第三者のdiff/test packageを追加するPLANにしない。これは依存追加禁止からの設計制約でありpackage監査を実行済みという意味ではない。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:22,36]

## Architecture Patterns

### System Architecture Diagram

```text
承認記録 + 固定基準 + 対象照合
                  |
           前提不一致? ─ yes → 未編集で停止・PMへ
                  | no
基準blob(raw) + 候補(raw) → 全体TOML解析 → 値/構造/バイト条件
                  |                           |
全tree差分 + index + worktree + 未追跡 → 個別用途一覧との照合
                                              |
                                  条件別結果 + exit + 指紋
                                              |
                       製品commit固定 → 別主体の再取得/再検証
                                              |
                          文字原本/VERIFICATION → PM受入
```

### Component Responsibilities and Proposed Structure

以下は**新規作成候補パス**で、実在の定義としてverifiedを主張しない。Plannerがこの名前を採用した場合、Wave 0のfiles_modifiedに全件明記する。

| Proposed file | Responsibility |
|---|---|
| `.planning/phases/06-pyproject-description-uat/verification/verify_description.py` | 内容の純粋検証 + read-only Git境界 + CLI |
| `.planning/phases/06-pyproject-description-uat/verification/test_verify_description.py` | 正負例・終了コード・Git状態oracleの自己テスト |
| `.planning/phases/06-pyproject-description-uat/verification/process-paths.json` | 除外する正確な工程ファイルパスと用途の一覧（prefix免除ではない） |
| `.planning/phases/06-pyproject-description-uat/evidence/builder-cli.md` | 承認/RED/GREEN/全条件/残存差分の文字原本 |
| `.planning/phases/06-pyproject-description-uat/evidence/quality-cli.md` | 別主体による独立取得・コマンド/結果の文字原本 |
| `.planning/phases/06-pyproject-description-uat/06-VERIFICATION.md` | REQ-23と独立品質原本への対応、判定 |

工程領域にあるだけで任意コードを許可しない。上の検証器はこの依頼の直接検証専用。実際の基準→製品commitに現れる既存 `.planning/`、`openspec/`、`_bmad-output/` の工程差分も、パスと用途を全件分類する。未知パスを自動追加して合格へ変えない。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:25,35]

### Pattern 1: 内容検証の純粋層とGit境界層を分ける

**推奨設計:** 内容層はbaseline bytes/candidate bytesだけを受け、条件別結果を返す。境界層だけがGitから固定blob、tree差分、index、worktree、未追跡を取得する。内容層の正例・負例は工程領域の隔離コピーだけで再現する。製品ファイルへの試験用書込みを禁止する。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:25–28]

**基準取得契約（後続Builder用、ここでは実行しない）:** CLI内の `subprocess.run` をargv配列で使用し、`git show b34cba0d008923e7f5267ce52d5403492ea53925:pyproject.toml` のstdout bytesを取得する。exitとstderrを保持し、非0/存在しないblobは実行エラー。baseline bytesを保存する場合もtext modeを経由しない。候補も製品commitのblobから同じ経路で取得する。SHA-256はGit object IDではなく取得したblob本文bytesをhashlibで計算する。[CITED: https://docs.python.org/3.14/library/subprocess.html] [CITED: https://docs.python.org/3.14/library/hashlib.html] [VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:16,25,28]

### Pattern 2: REDと最終受入を混同しない

**推奨CLI終了契約:** `0=全条件合格`、`1=要件不一致`、`2=実行/入力取得エラー`。これは新しい工程CLIの設計提案であり製品CLIの既存終了コードは変更しない。

編集前候補のdescription欠落を通常の要件不一致として返す。基準と候補の解析成功、基準欠落成功、全内容の同一性成功を先に観測する。`.get()`/存在確認で欠落を扱い、KeyErrorを期待失敗と呼ばない。REDのoracleは「exit1」だけでなく**不一致集合が固定完成値条件のみ**、基準取得/解析が成功、その他条件が成功であること。

そのためRED時の構造比較は候補からdescriptionを「存在する場合だけ」除去する。生バイト比較は追加行0件なら元候補bytesそのものを基準と比較する。最終GREENでは固定完成値の存在に加え、許可した追加行が正確に1件であることを要求する。行数条件を独立してREDの第二不一致にしてしまわず、値条件の詳細またはpost-edit gateに配置する。REDの確認専用wrapperが期待exitを検査して0を返す場合も、内側の実測exit1と条件別結果を証拠に残す。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:26–28]

不正候補TOMLは予期された候補不適合として `1` と解析条件のFAILを返す設計を推奨する。一方、基準TOML不正、基準取得失敗、候補ファイル読取不能、Git起動失敗、内部例外は `2`。同じ非0だからという理由で要件不一致と実行エラーをまとめない。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:27–28]

### Pattern 3: 構造と生バイトは別条件

1. baseline/candidate双方を全体解析する。baselineのprojectがtableでdescriptionが存在しないことを前提検証する。
2. candidateのdescriptionは文字列で、固定値と完全一致する。suffix検索だけで代用しない。
3. candidateの全体構造を複製し、project.descriptionだけを除去してbaselineの全体構造と比較する。projectだけの比較に限定しない。
4. 候補bytesから許可した追加description行の**位置・行境界・件数を限定**して取り除き、残りbytesとbaseline bytesを完全比較する。`strip()`、改行正規化、全体文字列replaceで既存部分を消さない。意味上同じ空白/コメント変更もここで拒否する。
5. 生テキストpatchで追加1行/削除0行を確認する。モード変更は内容一致では検出できないのでGit境界へ渡す。

これらは承認契約を実装可能に分解した推奨アルゴリズム。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:18–19,25–28]

**挿入位置:** 現物テキストでは `[project]` は5行、次のtableは10行の `[project.optional-dependencies]`。新設行はその間、既存version行後などに限定する。後のtableへ誤って置いても文字検索は成功し得るため、tomllibで所属を確定する。改行種別/末尾改行はread_fileの表示から推測せず、Builderのraw bytes照合で確定する。[VERIFIED: pyproject.toml:5–14]

### Pattern 4: 全Git状態を別々に判定

以下は後続検証器の**読取りコマンド設計**であり、本調査では未実行。

| Scope | Planned observation |
|---|---|
| 固定tree→製品commit | `git diff --raw --no-abbrev --no-renames -z BASE PRODUCT --` と生patch。追加/削除/型/modeを含め全パス確認。renameは削除+追加で漏れなく分類してもよい |
| index→製品commit | `git diff --cached --raw --no-abbrev --no-renames -z PRODUCT --` |
| worktree→index | `git diff --raw --no-abbrev --no-renames -z --` |
| 製品commit→worktree全体 | `git diff --no-ext-diff --no-textconv PRODUCT --`（相殺するstaged/unstagedも上2行で別途捕捉） |
| 未追跡一覧 | `git status --porcelain=v1 -z --untracked-files=all --ignore-submodules=none`、必要に応じignoredも別表示 |

`BASE` は固定基準、`PRODUCT` は実装後に確定する製品commitのfull IDであり、可変HEADに置換しない。機械判定はNUL区切りを扱い、証拠用は全件を読める文字表へ変換する。工程パスは正確な個別一覧との照合後にだけ製品判定から分離し、未知の追跡/未追跡製品ファイルを拒否する。既存の無視されたキャッシュを製品差分へ勝手に昇格させない一方、ignored一覧を取得したかと扱いの根拠は明記する。モード/削除/改名の検証をpatch本文だけに任せない。[CITED: https://git-scm.com/docs/git-diff] [CITED: https://git-scm.com/docs/git-status] [VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:23]

### Pattern 5: 製品commit、検証HEAD、報告commitを分離

証拠はbaseline commit、承認対象head、製品commit、検証開始/終了HEAD、報告commit（未確定なら未確定と記録）、実施者、検証器のパス/SHA-256、blob SHA-256、実際に検証した入力ファイルSHA-256を別欄にする。品質はBuilderのhash文字列をコピーせず、同じ製品commit blobを独立に取得して再計算し、実検証入力bytesと照合してから同じ検証CLI/自己テストを実行する。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:29; docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md:29–37]

後続文書commitが増えた場合は、同じ製品blobであることだけで全Git境界を省略しない。製品commit固定の内容証拠を保持し、最新HEADとの差分が用途付き工程成果物のみであることを再確認する。新たな製品差分/検証器変更は旧品質合格を流用せず品質へ戻す。未知の将来報告commitを証拠内で自己参照しようとせず、確定後の引継ぎ記録で帰属を示す。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:25,28; docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33–45]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| TOML意味検証 | regexだけの疑似parser | tomllib全体解析 | 所属table/重複キー/型/不正TOMLを判定 |
| 書式保持 | dict全体再出力/formatter | 承認した1行の局所挿入 + raw bytes除去比較 | 既存bytesを維持する契約 |
| SHA-256 | 独自hashまたはGit IDの読み替え | hashlib.sha256(blob bytes) | blob本文の同一性を示す |
| 自己テストrunner | 外部pytest導入/製品tests追加 | stdlib unittestを工程専用ファイルから実行 | 依存/製品試験/CI不変 |
| 全状態判定 | statusのパス一覧だけで内容不変を宣言 | 固定tree差分 + index/worktree + 未追跡分類 | 未追跡パス表示は内容指紋ではない |

[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:17–28; docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:31–42] [CITED: https://docs.python.org/3.14/library/tomllib.html] [CITED: https://docs.python.org/3.14/library/hashlib.html]

## Common Pitfalls

- **欠落descriptionから連結する:** `before[project][description]` の例外をREDとしてしまう。存在確認と条件結果を使い、指定連結元とbaseline欠落を別欄にする。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:16,18,27]
- **解析成功だけで合格:** 書式/コメント/他製品/modeは別のoracleが必要。構造比較の成功もraw bytes不変の代替ではない。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:25–28,34]
- **REDで複数条件が落ちる:** 欠落時の行除去を安全に0件扱いし、同一baseline比較は通す。最終受入は必ず存在+完成値を要求する。REDの都合で最終条件を緩めない。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:26–28]
- **不正TOML拒否をクラッシュで代用:** 候補不適合と基準/実行失敗を区別し、自己テストで結果の条件名まで照合する。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:27–28]
- **工程ディレクトリを丸ごと除外:** 用途不明コードがすり抜ける。全差分の個別分類を要求する。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:23]
- **検証器が存在するだけで完了:** 正例成功、負例の狙った条件での拒否、実製品GREEN、独立品質は別証拠。CIや旧phaseの成功を今回へ流用しない。[VERIFIED: .planning/argonauts/r-774f3cd6-learnings.md:23–28,49–56]
- **read_fileで改行種別を決める:** 表示上の行とraw bytesを混同しない。binary取得で改行/末尾を保持する。[VERIFIED: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md:36–42]
- **保存済みをPM配送済みとする:** VERIFICATIONとCLI原本を標準添付し、添付対象を読み戻して確認する作業を品質の受渡し条件にする。画像/圧縮不要。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:29; docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33–45]

## Code Examples

実装を行わない研究なので、以下は公式APIの使用パターンと許可された新設行だけを示す。実在検証器/実行結果ではない。

```toml
# [project] 内へ後続Builderが新設する1行（このコメント自体は追加しない）
description = "argonauts-uat public (UAT)"
```

固定値の正本引用: `argonauts-uat public (UAT)`。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:18; openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md:11]

```python
# 公式APIパターン。検証CLIの実装ではなく、入力bytesの扱いを示す。
parsed = tomllib.loads(raw_bytes.decode("utf-8"))
sha256 = hashlib.sha256(raw_bytes).hexdigest()
```

[CITED: https://docs.python.org/3.14/library/tomllib.html] [CITED: https://docs.python.org/3.14/library/hashlib.html]

## State of the Art

本件では新技術の選択より契約の更新が重要。以前の「既存description末尾へ連結」を現行アルゴリズムに残さず、新設と固定値完全一致へ置換する。PyPAのdescriptionはstring型の1行Summaryであり、READMEの長文descriptionとは別フィールド。tomllibはparserでwriterではないため、解析と局所編集を分ける。[VERIFIED: _bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md:49–67] [CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/#description] [CITED: https://docs.python.org/3.14/library/tomllib.html]

## Validation Architecture

`nyquist_validation` は `true` のため省略しない。[VERIFIED: .planning/config.json:25]

### Test Framework

以下のコマンド/ファイルは**Wave 0で新設する契約案**。本調査時点では06ディレクトリにCONTEXTと.gitkeepだけを探索で確認した。研究/計画中には実行しない。Plannerは採用するCLI引数をtasksの実装要件に含め、各taskのverifyはそのtaskまでに実在するファイル/入力にだけ依存させる。

| Property | Proposed value |
|---|---|
| Framework | Python 3.14.9 / stdlib unittest（自己テスト実動は未確認） |
| Config | 外部設定なし。用途一覧だけ `verification/process-paths.json` に新設 |
| Quick run | `python3 -B .planning/phases/06-pyproject-description-uat/verification/test_verify_description.py -v` |
| Full suite | Quick run + 内容CLI RED/GREEN + repository gateの逐次実行。以下のモードを実装してから使用 |

**提案CLIの各モード:**

- `preflight --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml` — baseline取得、双方解析、欠落/全内容一致と対象情報を確認。正常なら0。承認記録の人による照合を自動承認へ置換しない。
- `content --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml` — 未編集時は値だけFAIL/exit1、編集後は全PASS/exit0。stdout/stderrと生exitを保持。
- `repository --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --product-commit FULL_PRODUCT_ID --process-paths .planning/phases/06-pyproject-description-uat/verification/process-paths.json` — 固定blobの内容条件 + 全Git境界 + hash比較。実装後に取得したfull IDで置換し、HEADを暗黙比較先にしない。

上記モードはすべて `python3 -B .planning/phases/06-pyproject-description-uat/verification/verify_description.py` の後ろに渡す引数案。`FULL_PRODUCT_ID` は未確定placeholderであり、そのまま実行してはならない。製品commit前のcontent検証と製品commit後のrepository検証を分ける。

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Planned automated command / mode | File Exists? |
|---|---|---|---|---|
| REQ-23 | 承認/対象/基準/欠落を固定 | preflight + 文書照合 | CLI `preflight` + 承認記録read_file | ❌ Wave 0 |
| REQ-23 | REDは解析/取得成功、値条件だけFAIL | integration | CLI `content`、期待exit1と失敗集合を自己テストで照合 | ❌ Wave 0 |
| REQ-23 | 正しい完成値の成功 | unit / integration | 専用 `test_verify_description.py -v` + 編集後CLI `content` | ❌ Wave 0 |
| REQ-23 | 欠落/重複suffix/異値/他項目改変/不正TOMLを拒否 | unit | 同じ専用自己テスト、各caseの条件名/exitを照合 | ❌ Wave 0 |
| REQ-23 | description除去後全構造一致、1行除去後raw一致 | unit / integration | 自己テスト + `content` + `repository` | ❌ Wave 0 |
| REQ-23 | 他製品/追加削除改名mode/index/worktree/未追跡を検出 | integration | 隔離fixtureでの境界自己テスト + `repository` | ❌ Wave 0 |
| REQ-23 | 同一製品commit blob/入力SHA一致、独立品質文字証拠 | independent integration + 文書 | 品質自身の自己テスト + `repository`、VERIFICATION/CLI原本照合 | ❌ 後続品質 |

### Required Self-Test Matrix

**必須内容負例:** 欠落、`argonauts-uat public (UAT) (UAT)`、別文字列、description以外の項目変更、不正TOML。各caseで単なる非0でなく想定条件が拒否したことを確認する。正例はbaselineに許可行だけ加えたbytesで全PASS、欠落caseは基準取得/双方解析成功かつ値だけFAIL。[VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:27]

**追加推奨の判別力ケース（設計提案）:** 完成値正常+空白/コメントだけ変更→bytes条件FAIL、TOML他table改変→構造FAIL、description非文字列/別table配置/重複キー、baseline取得エラー→exit2。全状態oracleは他製品の変更・追加・削除・rename相当・mode変更、staged/unstaged相殺、未知工程パス、未追跡ファイルを隔離fixtureで個別に拒否する。正例も用意し、元から壊れたfixtureによる偽陽性と区別する。scratch fixtureをGitで構成する場合の操作は後続Builderの試験内に限り、本researchでは行わない。[VERIFIED: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:35–44]

### Sampling Rate

- 各実装task終了時: その時点で存在する専用自己テストを実行。1.1の承認記録作成taskに未来の検証器を要求せず、read_file/jq等で記録項目を確認する。
- 1.2完了gate: 自己テスト正負例成功 + 実未編集候補のpreflight成功 + 値条件だけのRED証拠。製品編集はまだしない。
- 1.3(a): 直前のpreflightと承認再照合後だけ1行新設。
- 1.3(b): content GREEN、製品commit固定後repository GREEN、条件別結果を残す。
- 1.3(c): 実測コマンド/exit/hash/残存差分の原本を保存し、品質へ同一対象を引き渡す。
- phase gate: 別主体の全条件成功と文字原本/標準添付、PM受入が必要。独立品質未実施をBuilder GREENで代替しない。
- 時間: 小さい入力のローカル検証として各自動コマンド30秒未満を設計目標とするが、実測は未実施。所要時間を捏造しない。

### Wave 0 Gaps

- [ ] 工程専用 `verify_description.py` と `test_verify_description.py` の新設。
- [ ] exact-path/用途一覧の新設と全工程差分の棚卸し。
- [ ] 正例/必須負例とGit境界fixtureの隔離配置（工程領域内、製品には書かない）。
- [ ] baseline blob取得・欠落解析・現物bytes一致と承認対象の直前再照合。
- [ ] RED/GREEN証拠の保存形式、CLI exit/条件名の具体化。
- [ ] 品質runbookと文字原本の標準添付/読取り確認手順。
- Framework install不要。製品tests/CI変更不要。研究段階で未作成コマンドを試さない。

## Recommended PLAN Boundaries

以下は分割の設計推奨でありPLANそのものではない。すべて同じ依頼branch上の直列依存、各PLAN3task以内とする。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:36]

1. **入力固定と試験先行:** task1=OpenSpec1.1承認/対象/基準記録、task2=OpenSpec1.2工程CLI+自己テスト+正負例、task3=実未編集REDと証拠。task1のverifyはファイル読取り、task2以降は実在CLIを使用する。
2. **局所製品tracerと引継ぎ:** task1=1.3(a)直前照合/1行新設、task2=1.3(b)content/repository全条件GREEN、task3=1.3(c)証拠原本/品質runbook。製品commitの確定方法・工程報告commitとの差を明記する。品質実行主体はBuilderと分離する。
3. **独立品質/PM受入:** Builderに独立品質を自認させず、同一製品commitの品質gateと文字添付を明示する。sync/archiveはその後の最終化だけ。旧閉鎖phaseやstale証拠を修復するtaskは追加しない。

## Security Domain

`security_enforcement: true` を維持する。認証などの製品機能は追加しないが、工程CLIにも入力と証拠の完全性の境界がある。[VERIFIED: .planning/config.json:49–51; .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:9,22–29]

### Applicable ASVS Categories

指定のV2–V6分類をチェック観点として用いた適用判定（ASVS準拠認証を主張するものではない）。

| Category | Applies | Standard Control / Rationale |
|---|---|---|
| V2 Authentication | 製品変更なし | auth境界を作らない |
| V3 Session Management | 製品変更なし | session状態を作らない |
| V4 Access Control | 工程入力/書込み範囲のみ | repo/対象commit/pathを固定、製品への負例書込み禁止 |
| V5 Input Validation | yes | tomllib全体解析、固定値完全一致、commit入力とパスを検証、argv配列・shell=False |
| V6 Cryptography | 証拠完全性のみ | hashlib SHA-256。hash一致を承認/品質合格の代替にしない |

### Threat Patterns

| Pattern | STRIDE | Mitigation |
|---|---|---|
| 可変HEAD/別repo/別blobへの差し替え | Tampering / Repudiation | 対象をfull commitで固定、blobと実入力をhash照合、実施者と開始/終了HEAD |
| prefix除外へ任意コード混入 | Tampering | 全差分のexact-path/用途分類、未知差分は停止 |
| shell/パス入力注入 | Tampering | subprocess argv、shell=False、作業root固定、通常ファイル/境界外パスを検証 |
| TOML巨大入力 | Denial of Service | 既知の小規模入力に限定し、必要ならparse前サイズ上限を具体化。上限値はPlanner/Builderが根拠付きで決める |
| 成功ログの取り違え | Repudiation | コマンド/exit/条件別結果、検証器hash、独立品質原本を保持 |

[CITED: https://docs.python.org/3.14/library/tomllib.html] [CITED: https://docs.python.org/3.14/library/subprocess.html] [CITED: https://docs.python.org/3.14/library/hashlib.html] [VERIFIED: openspec/changes/r-774f3cd6-pyproject-uat/design.md:24–28]

## Environment Availability

- Python 3.14.9、公式GSD応答、jqの設定抽出は確認済み。
- Context7 MCPはこのtool surfaceに見えず、`command -v ctx7` も出力なし。research-planが選んだjina用の公開toolもないため、許可済みweb_extractで公式URLを直接取得した。追加package導入/認証設定変更なし。
- Git操作禁止のため、repo identity/branch/基準blob到達性/現在の差分を本researchでは検証していない。baseline欠落は承認文書の主張と現物テキスト読了を区別する。
- 製品TOML解析、SHA計算、検証器自己テスト、RED/GREEN、品質実行は未実施。CLIの実動やfile hashを報告済みと扱わない。

[VERIFIED: 本調査terminal/search_files/web_extract出力; .planning/argonauts/r-774f3cd6-learnings.md:9,58]

## Assumptions Log

| # | Claim | Section | Risk / Handling |
|---|---|---|---|
| A1 [ASSUMED] | 実装時にも承認済みbaseline blobが利用可能で現物と一致する | Architecture / Wave 0 | 本調査ではGit未照合。実装前preflightで必ず検証、不一致時未編集停止 |
| A2 [ASSUMED] | 専用自己テストと境界検証を30秒未満で実行できる | Sampling Rate | 未実装/未計測。実測後に判定、達成したと先取りしない |

新設CLI名/引数/終了コード/配置は承認されたdiscretion内の**設計提案**であり、実在値や新たなユーザー決定としてverifiedにしない。入力固定の技術的前提は推測で補わず実装前gateで解決する。

## Open Questions

依頼者へ再質問する仕様OQはない。OQ-1は回答済み。残るのは工程上の検証事項である。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:16; _bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md:106–108]

1. **承認/対象の実装直前照合:** 正本に記載のrepo `ToR-O3/argonauts-uat-20261114-public`、branch `argonauts/r-774f3cd6`、承認head `56b70bdca4349c6d2f9eaeb62be2e340a3e04b49`、基準commit `b34cba0d008923e7f5267ce52d5403492ea53925` をBuilderが照合。本researchは再認証していない。[VERIFIED: .planning/phases/06-pyproject-description-uat/06-CONTEXT.md:17–19]
2. **工程パス全件:** 比較基準以降の実差分を取得してから用途一覧を確定する。未観測パスを想像で列挙しない。
3. **製品commit/品質/添付:** 実装後に実ID、CLI結果、実SHA、品質主体/添付対象を確定する。証拠の保存先があるだけで標準添付済みとしない。

## Sources

### Primary — session-read local sources

- `06-CONTEXT.md:15–36,59–61`: 全locked decisions/discretion/deferred（本書冒頭へ原文転記）。
- `.planning/REQUIREMENTS.md:84–92`: `REQ-23` 原文。
- `.planning/ROADMAP.md:140–155` / `.planning/STATE.md:91–99`: Phase6追加と旧履歴。
- `.planning/config.json:21–53,63`: 検証/security/plan_check/pattern_mapperのtrue、agent_skills空。
- `pyproject.toml:1–14`: 現物全文。バイト境界や基準blob一致までは未検証。
- `openspec/changes/r-774f3cd6-pyproject-uat/{proposal.md,specs/package-metadata/spec.md,design.md,tasks.md}`: 新設/不変/検証/最終化契約。
- `.planning/argonauts/r-774f3cd6-prd.md`: merge正本全文。
- `_bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md` / `prd/prd-r-774f3cd6.md`: AC/FRと旧description誤認の禁止。
- `.planning/argonauts/r-774f3cd6-learnings.md` と読了した4件の `docs/solutions/` 原本: 判別力、raw bytes、head帰属、PM読取り。過去の順位付け/CI/画像の要求は持ち込まない。

### Official documentation — cited, retrieved this session

- https://packaging.python.org/en/latest/specifications/pyproject-toml/#description — string、1行Summary。ページhistoryはAugust 2026等を記載。description自体の最終更新日は取得内容から特定していない。
- https://docs.python.org/3.14/library/tomllib.html — 3.11追加、parser専用、binary file入力、loads(str)、TOMLDecodeError、入力サイズ警告。
- https://docs.python.org/3.14/library/hashlib.html — sha256(bytes)/hexdigest。
- https://docs.python.org/3.14/library/subprocess.html — run、binary stdout、returncode、shell=False。
- https://docs.python.org/3.14/library/unittest.html — 専用ファイル直接実行、unittest.main/-v。
- https://git-scm.com/docs/git-diff / https://git-scm.com/docs/git-status — tree/index/worktree、raw/mode、NUL/porcelain、未追跡/ignoredの区別。

### Provenance / confidence limits

公式 `query research-plan` をscratch JSON入力で実行し、3件の公式URLに対しprovider `jina` を得た。提供toolの制約で `web_extract` へfallback。`query classify-confidence --provider jina` は `MEDIUM`、実際のfallbackに対応する `--provider webfetch` は `LOW`（`--verified` でもLOW）。外部取得の機械tierはこのLOWを維持し、実際にContext7/jinaで取得したとは主張しない。3件のdigestは公式research-storeへprovider `webfetch` / confidence `LOW` で保存した。

本書の `[CITED: URL]` は取得した公式ページへの参照であり、未実行コードへのHIGH信頼付与ではない。`[VERIFIED: file:lines]` はこのセッションでread_fileした文書/現物テキストの内容と引用値に限る。Git blob/CLI結果/品質合格の実測を文書引用から創作しない。Python docsの取得ページ表題は3.14.10、ローカルは3.14.9なので、patch版同一の実動検証を行ったとは扱わない。

## Metadata

**Confidence breakdown:**
- 要件/境界: HIGH（正本文書と現物全文の直接読取り、承認の運用再照合は後続）。
- Standard stack/API参照: LOW（公式URL取得済みだが、公式confidence seamのfallback tierを尊重、実動未確認）。
- 検証アーキテクチャ: MEDIUM（承認契約の具体化、自己テスト/実動をWave 0へ明示）。
- Git/製品/品質結果: 未検証。研究完了を製品合格としない。

**Research date:** 2026-11-24
**Valid until:** 実装直前の再照合まで。承認/基準/対象/設定が変わった場合は再調査し、旧成功を流用しない。
