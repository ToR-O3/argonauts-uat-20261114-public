# 07-01 実装と確認の記録

対象依頼: r-d4bcda40 / PLAN07-01。製品開始head: `8efbfaa1907ace272a4f685e2659144a4085d303`。
製品実装commit: `31953e1c3f1bd0b5da09484f079f0027976ec737`。
追加変異試験commit: `db08d285a23025263fbb30d033a73ea560f5b489`。

## 最新判断と実施範囲

`decision.md`に、元カードt_87068596の人（default）の2026-11-25 21:22 JST（created_at=1795609328）の原文を保存した。画像取得・比較を省き、HTMLの単語・回数は試験で確認する。品質の独立確認は維持する。Chromiumは未修復で、画像/描画/通信の実観測を合格と主張しない。通常幅・狭幅画像の代わりを捏造していない。

製品差分は `wordfreq/__main__.py` のtype=int/default=None登録と、既存別Counter生成に包含AND上限を加える2か所だけ。集計→元total保持→min/max共通選択→既存top→同一pairsを各formatterという順。抽出・正規化・aggregator/formatter/sourceの公開API、CSS、空文言を変更していない。READMEは07-02担当として未変更。依存/CI更新なし。

## 変更前の原本

- `../../baseline/index.json`とindex.sha256: 39 CLIケース、画像0/view0。初回採取1.154767425秒、有限timeout600秒。製品変更前に1回のみ実施。再採取しない。
- 同数/10種類超・既定text/全形式・明示min1・min2/top1・min全除外・空/空白/記号の全形式・Unicode・256字の長語/176字のbasename/連続空白/LF/TAB/CR/注入候補を固定した。
- caseごと入力bytes、literal期待pairs/元total、argv、exit、stdout.bin、stderr.bin、HTML原本を保存。実cwd/interpreter/version/明示環境/開始head/製品SHA-256はindex/provenanceへ保存。環境は秘密を含まない実行に必要なキーだけを明示する。
- 既存min-countの12caseは別依頼の履歴として不変参照し、旧index/head/rootを変更していない。既存の保存bytes回帰も全suiteに含まれる。
- baselineのread-only照合、stdout/input/argv/env/head/hash/HTML欠落/syntheticの拒否、既存root再使用拒否: `tests/test_max_count_verifier.py`。

## OpenSpec1.1全追加試験の先行実行

製品blobが開始headと同じ状態で、`red/command.json`の正確なargvにより全追加群を-xなしで実行。`red/result.json`は実行前後の製品blob・head・全case名と成否、stdout/stderr/JUnit/実行試験ソースのhashを保存する。

| グループ | 実件数 | 先行失敗 | 自然成功 | 契約 |
|---|---:|---:|---:|---|
| tracer | 3 | 3 | 0 | MAX-1 max2・全3形式・元7 |
| parser | 7 | 7 | 0 | None/0/-1/+2/02/正負10**100 |
| parser_equals_negative | 1 | 1 | 0 | equals負数 |
| help | 1 | 1 | 0 | ファイルなしhelp・表示 |
| selection | 90 | 90 | 0 | MAX-1/FR-2/FR-4/MC-1、包含/min併用/指定順/Unicode/tie/top/元12 |
| empty | 27 | 27 | 0 | MAX-2/MC-2、0/負数/逆転/空/抽出0/単語1つ/空文言 |
| invalid_before_read | 63 | 0 | 63 | MAX-1/MAX-2/MC-1、欠落/非整数/不正min/top、入力前spy＋実CLI |
| input_failure | 36 | 36 | 0 | MAX-2、max0/負数/逆転×4実入力失敗×全形式 |
| internal_order | 3 | 3 | 0 | top入力は別Counter・元値順不変・shared pairs・元12 |
| hashseed | 3 | 3 | 0 | 0/1/42、Unicode/tie/全形式 |
| saved_bytes | 39 | 39 | 0 | MAX-2/MC-2、固定oracle・省略/大max/明示min1 |
| read_only | 3 | 3 | 0 | cold-copy・実入力bytesとgit状態不変 |
| **計** | **276** | **213** | **63** | ERROR/skip 0 |

