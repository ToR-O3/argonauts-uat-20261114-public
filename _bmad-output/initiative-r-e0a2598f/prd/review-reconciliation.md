# PRD — 入力照合原本

原文/受入、Brief、initiative、正本、実装、tests、READMEを入力単位ごとに照合。subagent不可につき逐次fallback。

- 原文/受入: FRで指定語/行/比較/不存在/全形式/説明/試験を保持。不要な依存・通信・CI変更を除く。
- Brief: documentパスをsourcesとpurposeに渡し、利用背景の推定と未決を継承した。
- initiative: Requirements不在を隠さず、チケット採用やKanban更新を行わない。
- 正本/実装: casefoldをlowerへ変えず、Counterの初出順とformatters境界を保つ。本文エラーと新しい除外エラーを分離。HTML総数変更を採用しない。
- tests: 実CLI/各形式/Unicode/既定バイト/境界の既存検証面と整合。未作成の検証コマンドを試していない。
- README: 使い方とエラー説明は追加対象。実READMEは今回編集しない。

落ちた重要要求なし。未決の定義は../open-questions.mdだけに置く。背景推定は未承認のまま。
