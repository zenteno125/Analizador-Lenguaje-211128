import tkinter as tk
from tkinter import ttk, messagebox
import ply.lex as lex
import ply.yacc as yacc

# Define reserved words
reserved = {
    'int': 'INT',
    'asd': 'STRING',
    'inn': 'MAIN',
    'funn': 'FUNN',
    'si': 'IF',
    'sino': 'IFELSE',
    'return': 'RETURN',
    'repite': 'REPITE',
    'contenido': 'CONTENIDO',
    'desde': 'DESDE',
    'hasta': 'HASTA',
    'var': 'VAR',
}

tokens = [
    'PLUS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'NUMBER',
    'ASSIGN',
    'ID',
    'GT',
    'LT',
    'DOUBLESTRING'
] + list(reserved.values())

t_GT = r','
t_PLUS = r'\+'
t_LT = r'<'
t_DOUBLESTRING = r'"[^"]*"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_ASSIGN = r'='


def reset_program():
    txt.delete("1.0", tk.END)
    txt.insert(tk.END, codigo)
    error_table.delete(*error_table.get_children())  # Limpiar la tabla de errores
    lexer.input('')
    parser.restart()


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t\n'


def t_error(t):
    error_table.insert('', 'end', values=(f"Illegal character '{t.value[0]}'",))
    t.lexer.skip(1)


lexer = lex.lex()


def p_completo(p):
    '''completo : funtions
                | declarations
                | program
                | if_clause
                | expression'''


def p_funtions(p):
    'funtions : FUNN ID LPAREN INT ID GT INT ID RPAREN LBRACE RETURN ID PLUS ID SEMI RBRACE'


def p_declarations(p):
    '''declarations : VAR INT ID SEMI 
                    | VAR STRING ID SEMI'''


def p_program(p):
    'program : FUNN MAIN LPAREN RPAREN LBRACE VAR INT ID SEMI ID ASSIGN ID LPAREN NUMBER GT NUMBER RPAREN SEMI RBRACE'


def p_if_clause(p):
    '''if_clause : VAR INT ID SEMI ID ASSIGN NUMBER SEMI IF ID LT NUMBER LBRACE CONTENIDO RBRACE IFELSE LBRACE CONTENIDO RBRACE'''


def p_expression(p):
    '''expression : VAR INT ID SEMI REPITE ID DESDE NUMBER HASTA NUMBER LBRACE CONTENIDO RBRACE'''


def p_condition(p):
    '''condition :  LT 
                 |  GT 
                 |  GT GT '''

    print("end do")


def p_error(p):
    if p:
        error_table.insert('', 'end', values=(f"Error de sintaxis en token '{p.value}'",))
    else:
        error_table.insert('', 'end', values=("Error de sintaxis en EOF",))


parser = yacc.yacc()

symbol_table = set()


def check_code():
    code = txt.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo('Resultado', 'No hay código para verificar.')
        return

    symbol_table.clear()
    lexer.input(code)

    # Limpia la tabla de errores antes de volver a analizar
    error_table.delete(*error_table.get_children())

    result = parser.parse(code, lexer=lexer)

    if not error_table.get_children():
        messagebox.showinfo('Resultado', 'La sintaxis es correcta.')
    else:
        messagebox.showerror('Resultado', 'Se encontraron errores de sintaxis .')


root = tk.Tk()
root.title("Analizador")
root.configure(bg='white')

codigo = '''condicional -----------------------

var int edad;
edad = 18;
si edad < 18 {
contenido
} sino {
contenido }

Función Main------------------------

funn inn() {

var int resultado;
resultado = concatenar(5, 7);

}

Declaracion de variables ------------

var int numeros;   |    var asd letras;

Funciones ----------------------------

funn concatenar(int num1, int num2 ){
return num1 + num2;
}


Ciclos -------------------------------

var int ciclito;
repite ciclito desde 1 hasta 10 {
contenido
}'''

txt = tk.Text(root, width=45, height=20)
txt.pack(side='left', padx=10, pady=10)
txt.insert(tk.END, codigo)

btn_analizar = tk.Button(root, text="Analizar", command=check_code)
btn_analizar.pack(side='left', padx=10)

btn_reset = tk.Button(root, text="Reiniciar", command=reset_program)
btn_reset.pack(side='left', padx=10)

token_frame = tk.Frame(root, bg='gray')
token_frame.pack(side='left', padx=10, pady=10)

error_frame = tk.Frame(root, bg='gray')
error_frame.pack(side='left', padx=10, pady=10)

error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
error_table.heading('Error', text='Errores')
error_table.column('Error', width=200)
error_table.pack()

root.mainloop()
