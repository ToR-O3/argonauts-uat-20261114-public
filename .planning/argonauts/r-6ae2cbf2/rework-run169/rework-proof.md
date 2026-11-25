# 08-01 日本語描画の差戻し修正（run169）

## 結果と範囲

日本語が空白になった初回画像を比較基準から外し、既存Windowsフォントを検証プロセスだけから参照して、変更前原本を新規採取した。製品・README・依存・CI・権限は変更していない。表示種類数は未実装のまま、意図的REDであり、製品GREEN・phase合格ではない。

- 受付 r-6ae2cbf2、カード t_b82e2068、標準kanban_showのcurrent_run_id=169。profile argonauts-uat-builder。
- 採取時HEAD: fe0f0b322ff81b687bc8c8314e85614407f1d0c2。報告HEADはreview引継ぎmetadataに分けて記録。
- 新しい比較原本: `.planning/argonauts/r-6ae2cbf2/before-cjk-run169/`。
- index SHA-256: `c82372c9208e91315101f84ce758f5efae7aa2a4a45c78513aa313d945c01c80`。
- 初回 `before/` は上書き・補修していない。index SHA-256は `67ed798db1f5f6ff28a7f57af423ef2f483b83bc206685d4926106640c5e8a55` のまま。以後の製品比較は旧rootではなく新rootを使う。
- provenanceのtask/run欄は子環境で取得できずnullのまま。本書の帰属は標準Kanbanから確認した別記録。新rootも封印後に補修していない。

## 原因と最小修正

`fc-list :lang=ja` は空。`font_probe.py` は実CLIで生成済みの max2 HTMLを320×900 DPR1で開き、日本語h1にNoto Sans JPの実glyphがあることを要求する。

1. fontconfig指定なしで実行：exit1、`Japanese heading has no Noto Sans JP glyphs`。CDPはNoto Sansのみ。`font-probe-without-config.{png,json}`を保存。
2. 既存 `/mnt/c/Windows/Fonts/NotoSansJP-VF.ttf` をfc-scanし、Noto Sans JP・jaを確認。ファイルSHA-256: `5113756f8a3b5d01b2211025e267c50121e3b36f465b7bbaf3cdaf4c3430bfd0`。
3. task-local `rework-run169/fontconfig.conf` はシステム既存設定をincludeし、既存Windows Fonts directoryを参照するだけ。fontファイル自体をrepoへ追加せず、パッケージ導入・共有ユーザー設定の変更なし。config SHA-256: `ecaa4623045d34240f4864be1b733e847d27c44efeaad1a816fd9bdd8f4a7183`。
4. `FONTCONFIG_FILE` と専用scratch `XDG_CACHE_HOME` を検証子プロセスに渡して同じprobe実行：exit0。h1はNoto Sans JP、glyphCount7、isCustomFont=false。`font-probe.{png,json}`に保存。フォントをHTMLへ埋め込む変更、外部font通信はない。
5. 画像入力で子sa-0-5322a5cbが実画像2枚を比較。指定なしでは日本語見出し・ラベル・列名が空白、指定ありでは「単語の出現頻度」「ファイル名」「総出現回数」「集計結果」「順位／単語／回数」を判読。英数字と表も読め、切取りなし。

DOMの文字列・glyphCountだけで描画成功とは扱わず、画像の日本語可読性と合わせて確認した。初回capture-and-red-proof.mdの能力記述を訂正した。

## 再現する環境と実コマンド

repo rootで実行。fontconfig.confはworktree内の原本を用い、FONTCONFIG_FILEはその絶対パス。キャッシュは専用管理scratch（実値はfont-environment.txt）で、共有home設定は変更しない。

```sh
export FONTCONFIG_FILE="$PWD/.planning/argonauts/r-6ae2cbf2/rework-run169/fontconfig.conf"
font_cache=$(mktemp -d "$TMPDIR/fontcache.XXXXXX")
export XDG_CACHE_HOME="$font_cache"
browser_tmp=$(mktemp -d /tmp/ab.XXXXXX)
env TMPDIR="$browser_tmp" TMP="$browser_tmp" TEMP="$browser_tmp" FONTCONFIG_FILE="$FONTCONFIG_FILE" XDG_CACHE_HOME="$XDG_CACHE_HOME" PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_displayed_types.py --mode before --output .planning/argonauts/r-6ae2cbf2/before-cjk-run169
```

