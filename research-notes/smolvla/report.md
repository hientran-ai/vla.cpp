# Báo cáo thực nghiệm SmolVLA

[← Mục lục SmolVLA](README.md)

Cập nhật ngày 06/11/2026. Checkpoint: `vrfai/smolvla-libero-gguf`. Máy đo: RTX 3060 Laptop 6 GiB, WSL2; repo gốc tại commit `4a542ed3bfb8f330388aceb8926294a951156172`.

**Lựa chọn hiện tại: flash-mm**, theo SR official quan sát cao nhất trong các cấu hình đã chạy đủ 200 episode. Kết quả hơn defaults một episode, chưa chứng minh ưu thế thống kê hoặc độ ổn định qua nhiều seed. Q8 chưa có official200.

Đọc nhanh: [bản tóm tắt](summary.md). Tra cứu: [sơ đồ tài liệu và dữ liệu](../README.md).

## 1. Cài đặt và kiểm thử

Đã build CUDA architecture 86, Release, `GGML_CUDA=ON`, `VLA_BUILD_TESTS=ON`; CUDA graphs bật. Đây là incremental build, chưa xác minh clean rebuild.

| Công cụ | Kết quả đã ghi nhận |
|---|---|
| CLI | Trả chunk action 50 × 32 với input synthetic |
| Server và Python binding | Output hữu hạn, khớp bit với harness khi cùng input/noise |
| `vla_predict_check` | Kiểm tra output trên input/noise cố định; action thực có 7 chiều, phần còn lại là padding |
| `ctest` | 13/15 pass; `foldquant_cuda_op` và `fused_cuda_ops` fail bit-exact, chưa sửa hoặc rerun |

