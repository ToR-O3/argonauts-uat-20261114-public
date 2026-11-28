# Spine — 入力照合原本

PRD全文、依頼原文/受入、現行正本、wordfreq、tests、READMEをそれぞれspineと照合。subagent不可につき逐次fallback。

PRDの指定/解析/照合はAD-1/AD-2、エラーはAD-3、全形式と既存互換はAD-4とConventionsで保持。help/README/試験は技術的再定義せずPRDに委ねる。構造・Counter・casefold・InputErrorのcauseは既存コードと一致。HTMLtotal、空白、文字コード/その他取得失敗、不正行、同時失敗の未決を採用済みADに紛れ込ませていない。

運用/インフラ、状態、認証、永続化、サービスレベルは追加対象ではないことが明示され、次元の黙殺なし。ticketのRequirementsは存在せず、PRD/raw intent入力であることをmemlogに保持。親spineは入力されていないのでInherited Invariantsは作らない。重要な落ちなし。
