## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み r-774f3cd6 の `pyproject.toml` `[project].description` 新設をGSDで計画する。固定完成値は `argonauts-uat public (UAT)`。基準は `b34cba0d008923e7f5267ce52d5403492ea53925`。description欠落確認後の1行新設のみを製品変更とし、他項目・他製品・依存は不変、閉じたphaseは変更せず新規phaseを追加する（以上は依頼者指定の計画前提）。
- **Keywords Used**: description, pyproject.toml, tomllib, SHA-256, 生バイト, 構造, 試験先行, 固定値, baseline, commit, phase, workflow, tooling, git, test, 検証, evidence。大文字小文字を無視したtitle/tags/module/problem_type検索と、本文の関連語検索を並列実施。
- **Files Scanned**: 5 learning Markdown files。`docs/solutions/` 全体の検索対象となる学習本文5件を事前検索し、5件のfrontmatterを確認、関連ありと判定した4件を全文読了。`.gitkeep` とディレクトリ自体は件数に含めない。
- **Relevant Matches**: 4 files（直接関連2件、限定適用の隣接学習2件）。添付拒否の記事は今回のdescription計画には弱い関連のため採用しない。
- **Search Scope**: 検索rootは `docs/solutions/` のみ。実在カテゴリは `best-practices/` と `workflow-issues/`。用語の grounding としてrepo rootの `CONCEPTS.md` を読了。追加packなし。
- **Evidence Boundary**: 本書は学習調査の原本であり製品検証結果ではない。基準commitの内容、現在のdescription欠落、GSDの現在phase状態は本調査では検証していない。製品編集、検証スクリプト作成・実行、GSD状態変更、Kanban操作、commit/pushは行っていない。

`docs/solutions/patterns/critical-patterns.md` は検索rootのファイル探索で存在せず。

### Relevant Learnings

#### 1. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 「descriptionだけ変える」「他項目・他製品の生バイトは変えない」という主張を担う検証の判別力に直接関係する。元記事の対象はGit状態比較だが、不変性試験を意図した破壊で確かめる原則は今回にも適用できる。
- **Key Insight**: 合格1回では検出能力は証明されない。失敗種別ごとに隔離したscratchコピーを使い、期待したアサーションで失敗することを確認する（本文37–44行）。未追跡ファイルの内容変更はGit statusでは不可視になり得る。Git状態比較を使う一時repoなら、基底をステージしてから比較する。これはscratch内限定の設計であり、本調査workspaceへの `git add -A` の指示ではない。
- **Severity**: medium

#### 2. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 基準commit、実装後の検証対象head、証拠を運ぶ報告commitの区別に直接関連する。新規検証ファイルの存在だけを、description新設や不変性の検証成功と扱わないための制約になる。
- **Key Insight**: 設定・スクリプトの存在、過去headの報告、ローカル成功、現在headの独立検証は別種の証拠。報告直前に対象headを再確認し、基準commit・検証対象head・報告commitを別欄で残す（本文22–37行）。CI成功が要求される場合だけ、現在の対象headに対する独立CI証跡を必要とする。この記事を根拠に今回の依頼へCI要求を追加しない。
- **Severity**: high

#### 3. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 限定適用。今回に使うのは「構造・意味の一致」と「生バイト不変・改行方針」を分けて固定するという読み取り層の知見。トークナイザや順位付けの実装を今回の変更対象にはしない。
- **Key Insight**: 読み取り専用性は宣言ではなくread前後の `read_bytes()` 一致で固定する。テキスト読込みにはCRLF/CRをLFへ正規化する経路があるため、パース後一致だけでは生バイト不変を主張できない（本文36–42行）。tomllibでの構造比較と、元バイト列との比較を別々の検証観点として計画する。
- **Severity**: medium

**現行用語との衝突に注意**: この記事は2026-11-17の旧契約で、同率を「語のコードポイント昇順」としている。一方、今回読んだ `CONCEPTS.md` の「決定論的順位」は r-50053edc による「正規化後の初出順」への意図的な置換を明記する。frontmatterに `status: stale` はないが、順位付けの旧指示は現行契約として転用しない。本書が採用するのは読み取り・バイト不変の原則のみで、現行製品コードの実測を主張しない。

