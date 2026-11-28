# Brief — 入力照合原本

入力ごとに、原文/受入、initiative、現行正本、実装、tests、READMEをBriefと比較した。subagent不可につき逐次fallback。

- 原文/受入: --exclude、1行1語、空行/#、casefold、不存在stderr/exit2、help/README/tests、未指定互換をすべて保持。新依存/通信/CIを広げていない。
- initiative: 題名のみでRequirementsなし。原文を代わりの一次入力とし、架空のticket要求を追加しない。
- 正本/実装: Unicode casefold、同数初出順、min-count/top、本文exit1と取得境界を維持。HTML総数は明示未決。
- tests/README: 追加試験と説明を成果条件として残した。現試験を新機能の合格にすり替えていない。

落ちた重要要求なし。trim/字下げ/他読込み失敗を既存本文契約から決められない点は中央未決一覧で説明される。背景推定はAssumptionsとして残す。
