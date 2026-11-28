<!-- argonauts:guide:begin -->
## レビューの案内（Argonauts）
状態：人の判断が要る：最終の品質確認待ち（方針：smart、自動マージ：予約していない）
人がすること：今は操作せず、最終確認後のこの案内を確認する
変わったこと：wordfreq に --min-length N を追加し、N文字未満の単語を結果から除けます。
省略時はこれまでどおりです。--help に説明を追加し、README.md は変えていません。
受入条件と証拠：長さの境界・既定互換・help の対象試験29件成功。確認担当の全1080件成功記録と、基準実装との3形式の出力一致記録あり。README.md の差分なし。
危険の印：無し（実装担当の下書き。品質担当が最終判定）
読む順番：wordfreq/__main__.py の長さ条件、tests/test_cli.py の境界・互換試験、tests/test_max_count_verifier.py と tests/fixtures/max-count-scope/ の過去製品分離、docs/solutions/best-practices/pytest-basetemp-parent-only.md の実行時の注意
読まなくてよい所：計画や検証の作業資料
変更の大きさ：13ファイル（全体161）、+5466/-6（全体。作業資料を含む）
注意：衝突・out-of-date・『Expected』が出ていたら、GitHubで直さず /team-request r-1bae0a69 更新
<!-- argonauts:guide:end -->

## 作業の記録

依頼 r-1bae0a69 / light / 手順版1.14。最終の品質判定と自動マージの予約は品質担当が実施します。この下書きでは予約していません。

| 原本・受入条件 | 記録・結果 |
|---|---|
| BMAD要求 | `_bmad-output/initiative-r-1bae0a69/prd/prd-light-wordfreq-min-length.md` |
| GSD計画・完了記録 | `.planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-PLAN.md`、同SUMMARY・VERIFICATION。3 tasks対応、検証passed |
| N未満除外・境界保持 | 追加試験は全形式、casefold後の文字長、頻度上下限/top、空結果を検証 |
| 既定1で従来互換 | 確認担当が基準branch実装とのtext/json/htmlバイト一致を確認。固定期待値試験あり |
| --help・試験追加 | 最終化で `uv run --no-project --python 3.12 --with pytest python -m pytest -q -k min_length -p no:cacheprovider` を再実行し29 passed / 1051 deselected / exit0 |
| 全回帰 | 確認担当の原本 `.planning/argonauts/r-1bae0a69/VERIFICATION.md`：対象05ac9a1で1080 passed。最終化では製品・試験を変えず、全回帰を重複実行していない |
| README.md不変 | `git diff --quiet origin/v112-b HEAD -- README.md` exit0 |
| OpenSpec正本反映 | `archive r-1bae0a69-light --json` は仕様同期の確認要求のみ。続く `archive r-1bae0a69-light --yes --json` はexit0、3要求追加・既存変更0。公式archiveオブジェクトは `ARCHIVE-RESULT.json` |
| Archive原本 | `openspec/changes/archive/2026-11-28-r-1bae0a69-light/`、正本 `openspec/specs/wordfreq-cli/spec.md` のML-1〜3。元変更ディレクトリなし |
| 学び | `docs/solutions/best-practices/pytest-basetemp-parent-only.md` を同じPRに収録。残り2候補は既存試験と確認原本で回収できるため追加文書なし。予防策の追加提案なし |

既存の確認用補助スクリプト2件は工程の証拠として保持しています。今回の最終化は公式archiveとPR案内のみで、実装・試験の変更はありません。TDD工程上の過去の差異はQuick検証原本に留保されており、完全な工程準拠と読み替えません。
