# 未決事項（r-774f3cd6）

## OQ-1：連結元のdescriptionが現物に無い

何が起きたか：依頼branchのpyproject.tomlには `[project].description` がなく、「既存値への追加」という前提を確認できない。
決めてほしいこと：正しい連結元の値と対象、またはdescription新設を許可するか。
選択肢と結果：①既存descriptionを含む正しい対象・元値を提示する（その値への追加として仕様を確認する）。②description新設と、その元値・完成値を明示して承認する（受入条件と仕様を改訂する）。③依頼を取り下げる（製品は変更しない）。

- 依頼者の原文：「pyproject.toml の [project] の description の末尾に『 (UAT)』を足す。変えるのは pyproject.toml だけ。未決事項は無い。」
- 選択肢①ではrepo・branch/commit・ファイルパスを特定し、提示された元値と現物descriptionの一致を確認する。基準を変更する場合は下記commitの置換を記録する。選択肢②ではBrief・PRD・OpenSpecの受入条件を整合して改訂してから実装する。
- 実装前commit：`b34cba0d008923e7f5267ce52d5403492ea53925`。現物と `git show origin/argonauts/r-774f3cd6:pyproject.toml` を照合した。
- `[project]` の項目はname、version、dependenciesのみ。空文字への補完、nameからの生成、新設は承認されていない。
- Brief Q-1、PRD OQ-1、OpenSpec proposal/design/tasksの同一項目。重複した質問ではない。
- 後続仕様承認PMが1回にまとめて依頼者へ確認する。回答前は製品を編集せず、実装・最終受入を承認しない。
- BMADはpartial/draft。OpenSpec planning completeは成果物の存在確認であり、OQ-1の解決や製品実装の合格を意味しない。
