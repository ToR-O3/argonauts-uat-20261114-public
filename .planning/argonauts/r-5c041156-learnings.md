## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: r-5c041156 wordfreq HTML出力の承認済み仕様からGSD計画へ引き継ぐ学習調査。製品実装・検証実行・commit/push・Kanban操作は対象外。
- **Keywords Used**: wordfreq, stdlib-only Python CLI, HTML, pure formatter, Counter, casefold, stable first-seen ties, top, basename, total_count, escape, CR/CRLF, tokenizer, input-boundary, determinism, PYTHONHASHSEED, testing, verification, git-status, mutation-injection, staged-baseline, CI evidence, head, evidence-handoff, workflow, tooling-decisions, responsive table, browser/network/layout。
- **Files Scanned**: docs/solutions/ の全Markdown 4ファイル。発見した best-practices/ と workflow-issues/ を含む全木を、大文字小文字非区別の title/tags/module/problem_type 検索および条件リスト検索で事前抽出し、候補4件のfrontmatterを先頭30行で読み、関連度判定後に全文を読んだ。.gitkeepとディレクトリは件数から除外。pack指定なし、pack探索なし。
- **Relevant Matches**: 4ファイル（直接関連2件、証跡運用として隣接・条件付き関連2件）。
- **Grounding**: 先に CONCEPTS.md 全文を読んだ。現在仕様の対照は openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md と design.md。現コードは wordfreq/{aggregator,formatters,sources,tokenizer,__main__}.py、既存試験は tests/test_aggregator.py と tests/test_cli.py:152–189 を読み取った。GSDの状態判定は行っていない。
- **Critical Patterns**: docs/solutions/patterns/critical-patterns.md は今回の全木探索に存在しなかった。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 集計の順序、正規化とtokenizerの境界、入力不変、複数seedでの再実行が今回の全形式共通回帰に直結する。
- **Key Insight**: 語の定義・差替え境界・CJK粒度を混同しない。casefoldはトークン化後で維持する。単一seedの一致を決定論の証明にしない。FileSourceの入力バイト不変と、読取り後の改行正規化を別の契約として扱う。
- **Severity**: medium
- **Date / Current-spec Difference**: 2026-11-17の学習。本文Guidance 2はコードポイント昇順と安定sort元順への非依存を勧めるが、今回の承認済みFR-4・D-2は同数時を正規化語の初出順に明示置換し、design D-1はCounter挿入順を保持した頻度降順の安定sortを採る。CONCEPTS.md:45–47、wordfreq/aggregator.py:11–13、tests/test_aggregator.py:17–32 はまだ旧契約であり、過去学習より新仕様を優先する。今回の初出順依存は意図された契約であって、任意のset順への依存とは異なる。
- **Planning Input**: 初出順の情報をcount_wordsからtop_wordsまで失わず、sort後にtopを適用する。全形式でZoo/apple、Straße/STRASSE、top1、頻度優先を試験化し、各形式内で複数seedの出力一致を確かめる。読取り層のCR/CRLF→LF正規化（sources.py:19）は維持し、HTML表示対象の名前/直接formatter入力のCR/CRLF保持とは区別する。後者はHTML解析の改行正規化を含めてDOM textContentで照合する。旧学習の比較キーやハッシュ例をそのまま採用しない。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: HTMLをstdoutへ出す追加でも入力不変・作業ツリー不変の既存回帰を弱めてはならない。今回のHTML-4に直接関連する。
- **Key Insight**: 未追跡の基底は内容改変を隠し、温まったキャッシュやPYTHONDONTWRITEBYTECODEの継承は生成物を隠す。cold copy、条件付き.gitignoreコピー、git init後のgit add -A、環境変数除去、全未追跡パスを含むstatus比較を維持する。試験の判別力は「追跡内容改変」「無視規則欠落による生成物」の種ごとにscratchだけで証明する。
- **Severity**: medium
- **Date / Current-spec Difference**: 2026-11-17。tests/test_cli.py:152–180に上記対策が現存するため、現コードとの矛盾はない。ただし現試験のCLI実行は既定textのみ（171–174行）。承認済み仕様は全形式の入力不変と、HTMLを入力とは別ファイルへ保存する手順を必要とするため検証範囲を広げる必要がある。
- **Planning Input**: 既存試験の基底固定と隔離を削らずHTML経路を追加する。変異注入を行うなら実作業ツリーではなく使い捨てコピーに限定し、正常時成功と種ごとの期待assertion失敗を分けて記録する。今回の調査ではgit addも変異注入も行っていない。利用説明には同一パスへのリダイレクトがCLI起動前に入力を切り詰めることを明記する。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 隣接・条件付き関連。GSD計画の検証証跡の帰属と既存CI維持の扱いに有用だが、今回のHTML受入を新たなCI構築要求へ拡張してはならない。
- **Key Insight**: CI定義、人の過去head報告、ローカルpytest、現在の検証対象headへの独立したCI読取りは別種の証拠である。要求ステータスは必要な証拠種が揃うまでPending。検証対象headと報告commitを別に記録し、判定・報告直前に照合する。
- **Severity**: high
- **Date / Current-spec Difference**: 2026-11-17。過去事例ではCI欠如を人のworkflow追加で解消したが、今回HTML-4とdesign D-5はCI・依存の追加変更を禁止し、ローカル実ブラウザの画像・DOM/layout・networkを要求する。過去のCI追加手順や43 passedの値は今回へ転用しない。CONCEPTS.mdの「独立検証証跡」はCI実行結果そのものを要求する条件について用い、ローカルブラウザ証跡を無効化する意味に広げない。
- **Planning Input**: 既存pytest/CI回帰とHTML固有のローカルbrowser証跡を分離する。品質が実HTMLに対して自ら観測し、browser名/版・対象head・viewport・生成条件を記録する。静的CSS/JS不在の検査やpytestだけでlayout/通信0件/注入不実行を充足扱いにしない。手段不足は未検証gapとして人へ渡し、CI/依存追加で代替しない。

