# 07-01 品質差戻し対応: shallow checkout

## 対象と判断

- 元head: a2bb38361dd9b9f589992142645c78c96e977863。
- PR: ToR-O3/argonauts-uat-20261114-public#24。品質run128の必須指摘1だけを修正。
- 判断日時: 2026-11-25 21:22。人defaultの元カードコメント「変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。」を継続適用。受付の引継ぎも再読した。
- 原因: CI run45616390808の失敗ログを取得して読んだ。検証ツールstart_blobsが毎回 `git show 8efbfaa1907ace272a4f685e2659144a4085d303:<product>` を呼び、浅いcheckoutでexit128となる。製品動作の失敗ではない。

## 先行REDと修正

- `test_saved_evidence_without_git_history[baseline,red]` を先に追加。外部プロセスを禁止するmonkeypatchで実際の保存済み原本の検証を行う。成功応答の捏造はしない。
- `/usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k without_git_history -q`: **2 failed, 12 deselected**, exit1。両方がstart_blobsのGit読取りによる意図したAssertionError。原本 `red.txt`。
- 起動当初のpython3と/usr/bin/python3ではpytestがimportできなかった。既設の `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages` を設定し、pytest9.0.3を確認後に上記REDを採取した。依存追加なし。
- 開始commitの6製品ファイルを実際に `git show <START>:<path> | sha256sum` で計算し、既存baseline/provenance.jsonの全6値と一致を確認。その値をstart_blobsの固定辞書に保存した。現在の製品や検証対象のmanifestから値を導かず、検証の独立した比較値を維持する。
- 読取り検証でGit履歴を要求しない。captureの上書き禁止、製品編集検知、baseline/REDの保存済みハッシュ・argv・内容の検査は維持。
- `/usr/bin/python3 -m pytest tests/test_max_count_verifier.py -q`: **14 passed**, exit0、0.66秒。原本 `green.txt`。

## 実際の浅いcloneでの全試験

管理scratch内の専用ディレクトリへ `git clone --depth 1 --no-hardlinks --branch wt/t_87068596 file://<worktree> <scratch>` を実行。clone元のheadはa2bb383、修正した2ファイルだけをコピーした。

- `git -C <scratch> rev-parse --is-shallow-repository`: **true**。
- `git -C <scratch> cat-file -e 8efbfaa1907ace272a4f685e2659144a4085d303`: **exit1**、開始commitが不在。
- clone側とworktree側の修正ファイルSHA-256一致:
  - tools/verify_wordfreq_max_count.py: a922bb95ed1c16c0c2f5973510af178a7e7537082d83ff54777e9d8edd1c42f6
  - tests/test_max_count_verifier.py: bb523e872eb881bde00ca865126dd3f8c79f3776fef397a3b129e420c8975c01
- cloneをcwdとして `/usr/bin/python3 -m pytest tests/ -q --junitxml=<worktree>/.planning/argonauts/r-d4bcda40/builder/07-01/rework/shallow-full.xml` を実行。
- **999 passed in 186.28s**, exit0。失敗・ERROR・skipなし。stdout全文 `shallow-full.txt`、JUnit原本 `shallow-full.xml`。
- Python3.12.15、pytest9.0.3、PYTHONPATHは上記の既設パス、TMPDIRはProfile管理scratch。CI結果ではなく、実際の浅いcloneでのローカル全suite結果。

## 範囲と引継ぎ

- 製品コード、README、依存、workflow、OpenSpecチェックは変更なし。
- baseline/先行REDの原本は変更・再採取せず、開始headも付け替えない。
- SUMMARYとSTATE/ROADMAPは既にPLAN07-01完了・phase7/plan2/全3を記録済み。差戻し修正のためadvance/updateを重ねず、07-02以降は実行しない。
- 品質の任意提案WR-01/WR-02/IN-01〜03は今回の必須差戻しと混ぜて変更していない。後続で必要ならPMが判断する。
- GitHubの新headのCI結果はpush後に有限回読んだ結果をKanban引継ぎへ記録する。過去a2bb383のCI失敗を新headの結果として扱わない。
- 品質による新headの独立確認と、後続README/OpenSpec1.3・2.1集約・2.2は未完了のまま。