新規採取の実TMPDIRは `/tmp/ab.NQr3Dz`。Chromiumの実argv/user-data-dirもこの短いpathを使ったことをcapture-summary.jsonとindexのbrowser.launchで確認。既存rootへ再実行しない。品質は別のfresh rootを指定し、同じfontconfig環境で確認する。後続08-02/08-03もこの新rootと同じフォント条件を使う。旧before/は歴史的整合の検査だけに使う。

## 再採取と実画像の確認

- capture：exit0、stderr空、pending-review、independent_acceptance=false。
- CLI54ケース、HTML18ケース×両幅＝36表示、full36枚＋long狭幅tile2枚＝38枚。
- 1280×900・320×900、DPR1、Chromium148.0.7778.96。入力/argv/exit/stdout/stderr、raw Range/ancestor/style、platformFonts、network、全画像は新indexに保存。
- font-summary.json：36/36のh1でNoto Sans JP・glyphCount>0。raw原本からjqで集計し、座標やfont記録は変更しない。
- clean canary errors空。violating canaryは実resource試行をNetwork.requestWillBeSent/request/requestfailedで捕捉、ネットワーク経路でabort。製品HTMLに通信なし。
- 子sa-0-84832a4fが **新原本8枚**（max2/empty/escape/long、それぞれ1280/320のfull.png）を画像入力で実閲覧。日本語見出し・ラベル・表見出しを判読。emptyは空状態全文、escapeは日本語語、longは日本語basename末尾と折返し、長語と表下端を確認。横切取り・重なりなし。反復n/w文字の完全同定は目視だけでは困難で、raw/CLI byte oracleで補う。
- 上記8枚以外の30枚をBuilderが実閲覧したとは主張しない。全38枚の独立品質閲覧と変更後比較はpending。collectorのreviewed_imagesを後から書き換えない。
- 全54 stdoutを旧採取とcmpし、HTML/text/json全て同一bytes。実行前後の製品/README diffは空。新採取時のproduct hashesもGitの採取headと照合済み。

## 検証とRED再確認

| 実コマンド（PYTHONPATHと/usr/bin/python3指定） | 実結果 |
|---|---|
| tools/verify_wordfreq_displayed_types.py --mode validate-before --output 新root | exit0 / cases54 / pending-review |
| pytest tests/test_displayed_types_verifier.py -q（新rootを指し、旧rootの整合も追加） | exit0 / 18 passed in2.40s |
| pytest tests/test_max_count_verifier.py -k saved_baseline -q -x | exit0 / 1 passed,53 deselected |
| pytest tests/test_formatters.py::test_html_displayed_types tests/test_cli.py::test_displayed_types_cli_matrix -q --junitxml=…/new-feature.xml | exit1 / 41 failed in4.04s |
| pytest -q --junitxml=…/full.xml | exit1 / 42 failed,1065 passed in204.52s |

pytest stdout/stderr/JUnitは同directoryの new-feature.* と full.*。新機能41件のAssertionErrorは表示leaf/countの欠如。全suiteの残る1失敗は `test_complete_fixed_css_contract_is_static_not_browser_acceptance` が新しい局所2規則を期待するため。collection/import/setup ERRORではなく、品質run168で確認済みのREDと同じ範囲。新旧原本検証1件を足したため全suite成功数が1064から1065になった。製品GREENを報告しない。CIの旧head fe0f0b3にはpytest failureが2件（45700693104、45700604653）あることを実APIで確認。新pushのCIは別途1回読み、未報告を成功にしない。

## 後続へ

- testsのBEFORE定数は新rootへ切替。旧rootは追加のread-only整合テストで保全。下流のドキュメントでbefore/を参照する箇所は新比較rootを使うこと。
- OpenSpec1.1のみ。製品/README編集、OpenSpec1.2/2.1は次のPLANへ残す。
- 公式位置はPhase8/Current Plan2/Total3/Ready to executeのまま。08-01 SUMMARYのある差戻し修正であり、advance-planを重ねない。
- WR-01〜04/IN-01〜04は提案扱い。今回の必須差戻しは日本語描画と新原本・記述訂正だけに限定し、driver設計の追加変更はしない。
- 学習候補：画像能力probeはASCIIだけでなく対象言語のpixelsを確認する。japanese-browser-evidence skill作成は承認待ち（pending7eccd162）であり保存済みとは主張しない。
