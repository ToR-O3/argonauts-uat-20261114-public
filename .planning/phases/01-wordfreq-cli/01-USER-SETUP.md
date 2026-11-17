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
