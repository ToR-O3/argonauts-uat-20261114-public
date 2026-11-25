# 07-02 実装確認の記録

依頼 r-d4bcda40、カード t_f0f6e566、指定PLAN07-02のみ。起点は親の品質確認済み `0012db4060977bd5afeb07f12e36b857c1e6a882`。製品コード変更0。証拠rootは本書と同じディレクトリ。

## 判断と範囲

参照判断: 2026-11-25 21:22（JST）、t_87068596のdefault（人）のコメント created_at=1795609328。受付t_bcdd7392の引継ぎと `../07-01/decision.md` を照合した。

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

画像取得・画像比較・ブラウザー実測を実施/合格としない。今回のHTMLは既存の全形式試験で単語・回数・総数・空状態・構造を検査する。独立品質と文字証拠添付は後続に残す。1.1の先行REDは親の原本を保持し、今回の追加変異を代用しない。

## 環境と実行方法

- Linux 6.18.58.1-microsoft-standard-WSL2、CPython `/usr/bin/python3` 3.12.15、pytest既存環境。
- 全stageはrepo rootから `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 .planning/argonauts/r-d4bcda40/builder/07-02/run_stage.py <stage> <pytest引数>` で有限実行した。
- `run_stage.py` は前PLANの記録方法を同PLANの証拠ディレクトリ内へ複製し、出力先だけ07-02に変更。各stageの `command.json` に実argv/cwd/許可した環境、`result.json` に実head/Python/製品6件の実行前後SHA-256/件数/時間/exit、`stdout.txt`/`stderr.txt`/`junit.xml` に無加工原本、`test_cli.py.original` にその時点の試験を保存した。
- terminalにはHERMES_KANBAN_TASKが渡っていないため、resultのtask欄はnullのまま保存した。カード帰属は本書に明示し、実測値を改変しない。

## 実行結果

| stage | 正確なpytest引数（後ろに実JUnit出力先を追加） | 実結果 / wall秒 |
|---|---|---|
| 前提oracle/RED読取り | tests/test_max_count_verifier.py -k 'saved_baseline or saved_preimplementation_red' -q | 2成功、exit0、0.12秒（terminal実出力） |
| precondition | tests/test_cli.py -k 'max_count_empty or max_count_invalid_before_read or max_count_input_failure or max_count_read_only' -q -x | 129成功、exit0、5.521356699秒 |
| mutations | tests/test_cli.py -k max_count_empty_exit_discrimination -q -s | 4成功/4失敗、exit1、9.006907205秒。試験側のJUnit属性誤認。製品REDに数えない |
| mutations-green | 同上 | 8成功、exit0、8.889100510秒 |
| exits | tests/test_cli.py -k 'max_count_empty or max_count_invalid_before_read or max_count_input_failure or max_count_read_only' -q -x | 137成功、exit0、12.691700308秒 |
| cli-task1 | tests/test_cli.py -q -x | 649成功、exit0、57.488068019秒 |
| red | tests/test_cli.py -k max_count_readme_example -q -x | 1失敗、exit1、0.619013232秒。掲載commandの出現0対期待1 |
| green | tests/test_cli.py -k 'max_count_readme_example or max_count_help' -q -s | 2成功、exit0、0.473428516秒 |
| full | tests/ -q | 1008成功、exit0、217.374637236秒 |

成功stageの失敗/ERROR/skipはすべて0。全suiteのpytest表示時間は216.93秒、記録器のwallは217.374637236秒。CLI/全suiteは30秒を超え、高速とは主張しない。

## 受入条件と判別力

- 正常空exit0: 07-01で先行作成済みの `test_max_count_empty` はmax0/-1/負大整数/逆転/単語1つ/空/空白/記号/全除外の全形式を検査。text空、JSON []+LF、HTMLデータ0行/元total7・1・0・5と固定空文言を照合。
- 入力失敗exit1: `test_max_count_input_failure` はmax0/-1/逆転とmissing/directory/decode/permission×全形式。permissionは同一実効ユーザーの実readでPermissionErrorを確認しfinallyでchmod復元。skip/mock代用なし。
- 読取り前usage exit2: `test_max_count_invalid_before_read` はmax欠落/abc/1.5とmin/top不正の組合せ。read spy未呼出しと実subprocess両方を検査。stdout空/通知stderr/Tracebackなし。
- 追加単一変異4件: 製品を変更せず管理scratchのcold packageだけへ(1)max正値制約、(2)逆転エラー、(3)空集合の入力取得短絡、(4)既存usage検証を入力取得後へ移動、を別々に注入。`mutations-green/stdout.txt` に全inner報告を保存。各変異は狙ったAssertionErrorでexit1、各未変異対照はexit0。max正値/逆転は2対期待0、短絡は0対期待1、usage後回しはread spy呼出しを検出。これらは実装後の判別力であり、1.1未実装時REDと区別する。
- 初回変異検査ではpytestのJUnit failure要素にtype属性が無いため外側4件が失敗。実JUnit本文のAssertionErrorと固有失敗文言・errors/skip0・件数を検査するよう試験だけ修正し、8件すべて成功。初回原本も残した。
- README先行RED: README未編集で `test_max_count_readme_example` が掲載例欠落のassertで失敗。`red-evidence.json` と公式 `red-classifier.json` はpassed=true / RED_EVIDENCE_OK / target_test_failedを確認。ERRORやfixture事故をRED扱いしていない。
- READMEは指定の新コマンド1つ、同節の入力/固定JSON、整数全域/None/包含/min併用/正常空/上限調整/元HTML総数だけを追加・修正。旧7コマンドの連続ブロックと末尾検証B行は試験で保持。
- `green/stdout.txt` は実argvのfilenameがinput.txtで、入力 `beta beta beta alpha gamma alpha delta`、stdout `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]` + LF1つ、exit0・stderr空を記録。単なるREADME文字列確認ではない。helpも再確認。
- 全suiteは包含/積集合/元Counter・元総数/共通pairs/初出順/top前選択/選択後top10/Unicode/保存bytes/静的安全性/読取り専用を含む。

## 差分と証拠帰属

`git diff --exit-code 0012db4 -- wordfreq .github pyproject.toml` はexit0。製品6件・formatter/API/CSS/依存/CIは本PLANでは変更0。tests/test_cli.pyは102追加・削除0。READMEは新例と直接関連文だけ。封印baseline/親RED原本も変更していない。

full実行時headは `288e9162d5c22d2d804623db7d3d1f59a3633f53` ＋未commit README差分。試験はこのheadの試験に一致。検証済みREADMEのSHA-256は `43f1a6a69cd3aa616bd715e513f4913875f5c2ba0ef85907c98769787c318d68`、tests/test_cli.pyは `8dbe95e0bd71bdf585e7a3275c63ab1308a6af9d7f0f8770b4684f38377343da`。製品SHAは各stage resultへ記録。後の記録commitへ実行headを付け替えない。

OpenSpec1.1/1.2の既存チェックを保持し、実際に完了した1.3だけ今回チェックする。2.1のこのPLANの全試験は成功したが、07-03の最終scope/全体記録が残るので集約チェックは保留。2.2は独立品質まで未完了。

この記録時点のPRは同repo OPENのToR-O3/argonauts-uat-20261114-public#24（親head）。push後に新headを照合し品質へ渡す。新headのCIは未確認であり、ローカル成功からCI成功を推測しない。phase.complete/次PLANの実行/PR Ready化/マージは行わない。
