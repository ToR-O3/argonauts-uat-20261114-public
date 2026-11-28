# Phase 08: wordfreq exclude-file — Research

**Researched:** 2026-11-28（terminal `date +%F`）
**Domain:** 標準ライブラリCLIの除外一覧取得・共通集計前処理・pytest回帰設計
**Confidence:** LOW（公式分類CLIの `local --verified` / `webfetch --verified` の返値。原本・コードの直接確認と未実行の実装提案を以下で区別する。分類器がローカル一次資料を専用評価しないことを理由にHIGHへ引き上げない。）

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は `.planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-40,64-66` の原文転記。承認済み判断を再審議しない。

<!-- DATA_2123092e_START -->
### Phase Boundary
承認t_0d1aa16a、原本head8a2c69b8332e9704377fe680af51767c74e4ab56の同じOpenSpec変更を実装する。CLIの--exclude FILE、説明、試験と必要な工程原本。計画工程では製品/試験を実装しない。
公式ingestの旧HTML総数locked衝突はE.7の今回承認済み変更として公式phase.addで新phase8を追加する分岐で扱う。旧履歴を消さず、除外指定時だけHTML-2を拡張する。未指定の元総数やmin-countのみで全件除外したときの旧契約は変えない。Brief/PRD参照循環は背景Briefをmanifest対象外とし正本5文書へ絞って再合成、循環なし。既存phase1/3/4/5/7の古い検証状態は今回の範囲に混ぜない。

### Locked Decisions
### D-01: 共通除外と最後FILE（REQ-28 / EX-1）
- 任意の--exclude FILEで一致語の全出現を外す。全形式で共通、重複無影響、最後のFILEだけ読み以前のFILEは読まない。残存語の回数/相対初出順/順位規則を維持する。
- Zoo apple APPLE zoo bananaからapple除外はzoo2/banana1。zoo除外/top1はapple2。beta apple alphaからapple除外はbeta1/alpha1。該当語なし/空/コメントのみは未指定と同じ。missing→validなら成功、逆順は失敗、最後空FILEなら前の一覧無効。
### D-02: 行解釈（REQ-29 / EX-2）
- UTF-8、先頭BOM除去、strip後空行/先頭#行無視。LF/CRLF/最終改行なし。その他は行全体一語、分割/記号除去/途中#コメントなし。直接読込試験で無視項目が集合に入らないことも確認。
- foo barはfoo/barに無影響。foo_bar/123は一致語だけ。foo-barは本文のfoo/barに無影響、apple#noteもapple/noteに無影響。本文抽出規則を変更しない。
### D-03: casefold（REQ-30 / EX-3）
- 本文既存casefoldを維持し有効除外行もcasefold。lowerへ変更しない。Apple/APPLE/appleとaPpLe一致、実際のStraße/STRASSE一致を試験する。
### D-04: 読込失敗と順序（REQ-31 / EX-4 / AD-4）
- 既存引数検証→採用除外FILE→本文。除外不存在/権限不足/ディレクトリ/不正UTF-8等は対象と原因をstderr、exit2、stdout空。文言完全一致を追加しない。
- 不正top/min-count/format/値欠落等はファイルを読まず既存エラー。両FILE失敗は除外exit2で本文未読。除外成功後または未指定時の本文のみ失敗は既存exit1。直接試験とCLI双方で順序/優先を確認。
### D-05: 説明と試験（REQ-32 / EX-5）
- help/READMEに構文/一覧形式/行規則/casefold/最後FILEのみ/読込失敗exit2/空結果を記す。README例を実CLIで再現可能にする。
- OpenSpec tasks1.1は文書反映済みで再実行しない。未完2.1（正常系/説明/試験）2.2（異常/順序/説明/試験）3.1（統合回帰/証拠）をPLANと対応付け、未実装はチェックしない。
### D-06: 空結果と未指定互換（REQ-33 / EX-6）
- 全語除外はtext空、json []と末尾改行、HTML既存空表と既存空結果案内/総数0、全形式exit0・除外専用案内なし。
- 未指定の本文読込/抽出/casefold/全形式/同数初出順/min-count/top/空結果/エラー契約を維持し、既存全試験を通す。
### D-07: 証拠と範囲（REQ-34 / RULE-2）
- 追加依存/権限変更/外部送信なし。品質が対象headで独立実行しコマンド/環境/入力/stdout/stderr/exit/条件別結果をVERIFICATION.md等の文字原本へ保存し標準添付する。画像は品質が実閲覧して枚数/内容/結果を文字化、PMに画像/圧縮ファイルを開かせない。
- OQ7/8は背景不足のみで新条件/停止理由にしない。過去の学びの語昇順例ではなく現行初出順を優先。
### D-08: 処理順とHTML総数（REQ-35 / RULE-1 / HTML-2）
- 全形式で除外→計数→min-count→top→既存formatter。総数は除外後/min-countとtop前の回数和、種類数や表示行の和でない。
- Zoo apple APPLE zoo banana、除外apple、min-count2/top1はzoo2だけ・HTML総数3（5でも2でもない）。未指定時の従来総数は維持。
- basename限定/escape/自己完結/外部通信なし/明るい背景/既存レイアウトは継承。再設計しない。
### Claude's Discretion
既存4+1の部品境界を保つ最小の関数分割とテスト配置。設計AD-1〜4に従い、製品判断の追加はしない。

