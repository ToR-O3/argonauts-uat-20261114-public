# Phase 8 — 品質の独立確認 CLI 文字原本（整備前・branch比較）

- カード: t_5c607fb0（[フェーズ検証 8]、依頼 r-d78495de、流れ full）
- 実行者: argonauts-uat-quality（Builder の転載ではなく、品質が自分の worktree で実行した出力）
- 実行日: 2026-11-25（JST）
- 判断の根拠: 受付 t_b7fda225 の依頼者判断（日時 2026-11-25T06:53+09:00）原文「確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」
- 対象の種類: **D.5 整備前の依頼branch比較**。最終PRの整備後の確認ではない。

## 1. 対象の身元

| 項目 | 値 | 出典 |
|---|---|---|
| 期待repository | ToR-O3/argonauts-uat-20261114-public | カード固定入力 |
| `git remote get-url origin` | https://github.com/ToR-O3/argonauts-uat-20261114-public.git | 実行出力（期待repoと一致） |
| 基準branch | v112-a | カード固定入力 |
| fetch | `git fetch origin refs/heads/v112-a:refs/remotes/origin/v112-a refs/heads/argonauts/r-d78495de:refs/remotes/origin/argonauts/r-d78495de` → exit 0 | 実行出力 |
| BASE（fetch済み origin/v112-a） | cf407aaa6babebc0a21cf6370530d321b8a615e1 | `git rev-parse --verify 'origin/v112-a^{commit}'` |
| ローカル v112-a（参考。BASEには使わない） | c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 | `git rev-parse --verify v112-a`（origin と違う。更新しない） |
| HEAD_SHA（対象head） | 882b4c60e36a4457c6d504cb07cccc69a03e7130 | `git rev-parse --verify 'HEAD^{commit}'` = origin/argonauts/r-d78495de |
| MERGE_BASE | cf407aaa6babebc0a21cf6370530d321b8a615e1（= BASE） | `git merge-base BASE HEAD_SHA` |
| PR | ToR-O3/argonauts-uat-20261114-public#19：OPEN、draft、isCrossRepository=false、baseRefName=v112-a、baseRefOid=cf407aa…、headRefOid=882b4c6…、changedFiles=61 | `gh pr view argonauts/r-d78495de --json …` |
| start_sha（このフェーズ検証の起点） | 882b4c60e36a4457c6d504cb07cccc69a03e7130 | fetch 直後の `git rev-parse refs/remotes/origin/argonauts/r-d78495de` |

研究で使われた origin/main は使っていない。

## 2. 条件(1) README.md に --min-count 3 の実行例が1つ足されている

コマンド: `git --no-pager diff --no-ext-diff --no-textconv --unified=40 "cf407aa…...882b4c6…" -- README.md`（exit 0）

```diff
@@ -1,35 +1,36 @@
 ```sh
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
 python -m wordfreq input.txt --top 2 --format json
 python -m wordfreq input.txt --format html
 python -m wordfreq input.txt --format html > result.html
 ```
```

（上は該当部分の抜粋。全文 patch は hunk が1つだけで `@@ -1,35 +1,36 @@`、`+` 行は上の1行だけ、`-` 行は0行。hunk は README 全35行を文脈に含み、最終行 `検証A: v1.12 の通しの確かめ（2026-11-22）` も文脈行として変わっていない。）

- `git diff --numstat BASE...HEAD_SHA -- README.md` → `1	0	README.md`
- `git diff --check BASE...HEAD_SHA` の出力に README.md の行は無い（README.md の空白エラーは無い）
- `read_file README.md` で全文を直接読み、使い方の `sh` フェンス内、基本例 `python -m wordfreq input.txt` の直後に `python -m wordfreq input.txt --min-count 3` がちょうど1回あることを確認。既存の4例、説明の箇条、「部品の契約と検証状況」の節、最終行はそのまま。

**判定（1）: 合格**（追加は指定例1行だけ。値・引数は一致し、重複は無く、使い方フェンスの中にある。既存の例・説明・最終行は保持されている）。掲載したコマンドは実行していない（依頼者の判断で、3つの形式での実行の確かめは対象外）。

## 3. 条件(2) 変わったファイルが README.md だけである

コマンド: `git --no-pager diff --no-ext-diff --no-textconv --no-relative --name-status "BASE...HEAD_SHA"`（path の除外なし、exit 0、全61件）。
`--name-only` も61件で、name-status と同じパスの集合。

全件の出力は下の付録Aにある。分類:

| 分類 | 件数 | パス |
|---|---|---|
| 製品 | 1 | README.md (M) |
| 工程の文書 `.planning/` | 34 | 付録A |
| 工程の文書 `_bmad-output/` | 22 | 付録A |
| 工程の文書 `openspec/` | 4 | 付録A |

`.compound-engineering/` と `docs/solutions/` の下に差分は無い。README.md 以外の製品ファイル（実装・試験・設定・依存・workflow）の変更も無い。危険なパスにも触れていない。

