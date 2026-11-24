# Phase 08 Builder CLI — original text evidence

## Authority / identity

- Request r-d78495de, task t_6cbb9153, PLAN 08-01 only, full flow; Task1 → Task2 sequential.
- Latest reception judgement: 2026-11-25T06:53+09:00.
- 原文: 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。
- Expected repository (card): ToR-O3/argonauts-uat-20261114-public; base branch v112-a; origin https://github.com/ToR-O3/argonauts-uat-20261114-public.git matched by git remote -v. Delivery branch argonauts/r-d78495de; local branch wt/t_6cbb9153. All commands run at this card worktree root.
- EDIT_BASE=e18a818a6cc2f6cc37e7f320998c0f6c005e91da (fixed before README edit; not moving HEAD).
- Start: 2026-11-24T23:04:22Z. Initial git status --porcelain: empty; reflog branch: Created from HEAD. Standard checkout aligned to origin/argonauts/r-d78495de. Fetch and base merge exit0 / Already up to date. Workflow difference empty. GH authentication available (credential values not retained).
- Official execute-plan read from active profile gsd-core/workflows/execute-plan.md; card referenced generic home path absent, PLAN execution_context supplied the real installed profile path. Official runtime launcher sourced in same terminal as gsd_run. init.execute-phase 8: one runnable incomplete 08-01-PLAN.md, no summaries. STATE Current Position Phase8, Current Plan1, Total1, Ready to execute matched selected plan. begin-phase --phase 8 --name 'README min-count example' --plans 1 returned phase8/plan_count1 and updated execution state. Inline Pattern C (2 tasks <= threshold3), SEQUENTIAL=true by card marker; no child executor/next PLAN.

## Task1 RED — natural absence, not command failure

Before editing, read_file README.md full 35 lines/4696 bytes and git show e18a818a6cc2f6cc37e7f320998c0f6c005e91da:README.md full output were read. git diff HEAD -- README.md empty; tracked eol i/lf w/lf. Commands returned exit0, stderr empty. Usage lines 9–15 contained basic input.txt, min-count2/json and html examples, but no `python -m wordfreq input.txt --min-count 3`. Therefore REQ-28 content FAIL before edit. This is manual direct-reading failure, not fabricated nonzero exit or missing environment. Existing final line was 検証A: v1.12 の通しの確かめ（2026-11-22）.

## Task1 GREEN — direct reading

Inserted exactly `python -m wordfreq input.txt --min-count 3` after the basic invocation inside the existing sh fence. Read_file full resulting README: 36 lines/4739 bytes, requested line11; old min-count2/json, top/json, html examples still present in order; all option explanations and last line36 retained. Full unified40 patch read: one added line only, no removed line, no EOF-newline marker or mode change. numstat `1\t0\tREADME.md`; eol remains i/lf w/lf. diff --check empty, exit0. Display success is not the content judgement; full originals and patch support Builder REQ-28 GREEN. No new verifier/test, product invocation, dependency/config/tool/code changes. Existing text/json/html execution is excluded, not pending.

The following command transcript retains actual full stdout plus raw exit. Unless specifically shown, stderr was empty in terminal result (error=null). Git display exit0 never by itself means acceptance. Initial original remains reproducible at fixed EDIT_BASE; the full patch includes unchanged README context.

## Task1 actual verification transcript

```text
$ git diff --no-ext-diff --no-textconv --unified=40 e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
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
raw exit=0
$ git diff --numstat e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
1	0	README.md
raw exit=0
$ git diff --check e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
raw exit=0
```
