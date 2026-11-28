## Verification Report: r-e0a2598f-wordfreq-exclude

Using change: r-e0a2598f-wordfreq-exclude（上書きは `openspec-verify-change <other>`）
検証者: 品質（独立）。対象head: f3747b7e6235775b3c21fa13201d7921be77306c（製品内容は 526b89c と同一。`git diff 526b89c f3747b7 -- wordfreq tests README.md pyproject.toml` は空）
OpenSpec CLI 2.1.1（公式ランチャー: node …/openspec-cli/2.1.1/…/bin/openspec.js）

### 実行した公式コマンドと原本
| コマンド | 終了 | 原本 |
|---|---|---|
| `openspec status --change r-e0a2598f-wordfreq-exclude --json` | 0 | `.planning/argonauts/r-e0a2598f/quality/openspec-status.json`（schema spec-driven、proposal/specs/design/tasks すべて done） |
| `openspec instructions apply --change r-e0a2598f-wordfreq-exclude --json` | 0 | `.planning/argonauts/r-e0a2598f/quality/openspec-apply.json`（taskTrackingConfigured true、progress 4/5、unavailableTrackingFiles null） |
| `openspec validate r-e0a2598f-wordfreq-exclude --strict` | 0 | `.planning/argonauts/r-e0a2598f/quality/openspec-validate.txt`（"Change 'r-e0a2598f-wordfreq-exclude' is valid"） |

### Summary
| Dimension | Status |
|---|---|
| Completeness | 4/5 tasks（残り 3.2 = 本カードの独立検証と配布そのもの）、ADDED要件 5/5 実装あり |
| Correctness | 5/5 要件の実装を確認、シナリオ 21/21 に試験または品質の実CLI観測あり |
| Coherence | design の決定に従う（下記）。逸脱の警告 1 件（help の説明量） |

### Completeness
- Task Completion: 1.1/2.1/2.2/3.1 は完了。**3.2 は未チェック**。3.2 は「品質担当が対象headで独立に確認し、GSD VERIFICATION と OpenSpec verify を文字原本として保存・添付し、PM が read_file できること」で、本カード（t_d369e688）がこの報告・08-VERIFICATION.md・quality-evidence.md の添付で実行する。品質のcommitは `.planning/` 配下に限られる（チーム規約 E.9 / F.5-7）ため、`openspec/changes/.../tasks.md` のチェックは品質が編集しない。配布の事実（添付ID）は完了の要約と metadata に記録し、チェックの反映は後続の最終化の担当に渡す。→ 公式手順上は CRITICAL「Complete task: 3.2」として記録し、上記の理由で品質の範囲外の編集とする。
- Spec Coverage: ADDED 5件（EX-1〜EX-5）。REMOVED/RENAMED なし。

### Correctness（要件→実装→証拠）
| 要件 | 実装 | 試験 | 品質の実CLI観測（`quality/cli/cli-log.txt`） |
|---|---|---|---|
| EX-1 除外単語ファイル指定 | `wordfreq/__main__.py:19-20,32-42,50-51`、`wordfreq/exclusions.py:13-23` | `test_exclude_tracer*`、`test_exclude_selection_*` | AC1-zoo-text/json/html（`2\tzoo\n1\tbanana\n`）、AC6-* 30組を固定版 79d83ba と比較し stdout バイト一致 |
| EX-2 除外行と大小同一視 | `exclusions.py:16-22`（strip→空/# 無視→`re.fullmatch(r"\w+")`→casefold） | `test_exclude_grammar_*` 6件 | AC2-crlf-comment、AC3-case（Straße/STRASSE/Hello/HELLO/hello 除外→world）、AC3-validmisc（123/_word_/a_b/日本語 有効） |
| EX-3 除外FILE失敗の診断 | `__main__.py:33-42`（InputError/InvalidExclusion→stderr+exit2、本文取得の前） | `test_exclude_failures_role_mapping`、`test_exclude_precedence_*` | AC4-missing/dir/badutf8/permission-denied×3形式/bad-line4/bom/hyphen/combining/inline-comment/punct（全て exit2・stdout 0B・Traceback 0件）、AC4-value-missing exit2、AC4-badtop/badmin-before-ex（引数エラー優先）、AC4-body-missing/badutf8-valid-ex exit1、AC4-both-missing exit2、FIFO本文プローブ（除外失敗3種 exit2 即時＝本文未オープン、正常除外の対照は timeout 124） |
| EX-4 既存表示選択との併用 | `__main__.py:48-52`（total は除外前 Counter の和、除外は selected_counts のみ） | `test_exclude_selection_preserves_full_counter_and_shared_pairs`、`test_exclude_empty_*` | E-min2-ex、E-top1-ex、E-all-text/json/html（空・`[]\n`・総数5の空表）、AC1-zoo-html 総数5、E-emptybody-ex-html 総数0 |
| EX-5 説明と試験 | `__main__.py:19-20`（help）、`README.md:29-62` | `test_exclude_help_readme_tracer`、`test_exclude_docs_complete_contract_and_literal_example` | AC5-help exit0、`--exclude FILE` 行あり。全試験 1159 passed（品質が自分で実行） |

### Scenario Coverage
全21シナリオに対応する試験群がある（08-VALIDATION.md の要件→試験表、品質の再実行 `-k exclude` 457 passed）。品質の実CLIでも EX-1 2件、EX-2 5件中 4件（前後空白/改行形式・大小・数字underscore・Unicode正規化、空行コメント）、EX-3 8件すべて、EX-4 3件すべて、EX-5 2件を直接観測した。

### Coherence
- Design Adherence: 純関数 `parse_exclusions`（I/O・終了方針なし）、取得境界 `FileSource` の再利用、除外の後に既存 min-count/初出順/top、HTML 総数は除外前、formatter 不変（`git diff origin/v112-a...HEAD -- wordfreq/formatters.py` 空）— design と一致。
- Code Pattern Consistency: 既存モジュール構成・命名に従う。新依存・CI・pyproject 変更なし。

### Issues by Priority
1. **CRITICAL**
   - tasks.md 3.2 未チェック。Recommendation: 本カードの添付（完了要約の添付ID）を根拠に、最終化の担当が `openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md` の 3.2 をチェックしてから archive する。品質は `.planning/` 外を編集しない。
2. **WARNING**
   - Implementation may diverge from spec (EX-5): `--help` の文言は `exclude words from a UTF-8 file (one word per line)` のみで、空行/#行の無視・大小同一視・失敗 exit2 は README だけが説明する（`wordfreq/__main__.py:20`）。受付の受入条件5「--help と README.md の使い方に説明を追加する」は満たす。spec の「help と README に説明する」を help 単独で全項目と読む場合だけ差が出る。Recommendation: 必要なら help 文に「空行と#行は無視、大小を区別しない」を足す（提案扱い。受入条件より厳しい読み方の差として記録）。
3. **SUGGESTION**
   - 08-REVIEW.md IN-01/IN-02（浅い取得の試験が作業ツリーの fixture を読む点、`git clone` と CLI 実行に timeout が無い点）。Recommendation: tests/test_cli.py:1356-1375 に timeout を付ける。

### Final Assessment
1 critical issue(s) found（3.2 未チェック。本カードの配布で根拠が揃い、チェックの反映は最終化の担当）。1 warning、1 suggestion。他の検査はすべて実行し、未検証の検査はない。
