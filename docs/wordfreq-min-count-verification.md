# wordfreq --min-count：品質独立検証runbook（Phase 4）

対象は r-e476c11d / `argonauts/r-e476c11d`、AC1〜7 = REQ-15〜21。
本書は実行手順であり合格報告ではない。Builder自己承認不可。OpenSpec task 2.2、画像実閲覧、PM原本読取り、現head CIは実証までpending。
旧 `wordfreq-html-verification.md` の汎用raw/通信/画像契約だけ継承する。旧scope/head/AC1〜6や旧CLIは今回の判定に使わない。

## 1. 開始前のhard gate

- 品質は実profile `argonauts-uat-quality`、Builderは `argonauts-uat-builder`。role引数だけ変えて独立性を偽装しない。各自の実Kanban task/runを使い、環境に渡らない場合だけ現在のkanban_showの実IDを明示する。別run/別rootで実行する。
- 作業branch・PR・HEAD・originを照合し、実行面（製品、tools、tests、設定、未追跡shadow含む）cleanを確認する。品質はcommit/pushしない。
- 変更前基点（driver BASE）は `9eb1e694aafc6cd29f0f7d2a29382764bc1627fb`。baseline採取headは `789cc17267fb4cfeea24111797c3d934c542ce6a`、task t_337d3562/run143、baseline index SHAは `d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089`。これらは現在の対象headではない。
- `.planning/argonauts/r-e476c11d/baseline/` は製品変更前の不変原本。baseline不変：index/hash、12 CLI・18 view・32画像と入力/bytes/argv/envが読めることをsaved_baselineで検査する。元絶対rootは履歴として保存し、別worktreeへのpath解決はvalidator内のメモリ写像だけ。原本を書き換えない。
- `tools/verify_wordfreq_min_count.py`、`tests/test_min_count_verifier.py`、同phase `04-UI-SPEC.md` / `04-VALIDATION.md` / `04-04-PLAN.md`、PLAN-MAPPINGを読む。実source対象は `wordfreq/__main__.py`。
- 既存 `/usr/bin/python3` CPython3.12、PYTHONPATH下のpytest/Playwright/websockets、`/usr/bin/chromium-browser` を使う。browser版/OS/実フォント/描画条件をbaselineと照合する。新install、CI、依存、CSS、DOM、copy変更で救済しない。
- **能力gate**：全full/全tileとbaseline画像を実寸以上又は全域panで実際に開く手段、rawを読む手段、標準添付とPMへの原本配送手段を先に確認する。不能・拒否・環境差なら停止してgaps。台帳を自動readableで埋めない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k saved_baseline -x
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k browser_free -x
```

非0/0 collected/必須skipは失敗。高速feedbackを独立品質と呼ばない。全pytestは次のdriverも自ら実行しsuite.json/xml/stdout/stderrへ実argv/cwd/head/環境/件数/exitを保存する。各stageの開始・終了・所要時間を別記し、未測定を30秒以内としない。

## 2. 公開CLI（4 mode、改名・誤flag禁止）

全例はrepo root。baseline/capture例は**履歴・将来の許可された採取用の構文**であり、今回再実行しない。既存rootや部分原本は再利用/上書き/再採取しない。baselineはBuilder専用、non-baselineは --baseline-dir 必須、finalizeは --review-ledger も必須。--browser/--actor/--session-timeout等の旧driver専用flagを足さない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode baseline --role builder --output-dir .planning/argonauts/r-e476c11d/builder/baseline-example
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode capture --role builder --output-dir .planning/argonauts/r-e476c11d/builder/new-integration --baseline-dir .planning/argonauts/r-e476c11d/baseline
```

