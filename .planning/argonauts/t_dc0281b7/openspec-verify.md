## Verification Report: r-d4bcda40-max-count

Using change: r-d4bcda40-max-count（別の変更は `openspec-verify-change <name>`）
確認者: 品質 argonauts-uat-quality、カード t_dc0281b7 run 135、対象head b4e9037892f01582554a96df2389c9e0458d7c35
CLI: openspec 2.1.1（argonauts同梱のnodeランチャー）。`status --json` rc0（schema spec-driven、isPlanningComplete true、proposal/specs/design/tasks done）、`instructions apply --json` rc0、`validate r-d4bcda40-max-count --strict` → valid（rc0）、`validate --specs` → 2 passed 0 failed（wordfreq-cliにRFC2119語のWARNING 3件。既存要求の書式で、今回の変更ではない）。

### Summary
| Dimension    | Status |
|--------------|--------|
| Completeness | 4/5 tasks（残り2.2）、ADDED 3件・MODIFIED 5件 すべて実装を確認 |
| Correctness  | 8/8 reqs covered（ADDED 3、MODIFIED 5）。シナリオは全件、実CLIか既存pytestで確認 |
| Coherence    | design.md の決定1〜6に一致。コードの書き方も既存に合う |

### Completeness
- タスク: progress total 5 / complete 4 / remaining 1（unavailableTrackingFiles なし）。
- 残りの 2.2（品質による独立のCLI/HTML確認と、文字の証拠の添付）は、このフェーズ検証のrunで行った（下記と `.planning/argonauts/r-d4bcda40/quality/cli-ci-proof.md`）。チェックボックスは `openspec/` の下にあり、品質がcommitしてよいのは `.planning/` だけなので、印はまだ付けていない。最終化でsync/archiveするときに付ける（2.2の内容は終わっている。印の更新だけが残る）。
- 2.2の文言にあるブラウザ・画像・通信の検査は、依頼者の判断（2026-11-25 21:22、t_87068596）で受入条件から外れた。行っておらず、合格とも書かない。

### Correctness（要求 → 実装・確認）
- MAX-1 最大出現回数: `wordfreq/__main__.py:18`（type=int, default=None）、`:37-39`（下限 AND 任意の上限、両端を含む）。実CLIで、max2→alpha2/gamma1/delta1、max1→gamma1/delta1、min2/max2→alpha2、min2/max3と順序入替→beta3/alpha2、`+2`・`02`・`=-1` を受理、help に `--max-count MAX_COUNT`、abc/1.5/値なしは入力を読む前にexit2。
- MAX-2 空結果と互換: max0/負数/min3max2 は空でexit0、HTMLの総数は7のまま。空・空白・記号だけの入力も空でexit0。入力失敗（ファイルが無い・ディレクトリ）はexit1。min0/top0 との併用はexit2。上限なしと大きな上限は、変更前の固定バイト列と一致（`validate` exit0）。
- MAX-3 試験と使用例: README の例を一時ディレクトリで実行し、exit0・期待JSON+LF・stderr空。全suiteは1048 passed（exit0）。
- FR-2 top: max2 top1→alpha2。選択後12種類で、topなし→10件、top99→12件。
- FR-4 順序: 同じ回数は初出順（tie2→zoo2, apple2）。Unicode（Straße/STRASSE）は正規化した後に数えてから判定（max1→空、min2max2→strasse2, 日本語2）。
- HTML-2 総数: triple（min2 max3 top1）は zoo3 だけを表示し、総数12（フィルタ前）。
- MC-1/MC-2: 既存の min/top の検査と出力を保つ（explicit-min・min-top・excluded の固定バイト列と一致）。

### Coherence
- 決定1（None/int、正の値に限る制約を足さない）、2（同じ共通選択にAND、top の前）、3（元の総数はフィルタ前）、5（引数エラーは入力より先、正しい値なら入力失敗はexit1）、6（README例は1つ）を、ソースと実CLIで確認した。決定4（TDD）は builder/07-01 の先行RED（276件中213件が失敗、exit1）→GREEN の記録で確認した。
- 製品の変更は `__main__.py` の2か所だけ。formatter・依存・CI は変わっていない。

### Issues
- CRITICAL: 0（tasks.md の 2.2 の印だけが未更新。内容はこのrunで済み。最終化で印を付ける）
- WARNING: 0
- SUGGESTION: 1（GSDのREVIEW WR-01/02・IN-01〜04。検証用の道具と試験の堅牢さの改善案で、製品の振る舞いの問題ではない）

### Final Assessment
確認した項目に重大な問題は無い。省いた検査は無い。tasks.md の 2.2 の印が残っているが、品質の確認はこのrunで終わっている。印は最終化で付ける。
