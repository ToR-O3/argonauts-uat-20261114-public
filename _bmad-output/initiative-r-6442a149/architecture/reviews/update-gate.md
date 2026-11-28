# Update reviewer gate — 統合判定

## 判定

原本は後続の仕様統合に使用可能。実装・試験合格・実装着手承認の判定ではない。回答済み判断1〜6と維持条件は原本へ反映済み。OQ-7/8だけを背景不足として残し、機能受入の停止／追加条件にはしない。公式headless出力は背景の未確認によりpartial、原本はdraftを維持する。

## 実施と保存先

- 公式機械lint：`update-lint-spine.json`、ok:true／total_findings:0。
- rubric walker・入力照合・fresh reader：`../../reviews/update-independent-review.md` の4〜7節。
- configured floor reality check：`update-independent-reality.md`、PASS。現行tokenizer／aggregator／CLI／formatter／sourcesとmanifestを独立実読。
- configured floor adversarial seam：`update-independent-adversarial.md`。M-1のUnicode行境界追加明文化提案を保存。
- bmad-review edge／structure／prose：`../../reviews/update-independent-review.md` と `../../reviews/update-independent-findings.json`。edge配列は空、編集修正要求なし。
- authorのトリアージ：`../../update-review-triage.md`。M-1は未要求の文法拡張・入力域完全定義を新条件にしないためignore。その他のscope内修正要求なし。

configured floor全2件は別プロセスで並列実施し、authorと独立した文脈で結果を保存した。rubric等もauthorとは別の独立reviewプロセスで実施し、個別pass内の逐次方式と限界をレビューに明示した。レビュー間の不一致は隠さず、採用回答と作業範囲に照らして上記の通り裁定した。

## 最終照合

AD-1/2のIDを維持、AD-3/4を追加。比較境界は既存のcasefold済み本文キーと行全体casefoldキーで、Straße／STRASSEに必要な同値情報を保持し、lowerから復元しない。本文抽出・同数順・未指定動作、最後FILE非先行読込、既存検証→除外→本文、除外エラーのstderr／exit2／stdout空、既存本文exit1、全語除外exit0・HTML既存案内を保持する。

help／README／試験は後続実装。本runで製品・README・試験・GSD・OpenSpec・initiativeを変更せず、Git／Kanban操作も行わない。独立レビューと機械検査は機能試験の代わりではない。
