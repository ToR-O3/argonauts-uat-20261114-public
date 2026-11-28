# PRD — rubric walker 原本

入力: prd-wordfreq-exclude.md、.template.md、.memlog.md、Brief、source-context、open-questions。基準は公式rubric-planning、PRD done when。stakes=既存ローカルCLI単一機能、feature altitude。subagent不可の逐次fallback。

判定: 小さい機能に必要な観測可能要求と互換境界がある。製品未決を決めない限り実装用finalにはできず、partial/draftが妥当。

重要な対応: 承認待ちを先頭へ、正規表現の二重バックスラッシュを修正、本文と除外FILEのエラー役割を引き続き区別する。

| Dimension | Rating | Finding / disposition |
| --- | --- | --- |
| Decision-ready | adequate | 冒頭のpurposeにpartialの理由を加える。Open questionsだけでは実装可能と誤読され得る。修正対象。 |
| Earned | strong | UJの架空人物や事業KPIを作らず、capability-firstに縮小。 |
| Testable | strong | FRごとに例/観測点があり、Unicode、exit2、stdout/stderr、各形式、未指定互換を含む。 |
| Honest scope | strong | 曖昧行/他の取得失敗/総数/複合失敗は中央一覧へ。推定はタグ付け。 |
| Usable downstream | adequate | 公式idsチェック対象。Glossaryの正規表現がリテラル二重バックスラッシュであり、実装の一重と合わせる。修正対象。 |

Done when: FRはすべて依頼中の必要か既存互換に根拠がある。CLIなので旅程は短縮。Counter-metrics、非目標、変更境界があり、スコープ拡張なし。未決の承認と背景推定の確認だけは無人実行で充足できない。
