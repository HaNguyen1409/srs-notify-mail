# srs-notify-mail

**AG-NOTIFY** · Node dịch vụ · phiên bản **1.0.0** · giấy phép MIT

> Vietnamese-language Claude skill — one independent, reusable service of the SRS-SOP agent pipeline. Machine-readable contract: [`skill.json`](skill.json).

Node dịch vụ AG-NOTIFY (SOP, gọi bất kỳ lúc nào ngoài luồng B1–B30): soạn email phát hành tài liệu/thông tin dự án từ sổ tài liệu + changelog; kiểm phân loại mật (giữ tài liệu mật nếu gửi ra ngoài tổ chức); dừng ở Human Gate chờ xác nhận, không tự gửi.

## Hợp đồng giao tiếp

Skill là một dịch vụ độc lập, ghép lỏng: nhận đầu vào và trả đầu ra dưới dạng tài liệu/JSON mô tả trong [`SKILL.md`](SKILL.md), không gọi trực tiếp skill khác và không gắn với dự án cụ thể. Dùng riêng lẻ, hoặc ghép qua bộ điều phối [`srs-sop-pipeline`](https://github.com/HaNguyen1409/srs-sop-pipeline).

| Bước SOP | Việc | Loại | Nhận từ | Chuyển tới |
|---|---|---|---|---|
| — | Thông báo & phát tài liệu qua email | Agent | sổ tài liệu + changelog (workbook) | người nhận qua email |

## Cài đặt

**Claude Code** — clone đúng phiên bản vào thư mục skill:

```bash
git clone --branch v1.0.0 https://github.com/HaNguyen1409/srs-notify-mail.git ~/.claude/skills/srs-notify-mail
```

Nâng cấp: `git -C ~/.claude/skills/srs-notify-mail fetch --tags && git -C ~/.claude/skills/srs-notify-mail checkout v<phiên-bản-mới>`.

**claude.ai / Claude Desktop** — tải `srs-notify-mail-v1.0.0.zip` ở trang [Releases](https://github.com/HaNguyen1409/srs-notify-mail/releases) rồi tải lên ở phần Skills trong cài đặt.

**Cả bộ** — xem [`srs-sop-skills`](https://github.com/HaNguyen1409/srs-sop-skills) (cài toàn bộ skill theo phiên bản đã khoá).

## Quản lý phiên bản

Theo [SemVer](https://semver.org/lang/vi/), áp cho hợp đồng giao tiếp của skill:

| Tăng | Khi |
|---|---|
| MAJOR | Đổi hợp đồng làm vỡ skill phía sau: đổi/bỏ trường JSON, đổi hệ mã ID, đổi bố cục tài liệu đầu ra |
| MINOR | Thêm khả năng tương thích ngược: trường tuỳ chọn, mục mới, chế độ mới |
| PATCH | Sửa câu chữ, sửa lỗi, làm rõ luật mà không đổi đầu ra |

Phát hành: sửa `SKILL.md` → tăng `version` trong frontmatter, `VERSION`, `skill.json` → thêm mục vào [`CHANGELOG.md`](CHANGELOG.md) → `python tools/check_skill.py` → commit → `git tag -a vX.Y.Z -m "vX.Y.Z"` → `git push --follow-tags`. GitHub Actions kiểm lại, chạy test và đính kèm zip vào Release.

## Giấy phép

MIT — xem [`LICENSE`](LICENSE).
