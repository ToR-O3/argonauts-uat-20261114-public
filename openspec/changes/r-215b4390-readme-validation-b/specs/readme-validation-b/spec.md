# Spec Delta

## Purpose

README.md の末尾に依頼者が指定した検証Bの1行を記載するという、文書上の状態を定義する。記載自体は検証合格を意味せず、製品の新しい振る舞いは要求しない。

## ADDED Requirements

### Requirement: README末尾の指定行

README.md の末尾には、`検証B: v1.12 の通しの確かめ（2026-11-22）` が引用符なしの独立した1行として1回だけ存在しなければならない（MUST）。

#### Scenario: 追記後のREADME

- **WHEN** 本依頼の文書追記が完了したREADME.mdを読む
- **THEN** 指定行が独立した最終行として存在し、README.md全体での出現は1回である