Fused/unfused có max abs 0,000545874 trên harness đã lưu. LIBERO chạy được nhưng môi trường còn bảy xung đột dependency metadata. Lệnh và diễn biến kiểm thử nằm trong [nhật ký](history.md#lệnh-đã-chạy-và-ý-nghĩa).

## 2. Baseline

| Chỉ số | Giá trị |
|---|---|
| Mean / p50 / p90 | 112,0 / 111,8 / 112,8 ms, cùng lượt được chọn |
| Peak traced allocation | 1912,47 MiB, peak lớn nhất trong ba process |
| Input benchmark | Hai ảnh 512 × 512, 16 language tokens, 10 bước denoise; chunk 50 × 32 |
| Protocol | Ba process tuần tự; mỗi process có 3 warmup và 20 lần đo |
| Phạm vi | Engine predict, chưa gồm network hoặc simulator |

Laptop cắm sạc, nguồn bình thường, không tản nhiệt ngoài theo người dùng. Chưa xác minh mọi lượt đo đều cô lập với tải khác. Runtime bổ sung có guard từ chối chạy khi còn server. Telemetry bổ sung có 120 mẫu ở 53–72°C, không phủ toàn bộ baseline và chưa đủ kết luận throttle.

WSL trả N/A cho process resident VRAM. Allocation chỉ bao phần được trace, chưa gồm đầy đủ context/driver.

## 3. Tối ưu không train

Đã đo 10 cấu hình runtime và sáu GGUF quantized Q8/Q5/Q4, có và không quantize vision. [Bảng tối ưu](optimization.md) lưu kích thước file, allocation, mean/p50/p90 và sai lệch action cho từng cấu hình.

| Batch / cách chọn thống kê | Defaults mean | Flash-mm mean | Mức giảm |
|---|---:|---:|---:|
| Phần 3: lượt có mean thấp nhất | 104,0 ms | 85,5 ms | 17,79% |
| Runtime-pair: trung vị ba run means | 114,1 ms | 92,4 ms | 19,02% |

Các batch có điều kiện đo và control riêng. Không ghép số liệu giữa hai hàng. Quantization dùng control riêng 113,7 ms. Q8-vision có allocation 925,88 MiB; Q8-lm 1020,70 MiB; control 1912,47 MiB.

`steps-3` nhanh nhất trong tập runtime (79,2 ms) nhưng đổi solver và có sai lệch action lớn, chưa được đánh giá SR. Flash-mm giữ 10 bước denoise. Chưa đo cấu hình quantization kết hợp flash-mm nên không cộng các mức cải thiện.

Output-check dùng harness 6 token và noise cố định, khác input benchmark 16 token. Max abs/RMSE lấy trên 50 × 7 action thực; không suy SR từ sai số synthetic.

## 4. Đánh giá LIBERO

Suite `libero_object`, task 0–9, `n_action_steps=1`, seed môi trường 42. Server giữ noise ngẫu nhiên mặc định; cùng seed môi trường chưa đảm bảo cùng noise hoặc trajectory.

<!-- SMOLVLA_LIVE_START -->
### Kết quả từ manifest

Bảng sinh bằng `update_live_report.py`; audit CSV và hash ở [TASK_RESULTS.md](../smolvla-followup-20261104/TASK_RESULTS.md).

| Cấu hình / lượt đánh giá | Thành công | SR quan sát | Trạng thái |
|---|---:|---:|---|
| Defaults screening | 38/40 | 95,0% | Hoàn tất |
| Flash-mm screening | 35/40 | 87,5% | Hoàn tất |
| Q8-lm screening | 36/40 | 90,0% | Hoàn tất |
| Q8-vision screening | 36/40 | 90,0% | Hoàn tất |
| Defaults official | 177/200 | 88,5% | Hoàn tất |
| Flash-mm official | 178/200 | 89,0% | Hoàn tất |
| Vision-tail-10 screening | 0/40 | 0,0% | Hoàn tất |
| Vision-spaced-10 screening | 0/40 | 0,0% | Hoàn tất |
| Coupled-tail-30 screening | 23/40 | 57,5% | Hoàn tất |

SR official quan sát cao nhất trong các bản đã hoàn tất 200 episode: Flash-mm official 178/200. Chưa chứng minh ưu thế thống kê; hai bản Q8 và repeated-seed chưa có official.
<!-- SMOLVLA_LIVE_END -->

Smoke dùng 1 task × 2 episode; screening dùng 10 × 4; official dùng 10 × 20. Task 9 official defaults đã chạy lại đủ 20 episode sau timeout, loại toàn bộ lượt dở.

[Audit và bảng theo task](../smolvla-followup-20261104/TASK_RESULTS.md) kiểm tra 90 CSV / 680 episode: 400 official, 160 screening runtime/quantization và 120 screening pruning. Tất cả các CSV được chọn có `aborted=0`; hash và record từng episode nằm trong [submission-audit.json](../smolvla-followup-20261104/submission-audit.json).

## 5. Kiến trúc và profiling

[Kiến trúc và module timing](../smolvla-followup-20261104/ARCHITECTURE_AND_PROFILE.md) mô tả vision → connector → VLM → action expert và vòng denoise. [Audit Task 5](../task5-profiling/README.md) đối chiếu sáu benchmark log và hai SQLite node trace đã lưu.

Runtime-pair có trung vị mean 114,1 → 92,4 ms; p50 114,1 → 92,5 ms; p90 115,4 → 93,0 ms. Đây là trung vị thống kê của ba lượt, chưa phải percentile gộp 60 mẫu. Vision + connector wall time giảm 56,1 → 43,6 ms.

PHASE đổi graph/padding từ 48 xuống 16 language tokens, có copy K/V và backend synchronization. Timer gồm host dispatch, chờ và gaps; chưa phải phân rã chính xác default latency. Vision còn gồm connector, denoise còn gồm cross-KV và solver.

Trên 20 prediction được trace, tổng kernel duration giảm 2260,227 → 1733,185 ms. GEMM theo tên chiếm 58,30% → 51,85%, có cả attention matmul. Gaps trong recorded process activity giảm 10,54% → 9,13%; chưa chứng minh toàn GPU idle hoặc CPU bottleneck.

Cả hai trace cảnh báo `Not all CUDA events might have been collected.` và dùng legacy software tracing. Mọi tỷ lệ chỉ mô tả events đã ghi nhận; chưa có exact attention/connector timing hoặc hardware counters chứng minh bottleneck.

## 6. Pruning

Đã cắt layer thật và đo ba depth ablation: vision-tail-10, vision-spaced-10 và coupled-tail-30. Screening lần lượt đạt 0/40, 0/40 và 23/40; chưa chọn bản nào để triển khai. Smoke 0/2 trước đó là lượt riêng, không cộng vào screening.

[Phương pháp và script](../smolvla-pruning/README.md) phân biệt depth ablation với CKA. Có tiện ích capture/CKA và kiểm thử synthetic; chưa có calibration thực, checkpoint CKA, finetuning hoặc SR cho CKA. Kết quả giảm module latency không tự chứng minh giữ chất lượng.

## Những việc còn thiếu

| Hạng mục | Cần bổ sung |
|---|---|
| Kiểm thử CUDA | Sửa hai lỗi bit-exact và rerun; chưa thay tolerance |
| Chất lượng Q8 | Official200 cho từng bản Q8; tổng 400 episode nếu chạy cả hai |
| Độ ổn định SR | Protocol noise/seed rõ ràng và repeated-seed evaluation |
| Profiling | Tách connector/attention, xác minh trace completeness và source/binary provenance |
| CKA/CLP | Calibration riêng, chọn layer hợp lệ, finetuning và đánh giá mới |
| Môi trường | Lock sạch, giải quyết bảy dependency conflicts; đo resident VRAM trên backend hỗ trợ |

[Câu hỏi gửi review](review.md) tập trung vào các giới hạn này. [Phụ lục tính toán](calculations.md) lưu speedup, Wilson interval và các dự toán có nhãn; dự toán không thay thế kết quả official.

## Kiểm tra lại dữ liệu

Từ thư mục gốc repo, không cần GPU hoặc model:

```bash
python3 research-notes/smolvla-followup-20261104/audit_submission.py
python3 research-notes/smolvla-followup-20261104/report_part3.py
python3 research-notes/smolvla-followup-20261104/complete_calculations.py
python3 research-notes/smolvla-followup-20261104/update_live_report.py
git diff --check
```

Các lệnh kiểm tra/sinh báo cáo từ dữ liệu đã lưu, không chạy inference mới. GGUF, video, log và trace lớn vẫn là artifact cục bộ.
