## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: r-50053edc wordfreq HTML出力 Phase3のgaps追加計画。G1はlive finalize accepted後も全view・derivedにpending/空reviewed_imagesが残る問題。G2はCIの5 failed/279 passed（ISO-8859-15 locale依存2件、shallow git baseline欠落のscope3件）。tests/toolsのみの修正計画に学習を供給する。
- **Search Root**: `/home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_db3e2cfc/docs/solutions` のみ。CE packs指定なし。
- **Grounding**: 検索前に直下の`CONCEPTS.md`を全文読了。検証対象head、独立検証証跡、要求ステータス、試験の判別力、原本同一性、決定論的順位の現行定義を使用。
- **Keywords Used**: evidence, ledger, manifest, derived, pending, finalize, reviewed_images, viewed_at, sha256, git, baseline, staged, dirty, untracked, scope, actor, approved snapshot, shallow, ISO-8859, locale, encoding, filesystem, stdout, byte-level, rawRange, network, canary, head, independent verification, 検証, 証拠, 境界, workflow, test。
- **Files Scanned**: 4 total learning markdown files。workflow-issues 2件、best-practices 2件。`.gitkeep`とディレクトリは除外。4件すべてについて事前検索→先頭30行→関連度判定→残り全文の順に確認した。
- **Relevant Matches**: 4 files（強一致2件、隣接・部分一致2件）。
- **Search Method**: 実在ディレクトリを列挙し、複数領域にまたがるため全rootを対象にtitle/tags/module/problem_type/symptoms/root_causeとapplies_when相当の箇条書きを大文字小文字無視で並列検索。さらにG1/G2固有語の全文検索へ拡大した。今回読んだsolution文書のみを根拠とし、既存の計画向け報告は流用していない。
- **No Direct Match**: ledgerの全view伝播、ISO-8859-15、shallow exact baseline、actor、rawRange/network canaryを直接解決する学習は見つからなかった。
- **Evidence Boundary**: CI件数・現在症状は今回のwork-context由来で、今回の独立実測ではない。コード調査、テスト実行、GSD判定は行っていない。保存先には旧計画向け報告が存在したため、全文を読み取り後、今回のgap調査結果に置換した。

Critical Patterns: `docs/solutions/patterns/critical-patterns.md`は存在しない。

### Relevant Learnings

#### 1. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`（31–44行）
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 強一致。G2のscope/baseline、dirty/untracked漏れに関係する。ただしshallow checkoutのexact baseline確保手順そのものの記事ではない。
- **Key Insight**: 未追跡基底のgit statusは内容変更を隠して偽合格する。試験用scratch repoでは`git init`→`git add -A`→before取得の順を守る。追跡内容改変と予期しない未追跡生成物を別々のscratchで注入し、期待したassertionで落ちることを示す。cold copyと環境分離で継承キャッシュや環境による偽合格も断つ。
- **Severity**: medium
- **Planning Constraint**: staged baselineは試験内部の比較基底であり、実scope判定の承認済みexact baselineの代替ではない。欠落した実参照をHEADや任意snapshotへ置換して通す根拠にしない。正常系合格だけを判別力と呼ばず、dirty/untracked・actorもそれぞれ対象の失敗を捕捉する。

#### 2. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`（22–37行）
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 強一致。G2のCI失敗解消とfresh qualityの証拠境界に一致する。G1にも、一つのaccepted記録だけで要求充足を宣言しない原則が参考になる。
- **Key Insight**: workflowの存在、歴史的headの人の成功報告、ローカル成功は、現在の検証対象headの独立CI証跡を代替しない。必要証拠が欠ける間は要求Pendingを維持し、判定直前に対象headを再解決・照合する。検証対象headと報告commitは区別する。
- **Severity**: high
- **Planning Constraint**: Builderの成功要約や過去CI件数を品質合格として継承しない。品質はfreshな独立生成と対象headのCI証拠確認を担当する。G1の不整合pendingを修正することと、証拠不足の要求をPendingに保つことは別問題。全出力の一致を確認せずCompleteへ進めない。

