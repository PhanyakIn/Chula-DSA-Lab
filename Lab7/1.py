import math

# ==========================================
# ส่วนที่ 1: ฟังก์ชันคณิตศาสตร์พื้นฐาน
# ==========================================

# 1. ฟังก์ชันคำนวณระยะห่างระหว่างจุด 2 จุด
def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 2. ฟังก์ชันคำนวณความยาวเส้นรอบรูปของรูปสามเหลี่ยม
def get_perimeter(p1, p2, p3):
    return get_distance(p1, p2) + get_distance(p2, p3) + get_distance(p3, p1)

def print_dp_table(dp, n):
    """
    ฟังก์ชันสำหรับแสดงตาราง 2D DP ของ Polygon Triangulation
    """
    print("\n" + "=" * 60)
    print("=== 2D Dynamic Programming Table (dp[i][j]) ===")
    print("=" * 60)
    
    # สร้างหัวตารางแสดง Index ของคอลัมน์ j
    header = f"{'i \\ j':<6}" + "".join([f"{j:>9}" for j in range(n)])
    print(header)
    print("-" * len(header))
    
    # วนลูปพิมพ์แต่ละแถว i
    for i in range(n):
        row_str = f"{i:<6}"
        for j in range(n):
            val = dp[i][j]
            if val == float('inf'):
                val_str = "INF"
            elif val == 0.0:
                val_str = "0.0"
            else:
                val_str = f"{val:.1f}"  # จัดรูปแบบทศนิยม 1 ตำแหน่งให้อ่านง่ายในตาราง
            row_str += f"{val_str:>9}"
        print(row_str)
    print("=" * 60)

# ==========================================
# ส่วนที่ 2: โปรแกรมหลัก (Dynamic Programming)
# ==========================================

def main():
    # 3. เปิดอ่านไฟล์ 1.1.txt โดยตรง (ไม่ต้องพิมพ์ผ่าน Terminal แล้ว)
    try:
        with open("Lab7/testcase.txt", "r") as file:
            data = file.read().split()
    except FileNotFoundError:
        print("Error: หาไฟล์ 'testcase.txt' ไม่เจอ โปรดตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์เดียวกัน")
        return

    # 4. แปลงข้อมูลที่อ่านมาเก็บลงในตัวแปร
    n = int(data[0]) # บรรทัดแรกคือจำนวนจุด
    points = []      # ลิสต์สำหรับเก็บพิกัด (x, y)
    
    idx = 1
    for _ in range(n):
        x = float(data[idx])
        y = float(data[idx+1])
        points.append((x, y))
        idx += 2

    # ==========================================
    # เพิ่มส่วนนี้: เรียงลำดับจุดตามมุม Polar Angle รอบจุดศูนย์กลาง
    # ==========================================
    # 4.1 หาจุดศูนย์กลาง (Centroid) ของจุดทั้งหมด
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n

    # 4.2 เรียงลำดับจุดตามมุม (math.atan2) ทวนเข็มนาฬิกา
    points.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

    
    # 5. สร้างตาราง DP ขนาด n x n (ใส่ค่าเริ่มต้นเป็น 0.0)
    # dp[i][j] คือตัวแปรที่จะจดจำว่า "ชิ้นส่วนจากจุด i ถึง j มีต้นทุนการตัดต่ำสุดเท่าไหร่"
    dp = [[0.0 for _ in range(n)] for _ in range(n)]

    # 6. เริ่มกระบวนการคิดแบบ Dynamic Programming
    for gap in range(2, n):             # ลองขยายขนาดชิ้นส่วนทีละนิด
        for i in range(n - gap):
            j = i + gap
            dp[i][j] = float('inf')     # ตั้งค่าเริ่มต้นของชิ้นส่วนนี้ให้เยอะๆ (อนันต์) ไว้ก่อน
            
            # 7. สุ่มเลือกจุด k ที่อยู่ตรงกลางระหว่าง i กับ j เพื่อสร้างเป็นสามเหลี่ยม
            for k in range(i + 1, j):
                # ต้นทุน = (ต้นทุนชิ้นซ้าย) + (ต้นทุนชิ้นขวา) + (เส้นรอบรูปสามเหลี่ยมที่เพิ่งสร้าง)
                current_cost = dp[i][k] + dp[k][j] + get_perimeter(points[i], points[k], points[j])
                
                # ถ้าวิธีตัดแบบใหม่ (current_cost) ได้ค่าน้อยกว่าที่เคยจดไว้ ให้จำค่าใหม่แทน
                if current_cost < dp[i][j]:
                    dp[i][j] = current_cost

    # 8. แสดงผลลัพธ์คำตอบสุดท้ายที่ทศนิยม 4 ตำแหน่ง
    print()
    print(f"Answer = {dp[0][n-1]:.4f}")
    print()
    print_dp_table(dp, n)
# สั่งให้โปรแกรมเริ่มทำงาน
if __name__ == "__main__":
    main()