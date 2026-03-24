"""MiniComp lexical analyzer."""

KEYWORDS = {"int", "float", "if", "else", "while"}
OPERATORS = {"+", "-", "*", "/", "="}
SYMBOLS = {";", "(", ")", "{", "}"}


def tokenize(source_code):
    """Convert source code into a list of tokens.

    Each token is a dictionary with keys: type, value, line.
    """
    tokens = []
    i = 0
    line = 1

    while i < len(source_code):
        char = source_code[i]

        if char == "\n":
            line += 1
            i += 1
            continue

        if char.isspace():
            i += 1
            continue

        if source_code[i : i + 2] == "//":
            while i < len(source_code) and source_code[i] != "\n":
                i += 1
            continue

        if char.isalpha() or char == "_":
            start = i
            while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == "_"):
                i += 1
            value = source_code[start:i]
            token_type = "KEYWORD" if value in KEYWORDS else "IDENTIFIER"
            tokens.append({"type": token_type, "value": value, "line": line})
            continue

        if char.isdigit():
            start = i
            while i < len(source_code) and source_code[i].isdigit():
                i += 1
            value = source_code[start:i]
            tokens.append({"type": "NUMBER", "value": value, "line": line})
            continue

        if char in OPERATORS:
            tokens.append({"type": "OPERATOR", "value": char, "line": line})
            i += 1
            continue

        if char in SYMBOLS:
            tokens.append({"type": "SYMBOL", "value": char, "line": line})
            i += 1
            continue

        raise SyntaxError(f"Lexer error at line {line}: unexpected character '{char}'")

    tokens.append({"type": "EOF", "value": "EOF", "line": line})
    return tokens


def print_tokens(tokens):
    for token in tokens:
        if token["type"] == "EOF":
            continue
        print(f"{token['type']:<10} {token['value']}")
