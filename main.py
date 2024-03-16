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


# this function uses the simple propositions to find their logical values and return them
def find_simple_propositions_logical_values(char: str, s_pro: list) -> list:
    # [proposition/logical operator, logical values, row index]
    logical_values = [char]

    while len(logical_values) < 2 ** len(s_pro):
        for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
            logical_values.append(1)
        for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
            logical_values.append(0)

    logical_values.append(1)

    return logical_values


def find_denial_logical_values(s_pro_logical_values: list) -> list:
    # [proposition/logical operator, logical values, row index]
    logical_values = ["~"]

    for value in s_pro_logical_values:
        if isinstance(value, str):
            logical_values[0] = logical_values[0] + value
        if isinstance(value, int):
            if value == 0:
                logical_values.append(1)
            else:
                logical_values.append(0)

    logical_values[-1] = 2

    return logical_values


# this function uses the splited expression to find the logical values of a conjunction and return them
def find_conjunction_logical_values(
        char_index: int, expression: list, truth_table: list
        ) -> list:
    logical_values = ["^"]

    char = expression[char_index].replace(" ", "") #
    pp_char = expression[char_index-2].replace(" ", "") # char two steps before ^
    p_char = expression[char_index-1].replace(" ", "") # char one step before ^
    n_char = expression[char_index+1].replace(" ", "") # char one step after ^
    nn_char = expression[char_index+2].replace(" ", "") # char two steps after ^

    if pp_char == "~":
        for list in truth_table:
            if list[0][0] == pp_char and list[0][1] == p_char:
                previous_logical_values = list

    if n_char == "~":
        for list in truth_table:
            if list[0][0] == n_char and list[0][1] == nn_char:
                next_logical_values = list

    for index, value in enumerate(previous_logical_values):
        if isinstance(value, int):
            if value == 1 and next_logical_values[index] == 1:
                logical_values.append(1)
            else:
                logical_values.append(0)

    console.print(logical_values)

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


def resolve_expression(
        s_exp: list,
        s_pro: set,
        brackets: list
        ) -> list:
    truth_table = list()

    truth_table.append(s_exp)

    # find simple proposition logical values
    for char in s_exp:
        if len(char) == 2 and "(" in char or ")" in char:
            char = char.strip("()")

        if char in letters:
            logical_values = find_simple_propositions_logical_values(
                char, s_pro
            )
            truth_table.append(logical_values)

    # find denial operators logical values
    for index, char in enumerate(s_exp):
        if len(char) == 2 and "(" in char or ")" in char:
            char = char.strip("()")

        if char == "~":
            try:
                logical_values = find_denial_logical_values(
                    find_simple_propositions_logical_values(
                        s_exp[index+1], s_pro
                    )
                )
                truth_table.append(logical_values)
            except ValueError:
                logical_values = find_denial_logical_values(
                    find_simple_propositions_logical_values(
                        s_exp[index+1].strip("()"), s_pro
                    )
                )
                truth_table.append(logical_values)

    return truth_table


if __name__ == "__main__":
    console.print("[red]AVISO: ~ ^ : -> <->")
    expression = input("[!] INSIRA A EXPRESSÃO: ")

    splited_expression = split_expression(expression)
    simple_propositions = find_simple_propositions(splited_expression)
    brackets_order = resolve_brackets(splited_expression)

    truth_table = resolve_expression(
        splited_expression, simple_propositions, brackets_order
    )

    for v in truth_table:
        console.print(f"[yellow]{v}", end=" | ")

    for expression in brackets_order:
        if "^" in expression:
            char_index = expression.index("^")
            logical_values = find_conjunction_logical_values(
                char_index-1, split_expression(expression), truth_table
            )
