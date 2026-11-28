# Independent rubric walker / input reconciliation

## Verdict

**CONDITIONAL PASS（discussion用途）**：PRD原本の確定要求と既存CLIの主要な分岐点は保持され、機械検査も合格したが、Unicode比較の接続点に曖昧さがあり、PM経由で製品未決を解消するまでは実装・期待値確定の承認には使えない。

Critical / Highの新規設計欠陥は認定しない。Mediumの改善事項M-1は下記。製品判断待ちは既知のOQとして別記し、設計欠陥と重複計上しない。

## Scope / evidence / independence

- 対象：`../architecture.md`（feature / discussion / pipes-and-filters）。設計・memlog・既存実装は変更しない。
- 最初に公式 `bmad-architecture/references/reviewer-gate.md` を全文読了し、good-spine checklistの全観点を適用した。
- 入力を全文確認：`../../prd/prd-wordfreq-exclude.md`、`../../brief/brief-wordfreq-exclude.md`、それぞれの`.memlog.md`。
- brownfieldを全文確認：リポジトリの `wordfreq/__main__.py`、`sources.py`、`tokenizer.py`、`aggregator.py`、`formatters.py`、`__init__.py`。補助根拠として `README.md`、`tests/test_cli.py`、`pyproject.toml` も読了。
- 他のarchitectureレビュー本文は参照せず、この独立文脈で照合・判定した。本報告はrubric walker＋指定入力reconciliationの担当分であり、他のconfigured lensの代替やgate全体完了の認定ではない。
- 依頼原文はbrief memlog:9とPRD memlog:9に保存された記録を突合した。別の外部依頼原本を取得したとは主張しない。
- 親spineは指定入力にない。入力群に継承ADの提示もないため、継承整合の認定範囲は「提示された継承制約なし」に限定する。initiative本文のRequirementsや承認を推定しない。
- git / Kanban操作、インラインコード実行、製品仕様の決定、新機能・回帰試験の実行は行っていない。既存CLI試験にはgit操作とchmodを含むため、試験ファイルを読んだことを全件合格と扱わない。

## Deterministic gate

実行コマンド（既存の公式script、インラインコードなし）：

```sh
uv run /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/skills/bmad-architecture/scripts/lint_spine.py --workspace /home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_03a4d550/_bmad-output/initiative-r-6442a149/architecture
```

実出力：`ok: true`、`spine: architecture.md`、`total_findings: 0`、`by_severity: {}`、`findings: []`。終了コード0。placeholder、AD ID、Binds/Prevents/Rule、Stack table versionの機械検査に指摘なし。これは未決事項解消や実装の正しさを証明しない。

## Findings

### M-1 — Unicode未決に対して、フィルタが受け取る本文トークンの情報量が曖昧

- **Severity:** Medium（discussion提出の阻害ではない。OQ-1確定後・実装分割前に再確認）。
- **Location:** architecture:34、40–43、51、57、61、79。PRD:66–68、141。`wordfreq/tokenizer.py:14–18`。
- **Evidence:** 図は「Existing body tokenization → Pre-count exclusion」、seedは既存tokenizerを根拠にする。既存の `iter_tokens` はcasefold済みトークンだけを返す。一方、本文は新除外比較についてlower / casefoldを未決とし、特定の関数シグネチャも拘束しない。
- **Risk:** PM判断がcasefoldと区別のある比較を要求した場合、既存 `iter_tokens` の出力だけでは元の `Straße` / `STRASSE` の差を復元できない。入力側とフィルタ側が独立実装されると、「既存関数の出力をそのまま使える」という解釈と「比較に必要な元トークン情報を残す」という解釈に分かれ得る。現設計は明示的にcasefold採用を決定していないため、確定矛盾ではなく接続契約の曖昧さとして扱う。
- **Disposition:** **discuss → PM経由でOQ-1の回答を取得し、設計担当がその回答に必要な比較境界を明示する。** 現段階でlower/casefoldのどちらも推奨決定しない。OQ-1解消を待たず既存casefold済み出力だけに固定した実装契約を配布しない。
- **Acceptance:** OQ-1の合意例が、本文の未指定互換性を保ったまま、合意したフィルタ入力から判定可能であること。仕様に応じて既存の図で足りるか、抽出と正規化を区別すべきかを設計担当が確認する。
- **Autofix:** なし。本担当は設計編集禁止であり、比較の製品判断も行わない。

## Good-spine checklist — 全観点

