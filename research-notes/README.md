# Nghiên cứu SmolVLA

Bắt đầu từ [bản tóm tắt](smolvla/summary.md), sau đó đọc [báo cáo sáu phần](smolvla/report.md). Kết luận hiện tại: chọn flash-mm theo SR official quan sát 178/200, so với defaults 177/200; chưa chứng minh ưu thế thống kê.

## Tìm thông tin ở đâu?

| Cần đọc | Tài liệu |
|---|---|
| Kết quả, điều kiện đo và giới hạn | [Báo cáo chính](smolvla/report.md) |
| File size, latency, allocation, output delta | [Bảng tối ưu](smolvla/optimization.md) |
| Speedup, Wilson interval và dự toán | [Phụ lục tính toán](smolvla/calculations.md) |
| Success từng task và audit 680 episode | [Bảng LIBERO](smolvla-followup-20261104/TASK_RESULTS.md) |
| Kiến trúc và timing module | [Kiến trúc/profile](smolvla-followup-20261104/ARCHITECTURE_AND_PROFILE.md) |
| Phân tích timer, kernel, gaps và WSL | [Audit Task 5](task5-profiling/README.md) |
| Pruning và giới hạn CKA | [Pruning](smolvla-pruning/README.md) |
| Các câu hỏi thực nghiệm còn mở | [Yêu cầu review](smolvla/review.md) |
| Nguyên văn yêu cầu, lệnh và diễn biến cũ | [Nhật ký lịch sử](smolvla/history.md) |

## Bố trí dữ liệu

Trong `smolvla-followup-20261104/`:

| Thư mục / tệp | Nội dung |
|---|---|
| `official200-defaults/`, `official200-flash-mm/` | Official: 200 episode/cấu hình, protocol, result, CSV |
| `screen40-defaults/`, `screen40-variants/` | Screening: 40 episode/cấu hình, gồm runtime, Q8 và pruning |
| `candidate-smokes/` | Smoke: hai episode/task 0, giữ riêng với screening/official |
| `part3-runtime/`, `runtime-full-pair/`, `candidate-bench/` | Các batch benchmark độc lập, mỗi batch có control riêng |
| `memory-all/`, `quantization/`, `kernel-traces/`, `kernel-phase-traces/` | Allocation, export manifest và kết quả profiling |
| `fused-comparison/`, `user-on-off-summary.json` | Hai bản output gốc on/off của người dùng và phép so sánh |
| `submission-audit.json` | Hash và record của 90 CSV / 680 episode đã audit |

CSV, JSON và script cần kiểm chứng được lưu trong Git. Model, video, trace lớn, log và môi trường cài đặt là artifact cục bộ. Các thư mục có ngày trong tên ghi lại đợt đo; không đổi đường dẫn vì manifest và script đang tham chiếu chúng.

## Chạy lại kiểm tra

Từ gốc repo, không cần GPU hoặc model:

```bash
python3 research-notes/smolvla-followup-20261104/audit_submission.py
python3 research-notes/smolvla-followup-20261104/report_part3.py
python3 research-notes/smolvla-followup-20261104/complete_calculations.py
python3 research-notes/smolvla-followup-20261104/update_live_report.py
git diff --check
```

Các script trên kiểm tra/sinh tài liệu từ dữ liệu đã lưu. Script `run_*.py`, `bench_*.py` và `capture.py` thực hiện thí nghiệm; đọc protocol trước khi chạy vì chúng có thể dùng GPU, simulator hoặc ghi artifact mới.
