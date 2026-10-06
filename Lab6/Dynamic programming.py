# 1. Coin Change Problem: Print all ways and count --------------------------
def coin_change_all_ways_from_file(file_path):
    # อ่านข้อมูลจากไฟล์ txt
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    amount = int(lines[0])
    coins = list(map(int, lines[1].split()))
    all_ways = []
    
    # Backtracking หาคำตอบทุกรูปแบบ
    def find_ways(coin_idx, current_amount, current_combination):
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
    print("=== 1. Coin Change Problem (Print All Ways) ===")
    print(f"File: {file_path}")
    print(f"Amount = {amount}")
    print(f"Coins = {coins}")
    print(f"Ways to make change = {len(all_ways)}")
    print("All combinations:")
    for way in all_ways:
        print(" ", way)
    print()
    
    return len(all_ways), all_ways


# 2. Minimum Coin Change Problem & 2D Lookup Table ----------------------------
def min_coin_change_dp_all_solutions(file_path):
    # 1. อ่านข้อมูลจากไฟล์ txt
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    amount = int(lines[0])
    coins = list(map(int, lines[1].split()))
    n = len(coins)
    INF = float('inf')
    
    # 2. สร้างและเติมตาราง 2D DP Table
    # ขนาดตาราง (n + 1) x (amount + 1)
    dp = [[INF] * (amount + 1) for _ in range(n + 1)]
    
    # Base Case: จำนวนเงิน 0 บาท ใช้ 0 เหรียญเสมอ
    for i in range(n + 1):
        dp[i][0] = 0
        
    # เติมตารางแบบ Bottom-Up
    for i in range(1, n + 1):
        coin = coins[i - 1]
        for j in range(1, amount + 1):
            dp[i][j] = dp[i - 1][j]  # กรณีไม่เลือกใช้เหรียญนี้
            if j >= coin and dp[i][j - coin] != INF:
                # เลือกค่าขั้นต่ำระหว่างไม่ใช้ กับ เลือกใช้เหรียญนี้
                dp[i][j] = min(dp[i][j], 1 + dp[i][j - coin])
                
    min_coins = dp[n][amount]
    
    # 3. ฟังก์ชัน Recursion สำหรับ Backtrack หาคำตอบที่ดีที่สุด "ทุกวิธี"
    all_optimal_solutions = []
    
    def backtrack(curr_i, curr_j, current_path):
        # Base Case: ทอนเงินครบ 0 บาทแล้ว
        if curr_j == 0:
            all_optimal_solutions.append(list(current_path))
            return
        # ติดขอบตาราง
        if curr_i == 0:
            return
        
        coin_val = coins[curr_i - 1]
        
        # ทางเลือกที่ 1: ขยับขึ้นบรรทัดบน (ถ้าค่าเท่ากัน แปลว่าไม่ใช้เหรียญนี้ก็ได้คำตอบที่ดีที่สุดเท่ากัน)
        if dp[curr_i][curr_j] == dp[curr_i - 1][curr_j]:
            backtrack(curr_i - 1, curr_j, current_path)
            
        # ทางเลือกที่ 2: เลือกใช้เหรียญนี้ (ถ้าค่าสอดคล้องกับ 1 + dp[curr_i][curr_j - coin])
        if curr_j >= coin_val and dp[curr_i][curr_j] == 1 + dp[curr_i][curr_j - coin_val]:
            current_path.append(coin_val)
            backtrack(curr_i, curr_j - coin_val, current_path)
            current_path.pop()  # Backtrack ลบเหรียญออกเพื่อลองทางเลือกอื่น

    # เรียกใช้งาน Backtrack หากมีคำตอบที่ทอนได้
    if min_coins != INF:
        backtrack(n, amount, [])

    # 4. แสดงผลลัพธ์
    print("=== Minimum Coin Change Problem (DP - All Solutions) ===")
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
    
    # 5. แสดง 2D Lookup Table
    print("\n2-Dimensional Lookup Table:")
    header = f"{'Coin \\ Amount':<15}" + "".join([f"{j:>5}" for j in range(amount + 1)])
    print(header)
    print("-" * len(header))
    
    labels = ["Base (0)"] + [f"Coin ({c})" for c in coins]
    for i in range(n + 1):
        row_str = f"{labels[i]:<15}"
        for j in range(amount + 1):
            val = dp[i][j]
            val_str = "INF" if val == INF else str(val)
            row_str += f"{val_str:>5}"
        print(row_str)
    print()
    
    return min_coins, all_optimal_solutions, dp

if __name__ == "__main__":
    file_name = "Lab6/testcase.txt"

    # 6.1
    coin_change_all_ways_from_file(file_name)
    # 6.2
    min_coin_change_dp_all_solutions(file_name)