作業ツリーの別枠（確認した時点）:
- `git status --short` → 空
- `git diff --name-status` → 空
- `git diff --cached --name-status` → 空
- `git ls-files --others --exclude-standard` → 空

（既存の試験を走らせたとき `uv` が未追跡の `uv.lock` と `wordfreq.egg-info/` を作った。品質が作ったものなので個別に消し、上の空の状態を確認した。）

**判定（2）: 整備前は未達（暫定）**。README.md 以外に工程の文書60件が残っている。工程の文書を除いて合格にはしない。依頼者の判断とPLANのとおり、この条件の最終判定は、後続のPM・最終化がD.5の指定ファイル限定の手順で整備した後、品質が実PRを読み直してから行う。

## 4. 既存の試験（回帰の確認）

`uv run --with pytest python -m pytest -q` → `702 passed in 306.65s`（exit 0、対象head 882b4c6）。製品の実装・試験は変わっていないので、回帰が無いことの確認として使う。受入条件の証拠にはしない。

## 5. 画面

画像は0枚。README の文字だけの変更で、UI・画面の変更は無いため撮影は不要。

## 6. 後続への引継ぎ（D.5 整備後）

1. 後続PM・最終化がD.5の手順で、full の工程原本（PLAN・SUMMARY・この文書・08-VERIFICATION.md）がpush済みで、カードに標準添付されていることを確かめてから、最終PRを README.md だけに整備する。工程の文書を1つずつ消すことで代用しない。
2. 整備後、品質（最終確認）が実PRを読み直し、PR識別子・base branch（期待 v112-a）・base/head の完全SHAを記録する。そのうえで08-01-PLAN.md の「Independent quality / finalization handoff」の4のコマンド（name-status・name-only・README の両原本・README patch・diff --check）を全件文字の原本に保存し、2条件を別々に判定して標準添付する。
3. PMは08-VERIFICATION.md とこの文書を `read_file` で読んでから判断する。
4. この整備前の観測は消さない。整備後の確認は新しい対象として追記するか、別の文字原本にする。
5. 未解決のフラグ（edge 3件 E1〜E3、prohibition 2件 P1・P2）はそのまま残す。2条件の内容判定とは別のもの。

## 7. このフェーズ検証の判定

| 項目 | 結果 |
|---|---|
| 条件(1) README に --min-count 3 の例1つ | 合格 |
| 条件(2) 変わったファイルが README.md だけ | 整備前は未達（暫定）。D.5 整備後の最終確認で判定 |
| GSD verifier（08-VERIFICATION.md） | `status: human_needed`、score 3/4（`gsd_run query verification.status` で読み戻し） |
| Nyquist（08-VALIDATION.md） | validated、nyquist_compliant false（REQ-29 は D.5 後の manual-only） |
| security（08-SECURITY.md） | threats_open 0 |
| コードレビュー（08-REVIEW.md） | clean（同じ head 882b4c6 の実装レビューの原本を再利用。SHA-256 4cc0962a…一致） |
| OpenSpec verify（`.planning/argonauts/t_5c607fb0/openspec-verify.md`） | タスク 2.1 未完了（D.5 後の最終PR確認待ち）の CRITICAL 1件。`openspec validate --strict` は valid |
| UAT（08-UAT.md） | 4項目：1件 blocked（D.5 待ち）、3件 pending（prohibition P1・P2、仮定 E1〜E3。flag は残す） |
| phase 完了 | していない（`phase.complete` は呼んでいない）。next_phase は null（今回の依頼は Phase 8 だけ） |

## 付録A `--name-status BASE...HEAD_SHA` 全出力（61件）

