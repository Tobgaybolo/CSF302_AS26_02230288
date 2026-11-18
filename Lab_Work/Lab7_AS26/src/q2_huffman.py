"""
CSF302 Lab 7 - Q2: Huffman Coding

  1. Build a Huffman tree from the character frequencies of a text file
     (priority queue: heapq, which the lab allows)
  2. Print the code table
  3. Encode the file into a bit string, decode it, check decoded == original
  4. Compression ratio vs 8-bit fixed-length encoding for several files:
       ../data/texts/english.txt          English prose
       ../data/texts/source_code.txt      Python source (a copy of q1_greedy.py)
       ../data/texts/dna.txt              random A/C/G/T, 20,000 characters
       ../data/texts/random_printable.txt random printable ASCII, 20,000 characters

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q2_huffman.py                 (all four sample files)
      python q2_huffman.py FILE [FILE...]  (your own files)
"""
import heapq
import math
import sys
from pathlib import Path

from timing_utils import markdown_table


class Node:
    """Leaf: symbol set, left/right None. Internal: symbol None."""
    __slots__ = ("freq", "symbol", "left", "right")

    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq, self.symbol, self.left, self.right = freq, symbol, left, right


def char_frequencies(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq):
    """Repeatedly remove the two lowest-frequency nodes and join them under a
    new node with their combined frequency. n-1 merges, each O(log n):
    Theta(n log n) for n distinct symbols. The counter breaks ties so that
    heapq never compares Node objects (and makes the result deterministic)."""
    if not freq:
        raise ValueError("empty text")
    heap = []
    counter = 0
    for sym in sorted(freq):                      # fixed order -> reproducible codes
        heap.append((freq[sym], counter, Node(freq[sym], sym)))
        counter += 1
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, Node(f1 + f2, left=a, right=b)))
        counter += 1
    return heap[0][2]


def build_codes(root):
    """Left edge = '0', right edge = '1'. A one-symbol text gets code '0'."""
    if root.symbol is not None:
        return {root.symbol: "0"}
    codes = {}
    stack = [(root, "")]
    while stack:
        node, prefix = stack.pop()
        if node.symbol is not None:
            codes[node.symbol] = prefix
        else:
            stack.append((node.right, prefix + "1"))
            stack.append((node.left, prefix + "0"))
    return codes


def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, root):
    """Walk from the root; at a leaf output its symbol and restart. Because no
    code is a prefix of another, this is unambiguous."""
    if root.symbol is not None:                   # one-symbol text
        return root.symbol * len(bits)
    out, node = [], root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.symbol is not None:
            out.append(node.symbol)
            node = root
    if node is not root:
        raise ValueError("bit string ended in the middle of a code")
    return "".join(out)


def show(ch):
    return {" ": "' '", "\n": "\\n", "\t": "\\t"}.get(ch, ch)


def process(path, print_table=True):
    text = Path(path).read_text(encoding="utf-8")
    freq = char_frequencies(text)
    root = build_huffman_tree(freq)
    codes = build_codes(root)
    bits = encode(text, codes)
    decoded = decode(bits, root)
    assert decoded == text, "decoded text differs from the original!"

    n = len(text)
    fixed_bits = 8 * n
    ratio = len(bits) / fixed_bits
    avg = len(bits) / n
    entropy = -sum(f / n * math.log2(f / n) for f in freq.values())
    min_fixed = max(1, math.ceil(math.log2(len(freq))))

    # prefix-free check
    cl = sorted(codes.values())
    assert all(not cl[i + 1].startswith(cl[i]) for i in range(len(cl) - 1))

    print(f"\n=== {path} ===")
    print(f"characters = {n:,}, distinct = {len(freq)}")
    if print_table:
        rows = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
        limit = rows if len(rows) <= 30 else rows[:15] + rows[-5:]
        print(f"{'char':>6} {'freq':>7}  code")
        for i, (ch, f) in enumerate(limit):
            if len(rows) > 30 and i == 15:
                print(f"{'...':>6}   ({len(rows) - 20} more rows in results file)")
            print(f"{show(ch):>6} {f:>7}  {codes[ch]}")
    print(f"first 64 encoded bits: {bits[:64]}...")
    print(f"decoded == original: {decoded == text}")
    print(f"Huffman bits = {len(bits):,}  vs  8-bit fixed = {fixed_bits:,}  "
          f"-> ratio {ratio:.3f} ({1 - ratio:.1%} smaller)")
    print(f"average code length {avg:.3f} bits/char, entropy {entropy:.3f}, "
          f"best fixed-length code would need {min_fixed} bits/char")

    with open(f"../results/q2_codes_{Path(path).stem}.txt", "w", encoding="utf-8") as f:
        f.write(f"Huffman code table for {path}\nchar\tfreq\tcode\n")
        for ch, fr in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
            f.write(f"{show(ch)}\t{fr}\t{codes[ch]}\n")
    return (Path(path).name, n, len(freq), fixed_bits, len(bits), f"{ratio:.3f}",
            f"{1 - ratio:.1%}", f"{avg:.3f}", f"{entropy:.3f}", min_fixed)


