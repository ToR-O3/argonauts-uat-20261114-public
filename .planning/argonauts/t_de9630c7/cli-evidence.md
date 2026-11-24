# フェーズ検証 6 — CLI・CIの証拠（品質 t_de9630c7）

- 確認した対象: head `34eb0bb03d285843561faf567fa6cef4a4cd141c`（= origin/argonauts/r-5f8197e8 = ToR-O3/argonauts-uat-20261114-public#14 の headRefOid、OPEN・draft・同じrepo）。これが start_sha。
- 依頼基点: `2437aa3445ecdb87e7a11fe7a1c0e196726a5af4`（= origin/v112-a、HEADの祖先）。
- 報告を保存するcommitは、この確認の後に `.planning/` だけで作る別のcommit（確認対象のSHAとは別）。
- 判断の根拠（受付 t_dbab0a34 のコメントを run 37 の始めに再読）:
  - 範囲判断 2026-11-24T21:20+09:00「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」
  - 最新判断 2026-11-24T13:09:04.816724+00:00「Aに近いが、人の側では状態の修復をしない。進捗の照会が古い値を返すのは手続きの食い違いなので、保存済みの計画をそのまま使って、先（割振り・実装）へ進めてよい。」
- 画像: 0枚。README の文字1行の変更で、画面・動作の確認は依頼者判断により対象外。

## 条件ごとの実行と結果

| # | 条件 | 実行したコマンド | 結果 | 判定 |
|---|---|---|---|---|
| 1 | README.md に `--min-count 3` の例が1つ足されている | `git diff --no-ext-diff --no-color 2437aa3 HEAD -- README.md` | 通常例 `python -m wordfreq input.txt` の直後に `+python -m wordfreq input.txt --min-count 3` の1行だけ（numstat 1/0） | 満たす |
| 1 | 〃（独立期待との一致） | `cmp _bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/README.expected.md README.md` | exit0 | 満たす |
| 1 | 〃（基点の原本） | `git show 2437aa3:README.md \| cmp - …/README.request-base.md` | exit0 | 一致 |
| 1 | 〃（空白・改行） | `git diff --check 2437aa3 HEAD -- README.md` | exit0。末尾「検証A: v1.12 の通しの確かめ（2026-11-22）」を保持（read_fileで全36行を確認） | 満たす |
| 1 | 〃（回数） | `grep -c -- 'python -m wordfreq input.txt --min-count 3$' README.md` | 1 | 満たす |
| 2 | 変わったファイルが README.md だけ | `git diff --name-status 2437aa3 HEAD` | 84件（A 72 / M 12）。README.md 1、`.planning/` 49、`_bmad-output/` 30、`openspec/` 4 | **未達（現時点）** |
| 2 | 〃（製品の禁止範囲） | `git diff --exit-code 2437aa3 HEAD -- wordfreq tests tools pyproject.toml .github` | exit0（変更なし）。`.github/workflows/` の変更なし | README以外の製品変更なし |

条件2は、工程文書を除いて数えて「README.mdだけ」とは判定しない。必要な原本の添付保全の後、最終化が工程差分を基準branch相当へ戻し/外し、品質の最終確認で最終PRの全差分を取り直して再判定する（後工程の責務）。

## CI（1回だけ読取り、待たない）

`gh api "repos/ToR-O3/argonauts-uat-20261114-public/actions/runs?head_sha=34eb0bb…"`:
- 45402522159 pytest completed **success**（pull_request）
- 45402462563 pytest completed **success**（push）
受付・自分のカードにCI失敗のコメントは無い。pytestの手元実行は依頼者判断で対象外のため行っていない。

## GSD・OpenSpec

- `gsd_run query init.execute-phase 6`: plan_count 1、incomplete_count 0（全PLANにSUMMARY）。
- verify:post の activeHooks に nyquist（validate-phase）と security（secure-phase）が揃う。設定は既に有効（config-path はこのworktreeの `.planning/config.json`）。一時変更なし。
- Nyquist（gsd-validate-phase 6）: `06-VALIDATION.md` status validated、nyquist_compliant false（REQ-25 COVERED、REQ-27の最終README-onlyはmanual-only）。
- Security（gsd-secure-phase 6）: `06-SECURITY.md` threats_open 0、status verified。
- code-review フック: 同じhead 34eb0bb の実装レビュー（t_5e02213b、06-REVIEW.md 添付45、必須0件）を再利用。
- 公式 gsd-verifier（delegate_task）: `06-VERIFICATION.md` status **gaps_found**、score 4/5。gap は条件2のみ。`gsd_run query verification.status` → gaps_found / route plan-phase。
- phase.complete は呼んでいない（gaps のため）。GSD状態の古い値は承認済みの例外として修復していない。
- OpenSpec: `openspec validate --strict` exit0。詳細は `openspec-verify.md`。
