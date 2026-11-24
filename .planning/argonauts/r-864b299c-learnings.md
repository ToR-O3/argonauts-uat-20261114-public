# r-864b299c — CE 学習調査

`docs/solutions/` の Markdown 5件を対象に、README、wordfreq、CLI、JSON、UTF-8、一時入力、差分、PM向け証拠を調査。関連4件（直接2件）、critical-patterns なし。

- `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`: 実CLIを再実行し、JSONの件数・順序・値を照合する。今回は頻度が異なる4語を使い、上位3語を確認する。旧学習の同率時語昇順は現行契約ではなく、今回の証拠で同率順を主張しない。
- `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md`: コマンド・入力・終了値・実出力・差分を品質の平文証拠へ残し、添付後に原本を読み戻す。圧縮ファイルや画像をPMの判断の前提にしない。
- `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`（隣接）: 実装前の比較基点を固定して1行追加を確認。既存試験変更や新設を要求しない。
- `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`（隣接）: 独立検証の対象headを記録し、証拠のcommitと区別する。ローカルCLIの成功をCI成功とみなさない。
