ops = 0

def getFactorNaive(number):
    global ops
    factors = []
    temp = number
    d = 2

    while d * d <= temp:
        ops += 1

        while temp % d == 0:
            ops += 1
            factors.append(d)
            temp = temp // d
        d += 1

    if temp > 1:
        factors.append(temp)

    return factors

def findGCD1(*numbers):
    global ops
    
    if not numbers:
        return None
    
    # 1. หา Prime Factorization ของตัวเลขทุกตัว
    all_factors = []
    for num in numbers:
        factors = getFactorNaive(num)
        all_factors.append(factors)
        print(f"Find the prime factorization of {num} : {factors}")

    # 2. หาตัวประกอบเฉพาะร่วมของตัวเลขทั้งหมด
    # เริ่มต้นใช้ factor ของตัวเลขแรกเป็นตัวตั้งต้น
    common = []
    first_num_factors = all_factors[0].copy()

    for item in first_num_factors:
        ops += 1
        is_common = True
        
        # ตรวจสอบว่า item นี้มีอยู่ในตัวเลขตัวอื่นๆ ทุกตัวหรือไม่
        for other_factors in all_factors[1:]:
            ops += 1
            if item not in other_factors:
                is_common = False
                break
        
        # ถ้ามีอยู่ในทุกตัว ให้เก็บไว้ใน common และลบออกจากตัวเปรียบเทียบ 1 ตัว เพื่อป้องกันการนับซ้ำ
        if is_common:
            common.append(item)
            for other_factors in all_factors[1:]:
                other_factors.remove(item)

    print(f"Find all the common prime factors : {common}")

    # 3. คำนวณผลคูณของตัวประกอบร่วม
    gcd = 1
    for item in common:
        ops += 1
        gcd *= item

    print(f"Compute the product of all the common prime factors and return it as gcd : {gcd}")
    print("รอบทั้งหมดของ GCD1 (Naive) :", ops)
    return gcd

# เรียกใช้งานด้วยตัวเลขกี่ตัวก็ได้
findGCD1(953525754641,658518571823)
print("----------------------------------------------")