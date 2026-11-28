# 確認の記録 r-ba687bc1（light・手順版1.14）

- 依頼: README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 5 --format text` の1行を足す。変えるのは README.md だけ。
- 依頼者の最新判断: 受付に `argonauts: 依頼者の判断` のコメントは無い（受付PMの受付判断のみ）。
- 対象: ToR-O3/argonauts-uat-20261114-public#51（OPEN・draft）、試験したhead `c316b91bb03981c86d28a401056631c792a761f2`
- 照合: ローカルHEAD = origin/argonauts/r-ba687bc1 = PRのheadRefOid = c316b91。基準 v112-a（cf95bfc）は取込み済み。
- 判定: 合格

## 受入条件ごとの確認

1. 「wordfreq の実行」のコード例に指定の1行がある
   - `git diff origin/v112-a...HEAD -- README.md` → `--top 3 --format text` の直後に1行追加。見出し「## wordfreq の実行」（5行目）のコードブロック（9〜24行目）内。
   - `git show HEAD:README.md | rg -F -x -c -- 'python -m wordfreq input.txt --top 5 --format text'` → 1
   - 同じコマンドを基準 `origin/v112-a` で → 0件（終了コード1）
   - 結果: 満たす
2. 製品の変更は README.md だけ、既存の例・コード・設定・依存を変えない
   - `git diff --numstat origin/v112-a...HEAD -- README.md` → `1 0 README.md`（既存行の削除・変更なし）
   - 工程文書の場所を除いた変更ファイル → `README.md` だけ
   - 製品の変更：README.md（+1/-0）。工程の文書：21件（判定の対象外）。
   - 危険なパス・`.github/workflows/` の変更: なし
   - 結果: 満たす
3. 追加した実行例が実際に動く
   - 人工の入力（apple×6, banana×5, cherry×4, date×3, elder×2, fig×1）で
     `python -m wordfreq input.txt --top 5 --format text`（Python 3.12、PYTHONPATH=作業場所）
   - 結果: `6 apple / 5 banana / 4 cherry / 3 date / 2 elder` の5行（タブ区切り）、exit 0

## 既存の試験とCI

- 再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q
- 結果: 702 passed in 154.79s
- CI（Actions pytest、head c316b91）: completed / success（2件とも）

## GSD QuickとOpenSpec

- `gsd_run query verification.status .planning/quick/261128-v63-add-the-requested-top-5-text-command-to-` → status: passed
- Quick VERIFICATION.md: status passed、3/3 must-haves。STATE.md の Quick Tasks: 261128-v63 Verified
- `openspec status --change r-ba687bc1-light --json` → isComplete: true（specs は skip_specs で skipped）
- `openspec validate r-ba687bc1-light --strict` → valid（skip_specs、差分0件を許容）
- `openspec instructions apply --change r-ba687bc1-light --json` → tasks 1/1 完了
- openspec-verify-change: 完全性 1/1 tasks、正しさ Not applicable（skip_specs）、整合性 design の決定（top3・textの直後に1行、他は変えない）に一致。CRITICAL・WARNING なし。
- 正本 `openspec/specs` の基準からの差分: なし

## 学びの候補

特になし
