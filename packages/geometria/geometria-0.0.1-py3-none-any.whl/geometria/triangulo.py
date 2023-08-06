import math


def area(base, altura):
    if base <= 0 or altura <= 0:
        return "Valor de entrada invalido"

    return (base * altura) / 2


def perimetro(ladoA, ladoB, ladoC):
    if not condicao_existencia_triangulo(ladoA, ladoB, ladoC):
        return "Digite um triangulo valido"

    return str(ladoA + ladoB + ladoC)


def heron(ladoA, ladoB, ladoC):
    if not condicao_existencia_triangulo(ladoA, ladoB, ladoC):
        return "Digite um triangulo valido"

    s = (ladoA + ladoB + ladoC) / 2
    return str(math.sqrt(s * (s - ladoA) * (s - ladoB) * (s - ladoC)))


def area_triangulo_equilatero(lado):
    if lado <= 0:
        return "Digite um lado valido"

    return "{:.2f}".format((math.sqrt(3) / 4) * lado * lado)


def condicao_existencia_triangulo(ladoA, ladoB, ladoC):
    if ladoA <= 0 or ladoB <= 0 or ladoC <= 0:
        return False
    elif (ladoA + ladoB) < ladoC:
        return False
    elif (ladoA + ladoC) < ladoB:
        return False
    elif (ladoB + ladoC) < ladoA:
        return False
    return True
