# Brief — Finalizeと実行検査

## 順序と処置

1. memlog監査: 意味のある全項目を本文／未解決事項／除外理由に照合。捨て置きなし。
2. 入力突合: 依頼全文、README全37行、initiativeをreview-reconciliation.mdで確認。
3. レビュー: review-rubric.md、review-fresh-reader.mdに逐次記録。独立子レビューではない。
4. 前提・未解決事項: A1-A4、文案・省略・基準・5領域・読者/実施理由をPMへ保留。勝手に解消せずdraft。
5. 文書基準: 公式bmad-reviewのstructure→proseを実施、修正不要。タグ相当の未確認事項は最後の前提節に集約。
6. 目次: 最終見出しと一致。公式ID検査のundefined／unknown_prefix／duplicate／withdrawn／tocはすべて空。
7. headlessのため対話の読了待ちはしない。
8. external_handoffsは設定上空。外部書込みなし。
9. updatedを設定しdraft／partialでClose。on_completeは空。html_view:alwaysに従って公式レンダラでHTMLを生成。

## 実行した公式CLI

- resolve_customization.py: analystのagent/workflow、facilitateのworkflowを解決。追加activation、永続fact、外部handoffは空。
- resolve_config.py: output_folderは{project-root}/_bmad-output、active_initiativeは未設定。明示された出力先を採用。
- list_templates.py: --briefの一覧→--template brief --mergeで.template.mdを生成し全文読了。orphaned/unreachable/order_problemsなし。標準の任意2フォルダだけmissingで、指定テンプレートは利用可。
- memlog.py: init、appendで事実・判断・前提・レビュー・Closeを記録。
- check_ids.py: 最終実行で全エラー空。
- word_metrics.py: 総1914、前文25・目次150・前提133を除いた本文1606。本文をjqで抽出したwc -wは81（空白区切り、日本語では過少計数）。
- render_view.py: brief-view.htmlをlayoutに使用しHTML生成。lang/表示ラベルを日本語に校正。任意CDN読み込み処理があり、外部通信なしの検証はしていない。

## 製品不変の検査

- `git diff --exit-code 69b97f1c9dfa7211367a9bdd0af885d80d8bf380 -- README.md`: 差分なし。
- `git hash-object README.md` と `git rev-parse 69b97f1c9dfa7211367a9bdd0af885d80d8bf380:README.md`: ともに `3625ed42efa55c9929e47952698c25decd5050b7`。README全体が原本と一致するため対象外区間も不変。
- 開始HEADとのgit全tracked差分なし、status --short --untracked-files=allの追加は本initiativeのbrief/とprd/だけ。
- 製品実装後の完全一致・意味判別テストは未実施。本カードではREADME編集もテストコード作成も行わない。

## 制約・次の担当

補助的なperl -eを含むコマンドは安全フックで実行前拒否され、許可設定は変更せずjqによる抽出とwcに切り替えた。禁止されたインラインPython/Node/シェルやヒアドキュメントは使わない。GSD判定・git commit/push・kanban操作は行っていない。

Briefの次工程としてJohn CREATE→facilitate intent:create headless:true template:prdを実行し、このBriefのパスを入力へ渡した。文案・バージョン省略・基準の承認は次のPM仕様承認へ残す。