品質だけが下記を **tracked background terminal（background=true）** で起動する。fresh root `quality/final-01` とledgerを必ず同時に選ぶ。既存なら両方を新名に変え、部分保存を手修正して継続しない。terminalのsession_idと実PIDを控える。CIを待たない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode review-session --role quality --output-dir .planning/argonauts/r-e476c11d/quality/final-01 --baseline-dir .planning/argonauts/r-e476c11d/baseline
```

### この環境での短いbrowser一時path（人の明示許可）

長いprofile scratchでChromiumのSingletonSocketが失敗する場合、t_e22f75a9の人の回答（2026-11-18 11:08 JST）は本依頼の残りのカードにも、Chromium起動に限る短い `/tmp/aw-*` と使用後削除を許可している。
実在する `.planning/argonauts/t_e22f75a9/run154/authorized_capture_retry.py` を先に読む。このlauncherは無変更のdriverをimportしinstrumented_browser起動時だけTMPDIRを短くし、collection前に環境を復元、終了時にTemporaryDirectoryを削除する。collector/suite/validatorの注入なし。
同条件では上記review-sessionコマンドの **script pathだけをこのlauncherへ置き換え**、実task/runを束縛して起動する。rawや製品の変更、環境変数のprofile偽装は禁止。launcherの実argvと一時path/削除確認も保存する。finalizeはbrowserを起動しないため通常driverのまま。旧guideのsymlink例や全pytestを短いTMPDIRで実行する代案へ変えない。

## 3. ready → 品質本人の全画像/raw/ソース確認

ready:trueと同root manifestのpending-review/session/head/actor/run/task/ready_atを読む。readyは合格ではない。固定期限はready後7200秒、ownerプロセス内だけの有限sessionでありrepo監視サービスではない。中断/timeout/readyなし/非0は未検証。再試行は原因と許可を確認してfresh rootへ、過去headの付替えなし。

driverの実入力matrixは62 CLI、34 HTML×両幅=68 view。下表は独立literal期待値。未指定/1の12 baselineケース×2=24比較を含む。

| 状態 | 条件 | pairs / 元HTML総数 |
|---|---|---|
| baseline同数+10種類超 | 未指定/明示1、全形式、既定text/top10 | 変更前bytes/画像と一致、hello3,zoo2,apple2,one2,two1,b1,c1,d1,e1,f1 / 17 |
| beta beta beta alpha gamma alpha delta | min2、min2/top1、min4 | beta3/alpha2、beta3、空 / すべて7 |
| Zoo apple APPLE zoo banana | min2、min2/top1、逆指定順、min3 | zoo2/apple2、zoo2、同じ、空 / すべて5 |
| Straße STRASSE | min2 | strasse2 / 2 |
| 空・空白・句読点のみ | 有効min2 | 全形式空、HTML総数0 |
| 長語/長basename/CR | long12/既定10/99、未指定/1/2 | w×256が123回、row01〜11が12〜2回、元総数200。basename n×176と連続空白/LF/TAB/CRを保持 |
| 注入候補basename、Café CAFÉ Straße STRASSE 日本語 | 未指定/1/2 | café2/strasse2/日本語1（min2で日本語除外）/ 元5 |

全形式共通pairs、順位1始まり連番、textはcount/TAB/word/LF、jsonはensure_asciiと末尾LF一つ。全除外もexit0、text空/JSON[]+LF/HTML既存0データ行と固定空文言、正total保持。README実例 `python -m wordfreq input.txt --min-count 2 --top 1 --format json` はbeta3だけ、元HTML総数は7。

品質は1280×900と320×900 CSS px、DPR1、zoom100%、fresh contextの**全full/全tileおよび同環境baseline全画像**を実際に開く。fullが縮小されれば実寸以上/全域panも行い全tileを省略しない。scrollbarはcollectorのEmulation.setScrollbarsHidden条件をrawと画像で統一する。自然な縦scroll可、横scroll依存・clip・隣接重複は不可。存在/PNG寸法/DOM一致/scrollWidth単独では可読性合格でない。

raw.jsonの全文字Range（UTF16 offset/全codepoint/空白・ゼロ面積含む）、全祖先のoverflow/box、隣接列・前後行・metadata非重複、computed書体/CDP実font、全数値を画像に対応付ける。横収まり・clipなしを検査し、自身elementの厳格縦包含だけは要求しない。rawをclamp/丸め/削除しない。

| UI truth | 品質が確認する点 |
|---|---|
| UI01 | E1 h1の横収まり・clip/隣接重複なし |
| UI02 | E1 h1全文、24px/600を維持 |
| UI03 | E2 basename/元totalは表上、横収まり |
| UI04 | E2長basename・空白/LF/TAB/CR・total全文 |
| UI05 | E3空/抽出0/全除外の0行と固定copy、元total0/正 |
| UI06 | E3完成stdoutだけ、loading/部分文書なし |
| UI07 | E3使い方exit2/入力exit1、stderr、stdout空 |
| UI08 | E3部分/top後共通pairs・3列・連番・元total |
| UI09 | E3表示制限だけ、補足UIなし |
| UI10 | E3長語/数値の全Range、clip/重複なし |
| UI11 | E3の0/1/複数行でも同じ構造/順位 |
| UI12 | E3長語/順位10〜12/回数123が全文可読 |
| UI13 | E4空文言の自然折返しと横収まり |
| UI14 | E4固定空copy/書体サイズを維持 |

通信canary（clean/failed resource/document navigation/early popup/meta-refresh）で4違反の実試行を観測・拒否したことを読む。成功response0や遮断は無通信の証明でない。open前〜最終flushまでのrequest/failed/navigation/popup、frame/initiator/target/url/outcomeとbrowser-network原本を確認する。初回file文書と外部試行を区別し、背景除外は同一browser_ui等の帰属原本が必要、未知帰属は失敗。検証用loopback debuggerは製品サーバーではない。

品質本人が現headの `wordfreq/__main__.py` をread_fileしdiffと行を記録する。34: casefold済tokens→元counts、35: 元total、36〜37: 別mappingの閾値、38: 既存top_words、44: HTMLへ元total、45〜48: 全形式同じpairs。出力一致だけでfilter→topを証明しない。

## 4. reviews.json → finalize → owner実終了

台帳は実閲覧後だけ記入。top-level request/session/head/actor/root/run/taskはmanifestとexact一致。reviewsは現在とbaselineの**全画像を各一回**、image絶対path、sha256、raw絶対path/raw_sha256、実viewed_at（ready以後/観測終了以前）、scale>=1、extent=[0,0,width,height]、judgment=readable、具体notesを持つ。時刻や可読性を捏造しない。
ac_reviewsは全AC各一件、judgment=acceptedは独立確認後だけ、notesと当該manifest.ac_indexの完全evidence配列を持つ。source_orderは現head/path=wordfreq/__main__.py/SHA/lines=[34,35,36,37,38,44]/judgment=filter-before-top-original-total/具体notes。構造の自動補完は実閲覧の証拠ではない。

生きたsession中だけ次を実行する。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode finalize --role quality --output-dir .planning/argonauts/r-e476c11d/quality/final-01 --baseline-dir .planning/argonauts/r-e476c11d/baseline --review-ledger .planning/argonauts/r-e476c11d/quality/final-01/reviews.json
```

