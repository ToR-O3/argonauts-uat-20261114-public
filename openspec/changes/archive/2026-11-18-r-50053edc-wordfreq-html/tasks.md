# Tasks

## 1. 全形式の同数時初出順（AC3・既存回帰）
- [x] 1.1 集計時の正規化後初出順を保持し、回数降順の安定ソート後にtopで切る。集計単体とtext/jsonの実CLI試験で `Zoo apple APPLE zoo banana`、top 1/2、後の再出現、回数が異なる入力を確認し、旧仕様の語の昇順なら失敗することを示す。部品の順序契約と意図した互換性変更を同時に文書へ記録する。

## 2. 安全な静的HTMLとメタ情報（AC1・AC2・AC5）
- [x] 2.1 単語・basenameを安全な表示テキストとして埋め込むHTML整形を作り、順位・単語・回数の見出し、UTF-8宣言、内包CSSだけの1枚文書を返す。整形単体試験で空pairs、特殊文字 `& < > " '`、タグ・イベント候補が表示文字となり、余分なタグ・スクリプト・外部リソースが生成されないことを確認し、部品契約を文書化する。
- [x] 2.2 CLIへhtml形式を接続し、top前countsからの総数と実行環境のbasenameを整形へ渡す。入力パスはtitle/属性等にも出さない。実CLI試験で `zoo apple zoo banana apple cherry` のtop 1/2/10でも総数6、別の頻度入力 `beta beta beta alpha gamma alpha delta` のtop 2でも総数7、表の上の表示位置、既定10・種類数超過・空入力0行を確認する。利用説明へ実行と保存の使用例を追記する。
- [x] 2.3 同じ入力のtext/json/htmlの語・回数・順序を照合し、html指定でも不正top（0・負・非整数）、不正format、引数個数、読込み/デコード失敗のexit・stderr・空stdout、Unicode抽出・casefold・入力境界を回帰試験する。特殊文字を含む有効なbasenameをCLIで検査し、単語認識を緩めない。text/jsonの構造・空出力は同数時順序以外に変更せず、試験結果で確認する。

## 3. 明るいレスポンシブ表示（AC4）
UI設計・PLANで通常幅と対象ブラウザ、320 CSS pxで実際に折返す長い語・有効なbasenameの固定入力を確定する。名前の連続空白・改行・タブの保持、保存HTMLの実UTF-8と宣言の一致、複数桁の数値列も検証対象へ含める。
- [x] 3.1 明るい背景のみ・切替なし・1始まり表示行連番を適用し、長い語とbasenameを折返して読める表にする。通常幅と320 CSS pxの実CLI生成HTMLで、空・通常・長文・同数topの表示を試験し、順位1/2、横はみ出しなし、省略なしを確認する。採用したUIと確認条件を説明文書に残す。
- [x] 3.2 ブラウザ検証手順と必要なローカル補助を用意し、viewport・要素・文字Range行断片・切取り祖先・隣接内容の実測原本および画面画像を保存する。横方向の収まり、切取り祖先内の収まり、隣接内容との非重複、画像の可読性で判定し、要素自身への厳格な縦包含を必須にしないことを試験/手順で確認する。値を補正して合格に見せず、全文を確認できる画像と実測を対応付ける。

## 4. 独立した統合検証と証拠（AC1–AC6）
検証開始時の作業状態と製品コードの差分を保存し、headと実行コードの対応を確認する。通信観測は文書を開く前から表示確認終了までとし、失敗試行と文書由来の遷移を含め、ブラウザ背景通信を区別する根拠も残す。
- [x] 4.1 品質担当が対象headで入力原本からCLIを独立再実行し、text/json/htmlの一致と、空・通常・top・長文・注入候補のHTMLを通常幅および320 CSS pxで確認する。外部参照の静的検査と外部通信の試行記録を残し、通信遮断だけで無通信と判定しない。全画像を実際に読み、幾何原本と合わせACごとに判定する。head・入力・コマンド・exit/stdout/stderr・期待値・生成HTML・ブラウザ/viewport・矩形・画像・通信記録を保存して添付する。Builderの画像だけで代用しない。
- [x] 4.2 全自動試験と変更差分を確認し、AC1–AC6と既存回帰の結果を追跡可能にまとめる。未実施条件は未検証として残し、証拠不足のまま合格にしない。CI追加・変更、依存追加、生成日時、テーマ切替、対話操作、サーバー、単語認識変更がないことを差分で確認する。

