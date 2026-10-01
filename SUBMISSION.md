# Hướng dẫn nộp bài (SUBMISSION)

## 1. Hình thức nộp bài
- Bài tập được thực hiện theo hình thức **cá nhân**.
- **Mỗi cá nhân phải tự nộp link repo của mình lên hệ thống Codelab** theo thông báo của giảng viên hoặc coach (mỗi học viên một repository riêng, không nộp hộ, không dùng chung repo).
- Repository phải được để ở chế độ Public (hoặc cấp quyền truy cập cho giảng viên / coach nếu được yêu cầu).

## 2. Quy chuẩn đặt tên Repository

Cấu trúc tên repository nộp bài:

```text
K4-L3B-<HoVaTen>-<MSSV>-AIEvaluation
```

- `<HoVaTen>`: Họ và tên viết liền không dấu (PascalCase).
- `<MSSV>`: Mã số sinh viên chính xác.

**Ví dụ:**
```text
K4-L3B-NguyenVanAn-L3A202600280-AIEvaluation
```

> ⚠️ **Lưu ý:** Đặt sai tên repository sẽ bị trừ **5 điểm** theo quy định trong [RUBRIC.md](RUBRIC.md).

## 3. Thành phần bài nộp (Deliverables)

| File | Yêu cầu |
|---|---|
| `solution/solution.py` | Hoàn thiện tất cả TODO bắt buộc |
| `golden_dataset.json` | Đủ 20 QA, đúng schema |
| `exercises.md` | worksheet, benchmark 3.2, rubric 3.3 |
| `reflection.md` | report, 3 failures, 5 Whys, regression |

Các file sinh ra trong quá trình chạy (artifacts) là tùy chọn (optional):
- `artifacts/actual_answers.json`
- `artifacts/benchmark_results.json`

> ⚠️ **CẢNH BÁO BẢO MẬT:** Tuyệt đối **KHÔNG commit** file `.env`, OpenAI API key hoặc bất kỳ thông tin bí mật nào lên GitHub repository. Vi phạm sẽ bị trừ **10 điểm**.

## 4. Nơi nộp và Hạn nộp (Deadline)
- **Nơi nộp:** Nộp link GitHub repository cá nhân lên Codelab.
- **Hạn chót mặc định:** **23h59 ngày lab (GMT+7)**.
- Coach có thể gia hạn tối đa không quá **48 giờ (≤48h)** đối với các trường hợp đặc biệt có lý do chính đáng được phê duyệt trước.

## 5. Checklist kiểm tra trước khi nộp

Hãy chạy các kiểm tra sau và tích chọn đầy đủ trước khi nộp bài:

- [x] Repository đặt đúng tên: `K4-L3B-NguyenThanhLuan-2A202602769-AIEvaluation`.
- [x] `python validate_golden_dataset.py` báo `PASS`.
- [x] Required tests pass: 42/42 tests gốc, thêm 5 edge-case tests, tổng 47 passed.
- [x] `golden_dataset.json` đủ 20 QA (5 Easy + 7 Medium + 5 Hard + 3 Adversarial).
- [x] Kiểm tra 20 actual answers của RAG run đã lưu ngày 01/10/2026, không có inference errors; chunks có provenance.
- [x] `exercises.md` có bảng năm metrics, ba cases thấp nhất, rubric ba dimensions, edge cases và hai bonus.
- [x] `reflection.md` có ba 5 Whys analyses, taxonomy, improvement log và regression strategy.
- [x] `solution/solution.py` đồng bộ bản hoàn thiện `template.py`.
- [x] `.env` được ignore và không nằm trong danh sách commit.

Học viên còn cần review phần phân tích có AI hỗ trợ, bảo đảm giải thích được
code/nhận định theo `RULES.md`, và tự nộp link repository lên Codelab.

---

## Tài liệu liên quan
- [README.md](README.md) — Tổng quan bài lab và hướng dẫn khởi động
- [RUBRIC.md](RUBRIC.md) — Tiêu chí chấm điểm chi tiết và các trường hợp trừ điểm
- [CHECKPOINTS.md](CHECKPOINTS.md) — Hướng dẫn từng checkpoint và tiêu chuẩn nghiệm thu
- [RULES.md](RULES.md) — Quy định làm bài, sử dụng AI và bảo mật
