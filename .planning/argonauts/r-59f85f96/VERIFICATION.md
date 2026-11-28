# 確認の記録 r-59f85f96（light・手順版1.14）

- 依頼: r-59f85f96 — README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 5 --format text` を1行足す。変えるのは README.md だけ（製品範囲）。
- 対象head（今回の試験対象）: 3e68d321efd99b1d2584e485f823db40c65e2f51（ローカルHEAD・origin/argonauts/r-59f85f96・PR ToR-O3/argonauts-uat-20261114-public#49 の headRefOid が一致。OPEN・ready・同一repo）
- 基準: origin/v112-a cf95bfc5fed6c5fab2ccc72690670671e22e2fbd
- 訂正: 旧確認 t_f7e7b127（対象head 6a66bc8）の39行の再試験が `<13語の入力ファイル>` という実行できない書き方だったため、確認 t_52302528 で最新headの受入確認をやり直し、再試験の行を実行したコマンドそのものに直した（PM判断 t_ffdd6d3f の A）。
- 依頼者の判断: 受付に `argonauts: 依頼者の判断` のコメントは無い（judgement_at なし）
- 判定: passed

## 受入条件ごとの確認（作業場所: カードのworktreeのルート）

1. 指定行が「wordfreq の実行」のコード例にある
   - `rg -F -x -c -- 'python -m wordfreq input.txt --top 5 --format text' README.md` → 1（終了0）。`git show origin/v112-a:README.md | rg -F -x -c -- '<同じ行>'` → 該当なし（終了1）。
   - 位置: ```sh ブロック内、`--top 3 --format text` の直後、`--format html` の前。
2. 既存の記述を保つ
   - `git diff --numstat origin/v112-a...HEAD -- README.md` → `1	0	README.md`（+1/-0）。
3. 製品の変更は README.md だけ
   - `git diff --name-status --no-renames origin/v112-a...HEAD` 全29件（旧確認の27件＋この後の記録・archive）。
   - 製品の変更：README.md（1件）。工程の文書：24件（.planning 12・openspec 4・_bmad-output 8、判定の対象外）。
   - 記録（提案）：`_bmad/` の4件（pick_methods.py・tickets.py の追加、.gitkeep 2件の削除）は計画commit b5ff3d2 のBMAD公式setup修復で、wordfreq の製品コードではない。
   - 危険なパス・`.github/` の変更：無し（`git diff --name-only origin/v112-a...HEAD -- openspec/specs .github` → 0件）。
   - 6a66bc8 から 3e68d32 までの差分は `.planning/argonauts/r-59f85f96/` の2件と OpenSpec の archive への移動だけ。README・コード・試験は不変。
4. 実際の実行（実CLI）
   - 入力: 作業場所のルートで、`$TMPDIR/r-59f85f96-input.txt` に次の13語1行を書く（apple×4・banana×3・cherry×2・date×2・egg・fig）。
     `apple apple apple apple banana banana banana cherry cherry date date egg fig`
   - 結果: `4 apple / 3 banana / 2 cherry / 2 date / 1 egg` の5行（タブ区切り）、exit 0。`wc -w` → 13。
5. 既存の試験
   - `uv run --no-project --python 3.12 --with pytest python -m pytest -q` → 702 passed in 184.27s（終了0）。

## GSD Quick と OpenSpec

- 引き継いだQuick: `.planning/quick/261128-j9i-r-59f85f96-readme-wordfreq-top5-text-exa`（Quickは再起動しない）。
- `gsd_run query verification.status <上のQuick>` → `status: stale`、`moved_files: openspec/changes/r-59f85f96-light/tasks.md`。原因は公式archiveによる tasks.md の移動だけ。6a66bc8 の移動前と HEAD の archive 先で4ファイル（.openspec.yaml・design.md・proposal.md・tasks.md）のblobが全て一致（tasks.md c8e8322）。検証済みの内容は変わっていない。
- STATE.md 117行の Quick Tasks Completed に 261128-j9i（beae459、Verified）の行がある。
- OpenSpec: `openspec/changes/archive/2026-11-28-r-59f85f96-light/`（skip_specs: true）、tasks.md の `[x]` 1件・`[ ]` 0件。`openspec validate --specs` → 2 passed, 0 failed。正本 openspec/specs の差分0件。

## 再試験（最終headで繰り返すコマンド。作業場所はworktreeのルート）

再試験: rg -F -x -c -- 'python -m wordfreq input.txt --top 5 --format text' README.md
再試験: git diff --numstat origin/v112-a...HEAD -- README.md
再試験: git diff --name-status --no-renames origin/v112-a...HEAD
再試験: printf '%s\n' 'apple apple apple apple banana banana banana cherry cherry date date egg fig' > "$TMPDIR/r-59f85f96-input.txt" && uv run --no-project --python 3.12 python -m wordfreq "$TMPDIR/r-59f85f96-input.txt" --top 5 --format text
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q

## 学びの候補

- 再試験の行には入力の作り方まで含む実行可能なコマンドを書く（プレースホルダーは最終確認で再現できない）。
- 受付の工程文書の場所に `_bmad/` が無いと、公式setupの修復が製品範囲の判定で毎回議論になる。