## Workflow follow-up
- 03-01 task 1: 共通初出順・HTML CLI接続・最終UI構造/CSSを実装し、集計5件・CLI27件・全50件が成功。1.1の文書と2.1の部品安全性試験はtask 2へ続く。2.2の全メタ情報行列と3.1のブラウザ確認は後続PLANまで未完了。独立品質4.1は未実施。
- 03-01 task 2: HTMLParserで元値の一度escape/空tbody/意味構造/固定タグ属性/CSS外部経路不在/非破壊を確認。READMEとCONCEPTSに現行契約を記録。整形6件・全52件成功。1.1/2.1だけを完了とし、2.2/3.1は接続・CSS・使用例までの部分完了（後続の全行列/ブラウザ/品質は未実施）。
- 03-01 review rework CR-01/WR-01: 不正UTF-8 basenameの置換表示とHTML専用UTF-8バイト出力をCLI境界で修正。各2件の実CLI REDを確認後、回帰4件と全56件成功。READMEの環境前提を修正。2.2/2.3の全行列・3.1のブラウザ・4.1の独立品質は未完了のまま。
- 03-01 review rework round2 CR-01: basenameを実行環境のfilesystem encodingで復号し、復号不能バイトだけ置換するよう修正。ISO-8859-15の有効なcafé.txtを実CLIでRED確認後、既存UTF-8/出力encoding回帰を含む5件と全57件成功。新規試験はlocale実在/charmapを確認。READMEも訂正。後続taskのチェック・公式計画位置は進め直さない。
- 03-02 task 1: 実CLIの全形式・明示期待値で総数6/7/0/200、top1/2/10/12/既定/超過、保存UTF-8 bytes、有効な注入候補basenameと全HTMLの生/escape済み親path不在を確認。全形式の読込み/引数失敗・実PermissionError（chmod後に同一実効ユーザーの読込み拒否とCLI stderrを確認、finallyでmode復元）・例外cause・hash seed0/1/42・cold-copy非破壊を検証。CLI95件とsource/tokenizer/boundary15件が成功し、2.2/2.3を完了。
- 03-02 task 2: HTML前処理のCR→LFを再現する試験を先に失敗させ、公式RED_EVIDENCE_OK後、全動的値をhtml.escapeしてからCRだけ&#13;へ符号化。固定長basename/語・12連番・123/巨大整数・完全な固定CSS宣言・構造/安全性の静的契約を追加。実CLIでも長いbasenameとCRを保持、locale charmapを確認して黙ったfallback/locale不足skipを防ぐ。整形9件・全126件成功（skipなし）。3.1は静的実装・試験までの部分完了、ブラウザ実測・全画像/通信観測・独立品質4.1は未実施のため未チェック。
- 03-03 tooling（独立品質gateの完了ではない）:
  - [x] 3.1 tooling部分: 固定15 CLIケース・HTML11ケース×両幅の実再生成、DOM/順序/総数/長文折返しと数値の自動幾何判別を用意。全画像の可読性はpendingのため3.1全体は未チェックのまま。
  - [x] 3.2 tooling部分: raw element/全文/文字Range・空矩形・UTF-16/codepoint・全祖先・実フォント・full/tile画像の対応採取と、own-height越え許容/clip/隣接非重複の判別試験を実装。実閲覧は未実施で3.2全体は未チェック。
  - [x] 4.1 tooling部分のみ: pre-open context/main-CDP/browser-flatten-autoattach観測と、clean/failed-resource/document-navigation/early-popup/client-redirectの実canaryを用意。採取はcapture-only/pending-review、品質の独立再生成・全画像閲覧・live観測・AC別判定は未完了。4.1の独立品質gateは未チェック。
  - [x] 03-03 review round2 tooling修正: coverageをready順序と同文書context/main/flatten要求・paused target対応から導出し、検証側も再計算。各td/メタ値等は文字record・character Range・全文一致を必須とし、欠落/空/部分測定は失敗。回帰のRED後、58 verifier/全184試験成功。全画像閲覧・live・独立品質gateのチェックは進めない。
  - [x] 03-03 review round3 tooling修正: Network requestIdをsource/session/target単位の開始へ結び、response/redirectResponse/documentURLも検査。未帰属再取得を実22画面で失敗再現後、DOM/CSS有効化をopen前へ移動。非空白文字は正面積のRangeを必須化。回帰RED後全213試験・実capture/canary成功。全画像閲覧・live・独立品質gateは未完了。
