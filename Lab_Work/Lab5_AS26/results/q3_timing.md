# Q3 - inversion counting timing (seed 42)

| n | inversions | brute force (s) | merge-based (s) | note |
| --- | --- | --- | --- | --- |
| 1,000 | 243,362 | 0.0225 | 0.0011 |  |
| 2,000 | 1,005,397 | 0.0902 | 0.0032 |  |
| 5,000 | 6,195,597 | 0.5924 | 0.0084 |  |
| 10,000 | 25,151,963 | 2.1102 | 0.0190 |  |
| 20,000 | 100,683,842 | 8.0908 | 0.0313 |  |
| 50,000 | 625,213,658 | 53.6768 | 0.1291 | 1 run |
| 100,000 | 2,502,994,930 | — | 0.2557 | stopped: exceeded 60 s |
| 200,000 | 10,001,098,705 | — | 0.4945 | skipped (a smaller n already exceeded 60 s) |
| 500,000 | 62,467,515,644 | — | 1.4579 | skipped (a smaller n already exceeded 60 s) |
| 1,000,000 | 249,971,295,182 | — | 3.2192 | skipped (a smaller n already exceeded 60 s) |
