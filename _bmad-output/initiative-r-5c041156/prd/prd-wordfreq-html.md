---
title: "wordfreq HTML出力 — PRD"
template: prd
version: 1.1.0
status: draft
created: "2026-11-17"
updated: "2026-11-17"
---

# wordfreq HTML出力 — PRD

## Table of Contents

- [Document purpose](#document-purpose) — 読者・入力・承認境界
- [Vision](#vision) — ブラウザ閲覧という目的
- [Users and journeys](#users-and-journeys) — 利用者仮説・利用の流れ
- [Glossary](#glossary) — 語・総数・初出
- [Features and requirements](#features-and-requirements) — FR-1〜4
- [Rules](#rules) — RULE-1〜3・共通契約
- [Non-goals](#non-goals) — 範囲外
- [MVP scope](#mvp-scope) — 最小変更と設計への引継ぎ
- [Success metrics](#success-metrics) — SM-1〜4・受入証跡
- [Quality and constraints](#quality-and-constraints) — RULE-4〜6・安全性と可読性
- [Change boundary](#change-boundary) — 維持・追加・互換性変更
- [Decisions](#decisions) — 採用済み判断・省略理由
- [Assumptions](#assumptions) — A-1〜3・未承認の仮定
- [Review refinements](#review-refinements) — 独立レビュー後の受入具体化案
- [Open questions](#open-questions) — OQ-1〜4・PMの一括確認

## Document purpose

Builder・品質・仕様承認PM向けの小変更PRD。initiative配下だが、単一機能の受入境界を定める。FR/RULE/SMは旧specと別の本PRD内IDである。

入力は`../brief/brief-wordfreq-html.md`（partial/draft）と同所`.memlog.md`、リポジトリルートの`openspec/specs/wordfreq-cli/spec.md`、`wordfreq/`全実装、`CONCEPTS.md`、依頼全文・固定制約。initiativeファイルは題名のみで、承認済みRequirementsはない。本書は実装完了も仕様承認も主張しない。未承認のA-2/A-3と未決の背景・順位列を残すためdraftとする。

## Vision

wordfreqの集計結果を、利用者がstdoutから保存した1枚のHTMLで読めるようにする。単語と回数だけでなく入力名と総数を表の上に示し、スマートフォンでも結果の文脈を失わない。変換アプリやWebサーバは必要としない。

根拠は今回の依頼で、実績・時間削減・期限のデータはない。閲覧・共有の価値は未検証のA-1である。

## Users and journeys

A-1の利用者は、既存CLIでUTF-8ファイルを集計する人。利用者は、ファイルを指定して`--format html`を実行し、stdoutをHTMLとして保存して、ブラウザで入力名・総数・語頻度表を読む想定である（FR-1、FR-2）。実在人物のインタビューではないため人物名や利用頻度は創作しない。既存text/json利用者にはFR-3の順序変更が影響する。ブラウザからファイルをuploadする利用は対象外。

## Glossary

- **正規化語**: Unicode `\w`の最長連続トークンへ`casefold()`を適用した文字列。同一正規化語を1種類として集計する。
- **回数**: 1つの正規化語の入力内出現数。
- **総数**: A-2の推奨解釈では、全入力の正規化トークン出現数。異なり語数でも、topで表示した回数の合計でもない。
- **初出順**: 正規化後の各語が入力トークン列で最初に現れた位置の順。casefoldで同じ語になる表記は最も早い位置を共有する。
- **表示行**: 頻度降順→同数時初出順で並べた後、`--top N`で選んだ語と回数。ヘッダ行は含めない。
- **入力名**: HTMLに表示する入力ファイル名。パスからbasenameのみを出す案がA-3であり未承認。

## Features and requirements

### 自己完結した閲覧結果

- **FR-1**: 利用者は既存のUTF-8ファイル1個を指定し、`--format html`で単語・回数の表を持つ完全な単一HTML文書をstdoutに得られる。保存後にオフラインで読め、サーバ・JS・外部assetを必要としない。正常終了は0。
- **FR-2**: 利用者は表より前に入力名と数えた単語総数を読める。A-2/A-3は承認待ちの提案として実装前に確定する。推奨案では空入力は総数0・表示行0のHTMLとなる。

### 全形式で一致する順位

- **FR-3**: text/json/htmlはすべて「回数降順→正規化後初出順→topによる行制限」の結果を出す。同じ入力・オプションの再実行で同じ結果になる。旧来の同数時語昇順は意図的に置換する。

### 既存利用の継続

- **FR-4**: HTML追加・同数順変更以外のCLI契約は維持する。既定text/top10、textの`count TAB word`と改行、JSONの`word`文字列/`count`整数を持つ配列を変更しない。総数・入力名をtext/jsonへ追加しない。

## Rules

- **RULE-1**: 語の抽出はUnicode `\w`連続、正規化は`casefold()`を維持する。形態素解析や文字単位分割は追加しない。
- **RULE-2**: 入力はUTF-8ファイルちょうど1個。不存在・読取不能・UTF-8不正はstderr/終了1、引数個数不正・非整数または0以下のtop・未知formatはstderr/終了2。失敗時stdoutに結果を混ぜず、入力ファイルを書き換えない。
- **RULE-3**: 入力取得、トークン化、正規化、集計、整形の境界と部品の単体検証可能性を維持する。ランタイムは標準ライブラリのみ、依存追加・変更なし。対象Pythonは既存CIのCPython 3に従い、バージョン横断対応を拡張しない。

## Non-goals

Webサーバ、upload、stdin/URL入力追加、対話sort、graph、theme切替、依存変更、CI追加・変更は範囲外。既存CIの実行や既存試験の維持を削除する意味ではない。ファイル本文の表示、入力の編集、共有先への自動送信も追加しない。背景の明暗を選ぶこととtheme切替の実装は別であり、前者は未決、後者は範囲外。

## MVP scope

含むのはFR-1〜4、共通契約、安全な出力、モバイル可読性、および順序変更に対応する仕様・説明・試験の整合である。すでに小さな指定変更なので要求は削らず、将来機能や新たなリリース約束は作らない。

独立Architectureはこの小変更には不要という判断を引き継ぐ。データの受渡し方・formatterの署名・CSS等の設計詳細は後続OpenSpec designへ置く。本工程はPRDのみで、PLAN・OpenSpec・コード・CONCEPTS・CIを編集しない。Builder・品質は実在する検証ファイルを用いて検証を実行し、計画中に未作成の検証コマンドを試さない。

## Success metrics

実装前の受入目標であり実行結果ではない。現状はHTMLなし・同数時語昇順。全目標を満たし、OQ-1〜4の承認を得るまで実装受入完了としない。

- **SM-1**: FR-1・FR-2 — `Zoo apple zoo APPLE beta`のHTMLは、A-2承認時、総数5、全件の表示は`zoo:2, apple:2, beta:1`。top1でも総数5、表はzooの1行。空入力は総数0・データ行0、終了0。総数の正しさを表示行合計で代用しない。
- **SM-2**: FR-3 — 同じ例をtext/json/html全形式で照合し、top1の境界でappleでなくzooが選ばれる。casefold衝突例`ZOO Straße zoo STRASSE beta`は`zoo:2, strasse:2, beta:1`、top1はzoo。同一入力を異なる`PYTHONHASHSEED`で再実行し、形式ごとに、シード値を変えても出力が一致することを確認する。頻度が異なる語では初出より頻度が優先することも確認する。
- **SM-3**: FR-1・FR-2 — 実ブラウザのviewport幅320px・375px・1280pxで、空白のない長語と長い入力名を含む結果を開く。全語・回数・入力名に欠落、重複、重なり、切捨てがなく、語と回数の対応が読めること。画像に加えてブラウザ/version・viewport・DOM/layout測定とnetwork記録を保存する。画像だけで全内容の存在を判断しない。
- **SM-4**: FR-4 — 全形式の通常・空入力・top省略/指定/語種数超過、Unicode/casefold、RULE-2のエラーとstdout/stderr/終了値、入力不変、部品単体・入力境界越しの回帰を確認する。空textは空出力、空jsonは`[]`。カウンターメトリクスとして、HTML表示成功のために既存text/jsonの構造や安全性を犠牲にしない。回帰不一致・外部要求・実行可能な注入は0件を目標とする。

## Quality and constraints

- **RULE-4**: 語と入力名はHTML出力境界でescapeし、`& < > " '`やscript/event属性相当を文字として扱う。既定tokenizerが記号を除くため、特殊文字入り語をformatterへ直接渡す単体試験と、悪意あるfilenameでCLIから生成するE2Eの両方を必要とする。実ブラウザで、語や入力名に含まれる文字列がDOMのタグとして解釈されず、スクリプトやイベントハンドラとして実行されないことを確認する。
- **RULE-5**: 出力HTMLにJS・外部CSS/font/image等のasset・外部通信はない。ローカルファイルを開く実ブラウザのnetwork記録で外部要求0件を確認する。製品HTMLのオフライン性をPRD資料ビューの挙動で代用しない。
- **RULE-6**: UIは簡素な表で、SM-3の幅でも長語・入力名を省略せず読める。配色と順位列はOQ-1/OQ-2の回答まで仮の製品既定を置かない。共有HTMLには語と入力名が残るため共有前確認を説明する。basenameでも機密名・個人名は匿名化されず、同名ファイルを区別できない場合がある。

## Change boundary

追加はhtml形式とHTML内の入力名・総数。変更は全形式の同数順位とtop境界で選ばれる語。旧specのFR-4/D-2と`CONCEPTS.md`の「決定論的順位」は旧契約なので、後続変更で仕様・実装・試験・利用説明を同時に整合させる。旧契約との不一致は入力間の矛盾ではなく、今回明示された変更である。

CLI公開面は`--format text|json|html`となる。自動処理の同数順依存やスナップショットは更新対象として説明するが、旧順序併用オプション、JSONメタデータ、版番号・非推奨期間は新設しない。エラー処理、入力境界、tokenizer差し替え後のcasefold責務は変更しない。

## Decisions

採用済みはHTML追加・全形式の初出順変更・CI/依存変更なし・独立Architecture不要。未決のUIとA-2/A-3は仕様承認PMが人へ一括確認する。承認前のOpenSpec案にも未決の状態を保持し、回答は仕様修正の工程でBrief・PRD・OpenSpecの定義・例・検証条件へ反映して再承認する。無人実行のため質問を送信したとは主張しない。

任意章のAPI契約・移行・開発者説明はChange boundaryへ、StoriesはSuccess metricsへ、ExperienceはQualityへ統合。AI・複数チーム・外部連携/SLO・規制・hardwareは非該当で省略。実装後の学びと人の回答で本PRDをUpdateする。

## Assumptions

- **A-1**: Vision・Users and journeys — CLI結果をブラウザで閲覧・共有する人という利用者像と変換負担は未検証。PMが初回利用フィードバックで再確認する。利用者属性の追加質問は今回の機能境界を変えないため承認ゲートから外す。
- **A-2**: FR-2・SM-1・Glossary — Brief A-2を継承。総数はtop前の全正規化token出現数を推奨するが未承認。OQ-3で確認する。
- **A-3**: FR-2・RULE-6 — Brief A-3を継承。表前の入力名はbasenameを推奨するが未承認。OQ-4で確認する。

## Review refinements

以下は独立レビューを受けた設計・受入の具体化案で、利用者の追加要求を装わない。仕様承認の対象とし、配色・順位列を確定しない。

- HTMLはUTF-8で保存し、headのcharset宣言と保存バイトを一致させる。通常のUTF-8 stdoutを対象に、日本語の語・入力名を保存して文字列一致を検証する。非UTF-8 stdoutは既存Pythonの出力規則を維持し、利用説明で`PYTHONIOENCODING=utf-8`を指定した保存例を示す。新しい文字コードオプションは追加しない。
- 意味的なtable、thead/tbody、語と回数の列見出し（scope=col）を持つ。viewportメタ情報を含め、mobile emulationまたは実端末で実際のCSS viewport幅320/375を確認する。1280pxも確認する。200文字連続の語と長い日本語入力名を固定データにし、語・名前は折り返して省略せず、ページ・表とも横スクロール不要、回数列との重なりなしとする。縦スクロールは許す。
- 名前の連続スペース・タブ・LF/CR/CRLFは表示時も保持する（pre-wrap等）。HTMLの改行正規化でもCRを失わないよう設計し、escape試験は`&amp;`相当も含め、DOMのtextContentが元の語・承認済み規則で得た入力名と一致することを検証し、二重escapeと削除を防ぐ。
- 空白・句読点だけの非空入力も総数0・データ行0（text空、json空配列）、終了0とする。保存は必ず入力と異なる出力ファイルとし、同一パスへの`>`はシェルが入力を先に消すことを利用説明に明記する。
- ブラウザ証跡の手段は計画で既存環境を確認し、品質が実HTMLを開いて画像、DOM/layout測定、ブラウザ版、幅、外部request 0の記録を残す。ブラウザ手段がなければ未検証として人へ回し、CIや依存を追加して迂回しない。
- OQ-2で順位列を付ける場合、順位を行番号とするか同数同順位とするかも同じ回答で確定する。OQ-3/OQ-4が否認・条件付きなら推奨案を実装せず、代替案の期待値へGlossary・FR-2・SM-1/3とBriefを更新して再承認する。

## Open questions

仕様承認PMが人へ以下を一括質問し、各項目の回答を別々に記録する。必要時点はOpenSpec仕様承認・実装着手前であり、無回答を同意としない。

- **OQ-1**: 背景は明るいものか暗いものか。担当は仕様承認PM、影響はFR-1/RULE-6の見た目の承認。
- **OQ-2**: 順位列を付けるか。付けるなら表示行の連番か、同数同順位かも同時に確定する。担当は仕様承認PM、影響はFR-1/RULE-6の列構成。語と回数の2項目は必須のまま。
- **OQ-3**: 総数をtop前の全入力token出現数とするA-2でよいか。`Zoo apple zoo APPLE beta`はtop1でも総数5（表示zooの回数2ではない）を推奨する。担当は仕様承認PM、影響はFR-2/SM-1の受入確定。
- **OQ-4**: 入力名をbasenameのみとするA-3でよいか。フルパスのディレクトリ露出を避ける一方、basename自体の機密性と同名ファイル識別の制約がある。担当は仕様承認PM、影響はFR-2/SM-3の表示規則確定。
