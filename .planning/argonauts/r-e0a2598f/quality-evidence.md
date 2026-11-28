# 品質の独立検証の記録 — r-e0a2598f Phase 8（--exclude FILE）

カード: t_d369e688（フェーズ検証、品質）。Builder の原本は手掛かりとしてだけ読み、合否はすべて品質が自分で実行した結果で決めた。

## 対象 head
- 実行前: `f3747b7e6235775b3c21fa13201d7921be77306c`（`quality/head-before.txt`。origin/argonauts/r-e0a2598f・ローカルHEAD と一致）
- 実行後・報告前: 同じ（`quality/head-after.txt`）。途中で製品内容は変わっていないので再実行は不要。
- Builder の製品内容対象 526b89c と f3747b7 は製品範囲（wordfreq/ tests/ README.md pyproject.toml）の差分が空。
- 固定過去版: `79d83ba14dd59d289d2ecd3e33c85e8de437972e`。`git archive 79d83ba wordfreq` を /tmp の隔離ディレクトリに展開し、6ファイルの `git hash-object` が `git ls-tree` の blob と全件一致（`quality/cli/cli-log.txt` 冒頭）。過去版は `--exclude` を `unrecognized arguments` で拒否（BASE-rejects-exclude、exit2）＝隔離された過去版で動いた証拠。
- 実行環境: `.venv/bin/python`（CPython 3.12.15、`uv run --extra dev` が作る環境）、`env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8`、`-s -E -m wordfreq`。

## 品質が実行した試験
| コマンド（作業場所のルート） | 結果 | 原本 |
|---|---|---|
| `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` | exit0、457 passed / 358 deselected（20.64s） | `quality/pytest-exclude-{stdout,stderr,exit}.txt` |
| `uv run --extra dev python -m pytest -q` | exit0、1159 passed（188.30s） | `quality/pytest-full-{stdout,stderr,exit}.txt` |
| GSD regression gate（公式 regression-gate-run の pytest 分岐、既往phaseの試験9ファイル、timeout 600） | REG_TEST_EXIT=0、1159 passed | `quality/regression-gate.txt` |
| `python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py` | exit0、19 tests OK | `quality/handoff-unittest.txt` |
| `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json` | exit0、HANDOFF_READY_ONLY（引渡しの形が揃っているだけ。合否ではない） | `quality/handoff-checker.txt` |
| 実CLI 237出力（下の表）＋FIFO・権限・値欠落の追加観測 | 期待どおり（不一致0） | `quality/cli/cli-log.txt`、`quality/cli/out/*`、入力 `quality/cli/in/*` |

入力の不変: `quality/cli/inputs-sha256-before.txt` と `-after.txt` が一致（22ファイル、INPUTS_UNCHANGED）。

## 受入条件ごとの判定（受付の6条件）
| AC | 判定 | 品質の証拠（cli-log.txt の見出し） | 期待 → 実際 |
|---|---|---|---|
| AC1 --exclude FILE の1行1語を除外 | 合格 | AC1-zoo-text/json/html | text `2\tzoo\n1\tbanana\n` → 同じ。json 同じ語順。html 2行・総数5 |
| AC2 空行と#行を読み飛ばす | 合格 | AC2-crlf-comment（` \r\n  #banana\r\n apple `、最終改行なし）、E-commentonly-* | apple だけ除外・banana 残る → 同じ。コメントのみFILE＝未指定とバイト一致 |
| AC3 大文字小文字を区別しない（casefold） | 合格 | AC3-case、AC3-validmisc | `STRASSE`/`Hello` で Straße・STRASSE・HELLO・hello を除外し `1\tworld\n` → 同じ。123/_word_/a_b/日本語 は有効で `2\tkeep\n` |
| AC4 FILE が無いとき分かる文で exit2 | 合格 | AC4-missing ほか14件、permission-denied×3、value-missing、FIFO本文プローブ | `no-such-file.txt: [Errno 2] No such file or directory: …`、exit2、stdout 0バイト、Traceback 0件。不正行は `FILE: line N: expected one Unicode word`（line 4 は無視行を数えた元行番号）。本文の失敗は exit1 を維持。引数エラーが先（--top 0 / --min-count 0） |
| AC5 --help と README の説明 | 合格 | AC5-help（exit0、`--exclude FILE  exclude words from a UTF-8 file (one word per line)`）、README.md 37-62行 | help に項目あり、README に形式・例・エラー・有効/不正例・総数・検証順 |
| AC6 試験追加と未指定時の互換 | 合格 | AC6-* 15組（zoo/tie-top2/min2/empty/case × text/json/html）を head と 79d83ba で実行、全組 stdout・stderr・exit がバイト一致。エラー3組（missing/badtop/badfmt）は exit と stdout が一致 | badtop/badfmt の stderr は usage 行に `[--exclude FILE]` が増える差だけ（新しい選択肢の追加による意図した差） |

