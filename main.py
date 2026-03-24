"""MiniComp compiler frontend runner."""

from lexer import tokenize, print_tokens
from parser import parse
from semantic import analyze, print_symbol_table
from intermediate import generate_tac, print_tac


def run_pipeline(input_path="sample_input.txt"):
    with open(input_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    print("TOKENS:")
    tokens = tokenize(source_code)
    print_tokens(tokens)
    print()

    ast = parse(tokens)
    print("SYNTAX: VALID")
    print()

    symbol_table = analyze(ast)
    print("SYMBOL TABLE:")
    print_symbol_table(symbol_table)
    print()

    tac = generate_tac(ast)
    print("INTERMEDIATE CODE:")
    print_tac(tac)


if __name__ == "__main__":
    run_pipeline()
