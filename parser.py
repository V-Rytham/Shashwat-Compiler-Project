"""MiniComp recursive-descent parser."""


def parse(tokens):
    """Parse tokens and return a simple AST statement list."""

    index = 0

    def current():
        return tokens[index]

    def at_end():
        return current()["type"] == "EOF"

    def match(expected_type=None, expected_value=None):
        nonlocal index
        token = current()
        if expected_type is not None and token["type"] != expected_type:
            expected = expected_type
            raise SyntaxError(
                f"Parser error at line {token['line']}: expected {expected}, got {token['type']} ('{token['value']}')"
            )
        if expected_value is not None and token["value"] != expected_value:
            expected = expected_value
            raise SyntaxError(
                f"Parser error at line {token['line']}: expected '{expected}', got '{token['value']}'"
            )
        index += 1
        return token

    def stmt_list():
        statements = []
        while not at_end():
            statements.append(stmt())
        return statements

    def stmt():
        token = current()
        if token["type"] == "KEYWORD" and token["value"] == "int":
            return decl_stmt()
        if token["type"] == "IDENTIFIER":
            return assign_stmt()
        raise SyntaxError(
            f"Parser error at line {token['line']}: expected declaration or assignment, got '{token['value']}'"
        )

    def decl_stmt():
        match("KEYWORD", "int")
        name = match("IDENTIFIER")
        match("SYMBOL", ";")
        return {"type": "declaration", "name": name["value"], "var_type": "int", "line": name["line"]}

    def assign_stmt():
        name = match("IDENTIFIER")
        match("OPERATOR", "=")
        expression = expr()
        match("SYMBOL", ";")
        return {"type": "assignment", "target": name["value"], "expr": expression, "line": name["line"]}

    def expr():
        node = term()
        while current()["type"] == "OPERATOR" and current()["value"] in {"+", "-"}:
            op = match("OPERATOR")["value"]
            right = term()
            node = {"type": "binop", "op": op, "left": node, "right": right}
        return node

    def term():
        node = factor()
        while current()["type"] == "OPERATOR" and current()["value"] in {"*", "/"}:
            op = match("OPERATOR")["value"]
            right = factor()
            node = {"type": "binop", "op": op, "left": node, "right": right}
        return node

    def factor():
        token = current()
        if token["type"] == "IDENTIFIER":
            return {"type": "identifier", "value": match("IDENTIFIER")["value"]}
        if token["type"] == "NUMBER":
            return {"type": "number", "value": match("NUMBER")["value"]}
        if token["type"] == "SYMBOL" and token["value"] == "(":
            match("SYMBOL", "(")
            node = expr()
            match("SYMBOL", ")")
            return node
        raise SyntaxError(
            f"Parser error at line {token['line']}: expected identifier, number, or '(', got '{token['value']}'"
        )

    ast = stmt_list()
    return ast
