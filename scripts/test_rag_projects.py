#!/usr/bin/env python3
"""Run the reviewed, supplied RAG demonstration tests in a temporary directory.

These synthetic fixtures exercise local retrieval/context/access-control logic;
they do not test a deployed RAG application, vector store, or LLM.
"""
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_NAME = "VerbaEdge_RAG_3_Portfolio_Projects.zip"
# Reviewed against the owner-supplied integrated package before execution.
# A changed archive requires a fresh source review before updating this pin.
REVIEWED_SHA256 = "f45737baba872b599a2334e96328d0cac3767f0fd60afd9fa33b42280521d948"


def main():
    systems = ROOT / "website-package/sites/systems/downloads" / ARCHIVE_NAME
    main_site = ROOT / "website-package/sites/main/downloads" / ARCHIVE_NAME
    payload = systems.read_bytes()
    if payload != main_site.read_bytes():
        raise ValueError("Main and Systems RAG downloads differ")
    if hashlib.sha256(payload).hexdigest() != REVIEWED_SHA256:
        raise ValueError("RAG archive changed; review its source before running it")

    with zipfile.ZipFile(systems) as archive:
        entries = archive.infolist()
        if len(entries) > 100 or sum(item.file_size for item in entries) > 2_000_000:
            raise ValueError("Unexpected RAG archive size")
        names = set()
        for item in entries:
            path = PurePosixPath(item.filename)
            mode = item.external_attr >> 16
            if (path.is_absolute() or ".." in path.parts or "\\" in item.filename
                    or ":" in item.filename or item.filename in names
                    or stat.S_ISLNK(mode) or item.file_size > 1_000_000):
                raise ValueError(f"Unsafe RAG archive entry: {item.filename}")
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError(f"Unsupported RAG archive entry: {item.filename}")
            names.add(item.filename)
        if "verify_all.py" not in names:
            raise ValueError("Supplied RAG test runner is missing")

        with tempfile.TemporaryDirectory(prefix="verbaedge-rag-tests-") as temp_dir:
            archive.extractall(temp_dir)
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
            result = subprocess.run(
                [sys.executable, "-B", "verify_all.py"], cwd=temp_dir,
                env=environment, capture_output=True, text=True, timeout=120,
            )
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
            if result.returncode:
                return result.returncode
            counts = [int(value) for value in re.findall(r"Ran (\d+) tests? in", result.stderr)]
            if counts != [5, 5, 8]:
                raise ValueError(f"Unexpected test-suite counts: {counts}")
    print("PASS: identical reviewed downloads; safe extraction; 18 supplied regression tests and 3 demos passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
