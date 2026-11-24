# 独立rubricレビュー

## Verdict

PASS WITH MINOR FIX：internal stakesの単一README改善のBriefとして、依頼の理由、変更境界、後続工程の受入条件は明確であり、PRDへ進める深さを満たす。テンプレートのDone whenは概ね満たすが、Executive summaryだけで「誰のためか」を明示的に把握できるようにする軽微な補足が望ましい。

## 重要な修正（1件）

1. severity: minor
   location: brief-readme-min-count-3.md:24-26（Executive summary）
   fix: 「READMEを参照する利用者が、最小出現回数3の指定方法を具体例で理解できるようにする」旨を1文補う。Who it servesとProblemに既にある内容だけを要約し、新たな利用者像や効果数値は加えない。
   reason: 現在の要約は変更内容・着手理由・後続の証拠確認者を説明しているが、直接の読者とその便益は本文から補って読む必要がある。要約単独でwhat / who / why nowが分かるというテンプレートの完了条件に対して、whoが暗黙的である。

## Dimension別所見

### 1. Decision-ready — strong

severity: none
location: brief-readme-min-count-3.md:24-26, 38-40, 54-58
fix: 不要。
単一の主張は既存機能を変えずに閾値3の例を追加すること。何もしない場合とコード変更の場合の比較があり、full工程、Architecture不要、対象外も決定されている。スポンサーへの意思決定依頼ではないため、投資額・市場規模・承認依頼の追加は求めない。

### 2. Earned — strong

severity: none
location: brief-readme-min-count-3.md:24, 28-30, 38-44; .memlog.md:8-12
fix: 不要。
依頼そのものと既存説明の不足を根拠とし、顧客像・利用頻度・被害額・競争優位を作っていない。内部の小規模文書改善に商業的な差別化や市場検証を要求する必要はない。既存CLIの事実はmemlogの静的確認記録との整合のみを確認したもので、独立した実装検証済みとは扱わない。

### 3. Testable — adequate

severity: none
location: brief-readme-min-count-3.md:34-36, 46-52
fix: Brief段階での修正不要。
追加例の数、閾値、対象形式、終了コード、語と回数の一致、閾値未満の除外、文字の証拠原本、READMEのみの利用者向け差分はいずれも後続で判定可能。具体的な入力とコマンドはPRDで定めることが明記されており、Briefに実行手順や結果を前倒しする必要はない。

### 4. Honest scope — strong

severity: none
location: brief-readme-min-count-3.md:26, 52-58; .memlog.md:9-10
fix: 不要。
README以外の利用者向け変更と工程文書を区別し、コード・設定・依存・公開入出力・試験ファイルを対象外としている。後続の検証予定と完了事実を混同していない。HTML viewの省略は明示された利用者overrideに整合する。

### 5. Usable downstream — adequate

severity: minor
location: brief-readme-min-count-3.md:24-26
fix: 重要な修正1のとおり、直接の読者と便益を要約に明記する。
用語と変更境界は一貫し、後続PRDへ渡す情報量も小規模変更に見合う。本文全体では読者が明確だが、要約単独での伝達に限って改善余地がある。

## テンプレートDone when検査

- 全体（.template.md:28）：概ね充足。whatはREADMEへの例追加、why nowは利用者の依頼で明示。whoは本文:44では明示される一方、要約内では暗黙的なためminor。
- Executive summary（.template.md:35）：充足。2段落であり、本文が支えない追加主張はない。単独性の改善は上記1件に集約する。
- Problem（.template.md:38）：internal stakes相応に充足。利用者の具体的依頼と既存例の不足を示し、対処負担・費用が未提供であることを正直に限定する。実名の顧客や金銭的損失を追加しない。
- Solution（.template.md:41）：充足。足りない具体例を追加する方法が説明不足に直接対応する。
- What makes it different（.template.md:44）：internal stakes相応に充足。現状維持と不要なコード変更を比較し、説明だけを補う利点を示す。顧客の乗換えや製品の競争優位の主張は不要。
- Who it serves（.template.md:47）：充足。README参照者と実装・品質・PMの役割が具体的で、対象文書を使う人を識別できる。架空のペルソナは不要。
- Success criteria（.template.md:50）：充足。受入条件は後続で確認でき、不成立なら受入完了にしない停止条件も明示される。
- Scope（.template.md:53）：充足。例1つ、READMEのみの利用者向け変更、後続検証、対象外が依頼と整合する。
- The ask（.template.md:56）：条件不成立。スポンサー向け提案ではない旨が本文にあるため省略は妥当。
- Vision（.template.md:58-59）：任意。単一README改善に将来構想は不要であり、省略は妥当。

## レビュー範囲

対象Brief、同フォルダの.memlog.mdと.template.md、指定rubric-planning.mdのみを読み、文書内容を評価した。実装・CLI実行・出力の検証は行っておらず、その完了を保証しない。対象文書は編集せず、本レビューだけを作成した。
