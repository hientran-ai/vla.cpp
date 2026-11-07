# Báo cáo thực nghiệm SmolVLA

[← Mục lục SmolVLA](README.md)

Báo cáo này ghi lại quá trình chạy SmolVLA trên RTX 3060 Laptop 6 GiB với WSL2, từ kiểm tra cài đặt, đo hiệu năng đến đánh giá trên LIBERO. Các thử nghiệm dùng checkpoint `vrfai/smolvla-libero-gguf`, với repo gốc tại commit `4a542ed3bfb8f330388aceb8926294a951156172`. Số liệu được cập nhật đến ngày 06/11/2026.

Qua các lượt đo, **flash-mm** được chọn làm cấu hình sử dụng hiện tại: latency giảm và kết quả LIBERO đạt 178/200 episode thành công, so với 177/200 của defaults. Tuy nhiên, chênh lệch chỉ một episode nên chưa đủ để kết luận flash-mm có chất lượng tốt hơn hay ổn định hơn qua nhiều seed. Hai bản Q8 vẫn cần được đánh giá đủ 200 episode trước khi so sánh tiếp.

Có thể xem [bản tóm tắt](summary.md) để nắm các kết quả chính, hoặc tra [mục lục tài liệu và dữ liệu](../README.md) khi cần đối chiếu log và cách đo.

## 1. Cài đặt và kiểm thử

Bản build sử dụng chế độ Release cho CUDA architecture 86, bật `GGML_CUDA=ON`, `VLA_BUILD_TESTS=ON` và CUDA graphs. Các kết quả dưới đây được kiểm tra trên bản build cập nhật từ lần build trước; chưa kiểm tra lại bằng một lượt clean build.

| Công cụ | Kết quả đã ghi nhận |
|---|---|
| CLI | Trả chunk action 50 × 32 với input synthetic |
| Server và Python binding | Output hữu hạn, khớp bit với harness khi cùng input/noise |
| `vla_predict_check` | Kiểm tra output trên input/noise cố định; action thực có 7 chiều, phần còn lại là padding |
| `ctest` | 13/15 pass; `foldquant_cuda_op` và `fused_cuda_ops` fail bit-exact, chưa sửa hoặc rerun |

