# Phase 7: Project description UAT - Research

**調査日:** 2026-11-25（terminal `date -I`）
**Domain:** Pythonパッケージメタデータの単一行追加、TOML意味・バイト不変検証、Git差分と文字証拠
**Confidence:** MEDIUM（現物・承認仕様は直接確認済み。新規検証器の実行と判別力確認はBuilder以降）

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は `.planning/phases/07-project-description-uat/07-CONTEXT.md:13-24,40` の原文。

DATA_88779f0f_START
### Locked Decisions
## Implementation Decisions (locked)
- D-01: [project].descriptionを新規追加し解析値を厳密に `argonauts-uat public (UAT)` とする。さらに印を足さない。判断日時2026-11-24T19:13:42.938043+00:00、原文「新しく作ってよい。完成後の説明文は『argonauts-uat public (UAT)』とする。」
- D-02: 製品は当該1行だけ。既存TOML項目・値、既存行・改行・バイト、他製品ファイルを変えない。全体再シリアライズしない。
- D-03: 検証ファイルを `.planning/argonauts/r-cf2eeaab/` に作る。標準ライブラリのみ。既存製品テスト・依存・CI・CLIを変更しない。
- D-04: 固定起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較。TOML正常解析、完成値完全一致、description以外の解析データ一致、追加行除去後の生バイト一致、工程文書以外の製品差分がpyproject.tomlだけであることを検査。HEAD比較だけで未commit/未追跡の製品変更を見逃さない。
- D-05: 検証ファイルを先に実体として作成→description欠落の実測RED→最小1行追加→同じ検証でGREEN。環境エラー・import失敗・TOML破損を期待REDとしない。違反を確実に落とす検証設計にする。
- D-06: コマンド・終了コード・値・差分・起点・検証対象head・AC別結果を工程文書に記録。品質は対象headで独立再実行しVERIFICATION.mdとCLI文字証拠原本を標準添付。PMはread_fileで判断できること。画像不要は0枚・理由を記す。画像が必要なら品質の実閲覧枚数と結果を文字化し、PMへ画像・圧縮ファイルを開くよう求めない。
- D-07: full、skip_specs=true（振る舞い変更なし）、未決事項なし。危険パスpyproject.tomlのためsmartでも人がマージする。最終化sync/archiveは後工程。
- D-08: 各PLAN3tasks以内、同じ依頼branchへ番号順に直列積上げ。各task終了時点に検証入力が実在し、独立PLANは他PLANの有無に依存せず検証可能。phase検証では先行PLAN含む全成果が同branchに揃う。automatedに無人実行できる検証ファイルのコマンドをそのまま書き、外側cd/grep/インラインコードを付けない。fails_whenは対象誤動作を失敗として観測する条件。

### Claude's Discretion
検証ファイルの局所的な構成、工程記録、PLAN分割。製品範囲や完成値の変更は裁量外。

### Deferred Ideas (OUT OF SCOPE)
依存・既存製品テスト・CI・画面・実行時動作・旧phase修復は範囲外。実装・実検証・受入・最終化は後続カード。
DATA_88779f0f_END
</user_constraints>

## Project Constraints (from HERMES.md)

