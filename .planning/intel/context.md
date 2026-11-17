# Context (intel)

Running notes from DOC-classified sources, appended near-verbatim with source attribution.

## Brief — problem and solution
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

wordfreq は、テキストファイルを読んで単語の出現回数を多い順に表示する小さなコマンドラインツール。`python -m wordfreq <file>` で実行し、表示件数は `--top N`（既定 10）、出力形式は `--format text|json`。単語の切り出し・正規化（大文字・小文字の同一視）を行う部品と、集計・出力整形を行う部品を分離し、入力元（標準入力や URL）を後から追加できる構成にする。画面（UI）は作らない。主利用者はこの repository を使うエンジニア（依頼者自身）。価値は性能ではなく、正規化・並び順・出力形式の標準化と、入力元を拡張できる設計の明確さ。対抗案は即席パイプライン（`sort | uniq -c | sort -rn`）、既存 PyPI パッケージ、何もしない、の 3 つ。即席運用のコスト記述は作成した仮説（A-4）。

## Brief — success criteria（WF ID 対応）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

1. `python -m wordfreq <file>` が実行でき、出現回数の多い順に出力する。`--top N` で表示件数を指定でき、既定は 10。（WF-01, WF-02）
2. 切り出し・正規化の部品と集計・出力整形の部品が分離している。分離は部品を独立に呼ぶ単体試験で確認でき、入力元を追加できる構成の判断は WF-06 の設計文書に残す。（WF-04, WF-06）
3. `--format text|json` の 2 形式で出力でき、JSON は機械可読な構造（単語と回数の配列）。（WF-03）
4. pytest の単体試験があり、CI で通る。（WF-07）
5. 「まだ決まっていない点」2 件は明確な挙動として決定し、試験で確認できる。（D-1, D-2, D-3, WF-08）
6. 工程側の要求として、作業中に気づいたことが学習の候補として 2 件以上この依頼の記録に残る。

PRD 側の ID 対応（prd-wordfreq-cli.md Document purpose より）: WF-01→FR-1、WF-02→FR-2、WF-03→FR-3、WF-04→FR-5、WF-05→FR-4、WF-06→FR-6、WF-07→FR-7、WF-08→FR-1。FR-8 は PM 方針由来の全体制約。

## Brief — v1 scope WF-01..WF-08
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

- WF-01: `python -m wordfreq <file>` での実行。
- WF-02: `--top N`（既定 10）。N は 1 以上の整数。不正値は使い方エラー（非 0 終了・stderr）で終了。
- WF-03: `--format text|json`（既定 text）。不正値は使い方エラーで終了。
- WF-04: 単語の切り出し・正規化（大文字・小文字を同一視）を集計・出力整形から独立した部品にし、各部品を独立に呼ぶ単体試験を付ける。
- WF-05: 同回数ワードの並び順は決定論的とする（決定 D-2）。
- WF-06: 入力元（ファイル以外に標準入力・URL）を後から追加できる構成とし、構成判断を設計文書（OpenSpec 変更の design.md。ADR に相当するもの）に残す。
- WF-07: pytest による単体試験。CI で通る。対象は CI が使う現代的な CPython 3 の 1 つの版とし、バージョン横断の互換コードは不要。
- WF-08: 入力ファイル不存在とテキストデコード失敗はエラーメッセージを stderr に出して非 0 で終了する。空ファイルは結果 0 件として正常終了する。

## Brief — v1 の決定 D-1〜D-3
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

- D-1（空白で区切られない言語）: v1 では対象外。空白・句読点を区切りとするトークナイザ前提とし、日本語のような言語の形態素解析は明示的に範囲外。トークナイザは差し替え可能な部品として設計し、将来の決定余地を残す。
- D-2（同回数ワードの並び順）: 出現回数の降順、同じ回数の単語は正規化後単語の昇順（辞書順）。決定論的で試験可能な挙動。
- D-3（切り出しの定義）: 単語は「Unicode の単語構成文字（Python `re` の `\w`。英数字・underscore を含む）の連続する最大長」として抽出し、`str.casefold()` で正規化する。句読点・記号は単語に含めない。テストで確認できる形として仕様化する。

## Brief — v1 の範囲外
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

GUI・画面、URL 入力そのもの（WF-06 の拡張性だけ）、日本語形態素解析の実装（D-1 により将来の決定待ち）、標準ライブラリ以外のランタイム依存の追加。依存管理上 `pyproject.toml` 等の追加が避けられない場合は、smart マージ方針で人の承認対象になることを前提に、必要最小限に留める。

## Brief — assumptions A-1〜A-5
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/_bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md

- A-1: 依頼者以外に頻度集計を必要とするエンジニアがいるという利用者像の一般化は推定。依頼者自身が必要な点は依頼本文に裏付けがある。
- A-2: 「ランタイム依存を増やさない（標準ライブラリ中心）」は PM 指摘からの方向性。追加が必要な場合の例外は Scope に記載。
- A-3: 既存 PyPI パッケージとの比較は詳細調査をしない早断。価値の所在が変わらない限り再調査は不要と判断。
- A-4: 即席パイプラインでの現在の運用とそのコストは作成した仮説で、依頼本文に事実記述はない。
- A-5: ローカルパッケージ名 `wordfreq` と同名の PyPI パッケージの取り違えは、依存を追加せず repository 内で `python -m` 実行する範囲では問題にならないと判断。外部パッケージを CI に入れる日が来たら再評価する。

## wordfreq CLI implementation tasks
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/tasks.md

実装順は部品（内側）から外側。各 task はその時点で pytest が通る状態を保つ。

- 1.1 `wordfreq/tokenizer.py`（`\w` 連続抽出 + `casefold()`、差し替え可能な関数/注入点）。単体試験: 大文字小文字の同一視、句読点を語に含めない、underscore 語の固定、日本語テキストで決定的な出力。
- 1.2 `wordfreq/aggregator.py`（`count_words`、FR-4 ソートの `top_words`）。単体試験: 回数降順、同数は単語昇順、`--top` 超過時の全件、空入力。
- 2.1 `wordfreq/sources.py`（`TextSource` プロトコル + `FileSource`、UTF-8 デコード、`InputError`）。単体試験: 正常読み込み、不存在ファイル、デコード失敗、空ファイル。
- 2.2 `wordfreq/formatters.py`（design D-A の `<count>\t<word>` 1 行 と D-E の JSON 配列、0 件は `[]`）。単体試験: text/json 双方の出力構造、順序の保持、`json.loads` 可読性。
- 2.3 入力取得境界越しの試験（集計経路が `TextSource` を介してのみテキストを受け取ること、aggregator 系試験が FileSource 非経由であること）。
- 3.1 `wordfreq/__main__.py`（argparse: ファイル引数ちょうど 1 個、`--top` 既定 10・1 以上整数、`--format text|json` 既定 text。exit code 0/1/2 の分岐は design D-C どおり）。CLI 試験: 正常系、`--top` 既定と指定、`--format json` 構造、不正値の exit 2、不存在ファイルの exit 1、引数個数エラー。
- 3.2 `pyproject.toml` 追加（`wordfreq` パッケージ、ランタイム依存ゼロ、pytest 開発依存）。`python -m wordfreq <file>` が repo 直下で動くことを確認。
- 3.3 CI の pytest ジョブの有無を確認し、無ければ workflow 変更（人の対応）として block 判定の準備をする（proposal Impact 参照）。

注記: tasks.md が参照する design の D-A / D-C / D-E は design.md の決定であり、design.md は現 ingest 集（--manifest 縮小後）の外。
