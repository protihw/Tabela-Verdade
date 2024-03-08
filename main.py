import string

from rich.console import Console

console = Console()

letters = string.ascii_letters
letters = letters[15:26]


# this function splits the expression in simple propositions or logical operators and return it
def split_expression(exp: str) -> list:
    expression_values = list()
    bracket = ["", False]
    _ = 0

    for char in expression.replace(" ", ""):
        if char in ["<", ">"]:
            pass
        elif char in ["(", ")"]:
            bracket = [char, True]
        elif char == "-":
            index = expression.index(char, _)

            if expression[index - 1] == "<":
                char = "<->"
            else:
                char = "->"

            expression_values.append(char)

            _ = index + 1
        else:
            if bracket[1] is True:
                if bracket[0] == "(":
                    char = bracket[0] + char
                else:
                    char = char + bracket[0]
                bracket = ["", 0]

                expression_values.append(char)
            else:
                expression_values.append(char)

    if bracket[1] == 1:
        expression_values[-1] = expression_values[-1] + bracket[0]

    return expression_values


# this function uses a loop to read the splited expression and return the simple propositions
def find_simple_propositions(s_exp: list) -> set:
    simple_propositions = set()

    for char in s_exp:         
        if len(char) == 2:
            for c in char:
                if c in letters:
                    simple_propositions.add(c)
        else:
            if char in letters:
                simple_propositions.add(char)

    return simple_propositions


# this function uses the simple proposiitions to find their logical values and return them
def find_simple_logical_values(char: str, s_pro: list) -> list:
    # [proposition/logical operator, logical values, row index]
    logical_values = [char]
 
    while len(logical_values) < 2 ** len(s_pro):
        for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
            logical_values.append(1)
        for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
            logical_values.append(0)

    logical_values.append(1)

    return logical_values


def find_denial_logical_values(sp_logical_values: list) -> list:
    # [proposition/logical operator, logical values, row index]
    logical_values = ["~"]

    for value in sp_logical_values:
        if isinstance(value, int):
            if value == 0:
                logical_values.append(1)
            else:
                logical_values.append(0)

    logical_values[-1] = 2

    return logical_values


# this function uses the splited expression to find the brackets and organize/return them in order
def resolve_brackets(s_exp: list) -> list:
    result = []
    stack = []
    for char in expression:
        if char == '(':
            if stack:
                result.append(''.join(stack))
            stack = []
        elif char == ')':
            if stack:
                result.append(''.join(stack))
            stack = []
        else:
            stack.append(char)
    if stack:
        result.append(''.join(stack))
    return result


if __name__ == "__main__":
    console.print("[red]AVISO: ~ ^ : -> <->")
    expression = input("[!] INSIRA A EXPRESSÃO: ")

    splited_expression = split_expression(expression)
    simple_propositions = find_simple_propositions(splited_expression)  
    simple_logical_values = find_simple_logical_values(
        "p", simple_propositions
    )
    denial_logical_values = find_denial_logical_values(simple_logical_values)
    brackets = resolve_brackets(splited_expression)
    console.print(f"[yellow]{simple_logical_values}")
    console.print(f"[yellow]{denial_logical_values}")
    console.print(f"[yellow]{brackets}")
