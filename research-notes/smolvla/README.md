# SmolVLA — báo cáo thực nghiệm

**Kết quả chính:** flash-mm đạt official 178/200 (89,0%), defaults 177/200 (88,5%). Flash-mm được chọn theo SR quan sát; chênh lệch một episode chưa chứng minh ưu thế thống kê.

## Đọc theo thứ tự

1. [Tóm tắt](summary.md) — kết quả sáu phần, đọc nhanh.
2. [Báo cáo đầy đủ](report.md) — protocol, baseline, tối ưu, LIBERO, profile và pruning.
3. [Bảng tối ưu](optimization.md) — kích thước, latency, allocation và sai lệch output.
4. [Phụ lục tính toán](calculations.md) — speedup, Wilson interval và dự toán có giả định.
5. [Câu hỏi review](review.md) — các vấn đề thực nghiệm còn mở.

## Dữ liệu và tái lập

- [Mục lục dữ liệu/script](../README.md)
- [Kết quả LIBERO theo task](../smolvla-followup-20261104/TASK_RESULTS.md): 90 CSV / 680 episode đã audit.
- [Kiến trúc và profiling](../smolvla-followup-20261104/ARCHITECTURE_AND_PROFILE.md)
- [Audit Task 5](../task5-profiling/README.md)
- [Pruning](../smolvla-pruning/README.md)
- [Nhật ký lịch sử](history.md): nguyên văn yêu cầu, lệnh và diễn biến theo thời điểm.

Các lệnh trong tài liệu chạy từ **gốc repo**. Dữ liệu nằm trong các thư mục đợt đo bên cạnh; đường dẫn manifest được giữ nguyên.
