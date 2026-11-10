import sys
import heapq


def main():
    with open("Lab10/Lab 10 Example.txt", "r", encoding="utf-8-sig") as f:
        data = f.read().split()
    pos = 0

    n, m, c = int(data[0]), int(data[1]), int(data[2])
    pos = 3

    need = [0] + [int(data[pos + i]) for i in range(n)]  # need[i] = จำนวนคนที่ประเทศ i ต้องการ
    pos += n

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[a].append((b, w))

    k = int(data[pos])

    # Dijkstra จากประเทศ 1
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))

    # เรียงประเทศตามระยะทาง (เฉพาะที่ไปถึง) แล้วแจกคนไปทีละที่ว่าง
    countries = sorted((dist[i], i) for i in range(1, n + 1) if dist[i] != INF)

    out = []
    for d, i in countries:
        for _ in range(need[i]):
            if len(out) == k:
                break
            out.append(d + c)
        if len(out) == k:
            break

    # ที่ว่างไม่พอ -> พิมพ์ -1
    while len(out) < k:
        out.append(-1)

    print("\n".join(map(str, out)))


main()