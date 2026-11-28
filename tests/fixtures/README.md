# Fixed historical Git objects for exclusion compatibility tests

`exclude-baseline-git-objects.json` contains raw objects read with `git cat-file`
from commit `79d83ba14dd59d289d2ecd3e33c85e8de437972e`, not current source or
captured CLI output. It includes that commit, its root tree, the `wordfreq`
subtree (`49d9b98f8f34861b8777690ab68f4d4733584337`) and its six Python blobs.
Unrelated trees and commit ancestry are intentionally omitted.

The tests write these objects into a disposable Git database with
`git hash-object -w -t TYPE --stdin`, check every returned object ID, and resolve
`FIXED_COMMIT:wordfreq/...` with Git. The pinned commit authenticates the root
tree, which authenticates the package tree and all source blobs. Rehashing a
modified blob cannot make the unchanged parent tree refer to it.

This makes the fixed historical implementation available in depth-one CI
checkouts without fetching, network access, workflow changes, or modifying the
checkout's Git database. Missing/corrupt data fails the test; there is no skip,
current-source fallback, or self-generated expected output.

The original 64 comparisons still run both implementations with the same
interpreter, input pathname, arguments and environment in isolated module roots,
and compare raw stdout, stderr and exit code. The additional shallow-checkout
regression checks that the baseline commit is genuinely absent from that
checkout before exercising all three output formats. Corruption controls cover
missing fixture, missing blob, changed blob, and changed/rehashed blob.
