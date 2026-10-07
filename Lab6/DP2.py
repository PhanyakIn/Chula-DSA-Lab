# ==============================================================================
# 2. Minimum Coin Change Problem & 2D Lookup Table
# ==============================================================================
INF = float('inf')
def min_coin_change_dp_all_solutions(file_path, max_table_amount=50, show_table=False):
    """
    1. คำนวณจำนวนเหรียญขั้นต่ำด้วย 2D DP Table
    2. Backtrack หา Optimal Solutions ทั้งหมด
    3. แสดง 2D Lookup Table (พร้อมระบบซ่อนคอลัมน์หาก amount มีขนาดใหญ่เกินไป)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        amount = int(lines[0])
        coins = list(map(int, lines[1].split()))
        n = len(coins)
    except Exception as e:
        print(f" Error reading file {file_path}: {e}")
        return INF, [], []

    # 2.1 สร้างและเติมตาราง 2D DP Table
    dp = [[INF] * (amount + 1) for _ in range(n + 1)]
    
    # Base Case: จำนวนเงิน 0 บาท ใช้ 0 เหรียญ
    for i in range(n + 1):
        dp[i][0] = 0
        
    # Bottom-Up Dynamic Programming
    for i in range(1, n + 1):
        coin = coins[i - 1]
        for j in range(1, amount + 1):
            dp[i][j] = dp[i - 1][j]  # กรณีไม่เลือกใช้เหรียญนี้
            if j >= coin and dp[i][j - coin] != INF:
                dp[i][j] = min(dp[i][j], 1 + dp[i][j - coin])
                
    min_coins = dp[n][amount]
    
    # 2.2 Backtrack หาคำตอบที่ดีที่สุดทุกรูปแบบ
    all_optimal_solutions = []
    
    def backtrack(curr_i, curr_j, current_path):
        if curr_j == 0:
            all_optimal_solutions.append(list(current_path))
            return
        if curr_i == 0:
            return
        
        coin_val = coins[curr_i - 1]
        
        # ทางเลือก 1: ไม่ใช้เหรียญปัจจุบัน (ถ้าค่าใน DP Table เท่ากัน)
        if dp[curr_i][curr_j] == dp[curr_i - 1][curr_j]:
            backtrack(curr_i - 1, curr_j, current_path)
            
        # ทางเลือก 2: เลือกใช้เหรียญปัจจุบัน (ถ้าตรงตามสมการสถานะ optimal)
        if curr_j >= coin_val and dp[curr_i][curr_j] == 1 + dp[curr_i][curr_j - coin_val]:
            current_path.append(coin_val)
            backtrack(curr_i, curr_j - coin_val, current_path)
            current_path.pop()  # Backtrack

    if min_coins != INF:
        backtrack(n, amount, [])

    # 2.3 แสดงผลลัพธ์ Minimum Coins & Optimal Solutions
    print("=" * 65)
    print("=== 2. Minimum Coin Change Problem (DP - All Solutions) ===")
    print("=" * 65)
    print(f"File: {file_path}")
    print(f"Amount = {amount}")
    print(f"Coins = {coins}")
    
    if min_coins != INF:
        print(f"Minimum number of coins = {min_coins}")
        print(f"Total Optimal Solutions = {len(all_optimal_solutions)}")
        print("All Optimal Coin Selections:")
        for idx, sol in enumerate(all_optimal_solutions, 1):
            print(f"  วิธีที่ {idx}: {sol}")
    else:
        print("Minimum number of coins = Impossible")
        print("Optimal Coin Selection = None")
    
    # 2.4 แสดง 2D Lookup Table (พร้อมระบบป้องกันข้อความยาวเกินหน้าจอ)
    print("\n2-Dimensional Lookup Table:")
    if show_table:
        print("\n2-Dimensional Lookup Table:")
        
        if amount > max_table_amount:
            print(f" Notice: ตารางขนาดใหญ่เกินไป (Amount = {amount})")
            print(f"แสดงเฉพาะช่วง Amount [0 .. {max_table_amount}] เพื่อความสวยงามในการแสดงผล\n")
            display_amount = max_table_amount
        else:
            display_amount = amount

        header = f"{'Coin \\ Amount':<15}" + "".join([f"{j:>5}" for j in range(display_amount + 1)])
        print(header)
        print("-" * len(header))
        
        labels = ["Base (0)"] + [f"Coin ({c})" for c in coins]
        for i in range(n + 1):
            row_str = f"{labels[i]:<15}"
            for j in range(display_amount + 1):
                val = dp[i][j]
                val_str = "INF" if val == INF else str(val)
                row_str += f"{val_str:>5}"
            print(row_str)
        print()
    
    return min_coins, all_optimal_solutions, dp


# ==============================================================================
# Main Execution
# ==============================================================================
if __name__ == "__main__":
    # สามารถปรับเปลี่ยนไฟล์ Path ตามต้องการ
    file_name = "Lab6/testcase.txt"
    
    # 2. รันส่วน Min Coin Change DP + Table
    min_coin_change_dp_all_solutions(file_name)