```
M	.planning/INGEST-CONFLICTS.md
M	.planning/REQUIREMENTS.md
M	.planning/ROADMAP.md
M	.planning/STATE.md
A	.planning/argonauts/r-d78495de-learnings.md
A	.planning/argonauts/r-d78495de-manifest.yaml
A	.planning/argonauts/r-d78495de-prd.md
A	.planning/argonauts/t_19c23e10/PLAN-CHECK.md
A	.planning/argonauts/t_19c23e10/api-coverage.json
A	.planning/argonauts/t_19c23e10/gap-analysis.json
A	.planning/argonauts/t_19c23e10/verify-command-paths.json
A	.planning/argonauts/t_19c23e10/verify-failure-directions.json
M	.planning/intel/SYNTHESIS.md
A	.planning/intel/classifications/brief-readme-min-count-3-065f1da5.json
A	.planning/intel/classifications/prd-readme-min-count-3-0ae126e9.json
A	.planning/intel/classifications/proposal-5fd092e7.json
A	.planning/intel/classifications/r-d78495de/brief-readme-min-count-3-065f1da5.json
A	.planning/intel/classifications/r-d78495de/prd-readme-min-count-3-0ae126e9.json
A	.planning/intel/classifications/r-d78495de/proposal-5fd092e7.json
A	.planning/intel/classifications/r-d78495de/tasks-a4097a09.json
A	.planning/intel/classifications/tasks-a4097a09.json
M	.planning/intel/constraints.md
M	.planning/intel/context.md
M	.planning/intel/decisions.md
M	.planning/intel/requirements.md
A	.planning/phases/08-readme-min-count-example/.gitkeep
A	.planning/phases/08-readme-min-count-example/08-01-PLAN.md
A	.planning/phases/08-readme-min-count-example/08-01-SUMMARY.md
A	.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
A	.planning/phases/08-readme-min-count-example/08-CONTEXT.md
A	.planning/phases/08-readme-min-count-example/08-PATTERNS.md
A	.planning/phases/08-readme-min-count-example/08-RESEARCH.md
A	.planning/phases/08-readme-min-count-example/08-VALIDATION.md
M	.planning/state.json
M	README.md
A	_bmad-output/initiative-r-d78495de/brief/.memlog.md
A	_bmad-output/initiative-r-d78495de/brief/.template.md
A	_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.html
A	_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md
A	_bmad-output/initiative-r-d78495de/brief/review-fresh-reader.md
A	_bmad-output/initiative-r-d78495de/brief/review-prose.md
A	_bmad-output/initiative-r-d78495de/brief/review-reconciliation.md
A	_bmad-output/initiative-r-d78495de/brief/review-rubric.md
A	_bmad-output/initiative-r-d78495de/brief/review-structure.md
A	_bmad-output/initiative-r-d78495de/brief/review-update.md
A	_bmad-output/initiative-r-d78495de/initiative-r-d78495de.md
A	_bmad-output/initiative-r-d78495de/prd/.memlog.md
A	_bmad-output/initiative-r-d78495de/prd/.template.md
A	_bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md
A	_bmad-output/initiative-r-d78495de/prd/review-fresh-reader.md
A	_bmad-output/initiative-r-d78495de/prd/review-prose.md
A	_bmad-output/initiative-r-d78495de/prd/review-reconciliation.md
A	_bmad-output/initiative-r-d78495de/prd/review-rubric.md
A	_bmad-output/initiative-r-d78495de/prd/review-structure.md
A	_bmad-output/initiative-r-d78495de/prd/review-update.md
A	_bmad-output/initiative-r-d78495de/review-current.md
A	_bmad-output/initiative-r-d78495de/review-independent.md
A	openspec/changes/r-d78495de-readme-min-count/.openspec.yaml
A	openspec/changes/r-d78495de-readme-min-count/design.md
A	openspec/changes/r-d78495de-readme-min-count/proposal.md
A	openspec/changes/r-d78495de-readme-min-count/tasks.md
```

## 付録B README patch 全出力（unified=40）

```diff
diff --git a/README.md b/README.md
index 0961498..55a5aba 100644
--- a/README.md
+++ b/README.md
@@ -1,35 +1,36 @@
 # argonauts-uat public
 
 Argonauts v1.10 acceptance test repository.
 
 ## wordfreq の実行
 
 リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。
 
 ```sh
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
 python -m wordfreq input.txt --top 2 --format json
 python -m wordfreq input.txt --format html
 python -m wordfreq input.txt --format html > result.html
 ```
 
 HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を標準出力へ書きます。保存時はバイト列をそのままリダイレクトしてください（シェル側で文字コードを変換しないでください）。ファイル名の表示は basename のバイト列を実行環境のファイルシステム文字コードで読み、その文字コードで復号できないバイトだけを置換文字 `�` にします。入力ファイルの読み込みに使うパス自体は変更しません。保存した `result.html` はローカルのブラウザで開けます。HTML は内包 CSS のみの静的文書で、スクリプト・外部フォント・画像・リンク・対話操作はありません。
 
 - `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
 - `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
 - `--format text|json|html` の既定は text。text は `<count>\t<word>\n`、JSON は `word` と整数 `count` の配列に末尾改行1つです。空入力は text が空、JSON が `[]` と改行、HTML が見出し3列・データ0行・総数0です。
 - Unicode の単語文字の連続を抽出し、casefold した語を数えます。日本語の形態素解析は行いません。
 - 全形式で min-count 未満を除外し、回数降順に並べ、同数時は**正規化後の初出順**を保ってから top を適用します。両値は独立で、指定順による違いはありません。これは以前の「同数は語の昇順」からの意図した互換性変更です。`Zoo apple APPLE zoo banana` は min-count2 で zoo2 / apple2、さらに top1 で zoo2 になります。全件除外されたら min-count を下げてください。
 - HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
 - ファイル名と語はテキストとして一度だけ HTML escape し、属性・CSS・URL には使いません。明るい背景固定で、長い語・名前は連続空白・改行・タブを保持して折り返す設計です。
 - 読込み・UTF-8 decode 失敗は stderr と exit1、不正 top・format・引数個数は stderr と exit2。エラー時は stdout を空にし、エラー用 HTML は出しません。
 
 ## 部品の契約と検証状況
 
 `count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。
 
 `format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。
 
 自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
 検証A: v1.12 の通しの確かめ（2026-11-22）
```
