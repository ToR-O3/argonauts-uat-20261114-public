"""Operator-authorized single capture retry; only browser launch uses /tmp.

No collector/suite injection: all original driver code executes unchanged.
Short-lived path permission: t_3221bf48 human comment 2026-11-18 10:16 JST.
"""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from contextlib import contextmanager

root = Path.cwd()
spec = importlib.util.spec_from_file_location("min_count_driver", root / "tools/verify_wordfreq_min_count.py")
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
original = driver.parts.instrumented_browser

@contextmanager
def authorized_browser(pw, executable):
    previous = os.environ.get("TMPDIR")
    with tempfile.TemporaryDirectory(prefix="aw-", dir="/tmp") as short:
        try:
            os.environ["TMPDIR"] = short
            with original(pw, executable) as browser:
                # Keep the shorter spelling only in the browser startup boundary.
                if previous is None:
                    os.environ.pop("TMPDIR", None)
                else:
                    os.environ["TMPDIR"] = previous
                yield browser
        finally:
            if previous is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = previous

driver.parts.instrumented_browser = authorized_browser
sys.exit(driver.main())
