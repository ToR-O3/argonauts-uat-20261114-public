# Fresh-reader review — brief-wordfreq-cli.md

Reviewer read only this brief. Question answered: what must still be resolved to hand this to a planner/spec writer.

## Verdict

This is an unusually complete brief: scope boundaries (WF-01–07), the two previously-open behaviors (D-1, D-2), assumptions (A-1–A-3) and verifiable success criteria are all recorded, so a planner could start from it mostly as-is. The remaining gaps are behavioral details the brief claims are settled but are not: the tokenizer's definition of a "word" (punctuation/character classes), file/encoding/IO error behavior, and a name-collision risk with the PyPI `wordfreq` package — all three should be closed or explicitly delegated before spec writing.

## Top three fixes

1. **Define what counts as a "word" beyond "whitespace-delimited, case-folded."** Punctuation handling (`don't`, `foo.bar`, `(hello)`), the character class allowed in a token, and Unicode normalization are unspecified. Open questions (line 102) claims nothing is undecided, but this is a third open behavior that directly determines output and every acceptance test. Either add a D-3 or state that the spec writer owns it under stated constraints.
2. **Resolve the module name `wordfreq`.** `wordfreq` is an established PyPI library — itself a word-frequency package — so `python -m wordfreq` risks shadowing or being shadowed if that package (or a transitive dep) is installed in the internal repo environment. A-3 (line 98) explicitly admits the PyPI comparison was rushed; a 5-minute name-availability check or a rename decision belongs in the brief before packaging/CI specs are written.
3. **Specify I/O behavior for inputs and errors.** File-not-found, undecodable bytes/encoding (UTF-8 assumed? errors=strict?), empty file, and the exit codes for these are not covered — WF-02/WF-03 only cover invalid flag values. Success criterion 5 (line 73) promises decided behaviors are test-verifiable; these gaps leak straight into the acceptance card.

## Findings

| # | Severity | Location | Finding | Fix |
|---|----------|----------|---------|-----|
| 1 | Medium | Solution line 50; Scope WF-04/D-1 (lines 82, 89); Open questions (line 102) | Tokenizer semantics incomplete: only "whitespace split + case fold" is defined. Punctuation stripping, token character class (digits, hyphens, Unicode letters), and Unicode normalization are undecided, yet Open questions says nothing is open. Output determinism and test fixtures depend on this. | Add a decision (D-3) or an explicit delegation: "token definition owned by spec writer; constraint: deterministic + unit-tested", and remove the "なし" claim's implied completeness. |
| 2 | Medium | Exec summary (line 33); Solution (line 47); A-3 (line 98) | Name `wordfreq` collides with the well-known PyPI `wordfreq` package (a word-frequency library). Stdlib-only policy (A-2) does not prevent a pre-existing install in the repo env from shadowing `python -m wordfreq`. A-3 admits no research was done. | Check the internal repo env for a name conflict; if occupied, rename (e.g. `wfreq`/namespaced package) or record an explicit non-collision assumption. |
| 3 | Medium | Scope WF-02/WF-03 (lines 80–81); Success criteria (line 73) | Error behavior covers only invalid flag values. Undefined: nonexistent/unreadable file exit code, file encoding and decode-error handling, empty input, whether text output includes counts+words layout format. | Add IO/exit-code behavior to Scope or list them as spec-writer-owned decisions so acceptance criteria can test them. |
| 4 | Low | Exec summary line 33; WF-01 | No target Python version for `python -m wordfreq` or CI matrix. "Stdlib only" implies version tolerance, but the repo baseline (e.g. 3.11+) should be stated for the CI acceptance card. | State the repo's minimum Python version in Scope/WF-07. |
| 5 | Low | Scope line 92 | "`pyproject.toml` 等の追加が避けられない場合…smart マージ方針で人の承認" references an internal process ("smart マージ方針") without a pointer; a planner outside the team cannot act on it. | Add a one-line link/reference to the policy, or restate the concrete constraint (e.g. "any added runtime dep needs PM approval"). |

## Nitpicks skipped

JSON field names/key order, text output column layout, `--top` upper bound, and max-file-size expectations are spec-level details a planner can own; not flagged as gaps.
