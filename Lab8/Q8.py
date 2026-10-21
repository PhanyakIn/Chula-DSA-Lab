import os
import sys
import time

# ขยายขีดจำกัด Recursion สำหรับข้อมูลขนาดใหญ่
sys.setrecursionlimit(200000)


def max_profit_divide_and_conquer(prices, left, right):

    # Base Case: วันเดียว ไม่สามารถซื้อและขายคนละวันได้
    if left == right:
        return 0.0, left, left, left, left

    mid = (left + right) // 2

    # 1. หาคำตอบจากฝั่งซ้ายอย่างเดียว
    l_profit, l_buy, l_sell, l_min_idx, l_max_idx = (
        max_profit_divide_and_conquer(prices, left, mid)
    )

    # 2. หาคำตอบจากฝั่งขวาอย่างเดียว
    r_profit, r_buy, r_sell, r_min_idx, r_max_idx = (
        max_profit_divide_and_conquer(prices, mid + 1, right)
    )

    # 3. หาคำตอบกรณี ซื้อฝั่งซ้าย (ราคาต่ำสุด) และ ขายฝั่งขวา (ราคาสูงสุด)
    cross_buy = l_min_idx
    cross_sell = r_max_idx
    cross_profit = prices[cross_sell] - prices[cross_buy]

    # --- แก้ไขจุดนี้: หา min_idx และ max_idx ของช่วง [left, right] ที่ถูกต้อง ---
    if prices[l_min_idx] <= prices[r_min_idx]:
        current_min_idx = l_min_idx
    else:
        current_min_idx = r_min_idx

    if prices[l_max_idx] >= prices[r_max_idx]:
        current_max_idx = l_max_idx
    else:
        current_max_idx = r_max_idx

    # เปรียบเทียบเลือกผลตอบแทน (กำไร) ที่มากที่สุด
    best_profit = l_profit
    best_buy = l_buy
    best_sell = l_sell
    
    if r_profit > best_profit:
        best_profit = r_profit
        best_buy = r_buy
        best_sell = r_sell
        
    if cross_profit > best_profit:
        best_profit = cross_profit
        best_buy = cross_buy
        best_sell = cross_sell

    return best_profit, best_buy, best_sell, current_min_idx, current_max_idx


def main():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "testcase.txt"
    )
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            input_data = file.read().split()
    except FileNotFoundError:
        print(
            f"Error: หาไฟล์ '{file_path}' ไม่เจอ โปรดตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์ Lab8"
        )
        return

    if not input_data:
        return

    n = int(input_data[0])
    prices = [float(x) for x in input_data[1 : n + 1]]

    if n < 2:
        return

    # เริ่มจับเวลา
    start_time = time.perf_counter()

    # เรียกใช้ Divide and Conquer
    profit, buy_idx, sell_idx, _, _ = max_profit_divide_and_conquer(
        prices, 0, n - 1
    )

    # สิ้นสุดการจับเวลา
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

    buy_day = buy_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)[cite: 1]
    sell_day = sell_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)[cite: 1]
    buy_price = prices[buy_idx]
    sell_price = prices[sell_idx]
    days_held = sell_day - buy_day  # จำนวนวันที่ถือครอง[cite: 1]

    min_possible_profit = float("inf")
    worst_buy_idx = 0
    worst_sell_idx = 0

    if n >= 2:
        for buy in range(n):
            for sell in range(buy + 1, n):
                profit_val = prices[sell] - prices[buy]
                if profit_val < min_possible_profit:
                    min_possible_profit = profit_val
                    worst_buy_idx = buy
                    worst_sell_idx = sell
    else:
        min_possible_profit = 0.0

    worst_buy_day = worst_buy_idx + 1
    worst_sell_day = worst_sell_idx + 1

    # แสดงผลตามรูปแบบโจทย์ + เพิ่มกำไรต่ำสุด
    print(f"วันที่ควรซื้อคือ : {buy_day}")
    print(f"ราคาซื้อคือ : {buy_price:.2f}")
    print(f"วันที่ควรขายคือ : {sell_day}")
    print(f"ราคาขายคือ : {sell_price:.2f}")
    print(f"กำไรสูงสุดคือ : {profit:.2f}")
    print(f"กำไรต่ำสุดคือ (ขาดทุนสูงสุด) : {min_possible_profit:.2f}")
    print(f"ถือเงินไว้นาน : {days_held}")
    print(f"Run Time (Divide & Conquer): {execution_time_ms:.4f} ms")

    print(worst_buy_day)
    print(worst_sell_day)


if __name__ == "__main__":
    main()