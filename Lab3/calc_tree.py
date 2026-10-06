from tree import build_expression_tree, postorder, is_operator

def evaluate_postorder(postorder_tokens: list) -> float:
    """
    คำนวณหาผลลัพธ์จาก Postorder (Postfix) โดยใช้ Stack
    """
    stack = []

    for token in postorder_tokens:
        if is_operator(token):
            operand2 = stack.pop()
            operand1 = stack.pop() 

            if token == '+':
                res = operand1 + operand2
            elif token == '-':
                res = operand1 - operand2
            elif token == '*':
                res = operand1 * operand2
            elif token == '/':
                res = operand1 / operand2
            
            stack.append(res)
        else:
            stack.append(float(token))

    return stack.pop()


if __name__ == "__main__":
    expression = "((10 - 2) * (8 / (3 + 1))) + 5"
    
    # สร้าง Tree และหา Postorder traversal จาก Task 1
    root = build_expression_tree(expression)
    postorder_tokens = postorder(root)

    print("=== Task 2: Evaluate Expression using Postorder & Stack ===")
    print("Postorder Traversal Input:", " ".join(postorder_tokens))
    result = evaluate_postorder(postorder_tokens)
    print(f"Calculated Result: {result}")