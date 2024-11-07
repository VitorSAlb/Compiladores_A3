# Gramatica

Programa : 'init' Declara Bloco 'fim'.
Declara  : Tipo Id (',' Id)* ';'.
Tipo     : 'int' | 'dec' | 'text'.
Bloco    : (Cmd)+
Cmd      : CmdLeitura | CmdEscrita | CmdExpr | CmdIf | WhileStmt | ForStmt
CmdLeitura : 'leia' '(' Id ')' ';'.
CmdEscrita : 'escreva' '(' Texto | Id ')' ';'.
CmdIf    : 'if' '(' Expr Op_rel Expr ')' '{' Cmd+ '}' ('else' '{' Cmd+ '}')? ';'.
WhileStmt : 'while' '(' Cond ')' '{' Bloco '}' ';'.
ForStmt : 'for' '(' AssignStmt ';' Cond ';' AssignStmt ')' '{' Bloco '}' ';'.
CmdExpr  : Id ':=' Expr ';'.
Op_rel   : '<' | '>' | '<=' | '>=' | '!=' | '=='.
Expr     : Expr '+' Termo | Expr '-' Termo | Termo.
Termo    : Termo '*' Fator | Termo '/' Fator | Fator.
Fator    : Num | Id | '(' Expr ')'.
Texto    : '"' (0..9 | a..z | A..Z | ' ') '"'.
Num      : (0..9)+.
Id       : (a..z | A..Z) (a..z | A..Z | 0..9)*.



## Exemplo de entrada: ( nossa linguagem )
``` bash
init
    int a, b, c.
    dec d.
    text msg.
    escreva("Exemplo").
    a := 5.
    if (a < 10) {
        escreva(a).
    } else {
        escreva("Valor muito grande").
    }
fim
```


## Exemplo de saida: ( pytjon)

```python
a = 0
b = 0
c = 0
d = 0.0 
msg = "" 

print("Exemplo")

a = 5

if a < 10:
    print(a)
else:
    print("Valor muito grande")

```

Execurar o compilador:

python compiler.py input.lang output.py
