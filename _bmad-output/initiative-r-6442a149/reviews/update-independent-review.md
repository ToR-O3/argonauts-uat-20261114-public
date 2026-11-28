# BMAD更新原本・独立レビュー

## Verdict

原本は後続の仕様統合・要求整理に使用可能。採用回答1〜6と維持条件の欠落・矛盾、原本利用を止める設計seamは今回の静的レビューでは見つからなかった。実装合格・着手承認・機能試験合格の判定ではない。

OQ-7/8によるheadless partial／文書draftは背景不足を表す。欠陥、停止理由、新しい受入条件として数えない。重要な修正要求はなし。件数を満たすための指摘は追加しない。

## 実行条件と独立性

親authorの会話・レビュー結論を入力にせず、指定された更新原本とmemlogを直接read_fileで全文読了した独立reviewerによるレビュー。既存review-*.md、旧independent-review、親の今回レビュー結果は読んでいない。追加delegateは使用していない。

対象はbehaviorを定めるdocs。明示指定されたedge-case-hunter、structure、proseのみをbmad-reviewとして実施。edgeの経路分析と再走査を先に完了し、その結果をstructureの判断材料にせず、structureを完了してから依存passのproseを行った。proseだけは公式after=structureに従う。facilitate rubric-planning、fresh-reader、入力照合、設計gateは独立節に分けた。同一reviewerの逐次passであり、lensごとに別プロセス・別agentで隔離したとは主張しない。

公式resolve_customization.pyをuv runでbmad-review、bmad-facilitate、bmad-architectureそれぞれに対し明示project-rootと--key workflowで実行し、すべてexit0。prepend/append/persistent_facts/review_guidance/on_completeに追加指示なし。reviewはreader_type=humans、Microsoft Writing Style Guide、prose after structure。architecture configured floorはreality checkとadversarial seamの全2項目。resolve_config.pyもexit0、output_folderは{project-root}/_bmad-output、active_initiativeは返却なし。対象パスは依頼の明示値を使用し、設定変更はしていない。

レンズreferenceはedge-case-hunter、structure、editorial-common、structure-models、proseをロード。facilitateはrubric-planning、guidance-planning、保存済みmerged template両方を読了。architectureはreviewer-gateをロードした。一般のbmad-review adversarialとverification-gapは実施していない。以下の設計seam検査はconfigured floorであり、最低10件ルールの適用対象ではない。

実行は文書計量、公式customization/config解決、設計静的lint、jqによる算術・JSON検証のみ。製品CLI・機能試験・回帰試験は実行していない。Git／Kanban操作なし。製品、README、試験、GSD、OpenSpec、原本、memlog、プロファイル、設定、記憶を変更していない。新規保存先は依頼された本書とupdate-independent-findings.jsonのみ。

## 直接読んだ入力

パスは_bmad-output/initiative-r-6442a149/基準。

- brief/brief-wordfreq-exclude.md 全91行とbrief/.memlog.md 全25行。
- prd/prd-wordfreq-exclude.md 全141行とprd/.memlog.md 全22行。
- architecture/architecture.md 全94行とarchitecture/.memlog.md 全19行。
- decisions-oq1-6.md 全28行、open-questions.md 全10行。この2ファイルに対応する別memlogは対象ディレクトリのファイル探索で見つからず、上記3本の更新追記が来歴を保持する。
- brief/.template.md、prd/.template.md：既存のmerged template。新しいmerge出力は作っていない。
- initiative-r-6442a149.md：frontmatterのみでRequirements本文なし。ここから架空の要求を導出しない。
- リポジトリルートのwordfreq/tokenizer.py、aggregator.py、__main__.py、formatters.py、sources.py、pyproject.tomlをread_fileで全文読了。

## 1. Edge-case-hunter（独立behavior pass）

公式順序どおり、まず全体文書の分岐・境界を列挙し、次に同じ境界を再走査した。新規関数呼出しの実装diffではなく要求文書なのでcalleeの新旧シグネチャ比較は該当なし。既存参照先は実コードを読んだ。削除diffは入力にないためStep 3は該当なし。別claimsファイルの指定はないためStep 4は該当なし。原本内の実装参照については下記reality checkでも照合した。

