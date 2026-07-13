import re
from collections.abc import Iterable
from pathlib import Path


FORBIDDEN_PATTERNS = (
    re.compile(r"sender_[p]assword\s*="),
    re.compile(r"myApp[K]ey"),
    re.compile(r"spreadK[e]y"),
    re.compile(r"BEGIN\s+PRIVATE\s+KEY"),
    re.compile(r"@[g]mail\.com", re.IGNORECASE),
    re.compile(r"\b[a-z]{4}(?:\s[a-z]{4}){3}\b", re.IGNORECASE),
)


def find_forbidden_content(paths: Iterable[Path]) -> tuple[Path, ...]:
    findings = []
    for path in paths:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(content) for pattern in FORBIDDEN_PATTERNS):
            findings.append(path)
    return tuple(findings)
