# Historical max-count scope fixture

Only `tests/test_max_count_verifier.py::scope_repo` uses this frozen product/README.
It is not the current wordfreq implementation and must not be regenerated from it.
The current test_cli.py and pyproject.toml remain inputs to the cold scope repository.

Source commit: `27d359409c585cbb923b42aef3298cf6dfc28094` (pre-min-length).
Each file was extracted as bytes with `git show <commit>:<original-path>`;
paths below are original repository paths, mirrored under this directory.

| Original path | SHA-256 |
|---|---|
| wordfreq/__init__.py | 8004295c8623cc0913025efb31807353a72698470a9497cf8dee95ed6e7d7239 |
| wordfreq/__main__.py | 9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba |
| wordfreq/aggregator.py | 33c40f5d0c5bbc7c8e185bbc8a25051ef7d381ebd42c9ed42c35b4ec7cbbbd35 |
| wordfreq/formatters.py | 184bb48ae6badf9c7fedc874e55bf163e4bd576c0a234a0ccffa37c49056f726 |
| wordfreq/sources.py | 8800710801b75e5e87e085471f4fca7d8079dcf924e125da9536259bbda67f58 |
| wordfreq/tokenizer.py | beb26f7b2713dde42d6532397df50bec22a5676969ecbc3fdd7c1762e8668dc6 |
| README.md | 5a0ca56634033c569765f1c3002962b15357b45821cbfd1245b86862a54aeb3a |

The CLI and README hashes exactly match the unchanged approvals in
`tools/verify_wordfreq_max_count.py::validate_scope`. Clean/append acceptance and
product/README tamper rejection continue to use that original validator.
