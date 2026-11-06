# Pruning: scripts và kết quả screening

## Kết quả đã đối chiếu CSV

| Cấu hình | Thành công | SR |
|---|---:|---:|
| vision-tail-10 | 0/40 | 0% |
| vision-spaced-10 | 0/40 | 0% |
| coupled-tail-30 | 23/40 | 57,5% |

Mỗi cấu hình: libero_object, 10 task × 4 episode, seed môi trường 42,
n_action_steps=1; noise server ngẫu nhiên. Đã đối chiếu 30 CSV: 120 episode,
không abort. Protocol và result từng cấu hình ở
`../smolvla-followup-20261104/screen40-variants/`.
30 CSV screening pruning đã lưu trong Git để audit; video và log vẫn là artifact cục bộ.
Defaults screening 38/40; chưa chứng minh pruning giữ chất lượng.
Smoke 0/2 trước đó và screening mới là các lượt riêng, không cộng mẫu số.

## Vai trò các script

- `run_screening.py`: chạy tuần tự ba depth ablation qua runner hiện có.
- `capture.py`: tiện ích hook thu activation; cần adapter checkpoint và dữ liệu calibration thực.
- `cka_prune.py`: chọn layer theo linear CKA và ràng buộc attention từ activation NPZ.
  Đây là adaptation thử nghiệm, chưa có activation calibration thực, checkpoint CKA,
  finetuning hoặc SR cho cấu hình CKA. Không gọi là tái hiện hoàn chỉnh CLP.
- `test_*.py`: kiểm tra toán CKA, lựa chọn layer và capture bằng dữ liệu kiểm thử.

Chạy kiểm tra từ gốc repo (Python có numpy và torch):

```bash
python3 -m unittest discover -s research-notes/smolvla-pruning -p 'test_*.py'
```

## Kết quả chung

Official flash-mm và lựa chọn cấu hình nằm trong [báo cáo chính](../smolvla/report.md). Bảng này chỉ đánh giá pruning; không dùng kết quả runtime để suy ra hiệu quả pruning.
