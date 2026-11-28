# Rubric walker — sequential fallback

対象: ../architecture.md。独立委任不可のため著者の逐次代替。独立レビュー合格とは扱わない。

判定: 著者照合ではcritical/highなし。親の独立rubric review待ち。

- feature高度の分岐点をAD-1（共通集計前境界）とAD-2（未指定非干渉）に限定。配置・型・シグネチャはseed/Deferredでコード所有を維持。
- Binds/Prevents/Ruleは両ADに存在。表示だけの除外、形式別処理、除外前総数、未指定の新読取りはRuleに違反するため検出可能。
- PRD FR-1〜FR-6/RULE-1〜RULE-2をmapで照合済み。FR-4とFR-5を新しいschemaやADで膨らませずPRDを参照。
- Deferredのうち製品仕様はOQとして自由裁量と区別。OQ-1〜OQ-6が未決のため指定時の全仕様はまだ一意でない。議論用原本には許容するが最終受入の準備完了とはしない。
- brownfield単方向CLIを現行全実装と照合。新技術・versionを導入せず、既存コード以外の技術assertionなし。
- 運用・環境・外部provider・権限・依存・永続化は既存ローカルCLIの範囲と明記。新しい運用寸法を黙って追加しない。
- 親spineを入力としていない。initiativeのfrontmatter以外の要件・承認を推定しない。

処置: 製品未決はPRDへdefer。独立性不足は親へdiscuss。追加の設計修正なし。
