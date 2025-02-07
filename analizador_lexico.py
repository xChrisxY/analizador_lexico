import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

TOKENS = [
    ("COMENTARIO_MULTILINEA", r'"""[\s\S]*?"""'), 
    ("COMENTARIO_LINEA", r'#.*?(?:\n|$)'),      
    ("ENTRADA", r"\b(print|input)\b"),
    ("PALABRA_CLAVE", r"\b(if|else|while|for|def|return)\b"),
    ("DELIMITADOR", r"[{}();:]"),
    ("OPERADOR_LOGICO", r"(==|!=|<=|>=|<|>)"),
    ("OPERADOR_ARITMETICO", r"[+\-*/=]"),
    ("NUMERO_FLOTANTE", r"\b\d+\.\d+\b"),
    ("NUMERO", r"\b\d+\b"),
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("COMILLAS", r"['\"]"),
    ("ESPACIO", r"[ \t\n]+"),
]

def procesar_operadores_logicos(codigo):
    patrones = [
        (r'< =', '<='),
        (r'> =', '>='),
        (r'= =', '=='),
        (r'! =', '!=')
    ]
    
    for patron, reemplazo in patrones:
        codigo = re.sub(patron, reemplazo, codigo)
    
    return codigo

def analizador_lexico(codigo_fuente):
    codigo_fuente = procesar_operadores_logicos(codigo_fuente)
    
    tokens = []
    pos = 0
    
    while pos < len(codigo_fuente):
        match = None
        for token_tipo, patron in TOKENS:
            regex = re.compile(patron)
            match = regex.match(codigo_fuente, pos)
            if match:
                lexema = match.group(0)
                if token_tipo != "ESPACIO":
                    if token_tipo == "COMENTARIO_MULTILINEA":
                        lexema = lexema.strip() 
                    elif token_tipo == "COMENTARIO_LINEA":
                        lexema = lexema.strip()
                    tokens.append((token_tipo, lexema))
                pos = match.end()
                break
        if not match:
            raise ValueError(f"Error léxico: carácter inesperado en posición {pos} ({codigo_fuente[pos]})")
    return tokens

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        try:
            with open(archivo, 'r') as f:
                codigo_fuente = f.read()
            tokens = analizador_lexico(codigo_fuente)
            mostrar_tokens(tokens)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado.")
        except ValueError as e:
            messagebox.showerror("Error Léxico", str(e))

def mostrar_tokens(tokens):
    for row in tabla.get_children():
        tabla.delete(row)
    for tipo, lexema in tokens:
        tabla.insert("", "end", values=(tipo, lexema))

root = tk.Tk()
root.title("Analizador Léxico - 8° B")
root.geometry("600x450")
root.configure(bg="#2C3E50")
root.resizable(False, False)

frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=20)

title_label = tk.Label(frame, text="Analizador Léxico", font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
title_label.pack()

btn_cargar = tk.Button(frame, text="Cargar Código", command=cargar_archivo, font=("Arial", 12, "bold"), bg="#3498DB", fg="white", relief="raised", padx=10, pady=5)
btn_cargar.pack(pady=10)

cols = ("Tipo de Token", "Lexema")
tabla_frame = tk.Frame(root, bg="#2C3E50", bd=2, relief="solid")
tabla_frame.pack(pady=10, padx=10, fill="both", expand=True)

tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings", style="Custom.Treeview")
for col in cols:
    tabla.heading(col, text=col, anchor="center")
    tabla.column(col, width=250, anchor="center")
tabla.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("Custom.Treeview", background="#ECF0F1", foreground="black", rowheight=25, fieldbackground="#ECF0F1", borderwidth=1, relief="solid")
style.map("Custom.Treeview", background=[("selected", "#3498DB")])

root.mainloop()