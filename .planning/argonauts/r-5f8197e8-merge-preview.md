# 承認済み文書のmerge差分

- 入力: 仕様承認t_9c048e29 run28、要求・仕様t_38b60b51 run27。manifestの4文書。
- 公式進捗: project/requirements/roadmap/state全true。roadmap.analyze current_phase=1、STATEの位置5。phase1/3/4はstale、phase5はpassed。この履歴は変更しない。progressの通常案内はphase1再検証だが、本カードは承認済み新規依頼の取込みのみである。
- 追加だけ: REQ-25（README例1つと既存内容保持）、REQ-26（閾値3・同一UTF-8入力の3形式実行）、REQ-27（Builder/独立品質の読める文字原本）。既存REQの変更・削除なし。
- 新phaseを公式phase.addで追加し、その番号へ全3要求とOpenSpec1.1/1.2/2.1を対応付ける。新CONTEXTに承認内容を書く。
- PROJECT/STATEは今回の要求・phase追加の記録のみ。設定は開始値維持。コード・README・試験には書かない。
- 衝突報告: BLOCKERS/WARNINGS/INFOすべて0。
- E.7の「承認した仕様の要求追加のみ」のgate回答によりApprove。人の追加判断は不要。
- これは計画用差分の承認であり、実行検証や受入の合格ではない。
