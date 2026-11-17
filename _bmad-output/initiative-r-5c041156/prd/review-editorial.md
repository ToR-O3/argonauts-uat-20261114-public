# UPDATE 構成・文章 polish

本書はBuilder・品質・仕様承認PMが回答済みの小変更を実装・検証へ渡すためのPRD。docs/humans、Microsoft Writing Style Guide、Strategic/Context (Pyramid)で構成→文章を順次確認した。同一担当のfallbackであり独立レビューではない。

公式word_metrics実測は全体4566、本文4182（frontmatter/TOC/Assumptions除外）。Success metrics 654、Decisions 454、Review refinements 712。wc -w全体314は日本語量を過小評価する。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Success metrics（654） | PRESERVE | 通常/同数/top/空入力、3幅実ブラウザ証跡は指定条件。削減0。 |
| structure | §Review refinements（712） | PRESERVE | 既存の特殊文字/CR/CRLF・保存/検証制約を削らない。削減0。 |
| structure | §Decisions（454） | PRESERVE | 回答元と解決済みID履歴、省略理由を追えるよう保持。削減0。 |

文章パス: 追加修正なし。既存の未決文を確定回答へ置換済みで、未実証の利用者仮説と実装未検証を区別する。意味や範囲を変える書換えはしない。

追加削減は0（0%）。本文は約3000語目安を超え、印刷2ページ適合も未検証。収めるには詳細受入例・レビュー補足を下流へ移す必要があるが、今回の明示維持条件を優先して残した。これは新たな製品上の未決ではなく文書量の残余制約である。