非0は失敗。exit0/finalize-requestedは受付だけ。process_manageで追跡owner実終了とexit0を確認してから、最終manifestをread_fileする。accepted、independent_acceptance=true、errors空、AC1〜7すべてaccepted、verification_finished/observation_end/ended、end_provenanceの同head/実行面cleanを必須とする。ledger_sha256も実原本と照合する。
**全view/全derived** がacceptedで内容全体一致し、全full/tileとreviewed_imagesと台帳のpath/SHA/viewed_atが一対一でexact一致すること。途中derived単独や最上位だけのacceptedは不可。ownerは最終flushと再照合を行う。timeout/保存失敗/遅い通信/未閲覧/未帰属はunverified・gaps。pendingが残るfinalも失敗。

## 5. 全AC索引と配送3gate

manifest.ac_indexの全原本参照に、下表の判断内容と先行RED/GREENを結ぶ。原本request/head/run/actor/root/path/SHAを欠かさない。

| AC | REQ | 実原本・判断 |
|---|---|---|
| AC1 | REQ-15 | 全形式の閾値境界/Unicode/empty、beta/zoo/longのCLI/HTML/raw/全画像 |
| AC2 | REQ-16 | 変更前index、24未指定/1比較、bytes/raw/環境/画像、既定text/top10・同数初出順 |
| AC3 | REQ-17 | suiteの不正0/負数/非整数/非数値/欠落pre-I/O spyと実exit2、有効2の入力失敗exit1、1.2 RED/GREEN |
| AC4 | REQ-18 | casefold→元counts→元total→閾値→topの現ソース行/diff、同数初出順・指定順/独立値、1.3 RED/GREEN |
| AC5 | REQ-19 | beta N2/top1/N4で元7、zoo全除外5、抽出0語0、固定copy、1.4 RED/GREEN |
| AC6 | REQ-20 | 品質本人の全suite/CLI/全画像/台帳/canary/owner最終終了・全view照合、下の3gate |
| AC7 | REQ-21 | 今回baseline→対象headのscope全件、最小README/help/例、source/tokenizer/aggregator/formatter/CSS/copy/依存/CI不変 |

1. **保存gate**：index/manifest/全原本/ledgerと全AC索引を保存する。targetとbaselineのheadを混同しない。全原本を含むtar.gzと索引を作り、SHA-256とrequest/run/actor/root・展開時の相対path/元絶対rootの対応を記録する。baselineと入力/CLI出力/HTML/raw/network/画像/suite、先行RED/GREENへの参照を含める。Builderのrun154原本はhead904e95bの履歴であり後のheadへ付替えない。
2. **標準添付gate**：許可されたkanban_attachに原本（又は原本一式archiveと索引）を渡す。worktree原本の指定はcontent_base64=`argonauts:worktree:<相対path>`。kanban_attachmentsで添付ID/保存名/絶対pathを読み戻し、原本と保存先SHA-256を照合して配送記録へ書く。上限25MBなら原本を複数に分ける。拒否/能力不足を別の外部送信や権限変更で迂回しない。
3. **PM原本読取りgate**：受取PM本人が配送された実入力/argv/exit/stdout/stderr/HTML/raw/画像/閲覧台帳/AC索引を実際に読み、照合hashと読取り結果を自分のカードへ記録する。ローカルpath通知や添付成功だけでは読取り済みでない。PM未読は未達gateのまま渡す。品質実閲覧台帳をBuilderが署名しない。

## 6. head更新・後工程・範囲

headが変わったら文書/OpenSpec記録だけでも**新しいfresh rootで全品質gateを全面再実行**する。古い受入を持ち越さず過去原本のheadを変更しない。品質証拠は添付として保持し、製品/記録の直しはBuilderへ返す。

CI未報告は成功でない。pending/queued/in_progress/不調も成功でない。CI有限回確認、draft PR/同カードレビュー、公式phase検証、OpenSpec公式verify workflow、PM受入、sync/archiveは該当担当カードで行う。存在しないverify CLIを創作しない。待機ループ・CI追加変更なし。

旧phase1/3 staleは別債務。Q-01/Q-02/A-01〜04は非要件、P6並列製品保証を追加しない。今回の製品差分は引数/共通選択と最小READMEのみ、入力元/抽出/全体refactor/新見た目/依存/外部送信なし。本書・contract試験の完成はOpenSpec2.2/AC6/phase全体受入の完了ではない。
