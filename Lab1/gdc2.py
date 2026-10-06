import math

ops = 0

def buildSPF(number):
    global ops
    spf = list(range(number + 1))                   # สร้างตารางตำแหน่งตามจำนวนที่รับมา

    for i in range(2, int(math.sqrt(number)) + 1):  # เริ่ม loop หาตัวประกอบเฉพาะ
        ops += 1
        if spf[i] == i:                             # ถ้ายังไม่ได้ถูกเปลี่ยน แปลว่าเป็นตัวเลขเฉพาะ (Prime)
            for j in range(i * i, number + 1, i):   # กวาดเปลี่ยนตำแหน่งที่เป็นพหุคูณของ i
                ops += 1
                if spf[j] == j:                     # บันทึกเฉพาะตัวหารเฉพาะที่น้อยที่สุด (SPF)
                    spf[j] = i
    return spf

def getFactor(number, spf):
    global ops
    factors = []

    while number > 1:
        ops += 1
        prime = spf[number]         # ดึงตัวหารเฉพาะที่น้อยที่สุดจากตาราง SPF
        factors.append(prime)
        number = number // prime    # หารเพื่อหาตัวถัดไป

    return factors

def FindGCD2(*numbers):
    global ops
    if not numbers:
        return None

    # 1. หาค่าสูงสุดเพื่อสร้างตาราง SPF ให้ครอบคลุมตัวเลขทุกตัว
    max_val = max(numbers)
    spf = buildSPF(max_val)

    # 2. หา Prime Factorization ของตัวเลขทุกตัวโดยใช้ SPF
    all_factors = []
    for num in numbers:
        factors = getFactor(num, spf)
        all_factors.append(factors)
        print(f"Find the prime factorization of {num} : {factors}")

    # 3. หาตัวประกอบเฉพาะร่วมของตัวเลขทั้งหมด
    common = []
    first_num_factors = all_factors[0].copy()

    for item in first_num_factors:
        ops += 1
        is_common = True
        
        # ตรวจสอบว่า item นี้มีอยู่ในชุดตัวประกอบของตัวเลขตัวอื่นทุกตัวหรือไม่
        for other_factors in all_factors[1:]:
            ops += 1
            if item not in other_factors:
                is_common = False
                break
        
        # ถ้ามีครบทุกตัว ให้เก็บไว้ใน common และลบออกจากตัวเปรียบเทียบ
        if is_common:
            common.append(item)
            for other_factors in all_factors[1:]:
                other_factors.remove(item)

    print(f"Find all the common prime factors : {common}")

    # 4. หาผลคูณของตัวประกอบร่วมทั้งหมด
    gcd = 1
    for num in common:
        ops += 1
        gcd *= num
        
    print(f"Compute the product of all the common prime factors and return it as gcd : {gcd}")
    print("รอบทั้งหมดของ GCD2 (Sieve) :", ops)
    return gcd

def main():
    # สามารถส่งตัวเลขกี่ตัวก็ได้
    FindGCD2(189, 252, 1197, 292005)
    print("----------------------------------------------")

main()