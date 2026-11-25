"""Đóng gói skill thành dist/<tên>-v<phiên bản>.zip (bố cục <tên>/SKILL.md) để tải lên claude.ai.

    python tools/package.py
"""
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".github", "tools", "dist", "__pycache__", ".pytest_cache"}
EXCLUDE_FILES = {".gitignore", ".gitattributes"}


def main():
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    name, version = manifest["name"], manifest["version"]
    out = ROOT / "dist" / f"{name}-v{version}.zip"
    out.parent.mkdir(exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            rel = path.relative_to(ROOT)
            if path.is_dir() or set(rel.parts) & EXCLUDE_DIRS or rel.name in EXCLUDE_FILES or path.suffix == ".pyc":
                continue
            zf.write(path, f"{name}/{rel.as_posix()}")
            count += 1
    print(f"{out.relative_to(ROOT)} ({count} tệp)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
