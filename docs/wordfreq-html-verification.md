# wordfreq HTML のブラウザ証拠

## 検証対象headと環境

製品は標準ライブラリだけの静的HTML。検証でも依存・lockfile・CIを追加変更しない。サーバー、製品script、対話操作、生成日時、テーマ切替は追加しない。

既存 `/usr/bin/python3`（CPython3.12）と環境側のpytest/Playwright/websocketsを `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages` から使用する。通常pytestはブラウザをimportしない。`--browser` の既定は `/usr/bin/chromium-browser`。不足時はinstall/skip-to-passせず未検証で止める。

ChromiumのUnix socket名がmanaged scratchの絶対パス長を超える環境では、repo rootで下記を一度実行する。既存の別物を上書きしない。`.browser-tmp` はcommitしない。system /tmpへ逃がさない。

```sh
ln -s "$TMPDIR" .browser-tmp
export TMPDIR=.browser-tmp
```

すべてrepo rootから実ファイルを実行する。開始時のhead/status/product diff、未追跡製品コードの内容/SHAをprovenance.jsonへ保存する。製品/tools/tests/pyprojectと、ルートのconftest.py・pytest.ini・tox.ini・setup.cfgのdirtyは、未追跡・変更・staged・削除を含め拒否する。scope.jsonはplanning-start baseline **5a7659b949dc118b59cea5ef3eb40bcd94337d8d** と毎回解決したHEADを比較する。承認済03-02の製品snapshotからの変更、CI/依存/tokenizer/source/履歴Phase1/別依頼Phase2の変更は拒否する。旧語昇順から正規化後初出順への置換は承認済の意図した差分であり、取り消さない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --check-evidence-contract
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --check-scope
```

contractの結果はsynthetic predicate only。製品の画像閲覧・受入を表すものではない。scopeのJSONにはbase/target/全path/製品差分/errorsを残す。

## 独立検証証跡と起動

Builderはqualityとして実行しない。品質は自分のKanban run・実際の `HERMES_PROFILE=argonauts-uat-quality` で対象headを取り、自分のfresh root・入力原本から再生成する。`--role quality` だけで独立性は成立しない。actorは実Profileと一致しなければならず、rootのpath componentはquality（builderのrootと混在不可）。Profile環境はローカル単一利用者の帰属補助であり、悪意あるOS利用者に対する認証ではない。品質のカード・実行者・再生成原本と合わせて独立性を確かめる。`--actor`省略時は実際の`HERMES_PROFILE`を使い、指定した場合も実Profileとroleの一致を要求する。台帳の全フィールドをmanifest.jsonからスクリプトで埋めること自体は防げず、形式検査は実閲覧の証明ではない。これは信頼するローカル実行者の自己申告という限界であり、品質は画像を実際に開いて記録する義務を負う。

同じrootを再利用しない。既にある場合は新しいquality配下のrootを選び、以下のrootとledger両pathを同時に変える。終了済captureは後からlive観測済みへ昇格できない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/new-capture --mode capture
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality-network --self-test-network
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --actor argonauts-uat-quality --output-dir .planning/argonauts/r-50053edc/quality --mode review-session --session-timeout 3600
```

review-sessionは **tracked background** として開始する（Hermes terminalのbackground=true）。プロセスID/terminal session_idを控える。stdoutの `ready:true` と、同じrootのmanifest.jsonの `verdict:pending-review`・ready_at・sessionを確認してから画像を読む。readinessを合格と呼ばない。起動中はfull pytest（suite.xml/JSON/stdout/stderr）、独立した新canaries/、全CLI、全22 browser viewsを実行する。準備完了後の待機は最大3600秒、上限7200秒。時計/周期によるrepo監視サービスではなく、この検証プロセス内だけの有限の台帳完了待ちである。

プロセスが途中で終わったら非0終了とmanifestの理由を読み、未検証のまま新rootでやり直す。画像ツールが無い/全画像を読めない場合も、架空のレビューを作らない。pendingのままtimeoutするとexit1/unverifiedになる。

## 固定入力・コマンド・原本

15 CLIケースは `empty`、`normal-1`、`normal-2`、`normal-10`、`frequency`、`tie-text-1`、`tie-text-2`、`tie-json-1`、`tie-json-2`、`tie-html-1`、`tie-html-2`、`long-12`、`long-default`、`long-99`、`injection`。HTML11ケースは **1280×900 / 320×900 CSS px、DPR1 / 100% zoom**、各fresh contextで開く。期待値は製品関数でなくfixed_cases()の明示原本から作る。