追加の確認: 空FILE・コメントのみ・不一致語のみ＝未指定と3形式でバイト一致。全語除外は text 空・json `[]\n`・html 0行で総数5。空本文は総数0。min-count2/top1 と併用しても除外語は戻らず、同数の初出順を保つ（E-tie-ex: b2,a2,c1,d1）。

## 全差分の確認
- 製品の変更: README.md、tests/fixtures/README.md、tests/fixtures/exclude-baseline-git-objects.json、tests/test_cli.py、wordfreq/__main__.py、wordfreq/exclusions.py（6ファイル、+855/-5）。工程の文書: .planning 149件・_bmad-output 64件・openspec 5件（判定の対象外）。
- 危険なパス: `.github/`・pyproject.toml・uv.lock などへの差分なし（`git diff --name-only origin/v112-a...HEAD -- .github pyproject.toml uv.lock` が空）。新依存なし、外部送信なし（新コードに通信なし）、CI変更なし。
- formatter/CSS/basename/静的安全: `wordfreq/formatters.py`・aggregator・tokenizer・sources は差分なし。HTML は未指定時に過去版とバイト一致。
- 入力の書換えなし（読み取り専用 open、上の sha256 一致）。

## 26 edge の判定
| key | 判定 | 根拠 |
|---|---|---|
| REQ-28/boundary | 合格 | E-min2-ex、E-top1-ex、AC1-zoo-html 総数5、`test_exclude_selection_*` |
| REQ-28/adjacency | 合格 | E-tie-ex（同数は初出順、語は統合されない） |
| REQ-28/empty | 合格 | E-emptybody-ex-html 総数0、E-all-* 0行・総数5 |
| REQ-28/encoding | 合格 | AC3-case（Straße/STRASSE） |
| REQ-28/ordering | 合格 | AC1 3形式で同じ語・回数・順 |
| REQ-28/precision | 合格 | 整数の回数・総数、総数から引かない（AC1-zoo-html 5） |
| REQ-28/concurrency | human_needed / insufficient_spec（backstop。合格にも失敗にもしない） | 仕様に保証の定義なし。README 39行が「中断や並列実行について新しい保証は追加しません」と明記 |
| REQ-29/empty | 合格 | E-empty-*、E-commentonly-*、AC4-value-missing |
| REQ-29/encoding | 合格 | AC2-crlf-comment、AC4-bom/hyphen/combining/inline-comment/punct、AC3-validmisc |
| REQ-30/boundary | 合格 | AC4-badtop-before-ex、AC4-badmin-before-ex、AC4-value-missing |
| REQ-30/adjacency | 合格 | AC4-both-missing（除外の診断と exit2 だけ）、AC4-body-missing-valid-ex exit1 |
| REQ-30/empty | 合格 | 不在・読めないFILEは成功扱いにならない（AC4-missing/dir/badutf8/permission-denied） |
| REQ-30/ordering | 合格 | AC4-bad-line4（line 4）、FIFO本文プローブ（除外失敗3種で本文を開かず即 exit2、正常除外の対照は 124） |
| REQ-30/precision | 合格 | 元行番号が無視行を数える、exit は正確に2 |
| REQ-30/concurrency | human_needed / insufficient_spec（backstop） | 並列I/Oの保証は承認されていない。単発の除外先行の制御は上で確認 |
| REQ-31/concurrency | human_needed / insufficient_spec（backstop） | help/README は中断・並列の保証を約束しない（README 39行で確認）。保証の存否は仕様外 |
| REQ-32/boundary | 合格 | `test_exclude_baseline_exact_git_bytes`（品質の全試験で実行）、AC6-tie-top2/min2/case |
| REQ-32/adjacency | 合格 | 品質の AC6 比較は同じ interpreter・入力の絶対パス・argv・env、別の module root |
| REQ-32/empty | 合格 | AC6-empty-text/json/html 一致、E-empty/commentonly/nomatch/all を区別 |
| REQ-32/encoding | 合格 | AC6-* の生バイト比較（UTF-8 HTML、ASCII JSON+LF）、入力不変 |
| REQ-32/ordering | 合格 | AC6-tie-top2（逆辞書順の同数）、AC6-case（Unicode） |
| REQ-32/precision | 合格 | stdout はデコードせずバイト比較、件数は実測値 |
| REQ-32/concurrency | human_needed / insufficient_spec（backstop） | 同時編集・中断時の公開の保証なし。対象headを前後で記録（変化なし） |
| REQ-33/boundary | 合格 | 既定 text/top10/min-count1、body exit1/usage exit2、純関数の署名、formatter 不変（差分なし） |
| REQ-33/precision | 合格 | 整数 Counter、安定ソート、未指定時のバイト一致 |
| REQ-33/concurrency | human_needed / insufficient_spec（backstop） | 既存の単発・読み取り専用の範囲に一般の中断・並列の保証はない |

