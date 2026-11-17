---
title: wordfreq HTML出力 PRD
template: prd
version: 1.1.0
status: final
created: 2026-11-17
updated: 2026-11-17
---
# wordfreq HTML出力 PRD

## Table of Contents
- [Document purpose](#document-purpose)
- [Vision](#vision)
- [Users and journeys](#users-and-journeys)
- [Glossary](#glossary)
- [Features and requirements](#features-and-requirements)
- [Rules](#rules)
- [Non-goals](#non-goals)
- [MVP scope](#mvp-scope)
- [Success metrics](#success-metrics)
- [Quality and constraints](#quality-and-constraints)
- [Change boundary](#change-boundary)
- [API contract and versioning](#api-contract-and-versioning)
- [Developer experience](#developer-experience)
- [Decisions](#decisions)
- [Open questions](#open-questions)
- [Assumptions](#assumptions)

## Document purpose
依頼 r-50053edc の仕様承認PM・計画担当・実装担当・品質担当が使う機能追加の要求文書。入力はカードt_db216d64の全文とAC1–AC6、同じ依頼の `../brief/brief-wordfreq-html.md`、現行 `openspec/specs/wordfreq-cli/spec.md` と `wordfreq/`。前の受付の未完了成果は引き継がない。本書の要求は今回の追加と変更だけを定め、現行仕様の同数時語順を明示的に置き換える。
原文はuat-publicボードで `kanban_show(task_id="t_db216d64", board="uat-public")` により取得する。FR番号は本PRD内の識別子であり、現行OpenSpecの同番号とは区別して引用する。変更名は `r-50053edc-wordfreq-html` とし、人の判断が必要な未決だけをまとめて仕様承認PMへ渡す。現在は該当なし。

## Vision
ファイル集計結果を、通信のない1枚の静的HTMLとして保存しブラウザで確認できるようにする。入力の文脈と順位表を一緒に読め、スマートフォン幅でも内容を失わない。新しいサービスや対話UIにはしない。

## Users and journeys
単独CLI利用のため人物を創作した詳細journeyは省略する。利用の流れはファイル指定→stdoutをHTMLへ保存→ブラウザでファイル名・総数・表を読む（FR-1、FR-2、FR-4）。品質担当は検証対象headの実CLIでHTMLを独立生成して検証する（FR-6）。

## Glossary
- 単語: 現行のUnicode `\w` 最大連続部分をcasefoldした値。特殊文字を通すために認識規則を変えない。
- 初出順: 正規化後の同一語として、入力トークン列で最初に出現した位置の昇順。
- 総出現回数: 入力全体の全単語の回数の総和。種類数でも表示行の回数の和でもない。
- basename: 実行環境のパス規則でディレクトリを除いた入力ファイル名。
- 順位: topで選ばれた表示行の1始まり連番。同数でも同順位にしない。

## Features and requirements
### FR-1 静的HTML（AC1）
利用者は `python -m wordfreq <file> --format html` でstdoutに1枚のHTML文書を取得できる。順位・単語・回数の見出しと表を持ち、UTF-8として日本語のファイル名を表示できる。必要なスタイルは内部に持ち、スクリプト・外部リソース・外部通信に依存しない。正常終了はexit 0で、stdoutに説明ログを混ぜない。

### FR-2 入力情報と総数（AC2）
basenameのみと総出現回数を表より前に表示する。ディレクトリはHTMLのtitleや属性を含め埋め込まない。top既定10、正の整数Nの制約を保ち、表だけを上位N種類へ制限する。空入力でもbasename・総数0・見出しを持ち、データ行は0件。
検査例: `zoo apple zoo banana apple cherry` の総数は6。top 1ではzoo 2のみ、top 2ではzoo 2、apple 2、top 10では4行で、総数はいずれも6。別入力 `beta beta beta alpha gamma alpha delta` は総数7、top 2はbeta 3、alpha 2。

### FR-3 全形式の並び順（AC3）
回数降順の後、同数は初出順を適用し、最後にtopで切る。text・json・htmlで、語と回数の組が同じ順序で出力される。`Zoo apple APPLE zoo banana` は正規化後zoo 2、apple 2、banana 1、top 1はzoo。語の昇順ならappleが先になるため、旧仕様を残す実装はこの試験で失敗する。初出位置は正規化後語の最初の出現から決め、後の再出現で更新しない。

### FR-4 小画面で読める表（AC4）
背景は明るい色だけ、テーマ切替は設けない。順位は1からの表示行連番。通常幅と少なくとも320 CSS pxで、空・通常・長い連続語・長いbasenameを含め全内容が読め、ページ全体の横はみ出しや切取り、隣接内容との重なりで表が崩れない。折返しを許し、省略記号や切取りによる情報欠落を合格としない。
文字範囲そのもの（各テキストのRangeの矩形と行断片）、viewport・要素矩形・切取り祖先矩形を実測原本として残す。判定は横方向の収まり、切取りを行う祖先内の収まり、隣接内容との非重複、実画像で読めること。要素自身への厳格な縦包含は必須条件にしない。測定値を合格に見せるため改変せず、要素自身の縦のはみ出しがあれば値を残し、切取り・重なり・可読性への影響で判断する。

### FR-5 安全性と既存動作（AC5）
単語とbasenameをHTMLテキストとしてエスケープし、`& < > " '` を含むデータで表示文字が保たれ、タグ・イベント・スクリプトを生成しない。CLIの単語は認識規則で制限されるため、整形部品の直接試験で特殊文字を含む語を与え、実CLIでは特殊文字を含む有効なbasenameを用いる。basenameへパス区切りは含めず、入力認識を緩めない。
現行の入力取得境界、UTF-8読込み、Unicode抽出とcasefoldを維持する。ファイル個数エラー・不正top・不正formatはexit 2、読込み/デコード失敗はexit 1とする。いずれもstderrにエラーを出し、結果HTMLは出さない。textは `count\tword\n`、jsonはword/countオブジェクトの配列と末尾改行を保ち、空ではtextが空・jsonが `[]` と改行。同数時順序以外の不要な構造変更をしない。

### FR-6 条件別の検証証拠（AC6）
自動試験でFR-1–FR-5の通常・空・top既定/1/境界/種類数超過・不正値・Unicode・注入・エラー回帰を検査する。品質担当が対象headの実CLIから独立してHTMLを再生成し、通常幅と320 CSS pxを含む画面をブラウザで確認する。head、入力の原本、実行コマンド、exit/stdout/stderrと期待値、生成HTML、ブラウザ/viewport、文字範囲の測定原本、実画面画像、外部通信の検査結果を保存・添付し、ACごとの合否と対応付ける。Builderの画像や自動判定だけを品質の独立確認の代用にしない。実行できなかった条件を合格扱いしない。

## Rules
- RULE-1: 外部通信・外部依存のない静的HTMLとし、データは表示文字であって実行可能コードにしない。
- RULE-2: 旧同数時昇順からの変更は意図した互換性変更として利用説明と試験へ明記する。
- RULE-3: CIの追加・変更を行わない。既存CIの構成をこの依頼のために拡張しない。

## Non-goals
生成日時、暗色、テーマ切替、対話操作、Webサーバー、標準入力・URL入力、形態素解析、単語認識の変更、ランタイム依存追加、CI追加・変更。

## MVP scope
FR-1–FR-6を同じ変更で提供する。すでに限定された機能追加であり、UI・安全性・証拠を後回しにして範囲を削らない。

## Success metrics
SM-1: FR-1–FR-6の自動試験と品質の独立ブラウザ確認が条件ごとに合格し、証拠が追跡可能になる。現状は未実施。保護指標は既存回帰の成功、text/json構造維持、外部通信0、CI差分なし。利用人数等の事業数値は要求されていない。

## Quality and constraints
RULE-1をHTML構造検査と実ブラウザの通信記録で検証する。無通信は単にオフラインで成功したことだけでなく、外部リソース参照がないことと外部通信の試行がないことも確認する。ローカル文書を開くための読み込みと外部通信は区別する。FR-4の実画像と幾何条件の両方が必要。

## Change boundary
追加はhtml形式と関連するメタ情報。変更は全形式の同数時語順。既存のtop制約・入力・部品分離・text/json書式・標準ライブラリのみの実行を維持する。HTML用メタ情報をtext/jsonへ追加しない。

## API contract and versioning
CLIのformat選択肢へhtmlを追加する。text/jsonの同数時順序は破壊的な期待値変更であり、旧語順に依存する利用者・テストは初出順へ更新する。移行フラグは追加しない。

## Developer experience
使用例 `python -m wordfreq input.txt --format html --top 3 > result.html` を説明文書へ追記する。エラーは従来どおりstderrへ分離する。詳細なテストコマンド・UI設計・実装の順序は承認後の計画で決める。

## Decisions
明るい背景、切替なし、3列表、順位は表示行連番、basenameのみ、top前総数、全形式の初出順、FR-4の画面判定方法は決定済み。Architectureの別成果物は不要。既存の小規模な部品境界を維持し、OpenSpec designに局所設計を記録する。
AI評価・企業横断rollout・サービス運用・法規制・SLO・ハードウェアは該当しないため専用節を設けない。Consumer migrationはAPI contract節で扱い、Storiesは本書から重複生成しない。

## Open questions
人の判断が必要な未解決項目はない。実装・試験・ブラウザ確認は未実施であり、合格の宣言ではない。

## Assumptions
[ASSUMPTION: Users and journeysとVisionでは、詳細属性が未提供のため、既存CLI利用者によるローカル閲覧という説明上の仮定だけを置く。]実装者が選べるレイアウト・検証手段は今回の製品判断の未決事項とはしない。
