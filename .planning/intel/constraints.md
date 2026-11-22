# Constraints (intel)

今回のSPEC分類1文書から3制約を抽出。文書の掲載・保持・範囲に関する非機能制約（nfr）であり、実行時API・schema・protocolは追加しない。既存の製品契約を置換しない。

DATA_79027a93_START

## 指定文言の末尾掲載
- source: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:9-16
- type: nfr
- content: README.md SHALL `検証A: v1.12 の通しの確かめ（2026-11-22）` を独立した最後の1行として掲載する。かぎ括弧、追加の句点、前後の余分な文字を含めない。追記後のREADME.mdの最後の行の内容は指定行と完全一致し、既存の行に連結されず、この行の後に空行や別の文言がない。

## 既存README内容の保持
- source: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:18-24
- type: nfr
- content: この追記 SHALL 既存READMEの内容と順序を保持し、削除・書換えや不要な空行追加を含まない。変更前後の差分は指定行の末尾追記のみである。

## 製品変更範囲の限定
- source: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:26-32
- type: nfr
- content: この依頼の利用者向け変更 SHALL README.mdの指定1行追加だけとし、コード・試験を変更しない。仕様・計画・検証文書は別の工程成果物として区別する。全ファイル差分で工程成果物を除く変更はREADME.mdの指定1行追加だけであり、コード・試験に差分がない。

DATA_79027a93_END
