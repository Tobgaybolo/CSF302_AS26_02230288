# Q4.1 - quickselect vs sort+index, k = n/2 (median of 3, seed 42)

| n | quickselect (s) | merge sort + index (s) | speed-up vs merge sort | built-in sorted() + index (s) |
| --- | --- | --- | --- | --- |
| 10,000 | 0.0027 | 0.0200 | 7.3x | 0.0012 |
| 30,000 | 0.0080 | 0.0533 | 6.6x | 0.0055 |
| 100,000 | 0.0233 | 0.2216 | 9.5x | 0.0166 |
| 300,000 | 0.0993 | 0.8681 | 8.7x | 0.0550 |
| 1,000,000 | 0.3660 | 3.1447 | 8.6x | 0.3190 |
