def main():
    with open("Lab10/Lab 10 Example.txt", "r", encoding="utf-8-sig") as f:
        data = f.read().split()

    n, m, c = int(data[0]), int(data[1]), int(data[2])
    pos = 3
    need = [0] + [int(data[pos + i]) for i in range(n)]
    pos += n

    edges = []
    for _ in range(m):
        a, b, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        edges.append((a, b, w))
    k = int(data[pos])

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[1] = 0

    # Bellman-Ford: ผ่อนคลายทุกเส้น n-1 รอบ (รองรับน้ำหนักติดลบ)
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            if dist[a] != INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                changed = True
        if not changed:
            break

    # หา negative cycle: ประเทศที่ยังลดค่าได้ (หรือต่อจากวงจรติดลบ) = -INF ใช้ไม่ได้
    NEG = -INF
    for _ in range(n):
        for a, b, w in edges:
            if dist[a] == INF:
                continue
            if dist[a] == NEG:
                dist[b] = NEG
            elif dist[a] + w < dist[b]:
                dist[b] = NEG

    # เอาเฉพาะประเทศที่ไปถึงและมีค่าแน่นอน
    countries = sorted((dist[i], i) for i in range(1, n + 1)
                       if dist[i] != INF and dist[i] != NEG)

    out = []
    for d, i in countries:
        for _ in range(need[i]):
            if len(out) == k:
                break
            out.append(d + c)
        if len(out) == k:
            break

    while len(out) < k:
        out.append(-1)

    print("\n".join(map(str, out)))


main()