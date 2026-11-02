import sys

# เพิ่มขีดจำกัดของ recursion เพื่อรองรับกราฟที่มีขนาดใหญ่หรือลึกมาก
sys.setrecursionlimit(200000)

def solve():
    # อ่านข้อมูลจากไฟล์ testcase.txt
    try:
        with open('Lab9/testcase.txt', 'r') as f:
            input_data = f.read().split()
    except FileNotFoundError:
        print("ไม่พบไฟล์ testcase.txt")
        return
        
    if not input_data:
        return
        
    n = int(input_data[0]) # จำนวนเกาะ[cite: 72]
    m = int(input_data[1]) # จำนวนถนน[cite: 72]
    
    # สร้าง Adjacency List สำหรับกราฟปกติและกราฟกลับทิศทาง
    adj = [[] for _ in range(n + 1)]
    rev_adj = [[] for _ in range(n + 1)]
    
    # อ่านข้อมูลถนนเชื่อมต่อแบบทิศทางเดียว[cite: 72]
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        rev_adj[v].append(u)
        idx += 2
        
    visited = [False] * (n + 1)
    order = []
    
    # ขั้นตอนที่ 1: DFS เพื่อหาลำดับการทำงาน (Finishing time)
    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)
        
    # รัน DFS รอบแรกสำหรับทุกๆ โหนดที่ยังไม่ได้เยี่ยมชม
    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)
            
    # รีเซ็ตค่าสถานะการเยี่ยมชมสำหรับ DFS รอบที่ 2
    visited = [False] * (n + 1)
    
    # ขั้นตอนที่ 2: DFS บนกราฟกลับทิศทางเพื่อหาขนาดของ SCC
    def dfs2(u):
        count = 1
        visited[u] = True
        for v in rev_adj[u]:
            if not visited[v]:
                count += dfs2(v)
        return count
        
    max_scc_size = 0
    
    # รัน DFS รอบสองตามลำดับย้อนหลังของ order
    for i in range(n - 1, -1, -1):
        u = order[i]
        if not visited[u]:
            # นับจำนวนเกาะใน SCC กลุ่มนี้และอัปเดตค่าสูงสุด[cite: 72]
            current_scc_size = dfs2(u)
            if current_scc_size > max_scc_size:
                max_scc_size = current_scc_size
                
    # พิมพ์คำตอบ
<<<<<<< Updated upstream
    print("จำนวนเกาะสูงสุดที่เดินทางผ่านได้ :", max_scc_size)
=======
    print("จำนวนเกาะสูงสุดที่เดินทางผ่านได้:", max_scc_size)
>>>>>>> Stashed changes

if __name__ == '__main__':
    solve()
