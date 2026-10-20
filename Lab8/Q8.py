import os


def max_profit_divide_and_conquer(prices, left, right):

    # Base Case: วันเดียว ไม่สามารถซื้อและขายคนละวันได้
    if left == right:
        # ส่งค่ากลับ: (profit, buy_idx, sell_idx, min_idx_in_range, max_idx_in_range)
        return float("-inf"), -1, -1, left, right

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
    # หา index ของราคาน้อยที่สุดในฝั่งซ้าย
    cross_buy = l_min_idx
    # หา index ของราคามากที่สุดในฝั่งขวา
    cross_sell = r_max_idx
    cross_profit = prices[cross_sell] - prices[cross_buy]

    # คำนวณ min_idx และ max_idx ของช่วง [left, right] เพื่อส่งต่อขึ้นไป
    current_min_idx = (
        l_min_idx if prices[l_min_idx] <= prices[r_min_idx] else r_min_idx
    )
    current_max_idx = (
        r_max_idx if prices[r_max_idx] >= prices[l_max_idx] else l_max_idx
    )

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
    # เปิดอ่านไฟล์ testcase.txt ในโฟลเดอร์เดียวกับสคริปต์ (ไม่ต้องพิมพ์ผ่าน Terminal)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            input_data = file.read().split()
    except FileNotFoundError:
        print(f"Error: หาไฟล์ '{file_path}' ไม่เจอ โปรดตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์ Lab8")
        return

    # อ่านข้อมูลทั้งหมดเข้ามารวดเดียว รองรับ N ขนาดใหญ่ได้สบาย
    if not input_data:
        return

    n = int(input_data[0])
    prices = [float(x) for x in input_data[1 : n + 1]]

    if n < 2:
        return

    # เรียกใช้ Divide and Conquer
    profit, buy_idx, sell_idx, _, _ = max_profit_divide_and_conquer(
        prices, 0, n - 1
    )

    buy_day = buy_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)
    sell_day = sell_idx + 1  # เปลี่ยน index เป็นวันที่ (1-based)
    buy_price = prices[buy_idx]
    sell_price = prices[sell_idx]
    days_held = sell_day - buy_day  # จำนวนวันที่ถือครอง

    # แสดงผลตามรูปแบบโจทย์
    print(buy_day)
    print(f"{buy_price:.2f}")
    print(sell_day)
    print(f"{sell_price:.2f}")
    print(f"{profit:.2f}")
    print(days_held)


if __name__ == "__main__":
    main()