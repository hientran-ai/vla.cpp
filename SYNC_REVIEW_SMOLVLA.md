# Đồng bộ nội dung SmolVLA — 06/11/2026

Rà soát các tài liệu nghiên cứu hiện hành, script sinh báo cáo, manifest kết quả và CSV đã hoàn tất. Không chạy benchmark, simulator hoặc CUDA tests mới. Nhật ký theo thời điểm và snapshot archive giữ kết quả lịch sử; chúng không đại diện cho hiện trạng.

## Kết quả thống nhất

| Cấu hình | Screening | Official |
|---|---:|---:|
| Defaults | 38/40 | 177/200 (88,5%) |
| Flash-mm | 35/40 | 178/200 (89,0%) |
| Q8-lm | 36/40 | Chưa đo |
| Q8-vision | 36/40 | Chưa đo |
| Vision-tail-10 | 0/40 | Chưa đo |
| Vision-spaced-10 | 0/40 | Chưa đo |
| Coupled-tail-30 | 23/40 | Chưa đo |

Chọn flash-mm theo SR official quan sát cao nhất trong các cấu hình đã hoàn tất 200 episode. Chênh lệch một episode chưa chứng minh ưu thế thống kê hoặc chất lượng ổn định qua nhiều seed. Screening và official là các lượt riêng; không cộng mẫu số hoặc so trực tiếp hai loại đánh giá để xếp hạng.

## Những gì đã sửa trong lượt đồng bộ

| Tệp / nhóm tệp | Nội dung thay đổi |
|---|---|
| `NOTES_SMOLVLA.md` | Cập nhật checklist đầu file: official flash-mm, screening pruning, trạng thái CKA và audit 680 episode. Giữ nhật ký lịch sử phía sau. |
| `REPORT_SMOLVLA.md`, `SUBMISSION_SMOLVLA.md`, `REVIEW_REQUESTS.md` | Bỏ các kết luận hiện hành còn chọn defaults hoặc nói flash-mm chưa có official; cập nhật phạm vi, ngày, số CSV/episode, phần còn thiếu của Q8 và pruning. |
| `PART3_OPTIMIZATION.md` | Thống nhất lựa chọn theo SR; giữ nguyên bảng số đo và control của batch phần 3. |
| `CALCULATIONS_SMOLVLA.md` | Bổ sung cột screening pruning cạnh smoke lịch sử; phân biệt tiện ích CKA với thí nghiệm CKA thực. Giữ dự toán có nhãn và số đo official riêng. |
| `ARCHITECTURE_AND_PROFILE.md`, `task5-profiling/README.md` | Thống nhất official flash-mm và pruning; ghi rõ kiểm tra coverage chỉ áp dụng cho các kernel đã ghi nhận. Tách tình trạng Git/GPU lúc audit cũ khỏi hiện trạng. |
| `smolvla-pruning/README.md` | Sửa mô tả lưu trữ: 30 CSV pruning được đưa vào Git; video/log vẫn cục bộ. |
| `audit_submission.py`, `TASK_RESULTS.md`, `submission-audit.json` | Audit chín lượt/cấu hình, 90 CSV, 680 episode; thêm ba pruning và hash/record từng episode. Bảng có official flash-mm và pruning theo task. |
| `audit_screening.py`, `screening-final-audit.json`, `submission-progress.json` | Official dùng khóa `official_sr`; sắp task theo ID; snapshot tiến độ đọc kết quả official hiện có, không còn ghi mọi biến thể chưa đo official. |
| `report_part3.py` | Sinh bảng bằng kích thước đã lưu, không cần file GGUF local; giữ các đoạn audit/giải thích được bổ sung khi sinh lại. |
| `complete_calculations.py` | Sinh lại cột screening pruning và trạng thái CKA thống nhất với tài liệu. |
| `update_live_report.py` | Thay trạng thái live cũ bằng bảng đọc từ chín manifest; chỉ chọn trong official đã hoàn tất, không ghi đè phần báo cáo ngoài markers. |
| Liên kết tài liệu | Thay hai link tới `PAPER_READING_SMOLVLA_CLP.md` đã bị xóa; sửa đường dẫn tương đối trong archive `REPORT_HISTORY.md`. |
| Dữ liệu | Bổ sung 30 CSV screening pruning đang bị ignore, để audit có thể chạy từ bản clone. Không sửa kết quả CSV hoặc manifest thí nghiệm. |

## Kiểm tra đã thực hiện

- Đối chiếu 90 CSV / 680 episode: task ID, episode ID, steps, success, aborted, SR và hash; tất cả aborted=0.
- Kiểm tra link local trong toàn bộ 19 tài liệu Markdown nghiên cứu hiện có tại thời điểm rà soát: không còn target mất.
- Parse các Python/JSON thay đổi và chạy `git diff --check`.
- Sao chép bộ tài liệu/script/JSON/CSV dự kiến commit vào thư mục tạm, không có GGUF, build hoặc GPU. Chạy thành công bốn script dưới đây, rồi chạy lần hai: đầu ra không đổi.

```bash
python3 research-notes/smolvla-followup-20261104/audit_submission.py
python3 research-notes/smolvla-followup-20261104/report_part3.py
python3 research-notes/smolvla-followup-20261104/complete_calculations.py
python3 research-notes/smolvla-followup-20261104/update_live_report.py
git diff --check
```

## Giới hạn còn giữ nguyên

Hai CUDA tests có kết quả fail lịch sử, chưa rerun/sửa; chưa có official Q8 hoặc repeated-seed; chưa có checkpoint CKA/calibration thực/finetuning; chưa tách connector/attention đầy đủ; resident process VRAM trên WSL chưa đo được. Không ghép latency giữa các batch hoặc đồng nhất minimum run mean với median run means. Cảnh báo thiếu CUDA events vẫn được công bố.

`STUDY_GUIDE_SMOLVLA.md` có trong danh sách tab IDE nhưng không tồn tại trong working tree hoặc danh sách file Git hiện tại, nên không có nội dung để đối chiếu. `on.txt`, `off.txt` và metadata tải từ PyPI giữ local; không nằm trong commit đồng bộ.