| 公式観点 | 判定 | 根拠・境界 |
| --- | --- | --- |
| 一段下の本当の分岐点を固定し、取りこぼさない | 条件付き適合 | AD-1が集計前除外・全形式共通・総数の時点・I/O所有者を固定。AD-2が未指定経路・安定順位・重複不変性を固定。比較入力だけM-1。 |
| 各ADのRuleが強制可能で、Preventsを実際に防ぐ | 適合、M-1留保 | 下記AD別検証参照。構造・結果・I/O有無を試験やコードレビューで判定できる。 |
| Deferredに独立実装を分岐させる未決を放置しない | 条件付き適合 | 具体型・関数配置は非拘束でもADで収束可能。製品未決は自由裁量ではなく、該当仕様・期待値確定前の解消を要求（architecture:79）。OQを任意の実装既定値にしてはならない。 |
| named techがverified-current | 新規選定なし／適用不要 | Stack/versionの新規指定なし（architecture:63）。Counter、casefold、CLIは現行コード由来の観察で、ライブラリの最新採用を主張していない。`pyproject.toml`もruntime依存なし。今回webで技術の最新版を確認したとは主張しない。 |
| brownfieldをratifyし、矛盾しない | 適合 | CLI合成、入力例外のCLI終了判断、純粋集計・formatter、安定ソート、HTML総数時点が一致。新オプションの存在は主張せず、現行にないと明記。 |
| ticket / driving inputの全要求を網羅 | 適合 | FR-1〜FR-6・RULE-1〜RULE-2を下記表で照合。要求の詳細はPRDへ直接委譲しており、設計が試験期待値を全再掲しないことは欠落としない。 |
| 親spineのADを弱めない・矛盾しない | 適用対象未提示 | 親spine・継承ADが入力にない。未提示の親に対する完全整合性は認定しない。後から提示された場合は再照合が必要。 |
| 当該高度が所有する全次元を決定／延期／OQ化 | 適合 | 機能境界、依存方向、データ・状態、CLI公開面、互換性、異常系、説明・試験、運用・環境を下記で確認。 |

### ADごとのenforceability

**AD-1（architecture:30–51）**

- CLIが読取りと失敗判断を所有し、formatter/集計が除外FILEを読まないという依存制約は、import・呼出し・I/O spyで確認できる。`sources.py:1–22`の「取得するが終了しない」境界とも両立する。
- 集計前除外はFR-1のtop反例で表示後削除と識別可能。HTML総数は除外後かつ選択前という明確な値契約で、PRD RULE-1と一致する。
- min-count→top→formatterは既存 `__main__.py:34–48` に対応し、全形式で共通の選択結果を使える。
- RULE-2は依存宣言・権限操作・通信コードの差分確認対象として強制可能。単に「安全」と断定してはいない。
- 残る曖昧さはM-1。行解釈とエラー優先順位については製品未決の解消条件が示されており、ここで選ばないこと自体は正しい。

**AD-2（architecture:53–57）**

- 未指定で除外FILE読取り・検証を呼ばないという非干渉契約は直接試験可能。
- casefold、降順・同数初出順、min-count→topは `tokenizer.py:18`、`aggregator.py:11–17`、`__main__.py:34–38` と一致する。
- 残存語の回数と相対初出順、同一有効除外語の重複不変性はPRDの具体例で検証でき、集合の内部型まで固定する必要はない。
- 本文不存在exit1は `__main__.py:29–33` の現行契約と一致。除外FILE不存在exit2のFR-4へ一律置換する誤りを防ぐ。複合失敗の優先順位は選んでいない。

### 高度が所有する次元の網羅

| 次元 | 決着 |
| --- | --- |
| paradigm / 責務・依存 | 単方向pipes-and-filters。CLIが合成・I/O・終了判断、集計/formatterは逆依存なし。 |
| データ・状態・順位 | 一時的除外集合、集計前フィルタ、残存頻度・初出順維持、総数時点。具体型・APIはcode-owned。 |
| CLI / 行・比較 / 異常系 | オプション追加と単独不存在exit2はPRD。比較・行・読込・複数指定・空結果・複合失敗はOQ-1〜OQ-6。 |
| 書式・安全性・互換性 | 共通選択と既存formatter、未指定の書式・エラー契約維持。HTML escape・basename・UTF-8出力等は現行コード所有であり再設計しない。 |
| 説明・検証 | FR-5直接検証とFR-6へ明示委譲。新規・回帰実行済みとはしない。 |
| deployment / environments | 既存ローカルCLIのまま。環境移行なし（architecture:63、81）。 |
| infra / provider / integration | 新規provider・通信・認証・永続化なし。外部送信不要（architecture:34、63、74）。 |
| operations / 性能 / 公開 | 運用基盤・数値目標の新設なし、公開義務判明時OQ-8へ。価値評価OQ-7を機能受入へ混入しない。 |

## Input reconciliation — PRD原本

