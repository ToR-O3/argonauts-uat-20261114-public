---
phase: quick-261128-jaf-wordfreq-min-length-option
plan: "01"
type: tdd
wave: 1
depends_on: []
files_modified:
  - wordfreq/__main__.py
  - tests/test_cli.py
  - tests/fixtures/min-length-default.html
  - .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-EVIDENCE.md
autonomous: true
requirements: [ML-FR-1, ML-FR-2, ML-FR-3, ML-FR-4]
estimate:
  tokens: 30000
  raw_tokens: 30000
  tasks: 3
  confidence: low
must_haves:
  truths:
    - "--min-length N は抽出・casefold後の語の長さでN未満だけを除き、Nちょうどと超過を全形式で残す。"
    - "長さ・頻度上下限の選択をtopより前に行い、同頻度の正規化後初出順を保つ。"
    - "HTML元総数は全入力の総出現数であり、長さ・頻度・topや全除外によって減らない。"
    - "省略と明示1は、全形式で変更前に固定したstdout・stderr・exitに一致する。"
    - "helpは選択肢、N文字未満の除外、既定1を説明し、README.mdは変わらない。"
    - "追加試験と既存全pytestの実測証拠があり、未知引数REDと比較境界の検出証拠を区別できる。"
  artifacts:
    - path: wordfreq/__main__.py
      provides: "既定1の引数と正規化後長さの共通選択条件、help"
    - path: tests/test_cli.py
      provides: "全形式の境界・casefold・併用・空結果・固定既定互換・help・判別試験"
    - path: tests/fixtures/min-length-default.html
      provides: "製品変更前に検証して固定する完全なHTML期待バイト列"
    - path: .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-EVIDENCE.md
      provides: "対象head、変更状態、実行環境、コマンド、実測結果と要求対応"
  key_links:
    - from: wordfreq/tokenizer.py
      to: wordfreq/__main__.py
      via: "iter_tokensのcasefold済み語をcount_wordsで集計したキーのlenを選択に使用"
    - from: wordfreq/__main__.py
      to: wordfreq/aggregator.py
      via: "全countsから元totalを保存し、挿入順を保ったselected_countsをtop_wordsへ渡す"
    - from: wordfreq/__main__.py
      to: wordfreq/formatters.py
      via: "全形式で同じpairsを使用し、HTMLへ選択前totalを渡す"
    - from: tests/test_cli.py
      to: tests/fixtures/min-length-default.html
      via: "省略・明示1の各stdoutを固定原本へ別々にバイト比較"
---

<objective>
wordfreq利用者が短い正規化済み語を --min-length N で除外でき、既定の利用を変えずに全形式へ同じ結果を得られるようにする。ML-FR-1..4をこの1本で扱う。計画作成者は製品を実装せず、commitしない。本書の実行も現在のworkspaceに限定し、branch変更、push、追加worktreeを行わない。
</objective>

<context>
@_bmad-output/initiative-r-1bae0a69/prd/prd-light-wordfreq-min-length.md
@openspec/changes/r-1bae0a69-light/proposal.md
@openspec/changes/r-1bae0a69-light/specs/wordfreq-cli/spec.md
@.planning/argonauts/r-1bae0a69-learnings.md
@.planning/STATE.md
@.planning/config.json
@wordfreq/__main__.py
@wordfreq/tokenizer.py
@wordfreq/aggregator.py
@wordfreq/formatters.py
@tests/test_cli.py
@pyproject.toml
</context>

<planning_basis>
Discovery Level 0: 既存argparse、Counter、run_cli_bytes、assert_output_bytes、CLIHTMLとpytestを再利用する内部変更であり、外部依存・調査・アーキテクチャ文書は不要。既存tests/test_cli.pyは実在し、検証コマンドの対象はこのファイルと既存testsである。以下の新しい試験名はBuilderが作成してから実行する。計画中は新規nodeidも製品pytestも実行していない。

公式CLIのstate.loadで設定を確認。estimate-calibrationはfactor=1、sample_count=0、confidence=low。graphify statusはdisabled。quickのIDにroadmap phaseはなく、assumption-delta scanはphase_unresolvedによるskipであり陰性の判定ではない。今回の追加はローカルCLIの数値選択のみで、外部API/SDK/service、DB/ORM/schemaの変更はない。plan:pre snapshotからkind=contributionかつinto=plannerのfragment.inline/configValuesのみ適用し、renderedやstep/gateの自動実行指示は使わない。API coverageとschema pushは対象変更なし、assumption-deltaは上記skip、securityはASVS L1/highを適用する。