- normal本文 `zoo apple zoo banana apple cherry` は総数6、top1/2/10でzoo2 / zoo2,apple2 / zoo2,apple2,banana1,cherry1。
- frequency本文 `beta beta beta alpha gamma alpha delta` は総数7、top2はbeta3,alpha2。tie本文 `Zoo apple APPLE zoo banana` は全形式top1/2がzoo2 / zoo2,apple2。順位は表示行の1始まり連番。
- emptyはbasename/総数0/3見出し/tbody0行と固定補足文。空text/JSON、単語1件、不正top・format・引数個数、読込/permission/decode、Unicode抽出/casefold/入力境界はsuiteの実CLI/部品試験へも対応付ける。
- long語はw×256。basenameは `集計` + space2 + n×176 + 実LF + `続き` + 実TAB + `終わり` + space2 + `&<>"'.txt`。本文はL123回、row01〜11を12〜2回、space区切り末尾LF、総数200、top12/既定10/99。nとwの非空白連続部が両幅で複数行になること、順位10〜12/count123が欠けず同一行になることを確認する。
- injection basenameは `検査` + space2 + `&<>"'` + 実LF + `次` + 実TAB + `終.txt`。本文 `Café CAFÉ Straße STRASSE 日本語` はcafé2,strasse2,日本語1、総数5。直接のタグ風語escapeはformatter suiteでも検証し、tokenizerは緩めない。

各case/cli.jsonにinput/basename_repr/独立pairs・total/argv/cwd/executable/environment/exit/stdout/stderrを保存する。入力原本、stdout生bytes（HTMLはstdout.html）、stderr.binを保持。strict UTF-8、全HTMLの親path非埋込み、タグ/属性/CSSの静的監査とDOM値を確認する。HTMLを手修正/テンプレート貼付けして代用しない。

## rawRange・幾何・全画像の実閲覧

各case/widthのraw.jsonはelement/full text/全codepointのRange（空配列含む）、UTF16 offset・文字位置、元の浮動小数、全祖先のoverflow/box/border/padding/client/scroll、computed書体とCDP実使用platformFonts、viewport/scroll座標系を保持する。td/th/h1/caption/label/メタ値/空補足文に文字record・全文一致を要求。非空白文字は正面積Rangeを必須とする。ゼロ面積/空白矩形は原本から削除しない。

横方向viewport/列内収まり、ownerを含む実clip祖先内収まり、異なるテキスト間の正面積重複を検査する。隣接edgeが接するだけは重複ではない。**自身のelement縦矩形を越えるだけでは失敗にしない**。clamp/丸め/矩形補正で通さない。basenameの連続space/LF/TAB位置、break-spaces/tab-size4、長いn/wの折返し、全数値をrawと画像で突き合わせる。

全full.pngと全tileを画像閲覧ツールで実際に開く。full画像が縮小されるなら実寸表示または全領域を読めるpan/zoomで確認し、さらに全tileも読む。CDP captureBeyondViewportはviewportをresizeしない。全画像のPNG実寸/SHAと座標をmanifestに記録する。高さ900超は800刻み・最大900高の重なりtile、全域の穴・下端欠落を拒否。存在/寸法/DOMだけで閲覧済みにしない。罫線/隣接行に重なった文字、切取り、判読不能は不合格。

## reviews.json の外部台帳

collectorが作る台帳はreviews/ac_reviewsとも空。品質が実閲覧した後にだけ書く。全full/tileそれぞれに次のfieldを必須とする。

| field | 型と契約 |
|---|---|
| `actor` | string、実品質Profile。別actor不可 |
| `image` | string、manifestの絶対pathと完全一致 |
| `sha256` | string、閲覧画像のSHA-256 |
| `viewed_at` | timezone付きISO8601 string、ready_at以後・live観測終了以前の実閲覧時点 |
| `scale` | number、1以上（実寸以上で全文を読んだ尺度） |
| `extent` | number[4]、画像座標[0,0,実幅,実高]を全て閲覧 |
| `raw` | string、対応raw.json絶対path |
| `raw_sha256` | string、実際に確認したrawRange原本のSHA-256 |
| `judgment` | string、全文可読を確認した場合のみreadable。Boolean不可 |
| `notes` | string、当該画像とrawで確認した具体的可読性・空白・罫線等。空不可 |