- GSD対応表は03-COVERAGE.md。チェックは実際に完了したtaskだけを更新する。
- 03-04 task1 tooling（独立品質・全画像受入はpending）:
  - [x] 3.2 tooling: live review-session/finalize、全full/tile画像のactor・時点・SHA・全域・実寸scale・rawRange原本対応台帳と欠落拒否を実装。collectorは閲覧済みを生成しない。
  - [x] 4.1 toolingのみ: profile/role/root分離、fresh入力・CLI再生成、canary再実行と全試験、AC1〜AC6索引、pre-openからfinal flushまでの有限観測を用意。4.1本体の独立品質は未完了。
  - [x] 4.2 tooling: planning-start base5a7659bと実行HEADのscope確認、承認済03-02製品snapshot固定、dirty/untracked/head変更・終了済capture・証拠欠落の拒否を実装。phase受入はpending。
  - [x] 03-04 task2: 実CLI option/schema/全fixture/AC索引に照合した独立品質runbookとREADMEリンクを作成。空台帳finalize拒否と未閲覧timeout非0を実Chromiumで確認。終了時provenance・全browserContext帰属・画像/raw hashも再照合する。独立品質・全画像実閲覧・最終accepted経路は未実行のまま明示。
- 03-06 初回Builder delivery（H1独立品質前、3.1/3.2/4.1/4.2は未チェック）:
  - locale不在を制御した回帰が必須locale assertionでREDとなることを確認後、raw byte E9実ファイルと実CLI/FileSourceを使うcontrolled encoding seamを追加。filesystem表示codecとstdout encodingを分離、sidecarへraw argv往復・選択codecを記録し、strict UTF-8/日本語/全行/総数/入力不変を確認。実hostのnative ISO-8859-15とC/latin-1も別実測。CLI100件成功。native不在分岐はnative実行と呼ばない。
  - missing base/approved参照の未捕捉例外と新owned helper拒否、root pytest.pyのprovenance漏れをREDで確認後修正。fixture所有実git/depth1によるscope、外部tests/両収集pattern/nested conftest/root shadowのdirty/staged/deleted/untrackedとhash、別actor finalize拒否/省略actor保存を回帰。verifier200件・全358件成功（skipなし）。fixture成功と実exact-ref scope、Builder自己試験とCI/独立品質は別の結果。
  - runbookの同カードH1品質request_changes→Builder根拠確認・tasks記録/push H2→re-request_review→品質fresh-root全gate再実行を追加。guide契約試験のREDを確認してから文書化。独立品質の全画像/raw/通信/AC/最終headCIとOpenSpec critical0は未実施のため、完了したと記録しない。
- 実装・品質検証・受入が済んでから、別工程でsync・archiveと最終確認を行う。本カードではarchiveを行わない。

## 現在：03-06 H3独立品質に基づくBuilder事実記録（H4）

カード `t_13f258db` 品質run118・コメント56は、修正head H3 `48b02aaed5fa51120044c1b1fa8898c0a0191b77` のfresh-root全技術gateを合格とし、未チェックの原本4項目の記録だけを差し戻した。Builderは報告全文と品質原本を読み、manifestの131原本hash、全22 view/derived、全32画像のpath/hash/viewed_at集合、ledger hash、AC1〜6 accepted、independent_acceptance true、errors空、終了provenanceのH3一致・製品dirty/untracked空を再照合した（不一致0）。品質が実owner exit0を確認した報告も照合し、未達の技術条件がないため、3.1/3.2/4.1/4.2をH3での実施事実としてチェックする。これはH1根拠の復活でもH4受入でもない。

