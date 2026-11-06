# Task 5 — SmolVLA architecture và CUDA profiling

Ngày audit: 05/11/2026 (Asia/Bangkok). Commit tại lúc audit: `92d134a7557f4580f3b8c14042c1bad61c3f1d7c`.

Audit source và artifact đã lưu ngày 04/11, không chạy benchmark hoặc CUDA test mới. GPU có server hoạt động tại lúc audit nên chưa rerun kiểm thử. Kết luận tổng thể cập nhật ở [báo cáo chính](../../REPORT_SMOLVLA.md).

## Đọc theo thứ tự

1. [Architecture](architecture.md): luồng input → action và source anchors.
2. [Timing](timing-methodology.md): từng timer đo gì, vì sao PHASE khác default.
3. [Baseline](baseline-results.md): protocol, tất cả lượt chạy, thống kê.
4. [Nsight](nsys-analysis.md): kernel/API/memcpy/gap và cảnh báo trace.
5. [Comparison](comparison.md): số liệu so sánh có phân biệt loại phép đo.
6. [Limitations và các phần xin review](limitations.md).
7. [Giải thích kiến thức](explanation.md) và [tái lập](reproduction.md).

Kết luận được hỗ trợ: flash-mm là ứng viên runtime nhanh hơn defaults trên protocol đã lưu; trung vị mean ba lượt 114,1 → 92,4 ms (−19,0%). Cập nhật 06/11: flash-mm official 178/200 so với defaults177/200, được chọn theo SR quan sát; chưa chứng minh ưu thế thống kê. Hai bản Q8 chưa có official200. Giữ 10 bước denoise khi so sánh. `steps-3` nhanh nhưng thay đổi solver và sai khác action lớn nên không đưa vào cặp đối chứng giữ cùng số bước.

Cảnh báo quan trọng: cả hai node trace có diagnostic `Not all CUDA events might have been collected.` Các tổng bên dưới đúng với sự kiện đã lưu, chưa chứng minh coverage đầy đủ. Không gọi gap là toàn GPU idle, không gọi GEMM là module VLM.

## Môi trường được xác minh

Ubuntu 26.04.1, WSL2 kernel 6.18.33.2; RTX 3060 Laptop 6 GiB, compute capability 8.6 từ log lịch sử; nvidia-smi driver 610.43.02, KMD 610.62. CUDA compiler 13.3.73, nsys 2026.1.3.425, CMake 4.2.3. Build cache Release, CUDA ON, arch86; executable bench/cli/server có mặt. Không rebuild nên không chứng minh binary tái tạo từ commit hiện tại; hash binary hiện tại được lưu để nhận diện.

Model `/home/doris/.cache/vla/vrfai/smolvla-libero-gguf/smolvla-libero.gguf`, SHA256 hiện tại khớp lịch sử:
`6fb2d475c98b4c2cef3e27c4eff4e67b483740cbf983fff320a3b8a5e5f74fe8`.

## Bằng chứng

`logs/*/audit.json` chứa tổng tính lại, API, diagnostics, top kernels và SHA256 artifact/source/binary. `audit_evidence.py` dùng SQLite mode=ro, đối chiếu cả sáu raw benchmark log và hai node trace. Chạy lại tạo thư mục timestamp mới.

Artifact gốc được liên kết tại chỗ, không ghi đè. Phase boundary audit nằm ở `logs/20261105T040223880451Z/*-phase-audit.log` và `*.boundaries.json`; `.sqlite` tại đó là symlink tới dữ liệu gốc. Đây là kiểm tra bao phủ các kernel **đã ghi nhận**, không loại bỏ cảnh báo thiếu CUDA events.