無効Nの新たな受理範囲・拒否規則・固有エラー文言を作らない。argparseの既存int変換を利用し、正のNについて要求を満たす。README.md、依存設定、抽出・casefold、aggregator、formatters、CI、既存のOpenSpec原本は変更しない。学びの古い辞書順契約や過去の合格数を流用しない。
</planning_basis>

<tasks>

<task type="tracer" tdd="true">
  <name>Task 1: 固定既定互換を保護し、textの長さ選択をRED/GREENで接続する</name>
  <files>tests/test_cli.py, tests/fixtures/min-length-default.html, wordfreq/__main__.py</files>
  <behavior>
    - 製品変更前にtest_min_length_default_fixedの省略側を全形式で成功させる。入力名input.txt、入力a bb ccc bb、元総数4、全pairsはbb:2,a:1,ccc:1。textとjsonは固定literal、htmlは完全な固定fixture、stderr空、exit0。
    - test_min_length_tracerは同じ入力にN=2のtextでexit0、stderr空、stdoutが2\tbb\n1\tccc\nになることを要求する。
    - test_min_length_boundaryは全形式でaを除きbbとcccを残し、HTML元総数4を要求する。
  </behavior>
  <action>
最初にgit rev-parse HEADとgit status --shortを記録し、既存の全試験を実行して開始時の失敗を区別する。既定互換の試験とHTML固定fixtureを先に作る。fixtureは現在の未変更formattersの完全な文書を固定literalとして保存し、現在の実CLIの省略時出力に一致することを製品編集前に検証する。試験実行時にformatterを呼んで期待値を作らず、製品編集後にfixtureを再生成しない。default_fixedは省略と明示1を別パラメータとし、初回は省略側だけを実行する。

次にtextのtracerを1件だけ書いて実行し、未知の--min-lengthによるexit2のREDを保存する。このREDはCLI未配線の証拠であり比較境界の証拠ではない。build_parserへtype=int/default=1の引数だけを追加し、同じtracerを再実行してexit0だが短いaが残る意味的REDを保存する。その後はじめてselected_countsの既存条件にlen(word)がargs.min_length以上という条件を追加し、text tracerをGREENにする。count_wordsへの入力は間引かず、totalは全countsから先に求めたまま、元Counterを変えず挿入順を保つ。top_words、formatters、既存のmax-count条件の意味や既存変異試験が使うseamを不必要に変更しない。

全形式boundary試験を追加して実行する。実装で既に通る形式は追加カバレッジのGREENとして記録し、REDを捏造しない。明示1の既定互換もここで各固定期待値に別々に比較する。今後の追加挙動も1件の試験を先に書く→実行→必要な最小製品変更→再実行の順を守り、試験をまとめ書きしてから一括実装しない。証拠メモはTask 3で原本化する。
  </action>
  <verify>
    <automated>python3 -m pytest tests/test_cli.py -k 'min_length_default_fixed or min_length_tracer or min_length_boundary' -q</automated>
  </verify>
  <done>製品編集前の全形式固定既定値が確認済み。未配線RED、配線後の選択欠落RED、text GREENが別々に記録され、全形式のN未満/ちょうど/超と省略・明示1の固定互換が成功する。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: 正規化・合成・空結果・helpを拡張し境界の判別力を示す</name>
  <files>tests/test_cli.py, wordfreq/__main__.py</files>
  <behavior>
    - test_min_length_casefold: ß ss a、N=2は全形式でss:2のみ、HTML元総数3。
    - test_min_length_unicode: 日 日本 日本語 _ 12、N=2は日本,日本語,12の初出順で各1回、HTML元総数5。Unicode抽出・数字・下線の現行契約を保つ。
    - test_min_length_composition: a a a bb cc bb cc dddd、N=2/min-count=2/max-count=2/top=1は全形式でbb:2だけ、HTML元総数8。
    - test_min_length_tie_order: a zz aa zz aa、N=2/top=1はzz:2だけ、元総数5。辞書順へ戻す誤りを検出する。
    - test_min_length_empty: a bb、N=3は全形式で正常な空結果、text空バイト列、jsonは[]と改行1つ、HTMLは0データ行・既存空メッセージ・元総数2。
    - test_min_length_help: filenameなし--helpでexit0、stderr空。値指定付き選択肢、N文字未満を除く説明、既定1がstdoutにある。
    - test_min_length_discrimination: 独立したcold copyの対照はGREEN、長さ条件を無効化した変異と境界をstrictにした変異はboundary試験の期待値比較で失敗する。
  </behavior>
  <action>