未指定／指定、最後のFILEが成功／失敗／空、前のFILEが失敗、空／空白／コメント／途中#／有効行、BOM有無、指定改行形式と最終改行なし、Unicode同一キーと非一致、重複、本文にない行、部分／全語除外、全3形式、min-count/top、同数初出順、引数不正と読込エラーの組合せ、両入力失敗、除外成功後の本文失敗を走査した。各指定経路はFR-1〜FR-6、RULE-1、AD-1〜AD-4に処理または維持すべき既存動作があり、未処理経路のfindingは残らなかった。採用外の追加文法・性能閾値などを新条件として要求しない。

公式edge findings配列：[]。

update-independent-findings.jsonはこの公式配列そのものを保存する。空配列のためseverity、priority、lensなどの追加フィールドも存在しない。

## 2. Structure（edgeの結論を使わない編集pass）

目的・読者の読取り：これらの文書は、要求・実装・試験担当が採用済み除外仕様と維持境界を、承認履歴や未確認背景と混同せず使うためにある。読者はhumans。Brief／PRD／決定記録／OQ一覧はStrategic/Context (Pyramid)、architectureはExplanation (Conceptual)を主モデルとし、ADの定型はReference/Databaseとしても確認した。

### word_metrics実測

公式scripts/word_metrics.pyをuv runで各原本へ実行し全5回exit0。数え方は空白区切りtoken＋日本語・中国語文字単位であり、自然言語上の語数やページ数そのものではない。

| 原本 | total_words | per-heading body words（見出し文字自体は含まない） |
| --- | ---: | --- |
| Brief | 2029 | preamble 25; Table of Contents 93; Executive summary 319; Problem 73; Solution 334; What makes it different 73; Who it serves 81; Success criteria 359; Scope 273; Assumptions 115; Open questions 243 |
| PRD | 3333 | preamble 23; Table of Contents 123; Document purpose 229; Vision 52; Users and journeys 79; Glossary 219; Features and requirements 1369; Rules 175; Non-goals 83; MVP scope 54; Success metrics 92; Quality and constraints 56; Change boundary 123; API contract and versioning 45; Developer experience 36; Decisions 158; Assumptions 112; Open questions 245 |
| architecture | 1934 | preamble 40; Design Paradigm 149; Invariants & Rules 0; AD-1 302; AD-2 197; AD-3 356; AD-4 227; Structural Seed 184; Capability → Architecture Map 192; Deferred 194 |
| decisions | 905 | 根拠と日時 212; 採用値と追跡 500; 維持条件 163 |
| open-questions | 332 | 未決事項 325 |

各文書のタイトル直下のbodyはopen-questions以外0。全体合計8533、PRDはfrontmatter・TOC・Assumptions・見出しを除く各節bodyの和3015（jqで計算）。PRDテンプレートの約3000語という目安にほぼ相当する。3333という全ファイル計量だけで超過欠陥とはしない。Briefの1〜2ページはこの計量から確定できず、組版実測はしていない。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | Brief §Success criteria（359）、PRD §Features and requirements（1369） | PRESERVE — 成功条件の要約と原本の詳細期待値を維持 | 読者の入口と検証仕様は役割が異なる。SC→FR参照があり単純重複ではない。削減0。 |
| structure | architecture §AD-1（302）、§AD-3（356）、§AD-4（227） | PRESERVE — 成功経路図、比較境界、失敗直列順を維持 | 図の成功経路だけでは失敗順・本文非読込を表せない。図後の限定とAD-4が必要。削減0。 |
| structure | decisions §採用値と追跡（500）、open-questions本文（325） | PRESERVE — 解決履歴と背景未決を別の入口として維持 | 採用済み1〜6とOQ-7/8の混同防止。原文・日時・担当／再訪時点を落とさない。削減0。 |

変更を求める構成findingはなし。上表は保全判断3件であり欠陥件数には含めない。削減提案0件、推定削減0語相当／0%（8533基準、jq計算）、理解のための図・例・追跡を犠牲にする提案なし。文量を削るために採用仕様を再提案や未決へ戻さない。

## 3. Prose（公式after=structure）

文体を先に分析：日本語の短い断定文、FR／ADの技術識別子、CLIオプション、英語見出し、具体的な入出力例を使う仕様文体。これらを保持し、単なる好みの言換えは行わない。structureにCUT／MERGE指定はない。frontmatter、コードブロック、構造マークアップはcopy-edit対象から外した。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |

理解を妨げる表現上のfindingはなし。特に「途中#は文字」「全語除外の専用メッセージなし」と「既存HTML案内は維持」、「最後のFILEだけ採用」と「前を読まない」は別の意味を持ち、統合して意味を落とさない。本文casefoldと除外行を本文tokenizerで分割しない点も用語上区別されている。

## 4. Facilitate rubric-planning（独立節）

判定：この小規模CLI機能の採用仕様と後続の確認事項は判断可能な形になっている。利用者・why nowなどの背景の未充足は正直に留保されており、それを機能仕様の欠陥や停止へ変換する必要はない。

優先して直す事項はなし。3件を埋めるための修正要求は作らない。

| Dimension | 評価 | 原本根拠と判断 |
| --- | --- | --- |
| Decision-ready | strong | PRD:32-36、58-86、96、122。採用回答、期待値、non-goalsと後続境界が明示されている。 |
| Earned | adequate | Brief:27、35、49-51、78-80、PRD:128-130。架空のpersona・便益・技術刷新を置かず、背景は未確認のまま。 |
| Testable | strong | PRD:58-86。全形式、順序、診断の対象と原因、exit/stdout、Unicodeと空結果を検証可能。数値性能要件を創作しない。 |
| Honest scope | strong | PRD:90-118、132-141、設計:90-94。今回の文書更新と後続製品作業を分離。OQ担当と再訪時点あり。 |
| Usable downstream | adequate | SC→FR、FR/RULE→ADの参照が揃い、Glossaryと具体例で用語が定まる。設計の具体関数／型はcode-ownedとして適切に残す。 |

Done when照合：

- Brief：executive summaryだけで何を作るか・想定利用者・今回の契機は読める。実在利用者、負担、事業上のwhy nowまで証明するtemplateの理想状態は未充足だが、A-01〜03／OQ-7/8へ正しく記録されている。背景partialとして扱い、原本利用の停止条件とはしない。The ask／Visionの対象外理由はScopeとmemlogにある。
- PRD：各FRは既存CLIへの依頼に追跡でき、直接検証があり、non-goalsも明示。単一利用者CLIに架空journeyを足さない。SM-2はSM-1の対抗指標を明示。採用判断は決定記録と今回memlog追記に対応し、回答済み1〜6を再質問しない。追加公開義務や版番号を推定しない。

この節で報告すべき欠陥findingはなし。

## 5. Fresh-reader（独立節）

ここでは原本文書だけを使える後続読者として読み、親の会話やmemlogで不足を補わず、使用前に何を知る必要が残るかを検討した。別agentによる再読とは主張しない。

- PRDが期待値原本、決定記録が承認の来歴、architectureが実装間の共通拘束と判別できる。
- 除外ファイルの構文、読込順、終了状態、既存HTMLの空結果がそのまま追跡できる。
- 配置・関数シグネチャは実装担当が現行コードを見て決める範囲であり、読者を止める未定義仕様ではない。
- OQ-7/8は価値評価／公開条件を決めるときにPMへ戻す背景。現在の統合や機能仕様の使用に追加回答は不要。

結論：原本を使うために重要な未回答は残っていない。実装や試験の成否はこの読取りから判断しない。

## 6. 入力照合（独立節）

受付t_c172b029、人default回答2026-11-28T06:59:36.405633+00:00、PM t_834ece37、差戻しt_14fbf7f0を依頼で与えられた照合根拠として使用。外部チケット取得を行ったとは主張しない。原文『提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。』はBrief:29、PRD:34、decisions:5-8と一致する。

