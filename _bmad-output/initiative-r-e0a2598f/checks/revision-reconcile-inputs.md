# Update reconciliation — 原依頼・initiative・Brief入力

## 判定と範囲

**判定: 原依頼およびBriefから、更新PRDへ落ちた製品要件・制約・重要な文脈は認められない。** 原依頼→Briefの経路にも重要な欠落は認められない。採用済みの具体化と、過去の未承認状態の解消を、削除・取りこぼしとは扱わない。

公式 `bmad-facilitate` の Finalize 2（入力ごとのreconciliation: 文書が落とした内容、とくに意図・ニュアンスを返す）に沿った、委任された照合のみの結果。各入力を全文読み、以下に入力単位で結果を分離した。この子セッション内で逐次照合しており、入力ごとに別プロセスを起動したという意味の独立レビューではない。rubric/fresh-reader、spine照合、実装検証、承認、原本の修正は対象外。

参照する行番号は本照合時点の原本。以下のパスはinitiativeディレクトリ相対。

- 原依頼と根拠: `source-context.md`
- 薄いチケット: `initiative-r-e0a2598f.md`
- 入力Brief: `brief/brief-wordfreq-exclude.md`
- 更新PRD: `prd/prd-wordfreq-exclude.md`
- 採用済み変更の判断基準: `decision-update.md`

過去の `review-reconciliation.md` は現在の更新版の合格根拠には使用していない。本判定は文書間の保持確認であり、機能が実装済み・試験合格・仕様承認済みという判定ではない。

## 入力1: source-context.md → Briefおよび更新PRD

**結果: 保持。修正を要する取りこぼしなし。**

| 入力の要求・制約・文脈 | Briefの保持先 | 更新PRDの保持先・判定 |
|---|---|---|
| 原依頼の `--exclude FILE`、1行1語、指定語の除外（L11–13） | Executive summary / Solution（L31–45） | Glossary、FR-1、FR-2（L58–76）。指定語の全出現を外す。 |
| 空行・#開始行の無視（L11–13） | L31、L58–59 | FR-2（L74–76）。trim後判定と行終端は採用決定による具体化。 |
| 大小を区別しない、既存casefoldを維持しlowerに変更しない（L11–13、L21、L39） | L31、L45 | Glossary、FR-3、RULE-1、Decisions（L60、L80–82、L110、L147）。原文の「小文字にそろえる」をASCII lowerへ誤縮小していない。 |
| FILE不存在は分かるstderrとexit2（L11–13） | Solution、Success criteria（L43、L60） | FR-4（L86–90）。本文exit1へ誤って統合していない。 |
| --help、READMEの使い方、追加試験（L11–13） | L33、L61、L66 | FR-6/FR-7、Developer experience（L98–106、L139）。README実行例の試験まで明記。 |
| 未指定互換（L13、L18、L30） | L33、L61–62 | FR-1/FR-7、RULE-1、API contract（L68、L104–106、L110、L135）。既存出力のバイト比較と既存全試験を要求。 |
| HTML総数は元入力全体、min-count/top前。変更判断を独断で行わない（L13、L19、L23、L41） | L31、L43、L57 | Glossary、FR-1/FR-5、Change boundary（L62、L68、L94–96、L131）。旧未承認状態ではなく採用決定の元総数維持を反映。 |
| 既存回数・同数初出順・全形式・空状態・安全性の維持（L18–23、L30–34） | L57、L62、L66、L68 | FR-5/FR-7、RULE-1/3（L94–106、L110–112）。HTML見出し・空結果・escape・静的安全性を保持。 |
| 本文UTF-8/exit1と引数exit2、取得/解析/集計/整形の境界（L18–24、L33、L39–41） | L43、L62、L68 | Glossary、FR-4、RULE-2、Change boundary、API contract（L58、L86–90、L111、L131、L135）。終了コードはCLI、整形にI/Oを持ち込まない。 |
| 新依存・外部通信・CI変更不要（L13、L26、L45） | L62、L68 | RULE-3、SM-3（L112、L127）。既存契約の意図しない拡張を禁止。 |
| 薄いinitiativeにはRequirementsがない。原依頼を補助入力にしチケットを編集しない（L17） | sources（L9–11） | Document purpose / Decisions（L40、L147）。要求をチケットにあるかのように捏造しない。 |
| 元の依頼・根拠・現存試験と、新機能の未実装/未検証を分ける（L28–35） | L62 | FR-7、Developer experience、SM-3（L104–106、L127、L139）。新機能の合格証拠へすり替えていない。 |
| Update/headless、親レビュー前draft/partial、後続t_91b92aed承認とは別（L3–7） | 冒頭、Open questions（L15、L77） | 冒頭、MVP scope、Open questions（L17、L121、L160）。未解決製品事項なしとレビュー未了を混同しない。 |

