# wordfreq HTML のブラウザ証拠

## 環境

製品は標準ライブラリだけで動く。以下は既存のローカル検証環境を使い、プロジェクト依存・lockfile・CIを変更しない。

- `/usr/bin/python3`：CPython 3.12。既存pytest/PlaywrightとWebSocket transportは `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages` から読む。通常pytestはブラウザ関連パッケージをimportしない。
- `--browser` の既定は `/usr/bin/chromium-browser`。実行版・OS・起動argvを証拠へ記録する。フォントはcomputed値に加え、CDP `CSS.getPlatformFontsForNode` の実使用結果をrawへ保存する。
- 不足するパッケージ・ブラウザ・プロトコルは非0終了。install、代替の架空記録、skip-to-passは行わない。
- ChromiumのUnix socket名には長さ制限がある。この環境の絶対TMPDIRでは起動が `Socket path too long` で失敗した。repo root内にmanaged scratchを指す短い相対symlinkを作り、同じscratchを短い名前で参照すれば起動できた。製品/依存の変更ではない。新しいworktreeで必要なら、rootから以下を一度だけ実行する（既存の別物を上書きしない）。

```sh
ln -s "$TMPDIR" .browser-tmp
export TMPDIR=.browser-tmp
```

`.browser-tmp` はcommitしない。実体はmanaged scratchであり、system `/tmp` は使用しない。証拠は指定output-dirへ書く。

## 起動

必ずrepo rootから、実在するファイルを起動する。`--output-dir` は毎回空の新しい場所を指定する。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x

env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/new-capture --mode capture

env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/new-canaries --self-test-network
```

`--role quality` も採取に使えるが、role名だけで独立品質合格にはならない。品質は対象headで自分の新しい出力先・入力原本から再生成する。`--mode review-session` と `--mode finalize` は03-03では未実装で、明示的に失敗する。live画像閲覧/最終化/台帳は03-04の範囲であり、終了したcaptureを後からlive観測済みと読み替えない。

## 固定入力と原本

`fixed_cases()` は製品の集計・整形関数を使わず入力と期待値を定義する。計15 CLIケース：empty、normal top1/2/10、frequency top2、normalized tie top1/2をtext/json/htmlで、long top12/既定/99、injection。HTML11ケースをそれぞれ1280×900と320×900 CSS px、新規context、DPR1/zoom100%で開く。

longの語はw×256。basenameは `集計`+space2個+n×176+実LF+`続き`+実TAB+`終わり`+space2個+`&<>"'.txt`。L123回、row01〜row11を12〜2回の順、space区切り、末尾LF、総数200。injectionのbasenameは `検査`+space2個+`&<>"'`+実LF+`次`+実TAB+`終.txt`。本文 `Café CAFÉ Straße STRASSE 日本語` はcafé2/strasse2/日本語1、総数5。

各caseに入力原本、制御文字を可視化したbasename_repr、独立期待値、exact argv/cwd/executable/環境、exit、stdout原バイトとstderrを保存する。HTMLは実CLI stdoutそのものでstrict UTF-8として照合する。basename/total/headers/全行のDOMと静的tag/attribute/CSS監査、ディレクトリ情報不在を検査する。text/jsonも明示期待値と比較する。

開始と終了のhead/status/diffを保持する。追跡/未追跡の製品・tools・tests・pyproject変更がある場合は、診断を保存して帰属付きcaptureを拒否する。未追跡コードの内容・SHA-256も診断に残す。計画文書・生成証拠の変更はstatusに残すが、製品変更と混同しない。

## raw geometryと判定

各case/widthの `raw.json` は元の浮動矩形、全文Range、全codepointのRange（空配列を含む）、UTF-16開始/終了offset、codepoint位置、全文テキスト、全祖先のoverflow/box/border/padding/client/scroll情報を保持する。JSはディスクからautomation APIへ読み込み、製品HTMLへscriptタグを追加しない。座標系はviewport CSS px、採取時scrollを併記する。

`derived.json` はrawと別の判定。横viewport/列収まり、ownerを含む実切取り祖先のpadding clip、異なるテキストノード間の重なり、長いn/w連続部の複数行化、break-spaces/tab-size4、数値の全文/各桁を検査する。隣接列・行・メタ情報・captionを同じ文字矩形比較に含める。要素自身の縦矩形を越えただけでは失敗にしない。浮動値や空Rangeを丸め・clamp・削除して合格へ寄せない。clip領域の導出値はraw border/client原本とは別フィールド。

全ページ画像を保存し、高さ900pxを超える場合は800px刻み・最大900px高の重なり付きtileも保存する。索引に全画像pathと座標範囲を残す。**存在・寸法・幾何だけでは画像を読んだことにならない。** `reviewed_images` は空、可読性/画像閲覧は常にpending。

## 通信観測

製品文書を開く前にcontext全体のrequest/response/requestfailed/requestfinished、page/frame/popup、main page CDP Network/Pageを購読する。それより前にブラウザ階層の公開flatten CDPを接続し、Target auto-attachで新targetをpause、Network/Pageをenableしてからresumeする。早いpopupの最初の要求にもrequestId・initiator・frameId・targetId・sessionId・URL・失敗結果が残る。Playwrightのブラウザ階層非flatten方式は実機で拒否されたため使わない。

CDP transportはChromiumのloopback debuggerであり、製品Webサーバーは起動しない。既存 `websockets` を明示ブラウザ操作時だけimportする。起動argvは背景機能/拡張を減らすが、**通信を遮断したことや成功response0を安全の根拠にはしない**。

raw `network.json` に初回file読込みを含む全観測イベントと開始/終了時刻を残す。失敗・遷移未commit・popupでも外部/予期しないURLの試行は不合格。未知event、帰属できないrequest、初回local request欠損、observer coverage不足は未検証/失敗。

例外は、文書open前に生成/attachされたChromium `browser_ui`、opener無し、canAccessOpener=false、既知のomnibox chrome:// URLという原本がある**同一targetId・同一URL**だけ。page型や文書open後の新targetへこの除外を広げない。根拠イベントも削除せず保持する。一般的な「背景通信だから除外」はしない。

## negative canary

検証用の隔離ページだけでclean、failed-resource、document-navigation、early-popup、meta-refresh redirectを実行する。製品HTMLは改変しない。送信先は予約済み `.invalid` のport9で、このChromiumではERR_UNSAFE_PORTとなる。serverは不要。HTTP30xの成功応答を作る検査ではなく、実際のclient redirectと遷移試行の検査である。

self-testのexit0はclean controlが通り、全4違反の**実要求と対応する失敗を観測して拒否した**場合だけ。コマンド自体の例外、空イベント、別の要求の失敗、未pauseのpopup、観測欠損では成功しない。各違反で成功外部response0でもrequestfailed/CDP loadingFailedが残ることを実測する。`canaries.json` と各原本JSONが証拠。任意のprotocol不足は非0で止まり、対応できたと推定しない。

## pendingと独立品質gate

captureのexit0とmanifest `pending-review` は「採取・自動判別が終わった」の意味だけ。観測区間はcapture-onlyであり、画像を実際に閲覧する後続の時間を含まない。全画像可読性、rawRange/空白/祖先の品質による確認、live観測の終了処理、AC1〜AC6別の独立判定は未完了。OpenSpec4.1をこの結果で完了にしない。
