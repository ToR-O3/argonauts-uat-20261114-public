# Spine gate — configured reality-check lens 原本

設定finalize_reviewersの「committed decisionsをwebまたは既存現実で確認」を実行。入力: architecture.md、wordfreq全モジュール、pyproject.toml、tests、README、現行正本。別レンズ結果は入力にしない。subagent不可の逐次fallback。

- AD-1: sources.py/aggregator.py/formatters.pyの既存分離を実読。新しいframeworkやstarterを提案しない。
- AD-2: tokenizer.pyのcasefold、aggregator.pyのCounterとstable sort、test_tokenizer/test_aggregatorと一致。
- AD-3: sources.pyはcause付きInputError、__main__.pyは本文exit1。除外FILE不存在exit2だけは依頼者の明示要求。
- AD-4: __main__.py:34-38と既存回帰は元Counterからtotalを取り、別候補を選ぶ。totalの除外指定時意味は未採用。
- 標準ライブラリのみはpyprojectのdependencies=[]と一致。Python/pytestの現版やCI版を新たに固定していない。新技術の現在版をwebで調査して束縛する必要なし。

現実未確認の技術採用なし。web通信は行っていない。これは依存の更新可否調査でもCI実行成功証拠でもない。
