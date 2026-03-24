"""MiniComp three-address code generator."""


def generate_tac(ast):
    """Generate TAC lines from AST assignments."""
    tac = []
    temp_counter = [0]

    def new_temp():
        temp_counter[0] += 1
        return f"t{temp_counter[0]}"

    def emit_expr(node):
        if node["type"] == "number":
            return node["value"]
        if node["type"] == "identifier":
            return node["value"]
        if node["type"] == "binop":
            left = emit_expr(node["left"])
            right = emit_expr(node["right"])
            temp = new_temp()
            tac.append(f"{temp} = {left} {node['op']} {right}")
            return temp
        raise ValueError(f"Unsupported node in TAC generation: {node['type']}")

    for statement in ast:
        if statement["type"] == "assignment":
            result = emit_expr(statement["expr"])
            tac.append(f"{statement['target']} = {result}")

    return tac


def print_tac(tac_lines):
    for line in tac_lines:
        print(line)