Task 1に続いて上記各試験を一挙動ずつ先に追加・実行する。casefold、Unicode、合成、同頻度初出順、空結果は既存の共通経路で通ればカバレッジとして記録し、不要な製品変更でREDを演出しない。全形式でrun_cli_bytesとassert_output_bytesを使い、HTML空状態は既存HTMLDocumentの検査を再利用する。頻度上下限とtopの併用は期待pairsを固定し、長さの短い最頻語がtop枠を先に使わないことを確認する。helpの試験を先に実行して説明欠落のREDを記録してから、build_parserの新引数にN文字未満除外と既定1が分かるhelpとmetavarを追加してGREENにする。文言は意味の要求を満たし、無効Nに関する製品判断を足さない。

境界判別試験はpytestのtmp_path配下にwordfreqと必要なtest_cli.pyおよびtest_formatters.pyのみをcold copyする。追加worktreeやworkspace外の製品編集は行わない。tmp_pathは実行環境の管理scratch配下へ設定し、入力とコピー以外を変更しない。各コピーで実際の長さ条件seamに変更が1箇所当たったことをassertする。対照、長さ条件除去（N未満も残す）、比較の以上から超過への変更（Nちょうども落とす）を別々に実行する。子pytestはmin_length_boundaryのみを選び、自己再帰を防ぐ。対照exit0と正の実行件数、変異exit1、対象期待値のAssertionError、collection/syntax/importエラーなしをJUnitまたは同等の実測で確認する。単なる未知引数exit2、0件、collection失敗を検出成功に数えない。Task 1の初期REDとこの変異検出は別の証拠種別として保存する。
  </action>
  <verify>
    <automated>python3 -m pytest tests/test_cli.py -k min_length -q</automated>
  </verify>
  <done>全追加試験が成功。casefold後長さ、Unicode、初出順、合成、元総数、空状態、helpを全要求に照合できる。対照成功と2種の比較境界変異の実失敗を確認し、未知引数REDと区別している。</done>
</task>

<task type="auto">
  <name>Task 3: 全回帰と変更範囲を確認し、品質へ可読証拠を渡す</name>
  <files>.planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-EVIDENCE.md</files>
  <action>
既存の環境でpython3 --versionとpython3 -m pytest --versionを記録し、追加依存のinstallはしない。pytestが利用不可なら既存のプロジェクト用環境を調べて利用し、環境と正確な実行コマンドを記録する。利用可能な環境がなければ未実施のblockerとして親へ返し、合格としない。公式GSD判定にはランチャーを使う。

追加試験を実行後、python3 -m pytest tests -qで全既存試験を含めて実行する。開始時の既存失敗を除去したことにせず、実際の失敗・skip・件数・exitを明記する。git diff --check、git diff HEAD -- README.md、git diff --cached -- README.md、git status --shortで変更範囲を確認する。README差分があれば完了としない。他者変更を勝手に戻さず親へ報告する。

EVIDENCEへ実行環境、開始時headと最終検証時head、未commit差分状態、入力、引数、期待結果、実際のstdout/stderr/exit、pytest件数、TDD順序、対照/変異結果、ML-FRとML仕様の対応、README差分なしの実測をテキスト原本で残す。全出力が長ければ同じquickディレクトリのログへの相対参照と受入に必要な抜粋を残す。未実施を成功扱いせず、Builderによる実測と品質の独立実行とPM原本読取りを混同しない。品質は対象headとdirty状態を確認し、同じ実在試験ファイルのコマンドを自分で再実行する。過去フェーズの画像・ブラウザ台帳や大型検証器を今回へ自動的に追加しない。
  </action>
  <verify>
    <automated>python3 -m pytest tests -q</automated>
  </verify>
  <done>追加試験と既存全回帰が実行済みで失敗なし。README.mdのHEAD・index・worktree差分なしを確認。PM可読の証拠原本に対象状態・コマンド・実測件数・exit・要求対応・未確認事項があり、独立品質の未実施を明示する。</done>
