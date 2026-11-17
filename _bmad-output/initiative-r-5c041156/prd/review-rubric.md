# UPDATE Rubric review（順次fallback）

判定: 回答済み4点を実装・品質へ渡す文書としてadequate。製品実装・ブラウザ検証完了を主張せず、親の独立レビューは別途必要。

| Dimension | Rating | 所見・対応 |
|---|---|---|
| Decision-ready | strong | OQ-1〜4の回答元と各回答をDecisionsに保存。未決扱いは解消。 |
| Earned | strong | 需要は依頼を根拠とし、人物・利用実績・期限・効果数値を創作しない。 |
| Testable | strong | FR-1〜4にSM-1〜4が対応。通常/同数/top/空入力の連番例、basename、top前総数、3列/見出し関連付け/狭幅可読性が判定可能。 |
| Honest scope | strong | text/jsonの順位・メタデータ追加禁止。既存回帰、安全性、外部通信なし、範囲外を維持。A-1は非ゲート、Open questionsはnone。 |
| Usable downstream | adequate | ID/TOCは公式CLIで検査。分量は従前からの残余制約で、指定された詳細条件を削らない。 |

重要な対応は旧未決状態の除去、AC-2/3の具体化とSMへの反映、通常/同数/top/空入力の連番明示。すべて反映済みで、残るcritical/highの仕様欠落はない。

Template done when: 単一CLI操作を能力中心に記述。各FRは閲覧・文脈・順序・既存利用維持という必要性に対応する。実在の人物journeyは創作せず、非目標・counter-metric・利用者仮説を明記。詳細設計は後続へ委ねる。全必須章を保持し、任意章の統合/省略理由はDecisionsにある。

別担当subagentによる独立判定ではない。
