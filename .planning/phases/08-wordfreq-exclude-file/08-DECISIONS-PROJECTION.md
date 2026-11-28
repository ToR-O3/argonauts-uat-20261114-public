# Phase08 decision-coverage用の計画監査投影

原本は08-CONTEXT.mdのD-01〜08。公式gateが原本の`### D-NN:`見出しを抽出できずcould-not-parseを返したため、同じ8判断を公式parserのbullet形式へ投影した計画監査原本。原本CONTEXTや製品判断は変更しない。下記のgate結果はこの投影に対する参照網羅であって、原本parse障害そのものの修正ではない。実装・試験合格でもない。

<decisions>
## Implementation Decisions

- **D-01:** 共通除外と最後FILE（REQ-28 / EX-1）。任意の--exclude FILEで一致語の全出現を外す。全形式共通、重複無影響、最後FILEだけ読み以前は読まない。残存回数/相対初出順/順位維持。Zoo apple APPLE zoo banana/apple→zoo2,banana1、zoo除外/top1→apple2。beta apple alpha/apple→beta1,alpha1。無一致/空/コメントのみは未指定同じ。missing→valid成功、逆順失敗、最後空は前一覧無効。
- **D-02:** 行解釈（REQ-29 / EX-2）。UTF-8先頭BOM除去、strip後空行/先頭#行無視、LF/CRLF/最終改行なし。その他は行全体一語、分割/記号除去/途中#コメントなし。無視項目は直接試験の集合にも入らない。foo barはfoo/barに無影響、foo_bar/123は一致語だけ、foo-barは本文foo/barに無影響、apple#noteもapple/noteに無影響。本文抽出規則不変。
- **D-03:** casefold（REQ-30 / EX-3）。本文既存casefold維持、有効除外行もcasefold。lowerへ変えない。Apple/APPLE/appleとaPpLe、実際のStraße/STRASSE一致を試験する。
- **D-04:** 読込失敗と順序（REQ-31 / EX-4 / AD-4）。既存引数検証→採用除外FILE→本文。除外不存在/権限不足/ディレクトリ/不正UTF-8等は対象と原因をstderr、exit2、stdout空。文言完全一致なし。不正top/min-count/format/値欠落等はファイル未読で既存エラー。両FILE失敗は除外2で本文未読。除外成功後/未指定の本文だけ失敗は既存1。直接/CLI両方で順序を確認。
- **D-05:** 説明と試験（REQ-32 / EX-5）。help/READMEに構文/一覧形式/行規則/casefold/最後FILE/読込失敗exit2/空結果、README実CLI再現例。OpenSpec1.1完了は再実行せず、未完2.1正常/2.2異常/3.1統合をPLAN対応、未実装をチェックしない。
- **D-06:** 空結果と未指定互換（REQ-33 / EX-6）。全語除外text空、json []と末尾改行、HTML既存空表/既存案内/総数0、全形式exit0・専用案内なし。未指定の本文読込/抽出/casefold/全形式/同数初出順/min-count/top/空結果/エラーを維持し既存全件を通す。
- **D-07:** 証拠と範囲（REQ-34 / RULE-2）。追加依存/権限変更/外部送信なし。品質が対象headで独立実行しコマンド/環境/入力/stdout/stderr/exit/条件別結果をVERIFICATION.md等の文字原本へ保存・標準添付。画像は品質が全画像実閲覧して枚数/内容/結果を文字化、PMへ画像/圧縮閲覧を要求しない。OQ7/8は背景不足のみで新条件/停止理由にしない。旧学びの語昇順でなく現行初出順を優先。
- **D-08:** 処理順とHTML総数（REQ-35 / RULE-1 / HTML-2）。全形式除外→計数→min-count→top→既存formatter、総数は除外後かつ選択前countsの回数和、種類数/表示行和ではない。Zoo apple APPLE zoo banana/apple/min2/top1→zoo2/総数3（5でも2でもない）。未指定の従来総数維持。basename限定/escape/自己完結/外部通信なし/明背景/既存レイアウト継承、再設計しない。
</decisions>
