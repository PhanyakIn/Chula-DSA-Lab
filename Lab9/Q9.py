import sys
import os

sys.setrecursionlimit(200000)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTCASE_PATH = os.path.join(SCRIPT_DIR, 'testcase.txt')

def solve():
    try:
        with open(TESTCASE_PATH, 'r') as f:
            input_data = f.read().split()
    except FileNotFoundError:
        print("ไม่พบไฟล์ testcase.txt")
        return
        
    if not input_data:
        return
        
    n = int(input_data[0])
    m = int(input_data[1])
    
    adj = [[] for _ in range(n + 1)]
    rev_adj = [[] for _ in range(n + 1)]
    edges = []
    
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        rev_adj[v].append(u)
        edges.append((u, v))
        idx += 2
        
    # -------------------------------------------------------------
    # Step 1: Kosaraju's Algorithm หา SCC ทั้งหมด
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
            
    visited = [False] * (n + 1)
    
    def dfs2(u, component):
        visited[u] = True
        component.append(u)
        for v in rev_adj[u]:
            if not visited[v]:
                dfs2(v, component)

    all_sccs = []
    for i in range(n - 1, -1, -1):
        u = order[i]
        if not visited[u]:
            component = []
            dfs2(u, component)
            all_sccs.append(component)

    num_sccs = len(all_sccs)
    print("==================================================")
    print(f"           พบ SCC ทั้งหมด {num_sccs} กลุ่ม")
    print("==================================================")

    # หากราฟเดิมเป็น 1 SCC อยู่แล้ว ไม่ต้องเพิ่มถนน
    if num_sccs == 1:
        print("\nกราฟนี้เป็น Strongly Connected Component เดียวกันทั้งหมดอยู่แล้ว!")
        print("จำนวนถนนที่ต้องสร้างเพิ่ม: 0 เส้น")
        return

    # -------------------------------------------------------------
    # Step 2: สร้าง Condensed Graph และหา In-degree / Out-degree
    # -------------------------------------------------------------
    node_to_scc = {}
    for scc_idx, scc in enumerate(all_sccs, 1):
        for u in scc:
            node_to_scc[u] = scc_idx

    in_degree = [0] * (num_sccs + 1)
    out_degree = [0] * (num_sccs + 1)
    condensed_adj = [set() for _ in range(num_sccs + 1)]

    for u, v in edges:
        scc_u = node_to_scc[u]
        scc_v = node_to_scc[v]
        if scc_u != scc_v and scc_v not in condensed_adj[scc_u]:
            condensed_adj[scc_u].add(scc_v)
            out_degree[scc_u] += 1
            in_degree[scc_v] += 1

    # แยกแยะ Source SCCs และ Sink SCCs (เกาะปิด)
    sources = [i for i in range(1, num_sccs + 1) if in_degree[i] == 0]
    sinks = [i for i in range(1, num_sccs + 1) if out_degree[i] == 0]

    # -------------------------------------------------------------
    # Step 3: วิเคราะห์การต่อถนนเพิ่มน้อยที่สุดเพื่อสร้าง 1 Component ใหญ่
    # -------------------------------------------------------------
    min_edges_to_add = max(len(sources), len(sinks))
    print()
    print("   วิเคราะห์กลุ่มปิด (Sink SCCs) และกลุ่มต้นทาง (Source SCCs)")
    print(f"  • กลุ่มต้นทาง (Source SCCs - ไม่มีทางเข้า): {sources}")
    print(f"  • กลุ่มปิด/ปลายทาง (Sink SCCs - ไม่มีทางออก): {sinks}")
    
    print("\n--------------------------------------------------")
    print(f"  ★ จำนวนถนนที่น้อยที่สุดที่ต้องสร้างเพิ่ม: {min_edges_to_add} เส้น")
    print("--------------------------------------------------")

    print("\n[ข้อเสนอแนะเส้นทางถนนที่ควรสร้างเพิ่ม]:")
    # ตัวอย่างแนวทางสร้างถนนเชื่อมจากเกาะปิดไปหาเกาะต้นทางเพื่อจับลูป
    for k in range(min_edges_to_add):
        from_sink_scc = sinks[k % len(sinks)]
        to_source_scc = sources[k % len(sources)]
        
        # เลือกเกาะตัวแทน 1 เกาะจากกลุ่มปิด และ 1 เกาะจากกลุ่มต้นทาง
        from_node = all_sccs[from_sink_scc - 1][0]
        to_node = all_sccs[to_source_scc - 1][0]
        
        print(f"  เส้นที่ {k+1}: สร้างถนนจาก [เกาะ {from_node} (SCC_{from_sink_scc})] -> [เกาะ {to_node} (SCC_{to_source_scc})]")

if __name__ == '__main__':
    solve()