Khi so sánh fused và unfused bằng harness đã lưu, sai lệch tuyệt đối lớn nhất là 0,000545874. LIBERO đã chạy được, nhưng môi trường vẫn báo bảy xung đột trong metadata của các dependency. Vì vậy, phần cài đặt còn cần xử lý hai test CUDA và làm sạch môi trường. Các lệnh kiểm tra được lưu trong [nhật ký](history.md#lệnh-đã-chạy-và-ý-nghĩa).

## 2. Đo hiệu năng ban đầu

| Chỉ số | Giá trị |
|---|---|
| Mean / p50 / p90 | 112,0 / 111,8 / 112,8 ms, cùng lượt được chọn |
| Peak traced allocation | 1912,47 MiB, peak lớn nhất trong ba process |
| Input benchmark | Hai ảnh 512 × 512, 16 language tokens, 10 bước denoise; chunk 50 × 32 |
| Protocol | Ba process tuần tự; mỗi process có 3 warmup và 20 lần đo |
| Phạm vi | Engine predict, chưa gồm network hoặc simulator |

Theo thông tin về điều kiện chạy, laptop được cắm sạc, dùng nguồn bình thường và không có tản nhiệt ngoài. Chưa xác minh được tất cả các lượt đo đều không chịu ảnh hưởng từ tải khác. Ở đợt đo runtime bổ sung, script có kiểm tra và từ chối chạy nếu server vẫn còn hoạt động. Dữ liệu nhiệt độ bổ sung gồm 120 mẫu, nằm trong khoảng 53–72°C; các mẫu này không bao phủ toàn bộ baseline nên chưa thể dùng để kết luận máy có bị throttle hay không.

WSL không trả về lượng VRAM thực tế của process (hiển thị N/A). Vì vậy, báo cáo dùng lượng bộ nhớ cấp phát được trace để đối chiếu giữa các cấu hình. Con số này chưa bao gồm đầy đủ bộ nhớ của context và driver.

## 3. Các thử nghiệm tối ưu không huấn luyện lại

Phần này gồm 10 cấu hình runtime và sáu bản GGUF lượng tử hóa Q8/Q5/Q4, với cả hai lựa chọn giữ nguyên hoặc lượng tử hóa vision. Kích thước file, bộ nhớ cấp phát, latency mean/p50/p90 và sai lệch action của từng bản được ghi trong [bảng tối ưu](optimization.md).

| Batch / cách chọn thống kê | Defaults mean | Flash-mm mean | Mức giảm |
|---|---:|---:|---:|
| Phần 3: lượt có mean thấp nhất | 104,0 ms | 85,5 ms | 17,79% |
| Runtime-pair: trung vị ba run means | 114,1 ms | 92,4 ms | 19,02% |

Cả hai đợt đo đều ghi nhận latency giảm khi bật flash-mm. Tuy nhiên, mỗi đợt có điều kiện đo, bản đối chứng và cách chọn thống kê riêng, nên chỉ so sánh các số trong cùng một hàng. Đợt đo quantization cũng dùng bản đối chứng riêng, với mean 113,7 ms. Bộ nhớ cấp phát của Q8-vision là 925,88 MiB và Q8-lm là 1020,70 MiB, so với 1912,47 MiB ở bản đối chứng.

Trong các cấu hình runtime đã thử, `steps-3` có latency thấp nhất, đạt 79,2 ms. Tuy vậy, cấu hình này thay đổi solver, có sai lệch action lớn và chưa được đánh giá tỷ lệ thành công (SR). Flash-mm vẫn giữ 10 bước denoise và được tiếp tục đánh giá trên LIBERO. Chưa có phép đo kết hợp quantization với flash-mm; mức cải thiện của hai cách tối ưu chưa thể cộng lại.

Phép kiểm tra sai lệch output dùng harness với 6 token và noise cố định, trong khi benchmark latency dùng 16 token. Max abs và RMSE được tính trên 50 × 7 giá trị action thực. Các sai số trên input synthetic chỉ phục vụ đối chiếu output; chất lượng thực hiện task cần được kiểm tra riêng bằng SR.

## 4. Đánh giá LIBERO

Các lượt đánh giá dùng suite `libero_object`, gồm task 0–9, với `n_action_steps=1` và seed môi trường 42. Server vẫn dùng noise ngẫu nhiên mặc định. Do đó, dù giữ cùng seed môi trường, các cấu hình chưa chắc nhận cùng noise hoặc đi theo cùng trajectory.

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

Quá trình đánh giá được chia thành ba mức: smoke chạy 1 task × 2 episode để kiểm tra luồng chạy, screening chạy 10 task × 4 episode, và official chạy 10 task × 20 episode. Riêng task 9 của defaults ở lượt official bị timeout, nên đã chạy lại đủ 20 episode và loại toàn bộ lượt chạy dở trước đó.

[Audit và bảng theo task](../smolvla-followup-20261104/TASK_RESULTS.md) kiểm tra 90 CSV / 680 episode: 400 official, 160 screening runtime/quantization và 120 screening pruning. Tất cả các CSV được chọn có `aborted=0`; hash và record từng episode nằm trong [submission-audit.json](../smolvla-followup-20261104/submission-audit.json).

## 5. Phân tích kiến trúc và thời gian thực thi

[Kiến trúc và module timing](../smolvla-followup-20261104/ARCHITECTURE_AND_PROFILE.md) mô tả vision → connector → VLM → action expert và vòng denoise. [Audit Task 5](../task5-profiling/README.md) đối chiếu sáu benchmark log và hai SQLite node trace đã lưu.

Ở đợt runtime-pair, khi chuyển từ defaults sang flash-mm, trung vị của mean qua ba lượt giảm từ 114,1 xuống 92,4 ms. Các giá trị p50 và p90 tương ứng giảm từ 114,1 xuống 92,5 ms và từ 115,4 xuống 93,0 ms. Đây là trung vị của các thống kê theo từng lượt, chưa phải percentile tính gộp từ 60 mẫu. Thời gian wall time của vision và connector giảm từ 56,1 xuống 43,6 ms.

Cần đọc số đo PHASE trong điều kiện riêng của phép đo này: graph/padding được đổi từ 48 xuống 16 language tokens, đồng thời có thao tác copy K/V và đồng bộ backend. Timer tính cả thời gian host dispatch, chờ và các khoảng trống giữa hoạt động, nên chưa thể coi đây là bản phân rã chính xác latency của defaults. Ngoài ra, thời gian vision còn bao gồm connector; thời gian denoise còn bao gồm cross-KV và solver.

Với 20 prediction được trace, tổng thời gian kernel giảm từ 2260,227 xuống 1733,185 ms. Nhóm GEMM, được phân loại theo tên kernel và có bao gồm attention matmul, chiếm tỷ lệ từ 58,30% xuống 51,85%. Các khoảng trống trong hoạt động process được ghi lại giảm từ 10,54% xuống 9,13%. Những khoảng trống này chưa đủ để kết luận toàn bộ GPU đang rảnh hoặc CPU là nút thắt.

Cả hai trace đều dùng legacy software tracing và có cảnh báo `Not all CUDA events might have been collected.` Vì vậy, các tỷ lệ trên chỉ phản ánh những event đã thu được. Để xác định nút thắt rõ hơn, vẫn cần đo riêng attention/connector và bổ sung hardware counters.

## 6. Pruning

Thử nghiệm cắt layer trực tiếp được thực hiện ở ba cấu hình: vision-tail-10, vision-spaced-10 và coupled-tail-30. Kết quả screening lần lượt là 0/40, 0/40 và 23/40 episode thành công. Với kết quả này, chưa có bản pruning nào được chọn để sử dụng. Lượt smoke 0/2 trước đó được giữ riêng, không cộng vào kết quả screening.

Các thử nghiệm trên là depth ablation: cắt bớt layer để quan sát ảnh hưởng đến tốc độ và chất lượng. Phần này chưa phải chọn layer bằng CKA. Hiện đã có tiện ích capture/CKA và kiểm thử synthetic, nhưng chưa có calibration trên dữ liệu thực, checkpoint chọn bằng CKA, finetuning hay đánh giá SR cho hướng này. Vì vậy, dù thời gian chạy module có giảm, vẫn cần đánh giá chất lượng sau khi cắt. Chi tiết nằm trong [phương pháp và script](../smolvla-pruning/README.md).

## 7. Những việc cần làm tiếp

| Hạng mục | Cần bổ sung |
|---|---|
| Kiểm thử CUDA | Sửa hai lỗi bit-exact và rerun; chưa thay tolerance |
| Chất lượng Q8 | Official200 cho từng bản Q8; tổng 400 episode nếu chạy cả hai |
| Độ ổn định SR | Protocol noise/seed rõ ràng và repeated-seed evaluation |
| Profiling | Tách connector/attention, xác minh trace completeness và source/binary provenance |
| CKA/CLP | Calibration riêng, chọn layer hợp lệ, finetuning và đánh giá mới |
| Môi trường | Lock sạch, giải quyết bảy dependency conflicts; đo resident VRAM trên backend hỗ trợ |

Trước mắt, flash-mm vẫn là lựa chọn hiện tại dựa trên latency và kết quả official đã có. Để so sánh chắc chắn hơn, cần hoàn tất đánh giá Q8 và chạy lại với protocol noise/seed rõ ràng. Các điểm cần trao đổi thêm được ghi trong [câu hỏi gửi review](review.md). [Phụ lục tính toán](calculations.md) lưu cách tính speedup, Wilson interval và các dự toán; những dự toán này được ghi riêng với kết quả đo thực tế.

## 8. Cách đối chiếu số liệu

Có thể chạy các lệnh sau từ thư mục gốc repo để đối chiếu dữ liệu đã lưu, không cần GPU hoặc model:

```bash
python3 research-notes/smolvla-followup-20261104/audit_submission.py
python3 research-notes/smolvla-followup-20261104/report_part3.py
python3 research-notes/smolvla-followup-20261104/complete_calculations.py
python3 research-notes/smolvla-followup-20261104/update_live_report.py
git diff --check
```

Các lệnh trên kiểm tra hoặc sinh lại báo cáo từ dữ liệu đã lưu, không chạy inference mới. Những file lớn như GGUF, video, log và trace vẫn được lưu cục bộ.
