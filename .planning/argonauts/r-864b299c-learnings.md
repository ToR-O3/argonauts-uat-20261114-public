# r-864b299c — CE 学習調査（Phase 5 gap 1 / t_24b12432）

`docs/solutions/` の Markdown 5件を調査し、関連5件（直接3件、隣接2件）を確認。検索軸は Git index/worktree/commit、完全一致許可、既存フィクスチャ、実CLI、JSON順序、対象head、平文証拠と添付。pack指定なし。

- `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`: 固定比較基点を含む使い捨てコピーで、状態と変異を一つずつ独立に用意し、対象パスと拒否理由を照合する。
- `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`: 比較基点・実行対象 HEAD・index/worktree の状態・報告コミットを区別し、品質が最新の報告込み対象を再確認する。ローカル成功をCI成功とみなさない。
- `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md`: `05-VERIFICATION.md` と `05-CLI-EVIDENCE.md` に終了値・コマンド・入力・実出力・対象headを平文で保存し、添付を読み戻す。
- `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`（隣接）: 実 CLI の JSON を並べ替えずに比較する。古い同率時の語昇順は現行契約ではなく、今回は `alpha:4`、`beta:3`、`gamma:2` の順と3件ちょうどを確認する。
- `docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md`（隣接）: 添付拒否は検証器の差分拒否と区別する。拒否を迂回せず、共有可能なGit原本を特定し、標準添付時はバイト同一性まで確認する。

計画への適用: 現在の報告2件と次回に必要な報告・計画成果だけを限定する。既存の検証コマンドを変えず、隔離コピーで報告の未追跡・ステージ・コミットの3状態を確認し、無関係な追跡変更・未追跡・既存フィクスチャの独立した負例を残す。
