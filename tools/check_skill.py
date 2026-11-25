"""Kiểm tính nhất quán của repo skill trước khi commit/phát hành.

    python tools/check_skill.py            # kiểm tên, phiên bản, CHANGELOG, tag (trên CI)
    python tools/check_skill.py --notes    # in phần CHANGELOG của phiên bản hiện tại

Chỉ dùng thư viện chuẩn.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return fm


def changelog_section(version):
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def main(argv):
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if "--notes" in argv:
        print(changelog_section(version) or f"Phiên bản {version}")
        return 0

    errors, warnings = [], []
    fm = frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    if fm is None:
        print("LỖI: SKILL.md thiếu frontmatter YAML")
        return 1
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))

    if not SEMVER.fullmatch(version):
        errors.append(f"VERSION '{version}' không theo SemVer MAJOR.MINOR.PATCH")
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"frontmatter thiếu '{key}'")
    if fm.get("name") != manifest.get("name"):
        errors.append(f"tên frontmatter '{fm.get('name')}' khác skill.json '{manifest.get('name')}'")
    if fm.get("version") != version:
        errors.append(f"frontmatter version '{fm.get('version')}' khác VERSION '{version}'")
    if manifest.get("version") != version:
        errors.append(f"skill.json version '{manifest.get('version')}' khác VERSION '{version}'")
    if changelog_section(version) is None:
        errors.append(f"CHANGELOG.md chưa có mục '## [{version}]'")
    if len(fm.get("name", "")) > 64:
        errors.append("tên skill dài quá 64 ký tự")
    if len(fm.get("description", "")) > 1024:
        warnings.append(f"description dài {len(fm['description'])} ký tự (claude.ai giới hạn 1024)")

    ref = os.environ.get("GITHUB_REF", "")
    if ref.startswith("refs/tags/") and ref[len("refs/tags/"):] != f"v{version}":
        errors.append(f"tag '{ref[len('refs/tags/'):]}' khác phiên bản v{version}")

    for w in warnings:
        print("CẢNH BÁO:", w)
    for e in errors:
        print("LỖI:", e)
    if not errors:
        print(f"OK {manifest.get('name')} v{version}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
