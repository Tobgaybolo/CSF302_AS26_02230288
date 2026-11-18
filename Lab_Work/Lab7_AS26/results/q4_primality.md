# Q4.2 - Miller-Rabin vs trial division (seed 42)

## 20 random 12-digit numbers

| n | trial division | Miller-Rabin | MR (us) | trial (us) |
| --- | --- | --- | --- | --- |
| 223,005,401,501 | prime | prime | 233.0 | 19,064.1 |
| 911,856,239,313 | composite | composite | 14.9 | 0.5 |
| 367,469,214,295 | composite | composite | 13.0 | 0.4 |
| 251,282,538,206 | composite | composite | 0.3 | 0.3 |
| 214,832,269,481 | composite | composite | 11.6 | 30.3 |
| 914,655,221,101 | composite | composite | 13.5 | 0.9 |
| 700,832,336,208 | composite | composite | 0.3 | 0.2 |
| 748,913,461,122 | composite | composite | 0.2 | 0.2 |
| 136,171,878,809 | composite | composite | 13.1 | 10.6 |
| 198,912,225,902 | composite | composite | 0.2 | 0.2 |
| 354,342,113,419 | composite | composite | 12.5 | 0.5 |
| 763,595,448,017 | composite | composite | 13.6 | 3.3 |
| 714,294,294,451 | composite | composite | 14.0 | 5.8 |
| 886,833,016,361 | prime | prime | 254.5 | 36,998.3 |
| 871,590,378,377 | composite | composite | 15.0 | 4.1 |
| 561,902,006,518 | composite | composite | 0.2 | 0.2 |
| 590,573,056,992 | composite | composite | 0.2 | 0.2 |
| 407,473,554,860 | composite | composite | 0.2 | 0.2 |
| 933,251,567,391 | composite | composite | 13.2 | 0.3 |
| 275,259,659,197 | prime | prime | 254.0 | 20,926.7 |

## Extra: 12-digit primes (worst case for trial division)

| 12-digit prime | Miller-Rabin (us) | trial division (ms) | trial / MR |
| --- | --- | --- | --- |
| 840,633,436,777 | 242.8 | 37.9 | 156x |
| 597,707,816,159 | 238.4 | 31.7 | 133x |
| 116,633,204,627 | 255.7 | 14.2 | 55x |
| 439,982,645,429 | 223.2 | 27.2 | 122x |
| 357,991,902,637 | 261.0 | 24.9 | 95x |
