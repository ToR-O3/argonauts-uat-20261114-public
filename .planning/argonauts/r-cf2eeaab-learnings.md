## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み r-cf2eeaab の GSD 計画への学習入力。`pyproject.toml` の `[project].description` を新規追加し、値を厳密に `argonauts-uat public (UAT)` とする metadata-only 変更。既存項目と他の製品ファイルを変えない。
- **Keywords Used**: pyproject, tomllib, metadata-only, description, byte preservation, バイト不変, 改行, RED/GREEN, mutation-injection, test-discrimination, staged-baseline, workflow, verification, head-resolution, 計画, 差分。
- **Files Scanned**: `docs/solutions` 内の Markdown 全5ファイルを内容検索し、候補5ファイルの frontmatter を確認。関連3ファイルを全文読取り。
- **Relevant Matches**: 3ファイル（直接一致する TOML メタデータ変更の事例ではなく、試験・バイト保全・証拠帰属の横断的教訓）。
- **検索範囲**: `docs/solutions` のみ。事前の用語確認としてルート `CONCEPTS.md` を読取り。外部 pack は指定なし。
- **調査上の限界**: 製品コード・既存 PLAN・GSD 状態は調査対象外であり、現状の実装・要求充足・検証成功は判定していない。起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と完成値は依頼からの前提であり、本調査で実測した値ではない。

`docs/solutions/patterns/critical-patterns.md` は検索結果に存在しない。

### Relevant Learnings

#### 1. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 今回の「既存項目と他製品不変」「製品差分の限定」は、単に正しい description を読む試験では証明できない。状態比較や差分検査自体の判別力が必要。
- **Key Insight**: 文書35–44行の教訓は、正常時の合格に加え、検出すべき失敗の種ごとに隔離した scratch コピーで変異を入れ、期待するアサーションで失敗することを確認するというもの。未追跡ファイルの内容変更は `git status` のパス一覧だけでは見えず、偽合格になった実例がある。一時 Git リポジトリの状態比較を採用する場合だけ、scratch 内の基底をステージしてから比較する。
- **Severity**: medium
- **計画への適用**: まず検証ファイルを工程文書内へ実体として作成し、description 欠落の基底に対する RED と、追加後の GREEN を同じ検証で記録する。そのうえで、値の誤り・既存項目の改変・他製品ファイルの変更・許可しないバイト差分を個別に検出する設計とする。変異注入は scratch のみで行い、実作業ツリーへ一時的な製品改変を入れない。scratch のステージ操作を本作業ツリーへの `git add -A` 指示として転用しない。

#### 2. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 今回に直接持ち込むのは、読取り・書換えにおけるバイト不変と改行方針を別の検証対象にする教訓。トークナイザや出力順位の変更は今回の対象ではない。
- **Key Insight**: 文書36・42行は、読み取り専用性は宣言でなく `read_bytes()` 等によるバイト比較で固定すべきこと、テキストの改行正規化と原本のバイト保全は別問題であることを述べる。TOML の解析結果が同じでも、コメント・空白・改行まで不変とはいえない。
- **Severity**: medium
- **計画への適用**: 標準 `tomllib` による意味検査と、生バイトによる追加箇所以外の不変検査を分ける。依頼の制約を踏まえ、TOML 全体の再シリアライズや整形は避ける。検証では description の厳密値だけでなく、その項目を除いた解析結果の同一性と、許可した追加以外の生バイト差分がないことを独立に扱う。
- **現行用語との衝突**: この記事は2026-11-17の旧契約として同率時のコードポイント順を推奨するが、先に読んだ `CONCEPTS.md` の「決定論的順位」は現行契約を初出順として明記している。旧順位指針は採用しない。今回必要なのはバイト・改行保全の教訓のみである。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 起点 SHA に対する製品差分と、実装・品質検証が対象とした head の混同を防ぐ。計画書や検証ファイルの存在だけを、検証の実行成功として扱わないための工程上の教訓。
- **Key Insight**: 文書33–37行では証拠の種類を要求と対応させ、判定・報告直前に検証対象headを再解決する。検証対象headと報告commitは別物として残す。ローカル実行の成功は CI 実行結果そのものの証拠ではない。
- **Severity**: high
- **計画への適用**: Builder・品質は実在する検証ファイルを実行し、対象head・比較起点・実行コマンド・終了結果・RED の失敗理由・GREEN の結果を区別して記録する。比較起点は依頼の `c572613dc626160db2eb3bf4a41c95fc8283b828` に固定し、検証対象headは実行時と報告直前に照合する。CI 要求が別途存在する場合に限って独立 CI 証跡を追加し、この学習を理由に CI 変更を今回の範囲へ新設しない。

### Recommendations
1. **検証ファイル作成 → RED → 最小編集 → GREEN → 品質による独立再実行の順に計画する。** 計画段階で未作成の検証コマンドを試さない。PLAN の検証コマンドは、Builder・品質が実在する工程文書内の検証ファイルを実行する形にする。本調査では検証ファイルを作成・実行していない。
2. **意味・バイト・製品差分の3つを別々に確かめる。** 意味は標準 `tomllib` で `[project].description == "argonauts-uat public (UAT)"` および既存項目不変、バイトは承認した新規追加以外の保存、製品差分は指定起点から `pyproject.toml` の承認箇所以外に製品変更がないこと。工程文書の追加を製品変更と混同せず、許容する工程文書と許容しない製品差分を計画で明示する。これは依頼の制約と学習を組み合わせた適用案であり、既存の TOML 専用手順が見つかったという意味ではない。
3. **RED の理由を検査する。** import 失敗、ファイル不在、TOML 構文破損など試験設備の失敗を、description 欠落を捉えた RED として記録しない。正常対照が通ることと、各種の違反が対応するチェックで落ちることを切り分ける。
4. **起点と証拠帰属を分ける。** 指定起点は差分比較の基準、検証対象headは試験結果の対象、報告commitは記録の配送先である。計画中はファイル読取りと必要な公式 GSD CLI で状態確認し、学習調査だけで GSD の完了・要求充足を主張しない。
5. **Builder・品質の優先読書**は上記1の全文と上記2の Guidance 4、証拠引継ぎ前には上記3の Guidance。今回の製品差分を増やす目的で既存テストやランタイムコードを改変しない。

### 非採用の候補と不足
- `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md` と `docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md` は frontmatter を確認したが、主題は添付経路・受取側の展開能力・添付拒否であり、今回のメタデータ追加計画への直接の適用条件がないため採用しない。
- `pyproject`、`tomllib`、`description`、metadata-only の直接事例は、指定検索範囲の内容検索では見つからなかった。TOML 専用の既知手順として断定しない。
- 今回の完了後に、意味一致とバイト保存を両立させる metadata-only 変更の検証が実証された場合は、既存学習を補う候補になる。本調査では学習追加や他ファイル変更は行わない。
