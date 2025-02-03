#!/usr/bin/env python3 
import re 

TOKENS = [
    ("PALABRA_CLAVE", r"\b(if|else)\b"),
    ("DELIMITADOR", r"[{}();]"),
    ("OPERADOR_LOGICO", r"(==|!=|<=|>=|<|>)"),
    ("OPERADOR_ARITMETICO", r"[+\-*/=]"),
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NUMERO", r"\b\d+\b"),
    ("ESPACIO", r"[ \t\n]+")
]

def analizador_lexico(path):
    
    with open(path, 'r') as archivo:
        codigo_fuente = archivo.read()

    tokens = []
    pos = 0
    
    print("El valor de codigo fuente es:")
    print(codigo_fuente)

    while pos < len(codigo_fuente):
        print(f"El valor de pos es: {pos}")

        match = None

        for token_tipo, patron in TOKENS:
            print("El valor de token_tipo es %s y de patron es %s" % (token_tipo, patron))
            regex = re.compile(patron)
            match = regex.match(codigo_fuente, pos)

            if match: 
                print(match)
                lexema = match.group(0)
                if token_tipo != "ESPACIO":
                    tokens.append((token_tipo, lexema))
                pos = match.end()
                break

        if not match: 
            raise ValueError(f"Error léxico: carácter inesperado en posición {pos} ({codigo_fuente[pos]})")

    return tokens


archivo = 'programa.txt'
try:
    tokens = analizador_lexico(archivo)
    for token in tokens:
        print(token)
except FileNotFoundError:
    print(f'Error: El archivo {archivo} no fue encontrado.')
except ValueError as e:
    print(e)
    



