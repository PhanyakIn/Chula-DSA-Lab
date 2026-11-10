import sys
import os

# เพิ่มขีดจำกัดของ recursion เพื่อรองรับกราฟที่มีขนาดใหญ่หรือลึกมาก
sys.setrecursionlimit(200000)

# หา path ของ testcase.txt โดยยึดตำแหน่งของไฟล์นี้เป็นหลัก (รันจากที่ไหนก็ได้)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTCASE_PATH = os.path.join(SCRIPT_DIR, 'testcase.txt')

def solve():
    # 1. อ่านข้อมูลจากไฟล์ testcase.txt
    try:
        with open(TESTCASE_PATH, 'r') as f:
            input_data = f.read().split()
    except FileNotFoundError:
        print("ไม่พบไฟล์ testcase.txt ที่อยู่ข้างสคริปต์นี้")
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
        order.append(u)  # เก็บโหนดตามลำดับที่ทำงานเสร็จ
        
    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)
            
    # -------------------------------------------------------------
    # ขั้นตอนที่ 2: DFS บนกราฟกลับทิศทาง เพื่อดึงสมาชิก SCC แต่ละกลุ่ม
    # -------------------------------------------------------------
    visited = [False] * (n + 1)
    
    def dfs2(u, component):
        visited[u] = True
        component.append(u)  # สะสมรายชื่อเกาะใน SCC กลุ่มปัจจุบัน
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

    # -------------------------------------------------------------
    # ส่วนที่ 1: แสดงผล SCC ทุกกลุ่มที่พบ (ทุกรูปแบบทางผ่าน)
    # -------------------------------------------------------------
    print(f"==================================================")
    print(f"           พบ SCC ทั้งหมด {len(all_sccs)} กลุ่ม")
    print(f"==================================================")
    
    best_scc = None
    best_size = -1
    best_edges = float('inf')

    for idx_scc, scc in enumerate(all_sccs, 1):
        scc_set = set(scc)  # แปลงเป็น set เพื่อให้ตรวจสอบรวดเร็ว
        size = len(scc)
        
        # นับจำนวนถนน (Edge) จริงที่มีอยู่ภายใน SCC นี้
        actual_edges = 0
        for u in scc:
            for v in adj[u]:
                if v in scc_set:  # นับเฉพาะถนนที่ปลายทางยังอยู่ใน SCC เดียวกัน
                    actual_edges += 1

        min_required_edges = size if size > 1 else 0
        
        print(f"\n[SCC กลุ่มที่ {idx_scc}]")
        print(f"  • รายชื่อเกาะในกลุ่ม: {scc}")
        print(f"  • จำนวนเกาะ (Size): {size}")
        print(f"  • จำนวนถนนจริงภายในกลุ่ม: {actual_edges} เส้น")
        print(f"  • จำนวนถนนน้อยที่สุดในทฤษฎี: {min_required_edges} เส้น")

        # คัดเลือกตัวที่ดีที่สุด (ขนาดใหญ่สุด -> ถ้านเท่ากันเอาถนนน้อยสุด)
        if (size > best_size) or (size == best_size and actual_edges < best_edges):
            best_size = size
            best_edges = actual_edges
            best_scc = scc

    # -------------------------------------------------------------
    # ส่วนที่ 2: สรุปเฉพาะ SCC ที่ใหญ่ที่สุดและมีถนนน้อยที่สุด
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

if __name__ == '__main__':
    solve()