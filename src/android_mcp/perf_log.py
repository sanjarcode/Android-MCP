"""
Performance instrumentation utility.
Timing data is appended to {branch-name}.log in the working directory.
"""
import subprocess
import time
from contextlib import contextmanager


def _get_branch_name() -> str:
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        branch = result.stdout.strip()
        if branch and branch != 'HEAD':
            return branch.replace('/', '-')
    except Exception:
        pass
    return 'unknown'


_LOG_FILE = f"{_get_branch_name()}.log"


def _write(line: str) -> None:
    try:
        with open(_LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception:
        pass


def log_separator(label: str = "") -> None:
    """Write a section separator, e.g. at the start of a Snapshot call."""
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    _write(f"\n--- {label} [{ts}] ---")


@contextmanager
def timed(label: str):
    """Context manager that times a block and appends the result to the log file."""
    t0 = time.perf_counter()
    yield
    elapsed_ms = (time.perf_counter() - t0) * 1000
    _write(f"  {label}: {elapsed_ms:.1f}ms")
