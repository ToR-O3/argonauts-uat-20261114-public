## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: full依頼 r-5f8197e8 の計画。README の wordfreq 実行節に `python -m wordfreq input.txt --min-count 3` を1つ追加する。後続Builderと品質は同じUTF-8実入力を使い、閾値3のtext/json/htmlをそれぞれ直接実行して記録する。製品変更はREADMEのみ、工程文書は別扱いとする。
- **Keywords Used**: wordfreq, README, min-count, CLI, text/json/html, 入力境界, 初出順, フィルタ前総数, 文書のみ変更, 独立品質, verification, evidence, workflow, read_file, pm-readable。CONCEPTS.md の「決定論的順位」「要求ステータス」「検証対象head」「独立検証証跡」で用語を接地した。
- **Files Scanned**: 5 total files（docs/solutions/ 配下の全Markdownを内容検索し、候補5件のfrontmatterを読んだ。うち3件を全文読了。補助としてCONCEPTS.md、README.md、.compound-engineering/config.yamlを読了）。
- **Relevant Matches**: 3 files（強一致2件、条件付き中一致1件）。

検索根は docs/solutions/。実在カテゴリは best-practices/ と workflow-issues/ であり、文書・検証・工程を横断するため全体を検索した。title/tags/module/problem_typeと箇条書き条件を別々に大文字小文字非依存で検索し、統合候補は5件だった。設定は `docs_root: docs` のみでpack指定なし。patterns/critical-patterns.md は存在しない。

### Relevant Learnings

#### 1. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 強一致。今回もPMはread_fileで判定するため、Builder・品質が実行したという要約だけでは足りず、入出力原本をPMが開ける必要がある。applies_whenの「受取側にterminalやアーカイブ展開機能がない」と合致する。
- **Key Insight**: 保存済み・添付済み・受取側読取り済みは別の状態（31–45行）。CLI入出力を索引だけでなく読める個別原本として提供し、誰が実行し、誰が何を読んだかを分離する。PMのread_fileによる照合を、PM自身による製品再実行や画像閲覧と記述しない。68–81行の過去の画像閲覧代替承認は特定案件限定であり、今回への恒久免除ではない。
- **Severity**: high

#### 2. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 強一致。moduleがwordfreq CLIで、今回のUTF-8入力・正規化・順位・三形式の出力照合に直接関係する。ただし順位の具体則は現行文書と矛盾しており、そのまま採用できない。
- **Key Insight**: 入力文字列、トークン化、casefold、出力期待を区別して証拠を作る。CJKの連なりを文字単位として数える前提は置かない。**現行との衝突**: 学習の2026-11-17付34行・55–57行は同率を語のコードポイント昇順とするが、現在のCONCEPTS.md:49–51とREADME.md:23,30は「正規化後の初出順」を明示する。今回は後者を採用し、旧例 apple→zoo を転記しない。frontmatterにstatus: staleはないが、順位部分は現行契約によって置換済みである。
- **Severity**: medium

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 条件付き中一致。今回の要求はREADME追加と直接CLI実行でありCI成功要求ではないため、CI専用手順を新しい受入条件として持ち込まない。一方、独立検証・未実行を合格にしない・過去の成功を転用しないという判断原則は一致する。
- **Key Insight**: 2026-11-17付の教訓は「証拠の量ではなく対象」で充足を判定する（33–37行）。ファイルやコマンドの存在、他人の成功要約、過去のheadでの成功は今回の独立実行と等価でない。今回のBuilderのCLI原本と品質自身のCLI原本を区別し、phase1/3/4の過去の合格・stale記録を今回の実行証拠に付け替えない。CIの要件に対してはローカル実行を独立検証証跡と呼べないが、今回要求される直接CLI確認の証拠としては用途を限定して扱える。
- **Severity**: high

候補のうち git-state-test-discrimination-and-staged-baseline.md は状態回帰試験の新設・変異注入が今回の文書限定変更の範囲外、attachment-refusal-git-original-and-human-standard-reattachment.md は添付拒否が今回確認されていないため弱一致として除外した。後者の拒否回避やGit操作をこの調査で実行していない。

### Recommendations
- **製品差分を限定する**: README.md:9–15の既存実行例を保持し、同じコードブロックに `python -m wordfreq input.txt --min-count 3` を1行だけ追加する。既存の `--min-count 2 --top 1 --format json` を置換しない。README.md:35の `検証A: v1.12 の通しの確かめ（2026-11-22）` も保持する。コード・設定・依存・試験ファイル変更を計画に含めず、工程記録は別とする。
- **検証入力を先に固定する**: 後続の計画で同じUTF-8実ファイルのパスと全文を明記し、頻度が閾値3未満の語と閾値3に達する語を含める。同率の語は初出順と辞書順が異なるものを選び、casefold後の初出順を判別できるようにする。入力や期待結果は計画値と明記し、実行結果として作らない。
- **三形式を直接確認する**: Builderと品質は各自、固定入力に対し閾値3のtext/json/htmlを直接実行し、コマンド・入力原本・stdout・stderr・終了コード・実行担当・対象を読める文字原本で記録する。JSON/HTMLを手作業でtextから合成して代替しない。未実行の形式や品質未実行をpassedにしない。
- **現行契約で照合する**: README.md:23–24のとおりmin-countで除外し、頻度降順・同率は正規化後初出順、その後topを適用する。HTML総数はmin-count/top前の全出現数であって表示行の和ではない。今回の入力では除外語を含め、表示件数との混同を防ぐ。旧学習のコードポイント順や過去の試験件数を期待値に転記しない。
- **PMが読める形で渡す**: 工程文書にBuilder・品質それぞれの実入力と実CLI原本の相対pathを記載し、PMがread_fileで原本とREADMEを照合できる状態を完了条件にする。アーカイブのみ・別profileの保存先のみ・成功要約のみで配送完了としない。今回の文字証拠をブラウザ可読性や過去フェーズの全面受入の証明へ拡張しない。
- **計画と実行を分離する**: この調査はファイル読取りのみで製品コマンド未実行。GSD状態の判定や変更、git/kanban操作、検証コマンドの試行はしていない。後続PLANは未作成の検証ファイルを実行済み扱いせず、検証ファイルを指定するなら実在を確認してからBuilder・品質へ渡す。旧phase1/3/4の状態を今回の要求充足判定へ混ぜない。
