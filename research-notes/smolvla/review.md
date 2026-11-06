# SmolVLA — các vấn đề cần review

[← Mục lục SmolVLA](README.md)

Cập nhật ngày 06/11/2026. Số liệu và kết luận chính ở [báo cáo](report.md); [bản tóm tắt](summary.md) dùng để đọc nhanh.

Flash-mm có SR official quan sát 178/200, defaults 177/200. Audit đã đối chiếu 90 CSV / 680 episode, không abort. Chưa có bằng chứng ưu thế thống kê, official Q8 hoặc độ ổn định qua nhiều seed.

| Vấn đề | Bằng chứng / giới hạn | Câu hỏi review |
|---|---|---|
| Hai CUDA tests fail | Kết quả lịch sử 13/15 pass; `foldquant_cuda_op`, `fused_cuda_ops` fail bit-exact, chưa sửa/rerun | Cần kiểm tra kernel/numerics nào trước khi kết luận triển khai? |
| Fused/unfused | Max abs 0,000545874 trên harness cố định | Cần thêm real-observation hoặc calibration checks nào? |
| Chất lượng | Flash-mm official 178/200; defaults 177/200; hai Q8 mới screening 36/40 | Cần bao nhiêu seed/episode và thiết kế đánh giá nào để kiểm tra giữ chất lượng? |
| Noise | Seed 42 chỉ cố định môi trường; server noise vẫn ngẫu nhiên | Có cần protocol fixed-noise riêng, bên cạnh repeated seeds? |
| Recovery | Task 9 official defaults chạy lại đủ 20 episode, loại lượt dở | Policy này đã phù hợp và đủ minh bạch chưa? |
| Latency | Phần 3 chọn minimum run mean; Task 5 dùng median run means ở batch riêng | Cần final rerun với điều kiện nguồn/nhiệt nào? |
| Memory | Peak traced allocation chưa bao hết context/driver; WSL process NVML N/A | Chấp nhận chỉ số này hay cần backend khác để đo resident VRAM? |
| Profiling | Trace cảnh báo thiếu events; GEMM có cả attention; vision gồm connector | Cần thêm instrumentation/counters nào để xác định module và bottleneck? |
| Pruning | Screening 0/40, 0/40, 23/40; CKA mới có tiện ích và kiểm thử synthetic | Chọn calibration, mapping và bảo toàn parity SA/CA/coupling thế nào? |
| Tái lập | Bảy dependency metadata conflicts; chưa clean rebuild/lock | Cần môi trường sạch và kiểm chứng binary/source ở mức nào? |

## Bằng chứng để review

- [Bảng theo task](../smolvla-followup-20261104/TASK_RESULTS.md): ID, steps, success, aborted; [audit JSON](../smolvla-followup-20261104/submission-audit.json) lưu hash và record từng episode.
- [Audit Task 5](../task5-profiling/README.md): source anchors, timer, log, kernel/API/gap và giới hạn trace. Audit ngày 05/11 dùng artifact đã lưu, không đo GPU mới.
- [Pruning](../smolvla-pruning/README.md): depth ablation, capture/CKA và giới hạn thực nghiệm.
- [Phụ lục tính toán](calculations.md): speedup, allocation, Wilson interval và dự toán có giả định.

[Báo cáo chính](report.md#kiểm-tra-lại-dữ-liệu) có lệnh audit/sinh lại tài liệu, không cần GPU. Audit dữ liệu không chứng nhận kernel correctness, môi trường portable hoặc khả năng tái hiện trajectory từng bit.