#### 3. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`（34–36行）
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 部分一致。G2の環境差を含む出力検証に、単一環境の成功を不変性の証拠にしない原則とバイト列での境界確認が参考になる。ISO-8859-15やfilesystem/stdout encodingの直接解法はない。
- **Key Insight**: 環境を変えた実CLI再実行と出力一致を証拠にし、読み取り前後のバイト不変・改行方針を明示する。変換後の見た目だけでI/O契約を判定しない。
- **Severity**: medium
- **Date / Conflict**: 文書は2026-11-17時点の同率「語コードポイント昇順」を推奨するが、今回読んだ`CONCEPTS.md`45–47行は現行r-50053edc契約を「頻度降順・同率は正規化後の初出順」と定義し、旧契約を明示的に置換している。古いソートキーは採用しない。複数seedでの再実行という証明手順のみ持ち越す。
- **Planning Constraint**: locale依存の試験設定・入出力アサーションをtests/tools内で扱い、byte-levelの期待値を明示する。locale導入、依存・CI設定変更、skip回避の根拠にしない。

#### 4. 検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す
- **File**: `docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md`（31–35行）
- **Module**: 検証証拠の受け渡し（Argonauts カード添付・検証成果物の原本）
- **Problem Type**: workflow_issue
- **Relevance**: 隣接一致。G1画像証拠の原本同一性・記録の帰属に参考になる。添付拒否処理自体は対象外で、ledger/manifest/derived実装の記事ではない。
- **Key Insight**: 表示名の類似ではなくバイト列とsha256で原本同一性を確認する。失敗時点の履歴と解消後の事実を分けて保持し、参照パスの誤りを放置しない。
- **Severity**: high
- **Planning Constraint**: validated ledgerの画像path/sha256/viewed_atを全view・derivedへ一貫反映する今回の要求に、原本同一性原則を適用する。viewed_atやledger構造の具体契約は今回要件由来で、この記事の既存解法ではない。過去履歴や証拠を手で合格形へ修正しない。

### Recommendations
- **着手前の参照**: G2実装者は第1文書、品質担当は第2文書を先に読む。第3文書は古い順位契約を除外し、第4文書は原本同一性の原則だけを適用する。
- **G1の順序と失敗条件（今回要件からの適用）**: ledger検証を先に行い、画像path/sha256/viewed_atを全viewとmanifest等のderivedへ共通に反映し、finalize最終段で全対象との一致をfail-closedに確かめる。acceptedだけ・単一viewだけの合格では足りない。pending残存、空reviewed_images、欠落・不一致をそれぞれ検出する試験を計画する。証拠手修正は禁止し、fresh qualityで独立再生成する。
- **G2の基底境界**: shallow環境の試験fixtureに必要な基底を明示する。scratchのstagingは試験内部に限る。承認済みexact baselineの実参照欠落は、別基底fallbackやskipで成功させずfail-closedを維持する。tests外pytest収集のdirty漏れとactor profile回帰は、同箇所のscope境界に限定して修正する。互いの検出を代用しない。
- **G2のencoding境界**: filesystemとstdoutのencodingを同一視しない試験にし、localeの有無に左右されないbyte-levelの入力生成・出力比較を明示する。具体的修正方式は現行tests/toolsの調査後に決める。今回のcorpusにISO-8859-15依存2件の既知修正方式はない。
- **固定制約**: tests/tools以外の修正、CI/依存変更、skip追加、実scope参照不足を隠すfallback、証拠の手修正は行わない。これらは今回の依頼の制約であり、過去学習で緩めない。
- **検証責任**: 計画段階では未作成の検証コマンドを試さない。PLANの検証コマンドはBuilder・品質が実在する検証ファイルを根拠に実行する。品質は最新の検証対象headへの独立再生成・独立CI読み取りを行う。今回の調査では検証実行・GSD判定を行っていない。
- **一致なしの扱い**: rawRange/network canary、actor固有回帰、ledger全view伝播、shallow exact baseline、ISO-8859-15の直接的学習は確認できなかった。過去解法を創作せず現行ファイル調査へ引き継ぎ、今回解決後に原因・最小修正・負例を耐久的学習として残す価値がある。
