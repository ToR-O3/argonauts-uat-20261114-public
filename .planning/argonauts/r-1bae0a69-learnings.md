## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: wordfreq CLIへ `--min-length N` を追加するlight計画のための既存学習調査。N未満の単語を集計対象から除き、既定1・Nちょうどを含む境界・help・追加試験と既定互換試験を扱う。README.mdは変更しない。実装は後続の公式GSD quick --validateに委ねる。
- **Keywords Used**: wordfreq、tokenizer、Unicode、casefold、length／文字、filter、min-count／max-count／top、HTML、test-first、証拠、workflow、PM-readable。
- **Files Scanned**: 5 total files（`docs/solutions` 内の学習Markdown全5件をnative search_filesのfrontmatter keyword prefilterで検索、候補5件の先頭30行を確認。ディレクトリ2件と `.gitkeep` 1件は学習ファイル数から除外。全文読取りは関連する3件のみ）。
- **Relevant Matches**: 3 files（強関連2件、隣接する中関連1件）。残り2件はCI固有条件と添付拒否固有条件で、今回の最小文字数計画への直接性が弱いため除外。
- **Search Scope**: rootは `docs/solutions` のみ、packなし。実在する `best-practices/` と `workflow-issues/` を探索し、種類を限定せず全ツリーを検索した。候補5件のため「3件未満時の本文広域検索」は不要。`patterns/critical-patterns.md` は一覧に存在せず、読取りを行っていない。
- **Grounding**: 最初に `CONCEPTS.md` 全文を確認。現在の契約との照合だけを目的に `wordfreq/tokenizer.py`、`wordfreq/aggregator.py`、`wordfreq/__main__.py` をread_fileで参照した（検索rootの拡張ではない）。`wordfreq/cli.py` は存在せず、実際のCLI入口は `__main__.py`。製品試験・未作成の検証コマンドは実行していない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 強。最小文字数の対象である「語」を、空白区切りやCJK文字単位と誤解するとフィルタ境界の設計も試験も誤る。フィルタ追加で順位契約も壊さない必要がある。
- **Key Insight**: 既定はUnicode `\w+` の最長列で、数字・下線も含み、CJKの連なりは1トークン。差し替え境界はトークン化方針だけで、後段casefoldは共通。現行 `tokenizer.py:6-18` と一致する。新フィルタの試験ではASCIIだけでなくCJKとcasefoldによる長さ変化を区別する入力を計画し、何の長さを測るかを明示する。
- **Severity**: medium
- **現行との差異**: 2026-11-17の記事34行・55-57行の「同頻度はコードポイント昇順」は過去契約。現在の `aggregator.py:11-17` は回数だけの安定ソートで、Counterの正規化後初出順を保持し、その後topを適用する。`CONCEPTS.md:49-51` も旧契約の意図的置換を明記。古い語順キーを復活させない。複数PYTHONHASHSEEDで決定論を確かめる考え方は利用できるが、この記事の過去の合格件数・ハッシュは今回の証拠に流用しない。

#### 2. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 強。今回もPMがread_fileで読める証拠が必要であり、実装者側の保存先や成功要約だけでは確認が成立しない。
- **Key Insight**: 保存済み・配送済み・受取側読取り済みは別の主張。後続実装の証拠は通常のMarkdown等に、対象head、入力、実行条件、実際の出力、終了状態、要求との対応、未確認事項を残す。原本への参照だけや圧縮アーカイブだけに依存しない。過去の画像閲覧代替は人が限定承認した個別事例であり、今回への恒久免除ではない。
- **Severity**: high
- **適用範囲**: 証拠配送の運用学習であって製品機能ではない。今回の小変更へ過去の大規模画像試験や添付作業を自動的に追加しない。この記事の旧head・合格件数は今回の検証結果ではない。

#### 3. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 中・隣接。直接はGit状態比較試験の学習だが、「合格だけでは検出能力を示さない」という原則はN境界のtest-first計画にも有用。
- **Key Insight**: 検出すべき失敗の種は別々に示す。後続では、N未満を残す誤り、Nちょうどを落とす誤り、オプション省略時の既定互換を壊す誤りを区別できる試験を先に用意する。CLIが未知オプションで停止しただけのREDは、フィルタの比較演算子の誤りを捉えた証拠とは区別する。状態比較の試験そのものを改修する場合だけ、scratchのステージ済み基底・cold copy等の詳細を適用する。
- **Severity**: medium
- **適用範囲**: 最小文字数用の変異試験が既存であるとは主張しない。本文の `git add -A` は隔離試験基底に関する過去の手順であり、この調査worktreeでの実行指示ではない。既存試験の現行内容の照合・実行は本調査では行っていない。

### Recommendations
- **語と長さの境界を明記する**: 既定トークナイザとcasefoldの契約は維持する。現在の `iter_tokens` は正規化後の語を返すため、その語の長さを測る案が自然だが、casefold前後のどちらを「文字数」とするかは学習文書に確定仕様がない。受付範囲を勝手に拡張せず、後続計画で採る解釈を明示し、casefoldで長さが変わる語とCJKで期待値を固定する。
- **HTML総数をうっかり変えない**: 現行 `__main__.py:35-40` は全countsの合計を先にtotalへ保存し、その後min-count/max-countの表示候補を作ってtopを適用する。長さフィルタを単にcount_words入力へ差し込むとtotalも変わるため、指定されたHTML総数保持と両立する配置を計画する。全トークンの総数を保持し、長さ条件を満たす集計・表示候補と分ける案を検討する。これは現行コードと依頼からの計画上の推奨で、過去学習の確定仕様ではない。
- **合成と初出順を保持する**: 長さ条件・min-count・max-countを適用した後にtopを行う。フィルタで残る語のCounter挿入順を崩さず、同頻度は正規化後初出順を維持する。text/json/htmlに同じ選択済みpairsを渡す構造を維持する。
- **test-firstの小さい順序**: N未満除外・Nちょうど保持・既定1と省略時互換の期待値を先に置く。次に既存頻度フィルタ/topとの合成、同頻度初出順、全除外時、HTML総数保持、`--help`説明を確認対象にする。入力値の許容範囲は受付と既存CLI規約に照らして明示し、新しい製品判断を追加しない。README.mdは変更しない。
- **証拠の範囲を正直に残す**: 後続の公式GSD quick --validateで実際に実行した結果だけをPM可読のテキスト原本に残す。複数シード実行を採用する場合も、その実測のみを記録する。ローカル合格をCIの独立検証証跡と呼ばず、対象headと報告側のheadを混同しない。本調査は計画材料の調査完了であり、機能実装・試験合格・PM読取り完了の主張ではない。
