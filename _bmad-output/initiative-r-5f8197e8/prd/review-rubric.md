# Independent rubric review

## Verdict

PASS（軽微な編集提案のみ）：internal stakesの小さなREADME改善を扱うinitiative PRDとして、要件の検証可能性、変更境界、対抗指標とテンプレートのDone whenを満たしている。依頼で固定されたfull flowとPRDを維持する判断は妥当だが、同じ制約の反復は短縮できる。

## 重要修正（最大3件）

受入を妨げる重要修正はない。以下は任意の軽微改善であり、承認条件にしない。

- severity: low
  location: prd-readme-min-count-3.md:83–132（Rules、Non-goals、MVP scope、Change boundary、API contract、Developer experience、Stories、Decisions）
  fix: READMEのみ変更、既存CLI不変、例1つ、3形式確認という重複をRules・FR・受入条件に集約し、他節は参照か差分だけに短縮する。full flowや指定テンプレート自体を変更する必要はない。
- severity: low
  location: prd-readme-min-count-3.md:132（Decisions）
  fix: 「完了後の学びで要件が変われば」に加え、適用する各epic完了後にPRDを見直し、学びをUpdateへ反映する旨を一文で明示する。これはテンプレートのNextとの表現整合であり、Done whenの不合格ではない。

## Findings by dimension

### 1. Decision-ready — strong

severity: none
location: prd-readme-min-count-3.md:30–40, 96–100, 124–136; .memlog.md:8–11
fix: 不要。目的は既存フィルタのREADME例追加に一貫し、例のコマンド、full flow、不要成果物、後続担当に残す入力準備の裁量を区別している。承認が必要な未決事項がないことも入力記録と整合する。

### 2. Earned — adequate

severity: low
location: prd-readme-min-count-3.md:42–48, 83–132
fix: 上記の短縮提案を適用できる。架空のpersona、事業効果の数値、一般的NFRは追加していない。非該当節を省く理由は明示されているが、小さなREADME改善に対して制約の反復はやや多い。

### 3. Testable — strong

severity: none
location: prd-readme-min-count-3.md:59–81, 102–108, 124–126
fix: 不要。FR-1は追加位置・個数・完全なコマンド、FR-2は同一入力・閾値・3形式・終了コード・語と回数の一致、FR-3は証拠に必要な内容と保存先を示す。閾値以上と未満をともに含む検証入力が必要であり、空出力だけで成功する抜け道も防いでいる。これらは後続で検証する条件であって、今回のレビューで実行を確認したという意味ではない。

### 4. Honest scope — strong

severity: none
location: prd-readme-min-count-3.md:34, 69–100, 110–118, 134–136; .memlog.md:8–11
fix: 不要。READMEの利用者向け変更と工程証拠を区別し、コード・依存・設定・試験追加を明示的に除外している。既存契約と今回の要求、仕様と実行結果も区別されている。入力準備を後続作業の裁量に残すことは、このstakesでは妥当であり、未決の事業判断とは扱わない。

### 5. Usable downstream — adequate

severity: low
location: prd-readme-min-count-3.md:12–28, 50–57, 83–132; .template.md:21–29
fix: 重複を短縮し、任意で見直し時点を明記する。用語・FR/RULE/SMの対応と担当ごとの受入手順は追える。initiativeとして必要な境界と依頼固有の証拠条件は残すべきであり、短さだけを理由にprd-lightへの置換や実行条件の削除を求めない。長さは目的に比してやや冗長だが、文書分割や差戻しが必要な問題ではない。

## Template Done when

- FRの検証可能性とneedへの対応: 満たす。読者、実装・品質担当、PMのneedがそれぞれFR-1、FR-2、FR-3へ明示的につながる（42–48行）。
- productを要するjourney beatの網羅: 満たす。今回の文書改善ではnamed journeyを縮小し、作業上のneedを採用することがテンプレートのstanceに適合する。記載されたneedに未対応のFRはない。
- Non-goalsと対象外: 満たす（83–100行）。
- hobbyを超えるstakesのcounter-metrics: 満たす。SM-1〜SM-3それぞれが対象FR、現在の状態、目標、対抗指標を明示する（102–108行）。受入指標を利用者数や事業効果の測定値と誤認させない説明もある。
- 製品とstakesに合った形: 満たす。capability-firstで、不要なUX・企業展開・AI等の節を増やしていない。長さには軽微な短縮余地がある。
- 利用者の判断に根拠があり、節埋めの創作がない: 提供された入力記録の範囲で満たす。.memlog.md:8–11の依頼・確定事項と主要判断は整合する。利用者本人への再確認や未読の原資料との独立照合までは実施していない。

## Review boundary

指定されたPRD、.memlog.md、.template.md、rubric-planning.mdの文書レビューのみ。CLI実行、コード検証、README実体の照合は行っておらず、既存実装については提供された仕様・入力記録の主張として評価した。
