import sys


def main():
    # เปลี่ยนชื่อไฟล์ให้ตรงกับที่คุณใช้งาน หรือใช้ "test.txt"
    with open("test.txt", "r", encoding="utf-8-sig") as f:        data = f.read().split()

    if not data:
        return

    pos = 0
    n, m, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
    pos += 3

    # อ่านความต้องการคน (need) ของแต่ละประเทศ
    need = [0] + [int(data[pos + i]) for i in range(n)]
    pos += n

    # อ่านข้อมูลเส้นทาง (Edges)
    edges = []
    for _ in range(m):
        a, b, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        edges.append((a, b, w))

    # อ่านค่า k (จำนวนคนที่ต้องการแจกจ่าย) ตัวสุดท้าย
    k = int(data[pos])

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[1] = 0

    # Parent array สำหรับแกะรอยเส้นทาง
    parent = [-1] * (n + 1)

    # Bellman-Ford: ผ่อนคลายทุกเส้น n-1 รอบ (รองรับน้ำหนักติดลบ)
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            if dist[a] != INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                parent[b] = a
                changed = True
        if not changed:
            break

    # ตรวจจับ Negative cycle
    NEG = -INF
    for _ in range(n):
        for a, b, w in edges:
            if dist[a] == INF:
                continue
            if dist[a] == NEG:
                dist[b] = NEG
            elif dist[a] + w < dist[b]:
                dist[b] = NEG

    # ฟังก์ชันแกะรอยเส้นทาง
    def get_path(target):
        if dist[target] == INF or dist[target] == NEG:
            return []
        path = []
        curr = target
        while curr != -1:
            path.append(curr)
            curr = parent[curr]
        return list(reversed(path))

    # คัดเลือกและเรียงลำดับประเทศตามระยะทางจากน้อยไปมาก
    countries = sorted(
        (dist[i], i) for i in range(1, n + 1) if dist[i] != INF and dist[i] != NEG
    )

    out = []
    print("--- รายละเอียดการแจกจ่ายคนและเส้นทาง ---")
    person_idx = 1
    for d, i in countries:
        path = get_path(i)
        path_str = " -> ".join(map(str, path))
        for _ in range(need[i]):
            if len(out) == k:
                break
            cost = d + c
            print(
                f"คนที่ {person_idx}: ไปประเทศ {i} (เส้นทาง: {path_str}) | ระยะทาง: {d} + ค่าเดินทาง {c} = {cost}"
            )
            out.append(cost)
            person_idx += 1
        if len(out) == k:
            break

    # หากที่ว่างไม่พอ เติม -1 ให้ครบ k คน
    while len(out) < k:
        print(f"คนที่ {person_idx}: ไม่มีที่ไป -> -1")
        out.append(-1)
        person_idx += 1

    print("\n--- ผลลัพธ์สุดท้าย (Output) ---")
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()