# 08-01 浅いcloneの履歴欠落の修正（run171）

## 結果と範囲

品質run170の必須指摘を、実際のdepth1 cloneで再現して修正した。製品、README、workflow、依存、封印原本、standalone validatorは変更していない。表示種類数と局所CSSは未実装のまま。42失敗は意図的REDであり、製品GREEN・Phase合格ではない。

対象は r-6ae2cbf2 / t_b82e2068 / 08-01。開始HEADは c5c8707445d22dd2ee58d3be7b3e8da38ae34d54。報告HEADはレビューmetadataに分離する。受付には新しい日時付き依頼者判断は無かった。

## 原因を確認した証拠

GitHub Actions 45703841138 の実失敗ログを `gh run view 45703841138 --log-failed` で取得し、ci-c5c8707.logに保存。49 failed / 1058 passed、検証試験7件のgit show exit128を確認した。採取時commit be231840989079fed532c7372efb66f577e39b09 と fe0f0b322ff81b687bc8c8314e85614407f1d0c2 が浅いcloneに無い。

手元の全履歴では成功するため、実depth1 cloneへ環境だけを変えて同じ既存試験を実行した。修正前は7 failed / 11 passed（exit1）。失敗名も品質指摘と一致し、製品機能とは無関係だった。

## 最小修正

`tests/test_displayed_types_verifier.py` の歴史原本を使う試験だけに、原本のprovenance.headがGitに存在するかの前提検査を追加。

- commitがあり、履歴を照合できる場合は従来どおりvalidate_beforeと変異試験を全部実行。
- commitが無く、Git自身が浅いcloneと判定する場合だけ、必要なSHAとfull historyでの再実行を理由にskipする。11件（旧原本1、新原本のread-only1、変異9）が対象。
- full cloneなのにcommitが無ければpytest.fail。provenanceの欠落・不正JSONなどもskipに変換しない。
- standalone `--mode validate-before` はそのままfail-closedで、Git不在を受入にしない。自動fetch、workflow変更、合成の原本への代替なし。
- 実ブラウザーの起動は従来どおり `WORDFREQ_DISPLAY_CAPTURE=before` で明示実行するときだけ。通常suiteは起動しないため、CIへ手元のChromium・Windows fontを要求しない。skipは原本の検証済み／画像確認成功を意味しない。

## 実行と結果

全pytestは `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` を使用。Python 3.12.15。stdout/stderrは各.log、全suiteのJUnitは.xmlに保存した。

| 環境・対象 | 実結果 |
|---|---|
| 修正前depth1 clone / tests/test_displayed_types_verifier.py -q | exit1 / 7 failed, 11 passed / shallow-red.log |
| 修正後depth1 clone / 同ファイル -q -rs | exit0 / 7 passed, 11 skipped / shallow-green.log |
| 全履歴worktree / 同ファイル -q -rs | exit0 / 18 passed、skip無し / local-verifier.log |
| 修正後depth1 clone / pytest -q | exit1 / 42 failed, 1054 passed, 11 skipped / shallow-full.log, shallow-full.xml |
| 全履歴worktree / pytest -q | exit1 / 42 failed, 1065 passed、skip無し / local-full.log, local-full.xml |

両環境とも失敗名は `test_displayed_types_cli_matrix` の40件、`test_html_displayed_types` の1件、`test_complete_fixed_css_contract_is_static_not_browser_acceptance` の1件のみ。表示leaf欠如41件と新局所CSS期待1件の意図したREDに一致する。検証試験のexit128は修正後depth1 cloneでは発生しない。skip件数による成功件数の差を隠さない。

### 浅いcloneでの再現方法

リポジトリrootで、専用出力先を作成し以下を実行した。修正前後で同一のcloneを使用し、修正後は対象testファイルだけをcpした（製品は同一）。

```sh
git clone --depth 1 --no-hardlinks --single-branch --branch wt/t_b82e2068 "file://$PWD" .planning/argonauts/r-6ae2cbf2/rework-run171/shallow
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest .planning/argonauts/r-6ae2cbf2/rework-run171/shallow/tests/test_displayed_types_verifier.py -q
cp tests/test_displayed_types_verifier.py .planning/argonauts/r-6ae2cbf2/rework-run171/shallow/tests/test_displayed_types_verifier.py
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest .planning/argonauts/r-6ae2cbf2/rework-run171/shallow/tests/test_displayed_types_verifier.py -q -rs
```

全suiteは各repo rootで実行。cloneは検査後に専用管理scratchのshallow-run171.UguDK5/cloneへ退避し、PRへ含めない。再現にbrowserの起動・インストールは不要。

## 既存文書のCI記述の訂正

run169のrework-proof.md末尾の「CI failureが2件」はrunを数えたもので、失敗試験が2件という意味ではない。当時の「手元では42失敗」をCIにも一般化してはいけない。品質run170の実ログによればc5c8707のCIは49失敗で、履歴に依存した7件が混入していた。今回の浅いcloneでの修正後は42失敗のみだが、新pushのGitHub CIは別途1回読み、未完了なら合格と主張しない。

## 保全と後続

- 旧before index SHA: 67ed798db1f5f6ff28a7f57af423ef2f483b83bc206685d4926106640c5e8a55。
- 比較用before-cjk-run169 index SHA: c82372c9208e91315101f84ce758f5efae7aa2a4a45c78513aa313d945c01c80。
- 両root、wordfreq/、README.md、.github/workflows/の開始HEADからの差分は空。git diff --checkもexit0。
- 日本語38画像の品質閲覧済みという前回レビューの結果を引き継ぐ。今回は画像を採り直さず、再閲覧したとも主張しない。
- STATEはPhase8/Current Plan2/Total3/Ready to execute。08-01 SUMMARYは既存のためadvanceを重ねない。OpenSpec1.2/2.1も未完のまま。
- 後続はbefore-cjk-run169を比較基準とし、既存のrework-run169/fontconfig.confを検証プロセスへ渡す。変更前原本のfull-history検証を品質でも実行する。
