import sys
import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'ID', 'NUM', 'TEXTO',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA', 'DOT',
    'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'
]

# Palavras reservadas
reserved = {
    'init': 'INIT',
    'fimprog': 'FIMPROG',  # Ajustado para usar 'fimprog.'
    'int': 'INT',
    'dec': 'DEC',
    'text': 'TEXT',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR'
}

tokens += list(reserved.values())

# Expressões regulares para tokens simples
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_ASSIGN     = r':='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_DOT        = r'\.'

t_LE         = r'<='
t_GE         = r'>='
t_NE         = r'!='
t_EQ         = r'=='
t_LT         = r'<'
t_GT         = r'>'

# Ignorar espaços e tabs
t_ignore = ' \t'

# Definição de tokens com ações

def t_TEXTO(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover as aspas
    return t

def t_NUM(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

# Contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar comentários
def t_COMMENT(t):
    r'//.*'
    pass

# Definir erro léxico
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Dicionário para armazenar variáveis e seus tipos
symbol_table = {}

# Lista para armazenar código gerado
code_lines = []
indent_level = 1  # Começa com 1 dentro da função main()

def add_code(line):
    code_lines.append('    ' * indent_level + line)

def enter_block():
    global indent_level
    indent_level += 1

def exit_block():
    global indent_level
    indent_level -= 1

# Regra inicial
def p_Programa(p):
    '''Programa : INIT Declara Bloco FIMPROG DOT'''
    pass  # A geração de código principal será feita no compile_source

# Declaração de variáveis
def p_Declara(p):
    '''Declara : Declara Tipo ListaId SEMICOLON
               | Tipo ListaId SEMICOLON'''
    if len(p) == 5:
        tipo = p[2]
        ids = p[3]
    else:
        tipo = p[1]
        ids = p[2]
    for var in ids:
        if var in symbol_table:
            print(f"Erro: Variável '{var}' já declarada.")
            sys.exit(1)
        symbol_table[var] = tipo
    # Inicializar variáveis no código Python
    for var in ids:
        if symbol_table[var] == 'INT' or symbol_table[var] == 'DEC':
            add_code(f"{var} = 0")
        elif symbol_table[var] == 'TEXT':
            add_code(f"{var} = \"\"")

def p_Tipo(p):
    '''Tipo : INT
            | DEC
            | TEXT'''
    p[0] = p[1]

def p_ListaId(p):
    '''ListaId : ListaId COMMA ID
               | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Bloco de comandos
def p_Bloco(p):
    '''Bloco : Bloco Cmd
             | Cmd'''
    pass

# Comando
def p_Cmd(p):
    '''Cmd : CmdLeitura
           | CmdEscrita
           | CmdExpr
           | CmdIf
           | WhileStmt
           | ForStmt'''
    pass

# Comando de leitura
def p_CmdLeitura(p):
    'CmdLeitura : LEIA LPAREN ID RPAREN SEMICOLON'
    var = p[3]
    if var not in symbol_table:
        print(f"Erro: Variável '{var}' não declarada antes da leitura.")
        sys.exit(1)
    var_type = symbol_table[var]
    if var_type == 'INT':
        add_code(f"{var} = int(input())")
    elif var_type == 'DEC':
        add_code(f"{var} = float(input())")
    elif var_type == 'TEXT':
        add_code(f"{var} = input()")

# Comando de escrita
def p_CmdEscrita(p):
    '''CmdEscrita : ESCREVA LPAREN TEXTO RPAREN SEMICOLON
                  | ESCREVA LPAREN ID RPAREN SEMICOLON'''
    if p.slice[3].type == 'TEXTO':
        add_code(f'print("{p[3]}")')
    else:
        var = p[3]
        if var not in symbol_table:
            print(f"Erro: Variável '{var}' não declarada antes da escrita.")
            sys.exit(1)
        add_code(f'print({var})')

# Comando de atribuição
def p_CmdExpr(p):
    'CmdExpr : AssignStmt SEMICOLON'
    add_code(p[1])

# AssignStmt
def p_AssignStmt(p):
    'AssignStmt : ID ASSIGN Expr'
    var = p[1]
    expr = p[3]
    if var not in symbol_table:
        print(f"Erro: Variável '{var}' não declarada antes da atribuição.")
        sys.exit(1)
    p[0] = f"{var} = {expr}"

# Expressão
def p_Expr_plus(p):
    'Expr : Expr PLUS Termo'
    p[0] = f"({p[1]} + {p[3]})"

def p_Expr_minus(p):
    'Expr : Expr MINUS Termo'
    p[0] = f"({p[1]} - {p[3]})"

def p_Expr_term(p):
    'Expr : Termo'
    p[0] = p[1]

# Termo
def p_Termo_times(p):
    'Termo : Termo TIMES Fator'
    p[0] = f"({p[1]} * {p[3]})"

def p_Termo_divide(p):
    'Termo : Termo DIVIDE Fator'
    p[0] = f"({p[1]} / {p[3]})"

def p_Termo_fator(p):
    'Termo : Fator'
    p[0] = p[1]

# Fator
def p_Fator_num(p):
    'Fator : NUM'
    p[0] = str(p[1])

def p_Fator_id(p):
    'Fator : ID'
    var = p[1]
    if var not in symbol_table:
        print(f"Erro: Variável '{var}' não declarada antes do uso.")
        sys.exit(1)
    p[0] = var

def p_Fator_expr(p):
    'Fator : LPAREN Expr RPAREN'
    p[0] = f"({p[2]})"

# Comando if
def p_CmdIf(p):
    '''CmdIf : IF LPAREN Expr Op_rel Expr RPAREN LBRACE Bloco RBRACE SEMICOLON
             | IF LPAREN Expr Op_rel Expr RPAREN LBRACE Bloco RBRACE ELSE LBRACE Bloco RBRACE SEMICOLON'''
    if len(p) == 12:
        # Com else
        cond = f"{p[3]} {p[4]} {p[5]}"
        add_code(f"if {cond}:")
        enter_block()
        # 'Bloco' comandos já foram adicionados
        exit_block()
        add_code("else:")
        enter_block()
        # 'Bloco' do else já foram adicionados
        exit_block()
    else:
        # Sem else
        cond = f"{p[3]} {p[4]} {p[5]}"
        add_code(f"if {cond}:")
        enter_block()
        # 'Bloco' comandos já foram adicionados
        exit_block()

# Operador relacional
def p_Op_rel(p):
    '''Op_rel : LT
              | GT
              | LE
              | GE
              | NE
              | EQ'''
    p[0] = p[1]

# Comando while
def p_WhileStmt(p):
    'WhileStmt : WHILE LPAREN Cond RPAREN LBRACE Bloco RBRACE SEMICOLON'
    cond = p[3]
    add_code(f"while {cond}:")
    enter_block()
    # 'Bloco' comandos já foram adicionados
    exit_block()

def p_Cond(p):
    'Cond : Expr Op_rel Expr'
    p[0] = f"{p[1]} {p[2]} {p[3]}"

# Comando for
def p_ForStmt(p):
    'ForStmt : FOR LPAREN AssignStmt SEMICOLON Cond SEMICOLON AssignStmt RPAREN LBRACE Bloco RBRACE SEMICOLON'
    init = p[3]
    cond = p[5]
    increment = p[7]
    # Traduzir para a estrutura equivalente em Python
    add_code(f"{init}")
    add_code(f"while {cond}:")
    enter_block()
    # 'Bloco' comandos já foram adicionados
    exit_block()
    add_code(f"{increment}")

# Regra de erro sintático
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe na entrada.")
    sys.exit(1)

# Construir o parser
parser = yacc.yacc()

def compile_source(source_code):
    global code_lines, indent_level
    code_lines = []
    indent_level = 1  # Dentro da função main()
    parser.parse(source_code)
    main_code = '\n'.join(code_lines)
    compiled_code = f"def main():\n{main_code}\n\nif __name__ == '__main__':\n    main()"
    return compiled_code

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python compiler.py input.lang output.py")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        source = f.read()

    try:
        python_output = compile_source(source)
    except Exception as e:
        print(f"Compilação falhou: {e}")
        sys.exit(1)

    with open(output_file, 'w') as f:
        f.write("# Código Python gerado a partir do compilador\n")
        f.write(python_output)

    print(f"Compilação concluída. Código Python gerado em '{output_file}'.")
