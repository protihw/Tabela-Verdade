import string

from rich.console import Console

console = Console()

letters = string.ascii_letters
letters = letters[15:26]


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


# resolution method step by step


# this fuction uses a loop to read the splited expression and return the simple propositions
def find_simple_propositions(s_exp: list, letters: list) -> list:
    simple_propositions = list()

    for char in s_exp:                
        if len(char) == 2:
            for c in char:
                if c in letters and c not in simple_propositions:
                    simple_propositions.append(c)

        if char in letters:
            simple_propositions.append(char)
   
    return simple_propositions


# this function uses the simple proposiitions to find their logical values and return them
def find_sp_logical_values(s_pro: list, letters: list) -> list:
    logical_values = []
    row_logical_valeus = []
    
    for char in s_pro:
        row_logical_valeus.append(char)
        
        while len(row_logical_valeus) < 2 ** len(s_pro):
            for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
                row_logical_valeus.append(1)
            for _ in range(0, 2 ** (len(s_pro) - (letters.index(char) + 1))):
                row_logical_valeus.append(0)

        logical_values.append(row_logical_valeus)
        row_logical_valeus = []
    
    
    return logical_values


if __name__ == "__main__":
    console.print("[red]AVISO: ~ ^ : -> <->")
    expression = input("[!] INSIRA A EXPRESSÃO: ")
    
    splited_expression = split_expression(expression)
    
    console.print(f"EXPRESSÃO DIVIDA: {splited_expression}")

    simple_propositions = find_simple_propositions(splited_expression, letters)
    
    console.print(f"PROPOSIÇÕES SIMPLES: {simple_propositions}")
    
    logical_values = find_sp_logical_values(simple_propositions, letters)
    
    console.print(f"VALORES LÓGICOS SP: {logical_values}")