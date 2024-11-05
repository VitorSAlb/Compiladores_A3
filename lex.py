import ply.lex as lex

# Lista de tokens
tokens = [
    'ID',               # Identificadores
    'NUMBER',           # Números inteiros e decimais
    'STRING',           # Strings entre aspas
    'PLUS', 'MINUS',    # Operadores matemáticos
    'TIMES', 'DIVIDE',  # Operadores matemáticos
    'ASSIGN',           # Operador de atribuição :=
    'LT', 'GT',         # Operadores relacionais
    'LE', 'GE', 'EQ', 'NE', # Operadores relacionais
    'LPAREN', 'RPAREN', # Parênteses
    'LBRACE', 'RBRACE', # Chaves
    'COMMA', 'SEMICOLON' # Vírgula e ponto e vírgula
]

reserved = {
    'init': 'INIT',
    'fim': 'FIM',
    'int': 'INT',
    'dec': 'DEC',
    'text': 'TEXT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'leia': 'LEIA',       
    'escreva': 'ESCREVA'
}

# Mesclar palavras reservadas com tokens
tokens = tokens + list(reserved.values())

# Expressões regulares para tokens simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_ASSIGN  = r':='
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_EQ      = r'=='
t_NE      = r'!='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMMA   = r','
t_SEMICOLON = r';' 
t_ignore  = ' \t'  

# Expressão regular para números
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Expressão regular para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

# Expressão regular para strings
def t_STRING(t):
    r'"([^"\n]|(\\"))*"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

#-----------------------------------
# Código para testar o Lexer
if __name__ == "__main__":
    data = '''
    init
        int a, b, c;
        dec d;
        text msg;
        escreva("Exemplo");
        a := 5;
        if (a < 10) {
            escreva(a);
        } else {
            escreva("Valor muito grande");
        }
        while (a < 10) {
            escreva("Loop enquanto");
            a := a + 1;
        }
        for (a := 0; a < 5; a := a + 1) {
            escreva("Loop para");
        }
    fim
    '''
    
    lexer.input(data)
    
    # Tokenizar
    for tok in lexer:
        print(tok)