# Phase 05 — security auditor supplementary evidence

これは独立監査の文字証拠であり、公式 SECURITY.md、VERIFICATION.md、品質配送の完了記録、PM受入判定の代用品ではない。脅威別の公式構造化判定は親へ返す。指定文字列の掲載は通し検証の実施・合格認定ではない。descriptorless prohibition は flagged-unverified のまま保持する。

## Identity / scope

- cwd: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_df0c2ebc`。以下のコマンドはすべてここで実行。
- B_request: `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`。
- B_doc: `54106df87baa6cc017167eb311fd0fd4f81ea0fa`。
- H_impl: `5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e`。
- H_report / 今回の監査対象HEAD: `cc46cf164aeff3ccbf19cbb7489b5be01f486901`。
- 公式 `query config-get workflow.security_asvs_level --raw` は `1`、`query config-get workflow.security_block_on --raw` は `high`。register_authored_at_plan_time=true（PLAN:168–186）。設定変更なし。
- PLAN / SUMMARY / QUALITY-HANDOFF / BUILDER-CLI を全文 read_file。親・Builderの成功値を独立実行の代わりにしていない。新規脅威探索は行わず登録済み4脅威のみ確認。
- 画像閲覧0枚。製品変更はREADMEの文字・バイト・Git差分だけで、製品UI/HTMLを変えない。BMAD HTMLは工程仕様の表示ビューとしてソースを読み、ブラウザで実行していない。

## Independent command results

各C1–C4、C5 guard、C6 equalityは個別terminal呼出し。以下の空出力はstdout/stderrとも空、他の成功呼出しもstderr空・tool error=null。pipelineは記載どおり同じ呼出しでpipefailを有効化。Git/GNU既存CLIのみ。インラインPython/Node/シェルスクリプト、新しい試験・helperはなし。

| ID | 実行した完全コマンド | stdout / 結果 | raw exit |
|---|---|---|---:|
| C1 | `set -o pipefail && tail -n 1 README.md \| grep -Fx -- '検証A: v1.12 の通しの確かめ（2026-11-22）'` | 指定行+LF | 0 |
| C2 | `set -o pipefail && git show 54106df87baa6cc017167eb311fd0fd4f81ea0fa:README.md \| cmp -n 4643 - README.md` | 空 | 0 |
| C3 | `set -o pipefail && printf '%s\n' '検証A: v1.12 の通しの確かめ（2026-11-22）' \| cmp -i 0:4643 - README.md` | 空 | 0 |
| C4 patch | `git diff --no-ext-diff --no-textconv --no-color --unified=3 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | 下記全patch | 0 |
| C4 numstat | `git diff --numstat 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | `1\t0\tREADME.md`+LF | 0 |
| C4 check | `git diff --check 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md` | 空 | 0 |
| C5 inventory | `git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD` | 下表全66パス | 0 |
| C5 guard | `git diff --exit-code c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- wordfreq tests tools pyproject.toml .github` | 空 | 0 |
| C5 status | `git status --porcelain=v1 --untracked-files=all` | ` M .planning/phases/05-readme-verification-a/05-VALIDATION.md`+LF（本証拠作成前） | 0 |
| C5 untracked | `git ls-files --others --exclude-standard` | 空（本証拠作成前） | 0 |
| C6 identity | `git rev-parse HEAD` | `cc46cf164aeff3ccbf19cbb7489b5be01f486901`+LF、初回/終端とも同一 | 0 |
| C6 equality | `set -o pipefail && git show HEAD:README.md \| cmp - README.md` | 空 | 0 |

C4全patch（実出力を全文読了）:
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

README全文35行を別途read_file。C2/C3は既存4643バイト保持と残り全体=指定行+LFを分割検証。末尾hunkのみ、追加1/削除0、mode100644不変。

## Full C5 patch / long JSON / current differences

scratchルート S は `/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/cache/scratch`。下記 `<S>` はこの絶対パスの表記上の省略であり、実行時は絶対パスを用いた。既存ログ L は `/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/cache/terminal-output/out-1795338880-323618-4510.log`。

- Lをread_fileで1–600、601–1350、1351–2100、2101–2950、2951–3750、3751–4120と連続して独立読了。patch本体は1–4116。追加ファイルは全内容、変更ファイルは全hunkを読んだ。README/PLAN/SUMMARY/Builder文書/VALIDATION/REQUIREMENTS/ROADMAP/STATE/state.json/HTMLは現物も全文read_file。
- 初回 `git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD | cmp - <L>` はraw exit1、`cmp: EOF on - after byte 350134, line 4116`。これは黙って成功へ変換していない。Lの4117–4120はterminalのPIPE/CWDフッターでありGit patchではないと読取りで確認。
- `set -o pipefail && git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD > <S>/t_df0c2ebc-audit-committed.diff && wc -lc <S>/t_df0c2ebc-audit-committed.diff && cmp -n 350134 <S>/t_df0c2ebc-audit-committed.diff <L>` はraw exit0。wc=`4116 350134`。再生成した全patchの全350134バイトが読了済みLのpatch本体に一致する。フッター差を製品不一致と混同しない。
- `git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- > <S>/t_df0c2ebc-audit-current.diff` はraw exit0。
- `git diff --no-index -- <S>/t_df0c2ebc-audit-committed.diff <S>/t_df0c2ebc-audit-current.diff` は期待どおり差分表示exit1、stderr空。全文読了した差はVALIDATIONのblob ID、draft→validated、nyquist_compliant false→true、末尾のNyquist監査説明のみ。共通全patch+この全差分でcurrent全体を確認。`git diff --no-ext-diff --no-textconv --no-color HEAD --` の全出力も同じVALIDATION更新のみ、cached diffは空。
- 長いJSON行1030/1047/1061/1117のread_file省略を補完: `set -o pipefail && jq -r '.activeHooks[]?.fragment.inline // empty, .rendered // empty' .planning/argonauts/t_8a90bad6-plan-pre.json | fold -w 140 > <S>/t_df0c2ebc-audit-long-json.txt` はraw exit0。出力710行をread_fileで1–360/361–710と全文読了。API coverage / assumption delta / schema / securityのテンプレートとrenderedの引用データであり、実行ファイルではない。含まれるCLI引用は実行しない。
- inventory保存: `set -o pipefail && git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD | jq -R -s 'split("\n") | map(select(length>0) | split("\t") | {status:.[0],path:.[1]})' > <S>/t_df0c2ebc-audit-inventory.json` はraw exit0。JSON全266行をread_file。
- 件数: `git diff --name-only c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD | jq -R -s 'split("\n") | map(select(length>0)) | {count:length,unique:(unique|length)}'` はcount66/unique66、raw exit0。

## Request-wide path classifications

各行は監査者が読んだpatch内容で分類。工程フォルダ/拡張子だけで許可していない。表はH_reportの全66パス。既存上流成果を今回監査者/Builderの新規作業としない。

| 状態 | パス | 分類・内容 |
|---|---|---|
| M | `.planning/INGEST-CONFLICTS.md` | 工程計画: 今回5入力の取込み衝突と境界。製品仕様を変更しない |
| M | `.planning/REQUIREMENTS.md` | 工程計画: REQ22–24追記とBuilder checkbox、品質表はPending |
| M | `.planning/ROADMAP.md` | 工程計画: Phase5・1 PLAN・実行済み表記、phase完了は未チェック |
| M | `.planning/STATE.md` | 工程状態: Phase5/verify位置・日時・head履歴 |
| A | `.planning/argonauts/r-8ac79daf-learnings.md` | 工程計画: 学習検索と今回へ適用する注意 |
| A | `.planning/argonauts/r-8ac79daf-manifest.yaml` | 工程計画: 入力5文書のtype/pathデータ |
| A | `.planning/argonauts/r-8ac79daf-prd.md` | 工程仕様: 承認proposal/spec/tasks結合入力 |
| A | `.planning/argonauts/t_8a90bad6-checker.md` | 工程検証: 計画checker結果、実装合格との区別 |
| A | `.planning/argonauts/t_8a90bad6-command-paths.json` | 工程検証: 14 CLIパス検査応答、実行scriptではない |
| A | `.planning/argonauts/t_8a90bad6-edge-probe.json` | 工程検証: 3要件unclassified/unresolved保持 |
| A | `.planning/argonauts/t_8a90bad6-failure-directions.json` | 工程検証: CLIとfails_whenの対照データ |
| A | `.planning/argonauts/t_8a90bad6-init-plan.json` | 工程計画: 公式初期化、旧CLIは引用データ |
| A | `.planning/argonauts/t_8a90bad6-plan-post-result.json` | 工程検証: 10項目coverage応答 |
| A | `.planning/argonauts/t_8a90bad6-plan-post.json` | 工程計画: hook設定応答の保存 |
| A | `.planning/argonauts/t_8a90bad6-plan-pre.json` | 工程計画: テンプレート/CLI引用、jqで長文補完、非実行データ |
| A | `.planning/argonauts/t_8a90bad6-plan-sha256.txt` | 工程検証: 計画hash記録 |
| A | `.planning/argonauts/t_8a90bad6-plan-structure.json` | 工程検証: 2 tasksの構造検査とpipeline警告 |
| A | `.planning/argonauts/t_8a90bad6-probe-reqs.json` | 工程計画: REQ22–24のprobe入力 |
| M | `.planning/intel/SYNTHESIS.md` | 工程計画: 今回5入力の合成と非認定境界 |
| A | `.planning/intel/classifications/brief-readme-verification-a-80ad9a20.json` | 工程計画: Brief分類データ |
| A | `.planning/intel/classifications/prd-readme-verification-a-a6c14422.json` | 工程計画: PRD分類データ |
| A | `.planning/intel/classifications/proposal-7703648c.json` | 工程計画: proposal分類データ |
| A | `.planning/intel/classifications/r-8ac79daf/brief-readme-verification-a-80ad9a20.json` | 工程計画: 依頼別Brief分類 |
| A | `.planning/intel/classifications/r-8ac79daf/prd-readme-verification-a-a6c14422.json` | 工程計画: 依頼別PRD分類 |
| A | `.planning/intel/classifications/r-8ac79daf/proposal-7703648c.json` | 工程計画: 依頼別proposal分類 |
| A | `.planning/intel/classifications/r-8ac79daf/spec-a17eb14b.json` | 工程計画: 依頼別SPEC分類 |
| A | `.planning/intel/classifications/r-8ac79daf/tasks-b53d84f7.json` | 工程計画: 依頼別tasks分類 |
| A | `.planning/intel/classifications/spec-a17eb14b.json` | 工程計画: SPEC分類 |
| A | `.planning/intel/classifications/tasks-b53d84f7.json` | 工程計画: tasks分類 |
| M | `.planning/intel/constraints.md` | 工程計画: 文書掲載/保持/scopeの3制約 |
| M | `.planning/intel/context.md` | 工程計画: Brief/tasks引用と後工程、実行命令ではない |
| M | `.planning/intel/decisions.md` | 工程計画: ADR0、既存契約不変の説明 |
| M | `.planning/intel/requirements.md` | 工程計画: 同一要求の出典別2項目 |
| A | `.planning/phases/05-readme-verification-a/.gitkeep` | 工程計画: directory marker、空行のみ |
| A | `.planning/phases/05-readme-verification-a/05-01-PLAN.md` | 工程計画: 2 tasks/C1–C6/threat register、CLI引用のみ |
| A | `.planning/phases/05-readme-verification-a/05-01-SUMMARY.md` | 工程検証: executor要約、品質/配送pendingを区別 |
| A | `.planning/phases/05-readme-verification-a/05-BUILDER-CLI.md` | 工程検証: Builder raw結果・全path分類 |
| A | `.planning/phases/05-readme-verification-a/05-CONTEXT.md` | 工程計画: D01–07固定 |
| A | `.planning/phases/05-readme-verification-a/05-PATTERNS.md` | 工程計画: 文書analog調査、旧結果は転用しない |
| A | `.planning/phases/05-readme-verification-a/05-QUALITY-HANDOFF.md` | 工程検証: 独立再実行と添付/readback手順 |
| A | `.planning/phases/05-readme-verification-a/05-RESEARCH.md` | 工程計画: baseline/CLI調査と未実行の区別 |
| A | `.planning/phases/05-readme-verification-a/05-VALIDATION.md` | 工程計画/検証: CLI coverage戦略。currentはNyquist監査説明だけ追加 |
| M | `.planning/state.json` | 工程状態: milestone/next/日時のデータ |
| M | `README.md` | 唯一の製品変更: 指定末尾1行+LF、既存4643byte不変 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/.memlog.md` | 工程仕様: Brief作成/表示生成の来歴 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/.template.md` | 工程仕様: Briefテンプレートとhtml_view設定 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.html` | 工程仕様表示: Briefのview-dataと内包renderer、下記で個別確認 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.md` | 工程仕様: 指定行/BR01–04/境界 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/review-editorial.md` | 工程仕様: structure/prose編集記録 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/review-fresh-reader.md` | 工程仕様: 作成者の逐次レビューと明示 |
| A | `_bmad-output/initiative-r-8ac79daf/brief/review-reconciliation.md` | 工程仕様: 入力照合、独立品質ではない |
| A | `_bmad-output/initiative-r-8ac79daf/brief/review-rubric.md` | 工程仕様: Brief rubric自己点検 |
| A | `_bmad-output/initiative-r-8ac79daf/independent-review.md` | 工程仕様: 上流6文書の独立reviewと採否 |
| A | `_bmad-output/initiative-r-8ac79daf/initiative-r-8ac79daf.md` | 工程仕様: initiative識別frontmatter |
| A | `_bmad-output/initiative-r-8ac79daf/prd/.memlog.md` | 工程仕様: PRD作成来歴 |
| A | `_bmad-output/initiative-r-8ac79daf/prd/.template.md` | 工程仕様: PRDテンプレートのコメントデータ |
| A | `_bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md` | 工程仕様: FR01/RULE/SMと非認定条件 |
| A | `_bmad-output/initiative-r-8ac79daf/prd/review-fresh-reader.md` | 工程仕様: 自己レビューと独立性の限界 |
| A | `_bmad-output/initiative-r-8ac79daf/prd/review-polish.md` | 工程仕様: 編集結果 |
| A | `_bmad-output/initiative-r-8ac79daf/prd/review-reconciliation.md` | 工程仕様: Brief/依頼照合 |
| A | `_bmad-output/initiative-r-8ac79daf/prd/review-rubric.md` | 工程仕様: PRD rubric確認 |
| A | `openspec/changes/r-8ac79daf-readme-verification-a/.openspec.yaml` | 工程仕様: schema/作成日 |
| A | `openspec/changes/r-8ac79daf-readme-verification-a/design.md` | 工程仕様: byte保持/改行/CLI方針 |
| A | `openspec/changes/r-8ac79daf-readme-verification-a/proposal.md` | 工程仕様: 1行追記と範囲 |
| A | `openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md` | 工程仕様: 掲載/保持/scopeの契約 |
| A | `openspec/changes/r-8ac79daf-readme-verification-a/tasks.md` | 工程仕様/状態: 1.1/2.1完了checkbox、追加製品変更なし |

### BMAD HTML content-based classification

HTML現物301行をread_fileで全文読了。98行のapplication/jsonはlayout=view、slotsはBrief7節の文面。100–101行でmarked@12.0.2とmermaid@10.9.1のjsDelivr CDNを指定。111–116行はscript要素のロード、265–276行はslotsをMarkdown表示、296行はmarked取得後の表示。Mermaidは119–143行でmermaidブロックがある場合だけロードしstrictを設定。159–263行は汎用slide/presenter機能だが、このデータのlayout=viewではstartDeckを呼ばない。280–294行はraw HTML escapeとunsafe URL除外。すなわち「JSなしの静的HTML」とは主張しない。工程仕様の表示rendererであり、wordfreq製品処理・試験・検証helperではない。Brief memlogとtemplateのview/html_view指定にも表示生成の来歴がある。ブラウザ未実行のためCDN無通信は認定しない。新規脅威scanやCDN安全性監査へ範囲を拡張しない。

### H_impl / H_report independent reconciliation

- `git merge-base --is-ancestor 5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e cc46cf164aeff3ccbf19cbb7489b5be01f486901` はexit0。
- `git diff --no-ext-diff --no-textconv --no-color 5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e cc46cf164aeff3ccbf19cbb7489b5be01f486901 > <S>/t_df0c2ebc-audit-heads.diff` はexit0。429行全てread_file。8パス: REQUIREMENTS/ROADMAP/STATE/SUMMARY/BUILDER-CLI/QUALITY-HANDOFF/state.json/OpenSpec tasks。全て上表の工程状態・要約・証拠・手順・checkboxだけ。
- `git diff --exit-code 5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e cc46cf164aeff3ccbf19cbb7489b5be01f486901 -- README.md` は出力空、exit0。
- `git rev-parse 5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e:README.md cc46cf164aeff3ccbf19cbb7489b5be01f486901:README.md` は同じblob `09614982f57a4e65ec5d5b0e164b24b0e896d7c3` を2行、exit0。
- `git rev-parse b95d7b8^` はB_request一致、exit0。
- `git log --format='%H %s' 5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e..cc46cf164aeff3ccbf19cbb7489b5be01f486901` は0f385d2、da4da9a、cc46cf1の3工程commit（実際の出力は新しい順）。
- `git diff --no-ext-diff --no-textconv --no-color --exit-code c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- .planning/config.json` は出力空、exit0。

## Remaining evidence boundaries (not a replacement verdict)

- この監査の開始/終端で未追跡0。既存dirtyはVALIDATIONだけで全文読了済み。監査者はこれを変更しない。本証拠作成後に未追跡として加わる本Markdownは工程検証用の文字記録のみで、製品/試験/helper/scriptではない。
- 05-VERIFICATION.md、05-QUALITY-CLI.md、05-SECURITY.mdはread_fileでnot_foundを確認。親の後工程出力を現時点の実績としない。QUALITY-HANDOFF:16–18/45–55には独立再実行・対象head・2原本添付・hash照合・正確な添付readback・pending区別の手順があるが、添付/読戻しの完了証拠は今回未確認。Kanban操作禁止の委任範囲なので監査者は配送を代行しない。
- T-05-SCはPLAN:183でlow/acceptと理由を定義済み。C5でpackage導入/依存変更なしを内容確認したが、official auditorのaccept閉鎖条件であるSECURITY.md accepted risks logは未存在。親が正式文書へ保存した後に再確認できる。package auditや承認を捏造しない。
- SUMMARYには専用 `## Threat Flags` 節がない。全文中の実質的な注意はBMAD renderer分類とpending/provenanceで、T-05-02/03に対応する。専用節欠落を「新規脅威0の完全申告」と読替えず、登録外脅威scanも追加しない。
- 公式CLI: `node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs query agent-skills gsd-security-auditor --skills-only` は出力空。公式 `query init.phase-op 5` はphase_found=true、plan_count=1、has_verification=false。project .hermes/skills と .agents/skills は存在せず、初回rg discoveryはこの理由でexit2（CLI検証の失敗ではない）。
- 作成後の表照合: `jq -R -s --slurpfile inventory <S>/t_df0c2ebc-audit-inventory.json 'split("\n") | map(select(startswith("| M | `") or startswith("| A | `")) | split("`")[1]) as $classified | ($inventory[0] | map(.path)) as $expected | {expected:($expected|length), classified:($classified|length), unique:($classified|unique|length),missing:($expected-$classified),extra:($classified-$expected)}' .planning/phases/05-readme-verification-a/05-SECURITY-EVIDENCE.md` はexit0、expected66/classified66/unique66/missing[]/extra[]。
- 本証拠作成後の最終 `git rev-parse HEAD` は同じcc46cf164aeff3ccbf19cbb7489b5be01f486901。`git status --porcelain=v1 --untracked-files=all` はVALIDATION modified、本証拠のみuntracked。`git ls-files --others --exclude-standard` も本証拠のみ。`git diff --numstat HEAD --` は `3\t3\t.planning/phases/05-readme-verification-a/05-VALIDATION.md`。既知禁止guardと `set -o pipefail && git show HEAD:README.md | cmp - README.md` は再実行exit0/空出力。
- 実装ファイル編集、commit/push、branch切替、Kanban操作なし。SECURITY.mdと品質原本の作成・最終添付・受入は親の責任範囲。
