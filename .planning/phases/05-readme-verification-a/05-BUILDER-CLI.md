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

全依頼差分分類・C5/C6・C1-C4再実行はtask1確定後に追記する。現時点で実施済みとはしない。
