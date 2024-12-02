# Trabalho A3 - TCC

## Componentes

- Vitor Santana e Albuquerque - 1272215370
- Lucas Lopes - 1272215973
- Lucas Lima - 1272215898
- Wadson Daniel - 1272216683

## [Link do Video](https://www.youtube.com)

# Gramatica


Aqui está a tabela de gramática com base nos tokens definidos:

arduino
Copiar código
Programa     : 'init' Declara Bloco 'fim' '.'.
Declara      : Tipo Id (',' Id)* ';'.
Tipo         : 'int' | 'dec' | 'texto'.
Bloco        : (Cmd)+.
Cmd          : CmdLeitura | CmdEscrita | CmdExpr | CmdIf | WhileStmt | ForStmt.
CmdLeitura   : 'leia' '(' Id ')' ';'.
CmdEscrita   : 'escreva' '(' Texto | Id ')' ';'.
CmdIf        : 'se' '(' Expr Op_rel Expr ')' '{' Cmd+ '}' ('senao' '{' Cmd+ '}')? ';'.
WhileStmt    : 'enquanto' '(' Cond ')'{ Bloco '}' ';'.
ForStmt      : 'para' '(' AssignStmt ';' Cond ';' AssignStmt ')' '{' Bloco '}' ';'.
CmdExpr      : Id 'recebe' Expr ';'.
Op_rel       : 'menor_igual' | 'maior_igual' | 'igual' | 'diferente' | 'menor' | 'maior'.
Expr         : Expr 'mais' Termo | Expr 'menos' Termo | Termo.
Termo        : Termo 'vezes' Fator | Termo 'dividido' Fator | Fator.
Fator        : Numero | Id | '(' Expr ')'.
Texto        : '"' (0..9 | a..z | A..Z | ' ')* '"'.
Numero       : (0..9)+ ('.' (0..9)+)?.
Id           : (a..z | A..Z) (a..z | A..Z | 0..9)*.
Cond         : Expr Op_rel Expr.
AssignStmt   : Id 'recebe' Expr.

## Exemplo de entrada: ( nossa linguagem )
- No arquivo [testes.txt](./testes.txt), temos outros exemplos de código
``` bash
init
    dec numero.
    dec soma.
    int contador.

    escreva("Digite um número decimal:").
    leia(numero).

    soma recebe 1.1.
    contador recebe 1.

    enquanto (contador menor_igual numero) {
        soma recebe soma mais contador.
        contador recebe contador mais 1.
    }

    se (soma maior 20) {
        escreva("Game Over").
    } 

    se (soma menor_igual 20) {
        escreva("Soma fica").
        escreva(numero).
        escreva("é:").
        escreva(soma).
    }
fim

```

# Como utilizar nosso compilador

- No arquivo input.lang introduza o codigo com a linguagem desenvolvida pela equipe

- Após introduzir isto execute o comando a seguir:

``` bash

python compiler.py input.txt

```

- Depois de executar é só conferir o codigo gerado no output.py