### 削られた/圧縮された文脈の扱い

- `source-context.md` L15–35の実装ファイル別・試験ファイル別の読取り目録は、Brief/PRDへ逐語複写されていない。PRD L40とL139がsource-contextを証拠・現存検証面の所在として明示しており、元目録も残る。**参照による保持であり、要求削除ではない。**
- その目録中のソート非破壊性（source-context L22、L32）やパッケージ副作用抑制（L24）は、PRDに個別の新FRとしては列挙されない。既存公開契約を不必要に変えない境界（PRD L131）、未指定契約不変（L135）、既存全試験維持（L106）で保持する構成。これらを変更してよいという許可は追加されていない。
- 公式道具、scripts=stale、merge/memlog、Kanban/git禁止などの作業手順（source-context L7、L45–47）は、製品PRDのFRへ転載する性質ではない。source-contextに残る工程制約であり、この照合でも道具更新・git・Kanban操作をしていない。過去Create手順や逐次レビューの履歴を製品要件へ昇格させない。
- source-context L13、L39–41の「未承認」「未決」はCreate時点の履歴。L3–7と採用決定が現在の状態を明記している。更新文書がこれを現在の未決として再掲しないことは、意図された解消である。

## 入力2: initiative-r-e0a2598f.md → Briefおよび更新PRD

**結果: 保持。削除された要求なし。**

| 入力 | 照合結果 |
|---|---|
| title「wordfreqに除外単語ファイル指定を追加」（L3） | Briefタイトル/Executive summary（L13、L31）、PRDタイトル/FR-1（L15、L68）と一致。別製品・別機能へ逸脱していない。 |
| type: initiative、parent: none（L2、L4） | 文書sourcesから同じinitiativeへ追跡できる。架空の親やRequirementsを補っていない。 |
| Requirements/受入詳細なし（全文L1–5） | PRD L40が薄い入力であることを明示し、原依頼/source-contextで補う。詳細の不在を「受入条件なし」と解釈して元依頼を落としていない。 |

チケット原本の編集やKanban操作は行っていない。

## 入力3: brief/brief-wordfreq-exclude.md → 更新PRD

**結果: 保持。修正を要する取りこぼしなし。**

