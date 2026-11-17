# Review: prd-wordfreq-cli.md（rubric-planning）

## Verdict

内部単一機能・hobby/solo 高度に対して決定事項（D-1〜D-3）・非目標・試験方針が明示され、大部分の FR はそのまま検証可能な良質な capability spec である。ただし FR-6 の「拡張できる構成」が機械的に検証できない形のまま書かれており、Brief の推定タグ（A-1〜A-5、特に A-5 の同名 PyPI パッケージ衝突）が PRD に一切引き継がれていない点が、下流（OpenSpec）に持ち込む前に直すべき弱点である。

## Top 3 fixes

1. **FR-6 の検証形を明記する**: 「拡張できる構成とする」だけでは v1 では検査不能。検証形は design.md への記録だけになりがちなので、「ファイル入力を含む入力取得境界（抽象）が存在し、ファイル実装はその背後にあり、既存の単体試験がその境界越しに通る」等の機械的・レビュー的に確認できる形に書き直す。
2. **A-5 を PRD に引き継ぐ**: FR-8 は `pyproject.toml` 等のパッケージ化設定変更を許容しており、ローカルパッケージ名 `wordfreq` と既存 PyPI パッケージ `wordfreq` の取り違えリスクはパッケージ化時に実際に効く。Brief A-5（依存を入れない限り問題なし、CI に外部パッケージが入ったら再評価）を前提条件として明記する。
3. **WF→FR の対応表を記録する**: memlog は「Brief WF ID は memlog と本文対応で追跡」と宣言するが、WF-01〜08 → FR-1〜8 の実対応は文書のどこにも無い。FR-6〜FR-8 はどの journey の「満たす FR」にも列挙されず（UJ-1 は FR-1〜FR-5 まで）、ID 解決が暗黙の推測になる。1 行ずつの対応表（例: WF-01→FR-1, WF-02→FR-2, WF-03→FR-3, WF-04→FR-5, WF-05→FR-4, WF-06→FR-6, WF-07→FR-7, WF-08→FR-1）を Decisions か Features の冒頭に置く。

## Findings by dimension

### 1. Decision-ready — strong

所見なし。D-1〜D-3 は代替案と退けた理由を伴い、thesis（価値は性能でなく決定性と拡張点の明示）が Vision・Non-goals・MVP scope に一貫して通っている。text 列書式の design.md 委任もレベルの分け方が正しい。

### 2. Earned — strong

所見なし。persona も boilerplate NFR も無く、SM-2（学習候補 2 件）は受け入れカード側の工程要求で高度に適合。hobby stakes で counter-metric を置かない判断も妥当。

### 3. Testable — adequate

- **[medium] FR-6（Features F2）**: 「入力元をファイル以外（標準入力・URL）に拡張できる構成とする」は v1 の実装で機械的に検証できない曖昧な構成要求。検証可能部分は design.md への記録に依存している。→ 修正: 境界の存在を確認できる形（入力取得の抽象＋ファイル実装がその背後、試験が境界越しに通る等）で書く。
- **[low] FR-3（Features F1）**: 「単語と回数を読むことのできる形式」は列書式委任後の残存チェックとしてやや曖昧。→ 修正: 「1 行に単語と回数が（design.md で固定された）区切りで含まれる」と最小制約を1文足す。
- **[low] FR-8（Features F3）**: 「必要最小限に留める」は主観。実質チェックが smart マージの人の承認である点は書かれており許容範囲。→ 修正: 認めて「承認時に人が判断する基準（実行と試験に不要な変更を足さない）」を半行補う程度。

### 4. Honest scope — adequate

- **[medium] 全体（Assumptions 不在）**: rubric の「inferences tagged」が PRD 側にゼロ。A-5（`wordfreq` 名衝突は `python -m` 実行範囲では問題なし）は FR-8 のパッケージ化許容と直接絡む制約で、下流が PRD だけ reads する場合に失われる。→ 修正: 「前提（Brief A-1〜A-5 から要求に影響するもの）」として A-5（と必要なら A-2 の標準ライブラリ中心方針の由来）を 1〜2 行引き継ぐ。
- **[low] Non-goals / MVP scope**: 非目標は明示的で依頼明記（GUI）と決定由来（D-1 等）の区別もついており良好。URL 入力の「拡張性だけ残す」は FR-6 の曖昧さと連動（上記 medium を直せば解消）。

### 5. Usable downstream — adequate

- **[medium] Features / memlog**: WF→FR 再 ID 化の対応表が存在せず（memlog は追跡を宣言するのみ）、FR-6〜FR-8 はどの UJ の「満たす FR」にも入っていない（F2/F3 ヘッダの UJ-1 紐づけと UJ-1 行の FR-1〜FR-5 が不整合）。OpenSpec が FR ID を引き継ぐ以上、journey 以外の追跡経路である WF ID との対応を文書内に残すべき。→ 修正: Top 3 fix 3 の対応表を追加し、UJ-1 の「満たす FR」を FR-1〜FR-8 に整合させるか、構造要求（FR-6〜FR-8）は journey 非対応で WF のみ追跡と明記する。
- **[low] FR-4（Features F1）**: 「出力は決定的（識別子とする）」の「識別子」が意味を取りにくい（決定性こそが本ツールの価値識別子、程度の意図か）。→ 修正: 「決定的であること（受入の照合基準）」等に言い換える。

## Done-when チェック

- 全 FR が高度で checkable かつ journey/need へ追跡: 一部未達（FR-6 の検証形、FR-6〜FR-8 の追跡経路が暗黙）。
- 非目標が明示: 達。
- 単一運用者の capability spec に合う形: 達（約 2 ページ、lean 宣言あり、節の水増しなし）。
- 節埋めの捏造なし: 達。