通常maxは未登録引数exit2と期待exit0/1のassert差。NoneはNamespaceにmax_count無し、helpは表示無し。permissionは同じ実効ユーザーの実readでPermissionErrorを確認しfinallyで復元。非整数等は未登録でも既存usageとして自然GREENなので偽REDにしない。

公式 `gsd_run check tdd-red-evidence ... --raw` は最初にcommandを配列で渡したため `INVALID_RED/invalid_record`。レコードのcommandだけを文字列へ正しく直し、同一の無編集JUnit原本で `RED_EVIDENCE_OK/target_test_failed`（`red-classifier-corrected.json`）を確認してから製品を編集した。最初のmissing verifier-fileによるインフラ試験失敗は製品REDの代用にしていない。

## 実行結果

共通環境: `/usr/bin/python3` CPython3.12.15、`PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages`、pytest9.0.3。各stageの`command.json`は実argv/cwd/env、`result.json`は実head・製品blob/時間/件数/exit、`stdout.txt`/`stderr.txt`/`junit.xml`は無編集原本。

| stage | 結果 | wall秒 |
|---|---|---:|
| red | 276実行、213失敗/63成功、exit1、ERROR/skip0 | 16.406800224 |
| green | 276成功、exit0 | 10.855053241 |
| tracer | 3成功、exit0 | 0.552784130 |
| verifier | 12成功、exit0 | 1.102857575 |
| mutations | 7成功（各変異は内部CLIの狙ったassertでexit1）、外側exit0 | 31.945417195 |
| cli | 641成功、exit0、失敗/ERROR/skip0 | 53.303887239 |
| full | 997成功、exit0、失敗/ERROR/skip0 | 194.526869933 |

初回browser_free/saved_baselineは11成功、pytest報告0.75秒。read-only検査は30秒以内。変異、CLI全体、full suiteは30秒超のため高速feedbackとは呼ばない。全suiteの追加時間は独立品質で再実行する前提。

`green`時点はtest commit d89164d＋製品working diff、`full`時点は製品commit31953e1＋追加7変異試験working diff。どの原本も後の報告headへ付け替えない。resultに製品前後blobを保存し、最終製品との差分は無い。

## 単一変異の判別力

すべて管理scratchのpytest tmp_pathにcold packageを作り、製品worktreeへ適用せず、96のtracer/selection/internal_order試験を実行。各変異ごとの実stdout/stderrは `mutations/stdout.txt` にそのまま保存。

| 変異 | 内部失敗/成功 | 検出する方向 |
|---|---|---|
| 上限無視 | 60/36 | max超過語が残る |
| 排他的上端 | 90/6 | 境界語が消える |
| OR選択 | 66/30 | 両条件を満たさない語が残る |
| top後filter | 33/63 | 繰上げ語を失い、top入力spyも失敗 |
| 元Counter破壊 | 3/93 | 元Counter値と項目順の不変assert |
| 総数再計算 | 26/70 | 元7/12とformatter metadataの不一致 |
| 語昇順tie | 33/63 | zoo→apple等の初出順の不一致 |

これらは実装後の追加判別力であり、先行REDの代用ではない。正しい現コードは全追加群・既存全suiteで成功。

## 残る工程

- OpenSpec1.1/1.2のみチェック済み。2.1のこのPLAN分は実行済みだが、README試験等の後続分があるため全体チェックは残す。1.3/2.2未完了。
- 07-02の追加出口変異・README1例、07-03の最新判断に合わせた証拠手順整備は未実施。
- 品質は対象headで独立CLIとHTML内容（単語・回数・元総数・空結果・省略互換）を確認し、全試験・文字証拠を添付する。Builderの固定原本やcaptureだけでOpenSpec2.2を合格としない。
- CIの実行状況はpush後に1回読む。ローカル997成功をCI成功と取り違えない。draft PR、同カード品質レビューへ渡し、Botはマージしない。