台帳top levelはsession/head/actor/rootがmanifestと一致、reviewsは全画像を重複なく列挙する。ac_reviewsはAC1〜AC6を各1件、ac/judgment/notes/evidenceを必須とする。judgmentは独立確認後だけaccepted、notesは具体的根拠、evidence配列はmanifest.ac_indexの該当ACの完全なpath配列（省略しない）。時刻を後から作ったり未閲覧画像にreadableを書かない。

以下は**非受入の形の例**のみ。実ファイルへコピーして合格にしない。実寸/時刻/hash/path/判定は実閲覧から採る。この例は必ず拒否される。

```json
{
  "session": "NON-ACCEPTANCE-EXAMPLE",
  "head": "not-a-head",
  "actor": "not-a-reviewer",
  "root": "/non-acceptance",
  "reviews": [{
    "actor": "not-a-reviewer",
    "image": "/non-acceptance/full.png",
    "sha256": "not-a-hash",
    "viewed_at": "not-a-time",
    "scale": 0,
    "extent": [0, 0, 0, 0],
    "raw": "/non-acceptance/raw.json",
    "raw_sha256": "not-a-hash",
    "judgment": "unverified",
    "notes": "実閲覧していない例"
  }],
  "ac_reviews": []
}
```

## 通信・帰属・観測区間

observerはopen前にcontext request/response/requestfailed/requestfinished/page/frame/popupとmain CDPを購読する。さらにブラウザflatten CDPで新targetをpauseしNetwork/Pageをenableしてresume。初回file読込、失敗試行、遷移未commit/early popup/client redirectを残す。各Network requestIdはsource/sessionId/targetId/requestIdで同一channelのrequestWillBeSentに対応必須。url/request.url/response.url/redirectResponse.url/documentURL/frame.url/targetInfo.urlを検査。DOM/CSS enableはabout:blankで行い、DevTools孤立再取得を除外しない。

全22 context/page/listenerを実画像閲覧とfinalize/flush終了まで保持する。他context除外はbrowserContextId原本で証明できる場合だけで、excluded_other_contextsにevent・target・理由を残す。未知target/eventや帰属不明通信は失敗。全ブラウザ原本browser-network.jsonも保持する。ブラウザ背景除外はopen前の同一browser_ui targetId、openerなし/canAccessOpener=false、既知omnibox chrome:// URLという根拠だけ。一般的な「背景だから」は不可。

成功response0/遮断だけで無通信としない。canaries/はclean、failed-resource、document-navigation、early-popup、meta-refresh redirectを実行し、全4違反の実requestと対応失敗を観測して拒否した場合だけpassed。予約.invalid:9へのERR_UNSAFE_PORTも実試行として記録する。HTTP30x成功検査を実施したとは称さない。loopback debuggerは検証transportであり製品Webサーバーではない。

## finalize・検証verdict・決定論的再実行