</task>

</tasks>

<threat_model>
ASVS level 1、blocking threshold high。既存CLIの主要境界に限定する。

## Trust Boundaries
| Boundary | Description |
|---|---|
| argv → argparse/main | 利用者のNは既存int変換で受ける。shell評価や新しい無効値契約を導入しない。 |
| 入力ファイル → 正規化・集計 | 任意のUTF-8本文を既存FileSource/iter_tokensで読む。入力や元Counterは変更しない。 |
| 入力名・語 → HTML/stdout | 動的文字列は既存format_htmlのescapeとbasename制限を通る。 |
| 試験 → cold copy | 変異は管理scratchのコピーだけに適用し、本体へ戻さない。 |

## STRIDE Threat Register
| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|---|---|---|---|---|---|
| T-261128-jaf-01 | Tampering | wordfreq/__main__.py | medium | mitigate | 元countsとtotalを維持し、非破壊の選択後にtopを行う。Task 1/2の全形式・元総数検査で検証。 |
| T-261128-jaf-02 | Information disclosure | wordfreq/formatters.py | medium | mitigate | formatter・basename・escapeを変更せず、既存のhostile filename/privacy全回帰をTask 3で実行。 |
| T-261128-jaf-03 | Denial of service | wordfreq/__main__.py | low | accept | ローカル単発CLIの既存全文集計特性は今回拡張しない。長さ検査は既に集計済みの各キーに適用する。入力上限の新契約は範囲外。 |
| T-261128-jaf-04 | Tampering | tests/test_cli.py | medium | mitigate | Task 2の変異をtmp_pathのcold copyへ限定し、対照と失敗種別を検証する。 |
| T-261128-jaf-SC | Tampering | pyproject.toml | high | mitigate | 依存追加・install・依存設定変更を行わない。Task 3のdiff確認で新たな供給網経路がないことを確認。 |
</threat_model>

<verification>
Builder・品質はrepo rootから、作成済みのtests/test_cli.pyを読み、上記コマンドを実行する。新規nodeidを計画中に試さない。全形式で「N未満/ちょうど/超」「casefold」「併用と初出順」「全除外とtotal」「変更前固定期待値に対する省略・明示1」「help」を確認する。全pytest、git diff --check、README差分確認を完了条件に含む。新規試験のcollectionが0件、環境不備、未実施、無関係の失敗を成功へ置換しない。
</verification>

## Multi-Source Coverage Audit
| SOURCE | ID | Feature/Requirement | Task | Status |
|---|---|---|---|---|
| GOAL | quick description | 短い正規化済み語の選択と既定互換 | 1–3 | COVERED |
| REQ | ML-FR-1 / ML-1 | N境界、casefold、全形式 | 1,2 | COVERED |
| REQ | ML-FR-2 / ML-2 | 固定既定値、頻度・top、初出順、元総数、空結果 | 1,2 | COVERED |
| REQ | ML-FR-3 / ML-3 | help説明、README変更なし | 2,3 | COVERED |
| REQ | ML-FR-4 / ML-3 | 追加・全既存pytest、文字証拠 | 1–3 | COVERED |
| RESEARCH | learnings | 古い辞書順を採らず、未知引数REDと比較誤りを区別、可読証拠 | 1–3 | COVERED |
| CONTEXT | user constraints | test-first小刻み、依存なし、無効N契約なし、workspace限定 | 1–3 | COVERED |

quickのため新たなROADMAP phase/REQ番号やCONTEXT D番号を捏造しない。別RESEARCH/CONTEXTは支給されていないため上表は指定PRD・OpenSpec・学び・直接制約に対応する。順序は1→2→3、全て同じCLI試験を共有するため並列実装しない。checkpointや追加worktreeは不要。

<success_criteria>
ML-FR-1..4およびOpenSpec ML-1..3を満たし、全形式の固定期待値、境界、合成、空結果、helpと全回帰が成功する。READMEと範囲外ファイルを変更せず、実測に基づく証拠原本を残す。製品の完成と独立品質・PMの受入は別の状態として報告する。
</success_criteria>

<output>
実行結果は .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-SUMMARY.md にまとめ、.planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-EVIDENCE.md を参照する。計画作成工程では本PLANのみ作成し、製品実装・試験実行・commitを行わない。
</output>
