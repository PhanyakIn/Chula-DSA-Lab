ops = 0

def FindGCD3_pair(m, n):
    global ops
    ops += 1  

    # Base Case
    if m == n:
        return m

    # กรณี m > n
    elif m > n:
        rem = m % n
        if rem == 0:
            return n
        return FindGCD3_pair(rem, n)

    # กรณี m < n
    else:
        rem = n % m
        if rem == 0:
            return m
        return FindGCD3_pair(m, rem)

def FindGCD3(*numbers):
    global ops
    if not numbers:
        return None
    
    # ดึงตัวแรกมาเป็น GCD ตั้งต้น
    current_gcd = numbers[0]
    
    # นำไปหา GCD ร่วมกับตัวถัดๆ ไปทีละตัว
    for num in numbers[1:]:
        current_gcd = FindGCD3_pair(current_gcd, num)

    print(f"gcd{numbers} = {current_gcd}")
    print("รอบทั้งหมดของ GCD3 (Euclidean) :", ops)
    return current_gcd

def main():
    # เรียกใช้งานด้วยตัวเลขกี่ตัวก็ได้
    FindGCD3(189, 252, 1197, 292005)
    print("----------------------------------------------")

main()