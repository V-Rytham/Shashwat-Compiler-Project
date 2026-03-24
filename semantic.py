"""MiniComp semantic analyzer."""


def analyze(ast):
    """Analyze AST, return symbol table and raise on semantic errors."""
    symbol_table = {}

    def check_expr(node, line):
        if node["type"] == "identifier":
            name = node["value"]
            if name not in symbol_table:
                raise ValueError(
                    f"Semantic error at line {line}: variable '{name}' used before declaration"
                )
            return
        if node["type"] == "number":
            return
        if node["type"] == "binop":
            check_expr(node["left"], line)
            check_expr(node["right"], line)
            return

    for statement in ast:
        if statement["type"] == "declaration":
            name = statement["name"]
            if name in symbol_table:
                raise ValueError(
                    f"Semantic error at line {statement['line']}: duplicate declaration of '{name}'"
                )
            symbol_table[name] = statement["var_type"]
        elif statement["type"] == "assignment":
            target = statement["target"]
            if target not in symbol_table:
                raise ValueError(
                    f"Semantic error at line {statement['line']}: variable '{target}' assigned before declaration"
                )
            check_expr(statement["expr"], statement["line"])

    return symbol_table


def print_symbol_table(symbol_table):
    for name, var_type in symbol_table.items():
        print(f"{name:<10} {var_type}")
