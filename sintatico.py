import ply.yacc as yacc
from lex import tokens  # Importar os tokens do seu lexer

# Definição das regras da gramática

# Regra inicial: programa completo
def p_program(p):
    '''program : INIT declarations statements FIM'''
    p[0] = ('program', p[2], p[3])

# Declarações de variáveis
def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    '''declaration : INT var_list SEMICOLON
                   | DEC var_list SEMICOLON
                   | TEXT var_list SEMICOLON'''
    p[0] = ('declaration', p[1], p[2])

# Lista de variáveis
def p_var_list(p):
    '''var_list : var_list COMMA ID
                | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Lista de instruções
def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Declaração de instruções
def p_statement(p):
    '''statement : assignment
                 | conditional
                 | loop
                 | io_operation'''
    p[0] = p[1]

# Atribuição
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

# Expressões matemáticas
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression LT term
                  | expression GT term
                  | expression LE term
                  | expression GE term
                  | expression EQ term
                  | expression NE term
                  | term'''
    if len(p) == 4:
        p[0] = ('expression', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        p[0] = ('term', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Condicional (if-else)
def p_conditional(p):
    '''conditional : IF LPAREN expression RPAREN LBRACE statements RBRACE else_statement'''
    p[0] = ('if', p[3], p[6], p[8])

def p_else_statement(p):
    '''else_statement : ELSE LBRACE statements RBRACE
                      | empty'''
    if len(p) == 5:
        p[0] = ('else', p[3])
    else:
        p[0] = None

# Laço while
def p_while_loop(p):
    '''loop : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = ('while', p[3], p[6])

# Laço for
def p_for_loop(p):
    '''loop : FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN LBRACE statements RBRACE'''
    p[0] = ('for', p[3], p[5], p[7], p[10])

# Operações de entrada/saída
def p_io_operation(p):
    '''io_operation : ESCREVA LPAREN STRING RPAREN SEMICOLON
                    | ESCREVA LPAREN ID RPAREN SEMICOLON'''
    p[0] = ('escreva', p[3])

# Expressão vazia (para uso opcional)
def p_empty(p):
    'empty :'
    p[0] = None

# Comando de leitura
def p_cmd_leitura(p):
    '''io_operation : LEIA LPAREN ID RPAREN SEMICOLON'''
    p[0] = ('leia', p[3])


# Erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe: '{p.value}' na linha {p.lineno}, tipo: {p.type}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Construir o parser
parser = yacc.yacc()

#-----------------------------------



# Teste do Analisador Sintático
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

    teste = '''
    init
        int a;
        while(a < 10) {
            escreva(a);
            a := a + 1
        }
    fim
    '''
    
    result = parser.parse(teste)
    print(result)