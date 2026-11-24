# Structure review

本書は、実装担当・品質担当・PMが、READMEへの `--min-count 3` の例追加、同じ入力による3形式の検証、文字証拠による受入の範囲を共有するための仕様書である。

対象: `_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md`

適用条件: reader_type=humans、Microsoft Writing Style Guide、internalの小さなREADME仕様。構造モデルは Strategic/Context (Pyramid)。結論と変更範囲を先に示し、詳細と根拠を後に置く。指定テンプレートの見出し・要件・識別子・判断内容は維持し、本文の重複短縮を優先する。以下は提案のみで、対象本文は編集していない。

計測: `uv run /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/skills/bmad-review/scripts/word_metrics.py _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md` を実行し、終了コード0。全文3,526 words。日本語を含むため、この値は同スクリプトの計数単位であり、文字数ではない。削減量は各節の実測値を基準とする推定で、改稿後の実測値ではない。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | §Document purpose、§Vision（L31–41、154 / 175 words）。冒頭では入力資料の一覧が先に現れ、今回の変更・検証・受入の全体像は後の段落と各節に分散する。 | MOVE: §Vision第2段落の「例1つ・同じ入力と閾値で3形式を実行・文字証拠で受入」という概要を、§Document purposeの目的文直後へ移す。仕様段階で未実行である旨を隣接させ、入力資料一覧はその後に置く。§Visionの見出しと目的説明は維持する。 | 人間の読者が出典一覧より先に依頼の全体像と実施状況を把握できる。移動元には同じ概要を残さず、全文の語数影響は0。テンプレートの節順は変えない。 |
| structure | §Non-goals、§MVP scope、§Change boundary、§API contract and versioning（L91–119、212 / 205 / 182 / 79 words）で、READMEだけの変更、機能・公開CLI・依存・試験を変えないことが反復される。 | CONDENSE: 変更禁止事項の正本をRULE-1、具体的な既存出力契約の正本を§Change boundaryとする。他節は参照とその節固有の内容に絞る。§Non-goalsには全面改稿・視覚品質再設計・専用節を設けない対象、§MVP scopeにはFR-1〜FR-3・延期なし・リスク・一時データの扱い、§API contract and versioningには新API・互換性移行不要と既存起動表記を残す。 | 計678 wordsの範囲から約80 words削減。禁止範囲や対象外事項そのものは削らず、同じ制約を複数の説明文で言い直す箇所だけを参照に置き換える。見出しはすべて維持する。 |
| structure | §Success metrics（L103–109、292 words）はSMごとにFRとの対応を示した後、FRの達成条件を再説明する。 | CONDENSE: SM-1〜SM-3を、識別子・対応FR・現状・目標・対抗指標の短い一覧に整理する。目標の詳細は対応FRを参照し、「例0→1」「3形式の終了コード0と照合成功」「3形式の原本参照可」という判定の要点は残す。現状の未実施・未作成、対抗指標の各項目、受入条件であって事業効果ではない旨も維持する。 | 実測292 wordsから約70 words削減。判定に必要な現状・目標・失敗防止指標は保持し、FR全文の再説明だけを短くする。表にする場合も詳細な入れ子を避け、走査性を優先する。 |
| structure | §Decisions（L129–133、230 words）はFR-1のコマンドとRULE-2の工程指定を再掲してから理由を述べる。 | CONDENSE: コマンドはFR-1、工程指定はRULE-2への参照に置き換え、既存入力名・起動表記の維持、top不要、既定textで例自体を検証する理由は残す。利用者指定という出典、Architecture不要の理由、epic後のPRD見直し・変更時のUpdate・未承認拡張禁止、BriefとPRDのVisionの区別も維持する。 | 実測230 wordsから約50 words削減。決定そのものではなく重複する記載を縮め、判断理由と更新方針を見つけやすくする。 |
| structure | §Users and journeys（L43–49、213 words）は、冒頭の「架空の実名利用者による物語は作らない」という作成方針と、各項目の「FR-Nがこのneedを満たす」という反復を含む。 | CONDENSE: 見出しは維持し、README読者→例を見つけて実行（FR-1）、実装・品質担当→同じ条件で形式を確認（FR-2）、PM→文字原本で根拠確認（FR-3）の3項目にまとめる。作成方針の説明を省き、各項目の末尾に対応FRを添える。 | 実測213 wordsから約40 words削減。実名や架空の物語を追加せず、役割・行動・要件対応は維持する。後の§Storiesにある担当別の責任分担とは役割が異なるため、節そのものは削らない。 |
| structure | §Features and requirementsのコマンド例・入力条件・証拠項目（L60–82、116 / 248 / 215 words）、§Change boundaryの形式固有契約（L115）、§Storiesの受入停止条件（L127）。 | PRESERVE: 実行例と、その例と同じ入力を用いる条件、閾値以上・未満の両方を観察する条件、証拠の具体的な記録項目、HTML総数の解釈、担当別責任と受入停止条件は詳細のまま保持する。 | 語数影響0。小さなREADME変更でも、これらは別々の誤実装・誤受入を防ぐ情報であり、真の重複ではない。コマンドブロック、短い段落、FR別の小見出しは人間向けの視覚的な足場として機能している。 |

## Summary

6件の指摘: MOVE 1件、CONDENSE 4件、PRESERVE 1件。本文変更を提案するのは5件で、残る1件は維持の明示。

全提案を採用した場合の推定削減量は約240 words（80 + 70 + 50 + 40）、全文3,526 wordsの約6.8%。推定残量は約3,286 words。数値の長さ目標は指定されていないため、目標達成の判定は行わない。

見出し固定のため、節の統廃合や目次の削除による大幅短縮は提案しない。節をまたぐ参照が増える点は短縮とのトレードオフになるが、冒頭の概要と§Storiesの受入要約は残し、読者の全体理解を支える。要件・制約・判断理由・具体例を削ることによる短縮は含めていない。
