import string

from rich.console import Console

console = Console()

letters = string.ascii_letters
letters = letters[15:26]


def split_expression(exp: str) -> list:
    expression_values = list()
    bracket = ["", 0]

    for char in expression.replace(" ", ""):
        if char == "(" or char == ")":
            bracket = [char, 1]
        else:
            if bracket[1] == 1:
                if bracket[0] == "(":
                    char = bracket[0] + char
                else:
                    char = char + bracket[0]
                bracket = ["", 0]
            expression_values.append(char)

    if bracket[1] == 1:
        expression_values[-1] = expression_values[-1] + bracket[0]

    return expression_values


# resolution method step by step


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


def find_logical_values(s_exp: list, s_pro: list, letters: list) -> list:
    logical_values = []
    
    # Step 1: Initialize the logical_values list with None for all possible combinations
    for _ in range(2 ** len(s_pro)):
        logical_values.append(None)
        
    logical_values.append(None)
    
    # Step 2: Find simple propositions logical values
    for char in s_pro:
        if "(" in char:
            char = char[1]
        if ")" in char:
            char = char[0]
        if char in letters:
            char_index = letters.index(char)
            c = 0
            
            # Here you would assign logical values to the propositions
            
            while c < len(logical_values) - 1:
                for _ in range(2 ** (len(s_pro) - (char_index + 1))):
                    logical_values.insert(c, True)
                    c += 1
                        
                for _ in range(2 ** (len(s_pro) - (char_index + 1))):
                    logical_values.insert(c, False)
                    c += 1
            
        logical_values.insert(-1, 1)
                    
    # Step 3: Find ~ (negation) logical values

    # Step 4: Find ^ (conjunction) logical values
    # Implement similar to Step 3
    
    # Step 5: Find : (disjunction) logical values
    # Implement similar to Step 3
    
    # Step 6: Find -> (implication) logical values
    # Implement similar to Step 3
    
    # Step 7: Find <-> (biconditional) logical values
    # Implement similar to Step 3
                
    return logical_values


if __name__ == "__main__":
    console.print("[red]AVISO: ~ ^ : -> <->")
    expression = input("[!] INSIRA A EXPRESSÃO: ")
    
    splited_expression = split_expression(expression)
    
    simple_propositions = find_simple_propositions(splited_expression, letters)
    
    _ = find_logical_values(splited_expression, simple_propositions, letters)
    console.print(_)
    