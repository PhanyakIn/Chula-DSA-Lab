def precedence(op):
    if op in ('+', '-'): return 1
    if op in ('*', '/'): return 2
    return 0

def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b

def evaluate_expression(expr):
    values = [] # Stack เก็บตัวเลข
    ops = []    # Stack เก็บเครื่องหมาย
    i = 0

    while i < len(expr):
        if expr[i] == ' ':
            i += 1
            continue

        # เช็กว่าเป็น Unary Sign (+ หรือ - ที่อยู่หน้าตัวเลข) หรือไม่
        is_unary = False
        if expr[i] in ('+', '-'):
            # หา index ตัวอักษรก่อนหน้าที่ไม่ใช่ช่องว่าง
            prev_idx = i - 1
            while prev_idx >= 0 and expr[prev_idx] == ' ':
                prev_idx -= 1
            
            # อยู่หน้าสุด หรือ ตัวก่อนหน้าเป็น '(' หรือ เครื่องหมายอื่น
            if prev_idx < 0 or expr[prev_idx] in ('(', '+', '-', '*', '/'):
                is_unary = True

        if expr[i] == '(':
            ops.append(expr[i])

        elif expr[i].isdigit() or is_unary:
            # ดึงเครื่องหมาย (ถ้ามี)
            sign = 1
            if is_unary:
                if expr[i] == '-':
                    sign = -1
                i += 1
                # ข้ามช่องว่างหลังเครื่องหมาย (ถ้ามี)
                while i < len(expr) and expr[i] == ' ':
                    i += 1

            # อ่านตัวเลข (รวมทศนิยมถ้าต้องการ)
            val = 0
            has_digit = False
            while i < len(expr) and expr[i].isdigit():
                val = (val * 10) + int(expr[i])
                i += 1
                has_digit = True

            if has_digit:
                values.append(sign * val)
                i -= 1 # ถอย 1 เพื่อให้ลูปหลักวน i += 1 ได้ถูกต้อง

        elif expr[i] == ')':
            while ops and ops[-1] != '(':
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                values.append(apply_op(a, b, op))
            ops.pop() # ลบ '(' ออก

        else: # เครื่องหมาย +, -, *, / แบบ Binary
            while ops and precedence(ops[-1]) >= precedence(expr[i]):
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                values.append(apply_op(a, b, op))
            ops.append(expr[i])

        i += 1

    while ops:
        b = values.pop()
        a = values.pop()
        op = ops.pop()
        values.append(apply_op(a, b, op))

    return values[-1]

# ฟังก์ชันอ่านไฟล์มาคำนวณ
def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                result = evaluate_expression(line)
                print(f"Expression: {line} = {result}")


process_file('Lab2/test2.txt')