#### 4. 検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す
- **File**: docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md
- **Module**: 検証証拠の受け渡し（Argonauts カード添付・検証成果物の原本）
- **Problem Type**: workflow_issue
- **Relevance**: 隣接・条件付き関連。実HTML・画像・DOM/layout/networkの成果物を後工程へ渡す際に適用する。現在添付拒否があることを意味しない。
- **Key Insight**: 証拠の所在と原本同一性を保持し、添付フックの拒否を圧縮・リネーム等で迂回しない。拒否と後続解消を別記録にし、添付コピーとの一致は名前でなくバイト列/ハッシュで確かめる。秘密値や個人情報を証拠へ混ぜない。
- **Severity**: high
- **Date / Current-spec Difference**: 2026-11-17。学習のGit原本push・カードコメント・metadata訂正は後工程の権限と条件に従う手順であり、本調査のcommit/push/Kanban操作禁止を上書きしない。HTMLはbasenameのみでも語・名前を含むため、検証には無害な人工データを用い、共有前確認を案内する。
- **Planning Input**: phase資料から実HTML・画像・測定記録を辿れる原本パスを設計する。添付が必要な後工程で拒否された場合のみ、具体理由と原本パスを記録して人の標準添付へ回す。証拠を捏造せず、未取得は未取得と記す。

### Recommendations
- **優先して読む対象**: Builderは学習1・2および承認済みspecのFR-4/HTML-1〜4とdesign D-1〜5、品質は学習2・3とHTML-4の品質証跡条件、証拠受渡し担当は必要時に学習4を読む。旧学習とCONCEPTSの語昇順を現在仕様と誤認しないことが最優先。
- **逐次計画**: 同じ要求branchの共有ファイルを触るため並列化せず、各PLANは3 task以下とする。推奨順は (1) 全形式共通の初出順・casefold/top境界と旧期待/CONCEPTS/説明の同期、(2) 純粋HTML formatter・CLI配線・部品/CLI回帰、(3) 実ブラウザ受入と証跡/利用説明の確定。これは作業の分割案であり、GSD状態判定やPLAN検証を実行した結果ではない。
- **集計・表示境界**: 1回の集計でCounterを保持し、top前の全出現数の和とbasenameを選択済みpairsとは別引数でHTML formatterへ渡す。formatterはファイルを読まず、formatごとに再sortしない。text/jsonの署名・構造を維持する。
- **安全性と改行**: tokenizerの記号除去を安全性試験の代替にしない。formatterへ `& < > " '`、`&amp;`、タグ/イベント風文字列、空白・LF/CR/CRLFを直接渡す試験と、実在可能な悪意ある名前を使うCLI/browser試験の両方を用意する。単一escape境界、DOM文字列一致、CRの文字参照化等による保持、二重escapeなしを確認する。入力本文のユニバーサル改行動作は変更しない。
- **既存回帰の維持**: tests/test_aggregator.py の旧語昇順期待を明示変更として更新し、他の境界・CLIの終了値/stdout/stderr・空/記号のみ・Unicode・入力バイト不変は維持する。既存 tests/test_formatters.py、tests/test_cli.py、tests/test_sources.py、tests/test_sources_boundary.py、tests/test_tokenizer.py の回帰範囲も計画に残す。今回の学習調査では試験は実行していない。
- **実ブラウザ証跡**: 320px/375px mobile CSS viewportと1280pxで、明るい背景の順位/単語/回数3列、scope=col、空表、200文字連続語・長い日本語名・空白文字、連番/top前総数を実HTMLで確かめる。画像に加えてDOM textContent、ページ/表のoverflow、列の重なり、外部request 0、入力由来の要素/属性/script実行なしを記録する。ブラウザ名/版・viewport・対象head・実HTMLと証跡パスを残す。今回のcorpusにHTML固有のescape/CR保持/browser計測の既往学習はなく、これらの具体要件の根拠は現在の承認済みspec/designである。
- **コマンドと実行の責務**: 計画中は未作成の検証コマンドを試さない。Builderが検証ファイルを実際に作成し、品質は存在する検証ファイルから再実行する。GSDの状態/計画判定が必要な呼出元は公式CLIを使い、grepや独自スクリプトの推測で代用しない。この報告には未実在の検証コマンドや実行済みを装う数値を記載しない。
- **未解決範囲**: 本調査は読み取りと報告保存のみで、browser手段の可用性/版、製品動作、pytest/CI、layout/networkの受入は未検証。計画担当は既存の手段と証跡採取方法を確認して品質へ渡す。不足時は人へ明示し、CI・依存変更や仮の証拠で埋めない。実装後にHTML固有の安全性/改行/実browser証拠の知見を学習として追加するとよい。