台帳を実閲覧から完成し、**sessionが生きている間**に下記を実行する。終了capture/PID再利用/別root/別actor/dirty/head変更/欠損原本/空台帳/重複画像・AC/観測欠落は拒否する。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --actor argonauts-uat-quality --output-dir .planning/argonauts/r-50053edc/quality --mode finalize --review-ledger .planning/argonauts/r-50053edc/quality/reviews.json
```

finalizeは台帳・artifact/hash・AC・head/status/scope・canary・suite・直近のnetwork snapshotを検査してrequestを出すだけ。`finalize-requested`/exit0は最終合格ではない。live ownerは全listenerをflushし、台帳hash/sessionを再照合、最新の通信区間を含む全検査を繰り返す。検査後にもflushし、遅い外部/未帰属試行を失敗にする。最後のsnapshotまで観測を保持し、contextを閉じてから最終manifestを保存する。

追跡したbackground processの終了をprocess_manage waitで読み、**exit0と最終manifest accepted/independent_acceptance=true、AC1〜AC6全accepted、errors空、verification_finishedとobservation_endとended、end_provenanceのhead一致・product_status空**を確認する。finalize単体の戻り値で止めない。Builderが自分の実閲覧を完了した場合もbuilder-reviewedにしかならない。captureは常にpending-review、timeout/環境不足/未閲覧/失敗はunverified・exit1。headが変われば全証拠をfresh rootで再生成し、前の結果を流用しない。

品質は全suiteと全画像/rawと各ACを自分で確認し、原本を保全してAC索引・台帳・head/diff・通信記録を添付する。任意のPYTHONHASHSEEDで全試験を再実行し、実argv/環境を保持する。未実施条件を合格に変換しない。

## 最終全view照合（G1）

`finalize-requested` は受付だけなので、tracked background のlive ownerの実際の終了を待ち、exit0を確認する。最終 `manifest.json` が **completion marker** であり、derived.json単独や途中のpartial saveを成功として読まない。公開中はmanifestをunverified/independent_acceptance=falseで保存し、全derived保存と整合gateの後にだけ最終markerを最後に置く。中断・再起動時にmarkerがunverifiedなら、途中のderivedに判定があっても全体は未検証。既存rootを再開・手修正せずfresh rootで再生成する。

- `cases[].views[]` の全ケース・全幅を正規順で走査し、各 `derived.json` とviewの内容全体を一致させる。最上位だけacceptedでは不足。
- 各viewの `images` 全full/tileと `reviewed_images`、`reviews.json` の画像集合を一対一で突き合わせる。path/sha256/viewed_atを台帳から正確に保持し、欠落・余計・重複・空mappingを拒否する。台帳の列挙順が違っても画像identityと正規view順は変えない。
- qualityは全view/derivedがaccepted、Builderは全てbuilder-reviewedかつindependent_acceptance=false。最終manifest/derivedのどこにもpending-reviewが残らず、AC1〜AC6判定・ledger_sha256・原本raw/画像bytesも一致すること。capture中のpending-reviewは正常だが、finalのpendingは不合格。
- timeout、例外、無効ledger、遅い通信、head/dirty変更、保存・照合失敗は全view/derivedをunverified、reviewed_images=[]、AC判定unverifiedへ戻しexit1。raw/画像/ledger原本は変更しない。storage自体が利用不能なら完全なrollbackを保証できないため、stdoutのpersistence診断と非0終了を保持し、保存完了を主張しない。
- synthetic lifecycle regressionは画像を見た証明ではない。no-op/zero-test（0件収集）の結果を成功としない。G2のfull suite/既存CIとfresh final-head独立品質は03-06へpendingで引き継ぐ。OpenSpec3.1/3.2/4.1/4.2は先にチェックしない。

## G2: encoding・shallow・実行帰属の分離

- `tests/fixtures/encoding_cli_probe.py` は **controlled-seam-not-native-locale** とsidecarへ記録するテスト専用launcher。raw byte E9を含む実ファイルを実FileSource/mainで開き、表示用filesystem encodingとstdout TextIOWrapper encodingだけを制御する。raw argvのos.fsencode往復、元入力bytes不変、café、全行/総数/日本語見出し、保存HTMLのstrict UTF-8 bytes一致を無条件に確認する。これはOS localeを変えた証拠ではない。
- `native ISO-8859-15` は `locale -a` で実在したhostだけで追加実行する。PYTHONUTF8=0/PYTHONCOERCECLOCALE=0、`locale charmap` のISO-8859-15とstderr空を必須とし、不一致は失敗。native不在はその旨を記録するがcontrolled byte義務をskipしない。通常の `-m wordfreq` とC locale/PYTHONIOENCODING=latin-1も実行する。availabilityの両分岐は決定論的回帰、native実行は実host測定と区別する。
- scope単体試験はfixture所有の実git repositoryとfile:// depth1 cloneを使用する。実scopeのbase **5a7659b949dc118b59cea5ef3eb40bcd94337d8d** と `approved_product` **ed7e6cc9d608bc40a82da76e85ca6e57a0808b54** は変えない。両方をcommit objectとして先に解決し、欠落時はJSONの `ref_diagnostics` / exact requested IDs / target / errorsとexit1 / verdict unverifiedを読む。未取得diffはnullであり空のclean一覧ではない。fetchやHEADへの代替をしない。fixture成功は実exact-ref scope成功を意味せず、実参照不足は品質の実行blocker。
- provenanceは既存code/configに加え、pytest既定収集の全 `test_*.py` / `*_test.py`、全階層conftest.py、root `pytest.py` のimport shadowを同じpath selectionでstatus/diff/untracked content+SHAへ記録する。tests/外でもmodified/staged/deleted/untrackedは拒否。独立fixture subprocessのcollect-only/root shadow制御で実影響を示すが、この作業repoでは制御コードを実行しない。ignored cacheと生成.planning証拠はcode扱いしない。
- `--actor`省略でもreview-sessionが保存したmanifest.actorは実HERMES_PROFILE。roleや出力rootとの一致は必須。finalizeは別actorのmanifestを非0で拒否し、finalize-request.jsonを生成しない。profileの単体解決だけでなく保存manifestの回帰を実施する。

## 同カードの品質→Builder記録→最終head再品質

この節は**最後の実装03-06カードそのもののレビュー**の義務であり、後続PMへの曖昧な依頼ではない。品質は製品/OpenSpecを編集しない。

1. **H1**: Builderは修正コード・試験・実施事実のみpushし、OpenSpec原本 **3.1/3.2/4.1/4.2** は未チェックでrequest_reviewする。Builder自身のgreenやsyntheticテストは独立合格を表さない。
2. 品質はpush先/PRのH1を照合し、03-06-PLANのindependent_quality_gate全文をfresh quality rootで実施する。全suiteと実exact-ref scope、fresh入力・全CLI・全canary・全22 views、両幅の全full/全tileの可読倍率実閲覧と全rawRange監査、open前から閲覧/live finalize/flush終了までの通信帰属、AC1〜AC6を確認する。ownerの実exit0後、manifest/全derived/ledgerのexact image path/hash/viewed_at集合が全て一致し、全view/全AC accepted、independent_acceptance=true、pending無し/errors無し、final provenance/head一致を読む。
3. 同じheadの既存CI run/jobs/logを有限回だけ読み、結論と実試験結果を記録する。未報告/queued/in_progressは成功ではない。待機ループ、CI編集、local成功による代用は禁止。技術条件が未達ならrequest_changesで具体的に返す。
4. 技術合格でも原本記録が未完なら品質は **request_changes**。独立報告と標準添付へ **head/path/hash** とtask別根拠（3.1:両幅表示、3.2:全raw/画像、4.1:独立全AC/通信、4.2:全suite/実scope/同head CI）を書く。Builderは今回添付と未達無しを照合し、満たした事実だけtasks.mdへ証拠付きで記録しチェックする。CI/browser/原本等が不足なら該当taskは未チェックで修正/blockし、架空の完了を書かない。
5. **H2**: Builderは記録更新をpushし **re-request_review**。文書だけのheadでも品質は新rootで手順2/3の**全gateを全面再実行**する。H1の合格をH2へ持ち越さない。追加 **H3** も同じ。品質証拠は添付として保持し、検証headを黙って変更しない。
6. 最終headの独立品質・CI・OpenSpec公式verify workflowの **critical0**（未チェックtask無し）がそろうまで承認しない。導入済み公式status/apply instructions/strict validationとverify workflowを使い、不存在の `openspec verify` CLIは作らない。次のphase検証はこの結果の後に正式実行する。archive/sync/mergeはこのPLANでは行わない。

## AC証拠の索引とpending gate

manifest.ac_indexはACごとに全CLI原本/全幅raw・全画像・network・suite・canary・scope/provenanceを結ぶ保守的な完全索引。各ACの独立判定で見る点は下記。

| AC | 要求・確認する内容 |
|---|---|
| AC1 | REQ-09、1枚UTF-8/3列/内包CSS/静的外部経路なし + failed試行を含む通信原本 |
| AC2 | REQ-10、basenameだけ/上配置/親path不在/top前総数6・7・0・200/default/oversized |
| AC3 | REQ-11、全形式の回数降順・正規化初出順・top・後の再出現・連番 |
| AC4 | REQ-12、lightのみ、両幅全文/空白/複数桁/raw/clip/非重複/全画像実閲覧 |
| AC5 | REQ-13、escape/注入/strict UTF8/既存Unicode・casefold・入力境界・error/空text-json回帰 |
| AC6 | REQ-14、品質のfresh対象head再生成・全試験・全artifact/actor/区間/現head/scope整合 |

REQ-09/REQ-10のunclassified2件（EDGE-01/02 flagged_assumptions）は原本どおり未解決で保持する。上の具体AC試験と独立gateで扱うが、分類を自動解決済みにしない。BuilderのSUMMARY/ツール完成は独立品質やphase受入の完了ではない。OpenSpec4.1本体と全画像を必要とする3.1/3.2/4.2は品質が実際に満たすまでpending。