def main(paths):
    rows = [process(p) for p in paths]
    table = markdown_table(["file", "chars", "distinct", "8-bit size (bits)", "Huffman (bits)",
                            "ratio", "saving", "avg bits/char", "entropy", "fixed ⌈log2 n⌉"],
                           rows)
    print("\n" + table)
    with open("../results/q2_huffman.md", "w", encoding="utf-8") as f:
        f.write("# Q2 - Huffman compression vs 8-bit fixed length\n\n" + table + "\n")
    print("\nSaved ../results/q2_huffman.md and q2_codes_*.txt")


if __name__ == "__main__":
    args = sys.argv[1:] or [f"../data/texts/{n}" for n in
                            ("english.txt", "source_code.txt", "dna.txt", "random_printable.txt")]
    main(args)

# ---------------------------------------------------------------------------
# Analysis / conclusion
#
# | file                 | chars  | distinct | Huffman / 8-bit | saving | bits/char | entropy |
# |----------------------|--------|----------|-----------------|--------|-----------|---------|
# | english.txt          | 2,935  | 50       | 0.543           | 45.7%  | 4.342     | 4.314   |
# | source_code.txt      | 11,691 | 81       | 0.599           | 40.1%  | 4.790     | 4.762   |
# | dna.txt              | 20,001 | 5        | 0.281           | 71.9%  | 2.244     | 2.001   |
# | random_printable.txt | 20,001 | 96       | 0.830           | 17.0%  | 6.637     | 6.567   |
#
# All four files decoded back to exactly the original text, and every code
# table was checked to be prefix-free.
#
# - English: space (497) and 'e' (329) get 3-bit codes, while single
#   capitals get 12 bits. The skewed letter frequencies give a 46% saving.
# - Source code: dominated by spaces (indentation, 2-bit code) and the
#   '-' of comment rulers. 81 distinct symbols -> 40% saving.
# - DNA: only 4 letters (+1 newline), so ~2 bits/char instead of 8 -> 72%.
#   Most of that saving would come even from a 2-bit fixed code. The one
#   newline forces one letter (G) to share a branch and take 3 bits, which is
#   why the average is 2.244 rather than the entropy 2.001.
# - Random printable: 96 almost equally likely symbols. Huffman cannot do
#   better than ~log2(96) = 6.58 bits, so the saving (17%) comes only from
#   not needing all 8 bits. This is the worst case for Huffman.
#
# In every file the average code length is within 1 bit of the entropy
# H <= L < H + 1, as the theory says Huffman guarantees. The more uneven the
# frequencies, the bigger the gain over a fixed-length code.
# Note: the ratio counts only the encoded bits. A real compressed file must
# also store the code table, which matters for small files.
# Complexity: counting Theta(N) for N characters, building the tree
# Theta(n log n) for n distinct symbols, encoding and decoding Theta(total bits).
# ---------------------------------------------------------------------------