内訳: 21 explicit すべて合格、5 backstop は human_needed / insufficient_spec のまま。

## 14 UI 状態の判定
画像: 品質の ui-review 委任（同じ品質の実行内の子）が HeadlessChrome 156 で実CLI生成HTMLを 1280×900 / 320×900・DPR1 で開き、**2枚を閲覧**（(a) 長いbasename・320px、(b) 全語除外・1280px）。品質の親は画像を直接見ていない（0枚）。画像は添付していない。DOM測定は 9文書×2幅＝18描画で metaAboveTable true、rowOverlap 0、cellOverlap 0、scrollWidth==clientWidth。文字単位の Range／glyph clip 検査は**未実施**。この環境に日本語フォントが無く、日本語の文言は描画されなかった（formatter は不変で、HTMLは未指定時に過去版とバイト一致）。詳細は `.planning/phases/08-wordfreq-exclude/08-UI-REVIEW.md`。

| key | 判定 | 証拠の種類 |
|---|---|---|
| UI-E1/overflow | 合格（DOM測定）／文字の重なりは未確認 | G、S |
| UI-E1/long-text | 合格（バイト・算出サイズ）／日本語の読みやすさは未確認 | B、G |
| UI-E2/overflow | 合格 | G、I(a) |
| UI-E2/long-text | 合格 | B、G、I(a) |
| UI-E3/empty | 合格（全語除外は総数5、空本文は総数0） | B（E-all-html、E-emptybody-ex-html）、I(b) |
| UI-E3/loading | 合格（完成した文書だけ） | B、S |
| UI-E3/error | 合格（stderr のみ、stdout 0バイト、エラー用HTMLなし） | B（AC4-* html） |
| UI-E3/populated | 合格 | B（AC1-zoo-html）、I(a) |
| UI-E3/partial | 合格（不正行は出力前に exit2） | B |
| UI-E3/overflow | 合格（DOM測定） | G |
| UI-E3/zero-one-many | 合格 | B、G |
| UI-E3/long-text | 合格 | B、G |
| UI-E4/overflow | 合格 | G、I(b) |
| UI-E4/long-text | 合格（固定文言を維持）／日本語の読みやすさは未確認 | B |

B=実CLIのHTMLバイト、G=DOM測定、I=閲覧した画像、S=ソース。静的バイトは見た目の維持の根拠で、幾何の実測ではない。

## 禁止事項（descriptor-less）
| key | 判定 | 品質の観測（非権威） |
|---|---|---|
| P-08-01 自動の除外辞書・推定除外の禁止 | flagged-unverified（黙って合格にしない） | 未指定時は過去版とバイト一致、空・コメントのみ・不一致FILEは未指定と一致、ソースに辞書なし。違反は見当たらない |
| P-08-02 Builder結果等を独立受入として示すことの禁止 | flagged-unverified | この記録の合否は品質が f3747b7 で実行した結果だけに基づく。Builder の実行結果は転記していない |

## 公式の手順の結果
- GSD: verify:post（nyquist・security・ui）→ code-review → regression gate → gsd-verifier → verification.status。原本: 08-VALIDATION.md（nyquist_compliant true）、08-SECURITY.md（threats_open 0）、08-REVIEW.md（critical 0 / warning 0 / info 2）、08-REVIEW-DISPOSITION.md、08-UI-REVIEW.md、08-VERIFICATION.md（**status human_needed、score 38/44**）。
- OpenSpec: `.planning/argonauts/t_d369e688/openspec-verify.md`（validate --strict 合格、tasks 4/5、残り 3.2 は本カードの配布。品質は `.planning/` 外を編集しないため、チェックの反映は最終化の担当）。

## 判定
- 受入条件6件はすべて合格。製品の不具合は見つからなかった。
- フェーズの公式判定は human_needed: backstop 5件（insufficient_spec）と禁止事項2件（flagged-unverified）、日本語の描画の目視（環境にフォントなし）、配布の確認。どれも依頼者が人の目を明示した受入条件ではない。品質が受入条件に照らして試した結果は 08-UAT.md に記録した。phase は完了にしていない。
- 学びの候補: 単発CLIの「中断・並列」backstop は仕様で扱わないと決めておくと、毎回 human_needed で止まらずに済む。
