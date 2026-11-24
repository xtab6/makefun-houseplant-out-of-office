"""The Houseplant Out-of-Office — make.fun entry.

Writes one out-of-office auto-reply, as if a houseplant sent it, to
/output/entry.txt. Gate: UTF-8 text of 1 to 120 characters, not only
whitespace. Stdlib only; no network, no files outside the repo.
"""

import os
import sys

LINE = (
    "Out of office. My leaves are on strike, my roots filed a complaint, "
    "and the watering can is in witness protection."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    if not 1 <= len(LINE) <= 120:
        print(f"line is {len(LINE)} chars, must be 1-120", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line is only whitespace", file=sys.stderr)
        return 1
    # Clean only the contents of /output; never remove the folder itself
    # (the grader mounts it and removing it fails with EPERM).
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