保存先 `Q` = `/home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-quality/evidence/t_13f258db`、`F` = `Q/quality-roots/gap1-final-03`。実行時root `.planning/argonauts/r-50053edc/quality/gap1-final-03` から保存先へ移動した原本であり、内部の実行時絶対pathは変更していない。GSD原本は標準添付106、主要画像は107〜112。報告全文はコメント56にも保存。JSON/通信/全画像等の残りの原本はQに保存されているが、品質の添付ガードで拒否されたものを「標準添付済み」とは記録しない。最終再品質で標準原本添付の確認がなお必要。

| H3原本path | SHA-256 |
|---|---|
| `Q/h3/quality-report-H3.md` | `40f821efe5fc00310461508ab439199e4e04b7c622535fb19c55309a5e4adde8` |
| `F/manifest.json` | `228f7103f256494bdb5694755b61753cbd8f9cf645b82f9fda92e46a72e4069f` |
| `F/reviews.json` | `2ac3f23a13d6d9c4a9653cfe9c6912ad550d2e681b8308bca59b6b919edc434a` |
| `F/canaries/canaries.json` | `06d078da506f5565d13550605592762a9d6bbb0c6ba12964ce2cdbfc48b3578e` |
| `Q/quality-roots/gap1-network-04/canaries.json` | `4bde1f1b1c73dfc1908496b12cc4d9571a34d4531a90a72e952d06a77bbb6c7f` |
| `F/scope.json` | `43e33d6cbef9d9951a533373fb5dc2aaedf4f9fe30cc64d943d83f63276d5c97` |
| `F/suite.xml` | `bee8f3b6a2c5cae85e96309354afd77ff9c0781a9e1d3dcf8d1ef12f0c3d30b5` |
| `Q/h3/suite.xml` | `9d022e251081442d711f1ee66f14097816639a6e8ebae3fb93707fb68c8ced4c` |
| `Q/h3/scope.json` | `d3340e7c550dbddaf641d5cf1000046ce2f9a9d82628c2014cc2c2c55b697676` |
| `Q/h3/ci-job-134274566962.log` | `6a4452400e2ef91e06e9d5677237a3626d868a3b2f6ee5835295eede4976dd47` |
| `Q/h3/ci-job-134274502310.log` | `7892a7251f29026e0d1b2b3292734f969dc9ac32c8db93fe33072680586d82ce` |
| `Q/quality-roots/gap1-layout-01/pixel-comparison.json` | `04a5d87092f85c77c8be55ebbe4392a5a7f05247a7113b85e682829c964f83cc` |
| `Q/h3/rawaudit.txt` | `b9cdd277d93d88f4be987228b5d944c9eb259f1508e092db43957423ec46127f` |

### task別の完了事実（すべて品質H3、H4ではない）

- **3.1**: 品質が入力から独立再生成した空・通常top1/2/10・frequency・同数top1/2・長文top12/既定/99・注入の11 HTMLをChromium 1280×900/320×900 CSS px・DPR1・zoom100%で確認。`F/<case>/{1280,320}/full.png` と全tiles計32枚を品質が1:1で実閲覧し、上表ledgerの32件がreadable/full extent、全22 view accepted。明背景のみ・切替なし・1始まり連番・長い語/basenameの空白/LF/TAB保持・折返し・横収まり・非省略を確認。採用UI/条件は `03-UI-SPEC.md` と `docs/wordfreq-html-verification.md` に記録。
- **3.2**: `F/<case>/{1280,320}/raw.json` 全22件のhashがmanifestと一致。品質の無補正監査でtext/index/codepoint/UTF16/非空白面積/横収まり/clip祖先/正面積隣接重複は問題0。各clientWidthは320/1280。画像とrawの行数・位置が一致（320ではn=29×6+2、w=12×21+4、123右端296；1280ではn=90+86、w=60×4+16、h1左192、123右端1080）。品質独立pixel probeは8 viewのviewport/full差分0、全tile/full差分0。own-heightの厳格縦包含は要求せず、横/切取り祖先/隣接非重複/実画像可読性で判定。全32画像集合がledger/manifest/全derivedで一致。
- **4.1**: `F/*/cli.json` 全15件を品質が独立実行。全exit0/stderr空、11 HTML strict UTF-8、外部参照/親path無し、全形式の期待pairs/総数一致。全22 `network.json` はerrors0、http(s)/ws無し、file/about/chromeのみ（chromeはomnibox）。除外はdifferent browserContextIdの根拠付き。pre-open〜閲覧/live finalize/flushまで観測し、session内とgap1-network-04のcleanおよびfailed-resource/navigation/early-popup/redirect実試行の検出・拒否を確認。finalize-requestedだけで成功とせず、owner実exit0後にAC1〜6 accepted・独立受入true・errors空・終了provenance H3を品質が読戻し、Builderも保存原本の最終状態を照合。
- **4.2**: 品質full suite361 passed、failures/errors/skipped0、session内も361成功。実scopeは固定baseline `5a7659b949dc118b59cea5ef3eb40bcd94337d8d` / approved `ed7e6cc9d608bc40a82da76e85ca6e57a0808b54` / target H3でpassed/errors空。CI run44149774801/job134274566962とrun44149757304/job134274502310は同H3・両success、各ログ361 passed。禁止CI/依存/製品/生成日時/テーマ/対話/サーバー/抽出変更なし。GSD添付106はcritical0/warning2/info3。WR-01/02と旧非block指摘は品質判断どおりPM/フェーズ検証へ引継ぎ、承認範囲外の変更を加えない。

