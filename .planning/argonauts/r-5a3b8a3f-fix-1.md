# r-5a3b8a3f — gap 1 / task t_0d6af354

## 対象と根拠
- phase 1、OpenSpec r-5a3b8a3f-wordfreq。init.plan-phase 1 は phase_status=Executed、verification.status=gaps_found。phase挿入・新規ingest不要。
- 元の不足は .planning/phases/01-wordfreq-cli/01-VERIFICATION.md の REQ-07 / Success Criterion 5。CI workflow/job不在、対象head成功証拠なし。
- .planning/phases/01-wordfreq-cli/01-CI-GAP.md と 01-USER-SETUP.md は過去時点の記録として保持する。ローカル43件成功・OpenSpec 8/8チェックはCI成功と同義ではない。

## 人の回答とGitで確認した入力
- 人のコメント: CI CPython 3.12 を確定。人のWorkflows権限で .github/workflows/pytest.yml を依頼branchへ追加・push。
- commit: 5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2。現在のworktreeをorigin/argonauts/r-5a3b8a3fに合わせ、workflow原本を読んだ。
- 原本: name pytest、push(argonauts/**) と pull_request、job pytest、ubuntu-latest、checkout@v4、setup-python@v5 python-version 3.12、python -m pip install pytest、python -m pytest、permissions contents:read。
- 人の報告: run 44017344659 (pull_request)、44017344584 (push)、上記head、両方completed/success、43 passed。
- 上記runとログの成功は人の報告であり、architectがActionsを独立検証した事実ではない。後続品質が対象headとCI証拠を一回読みで照合する。待機ループ禁止。

## 残余gapの計画範囲
- 既存01-01〜04の実装を繰り返さない。必要な追加PLANは既存実装上でCI引継ぎを整え、品質の再検証へ渡す範囲だけ。
- Builderは人の回答・Git上のworkflow・過去の未完記録の関係を正確に記録し、人の設定済み部分と品質未検証部分を区別する。手順書を再作成しただけでREQ-07完了にしない。
- 品質は最新の対象headでローカル全試験を独立実行し、Actionsのworkflow/job/head/event/Python版/全件成功ログを有限回読みで確認する。既存のrunは5c9d8fa時点の証拠であり、後のdocs commitのCI成功を推定しない。
- Actions未報告/pendingは成功としない。要求を緩和せず、後続品質の公式gaps判定へ返す。失敗時も結果を記録し、CI待機ループや再実行自動化を作らない。
- Botはworkflowを変更・pushしない。人の権限変更も不要。workflow修正が必要なら人へ回す。
- REQ-07を満たしたという最終判定、VERIFICATION.mdのpassed化、REQ-07 checkbox更新は品質の独立再検証後。計画段階では行わない。
- 継承GIT_* / global Git設定隔離と非UTF-8 stdoutは非阻害の観察のみ。必須修正や新機能にしない。

## 実行・検査の条件
- PLANは最大3 task。各taskのautomatedは実在する試験ファイルへ標準コマンドを使い、必要な新規検証ファイルはそのtaskまたは先行taskで作ると明記。
- 各automated直後にfails_whenで非ゼロ終了など観測可能な失敗方向を明記。ローカルpytestでCI成功の代用をしない。
- 依頼branchへ先行PLANと今回PLANを直列に積む。タスク終了時にその時点の成果物で検証でき、phase検証は全先行成果物が同じbranch上に揃った状態で行う。
- 追加PLANはOpenSpec task 3.3のCI gap follow-upとして対応付ける（新しいOpenSpec taskを勝手に追加・既存taskを再実装しない）。
- 受入用証拠: 元のVERIFICATIONとcli証拠の添付はフック拒否のためGitのみ。cli原本は .planning/argonauts/t_3dc4a405/cli-evidence.md（.planning/archive-noneは誤記）。品質は今回の証拠添付可否または不能理由を明記する。
