import re

# Lexer
tokens_definitions = {
    'INIT': r'\binit\b',
    'END': r'\bfim\b',
    'INT': r'\bint\b',
    'DEC': r'\bdec\b',
    'TEXT': r'\btext\b',
    'IF': r'\bif\b',
    'ELSE': r'\belse\b',
    'WHILE': r'\bwhile\b',
    'FOR': r'\bfor\b',
    'READ': r'\bleia\b',
    'WRITE': r'\bescreva\b',
    'ASSIGN': r':=',
    'REL_OP': r'<|>|<=|>=|!=|==',
    'ADD_OP': r'\+|-',
    'MUL_OP': r'\*|/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'COMMA': r',',
    'SEMI': r';',
    'NUMBER': r'\d+(\.\d+)?',
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r'"[^"]*"',
    'WHITESPACE': r'[ \t]+',
    'NEWLINE': r'\n',
}

def lex(code):
    tokens_found = []
    position = 0
    while position < len(code):
        match = None
        for token_type, pattern in tokens_definitions.items():
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                text = match.group(0)
                if token_type not in ['WHITESPACE', 'NEWLINE']:
                    tokens_found.append((token_type, text))
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Erro Léxico: caractere inesperado '{code[position]}' na posição {position}")
    return tokens_found

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.code = []

    def match(self, expected_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == expected_type:
            self.position += 1
            return True
        return False

    def error(self, message="Erro de Sintaxe"):
        current_token = self.tokens[self.position] if self.position < len(self.tokens) else "EOF"
        raise SyntaxError(f"{message} no token {current_token} na posição {self.position}")

    def parse(self):
        self.program()
        return "\n".join(self.code)

    def program(self):
        if not self.match('INIT'):
            self.error("Esperado 'init'")
        self.declara()
        self.bloco()
        if not self.match('END'):
            self.error("Esperado 'fim'")

    def declara(self):
        while self.tokens[self.position][0] in ['INT', 'DEC', 'TEXT']:
            tipo = self.tokens[self.position][1]
            self.position += 1
            ids = []
            while self.match('ID'):
                ids.append(self.tokens[self.position - 1][1])
                if not self.match('COMMA'):
                    break
            if not self.match('SEMI'):
                self.error("Esperado ';' após declaração")
            for var in ids:
                if tipo == "int":
                    self.code.append(f"{var} = 0")
                elif tipo == "dec":
                    self.code.append(f"{var} = 0.0")
                elif tipo == "text":
                    self.code.append(f"{var} = ''")

    def bloco(self):
        while self.tokens[self.position][0] in ['READ', 'WRITE', 'ID', 'IF', 'WHILE', 'FOR']:
            self.cmd()

    def cmd(self):
        if self.match('READ'):
            self.cmd_leitura()
        elif self.match('WRITE'):
            self.cmd_escrita()
        elif self.match('ID') and self.match('ASSIGN'):
            self.cmd_expr()
        elif self.match('IF'):
            self.cmd_if()
        elif self.match('WHILE'):
            self.cmd_while()
        elif self.match('FOR'):
            self.cmd_for()
        else:
            self.error("Comando inválido")

    def cmd_leitura(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'leia'")
        if not self.match('ID'):
            self.error("Esperado identificador em 'leia'")
        var = self.tokens[self.position - 1][1]
        if not self.match('RPAREN') or not self.match('SEMI'):
            self.error("Erro no comando 'leia'")
        self.code.append(f"{var} = input()")

    def cmd_escrita(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'escreva'")
        if self.match('STRING'):
            texto = self.tokens[self.position - 1][1]
            self.code.append(f"print({texto})")
        elif self.match('ID'):
            var = self.tokens[self.position - 1][1]
            self.code.append(f"print({var})")
        else:
            self.error("Esperado texto ou identificador em 'escreva'")
        if not self.match('RPAREN') or not self.match('SEMI'):
            self.error("Erro no comando 'escreva'")

    def cmd_expr(self):
        var = self.tokens[self.position - 2][1]
        expr = self.expr()
        if not self.match('SEMI'):
            self.error("Esperado ';' após expressão")
        self.code.append(f"{var} = {expr}")

    def cmd_if(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'if'")
        cond = self.expr()
        if not self.match('RPAREN'):
            self.error("Esperado ')' após condição")
        if not self.match('LBRACE'):
            self.error("Esperado '{' após 'if'")
        self.code.append(f"if {cond}:")
        self.cmd_bloco()
        if self.match('ELSE'):
            if not self.match('LBRACE'):
                self.error("Esperado '{' após 'else'")
            self.code.append("else:")
            self.cmd_bloco()

    def cmd_while(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'while'")
        cond = self.expr()
        if not self.match('RPAREN'):
            self.error("Esperado ')' após condição")
        if not self.match('LBRACE'):
            self.error("Esperado '{' após 'while'")
        self.code.append(f"while {cond}:")
        self.cmd_bloco()

    def cmd_for(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'for'")
        assign1 = self.cmd_expr()
        cond = self.expr()
        assign2 = self.cmd_expr()
        if not self.match('RPAREN'):
            self.error("Esperado ')' após 'for'")
        if not self.match('LBRACE'):
            self.error("Esperado '{' após 'for'")
        self.code.append(f"for {assign1}; {cond}; {assign2}:")
        self.cmd_bloco()

    def cmd_bloco(self):
        while self.tokens[self.position][0] not in ['RBRACE']:
            self.cmd()
        if not self.match('RBRACE'):
            self.error("Esperado '}' ao final do bloco")

    def expr(self):
        result = ""
        while self.tokens[self.position][0] in ['ID', 'NUMBER', 'ADD_OP', 'MUL_OP', 'LPAREN', 'RPAREN']:
            result += self.tokens[self.position][1]
            self.position += 1
        return result

arquivo_output = 'codigo_saida.py'

# Main
def compiler():
    code = """
    init
    int a, b, d;
    dec c;
    text t;
    a := 5;
    b := 10;
    c := a + b;
    escreva(a);
    escreva(c);
    while() {
    escreva(1);
    c := c + 1
    }
    leia(d);
    fim
    """
    tokens = lex(code)
    parser = Parser(tokens)
    try:
        python_code = parser.parse()
        
        with open(arquivo_output, 'w', encoding='utf-8') as f:
            f.write(python_code)


    except SyntaxError as e:
        print(f"Erro: {e}")

compiler()
