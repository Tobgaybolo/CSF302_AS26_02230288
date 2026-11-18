# Q2 - Huffman compression vs 8-bit fixed length

| file | chars | distinct | 8-bit size (bits) | Huffman (bits) | ratio | saving | avg bits/char | entropy | fixed ⌈log2 n⌉ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| english.txt | 2935 | 50 | 23480 | 12744 | 0.543 | 45.7% | 4.342 | 4.314 | 6 |
| source_code.txt | 11691 | 81 | 93528 | 55996 | 0.599 | 40.1% | 4.790 | 4.762 | 7 |
| dna.txt | 20001 | 5 | 160008 | 44892 | 0.281 | 71.9% | 2.244 | 2.001 | 3 |
| random_printable.txt | 20001 | 96 | 160008 | 132740 | 0.830 | 17.0% | 6.637 | 6.567 | 7 |
