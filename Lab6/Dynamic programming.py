import sys

# ปรับ Recursion limit เผื่อกรณี amount มีขนาดใหญ่
sys.setrecursionlimit(20000)

INF = float('inf')


# ==============================================================================
# 1. Coin Change Problem: Count & Print All Ways
# ==============================================================================

def coin_change_all_ways_from_file(file_path, max_print_limit=100):
    """
    ใช้ Backtracking หา Combinations ทั้งหมดเพียงอย่างเดียว (ไม่ใช้ DP)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 2:
            raise ValueError("รูปแบบไฟล์ไม่ถูกต้อง (ต้องมีอย่างน้อย 2 บรรทัด)")

        amount = int(lines[0])
        coins = list(map(int, lines[1].split()))
    except Exception as e:
        print(f" Error reading file {file_path}: {e}")
        return 0, []

    all_ways = []
    
    # Backtracking หาคำตอบทุกรูปแบบ
    def find_ways(coin_idx, current_amount, current_combination):
        # Safety limit: หยุดถ้าเก็บคำตอบครบตาม limit ที่ตั้งไว้
        if max_print_limit is not None and len(all_ways) >= max_print_limit:
            return
            
        if current_amount == 0:
            all_ways.append(list(current_combination))
            return
        if coin_idx < 0 or current_amount < 0:
            return
        
        # กรณีที่ 1: ไม่เลือกใช้เหรียญที่ coins[coin_idx]
        find_ways(coin_idx - 1, current_amount, current_combination)
        
        # กรณีที่ 2: เลือกใช้เหรียญที่ coins[coin_idx]
        if current_amount >= coins[coin_idx]:
            current_combination.append(coins[coin_idx])
            find_ways(coin_idx, current_amount - coins[coin_idx], current_combination)
            current_combination.pop()  # Backtrack

    find_ways(len(coins) - 1, amount, [])

    # แสดงผลลัพธ์
    print("=" * 65)
    print("=== 1. Coin Change Problem (Print All Ways) ===")
    print("=" * 65)
    print(f"File: {file_path}")
    print(f"Amount = {amount}")
    print(f"Coins = {coins}")
    
    if max_print_limit is not None and len(all_ways) >= max_print_limit:
        print(f"Found ways (Limited) = {len(all_ways)} (Reached max limit: {max_print_limit})")
        print(f"\n Warning: หยุดการค้นหาเมื่อครบ {max_print_limit} รายการแรกเพื่อป้องกันหน่วยความจำเต็ม\n")
    else:
        print(f"Ways to make change = {len(all_ways)}")
        print("\nAll combinations:")

    for way in all_ways:
        print(" ", way)
    print()
    
    return len(all_ways), all_ways

# ==============================================================================
# Main Execution
# ==============================================================================
if __name__ == "__main__":
    # สามารถปรับเปลี่ยนไฟล์ Path ตามต้องการ
    file_name = "Lab6/testcase.txt"
    
    # 1. รันส่วน Print All Ways
    coin_change_all_ways_from_file(file_name)
    