### Deferred Ideas (OUT OF SCOPE)
新入力元、抽出変更、全体リファクタ、外部送信、依存追加、画面再設計、OQ7/8の追加要件化、旧phaseの再検証は今回対象外。
<!-- DATA_2123092e_END -->
</user_constraints>

## Summary

[VERIFIED: wordfreq/__main__.py:13-54; wordfreq/sources.py:13-22; _bmad-output/initiative-r-6442a149/architecture/architecture.md:29-71] 現行CLIは引数検証後に本文取得、抽出・計数、総数、閾値、順位、整形を直列に合成する。承認設計はその前に除外一覧取得、計数直前に所属判定フィルタを挿入するもの。既存 `count_words(iter_tokens(text))` と `total = sum(counts.values())` を、除外済みトークンを数える接続にするだけで総数の新契約へ自然につながる。HTML formatterの再計数・新引数・CSS変更は不要とする（実装提案）。

[VERIFIED: tests/test_cli.py:16-20,201-260,418-441,598-817; tests/test_sources.py:7-80; tests/test_formatters.py:94-178] 実CLIのsubprocessヘルパー、HTMLParser、バイト単位出力検査、入力エラーと引数前検証の試験パターンが既にある。新規大規模検証ツールではなく、既存試験モジュールへ直接読込試験と全形式パラメータ試験を追加する。新ケースは未実装であり、本研究では機能試験・既存全件の合格を主張しない。

**Primary recommendation（計画提案）:** 正常系の縦切り＋行規則・空結果を先行し、異常・順序と統合証拠を後続に置く、依存付きの少数直列PLANにする。各タスクは試験追加→RED確認→最小実装→自分と先行タスクの試験を実行する。未作成node-idや検証スクリプトをPLANの前提にしない。

## Architectural Responsibility Map

根拠: [VERIFIED: _bmad-output/initiative-r-6442a149/architecture/architecture.md:23-77; wordfreq/__main__.py:22-54; wordfreq/formatters.py:22-27]。以下はその最小実装への責務割当提案。

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 引数検証・最後FILE採用・処理順・終了判断 | ローカルCLI composition | — | I/O開始順と終了判断を一箇所に置く |
| 除外FILE取得・行から正規化集合 | ローカル入力取得境界 | 標準文字列処理 | 本文用tokenizerと別の一覧文法 |
| 本文抽出・casefold | 既存純粋tokenizer | — | 本文の抽出契約を保持 |
| 集計前除外 | CLI composition内の順序保持フィルタ | 既存計数部品 | 集合は所属判定専用。本文列は順序保持 |
| 総数・閾値・topの接続 | CLI composition | 既存aggregator | 除外済みcountsから総数、その後選択 |
| text/json/html表示 | 既存純粋formatter | — | 除外一覧の存在を知らず、受取pairsとmetadataのみ使用 |
| DB／API／ブラウザでの処理 | 追加しない | — | 新サービス・永続化・画面再設計は対象外 |

<phase_requirements>
## Phase Requirements

IDと要求原本: [VERIFIED: .planning/REQUIREMENTS.md:104-126]。以下のDescriptionは計画用要約、Research Supportは本研究の対応箇所。

| ID | Description | Research Support |
|---|---|---|
| REQ-28 | 全形式共通除外、残存回数・初出順、重複、最後FILEのみ読む | Architecture Patterns、scenario表EX-1、CLI／境界試験 |
| REQ-29 | UTF-8先頭BOM、strip・空／先頭#、改行、行全体比較 | 専用読込境界、EX-2直接集合試験 |
| REQ-30 | casefold、実際のStraße／STRASSE、本文処理保持 | tokenizer維持、EX-3両方向の比較 |
| REQ-31 | 引数→除外→本文、除外失敗2／本文失敗1、stderr原因と対象、stdout空 | 直列I/Oと例外分離、EX-4直接spy＋実CLI |
| REQ-32 | help／READMEの仕様説明と再現例、対応試験 | 文書の最小更新箇所、EX-5案内試験 |
| REQ-33 | 全語除外の既存空形式、未指定の全既存契約維持 | EX-6、既存バイト／min-count／Unicode回帰 |
| REQ-34 | 依存・権限・外部送信追加なし、独立品質の対象headと文字証拠 | Security Domain、証拠設計と独立品質引渡し |
| REQ-35 | 除外→計数→min-count→top、HTML総数は除外後・選択前 | 共通データフロー、HTML-2全scenario、総数の判別値 |
</phase_requirements>

## Project Constraints (from HERMES.md)

[VERIFIED: 今回のread_fileによる存在確認結果] repo直下 `HERMES.md` と `.hermes/HERMES.md` はいずれもnot_found。`.hermes/skills`／`.agents/skills` も探索時にPath not found。そこから追加project指示を推定しない。追加researcher skillなしという依頼の結果を受領しており、再設定しない。

[VERIFIED: .planning/config.json:21-53,63-64] `"nyquist_validation": true`、`"security_enforcement": true`、`"security_asvs_level": 1`。そのためValidation ArchitectureとSecurity Domainを含める。`"claude_md_path": "./.hermes/HERMES.md"` の設定値だけで、そのファイルの存在を仮定しない。

依頼の追加拘束: ファイル／JSONはread_file、抽出は利用可能ならjq、GSD判定はruntime launcher経由の公式CLI。インラインPython／Node／shellスクリプト、ヒアドキュメント、直接gsd-tools実行は禁止。研究では製品・試験・設定・PLANを変更せず、commit／push／Kanban操作をしない。`commit_docs`設定より今回のcommit禁止を優先する。

## Standard Stack

