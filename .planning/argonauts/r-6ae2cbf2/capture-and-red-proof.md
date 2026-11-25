# 08-01 変更前原本と先行RED

## 実施範囲と帰属

- 受付 r-6ae2cbf2、カード t_b82e2068、標準Kanbanの実行run 167、profile argonauts-uat-builder。
- 採取・RED実行時HEAD: be231840989079fed532c7372efb66f577e39b09。製品 wordfreq/*.py と README.md は一切編集していない。
- terminalの子環境にはHERMES_KANBAN_TASK/HERMES_KANBAN_RUN_IDが渡っておらず、変更前のprovenance.jsonとREDのcommands.jsonは該当欄がnullのまま保存した。これらを後から書き換えていない。本書のカード/runは標準kanban_showのcurrent_run_id=167と当カードのworkspaceから照合したworker側の帰属記録であり、子環境から採れた値ではない。
- 作業場所・Python・profile・実コマンド・環境・製品とdriverのSHAは各原本に保存。採取HEADと後の報告commitは別物で、報告HEADはレビュー引継ぎmetadataに記録する。

## ブラウザー能力の初手確認

既定のplaywrightコマンドはPython importに失敗。指定済みの `/usr/bin/python3` と `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages` ではPlaywright 1.60.0を確認した。標準ブラウザーの保存先には実行ファイルがなくscreenshotが失敗したため、既設 `/home/Yuki/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome` を明示。依存の導入・更新はしていない。

probe/browser_probe.py は実CLIでREADME.mdから生成したHTMLを320×900/DPR1で開き、Chromium 148.0.7778.96とtitle「単語の出現頻度」を返してexit0。probe/launch.pngを画像入力で実閲覧した子sa-0-4d06d912は、白背景・README.md・総数404・10行の表（sh/readme/result等）と判読可能な文字を報告した。能力確認のみで、製品の受入合格ではない。

端末からの起動は自身の `mktemp -d /tmp/ab.XXXXXX` による短い専用パスをTMPDIR/TMP/TEMPへ同一コマンドで渡した。変更前採取の実パスはbefore/provenance.jsonの `/tmp/ab.iaPDXe`。Chromiumの実argv/user-data-dirはindex.jsonのbrowser.launchに保存され、子へ短いパスが渡ったことを確認できる。

## 変更前採取

実行コマンド（browser_tmpにはmktempの実出力を代入）:

```sh
env TMPDIR="$browser_tmp" TMP="$browser_tmp" TEMP="$browser_tmp" WORDFREQ_DISPLAY_CAPTURE=before PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_displayed_types_verifier.py::test_capture_before_real_browser -q -s
```

結果: exit0、1 passed in 27.07s。

- before/index.json: pending-review、independent_acceptance=false。
- 実CLI54ケース（18入力条件×HTML/text/json）、HTML18ケースを1280×900・320×900、DPR1で描画。36表示、full36枚＋長い狭幅ページのtile2枚＝38画像。
- 各入力原本、正確argv、exit、stdout/stderr、HTML、raw文字Range/祖先/CSS/実font、network観測、full/tileはindexから追跡する。
- clean canary: errors=[]。violating canary: 外部resourceへの試行をNetwork.requestWillBeSent/request/requestfailedで捕捉し拒否。canaryだけネットワーク経路でabortし、製品HTMLには通信もscriptも追加していない。
- 原本の画像台帳は未閲覧のまま。collectorは閲覧済み・独立受入を偽装しない。品質は変更後とともに全比較画像を実閲覧する。
- before/index.json SHA-256: 67ed798db1f5f6ff28a7f57af423ef2f483b83bc206685d4926106640c5e8a55。
- 封印後にbefore/を編集・再採取していない。以後のvalidator改良は現在のtoolだけで、保存時のdriver hashは採取HEADのGit内容と照合する。

## 非ブラウザー検証

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_displayed_types_verifier.py -q
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k saved_baseline -q -x
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_displayed_types.py --mode validate-before --output .planning/argonauts/r-6ae2cbf2/before
```

最終結果: 17 passed in 2.19s、旧封印baselineは1 passed/53 deselected、validate-beforeはexit0/pending-review/cases54。

tool作成前の試験は11 failed/3 passed（API欠如の開発RED。製品の機能REDには数えない）。inventory削除変異は1 failed（DID NOT RAISE）を実測し、全artifact一覧の完全一致検査追加後は拒否成功。既存root/所有中root、欠損、改変、出所不一致、viewport/DPR不一致、synthetic、collecting、中断、capture時製品hash不一致も拒否する。これらの変異・中断はsynthetic controlであり、実ブラウザー受入の代わりではない。

## 製品の先行RED（OpenSpec 1.1のみ）

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tests/test_cli.py --record-display-red .planning/argonauts/r-6ae2cbf2/red
```

recorder自体はexit0（記録成功）。内部のpytestは両方exit1:

| 実コマンドの対象 | 結果 | 原本 |
|---|---|---|
| test_html_displayed_types と test_displayed_types_cli_matrix | 41 failed in 4.09s | red/new-feature-stdout.bin、stderr.bin、new-feature.xml |
| tests/test_formatters.py tests/test_cli.py | 42 failed, 658 passed in 64.37s | red/focused-stdout.bin、stderr.bin、focused.xml |

正確argv/cwd/Python/env/exitはred/commands.json。formatter1件とCLI40件は `missing unique displayed-types leaf` / `missing displayed-types count` によるAssertionError。追加でCSSの完全辞書照合1件が新しい局所2規則の欠如により失敗。collection/import/setup ERRORではない。40通りのCLI試験はHTMLの欠如判定より先に、対応text/jsonの全バイト、総数、basename、順位・行を照合している。

N=0/1/3/10/12、空/空白/記号/全除外、min/max/topと引数順、12候補、Unicode合算、元総数の独立性を網羅。formatterは未ソートpairs・巨大整数・hostile/CR・引数非変更も対象。既存の安全性・固定バイト・入力失敗試験は保持した。

全suiteを合格とするwave gateは本RED境界では実行しない。製品GREEN、README1行、OpenSpec1.2/2.1、独立品質・phase合格は未達で、08-02以降の担当へ残す。CIは成功未確認。既存baselineや過去scopeを緩めていない。
