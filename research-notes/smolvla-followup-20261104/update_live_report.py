"""Render current evaluation status from manifests, preserving reviewed report text."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent
START = '<!-- SMOLVLA_LIVE_START -->'
END = '<!-- SMOLVLA_LIVE_END -->'


def main():
    configurations = [
        ('Defaults screening', 'screen40-defaults/result.json'),
        ('Flash-mm screening', 'screen40-variants/flash-mm/result.json'),
        ('Q8-lm screening', 'screen40-variants/q8-lm/result.json'),
        ('Q8-vision screening', 'screen40-variants/q8-vision/result.json'),
        ('Defaults official', 'official200-defaults/result.json'),
        ('Flash-mm official', 'official200-flash-mm/result.json'),
        ('Vision-tail-10 screening', 'screen40-variants/smolvla-vision-tail-10/result.json'),
        ('Vision-spaced-10 screening', 'screen40-variants/smolvla-vision-spaced-10/result.json'),
        ('Coupled-tail-30 screening', 'screen40-variants/smolvla-coupled-tail-30/result.json'),
    ]
    lines = [START, '## Hiện trạng đánh giá từ manifest', '',
             'Bảng sinh bằng `update_live_report.py`; audit CSV và hash ở '
             '[TASK_RESULTS.md](research-notes/smolvla-followup-20261104/TASK_RESULTS.md).', '',
             '| Cấu hình | Thành công / episode hoàn tất | SR quan sát | Trạng thái |',
             '|---|---:|---:|---|']
    official = []
    for label, relative in configurations:
        result = json.loads((DATA / relative).read_text())
        n, k = result['completed_episodes'], result['successes']
        state = result['state']
        if state == 'complete':
            assert n == result['expected_episodes'], relative
        lines.append(f'| {label} | {k}/{n} | {100*k/n:.1f}% | {state} |')
        if label.endswith('official') and state == 'complete' and n == 200:
            official.append((k/n, label, k, n))
    if official:
        top = max(r[0] for r in official)
        winners = [r for r in official if r[0] == top]
        lines += ['', 'SR official quan sát cao nhất trong các bản đã hoàn tất 200 episode: '
                  + ', '.join(f'{label} {k}/{n}' for _, label, k, n in winners) + '. '
                  'Chưa chứng minh ưu thế thống kê; hai bản Q8 và repeated-seed chưa có official.']
    lines += ['', 'Smoke, screening và official là các lượt riêng, không cộng mẫu số. '
              'Pruning hiện là depth ablation; có tiện ích CKA/capture nhưng chưa calibration thực hoặc finetuning.', END]
    block = '\n'.join(lines) + '\n'
    path = ROOT / 'REPORT_SMOLVLA.md'
    content = path.read_text()
    pattern = re.escape(START) + r'.*?' + re.escape(END) + r'\n?'
    if re.search(pattern, content, re.S):
        content = re.sub(pattern, lambda _: block, content, count=1, flags=re.S)
    else:
        title, rest = content.split('\n', 1)
        content = title + '\n\n' + block + '\n' + rest
    path.write_text(content)
    print('Updated manifest status; preserved report outside managed markers.')


if __name__ == '__main__':
    main()
