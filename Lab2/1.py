def check_file_balanced(filename):
    stack = []
    # พจนานุกรมจับคู่วงเล็บ
    matching = {')': '(', ']': '[', '}': '{'}

    try:
        # เปิดอ่านไฟล์ที่ต้องการตรวจ
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                for char in line:
                    # ถ้าเจอวงเล็บเปิดเก็บเข้า Stack
                    if char in "({[":
                        stack.append(char)
                    # ถ้าเจอวงเล็บปิดเช็กกับ Stack
                    elif char in ")}]":
                        if not stack or stack[-1] != matching[char]:
                            return "The file is NOT balanced."
                        stack.pop()

        # อ่านจบไฟล์แล้ว Stack ต้องว่าง
        if len(stack) == 0:
            return "The file is balanced."
        else:
            return "The file is NOT balanced."

    except FileNotFoundError:
        return f"Error: File '{filename}' not found."

# การใช้งาน: ใส่ชื่อไฟล์ที่ต้องการตรวจ เช่น 'Example1.py'
print(check_file_balanced('Lab2/c.txt'))