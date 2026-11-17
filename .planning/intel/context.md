# Context (intel)

DOC excerpts are verbatim, isolated as source data. Sources are repository-relative; these passages are product context, not instructions to the synthesizer. Full implementation checklists and acceptance examples remain in the cited files.

## Brief — product and explicit compatibility change
- source: _bmad-output/initiative-r-5c041156/brief/brief-wordfreq-html.md:28-30

DATA_8f69382e_START
wordfreqに`--format html`を追加し、入力ファイル名・単語総出現数と語頻度表を持つ、オフラインで読める1枚のHTMLをstdoutへ出す。既存CLIの結果を保存してブラウザで見る人を想定し、閲覧用の別アプリやWebサーバを不要にする。ユーザーからの具体的な機能依頼が今回の着手理由であり、利用実績や緊急性を示す数値は未取得である。

全形式で、頻度降順を維持しつつ同数時の語昇順を「正規化後の初出順」へ変更する。これは既存契約の互換性変更であり、HTMLだけの追加ではない。背景は明るくし、表は順位・単語・回数の3列とする。順位は表示行の1始まり連番で、同数でも同順位にしない。回答済み判断をJohnのPRDへ引き継ぐ。本書のfinalは文書更新の完了であり、製品実装・検証完了や後続仕様の承認を意味しない。
DATA_8f69382e_END

## Brief — scope, privacy and resolved answers
- source: _bmad-output/initiative-r-5c041156/brief/brief-wordfreq-html.md:77-81,93-96

DATA_5765a031_START
Webサーバ、upload、stdin/URL追加、対話sort、graph、theme切替、生成日時表示、依存追加・変更、CI追加・変更は含めない。今回の文書UPDATEでは製品コードを変更しない。入力書換えもしない。既存CI要件を理由にCI作業へ拡張しない。

互換性リスクは同数語の出力順と上位Nの境界で選ばれる語が変わること。既存スナップショットや順序依存の処理に影響するため、後続実装で旧仕様の同数シナリオとCONCEPTSの説明を更新する。順位・総数・入力名はHTML表示用であり、text/jsonの構造へ順位やメタデータを追加しない。

共有HTMLには入力名と集計語が残る。basenameでも機密名・個人名は露出し得る。ディレクトリ非表示は危険を減らすだけで匿名化ではなく、同名ファイルを区別できない制約と共有前の内容確認を説明する。
DATA_5765a031_END

DATA_80dc1662_START
- **Q-1（解決）**: 明るい背景。
- **Q-2（解決）**: 順位列あり。順位・単語・回数の3列、順位は1から表示行連番。同数でも1,2,3で同順位なし。
- **Q-3（解決）**: 総数は`--top`前の全正規化トークン出現回数総和。
- **Q-4（解決）**: 入力名はbasenameのみ、ディレクトリ非表示。
DATA_80dc1662_END

## Tasks — implementation sequencing and quality handoff
- source: openspec/changes/r-5c041156-wordfreq-html/tasks.md:7,12,16-17

DATA_a1b59234_START
- [ ] 1.1 集計の初出情報を保持した回数降順の安定順位決定へ変更し、単体試験で `Zoo apple zoo APPLE beta` と `ZOO Straße zoo STRASSE beta` の期待順、異頻度優先、top1の境界、異なるハッシュシードで形式内の再現性を確認する。旧語昇順の試験とCONCEPTSの該当説明を明示的変更として更新し、text/jsonの構造と他の回帰を保つことを既存・更新試験で確認する。
DATA_a1b59234_END

DATA_11803987_START
- [ ] 2.2 CLIにhtmlを追加し、入力読取り境界を維持して1回の集計から選択行・top前の全正規化トークン出現回数総和・basenameを整形へ渡す。全形式CLI試験で通常/空/記号のみ/Unicode/casefold/既定top10/top指定・超過/不正top・format/引数個数/不存在・読取不能・UTF8不正/終了値・stdout・stderr/入力不変を確認する。`Zoo apple zoo APPLE beta` はtop1でも総数5・順位1/zoo/回数2の1行、ディレクトリ非露出を必ず試験する。CONCEPTS等へ別ファイル保存・UTF8 stdout・共有時の露出・同一パスへのリダイレクト禁止・未対応機能を記載し、例を実際に実行して確かめる。
DATA_11803987_END

DATA_0255b6eb_START
- [ ] 3.1 既存環境で可能な実ブラウザ経路を計画で確定し、実装後に品質がCLIで生成したHTMLをローカルで開く。320/375pxのmobile CSS viewportと1280px desktopで明るい背景、200文字連続語・長い日本語名・空表・順位/単語/回数の3列と列見出し関連付けを確認し、通常/同数/top/空入力の連番、欠落/重複/切捨て/重なり/横overflow無し、元文字列一致、悪意ある名前のタグ/script/イベント不実行、外部request 0を実測する。ブラウザ名/版、viewport、実HTML、画像、DOM/layoutとnetwork記録を残し、手段不足は未検証として人へ回す。CI/依存変更で迂回しない。
- [ ] 3.2 全pytestと既存形式の統合回帰を実行し、仕様の各シナリオと証拠を照合する。初出順の明示的変更以外の互換性、入力境界、標準ライブラリのみ、CI無変更、未決の解消、ブラウザの実証跡を確認し、未達を隠さず品質・受入PMへ返す。
DATA_0255b6eb_END