| 原本要求・補助条件 | 設計への着地 | 結論 |
| --- | --- | --- |
| FR-1：任意 `--exclude FILE`、1行1語、全出現除外、残存回数不変 | scope、AD-1、AD-2、map FR-1。行の詳細はPRD参照。 | 重要脱落なし。 |
| FR-2：空行と先頭文字#を除外語にしない | map FR-2/3、AD-1の読取り境界、OQ参照。 | 規則はPRDで確定。strip・空白コメントを勝手に追加しない。直接読込試験もPRD RULE-1のまま有効。 |
| FR-3：大小文字非区別、ASCII受入、Unicode未決 | architecture:22、51、70、79。 | 要求を保持。Unicode比較入力の実装接続はM-1。 |
| FR-4：読める本文＋除外FILE不存在で原因通知・exit2 | map:71、AD-2、CLI終了責務。 | 条件を狭めず拡張せず保持。文言完全一致・stderr・一行・汎用exit2を新条件にしていない。 |
| FR-5：help・README説明、例、対応試験 | map:72、Deferred:80がPRD直接検証を参照。 | 省略ではなく後続検証へ委譲。具体文面をこの高度で重複決定しなくてよい。 |
| FR-6：既存全試験・未指定互換 | AD-2、map:73。 | 本文Unicode、全形式、安定順位、min-count/top、空入力・既存エラーはPRDの直接検証で保持。試験未実施のまま。 |
| RULE-1：表示抑制ではない、全形式・選択前、HTML総数、重複不変 | AD-1:34、AD-2:57。 | 一致。全語除外の空結果・総数0、存在しない語だけの一覧、直接読込試験はPRDに残り、設計で上書きされていない。 |
| RULE-2：追加依存・権限変更・外部送信不要 | AD-1、map:74、運用境界。 | 一致。 |
| Non-goals・本文読込契約の自動流用禁止 | paradigm/seed、architecture:22、80。 | Web化・分割変更・曖昧一致等を導入せず、UTF-8を除外FILEに暗黙固定しない。 |
| SM-1/2、性能数値なし、利用者/why now仮説 | map、Deferred:81、PRD OQ-7/8参照。 | 試験合格や実測便益を捏造せず、追加SLOも作らない。 |
| PRDの未決は将来機能延期でなく仕様確定前の確認事項 | architecture:22、79。 | 一致。Deferredは実装者の自由裁量ではない。 |

## Input reconciliation — Brief / 保存された依頼原文

- 保存原文の除外指定、1行1語、空行/#、大小文字非区別、不存在exit2、help/README/試験、既存互換、運用制約は上記FR/RULE照合へすべて到達する。
- Brief SC-03 / Solutionにはcasefoldを既定と読める旧記述があるが、Brief:27が新除外比較について未承認案へ戻し、競合時はPRDの明示整理を優先すると宣言している。設計がOQ-1を保持するのはその更新に合致し、旧案の黙殺ではない。
- Brief Q-03の重複、Q-04のHTML総数、Q-05の通常絞込み関係はPRD RULE-1へ解決済み。設計はこれらを未決へ逆戻りさせていない。
- Brief Q-01/Q-02/Q-03の残部/Q-04の空結果案内/Q-05の複合異常/Q-06の価値評価はPRD OQ-2〜OQ-7へ、公開義務はOQ-8へ継承。設計は対応先と必要時点を保持している。
- Briefの既存tokenizer/aggregator試験合格記録は過去工程の記録に限定される。本担当が実行・追認した全件回帰結果ではない。

## PMへの引継ぎ — 製品未決を解決しない

| 未決 | 実装・合意への影響 | 戻し先／期限 |
| --- | --- | --- |
| OQ-1 | Unicode比較、M-1の情報境界、例と期待値。 | PM→依頼者／仕様・期待値確定前。 |
| OQ-2 | 空白、コメント、改行等の行解釈。 | PM経由で原PRDの要求・仕様担当→依頼者／行仕様確定前。 |
| OQ-3 | 文字コード/BOM、その他I/O失敗、診断先、失敗時stdout。 | PM経由で原担当→依頼者／読込仕様確定前。 |
| OQ-4 | 不正・複数語行、記号、複数指定、分割流用。 | PM経由で原担当→依頼者／引数・行仕様確定前。 |
| OQ-5 | 全語除外の案内・各形式の空結果と終了状態。 | PM／要求・仕様担当→依頼者／空結果仕様確定前。 |
| OQ-6 | 複合失敗・不正引数との優先順位。 | PM経由で原担当→依頼者／異常系仕様確定前。 |
| OQ-7 | 利用者、why now、価値指標。 | PM→依頼者／価値評価時。機能受入へ便益数値を追加しない。 |
| OQ-8 | 公開・契約義務・引渡し条件。 | PM→依頼者／公開・引渡し条件設定時。 |

OQの回答、承認者、採用値を本報告では作らない。architectureの`status: final`はdiscussion文書の確定状態にすぎず、本文:22の「後続実装の承認を意味しない」を優先して読む。Discussionの受領と実装準備完了を区別する。

## Disposition summary

- **autofix:** なし（設計編集禁止）。
- **discuss:** M-1と既知OQを上記PMルートへ。
- **defer to Deferred / open items:** 既存OQの担当・必要時点を維持。比較境界の再確認はOQ-1解消時に行い、仕様を未決のまま自由実装しない。
- **ignore:** 追加スタック選定、架空provider/SLO、未指定の継承ADの推測は不要。技術最新版の未確認を、新規技術選定のない本設計の欠陥とはしない。
- 作成物は本報告のみ。設計、PRD、Brief、実装、試験、READMEは変更していない。
