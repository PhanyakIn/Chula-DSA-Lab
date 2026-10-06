from collections import deque


def set_parser(s: str) -> list[str]:
    """Extracts top-level elements by comma, respecting nested braces."""
    s = s.strip()
    # Remove only the outermost pair of braces
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]
    s = s.strip()
    if not s:
        return []

    elements: list[str] = []
    current: list[str] = []
    depth = 0
    seen: set[str] = set()

    for char in s:
        if char == "{":
            depth += 1
            current.append(char)
        elif char == "}":
            depth -= 1
            current.append(char)
        elif char == ",":
            # Only split on commas at the top level
            if depth == 0:
                elem = "".join(current).strip()
                if elem and elem not in seen:
                    seen.add(elem)
                    elements.append(elem)
                current.clear()
            else:
                current.append(char)
        else:
            current.append(char)

    if current:
        elem = "".join(current).strip()
        if elem and elem not in seen:
            seen.add(elem)
            elements.append(elem)

    return elements


def sub_sets(elements: list[str]) -> list[list[str]]:
    """Generates all subsets using a BFS queue approach."""
    q: deque[list[str]] = deque([[]])

    for elem in elements:
        for _ in range(len(q)):
            curr = q.popleft()

            # Branch 1: Exclude element
            q.append(list(curr))

            # Branch 2: Include element
            q.append(curr + [elem])

    return list(q)


def subset_f(subsets: list[list[str]]) -> list[str]:
    """Formats each subset as a brace-enclosed string."""
    return [f"{{{', '.join(sub)}}}" for sub in subsets]


def main():
    filename = "Lab2/test3.txt"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, 1):
                raw_set = line.strip()
                if not raw_set:
                    continue  # ข้ามบรรทัดว่าง

                elements = set_parser(raw_set)
                all_subsets = sub_sets(elements)
                formatted_subsets = subset_f(all_subsets)

                print(f"Line {line_number}: {raw_set}")
                print(f"Parsed Elements: {elements}")
                print(f"Subsets Count: {len(formatted_subsets)}")
                print(f"Power Set: {', '.join(formatted_subsets)}")
                print("-" * 50)

    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ '{filename}' กรุณาตรวจสอบตำแหน่งของไฟล์")


if __name__ == "__main__":
    main()