**残る工程**: H4はこの事実記録を追加した新headで、独立受入未実施。fresh `gap1-final-04` / `gap1-network-05` 以降でPLAN全文（画像/raw対応を含む）を全面再実行し、同H4 CIと公式OpenSpec implementation verify critical0、標準原本添付を確認する。H3合格/CIの持越し禁止。文書のみの変更でも省略しない。未達時は承認不可。phase検証・phase.complete・sync/archive・マージは別工程で未実行。

## 履歴：03-06 H1独立品質後のBuilder事実記録（H2記録更新）

**訂正：このH2記録の完了判定は撤回し、原本3.1/3.2/4.1/4.2を未チェックへ戻した。** カード `t_13f258db` の品質run116・コメント54で、H2 `203e3cb9eb1be18cc2fcd0c4375391463f441423` の5つの長文viewに画像/raw layout不一致が判明し、H1にも同じ欠陥があった。対象H1 `fe5d67863ad7d8927b17eb33cbdfdd560a82951f` で実施者 `argonauts-uat-quality` が当時合格と報告し、Builderが原本131件hashと保存されたaccepted値を照合した事実は残すが、hash/台帳整合は実画像とrawのlayout一致を証明しない。「H1に未達の技術条件はない」という判断を取り消す。下記の所在/hashとtask別記述は当時の報告履歴であり、現在の合格根拠ではない。原本を書き換えない。

### 証拠の所在と同一性

品質の保存先 `Q` は `/home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-quality/evidence/t_13f258db`。実行時rootは `.planning/argonauts/r-50053edc/quality/gap1-final-01`、保存後は `Q/quality-roots/gap1-final-01`（以下 `F`）。移動前の絶対pathはmanifest/ledger内に原状保持されており、書き換えていない。画像は本カード標準添付72〜103（全32枚）、GSDレビューは添付71。JSON等の全原本archiveは品質側で添付ガードに拒否されたため、**添付済みとは扱わず** `Q/quality-evidence-H1.tar.gz` に保存、品質報告はコメント52にも全文保存されている。最終headの品質では原本の標準添付も改めて確認する。

| 原本path | SHA-256 |
|---|---|
| `Q/quality-report-H1.md` | `d2957a215593cb1c8d3607dddedb3574ca4d73d93feaf55e9e8bfd94c8baa62b` |
| `Q/quality-evidence-H1.tar.gz` | `bd7c240afcbeeabd16d53d5d1a817c5498749bb0009d5030240f8c7edbf0ea25` |
| `F/manifest.json` | `f864eff3265603f8207f9ffca439f7c53e3170295a719e63697b4dfc85bdec19` |
| `F/reviews.json` | `813c793c618299d0573a9186aa93bc500000eb1687bde5c4e27636eb29f6b94d` |
| `F/canaries/canaries.json` | `a206a60337de553977cb9027c23c186c4bdfa5abf50eedbc1b69f81af34d24f4` |
| `Q/quality-roots/gap1-network-02/canaries.json` | `fd1aaeaa0ae4f0a04724222a32bdc97e5fcd135c829a2561b677b48ddd66b5b0` |
| `F/scope.json` | `cfe9e716459f317fa99338403a94583e69eaaa318dbc9ae686043089dedfa02d` |
| `F/suite.xml` | `0eb3b2a8603fe4a4bfe684a9195c3a2324a332d8062adc192b72e55764c08934` |
| `Q/quality-ci-job-134236962775.log` | `93daacda851d30b682c5f36995539481d9c382a7f38d056d41b28ec24c010057` |
| `Q/quality-ci-job-134236900168.log` | `7a9eef9894441ccf949504fec45a53a1f27a849fed9839d7c94c3995a77a5cbf` |

