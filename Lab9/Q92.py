import sys

# เพิ่มขีดจำกัดของ recursion เพื่อรองรับกราฟที่มีขนาดใหญ่หรือลึกมาก
sys.setrecursionlimit(200000)

def solve():
    # 1. อ่านข้อมูลจากไฟล์ Lab9/testcase.txt
    try:
        with open('Lab9/testcase.txt', 'r') as f:
            input_data = f.read().split()
    except FileNotFoundError:
        print("ไม่พบไฟล์ Lab9/testcase.txt")
        return
        
    if not input_data:
        return
        
    n = int(input_data[0])  # จำนวนเกาะทั้งหมด
    m = int(input_data[1])  # จำนวนถนนทั้งหมด
    
    # สร้าง Adjacency List สำหรับกราฟปกติ (adj) และกราฟกลับทิศทาง (rev_adj)
    adj = [[] for _ in range(n + 1)]
    rev_adj = [[] for _ in range(n + 1)]
    
    # อ่านข้อมูลถนนเชื่อมต่อแบบทิศทางเดียว (u -> v)
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        rev_adj[v].append(u)
        idx += 2

    # -------------------------------------------------------------
    # ขั้นตอนที่ 1: DFS บนกราฟปกติ เพื่อหา Finishing Time (Order)
    # -------------------------------------------------------------
    visited = [False] * (n + 1)
    order = []
    
    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)
        
    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)
            
    # -------------------------------------------------------------
    # ขั้นตอนที่ 2: DFS บนกราฟกลับทิศทาง เพื่อดึงสมาชิก SCC แต่ละกลุ่ม
    # -------------------------------------------------------------
    visited = [False] * (n + 1)
    
    def dfs2(u, component):
        visited[u] = True
        component.append(u)
        for v in rev_adj[u]:
            if not visited[v]:
                dfs2(v, component)

    all_sccs = []
    
    # รัน DFS รอบสองตามลำดับย้อนหลังของ order
    for i in range(n - 1, -1, -1):
        u = order[i]
        if not visited[u]:
            component = []
            dfs2(u, component)
            all_sccs.append(component)

    num_sccs = len(all_sccs)

    # -------------------------------------------------------------
    # ส่วนที่ 1: แสดงผล SCC ทั้งหมดที่พบ
    # -------------------------------------------------------------
    print("==================================================")
    print(f"           พบ SCC ทั้งหมด {num_sccs} กลุ่ม")
    print("==================================================")
    
    best_scc = None
    best_size = -1
    best_edges = float('inf')

    for idx_scc, scc in enumerate(all_sccs, 1):
        scc_set = set(scc)
        size = len(scc)
        
        # นับจำนวนถนนจริงภายใน SCC นี้
        actual_edges = 0
        for u in scc:
            for v in adj[u]:
                if v in scc_set:
                    actual_edges += 1

        min_required_edges = size if size > 1 else 0
        
        print(f"\n[SCC กลุ่มที่ {idx_scc}]")
        print(f"  • รายชื่อเกาะในกลุ่ม: {scc}")
        print(f"  • จำนวนเกาะ (Size): {size}")
        print(f"  • จำนวนถนนจริงภายในกลุ่ม: {actual_edges} เส้น")
        print(f"  • จำนวนถนนน้อยที่สุดในทฤษฎี: {min_required_edges} เส้น")

        # คัดเลือก SCC ที่ใหญ่สุด (ถ้าขนาดเท่ากันเลือกตัวที่มีถนนน้อยที่สุด)
        if (size > best_size) or (size == best_size and actual_edges < best_edges):
            best_size = size
            best_edges = actual_edges
            best_scc = scc

    # -------------------------------------------------------------
    # ส่วนที่ 2: แสดงผล SCC ที่ใหญ่ที่สุดที่มีจำนวนถนนน้อยที่สุด
    # -------------------------------------------------------------
    print("\n==================================================")
    print("   สรุป: SCC ที่ใหญ่ที่สุดที่มีจำนวนถนนน้อยที่สุด")
    print("==================================================")
    if best_scc:
        min_req = best_size if best_size > 1 else 0
        print(f"  • รายชื่อเกาะในกลุ่ม: {best_scc}")
        print(f"  • จำนวนเกาะสูงสุด (Size): {best_size}")
        print(f"  • จำนวนถนนจริงภายในกลุ่ม: {best_edges} เส้น")
        print(f"  • จำนวนถนนน้อยที่สุดในทฤษฎี: {min_req} เส้น")

    # -------------------------------------------------------------
    # ส่วนที่ 3: การหาถนนเพิ่มเพื่อรวมทุก Component เป็นหนึ่งเดียวกัน
    # -------------------------------------------------------------
    print("\n==================================================")
    print("   การรวมทุก Component เป็นหนึ่งเดียวกัน (ขั้นต่ำที่สุด)")
    print("==================================================")
    
    if num_sccs <= 1:
        print("• กราฟนี้เป็น Component เดียวกันทั้งหมดอยู่แล้ว (ต้องสร้างเพิ่ม 0 เส้น)")
    else:
        # แมปว่าแต่ละเกาะอยู่ SCC หมายเลขใด
        scc_id = {}
        for idx_scc, scc in enumerate(all_sccs):
            for node in scc:
                scc_id[node] = idx_scc

        # คำนวณ In-Degree และ Out-Degree ของแต่ละ SCC
        in_degree = [0] * num_sccs
        out_degree = [0] * num_sccs

        for u in range(1, n + 1):
            for v in adj[u]:
                if scc_id[u] != scc_id[v]:
                    out_degree[scc_id[u]] += 1
                    in_degree[scc_id[v]] += 1

        zero_in_sccs = [i for i in range(num_sccs) if in_degree[i] == 0]
        zero_out_sccs = [i for i in range(num_sccs) if out_degree[i] == 0]

        # ถนนขั้นต่ำที่ต้องสร้างเพิ่ม = max(กลุ่มที่ไม่มีทางเข้า, กลุ่มที่ไม่มีทางออก)
        min_edges_needed = max(len(zero_in_sccs), len(zero_out_sccs))

        print(f"  • จำนวนถนนขั้นต่ำสุดที่ต้องสร้างเพิ่มจริง: {min_edges_needed} เส้น")
        print("  • รายการถนนที่แนะนำให้สร้างเพิ่ม:")
        
        for k in range(min_edges_needed):
            src_scc = zero_out_sccs[k % len(zero_out_sccs)]
            target_scc = zero_in_sccs[k % len(zero_in_sccs)]
            
            u = all_sccs[src_scc][0]      # ตัวแทนเกาะจาก SCC ปลายทาง
            v = all_sccs[target_scc][0]   # ตัวแทนเกาะจาก SCC ต้นทาง
            print(f"    - สร้างถนนจากเกาะ {u} (SCC {src_scc+1}) -> เกาะ {v} (SCC {target_scc+1})")

if __name__ == '__main__':
    solve()