| Brief入力 | 更新PRDでの保持先・判定 |
|---|---|
| 小さな既存CLI拡張、語指名による除外。min-countだけでは代替できない（L31–49） | Vision、FR-1、FR-5、MVP scope（L44、L68–70、L94–96、L121）。回数閾値ではなく語による除外を別条件として保持。 |
| UTF-8、trim後の空行/#、行全体の既存Unicode `\w+` 一致（L31、L58–60） | Glossary、FR-2/FR-4（L59、L74–76、L86）。数字/underscoreの受理と全不正行例も保持。 |
| casefoldと `Straße STRASSE` の同値（L45） | FR-3（L80–82）。Unicode例とASCII例で全出現除外を明確化。 |
| 元入力HTML総数、残る語の回数と同数初出順（L43、L57） | Glossary、FR-1/FR-5、RULE-1、Change boundary（L62、L68、L94–96、L110、L131）。 |
| 引数検査→除外取得/全行検証→本文。全読込み失敗exit2、不正行のファイル名/行番号。本文未読、結果/HTML/Tracebackなし、本文exit1維持（L43、L59–60） | FR-4とFR-7（L86–90、L106）。複合失敗の受入例と本文未読の検証も保持。 |
| help/README・追加試験・既存試験・未指定互換（L33、L61–62） | FR-6/FR-7、Developer experience（L100–106、L139）。 |
| 全形式共通、top/min-countの表示枠を除外語に消費させない（L66） | FR-5（L94–96）。全件除外や空本文の観測点を具体化。 |
| 新依存/通信/CI/正規化/並び/自動辞書/複数ファイルの新利用方式/永続設定/HTMLデザイン変更の除外（L68） | RULE-1/3、Non-goals、API contract（L110–112、L117、L135）。サーバー/Web UI向け拡張でない文脈（Brief L53）もMVPの新規サービス/インフラなし（PRD L121、L135）に保持。 |
| 未確認の利用者像・業務背景・時期・締切・効果量を捏造しない（L33、L39、L49、L53、L70–73） | Vision、Users and journeys、Decisions、Assumptions（L44、L48、L151、L155）。未確認のまま継承。 |
| 一覧を繰り返し指定できる価値は推定（L72） | PRDの利用手順（L50–52）と「Briefの利用背景推定を継承」（L155）。永続設定や反復利用の実績を確定事実へ変えていない。 |
| 新市場・競合優位・予算要請・中長期ロードマップを主張しない（L49、L68） | 単一featureのVision/MVPと「予算・担当名・日程・性能値を発明しない」（L44、L121、L151）。市場/予算節の不転載は必要な文脈の削除ではない。 |
| 5決定解消済み、現在の製品未決なし。draft/partialと後続承認は別（L15、L77） | 冒頭、Decisions、Open questions（L17、L149、L160）。 |
| PRDはBriefと採用決定を入力にする（L77） | sources、Document purpose、Decisions（L10–13、L40、L149）。 |

Briefの説明的な比較・背景の全文章を逐語転記する構成ではないが、語を指名して除外する意図、既存CLIの一貫性、未調査の背景を誇張しない慎重さは失われていない。

## 採用済み変更を欠落と誤認しないためのクロスチェック

| decision-update.md | Brief | 更新PRD |
|---|---|---|
| 1. 元入力HTML総数維持（L9） | L31、L43、L57 | L62、L68、L96、L131 |
| 2. trim後判定・LF/CRLF/最終改行なし（L10） | L31、L58 | FR-2（L74–76） |
| 3. UTF-8/全読込み失敗exit2、無結果/HTML/Traceback、本文exit1維持（L11） | L43、L60 | FR-4（L86–90） |
| 4. 既存 `\w+` 全体一致、受理/不正例、ファイル名/行番号、本文分割維持（L12） | L31、L59 | FR-2/FR-4（L74–76、L86） |
| 5. 引数検査→除外→本文、除外失敗優先・本文未読（L13） | L43、L60 | FR-4/FR-7（L88–90、L106） |
| 元受入・新依存/外部送信/入力書換え/CI範囲外、後続承認分離（L15） | L15、L61–68 | FR-1–7、RULE-3、Change boundary、冒頭（L17、L68–112、L131） |

採用決定の具体化は元の受入条件を削るものではない。原文の「集計から外す」は、採用済みの「ランキングから外すがHTML元総数から引かない」と整合させて扱った。

## 最終結果

- 入力ごとの照合結果は上記に保存した。修正を要求する未反映事項はなし。
- 原本・コード・既存レビュー・git・Kanbanは変更していない。作成対象はこの照合報告のみ。
- 製品実装・製品試験・仕様承認は未実施であり、本報告はその代替ではない。
