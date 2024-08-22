from __future__ import annotations
import ast
from typing import cast, Union


with open("./2020/resources/18.txt") as f:
    lines = f.read().splitlines()


Expression = list[Union["Expression", int, str]]


def problem_1() -> None:
    def parse(line: str) -> Expression:
        if "(" not in line:
            return [int(item) if item.isnumeric() else item for item in line.split()]
        depth = 0
        result: Expression = []
        start = 0
        for i, char in enumerate(line):
            if char == "(":
                depth += 1
                if depth == 1:
                    result.extend(parse(line[start:i]))
                    start = i + 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    result.append(parse(line[start:i]))
                    start = i + 1
        if start != len(line):
            result.extend(parse(line[start:]))
        return result

    def evaluate(expr: Expression | int | str) -> int:
        if isinstance(expr, str):
            raise ValueError(f"expr {expr} should not be a string")
        elif isinstance(expr, int):
            return expr
        while len(expr) > 1:
            left = evaluate(expr[0])
            op = expr[1]
            right = evaluate(expr[2])
            if op == "+":
                result = left + right
            elif op == "*":
                result = left * right
            else:
                raise ValueError(f"unknown operator {op}")
            expr[:3] = [result]
        if not isinstance(expr[0], int):
            print(f"evaluation finished, but the remaining item is of type {type(expr[0])}")
        return cast(int, expr[0])

    print(sum(evaluate(parse(line)) for line in lines))


def problem_2() -> None:
    class ReplaceNodes(ast.NodeTransformer):
        def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp:
            self.generic_visit(node)
            if isinstance(node.op, ast.Add):
                return ast.BinOp(left=node.left, op=ast.Mult(), right=node.right)
            elif isinstance(node.op, ast.Mult):
                return ast.BinOp(left=node.left, op=ast.Add(), right=node.right)
            else:
                raise ValueError(f"invalid operatior of type {type(node.op)}")

    total = 0
    for line in lines:
        replaced = line.replace("+", "_tmp").replace("*", "+").replace("_tmp", "*")
        parsed = ReplaceNodes().visit(ast.parse(replaced))
        expr = ast.fix_missing_locations(ast.Expression(parsed.body[0].value))
        total += eval(compile(expr, "<string>", "eval"))
    print(total)
