import re

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def precedence(op: str) -> int:
    """กำหนดลำดับความสำคัญของเครื่องหมายคณิตศาสตร์"""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def is_operator(token: str) -> bool:
    """ตรวจสอบว่าเป็นตัวดำเนินการหรือไม่"""
    return token in ('+', '-', '*', '/')


def build_expression_tree(infix_expression: str) -> Node:
    tokens = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', infix_expression)
    nodes_stack = []
    ops_stack = []

    def process_operator():
        op = ops_stack.pop()
        node = Node(op)
        node.right = nodes_stack.pop()
        node.left = nodes_stack.pop()
        nodes_stack.append(node)

    for token in tokens:
        if token == '(':
            ops_stack.append(token)
        elif token == ')':
            while ops_stack and ops_stack[-1] != '(':
                process_operator()
            ops_stack.pop()  # Pop '('
        elif is_operator(token):
            while (ops_stack and ops_stack[-1] != '(' and
                   precedence(ops_stack[-1]) >= precedence(token)):
                process_operator()
            ops_stack.append(token)
        else:
            # เป็นตัวเลข (Operand)
            nodes_stack.append(Node(token))

    while ops_stack:
        process_operator()

    return nodes_stack[-1]


def inorder(root: Node) -> list:
    """Inorder Traversal: Left -> Root -> Right"""
    result = []
    if root:
        result.extend(inorder(root.left))
        result.append(root.value)
        result.extend(inorder(root.right))
    return result


def preorder(root: Node) -> list:
    """Preorder Traversal: Root -> Left -> Right"""
    result = []
    if root:
        result.append(root.value)
        result.extend(preorder(root.left))
        result.extend(preorder(root.right))
    return result


def postorder(root: Node) -> list:
    """Postorder Traversal: Left -> Right -> Root"""
    result = []
    if root:
        result.extend(postorder(root.left))
        result.extend(postorder(root.right))
        result.append(root.value)
    return result


if __name__ == "__main__":
    expression = "(3 + 5) - (2 - 8) / (4 + 6)"
    root = build_expression_tree(expression)

    print("=== Task 1: Binary Expression Tree Traversals ===")
    print("Expression:", expression)
    print("Inorder:   ", " ".join(inorder(root)))
    print("Preorder:  ", " ".join(preorder(root)))
    print("Postorder: ", " ".join(postorder(root)))