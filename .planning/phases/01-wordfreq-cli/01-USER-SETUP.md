# Phase 1: User Setup Required

**Generated:** 2026-11-17
**Phase:** 01-wordfreq-cli
**Status:** Incomplete

REQ-07 の CI 部分は未検証。実測とローカル試験結果は [01-CI-GAP.md](./01-CI-GAP.md) を参照。

## Environment Variables / Account Setup

追加のアプリ用環境変数・秘密・新規アカウントは不要。workflow を変更できる人の既存の GitHub 権限が必要。Bot の権限は変更しない。

## Dashboard Configuration

- [ ] 対象 CPython 3 の版を人が確定する。
- [ ] `ToR-O3/argonauts-uat-20261114-public` の依頼branch `argonauts/r-5a3b8a3f` に pytest CI ジョブを 1 本追加する（例: `.github/workflows/`、GitHub の Actions 設定）。
- [ ] repo をチェックアウトし、pytest 開発依存を導入した環境で repo 直下の `python -m pytest` を実行する。ランタイム依存の追加は不要。
- [ ] 対象 head の実行であることを確認し、run・job 名・head SHA・Python 版と成功ログを品質へ渡す。

## Local Development / Verification

既存の開発環境では repo 直下で `python -m pytest`。実測は 43 passed / exit 0 だが、ローカル成功を CI 成功として扱わない。

CI の期待結果: pytest が全試験を実行し、failed 0・終了コード 0。skipped の CI ジョブは証拠にしない。品質の後続フェーズ検証で設定と実行証拠を再確認した後にのみ、このチェックリストの完了を記録する。

## 01-05 follow-up — 2026-11-17（現在のチェックリスト）

**Current Status: Human setup supplied / independent quality validation pending**。
先頭の `Status: Incomplete` と上記未チェック項目は01-04当時の履歴として保持する。現在の状態は本節で区別し、済んだworkflow追加を再依頼しない。

- [x] 人が CI 対象 **CPython 3.12** を選択した（人の回答、fix-1）。
- [x] 人が `.github/workflows/pytest.yml` を依頼branchへ追加した。commit `5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2`。BuilderはGitの当該commitと現行原本を読取り照合済み（ファイル証拠のみ）。
- [x] 歴史的headの成功報告を引継ぎ入力として受領した。run `44017344659`（pull_request）/ `44017344584`（push）、completed/success、43 passed は**人報告のみ**。architect / Builderによる独立Actions検証ではない。
- [ ] 品質が最新対象headとworkflow/job/event/Python 3.12/pytest全43件成功・failed 0・exit 0の実ログを独立照合する（remote-success item）。
- [ ] 品質が全先行PLANを含むPhase 1を再検証し、REQ-07とVERIFICATIONの実際の判定を記録する。

Git原本の確認事項: name/job pytest、ubuntu-latest、checkout@v4、setup-python@v5 / python-version 3.12、push(argonauts/**) とpull_request、contents:read、python -m pip install pytest、python -m pytest。現行原本と人commitの差分なし。これだけで実行成功とはしない。

ローカルの既存全試験もTask 1終了時に実行し、実測を [01-CI-GAP.md](./01-CI-GAP.md) に記録する。ローカルPythonはCI版の証拠ではない。文書・ローカル成功・task 3.3のチェックだけではgapを閉じない。

次の引継ぎ: [ci-handoff.md](../../argonauts/t_0d6af354/ci-handoff.md) はTask 2で作成予定。品質は最新headを解決してローカルとremoteを別gateで確認する。不足/pending/auth拒否/ログ不可/不一致/failed/skipped/0件ならREQ-07 Pending・gaps_foundを維持し、観測を記録して人・PMへ返す。待機ループ、workflow修正/push、権限変更、依存追加、CI dispatchは行わない。元のVERIFICATIONとCLI証拠の添付はフック拒否によりGitのみだったため、品質は今回の添付可否または具体的不能理由も記録する。