| Component | 確認済みversion／値 | Purpose / 採用理由 |
|---|---|---|
| 既存wordfreqパッケージ | `version = "0.1.0"` | [VERIFIED: pyproject.toml:5-12] `dependencies = []`、`dev = ["pytest"]` を保持。製品依存を追加しない |
| Python標準ライブラリ | 実行可能な既存系統は下記Environment参照 | [VERIFIED: wordfreq/__main__.py:2-10; wordfreq/sources.py:19-22] argparse／Counter／I/Oの既存構成を維持 |
| argparse | 標準ライブラリ同梱 | [CITED: https://docs.python.org/3.14/library/argparse.html#action] 既定storeを使い、パス文字列だけ保持。全引数検証後に採用パスを読む |
| UTF-8-sig codec | 標準ライブラリ同梱 | [CITED: https://docs.python.org/3.14/library/codecs.html#encodings-and-unicode] 先頭にあるBOMの3バイトだけをデコード時に除去できる |
| str.casefold / strip | 標準組込み | [CITED: https://docs.python.org/3.14/builtins/stdtypes.html#str.casefold] lowerではßがそのまま、casefoldではss。現行本文処理とも一致 |
| pytest | 使用可能な既存環境で9.0.3 | [VERIFIED: terminal環境probe] 新規framework導入不要。既存試験モジュールへ追加する |
| HTMLParser | 標準ライブラリ同梱 | [VERIFIED: tests/test_cli.py:201-239; tests/test_formatters.py:51-133] CLI表／metadata、静的安全性の既存検査を再利用 |

**Installation / Package Legitimacy Audit:** 新しい製品・試験依存をインストールする研究ではない。新規package候補なし、registry照会・package legitimacy gateは対象外。Python／pytestの最新版への更新や版横断互換を新条件にしない。[VERIFIED: pyproject.toml:1-15; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:32-40]

## Architecture Patterns

### System Architecture Diagram（実装提案）

```text
argv → 既存parse + top/min検証 ──不正→ stderr / exit2 / I/Oなし
                     │
                     ├─除外なし────────────────────┐
                     └─最後の除外パスだけ読む       │
                            │                      │
                            ├─失敗→ stderr / exit2 │
                            └─先頭BOM除去           │
                              → 行strip             │
                              → 空/先頭#を無視      │
                              → 行全体casefold集合  │
                                                    ↓
                                               本文取得
                                                  ├─失敗→ stderr / exit1
                                                  └─既存抽出＋casefold
                                                       ↓
                                            順序保持の除外所属判定
                                                       ↓
                                                     計数
                                            ┌──────────┴─────────┐
                                         回数和                min-count
                                            │                    ↓
                                            │               安定順位→top
                                            └──────────┬─────────┘
                                                   既存formatter
                                                       ↓
                                                stdout / exit0
```

処理順と出口の原本は `「既存引数検証→採用除外FILE→本文」`、`「除外exit2」`、`「本文のみ失敗は既存exit1」`。[VERIFIED: .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:23-25] 図はこの仕様の接続案であり実装済み状態を表さない。

### Component Responsibilities / 最小変更候補

以下は配置提案であり、新規関数名・APIは未固定。既存モジュールを維持する。[VERIFIED: _bmad-output/initiative-r-6442a149/architecture/architecture.md:73-94]

| 対象 | 推奨変更 | 保持する境界 |
|---|---|---|
| wordfreq/__main__.py | exclude引数・help、検証後の一覧取得、トークンフィルタ、除外例外だけexit2 | 全形式共通のpairs生成、basename処理、stdout書込、既存引数検証 |
| wordfreq/sources.py | 除外専用の小さい読込関数を置く。UTF-8-sig／行解釈／casefold集合、InputErrorへ原因連鎖 | FileSource.read_textの本文UTF-8契約は無変更 |
| README.md | 構文・一覧例・処理順・本文と除外の失敗コードを区別、HTML総数の説明を更新 | 既存利用例・format公開契約・無関係な末尾注記を不要に変更しない |
| tests/test_sources.py | 読込集合の直接assert、原因連鎖、入力バイト不変 | 本文FileSourceの既存試験を残す |
| tests/test_cli.py | 共通ヘルパーで正常／空／行／Unicode／複数指定／失敗／順序／案内を追加 | 既存全形式、未指定、保存済みバイト回帰を保持 |
| tokenizer / aggregator / formatters | 原則変更不要 | Unicode抽出、初出順の安定順位、純粋整形とCSS |

[VERIFIED: wordfreq/sources.py:17-22; tests/test_sources.py:64-80] 本文読込の実定義は `with open(self._path, "r", encoding="utf-8") as source:`、失敗は `except (OSError, UnicodeDecodeError) as error:` から `raise InputError(f"{self._path}: {error}") from error`。既存直接試験が `{"encoding": "utf-8"}` まで確認するため、FileSourceを一律utf-8-sigへ変更しない。除外専用読込にだけcodecを適用する。

### Pattern 1: parseで開かず、検証後に最後の文字列を読む

[CITED: https://docs.python.org/3.14/library/argparse.html#type] 公式文書は複雑な資源管理をparse後で行い、withでファイルを扱うことを推奨する。既定storeで採用パスを保持し、appendやFileType、I/Oするtype変換は使わない（実装提案）。複数指定の前のパスを開かないことはparserの値試験だけでなく、read呼出し追跡と実CLIのmissing→validで確定する。

### Pattern 2: 専用一覧文法、本文トークン順を保持

[VERIFIED: wordfreq/tokenizer.py:6-18; _bmad-output/initiative-r-6442a149/architecture/architecture.md:59-65] 本文の定義は `_WORD_RE = re.compile(r"\w+", re.UNICODE)` と `return (token.casefold() for token in tokenizer(text))`。除外は本文抽出を流用せず、デコード済みファイルを行ごとにstripして空／先頭#を除き、行全体をcasefoldして集合へ入れる。集合から出力列を構築せず、既存トークンiteratorを順に通して非該当語だけ数える（実装提案）。

### Pattern 3: 計数前除外で総数の分岐を増やさない

[VERIFIED: wordfreq/__main__.py:34-44; wordfreq/aggregator.py:11-17] 現行選択は `if count >= args.min_count`、順位は `return sorted(counts.items(), key=lambda wc: -wc[1])[:n]`。除外済みcountsの回数和を従来位置で取り、選択前の総数を渡す。除外未指定なら同じ全countsとなるため、旧総数のための別formatterや条件分岐は不要とする（実装提案）。

### Anti-Patterns to Avoid

- 表示後削除／Counterを削除してから古い総数だけ残す: 承認された計数前除外と総数がずれる。
- Counterキーやsetをソートし直す: 相対初出順を失う。
- 除外FILEを本文用tokenizerへ渡す: 行内空白、ハイフン、途中#の非分割契約を破る。
- catch一箇所で全InputErrorをexit2化: 本文失敗exit1を壊す。
- stdoutの逐次出力: 失敗前に部分結果が出る。

これらの回避理由: [VERIFIED: _bmad-output/initiative-r-6442a149/architecture/architecture.md:29-71; .planning/argonauts/r-6442a149-learnings.md:49-53]。

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | 根拠 |
|---|---|---|---|
| BOM処理 | 全行のBOM削除／手製decode推測 | 除外専用openのutf-8-sig、厳格decode | [CITED: https://docs.python.org/3.14/library/codecs.html#encodings-and-unicode] |
| 反復オプション | 全FILEを読んで後から最後を選ぶ独自action | argparseの値保存＋parse後1回読込 | [CITED: https://docs.python.org/3.14/library/argparse.html#action] |
| 大小文字比較 | lower、正規表現、元表記復元、追加Unicode正規化 | 本文と同じcasefold | [VERIFIED: wordfreq/tokenizer.py:14-18; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:21-22] |
| 順位・全形式比較 | 新しい順位アルゴリズム／HTML文字列split | 既存top_words、CLIHTML、assert_output_bytes | [VERIFIED: wordfreq/aggregator.py:11-17; tests/test_cli.py:201-239,425-441] |
| HTML安全性 | 新テンプレート／新CSS／独自escape | 既存format_htmlと静的構造assert | [VERIFIED: wordfreq/formatters.py:17-27; tests/test_formatters.py:94-178] |

## Common Pitfalls

| Pitfall | 判別する試験・回避策 | 根拠 |
|---|---|---|
| BOMが語の一部になる／各行BOMまで除く | ファイル先頭BOM＋空白付きAPPLEの直接集合assert。ファイル全体のdecode時だけBOM除去 | [VERIFIED: spec.md（下記Sourcesの差分）:28-45]; [CITED: https://docs.python.org/3.14/library/codecs.html#encodings-and-unicode] |
| 空行・コメントが集合に残ってもCLI結果だけは通る | 無視項目が集合に存在しないことを直接assert | [VERIFIED: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:31-41] |
| 途中#やハイフンを勝手に分割 | 混合文字列例の残存foo/bar/apple/noteを明示assert | [VERIFIED: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:43-45] |
| ASCIIだけの試験でlower誤実装が通る | 実際のStraßeを本文と一覧の双方で使い、一覧STRASSEでも再確認 | [VERIFIED: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:50-56] |
| 結果exitだけで「前FILE未読」「本文未読」と判定 | 直接呼出しspyでパス順・呼出しなしをassert、実CLI複合失敗も検査 | [VERIFIED: .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:23-25] |
| 権限不足のつもりで実際は読める | subprocessと同一実効ユーザーでPermissionErrorを直接確認してからCLI。root等で読めたら成功扱いしない | [VERIFIED: tests/test_cli.py:503-527] |
| help試験がHTMLバッファ書込みで壊れる | 正常HTMLはsubprocessのbytes helperを優先。順序失敗の直接試験は出力前に終了する経路でcapsysを使う | [VERIFIED: wordfreq/__main__.py:49-53; tests/test_cli.py:418-441,624-644] |
| 全語除外で既存HTML案内も消す | 空表・見出し・既存案内とtotalを別assert。独自案内は足さない | [VERIFIED: tests/test_formatters.py:164-178] |
| 旧学習の語昇順を復活／旧ingest衝突で停止 | 今回CONTEXTと現行初出順を優先し旧履歴は変更しない | [VERIFIED: CONCEPTS.md:49-55; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-10,32-38] |
| 旧HTML検証ツールをPhase8の受入に転用 | 旧固定起点・変更許容範囲は今回とは異なる。通常pytest回帰と今回文字証拠を分離する | [VERIFIED: docs/wordfreq-html-verification.md:16-24; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-10] |

## Code Examples

以下は新APIのstubではなく、今回読了した既存実装の引用。ソースパスは参照先であり生成先ではない。

```python
# wordfreq/tokenizer.py:14-18
return (token.casefold() for token in tokenizer(text))

# wordfreq/aggregator.py:17
return sorted(counts.items(), key=lambda wc: -wc[1])[:n]

# wordfreq/__main__.py:35-38
 total = sum(counts.values())
 selected_counts = Counter({word: count for word, count in counts.items()
                            if count >= args.min_count})
 pairs = top_words(selected_counts, args.top)
```

[VERIFIED: wordfreq/tokenizer.py:14-18; wordfreq/aggregator.py:11-17; wordfreq/__main__.py:34-38] 上記は抜粋であり実行ファイルではない。計画ではcasefold済み列から一致語だけ除く接続を追加し、これらの集計・選択契約を維持する。

## Validation Architecture

### Test Framework

[VERIFIED: tests/test_cli.py:11-20; tests/test_sources.py:4-7; terminal環境probe] pytest基盤があり、使用可能な既存環境はpytest 9.0.3。以下の `PYTHONPATH` 付きコマンドは既存文書の実ファイル実行方式を踏襲する。[VERIFIED: docs/wordfreq-html-verification.md:7,18-22]

| Property | Value |
|---|---|
| Framework | pytest 9.0.3 / CPython 3.12.15（今回version probeのみ） |
| Config | pyproject.tomlにpytest専用設定なし。既存tests配下の標準検出を維持（追加設定不要） |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` |
| Research execution | 上記の機能試験は未実行。既存version probeのみ実行 |

[VERIFIED: pyproject.toml:1-15] 設定原本は全文読了したがPython対応範囲を宣言する値はない。これをPython 3.14の互換／非互換の証明にしない。試験環境の選択は既存pytestが実在してimportできるかを基準にし、プロジェクトの対応版を新規固定しない。

### Phase Requirements → Test Map

すべて既存モジュールを対象にした実在pathのコマンド。✅は**ファイルがある**という意味で、新しい除外ケースの存在・合格ではない。各REQの新assertはBuilderが書いてから実行する。以下は試験設計提案。[VERIFIED: tests/test_sources.py:7-80; tests/test_cli.py:418-441,598-817]

コマンド中の `P` は上表と同じ `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` の説明上の省略で、shell変数・aliasを作る指示ではない。PLANへは展開した完全なコマンドを書く。

| Req ID | Behavior | Test Type | Automated Command（Pを展開） | File Exists? |
|---|---|---|---|---|
| REQ-28 | 全形式、順序、重複、最後FILE | 実CLI＋parser／read spy | `P tests/test_cli.py -q -x` | ✅ 新case追加必要 |
| REQ-29 | BOM・空白・コメント・改行・行全体 | 直接unit＋実CLI | `P tests/test_sources.py tests/test_cli.py -q -x` | ✅ 新case追加必要 |
| REQ-30 | ASCII混在と実Unicode casefold | 直接unit＋実CLI＋本文回帰 | `P tests/test_sources.py tests/test_tokenizer.py tests/test_cli.py -q -x` | ✅ 新case追加必要 |
| REQ-31 | 全読込失敗・引数／除外／本文優先 | 直接spy＋実CLI | `P tests/test_sources.py tests/test_cli.py -q -x` | ✅ 新case追加必要 |
| REQ-32 | help記載とREADME例の再現 | 実CLI＋文書assert | `P tests/test_cli.py -q -x` | ✅ 新case追加必要 |
| REQ-33 | 全語除外・未指定バイト／Unicode／順位／空／本文エラー | 実CLI＋全回帰 | `P -q` | ✅ 新caseと全件回帰必要 |
| REQ-34 | 新依存等なし／対象headの独立実行証拠 | 自動scope／入力不変＋品質の文字原本照合 | `P tests/test_cli.py -q -x` ＋ `git diff --stat` / `git diff -- pyproject.toml wordfreq tests README.md` | ✅ 既存scope試験＋今回証拠は新規必要 |
| REQ-35 | 計数前除外・選択前総数／旧総数維持 | 実CLI＋直接composition spy | `P tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py -q -x` | ✅ 新case追加必要 |

REQ-34の標準添付・受取可読性はpytestだけで証明できない。品質が対象headで自分の実行原本を保存し、PMが文字原本を読める形で引き渡す手続を別のgateとする。[VERIFIED: .planning/argonauts/r-6442a149-learnings.md:39-44,53; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:32-34]

### Scenario Coverage Matrix（漏れ防止の設計原本）

各行は承認scenarioのテスト化案であり、実行結果ではない。全形式共通と書いた項目はtext/json/htmlパラメータ化。期待値は製品関数で再計算せず原本値を固定する。[VERIFIED: openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:5-114]

| 原本scenario | 入力／判別点とassert |
|---|---|
| EX-1 指定語の全出現 | Zoo apple APPLE zoo banana／apple → zoo2,banana1、appleなし、HTML総数3 |
| EX-1 topより前 | 同本文／zoo、top1 → apple2。先にtop1を選んでから削除する誤実装を拒否 |
| EX-1 同数と重複 | beta apple alpha／apple,APPLE,aPpLe → beta1,alpha1。単一apple版と全形式stdout・総数一致 |
| EX-1 該当語なし | 未指定と語・回数・順位・総数・exit／stderr一致 |
| EX-1 最後FILE | missing→validは成功、valid→missingは2、最後空なら前の一覧無効。spyで実際の読込対象も確認 |
| EX-2 空行／コメント | apple marker banana／空行,#marker,apple → marker1,banana1。直接集合に空文字／コメントなし |
| EX-2 有効項目なし | 空FILE、空白＋コメントのみをそれぞれ未指定と全形式比較 |
| EX-2 BOM／改行 | 先頭BOM＋空白のみ＋`  #marker  `＋`  APPLE  ` をLF／CRLF／終端改行なしで用意。直接集合と全形式marker1,banana1 |
| EX-2 行全体 | foo bar foo_bar 123 foo-bar apple note／foo bar,foo_bar,123,foo-bar,apple#note → foo2,bar2,apple1,note1。直接集合は行文字列を保持 |
| EX-3 混在表記 | Apple APPLE apple banana／aPpLe → banana1 |
| EX-3 Unicode | STRASSE Straße banana／StraßeとSTRASSEを別々に実行 → どちらもbanana1 |
| EX-4 不存在 | 読める本文＋missing除外、2／stdout空／stderrに対象パスと原因 |
| EX-4 不存在以外 | 除外permission／directory／decodeを全形式で実CLI。直接読込は原因例外の連鎖もassert |
| EX-4 複合失敗 | top/min-countの0・負・非数／非整数・値欠落、format不正／欠落、exclude値欠落、位置引数不正と読めない両FILEを組合せる。引数エラーで読込0回。両FILE失敗で除外のみ読込・2。除外成功＋本文失敗と未指定本文失敗で1。helpも読込0回 |
| EX-6 全語除外 | Apple apple／apple → text空、JSON `[]\n`、HTMLデータ0行＋既存案内＋総数0。全形式exit0、追加専用案内なし |
| EX-5 案内 | --helpに構文、行規則、casefold、最後FILE、exit2、空結果。READMEの本文・一覧例をtmp_pathにそのまま書き、実CLI再現 |
| EX-5 新旧回帰 | 既存全件＋新ケース。未指定と空／コメント／無一致一覧の比較、入力両ファイルのバイト不変、複数hash seedで指定時の全形式stdout一致 |
| HTML-2 top可変 | 既存のzoo apple zoo banana apple cherry、top1/2/10、総数6と既定min1を維持 |
| HTML-2 別頻度 | beta beta beta alpha gamma alpha delta、top2 → beta3,alpha2、総数7 |
| HTML-2 既定／不正top | 11種類以上で既定10行、topが残存種類数より大きければ全件、不正topは2／HTMLなし。除外ありでの残存種類数も追加 |
| HTML-2 min/top両方 | 上記beta本文、min2/top1 → beta3・総数7、min4 → データ0行でも総数7（未指定の旧契約） |
| HTML-2 除外後総数 | Zoo apple APPLE zoo banana／apple、min2/top1 → zoo2のみ／総数3。minを上げて表示0行でも除外後の正の総数を保持する境界も追加 |

直接順序試験ではCLIがimportした参照をpatchし、呼出し履歴をパス付きで記録する（実装提案）。count_wordsに渡されたトークンをspyで消費し、除外語が**計数前**に落ちていることを検査する。実CLIだけでは計数後の削除が同じ結果になるため、ソース順序／直接compositionも併用する。[VERIFIED: tests/test_cli.py:624-644,759-793; _bmad-output/initiative-r-6442a149/architecture/architecture.md:29-33]

### Sampling Rate

- タスクごと: Quick run command。単純unit追加時は対応モジュールを先にRED→GREEN、その後quickで自分と先行成果を確認する（計画提案）。
- 直列PLANの完了ごと／phase gate: Full suite command。独立品質が対象headで再実行する。研究時点では所要時間未測定であり、30秒以内とは保証しない。遅い場合も未実施を合格にしない。
- pytestの `-k exclude` だけに依存しない。ケース名の未一致で実行0件になる設計より、既存モジュール全体を指定する（計画提案）。

### Wave 0 Gaps

- 新framework・専用設定・新conftestは不要とする（既存pytestパターンを再利用する提案）。
- **未実装assert:** tests/test_sources.pyに除外読込集合／原因、tests/test_cli.pyに上表の全形式・順序・案内を追加する。ファイルは実在するが除外機能の試験は未作成。[VERIFIED: tests/test_sources.py:1-80; tests/test_cli.py:1-819]
- **未作成の証拠原本:** 今回対象head・入力両FILE・argv・環境・stdout/stderr bytes・exit・条件別判定を保存する工程文書。独立品質が実行してから記入する。PLANは保存対象を指示できるが未作成スクリプトの実行を前提にしない。
- **実行系の注意:** 既定pythonではpytestをimportできない。下記の確認済み既存系統を使う。研究ではinstallしない。

## Planning Implications（PLANそのものではない）

[VERIFIED: openspec/changes/r-6442a149-exclude-file/tasks.md:5-21; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:26-28,59-62] 完了済みは `「[x] 1.1」`、実装・統合は `「[ ] 2.1」`、`「[ ] 2.2」`、`「[ ] 3.1」`。1.1を再実行せず、未実行項目をチェックしない。以下は少数PLANへの分け方の提案であり、PLANファイルや番号は本研究で作らない。

1. **先行の正常系縦切り:** parser＋専用読込＋計数前フィルタ＋全形式の単純例を最初に実装し、その同じPLANで行規則／Unicode／重複／最後FILE／全語除外／総数へ拡張。helpとREADMEの正常再現例を同時に追加する。OpenSpec 2.1主体。loaderの例外を握り潰すstubや本文の既存契約変更を避ける。
2. **後続の失敗と統合:** 2.2の全原因、順序spy、実CLI優先順位、本文exit1保持、異常時help／READMEを完了し、3.1の既存全件＋全scenario照合と文字証拠へ続ける。先行PLANに依存し同じ依頼branchで直列実行。品質の独立再実行・標準添付はBuilder自身の試験合格とは分離する。

先行の正常系だけでphase完了にしない。一般的な終了・例外経路を先行で最小実装しても、2.2完了は直接試験と実CLIの条件別照合が揃った後に限る（計画提案）。

## Environment Availability

今回のterminal probe実測。コマンド実行失敗を機能不合格やPython対応版の判定にすり替えない。

| Dependency | Available / Version | 運用上の扱い |
|---|---|---|
| PATH上のpython | Python 3.14.9、`python -m pytest --version` は失敗 | `No module named pytest`。この系統でのpytestをPLANに無条件指定しない |
| PATH上のpytest | コマンドpathは存在するが実行失敗 | `ModuleNotFoundError: No module named 'pytest'`。コマンドの存在だけでは利用可能でない |
| /usr/bin/python3 | Python 3.12.15 | 既存文書にある環境を独立probeで確認 |
| 既存PYTHONPATH付きpytest | pytest 9.0.3 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --version` 成功。検証実行は後続 |
| 実効UID | 1000 | permission試験は実際のPermissionErrorを毎回確認。UIDだけで拒否成立を保証しない |
| uv | command path確認済み | 今回install／新環境作成には使わない |
| Context7 / ctx7 | この研究で使用可能なContext7 toolなし、ctx7もcommand lookupなし | 公式Python URLを直接読んでfallback。未承認installしない |
| GSD | runtime launcherから利用 | `query init.phase-op 8` は `"phase_found": true`、`"phase_number": "08"`、`"has_research": false`、`"has_plans": false`（研究開始時） |
| graphify | `graphify status` は `"disabled": true` | graphなしで原本・コードを調査。設定を変更しない |

追加製品サービスは不要。[VERIFIED: _bmad-output/initiative-r-6442a149/architecture/architecture.md:73-77] 外部runtimeの新規導入監査は対象外だが、pytest実行環境だけは上記の障害と既存代替を明示した。ブラウザの起動可否は本研究では未probeであり、画像閲覧を完了したとは扱わない。

## Security Domain

[VERIFIED: .planning/config.json:49-51; wordfreq/sources.py:17-22; wordfreq/formatters.py:17-27; _bmad-output/initiative-r-6442a149/architecture/architecture.md:23,33,71] ASVS分類はローカルCLIへの適用範囲整理であり、Webアプリ認証機能を追加する理由ではない。

| ASVS Category | Applies | Standard Control / 設計提案 |
|---|---|---|
| V2 Authentication | なし | 認証サービスなし、追加しない |
| V3 Session Management | なし | セッションなし、追加しない |
| V4 Access Control | ローカルファイル境界のみ | OS既存権限でread-only、昇格・権限緩和しない。指定パスを勝手に別パスへ補正しない |
| V5 Input Validation | あり | argparseの既存検証、厳格UTF-8-sig、一覧行規則、失敗時後段I/Oなし |
| V6 Cryptography | 製品機能としてなし | 暗号・独自hash実装を追加しない。証拠同一性が必要なら既存標準コマンド |

| Threat Pattern | STRIDE | Mitigation / 判別 |
|---|---|---|
| パス文字列をshell実行に渡す | Tampering / Elevation | openでローカル読込のみ。shell評価・URL読込・新サービス禁止 |
| 除外成功前に本文・stdoutへ進む | Information Disclosure / Tampering | 直列I/Oとstdout空、直接spyと実CLI複合失敗 |
| HTMLへ除外パスや親ディレクトリが混入 | Information Disclosure | formatterは既存の本文basename＋pairs＋totalだけ。除外パスをmetadataに渡さない |
| タグ／CSS／外部参照の混入 | Tampering / Information Disclosure | 現行escape・静的構造・固定CSSを保持。既存安全性試験と指定時のHTML確認 |
| 品質未実施や未閲覧を合格と記録 | Repudiation | 実対象head・入出力・終了結果を条件別保存。画像は品質の実閲覧結果を文字化し、PMへ画像閲覧を要求しない |

[VERIFIED: tests/test_cli.py:153-182; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:32-38] permission失敗fixtureの一時ファイルのmode操作は既存試験パターンであり、製品の権限追加とは別。製品自身によるchmod、権限昇格、実入力の書換えは追加しない。新機能試験でも本文と除外一覧のバイト不変を確認する（提案）。

## State of the Art / Compatibility Boundary

[VERIFIED: CONCEPTS.md:49-55; .planning/REQUIREMENTS.md:106,115; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-10] 現行は「頻度降順・同数初出順」、古いPhase1の語昇順は履歴。HTML総数の旧説明は未指定・min-countのみでは依然有効、今回の名前指定除外でのみ除外後総数へ拡張する。旧ingest衝突記録を消さず、CONTEXTで承認された新phaseの範囲を採用する。

[VERIFIED: .planning/STATE.md:4-8,94-104] STATE frontmatterは `current_phase: 7`、`status: verifying` の旧作業を残す一方、履歴には `Phase 8 added` がある。調査対象は明示指定の08であり、STATEを修正したり旧phase検証を巻き込まない。公式initの08存在確認を使用した。

## Assumptions Log

| # | Claim | Section | Risk if Wrong / 後続の扱い |
|---|---|---|---|
| A1 | [ASSUMED] quick/fullの所要時間は未測定 | Validation Architecture | 時間上限や件数を創作しない。Builder／品質が実測して記録 |
| A2 | [ASSUMED] 品質実行環境でも今回probeと同じpytest系統を使用できる | Environment Availability | 独立品質が自環境でversionとimportを再確認。利用不可なら未検証を報告 |

配置・少数PLAN分割・テスト追加方法は明示的な設計提案であり、存在するAPIや合格結果の仮定ではない。製品判断の未決事項は追加しない。

## Open Questions

- 製品判断に関する停止事項なし。OQ7/8は背景不足のみで受入条件にしない。[VERIFIED: .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:32-34,64-66]
- 既定pythonのpytest欠落は既存代替で回避可能と確認したが、全件成功と時間は未検証。研究の完了と機能・独立品質の完了を区別する。
- 旧HTML collectorには旧依頼の固定scopeがある。Phase8証拠へそのまま流用しない。今回の文字証拠を最小に構成し、画像を得た場合の実閲覧記録を品質へ引き渡す。旧phaseの全ブラウザ受入を再開しない。[VERIFIED: docs/wordfreq-html-verification.md:16-24; .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-10,32-38]

## Sources

### Primary — 今回全文／該当定義をread_fileした原本

- `.planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md:8-66` — 承認済み全判断、裁量、範囲、原本参照。
- `.planning/REQUIREMENTS.md:104-126` — REQ-28〜35。
- `.planning/STATE.md:4-8,94-104` — 旧状態と今回phase追加の分離。
- `.planning/argonauts/r-6442a149-prd.md:1-163` — 結合proposal/spec/tasks原本。
- `_bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md:46-118,144-153` — FR／RULEと期待値、非目標。
- `_bmad-output/initiative-r-6442a149/architecture/architecture.md:23-94` — AD-1〜4、配置の裁量。
- `_bmad-output/initiative-r-6442a149/decisions-oq1-6.md:1-28` — 採用判断の来歴。
- `_bmad-output/initiative-r-6442a149/brief/brief-wordfreq-exclude.md:25-102` — 背景資料。再ingestしない。
- `openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md:5-114` — 本文中の「spec.md」はこの差分を指す。
- `openspec/changes/r-6442a149-exclude-file/tasks.md:5-21` — 1.1完了、2.1／2.2／3.1未完。
- `.planning/INGEST-CONFLICTS.md:5-23` — 旧lockedとの衝突履歴。現在の研究停止判定には転用しない。
- `wordfreq/__main__.py:13-54`、`sources.py:5-22`、`tokenizer.py:6-18`、`aggregator.py:6-17`、`formatters.py:6-38,103-127` — 既存定義。
- `tests/test_cli.py:1-819`、`tests/test_sources.py:1-80`、`tests/test_sources_boundary.py:1-42`、`tests/test_tokenizer.py:1-60`、`tests/test_aggregator.py:1-55`、`tests/test_formatters.py:1-262` — 実在する試験と再利用パターン。
- `tests/test_html_verifier.py:1-55`、`docs/wordfreq-html-verification.md:1-90` — 旧証拠基盤の責務／scope／既存実行環境。
- `README.md:7-43`、`CONCEPTS.md:41-59`、`pyproject.toml:1-15`、`.planning/config.json:21-64` — 現行公開説明・語彙・依存・workflow。
- `.planning/argonauts/r-6442a149-learnings.md:14-54` — 旧順序への注意、直接境界、判別力、証拠配送。

### Official Documentation（CITED、取得済み／実装未試行）

- https://docs.python.org/3.14/library/argparse.html#action — 既定store。
- https://docs.python.org/3.14/library/argparse.html#type — parse後のI/O／with推奨。CPython公式原本 `Doc/library/argparse.rst:755-764,1182-1197` も取得してread_fileした。
- https://docs.python.org/3.14/library/codecs.html#encodings-and-unicode — UTF-8-sigの先頭BOM除去。CPython公式原本 `Doc/library/codecs.rst:1033-1059` も取得してread_fileした。
- https://docs.python.org/3.14/builtins/stdtypes.html#str.casefold — ß／ssの差を取得本文の該当箇所で確認。

### Official CLI / 実測

- runtime launcher経由 `query init.phase-op 8`、`graphify status`。新phase存在、planなし、graph無効を確認。
- `query research-plan` がContext7を指定したが、利用可能tool／ctx7がなく公式URLへfallback。取得概要は同じprofileのresearch-storeへLOWで保存した。
- `query classify-confidence --provider local --verified` と `--provider webfetch --verified` はLOW。公式文書の内容確認を取り消すものではないが、package監査なしの調査をHIGHと偽装しない。
- Python／pytest version probe、UID、git status／HEAD、date。調査開始時HEAD `61705de6015280bc7368a8cdac8b33edef7711ed` は承認原本headとは別。

## Metadata

- **実行したこと:** 必読原本・コード・実在試験の読取り、公式GSDの読取り判定、公式Python資料取得、環境version probe、研究原本作成。
- **実行していないこと:** 製品／試験／設定／PLAN変更、機能試験、既存全件pytest、ブラウザ検証、commit／push／Kanban。開始時の既存dirty文書には触れない。
- **Confidence breakdown:** 標準ライブラリの意味は公式資料でCITED、現行定義と要求はread_fileでVERIFIED、配置・分割・追加試験は設計提案、未測定事項はASSUMED。provider分類の総合表記はLOWのまま。
- **Research date:** 2026-11-28。
- **Valid until:** 原本／製品head／実行環境が変更された時点で該当箇所を再確認する。時間経過だけで機能試験済みへ昇格しない。
