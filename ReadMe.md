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
    int a, b;              
    dec c;                  
    text mensagem;           

    escreva("Digite o valor de a:"); 
    leia(a);             

    escreva("Digite o valor de b:");
    leia(b);         

    escreva("Digite um valor decimal para c:");
    leia(c);              

    escreva("Digite uma mensagem:");
    leia(mensagem);      


    if (a > b) {
        escreva("a é maior que b.");
    } else {
        escreva("a não é maior que b.");
    }

    escreva("Contando até 5 usando while:");
    int contador;       
    contador := 1;         
    while (contador <= 5) {
        escreva(contador);   
        contador := contador + 1; 
    }

    escreva("Contando de 1 a 5 usando for:");
    for (int i := 1; i <= 5; i := i + 1) {
        escreva(i);
    }

    escreva("Programa finalizado.");
fimprog.
```

## Exemplos menores: ( nossa linguagem )

### Exemplo output: ( nossa linguagem )

``` bash

init
    int a;
    escreva(a);
fimprog.

```

### Exemplo for: ( nossa linguagem )

``` bash

init
    int i;
    for (i := 0; i < 5; i := i + 1) {
        escreva(i);
    }
fimprog.


```

### Exemplo while: ( nossa linguagem )

``` bash

init
    int a;
    a := 0;
    while (a < 5) {
        escreva(a);
        a := a + 1;
    }
fimprog.

```

### Exemplo if/else: ( nossa linguagem )

``` bash

init
    int a, b;
    a := 5;
    b := 10;
    if (a < b) {
        escreva(a);
    } else {
        escreva(b);
    }
fimprog.

```

Execurar o compilador:

python compiler.py input.lang output.py