- ルートの `HERMES.md` と `.hermes/HERMES.md` は、それぞれread_fileで不存在を確認。追加指示を推測しない。[VERIFIED: 本セッションread_fileのFile not found結果]
- project skillsの `.hermes/skills/` と `.agents/skills/` は探索先自体が不存在。公式 `query agent-skills gsd-phase-researcher --skills-only` の出力も空。追加のproject skill適用はない。[VERIFIED: search_files結果、公式CLI結果]
- 本依頼の運用制約：確認はread_file、JSON抽出はjq、GSD判定は公式CLI。インラインPython/Node、シェル経由のスクリプト、ヒアドキュメントを使わない。研究段階で未作成の検証を試さない。commit/push/Kanban操作は禁止。[CITED: 本タスクのCONTEXT・additional_context・output]
- `"nyquist_validation": true` と `"security_enforcement": true` が宣言済みなので、Validation ArchitectureとSecurity Domainを含める。[VERIFIED: .planning/config.json:21-25,49-51]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| REQ-25 | pyproject.tomlの[project].descriptionを新規追加し、解析後の値が厳密に `argonauts-uat public (UAT)` と一致する。完成値に印をさらに追加しない。 | project直下への1行挿入とtomllib厳密比較 |
| REQ-26 | 製品変更は当該descriptionの1行追加のみ。他製品ファイル・既存TOML項目と値・既存バイトを保持する。工程文書は許容し、既存製品テストと依存は変更しない。 | 解析データ比較＋追加行除去後の生バイト比較＋Git全変更の分類 |
| REQ-27 | 変更後のTOMLを正常解析できる。工程配下の標準ライブラリ検証で起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較し、欠落でRED・追加後GREEN、解析データと追加行以外のバイト不変・製品差分限定を直接検査する。品質が対象headで独立実行し、AC別の文字証拠を添付する。 | 検証器先行、欠落固有RED、同一検証器GREEN、隔離変異試験、品質head別原本 |

要件原文は `.planning/REQUIREMENTS.md:92-94`。[VERIFIED: .planning/REQUIREMENTS.md:88-100]
</phase_requirements>

## Summary

今回の製品実装はTOMLの1行挿入だけである。現物のproject部分は `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` でdescriptionは存在しない。build、optional-dependencies、setuptools設定も存在するため、全文書換えでなくprojectの既存行の間に追加する。[VERIFIED: pyproject.toml:1-14] 承認仕様は `description = "argonauts-uat public (UAT)"` を指定する。[VERIFIED: openspec/changes/r-cf2eeaab-project-description-uat/design.md:13-18]

計画の中心は製品コード設計ではなく、欠落で本当に失敗する検証器と、他変更を見逃さない差分検査である。固定起点のblobと作業ファイルを別々に読み、構文、値、description以外の構造、既存バイト、製品変更範囲を別条件として出力する。品質はBuilderの成功報告を転記せず対象headで再実行する。[VERIFIED: openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:7-13]

**Primary recommendation（設計提案）:** 1 PLAN・最大3 tasksで「工程検証器と判別力試験作成／実測REDから1行追加しGREEN／文字証拠を整理し品質へ引継ぎ」とする。製品の機能追加、依存インストール、CI変更は計画に入れない。

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 説明文の保存 | パッケージの静的設定 | — | runtime/API/UIではなくメタデータの変更 |
| 構文・意味・バイト不変の判定 | 工程用ローカル検証器 | 標準tomllib、Git | 製品コードや既存製品試験へ責任を移さない |
| 独立判定と証拠配送 | 品質工程 | PMの文字原本確認 | 自動成功と受入判断を分ける |

上記は本研究の責任分割提案。範囲の根拠は承認designの「データ移行や実行環境変更はない」。[VERIFIED: openspec/changes/r-cf2eeaab-project-description-uat/design.md:28-30]

## Standard Stack

