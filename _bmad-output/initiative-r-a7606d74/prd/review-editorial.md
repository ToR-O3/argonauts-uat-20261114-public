# Editorial polish — structure, prose

この文書はcoding agentと確認者が単一CLI機能を実装・検証するための要求書。BMad reviewの公式activationを解決し、明示されたstructure、次にproseだけを適用した。読者は既定humans、style guideはMicrosoft Writing Style Guide。内容を変更せず表現・配置のみを確認した。

## Structure

Strategic/Context (Pyramid)を選択。確定結論と実装完了との区別をProblem冒頭へ置き、要求・判定可能な受入条件・非対象を分離している。casefold後の境界例はFR-1を具体化し、重複による無意味な水増しではない。Open questionsの目次・節は未決なしのinclude-whenに従って除去済み。内容上の追加修正提案なし。

## Prose

日本語の簡潔な要件表現、FR/SC、MUST、Given/When/Thenと既存技術用語を維持。曖昧な「確定後」「案」「回答待ち」は更新で解消済み。意味理解を妨げる表現の指摘なし。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | 目次後の重複空行 | 空行1行へ | 空白のみ整理、語数影響0。 |

公式word_metricsは1931語相当（日本語分割）、Problem 122、Requirements 368、Success criteria 394。テンプレートに数値上限はない。frontmatter・目次・Assumptionsを除いたbodyをcsplitでscratchへ分割し `wc -w` で計数：109 + 6 = 115（空白分割）。計数方式が異なるので日本語分割の総数とは比較しない。追加の内容削減提案0、削減0語・0%、理解上の犠牲なし。新しい製品判断・仮定は追加していない。

トリアージ：空行修正のみ適用済み。旧runの引渡し保留前置きは確定回答により不要となり、Problemに確定判断を記載した。要求確定と実装・試験完了の区別は残した。