| 入力 | 原本の着地点 | 照合結果 |
| --- | --- | --- |
| 1 本文casefold維持／除外casefold／Straßeで本文STRASSE除外／情報損失再確認 | Brief SC-03、PRD FR-3:66-68、AD-3:59-65、decisions OQ-1 | 採用済み。抽出後キーを使う実読説明あり。lowerへの変更や失われた元表記の復元を要求しない。 |
| 2 strip→空／先頭#無視、途中#そのまま、LF／CRLF／最終改行なし | Brief:39、SC-02、PRD FR-2、AD-3、decisions OQ-2 | 一致。コメント判定はstripの後。 |
| 3 UTF-8先頭BOM除去／各読込失敗の対象原因stderr・exit2・stdout空 | Brief:39、43、PRD FR-2／FR-4、AD-3／4、decisions OQ-3 | 一致。不在だけでなく権限・dir・不正コード等を含む。 |
| 4 全体一語、分割／記号除去なし、foo bar個別除外なし、foo_bar／123／foo-barそのまま、非出現・重複無影響、最後のFILEのみ／前を読まない | Brief:41、PRD FR-1／2、RULE-1、AD-2／3／4、decisions OQ-4 | 一致。最後が空のケースもFR-1に明示。 |
| 5 全語除外は既存空結果exit0・専用メッセージなし | Brief:43、66、PRD FR-6、AD-2、decisions OQ-5 | 一致。既存HTML案内の保存も明示。 |
| 6 既存引数検証→除外→本文、両失敗は除外exit2、除外成功本文失敗exit1 | Brief:43、PRD FR-4、AD-4、decisions OQ-6 | 一致。help既存終了、引数不正時FILE非読込も明示。 |
| 全形式除外はmin-count/top前、残存回数・相対初出順、HTML総数は除外後min-count/top前 | Brief:64-70、PRD RULE-1／FR-1、AD-1／2、decisions:26 | 一致。具体例の総数3、同数順beta→alphaとも整合。 |
| help／README／追加試験／既存互換、依存・権限・外部送信不要 | Brief SC-05、PRD FR-5／6、RULE-2、設計map／Deferred | 後続要件として保持。このレビューでは実施していない。 |
| OQ-7/8だけ背景不足、停止理由でも新条件でもない | 全原本の未決節、設計Deferred | 一致。採用回答1〜6を未決に戻していない。 |

memlog監査：Brief:13・18、PRD:10・15、architecture:12・13などは旧時点の留保。各memlog末尾の今回update（Brief:24-25、PRD:21-22、architecture:18-19）が明示回答による解決を記録し、現行原本・decisionsへ着地している。過去のpytest実行記録を今回の新機能合格に流用しない。旧discussionからbuild-substrateへの更新とAD-1/2継続、AD-3/4追加も整合する。

## 7. Architecture reviewer-gate

### 7.1 機械検査

公式lint_spine.py --workspace _bmad-output/initiative-r-6442a149/architectureをuv runで実行。exit0、ok:true、spine:architecture.md、total_findings:0、by_severity:{}、findings:[]。これはplaceholder／AD識別子／必要field／Stack表などの機械検査であり機能試験ではない。

### 7.2 Rubric walker

| Good-spine観点 | 実読結果 |
| --- | --- |
| 実際の分岐点を固定し、RuleがPreventsを防ぐ | AD-1は共通の集計前境界と総数、AD-2は非干渉・残存順・空結果、AD-3は正規化／行解釈、AD-4はFILE選択と失敗順を固定。各RuleはPRDの期待値で反証可能。 |
| Deferredから不整合が入り込まない | 関数配置・集合型・例外型・説明文・試験配置は実装所有。比較キー、行文法、優先順位を変更する裁量は明示的に与えていない（設計:92）。 |
| 技術とbrownfieldに適合 | 現行5モジュールとpyprojectを読了。新サービス／永続化なし、既存の取得→tokenizer→aggregator→formatterを維持する。詳細は7.3。 |
| 入力要求の網羅 | FR-1〜6、RULE-1/2すべてがmapにある。FR-5は後続help／README／試験であり新しい設計拘束の創作は不要。initiativeはRequirementsなしのためPRDを実際の拘束元として照合した。 |
| 継承・識別子 | 本入力に上位spine指定はない。旧AD-1/2はmemlogと現行で同ID維持。回答済み判断を弱めていない。 |
| 構造・運用の次元 | 単方向依存、入力・正規化・計数・選択・表示・エラー所有を明示。ローカルCLI維持、デプロイ・環境移行・provider・認証・通信・永続化・技術version追加なしもStructural Seedに明示。運用次元の無言の欠落はない。 |

rubric walkerとして追加の修正要求なし。

### 7.3 Configured floor: reality check

