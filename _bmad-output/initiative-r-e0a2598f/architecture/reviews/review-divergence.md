# Spine gate — configured adversary / two-unit lens 原本

設定finalize_reviewersの「全ADに従う二つの下位単位が不整合を作れるか」を実行。入力はarchitecture.mdとPRD/共通未決。別レンズ結果は入力にしない。subagent不可の逐次fallback。これはbmad-reviewのadversarialレンズではなく、設定されたspine固有レンズである。

1. loader側がlower、CLI側がcasefold: AD-2に違反するため両方準拠の反例にならない。
2. formatter側がFILEを読む、CLI側も読む: AD-1に違反。
3. loaderがmissingをInputErrorだけに潰し本文ハンドラでexit1: cause/役割保持とexit2のAD-3に違反。
4. selectionが集合順を出しformatterが別々に並べる: AD-2/AD-4に違反。
5. selectionがtopの後に除外して表示枠を減らす: AD-4に違反。
6. 一方が除外後総数、もう一方が元総数を採用する: 未決の実装ゲートが開いておらず、どちらも承認前に期待値を固定できない。穴をADで埋めるのではなく依頼者回答待ち。
7. 字下げ#や他取得失敗を異なる方針で実装する: 共通未決を採用禁止としたRule/Deferredに違反。

全ADに従い、承認ゲートも守る二者が契約不一致を作る新たな反例は見つからない。ただし未決のまま並行実装へ渡すこと自体は不可。partialを保持する。
