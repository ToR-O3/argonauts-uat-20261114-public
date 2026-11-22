# Phase 05 independent quality handoff

指定文字列の掲載は通し検証の実施・合格認定ではない。
Builder判定と独立品質・添付配送・PM受入は別。品質は実行までpending。画像0枚（README文字・バイト・Git差分だけが対象。製品画面・HTML変更なし）。

## Fixed identity

- B_doc: `54106df87baa6cc017167eb311fd0fd4f81ea0fa`、既存README4643 bytes / 34 LF行 / 最終0a。
- B_request: `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`、initiative b95d7b8の親。
- H_impl: `5863f7a0ff635dd3bb697c597bf6cf0f6d5a601e`（README・task1文字証拠・OpenSpec1.1を確定）。
- H_report: 後続SUMMARY/状態commitを含む配送head。確定後のKanban metadataを読む。自己commit SHAを本書へ書かない。
- repo: `ToR-O3/argonauts-uat-20261114-public`、配送先 `argonauts/r-8ac79daf`。Builder localはwt/t_28db1326、計画時wt/t_8a90bad6ではない。

## Required independent procedure

1. E.4/品質skillに従いPR・remote・作業HEADを照合し、対象H_reportを固定。BuilderのC1-C6結果は参考のみ、品質自身が同じ対象headで再実行する。README全文、Builder CLI文書、SUMMARY、PLANを読む。
2. H_impl..H_reportの全patchを読み、README不変・工程文書だけであることを内容で判定する。変更が増えれば全パスを再分類し、新しいheadで検証。旧headの合格を転記しない。
3. 実行するシェルで `set -o pipefail` を有効化。下記の各行を個別tool呼出しで実行し、完全argv/cwd/環境（秘密なし）・stdout/stderr・raw exitをその場で記録する。pipelineの上流失敗も非0なら停止。grep0のみ一致、1不一致、2以上エラー。cmp0のみ一致、1差分、2エラー。guard0のみ不変。後の成功で前の非0を覆わない。

### C1-C4 (PLANの原文、品質が独立実行)
```sh
tail -n 1 README.md | grep -Fx -- '検証A: v1.12 の通しの確かめ（2026-11-22）'
git show 54106df87baa6cc017167eb311fd0fd4f81ea0fa:README.md | cmp -n 4643 - README.md
printf '%s\n' '検証A: v1.12 の通しの確かめ（2026-11-22）' | cmp -i 0:4643 - README.md
git diff --no-ext-diff --no-textconv --no-color --unified=3 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
git diff --numstat 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
git diff --check 54106df87baa6cc017167eb311fd0fd4f81ea0fa -- README.md
```
C1完全一致、C2既存全prefix、C3suffix全体が指定行+LFのみで全て0を要求。C4は全patchを読み追加1/削除0・末尾hunkのみ・mode不変を確認。表示exit0を内容合格にしない。

### C5-C6 (PLANの原文、品質が独立実行)
```sh
git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD
git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 HEAD
git diff --no-ext-diff --no-textconv --no-color c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 --
git status --porcelain=v1 --untracked-files=all
git ls-files --others --exclude-standard
git diff --exit-code c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 -- wordfreq tests tools pyproject.toml .github
git rev-parse HEAD
git show HEAD:README.md | cmp - README.md
```
commit済みとindex/worktree全patchを省略せず読む。status/未追跡は全パスの原本内容をread_fileし、製品README・工程仕様・工程計画・工程検証・工程状態に分類。既知guardだけでは未知パスを保証しない。工程配下の検証コード追加も拒否する。upstream state.json等をBuilder新規作業と誤認しない。
既存BMADのbrief HTMLは仕様文書の生成表示ビューであり、wordfreq製品HTMLではない。内包のrenderer JS/CDN参照も内容を読む。製品コードや新しい検証スクリプトへの利用を許可せず、必要な危険の印は品質自身が判断する。

## Quality outputs / delivery

品質の後工程出力を次の文字原本に固定する。Builderは作成も代理合格認定もしない。
- `.planning/phases/05-readme-verification-a/05-VERIFICATION.md`
- `.planning/phases/05-readme-verification-a/05-QUALITY-CLI.md`

VERIFICATIONにはREQ-22/23/24の要件→独立判定→CLI原本参照表、covered files、B_doc/B_request/H_impl/品質検証head/H_report、非認定文言、画像0枚と理由を記録。CLI文書には各コマンド完全argv/cwd/環境/stdout/stderr/raw exit、README全patch、全変更と未追跡の内容分類を自身の実結果で残す。実際に画像を閲覧した場合は枚数・確認内容・結果も文字に書く。

品質はこの2原本を自分のカードへ標準 `kanban_attach` で添付する。filenameを05-VERIFICATION.mdおよび05-QUALITY-CLI.md、content_base64をそれぞれ `argonauts:worktree:.planning/phases/05-readme-verification-a/<文書名>` とする。`kanban_attachments`で返った添付ID・保存名・stored_pathを読む。原本と添付のSHA-256をsha256sumで照合し、添付した正確なstored_pathの両文書をread_fileで全文読戻す。PMが文字原本だけで確認できるようにする。画像・圧縮物を開かせない。添付不能・未読・不一致は未配送として残し、passedに変換しない。

報告直前にC6を再実行し対象headを再照合する。品質報告commitを作るphase検証工程では製品検証headと報告headを別記し、工程差分だけか再確認する。同一カード実装レビュー中はcommit/pushしない（E.4）。phase検証カードで報告を確定する。descriptorless prohibitionはflagged-unverifiedのまま、品質が非認定文言の内容を明示レビューする。probeのunresolvedを勝手に解除しない。