- tokenizer.py:6-18：Unicodeの\w+で抽出し、iter_tokensは入力順にtoken.casefold()を返す。本文の比較元は既にcasefold済み。元表記や区切り記号は残らないが、採用した同一casefoldキーの比較には必要ない。PRD FR-3／AD-3がこの情報境界を正しく扱う。Straße／STRASSEの一致は仕様として採用済みであり、今回実行確認したとは主張しない。
- aggregator.py:6-17：Counterで計数し、top_wordsは回数降順のstable sort。入力の相対初出順を保つフィルタなら同数順維持と整合する。
- __main__.py:13-38：現在exclude引数はなく、parse_args→top/min-count検証→本文取得、本文InputErrorはexit1。totalは選択より前、min-countの後にtopを呼ぶ。AD-1/4の追加位置・維持順と整合する。未実装であることも原本が明示している。
- __main__.py:39-54／formatters.py:6-14、22-38：形式ごとの出力と終了はCLI所有。text空、JSON []改行、HTMLの空表・既存案内・呼出し元totalは設計の空結果定義と一致する。
- sources.py:17-22：本文はencoding=utf-8、OSError／UnicodeDecodeErrorを対象パスと原因を持つInputErrorへ変換。現在の本文読込をそのまま使っても除外先頭BOM除去やexit2にはならない点を、PRD Non-goalsとAD-3/4が区別している。
- pyproject.toml:5-12：既存Pythonパッケージでdependencies=[]、devはpytest。設計は新ライブラリ／starter／providerを指名・固定していない。変更しないPython、setuptools、wordfreq等のversionを新規に固定せず、既存実コード・manifestでfitを確認した。新技術判断がないためweb-researchは不要。

結論：トレーニング由来の未確認技術判断は見つからなかった。現行コードが新機能を満たすという意味ではない。

### 7.4 Configured floor: adversarial seam

全ADを文字どおり守る二実装が異なる観測結果を出せるか、次の対を静的に構成・棄却した。公式bmad-review adversarialではなく、設計のconfigured floorに限定する。

| 対の候補 | 全AD適合性とseam判定 |
| --- | --- |
| A: readerがcasefold集合を作りgenerator filter、B: readerが有効行列を作り同一キーで順序保存filter | 両方とも全ADを守れるが、重複・非一致・残存順を含め観測差は出ない。集合型や配置を固定する理由にはならない。 |
| A: 除外行を丸ごとcasefold、B: 本文tokenizerで除外行も分割 | BはAD-3違反。foo bar／foo-barの不一致は既に拘束されており、全AD適合の対ではない。 |
| A: 最後のFILEだけ読む、B: 先行FILEを検証後最後を採用 | BはAD-4の前を読まない規則に違反。先行missingによる不一致は設計の穴ではない。 |
| A: 除外成功後に本文を読む、B: 本文を先読みし失敗を保留 | BはAD-4の順序と除外失敗時本文非読込に違反。終了コードだけ合わせても全AD適合にはならない。 |
| A: 全形式共通で集計前除外・総数再計算、B: formatter直前に行だけ削除 | BはAD-1違反。HTML総数やtop差は拘束済み。 |
| A: 残存入力順を保存、B: 集合／ソートを経由し同数語を並べ替え | BはAD-2の相対初出順保存に違反。 |
| A: 全語除外を既存formatterへ渡す、B: 専用メッセージで置換 | BはAD-2違反。既存HTML案内自体はAにも残る。 |
| A/B: 異なる除外エラー文だが両方とも対象・原因、stderr、exit2、stdout空、本文非読込を満たす | 文言の完全一致は契約外なので、許容差であり不整合ではない。 |

全AD適合でありながら契約上の観測が食い違う対は、今回検査した境界では見つからなかった。配置・具体型の違いを理由に新ADを追加しない。有限の静的検査であり、あらゆる実装の一致を証明したものではない。

## 保存と結論の範囲

本レビューは原本使用可能性の判定まで。設計lintと文書計量は実行したが、実装・追加試験・既存回帰の合格は未判定。原本への修正は行っていない。

保存先：
- _bmad-output/initiative-r-6442a149/reviews/update-independent-review.md
- _bmad-output/initiative-r-6442a149/reviews/update-independent-findings.json
