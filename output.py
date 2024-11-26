numero = 0.0  # float
soma = 0.0  # float
contador = 0  # int
print("Digite um número decimal:")
numero = float(input())
soma = 1.1
contador = 1
while contador <= numero:
    soma = (soma + contador)
    contador = (contador + 1)
if soma > 20:
    print("Game Over")
if soma <= 20:
    print("Soma fica")
    print(numero)
    print("é:")
    print(soma)