| 要素 | Version / 現状 | Purpose | 選定根拠 |
|---|---|---|---|
| Python標準ライブラリ | 実機 `Python 3.14.9` | pathlib、subprocess、unittest等による工程検証 | 標準ライブラリ限定の承認条件。実機版はterminalで確認 |
| tomllib | Python付属、3.11から提供 | TOMLの正常解析とdict比較 | loadはbinary file、loadsはstrを受け取り、破損時TOMLDecodeError。書込み機能なし。[CITED: https://docs.python.org/3.14/library/tomllib.html] |
| Git | 実機 `git version 2.52.0` | 固定blob取得、追跡差分・未追跡の列挙 | 実機版と固定起点の対象blob到達を確認済み。[VERIFIED: terminal git --version / git cat-file -e結果] |
| unittest | Python付属 | 工程検証器自体の変異・境界試験 | 新規依存を要しない構成として採用する設計提案 |

**Installation:** 不要。外部パッケージ追加なし。Package Legitimacy Auditのインストールゲートは対象外。[VERIFIED: 07-CONTEXT.md:16、design.md:11]

既存製品は `dev = ["pytest"]` を宣言し、CIは `python-version: "3.12"` で `python -m pytest` を実行する。これを工程検証器の新しい依存や変更対象にはしない。[VERIFIED: pyproject.toml:10-11、.github/workflows/pytest.yml:13-18] 既存試験もtomllibでmetadataの一部を読むが、新descriptionの完全一致・バイト不変・全差分限定まではその試験に含まれていない。[VERIFIED: tests/test_cli.py:185-189]

## Architecture Patterns

### データフロー（設計提案）

```text
固定起点のGit blob ─→ bytes ─→ UTF-8/TOML解析 ─┐
作業ツリーの設定 ──→ bytes ─→ UTF-8/TOML解析 ─┼→ 条件別判定
                          └→ 追加行だけ除去 ──┘
固定起点/HEAD/index/worktree/未追跡一覧 → 工程パス分類 → 製品範囲判定
全条件結果＋コマンド＋head＋exit → Builder文字原本
同じ検証ファイル＋対象head → 品質独立再実行 → 品質文字原本 → PM
```

### 1. bytesを原本にし、意味と形式の検査を分ける

設計提案：基準を `git show c572613dc626160db2eb3bf4a41c95fc8283b828:pyproject.toml` のstdout bytesとして取得し、作業側をread_bytesで読む。Git取得失敗、decode失敗、parse失敗、値欠落を異なる結果として記録する。基準側にもdescriptionがないことを確かめ、新規追加という前提を固定する。起点はHEADへ置換しない。[VERIFIED: 07-CONTEXT.md:14-18、design.md:5,17]

設計提案：両側をtomllib.loadsで解析し、作業側project.descriptionの存在・型・完全一致を確認する。値をstrip/正規化しない。解析結果を複製してproject.descriptionだけ削除し、基準解析結果と全体比較する。bytesはsplitlines(keepends=True)等で保持し、指定の追加行がちょうど1行あることを確認してその1行だけ除去し、基準bytesと比較する。replace_allで複数行を消さない。

実機の `git ls-files --eol -- pyproject.toml` は `i/lf w/lf`。既存改行を正規化せずLFの1行を挿入する。挿入候補はversion直後、dependencies直前であり、後続のoptional-dependenciesテーブルに入れない。[VERIFIED: terminal --eol結果、pyproject.toml:5-11]

### 2. Gitの変更集合は検証器内で分類する

承認designの工程パスは `.planning`、`openspec`、`_bmad-output`、`.compound-engineering`、`docs/solutions`。[VERIFIED: openspec/changes/r-cf2eeaab-project-description-uat/design.md:18] 設計提案：これらをディレクトリ境界付きで判定し、それ以外は原則製品として扱う。許可された製品パスは `pyproject.toml` だけ。未知のパスを工程とみなして黙って除外しない。

設計提案：少なくとも以下を検証器のsubprocess argvで別々に取得する。NUL区切りを使い、空白・改行を含むパスをsplitlinesで壊さない。renameは無効化するか旧新両パスを評価し、mode変更・削除も落とす。

- 固定起点→HEAD：既にcommitされた製品便乗変更。
- 固定起点→index、および固定起点→worktree：stagedのみ、unstagedのみ、HEADの変更を手元で戻したケースを含める。
- 未追跡：`git ls-files --others --exclude-standard -z`。追跡差分のみでは新規ファイルを拾わない。
- worktreeのdirty一覧：証拠に全状態を残し、品質では検証対象headに対し製品dirtyがないことを追加gateにする。

Gitのcommit1個指定diffは当該commitとworktreeの比較であり、commit2個指定はtree同士の比較。ls-filesのothersとexclude-standardは未追跡・無視規則の扱いを明示する。[CITED: https://git-scm.com/docs/git-diff][CITED: https://git-scm.com/docs/git-ls-files]

**実機固有の注意:** 調査中、否定pathspecで工程を外そうとした呼出しは `fatal: Unimplemented pathspec magic '_' in ':!_bmad-output'` を返した。全パスの `git diff --no-ext-diff --name-only <起点>` に戻すと成功し、列挙された追跡差分は工程パス内だった。よって外側shellやGit否定pathspecへ分類を任せず、検証ファイル内で明示分類する。未作成検証器がこの環境で動くことは未立証。[VERIFIED: 本セッションterminal失敗・再試行結果]

ignore対象のキャッシュは製品追加と混同しない。一方、ignoreされた場所の新しい製品を扱う保証を主張するなら別途明示走査が必要で、通常の未追跡列挙だけで全filesystemを検査したとは書かない。[CITED: https://git-scm.com/docs/git-ls-files] 現在のignoreは `__pycache__/`、`*.pyc`、`.pytest_cache/`。[VERIFIED: .gitignore:1-3]

### 3. PLANは1本で検証入力の実在を閉じる（提案）

| Task | 作成・実施するもの | task終了時の直接検証 |
|---|---|---|
| 1 | 工程検証器と標準unittestによる判別力試験を先に作成 | 孤立fixtureの正常対照と各違反検出が成功。実repoの同じ検証器でdescription欠落固有のREDを保存 |
| 2 | 指定1行だけ追加 | Task1と同じ検証器の実repo実行がGREEN。起点、値、bytes、変更集合がすべて合格 |
| 3 | BuilderのAC別文字証拠・品質引継ぎ整理 | 全成果が同branchに存在し、同じ検証器と判別力試験を再実行できる |

Task1のautomated成功は「製品が完成」ではなく「検証器の判別力が成立」。REDの子実行exitと原因を別に保存し、環境失敗を成功扱いしない。品質の独立実行・標準添付・PM判定は後続の役割として明記し、Builderの自己検証で代用しない。[VERIFIED: 07-CONTEXT.md:18-21、tasks.md:10-13]

## Don't Hand-Roll

| 問題 | 作らないもの | 使うもの | 理由 |
|---|---|---|---|
| TOML構文の正当性 | 独自正規表現パーサ | tomllib | 別テーブル・重複・型違いを字面検索だけで合格させない |
| 改行・空白保持 | TOML全体の再serializer | 局所1行挿入＋bytes比較 | 意味一致だけでは既存バイト不変を示せない |
| Git引数構築 | shell=True、外側grep、否定pathspec依存 | subprocessのargvと明示パス分類 | 実機pathspec失敗とパス引用の曖昧さを避ける |
| 品質独立性 | Builder原本の品質名義コピー | 品質自身による対象head再実行 | 実行者・対象head・未実施を偽らない |

これは設計提案であり、tomllibのAPI根拠と承認禁止事項は上記出典を参照。

## Common Pitfalls

1. **字面があれば合格:** project以外に同名キーがあってもgrepは通る。project配下の厳密値とTOML解析を必須化する。[VERIFIED: design.md:23-25]
2. **解析一致で整形差分を見逃す:** 全文再serialize、CRLF化、空白・末尾改行変更はbytes検査で落とす。[VERIFIED: 07-CONTEXT.md:15,17]
3. **HEADだけの確認:** 未commit/未追跡が不可視。Git比較面を分ける。[VERIFIED: 07-CONTEXT.md:17]
4. **REDの理由を見ない:** FileNotFound、import失敗、Gitエラー、TOML破損は欠落REDの代替にならない。[VERIFIED: 07-CONTEXT.md:18]
5. **検証器はGREENしか試さない:** 正常対照が通り、各違反が狙った条件で落ちる変異試験を隔離fixtureで行う。本repoへ一時的な製品改変を注入しない。[VERIFIED: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:35-44]
6. **stale STATEを現phaseと誤認:** STATE frontmatterは `current_phase: 5`、本文にPhase7追加履歴がある。公式initはphase_number `07` を返した。旧phaseの修復はしない。[VERIFIED: .planning/STATE.md:3-7,93-101、07-CONTEXT.md:9、公式init.phase-op 7結果]
7. **報告commitを検証headへ付替え:** 検証対象headと後から証拠を保存したheadを区別し、製品が変わったら品質を再実行する。[VERIFIED: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:66,74-81]

## Code Examples

以下はBuilderがファイル内へ実装するための断片であり、この研究で実行したスクリプトではない。固定値の根拠は `description = "argonauts-uat public (UAT)"` と起点 `c572613dc626160db2eb3bf4a41c95fc8283b828`。[VERIFIED: tasks.md:7-8] APIはPython公式3.14文書参照。[CITED: https://docs.python.org/3.14/library/tomllib.html]

```python
# 設計断片。base_raw/current_rawはそれぞれ独立に取得したbytes。
base_data = tomllib.loads(base_raw.decode("utf-8"))
current_data = tomllib.loads(current_raw.decode("utf-8"))
# 実装ではKeyErrorやTOMLDecodeErrorを条件別の結果として記録する。
assert "description" not in base_data["project"]
assert current_data["project"]["description"] == "argonauts-uat public (UAT)"
without_description = copy.deepcopy(current_data)
del without_description["project"]["description"]
assert without_description == base_data
line = b'description = "argonauts-uat public (UAT)"\n'
lines = current_raw.splitlines(keepends=True)
assert lines.count(line) == 1
lines.remove(line)
assert b"".join(lines) == base_raw
```

本番検証器ではassertだけに依存せず、明示的な条件分岐・非zero終了を推奨する（最適化実行で検査を無効化しないための設計提案）。この断片はスコープ検査や文字証拠の代わりにならない。

## Validation Architecture

### Test Framework

**予定名:** 以下の2ファイル名は本研究の設計提案であり、未作成。作成場所 `.planning/argonauts/r-cf2eeaab/` は承認済み。[VERIFIED: 07-CONTEXT.md:16、tasks.md:7] 研究中には一切実行していない。

| Property | Value |
|---|---|
| Framework | Python 3.14.9標準unittest＋工程用standalone検証器 |
| Config file | 追加不要。固定起点・完成値・工程パスは検証器に明示 |
| Quick run command（作成後） | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` |
| 判別力試験（作成後） | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` |
| Full suite | 上記2コマンドをそれぞれ直接実行。外側cd/grep/インラインコードを付けない |

検証器は自分のファイル位置からrepo rootを確定しsubprocessのcwdを内部設定する。必要なGit機能が実機で未対応なら環境エラーとして区別して停止する。架空の成功出力へ差替えない（設計提案）。

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command（作成後） | File Exists? |
|---|---|---|---|---|
| REQ-25 | project.descriptionの存在と完成値完全一致 | integration | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ❌ Wave 0 |
| REQ-26 | 全体解析データ、既存bytes、製品パスの限定 | integration | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ❌ Wave 0 |
| REQ-27 | TOML成功、固定起点、条件別判定 | integration | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ❌ Wave 0 |
| REQ-27 | 違反を狙った理由で落とす判別力 | unit / isolated Git fixtures | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` | ❌ Wave 0 |
| REQ-27 | 品質の独立実行・文字証拠の標準添付 | quality/manual evidence gate | 品質が同じ実在ファイルを対象headで直接実行。添付原本をPMがread_file | 後続品質工程 |

### 最低限の判別力ケース（設計提案）

- 正常な1行追加だけの対照が成功。
- description欠落、値の前後空白、二重接尾辞、別テーブルへの追加、重複キー、TOML破損がそれぞれ失敗。
- 既存metadata変更、既存空白変更、改行変更、追加空行がそれぞれ失敗。
- 他製品のcommitted/staged/unstaged変更、削除、新規未追跡、mode変更が失敗。
- 工程パスの変更は分類を明示したうえで許容。似たprefixだけの未知パスを許容しない。
- Git失敗とparse失敗をdescription欠落REDとして認定しない。
- 孤立Git fixtureは追跡された基準を先に作り、正しい対照が成功してから各変異を別々に適用する。scratchはTMPDIR配下のみ。基準作成前の未追跡状態を正常比較点にしない。[VERIFIED: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:37-43]

### Sampling Rate

- 各task終了時：その時点で存在する検証入力を使う。Task1は判別力試験の成功と実repo欠落REDの原本、Task2以降は実repoGREEN＋判別力試験。
- 各wave完了時：上記2ファイルの全検査。
- Phase gate：全成果が同branchに揃い、品質が対象headで独立再実行し、AC別文字証拠を添付するまで完了扱いにしない。
- 30秒未満を目標とする小さなfixture設計を推奨するが、所要時間は未測定。旧CLI/browserスイートを今回の検証器に組み込まない。

### Wave 0 Gaps

- [ ] 提案 `verify_description.py` を工程配下へ作る。既存製品テストは編集しない。
- [ ] 提案 `test_verify_description.py` を工程配下へ作る。標準unittestで対照・変異を確認する。
- [ ] 欠落固有のREDと同一検証GREENを、コマンド・exit・stdout/stderr原本として保存する。
- [ ] Builder記録と品質用VERIFICATION.mdのAC対応、対象head、dirty状態、画像0枚の理由、原本添付先を確定する。
- Framework installは不要。

## Evidence Contract（品質への引継ぎ提案）

AC-1/AC-2/AC-3は承認PRDの定義を保持する。[VERIFIED: _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:98-102]

| 記録項目 | 必須内容 |
|---|---|
| 帰属 | 実行者、役割、起点SHA、検証対象head、後続報告headを別記 |
| 再現 | 実行場所、実コマンド、Python/Git版、終了コード、stdout/stderr原本 |
| AC-1 | 解析された値を引用し、完全一致結果を示す |
| AC-2 | descriptionを除いた解析データ一致、追加行除去後bytes一致、工程と製品の全変更一覧 |
| AC-3 | TOML解析成功。RED側は構文成功のうえで欠落が原因と分かる記録 |
| RED/GREEN | 同じ検証器の欠落失敗と追加後成功。環境失敗・未実施を別扱い |
| 品質 | 品質自身の対象headでの再実行、VERIFICATION.md、CLI文字原本の標準添付 |
| 画像 | 今回はメタデータのみで視覚変更がないため0枚・理由を明記 |

保存済み、標準添付済み、PMが原本読取り済みは異なる状態。archiveだけをPMへ渡さず、read_fileで読める文字原本を渡す。[VERIFIED: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33-45] 本研究で添付・独立品質・受入を実施したとは主張しない。

## Security Domain

有効化根拠は `"security_enforcement": true`、`"security_asvs_level": 1`。[VERIFIED: .planning/config.json:49-51] 以下は本変更範囲に対する適用判断であり、新しい製品セキュリティ仕様ではない。

| ASVS Category | Applies | Standard Control |
|---|---|---|
| V2 Authentication | いいえ | 認証の追加・変更なし |
| V3 Session Management | いいえ | sessionの追加・変更なし |
| V4 Access Control | 製品上の変更なし | 危険パスを人がマージする工程gateを維持 |
| V5 Input Validation | 工程検証器に適用 | tomllib、厳密値比較、パス境界、Git失敗のfail-closed |
| V6 Cryptography | いいえ | 暗号機能追加なし。SHAは比較対象識別であり暗号設計を追加しない |

| Threat / 失敗型 | STRIDE | Mitigation（提案） |
|---|---|---|
| shell引数・パス解釈の混同 | Tampering | argv配列、shell=False、固定起点、NUL区切り |
| 検証失敗の握り潰し | Repudiation | 実exitと条件別結果を保存、予期しない例外は環境/検証失敗として停止 |
| 証拠headの取り違え | Tampering | 起点・対象head・報告head・dirtyを別記し品質独立再実行 |

外部送信・権限変更・課金・データ消去はしないという承認境界を維持する。[VERIFIED: _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:88-92]

## State of the Art / Alternatives

- tomllibは読むために使い、書くための依存を追加しない。公式3.14文書がTOML 1.0.0とwrite非対応を明記する。[CITED: https://docs.python.org/3.14/library/tomllib.html]
- バージョンなしPython文書は取得時に3.15向けTOML 1.1.0を記載していた。実機3.14.9に合わせて3.14文書を読み直した。将来版の機能をこの計画へ持ち込まない。[VERIFIED: 本セッションweb_extract両ページ結果]
- TOML writerの採用、全文再serialize、製品pytestの増設は今回の承認境界に反するため採用しない。選択が未決だからではない。[VERIFIED: 07-CONTEXT.md:15-16,40]

## Open Questions / Assumptions Log

**要求の未決事項:** なし。[VERIFIED: 07-CONTEXT.md:20]

**実装前の未検証事項:** 新規検証器の具体的Gitフラグ互換性、変異の判別力、実測所要時間。すべてBuilderが実在ファイル作成後に測定する。新規ファイル名・責任分割・task構成は本研究の提案であり、既存実装やユーザーの追加要求ではない。

学習済み知識だけに依存した互換性主張は採用していない。外部依存追加がないためEnvironment Availabilityの外部サービス監査とRuntime State Inventory（rename/refactor/migration）は対象外。Python/Git版は現物確認したがtomllib実import試験や製品試験は本研究で行っていない。

## Sources / Research Execution Notes

### Primary: 直接読んだrepo一次資料

- `07-CONTEXT.md:9-24,39-40` — locked decisions、裁量、対象外。
- `.planning/REQUIREMENTS.md:88-100` — REQ-25/26/27。
- `pyproject.toml:1-14` — 現在の全設定、description欠落。
- `openspec/changes/r-cf2eeaab-project-description-uat/design.md:5-30` と `tasks.md:7-13` — 固定起点、bytes、工程許可パス、独立品質。
- `.planning/argonauts/r-cf2eeaab-prd.md:37-45` — 承認task全文。
- `_bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:88-118` — ACと未決なし。
- `tests/test_cli.py:153-189`、`.github/workflows/pytest.yml:13-18`、`.gitignore:1-3` — 既存試験/CIの境界。
- `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:35-44` — 判別力とscratch基準。
- `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33-45,66-81` — 原本配送とhead帰属。

### Official docs: cited API根拠

- https://docs.python.org/3.14/library/tomllib.html — 実機系列のAPI。取得ページtitleはPython 3.14.10 documentation。公開日を別途確認したとは主張しない。
- https://git-scm.com/docs/git-diff — 各比較面。
- https://git-scm.com/docs/git-ls-files — 未追跡、exclude-standard、NUL、mode。

### 研究実行と制約

- 公式launcher経由の `query init.phase-op 7` はphase_found=true、phase_number="07"、has_context=true、has_research=falseを返した。graphifyはdisabledであり、有効化していない。
- research-plan seamをTMPDIR内JSONで呼び、3件の公式URLにjina fetchを指示された。専用jina/Context7/ctx7が利用できなかったため、組込みweb_extractで公式URLを取得した。キャッシュ永続化はrepoに追加の工程状態を書かないため省略した。
- classify-confidenceは実fetch相当のwebfetchにLOWを返した。Context7にはMEDIUMを返したが本研究では使っておらず、その値で外部取得のtierを昇格していない。外部文書は[CITED]、repo一次資料は実読箇所を[VERIFIED]で示す。総合MEDIUMはローカル根拠と未実行部分を併記した研究判断であり、外部providerのHIGHを主張しない。
- 調査対象headは `72a31e6572844a518845e73eedc1fe52ee8d6113`。固定起点との差分でpyproject.tomlは変更なし。`git cat-file -e`で起点blobの存在を確認した。現在は既存の `.planning/state.json` の変更とphaseの `.gitkeep` 未追跡があるため、全tree cleanとは記さない。
- 全差分の一括取得を工程deny-pathspecで絞る案は実機エラーとなり、全パス取得に切替えて解消した。研究中に製品ファイル・設定・既存試験を変更せず、RED/GREENや品質完了を捏造していない。

## Metadata

| Area | Confidence | 根拠と限界 |
|---|---|---|
| Standard Stack | MEDIUM | 実機版・既存tomllib利用・公式API確認。新規検証器は未実行 |
| Architecture | MEDIUM | locked decisionsに沿った局所設計。構成名とtask構成は提案 |
| Pitfalls | MEDIUM | repo学習文書と実機pathspec失敗で裏付け。各変異は後続実測 |

**Research date:** 2026-11-25
**Valid until:** 固定起点、承認範囲、実行環境が変わるまで。特に対象head更新時は品質証拠を流用せず再実行する。
