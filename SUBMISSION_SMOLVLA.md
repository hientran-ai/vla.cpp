# SmolVLA — tóm tắt kết quả

Cập nhật ngày 06/11/2026. Checkpoint `vrfai/smolvla-libero-gguf`, RTX 3060 Laptop 6 GiB, WSL2.

**Chọn flash-mm theo SR official quan sát:** 178/200 (89,0%), so với defaults 177/200 (88,5%). Chênh lệch một episode chưa chứng minh ưu thế thống kê; Q8 chưa có official200.

| Phần | Kết quả chính |
|---|---|
| Cài đặt | CUDA arch86; CLI/server/binding hoạt động; tests lịch sử 13/15 pass, hai lỗi bit-exact còn mở |
| Baseline | Mean/p50/p90 112,0/111,8/112,8 ms; peak traced allocation 1912,47 MiB |
| Tối ưu | 10 runtime configs và sáu GGUF quantized; flash-mm giảm mean 104,0 → 85,5 ms trong batch phần 3 |
| LIBERO | Defaults official 177/200; flash-mm official 178/200; Q8-lm và Q8-vision screening cùng 36/40 |
| Profile | Runtime-pair giảm median run mean 114,1 → 92,4 ms; chưa tách connector/attention đầy đủ |
| Pruning | Vision-tail 0/40, vision-spaced 0/40, coupled-tail 23/40; chưa đạt chất lượng triển khai |

Hai batch latency trong bảng có control và cách chọn thống kê riêng. Allocation chưa phải toàn bộ process resident VRAM. Trace có cảnh báo thiếu CUDA events. Server noise chưa cố định; chưa có repeated-seed evaluation, calibration CKA thực hoặc finetuning. Hai lỗi CUDA chưa được sửa/rerun.

Audit đã đối chiếu **90 CSV / 680 episode**, tất cả `aborted=0`; giữ riêng smoke, screening và official.

- [Báo cáo đầy đủ theo sáu phần](REPORT_SMOLVLA.md)
- [Bảng tối ưu và điều kiện đo](PART3_OPTIMIZATION.md)
- [Kết quả từng task và audit](research-notes/smolvla-followup-20261104/TASK_RESULTS.md)
- [Câu hỏi cần review](REVIEW_REQUESTS.md)
- [Chỉ dẫn tài liệu, dữ liệu và script](research-notes/README.md)