#### 4. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 限定適用。工程管理領域の検証スクリプトとcommit/SHA-256証拠をBuilder・品質・受取担当が読むための成果物配置と引継ぎに有用。今回、大型画像や添付操作を追加する必要はない。
- **Key Insight**: 保存済み、配送済み、受取側で原本照合済みは別の状態。相対path・対象head・実施者とSHA一覧を一緒に残す。SHA一致は原本同一性の証拠であり、製品の正しさや検証合格自体の証拠ではない（本文33–45行）。read_fileで開けるテキスト原本を使い、別profileの絶対pathや要約だけで引継ぎ完了としない。
- **Severity**: high

### Recommendations
- **新規phaseの計画入力**: 既存の閉じたphaseを変更しないという依頼者決定を保持する。phase状態や番号・追加可否は計画担当がGSD公式CLIで判定する。本調査はその判定を代行せず、未作成の検証コマンドも試さない。
- **試験先行の順序**: Builderが工程管理領域に実在する検証ファイルを先に作成し、description欠落で期待した検証失敗を確認した後、承認された1行を新設して成功を確認する。品質もその実在ファイルから独立実行する。固定値は `argonauts-uat public (UAT)` を完全一致で扱い、別表記へ補正しない。これは依頼者要件に、学習1の「意図した失敗を本当に検出する」という原則を適用した計画案である。
- **構造比較とバイト比較を分離**: stdlib `tomllib` で基準と変更後の構造を読み、基準で `[project].description` が存在しないこと、変更後に固定文字列が存在すること、変更後から当該キーだけを除いた全体構造が基準と一致することを検証対象にする。加えて変更後から許可した追加1行だけを取り除いた生バイト列が基準と一致することを別途検証し、改行・空白・コメント・並び替えの副作用を見逃さない。tomllib自体を推奨する既存学習は見つからず、ここでの選択は依頼者指定に由来する。
- **判別力を種別ごとに計画**: description欠落、固定値違い、他キーの改変、意味が等価な改行/空白だけの変更、他製品ファイルの変更をそれぞれ隔離scratchで扱う候補にする。各種を狙った検証箇所で失敗させ、無変異ケースの成功と区別する。正しいdescription追加によって成功に転じることも必要。実workspaceや製品に破壊変異を入れない。
- **不変性の範囲を明記**: 製品変更は `pyproject.toml` の当該1行のみ。工程管理領域の新規検証ファイル・証拠・計画文書は製品差分とは分けて列挙し、他製品・依存の不変性を検証する際の比較対象を事前定義する。Git statusのパス表示だけで内容一致を主張せず、基準commitに帰属する内容比較を用いる。
- **証拠原本を設計**: 基準 `b34cba0d008923e7f5267ce52d5403492ea53925`、検証対象head、報告commit（存在する場合）、実行した検証ファイルとコマンド、終了コード、期待した失敗/成功、対象path、SHA-256の対象と計算実施者を区別して記録する。ハッシュ一致だけで構造・値の正しさを充足したと扱わない。今回の調査ではcommit生成やSHA計算は実施していない。
- **着手前の読む順序**: Builder・品質は学習1のGuidance、学習2の証拠種別/head区別を優先し、生バイト検証には学習3の読み取り層の段落、原本引継ぎには学習4の三段階を参照する。過去の順位付け契約、既存CI要件、大型画像受渡しの手順を今回へ拡張しない。

**調査上の限界**: description新設、tomllib、GSDのphase追加、工程管理領域へ検証スクリプトを置く方式そのものを直接扱う既存学習は見つからない。これらは依頼者指定の前提として扱い、上の周辺学習で検証の穴と証拠帰属の誤りを防ぐ。実装・品質確認後、構造一致と最小バイト差分の両立方法に新しい再利用可能な知見があれば、その時点で学習化を検討できる。
