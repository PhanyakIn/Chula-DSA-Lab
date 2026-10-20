import os
import time


def max_profit_brute_force(prices, n):
    best_profit = float("-inf")
    best_buy = -1
    best_sell = -1

    # วนลูปจับคู่ทุกวันซื้อ (i) และทุกวันขาย (j) โดยที่ j > i
    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            # หากพบกำไรที่มากกว่าค่าสูงสุดเดิม ให้บันทึกค่าใหม่
            if profit > best_profit:
                best_profit = profit
                best_buy = i
                best_sell = j

    return best_profit, best_buy, best_sell


def main():
    # เปิดอ่านไฟล์ testcase.txt ในโฟลเดอร์เดียวกับสคริปต์
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

    # เรียกใช้วิธี Brute force
    start_time = time.perf_counter()
    profit, buy_idx, sell_idx = max_profit_brute_force(prices, n)
    end_time = time.perf_counter()
    runtime = end_time - start_time

    buy_day = buy_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)
    sell_day = sell_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)[cite: 1]
    buy_price = prices[buy_idx]
    sell_price = prices[sell_idx]
    days_held = sell_day - buy_day  # จำนวนวันที่ถือครอง[cite: 1]

    # แสดงผลตามรูปแบบโจทย์[cite: 1]
    print(f"วันที่ควรซื้อคือ : {buy_day}")
    print(f"ราคาซื้อคือ : {buy_price:.2f}")
    print(f"วันที่ควรขายคือ : {sell_day}")
    print(f"ราคาขายคือ : {sell_price:.2f}")
    print(f"กำไรสูงสุดคือ : {profit:.2f}")
    print(f"ถือเงินไว้นาน : {days_held}")
    print(f"Runtime : {runtime:.6f} วินาที")



if __name__ == "__main__":
    main()