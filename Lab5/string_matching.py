import sys


def get_lps(pattern):
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    return pi


def search_kmp_raw(text_circular, pattern):
    pi = get_lps(pattern)
    m = len(pattern)
    n = len(text_circular)
    start_indices = []

    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text_circular[i]:
            q = pi[q - 1]
        if pattern[q] == text_circular[i]:
            q += 1
        if q == m:
            start_indices.append(i - m + 1)  # ตำแหน่งจุดเริ่มต้น (0-based)
            q = pi[q - 1]

    return pi, start_indices


def kmp_search(text, pattern):
    orig_n = len(text)
    m = len(pattern)
    
    # เพื่อรองรับการวนรอบวงกลมแบบสมบูรณ์ นำ Text มาต่อเพิ่มอีก (m - 1) ตัวอักษรแรก
    text_circular = text + text[: m - 1]
    matches = []

    # 1. Search Left-to-Right (LR)
    pi, lr_starts = search_kmp_raw(text_circular, pattern)
    for start_pos in lr_starts:
        # ตำแหน่งเริ่มต้นในการค้นหาต้องไม่เกินความยาวเดิมของ text (0 ถึง orig_n - 1)
        if start_pos < orig_n:
            matches.append((start_pos + 1, "LR"))

    # 2. Search Right-to-Left (RL)
    rev_pattern = pattern[::-1]
    _, rl_starts = search_kmp_raw(text_circular, rev_pattern)
    for start_pos in rl_starts:
        if start_pos < orig_n:
            # ตำแหน่งตัวอักษรแรกของ Pattern ดั้งเดิมเมื่ออ่านทิศทาง RL
            first_char_pos = (start_pos + m - 1) % orig_n + 1
            matches.append((first_char_pos, "RL"))

    matches = list(set(matches))
    matches.sort(key=lambda x: (x[0], x[1]))
    return pi, matches


def naive_search(text, pattern):
    orig_n = len(text)
    m = len(pattern)
    matches = []

    text_circular = text + text[: m - 1]

    # 1. Search Left-to-Right (LR)
    for i in range(orig_n):
        if text_circular[i : i + m] == pattern:
            matches.append((i + 1, "LR"))

    # 2. Search Right-to-Left (RL)
    rev_pattern = pattern[::-1]
    for i in range(orig_n):
        if text_circular[i : i + m] == rev_pattern:
            first_char_pos = (i + m - 1) % orig_n + 1
            matches.append((first_char_pos, "RL"))

    matches = list(set(matches))
    matches.sort(key=lambda x: (x[0], x[1]))
    return matches


# --- ส่วนอ่านข้อมูลจากไฟล์ ---
def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "Lab5/5.4.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            tokens = f.read().split()
    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ชื่อ '{filename}'")
        return

    if not tokens:
        print("Error: ไฟล์ไม่มีข้อมูล")
        return

    idx = 0
    while idx < len(tokens) and not tokens[idx].isdigit():
        idx += 1

    alphabet = tokens[:idx]
    n = int(tokens[idx])
    m = int(tokens[idx + 1])
    idx += 2

    pattern = "".join(tokens[idx : idx + n])
    idx += n

    text = "".join(tokens[idx : idx + m])

    # --- ประมวลผล KMP และ Naïve ---
    kmp_pi, kmp_matches = kmp_search(text, pattern)
    naive_matches = naive_search(text, pattern)

    # --- แสดงผลลัพธ์ KMP ---
    print("=== KMP Output ===")
    print("".join(map(str, kmp_pi)))
    print(len(kmp_matches))
    for pos, direction in kmp_matches:
        print(f"{pos} {direction}")

    print()

    # --- แสดงผลลัพธ์ Naïve ---
    print("=== Naïve Output ===")
    print(len(naive_matches))
    for pos, direction in naive_matches:
        print(f"{pos} {direction}")


if __name__ == "__main__":
    main()