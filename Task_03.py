import timeit
from typing import Callable, Dict

def boyer_moore_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    bad_char = {c: i for i, c in enumerate(pattern)}
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        char = text[i + j]
        last_occ = bad_char.get(char, -1)
        i += max(1, j - last_occ)
    return -1

def _kmp_prefix(pattern: str):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    lps = _kmp_prefix(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    base = 256
    mod = 10**9 + 7
    pat_hash = 0
    txt_hash = 0
    h = 1
    for _ in range(m - 1):
        h = (h * base) % mod
    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        txt_hash = (txt_hash * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if pat_hash == txt_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            txt_hash = (txt_hash - ord(text[i]) * h) % mod
            txt_hash = (txt_hash * base + ord(text[i + m])) % mod
            txt_hash = (txt_hash + mod) % mod
    return -1

ARTICLE1_PATH = "article_1.txt"
ARTICLE2_PATH = "article_2.txt"

PATTERNS = {
    "article1": {
        "exists": "жадібний алгоритм",
        "missing": "вигаданий підрядок, якого немає у цьому тексті",
    },
    "article2": {
        "exists": "рекомендаційної системи",
        "missing": "вигаданий підрядок, якого немає у цьому тексті",
    },
}

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def measure_time(
    func: Callable[[str, str], int],
    text: str,
    pattern: str,
    repeat: int = 5,
    number: int = 10,
) -> float:
    timer = timeit.Timer(lambda: func(text, pattern))
    runs = timer.repeat(repeat=repeat, number=number)
    return min(runs) / number

def main():
    text1 = read_file(ARTICLE1_PATH)
    text2 = read_file(ARTICLE2_PATH)

    algorithms: Dict[str, Callable[[str, str], int]] = {
        "Boyer-Moore": boyer_moore_search,
        "Knuth-Morris-Pratt": kmp_search,
        "Rabin-Karp": rabin_karp_search,
    }

    results = {
        "article1": {"exists": {}, "missing": {}},
        "article2": {"exists": {}, "missing": {}},
    }

    for article_name, text in [("article1", text1), ("article2", text2)]:
        for case in ("exists", "missing"):
            pattern = PATTERNS[article_name][case]
            for alg_name, func in algorithms.items():
                t = measure_time(func, text, pattern)
                results[article_name][case][alg_name] = t

    for article_name in ("article1", "article2"):
        print(f"\n=== {article_name.upper()} ===")
        for case in ("exists", "missing"):
            print(f"\n  Підрядок: {case}")
            for alg_name, t in results[article_name][case].items():
                print(f"    {alg_name:20s}: {t:.6f} сек")

    print("\n=== Підсумки ===")
    for article_name in ("article1", "article2"):
        for case in ("exists", "missing"):
            best_alg = min(
                results[article_name][case].items(),
                key=lambda x: x[1],
            )[0]
            print(f"{article_name}, '{case}' → найшвидший: {best_alg}")

if __name__ == "__main__":
    main()