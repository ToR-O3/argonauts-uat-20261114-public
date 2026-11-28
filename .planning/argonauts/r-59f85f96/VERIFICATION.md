# 確認の記録 r-59f85f96（light・手順版1.14）

- 依頼: r-59f85f96 — README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 5 --format text` を1行足す。変えるのは README.md だけ（製品範囲）。
- 対象head: 6a66bc88de224d985556f8a37ce9d4d51defc3e3（ローカルHEAD・origin/argonauts/r-59f85f96・PR ToR-O3/argonauts-uat-20261114-public#49 の headRefOid が一致。OPEN・draft・同一repo）
- 基準: origin/v112-a cf95bfc5fed6c5fab2ccc72690670671e22e2fbd
- 依頼者の判断: 受付に `argonauts: 依頼者の判断` のコメントは無い（judgement_at なし）
- 判定: passed

## 受入条件ごとの確認

1. 指定行が「wordfreq の実行」のコード例にある
   - `rg -F -x -c -- 'python -m wordfreq input.txt --top 5 --format text' README.md` → 1（head）。基準の README.md では 0（rg 終了コード1）。
   - 位置: `## wordfreq の実行` の ```sh ブロック内、`--top 3 --format text` の直後、`--format html` の前。
2. 既存の記述を保つ
   - `git diff --numstat origin/v112-a...HEAD -- README.md` → `1 0 README.md`（+1/-0、削除・変更なし）。
3. 製品の変更は README.md だけ
   - `git diff --name-status --no-renames origin/v112-a...HEAD` 全27件を確認。
   - 製品の変更：README.md（1件）。工程の文書：22件（.planning 10・openspec 4・_bmad-output 8、判定の対象外）。
   - 記録（提案）：`_bmad/` の4件（core-tools/scripts/pick_methods.py・method/scripts/tickets.py の追加、同ディレクトリの .gitkeep 2件の削除）は計画のcommit b5ff3d2 で入ったBMAD公式setupの修復で、wordfreq の製品コードではない。承認済みの要求原本（_bmad-output/initiative-r-59f85f96/prd/prd-light-wordfreq-text-example.md 42行）が「工程用 `_bmad` 修復差分」として製品ファイルと区別している。受付の工程文書の場所の一覧には `_bmad/` が無いため、最終確認とPMの目に入るよう記録する。
   - 危険なパス・`.github/workflows/` の変更：無し。
4. 実際の実行（実CLI）
   - 13語の入力ファイル（scratch）で `uv run --no-project --python 3.12 python -m wordfreq <input.txt> --top 5 --format text` → `4 apple / 3 banana / 2 cherry / 2 date / 1 egg` の5行（タブ区切り）、exit 0。
5. 既存の試験
   - `uv run --no-project --python 3.12 --with pytest python -m pytest -q` → 702 passed in 154.08s（CIと同じ Python 3.12 と pytest）。

## GSD Quick と OpenSpec

- `gsd_run query verification.status .planning/quick/261128-j9i-r-59f85f96-readme-wordfreq-top5-text-exa` → status: passed。
- STATE.md の Quick Tasks Completed に 261128-j9i（beae459、Verified）の行がある。
- OpenSpec `status --change r-59f85f96-light --json` → isComplete: true（proposal・design・tasks done、specs skipped）。
- OpenSpec `validate r-59f85f96-light --strict` → valid（skip_specs: true）。tasks.md 1/1 完了。
- `git diff --name-only origin/v112-a...HEAD -- openspec/specs` → 0件（正本は不変）。

## 再試験（最終headで繰り返すコマンド）

再試験: rg -F -x -c -- 'python -m wordfreq input.txt --top 5 --format text' README.md
再試験: git diff --numstat origin/v112-a...HEAD -- README.md
再試験: git diff --name-status --no-renames origin/v112-a...HEAD
再試験: uv run --no-project --python 3.12 python -m wordfreq <13語の入力ファイル> --top 5 --format text
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q

## 学びの候補

- 受付の工程文書の場所に `_bmad/`（フレームワークの置き場）が無いと、公式setupの修復が製品範囲の判定で毎回議論になる。工程の置き場の一覧に `_bmad/` を含めるか、修復を初期化で済ませることを検討する。
