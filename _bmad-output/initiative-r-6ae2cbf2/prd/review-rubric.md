# PRD rubric review

Verdict: adequate、軽微な文書修正1点。要求の判断に不足はなく、既存HTML期待値の扱いも明確である。

最優先の修正: Decisions の「リスクは…のみ」はリスクを網羅した根拠がなく限定が強い。「確認したリスク」とする。ほかに重要な修正なし。

| Dimension | Rating | Finding / severity / location / fix |
|---|---|---|
| Decision-ready | strong | 単一機能・FR-1〜FR-3・RULE-1〜RULE-3 で範囲確定。指摘なし。 |
| Earned | adequate | low / Decisions / リスクの限定表現のみ修正。市場・利用者実績・期限・架空の担当者は追加していない。 |
| Testable | strong | 動的件数、top未満、min/max後、空0、総数維持、他形式不変が検証できる。指摘なし。 |
| Honest scope | strong | 依存・権限・送信・移行を除外。製品未変更／製品試験未実行を区別。指摘なし。 |
| Usable downstream | adequate | 命令例を未実行と表示。実在しない検証名・PLAN・新CLIは作らない。指摘なし。 |

Template done-when: FR の根拠が Brief と HTML 読者のニーズに紐付く。単一CLI機能なので journeys は縮小し、受入条件を持つ1 storyを記す。Rulesとカウンターメトリクスがあり、適用外セクションはDecisionsへ理由を記す。構成は initiative 粒度で、依頼が明示した境界例だけ補足する。

Memlog audit: 入力、明示テンプレート、既存契約、HTMLバイト期待値リスク、適用判断、2推定、Architecture不要、引継ぎ記録のみを反映。技術実装や検証コマンドは本文に持ち込まない。

Reconciliation（入力ごと）:
- 依頼原文: HTMLのみ・総数横・実表示数・top後・空0・text/json不変・テスト・README1行・範囲外を全て反映。
- Brief原本: B1〜B6、2つの非重大推定、Architecture判断、実装未完了を反映。
- initiative: frontmatterのみであると明記。本文要求を捏造していない。
- 現状ファイル: 各引用箇所と契約を照合。旧HTMLバイト期待値との意図した差分を認識している。

IDs/TOC: check_ids.py の undefined/duplicate/withdrawn/toc は空。unknown_prefix の UTF-8 は符号化名をIDと認識した警告で、要件IDではない。CLIはexit0。

方式: subagent起動ツールがないため公式fallbackで順次実施。別実行者の独立レビューではない。