### task別の当時報告（すべてH1、完了根拠として撤回）

- **3.1**: 品質が入力から独立生成した空・通常top1/2/10・frequency・同数top1/2・長文top12/既定/99・注入の11 HTMLをChromium 1280×900/320×900 CSS px・DPR1・zoom100%で検証。`F/<case>/{1280,320}/full.png` と全tiles計32枚を1:1で実閲覧。`F/reviews.json` の全32判断readable、22 view accepted。明背景・切替なし・連番・長い語/basename/空白の保持・折返し・横収まり・非省略を確認。設計/手順は `03-UI-SPEC.md` と `docs/wordfreq-html-verification.md`。
- **3.2**: `F/<case>/{1280,320}/raw.json` 全22原本のhashをmanifestと対応付け。品質は文字/UTF16/codepoint/空白/祖先を無補正で監査し、text一致・非空白の正面積・横収まり・切取り祖先・正面積隣接非重複を確認。own-heightだけの越えを失敗条件にしない。品質最終読取りではledger/manifest/全derivedのimage/path/hash/viewed_at集合32件が一致し、全22 derived accepted、pending無し。
- **4.1**: `F/*/cli.json` 全15実CLI、stdout HTML11件とtext/json同数入力を独立再生成。全exit0・stderr空・strict UTF-8、親path/外部参照なし。全22 `network.json` はerrors空・file://のみ、背景通信はdifferent browserContextIdで帰属分離。pre-openから閲覧/live finalize/flushまで観測し、session内/別rootのcleanとfailed-resource/navigation/early-popup/redirect canary実試行を確認。最初のnetwork-01はSocket path too longでexit1/unverifiedとして保存し、短いTMPDIRで新network-02を実行してexit0/passed（失敗を消していない）。finalize-requestedを合格とせずowner実exit0後のmanifestでAC1〜6 accepted・independent_acceptance true・errors空・終了provenance H1/製品dirty空を確認。
- **4.2**: 品質の全358試験成功、skipなし（hash seed12345でも358成功）。実scopeは上記baseline `5a7659b949dc118b59cea5ef3eb40bcd94337d8d` / approved `ed7e6cc9d608bc40a82da76e85ca6e57a0808b54` を解決してpassed/errors空、製品snapshot・禁止差分なし。H1 CI run44139189750/job134236962775とrun44139172431/job134236900168は両success、各ログ358 passed。未報告を成功に読み替えていない。GSD添付71はcritical0/warning3/info3、非block指摘はPM/フェーズ検証へ引継ぎ。native ISO実在hostの実測と、native不在制御下の実byte seamは別々に実行済み。

**H3初回提出時の残るgate（履歴、現在の状態は次節）**: H1/H2の完了根拠は上記の理由で撤回。3.1は同じlayoutに対応する新画像とrawで再判定、3.2は全full/tileと実測の対応を再確認、4.1は新headで独立全AC/通信/owner完了を再実行、4.2は新head全suite/実scope/同head CIと未実施項目なしを再確認するため、4件とも未チェック。H2は欠陥発見後finalizeせずunverifiedで終了しており、合格を持ち越さない。H3の修正はopen前からscrollbar gutter条件を統一し、通常幅/狭幅の実pixel差分回帰をRED→GREENで確認したが、これはBuilder自己試験のみ。品質は新head/H3・新root（gap1-final-03 / gap1-network-04以降）でPLANの全gate・全画像実閲覧・画像/raw対応・実scope・全試験・同head CIを全面再実行する。技術合格後にtask別head/path/hash根拠を返し、Builderが記録を更新する。その記録headも新rootで全面再品質し、最後に公式OpenSpec verify critical0が要る。原本添付の確認も含め未達があれば承認不可。phase.complete、sync/archive、マージは未実行。
