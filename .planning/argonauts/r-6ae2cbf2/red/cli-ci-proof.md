# 08-01 実RED記録

表示追加は未実装。製品GREEN・phase合格ではない。
実行head: be231840989079fed532c7372efb66f577e39b09
Python: 3.12.15 (main, Oct  1 2026, 00:00:00) [GCC 14.3.1 20251022 (Red Hat 14.3.1-4)]

環境・正確argv・exit・元stdout/stderrはcommands.json、JUnitはnew-feature.xml/focused.xml。
新機能試験はdisplayed-types欠如、既存CSS試験は新しい局所2規則の欠如で失敗。
text/jsonの全バイト照合は各HTML失敗より先に実行。CIは未確認（ローカル結果のみ）。
