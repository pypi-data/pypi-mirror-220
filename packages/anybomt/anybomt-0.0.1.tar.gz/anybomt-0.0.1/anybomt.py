import ctypes
import numpy as np
# -*- coding: utf-8 -*-

# Carrega a biblioteca C
lib = ctypes.CDLL("./anybomt.so")

# Definir o tipo de retorno e os tipos de argumentos para a função factorial
lib.factoriall.restype = ctypes.c_int
lib.factoriall.argtypes = [ctypes.c_int]

# Definir o tipo de retorno e os tipos de argumentos para a função power
lib.potenc.restype = ctypes.c_int
lib.potenc.argtypes = [ctypes.c_int, ctypes.c_int]

# Definir o tipo de retorno e os tipos de argumentos para a função max
lib.maximo.restype = ctypes.c_int
lib.maximo.argtypes = [ctypes.c_int, ctypes.c_int]

# Definir o tipo de retorno e os tipos de argumentos para a função min
lib.minimo.restype = ctypes.c_int
lib.minimo.argtypes = [ctypes.c_int, ctypes.c_int]

# Definir o tipo de retorno e os tipos de argumentos para a função raiz_quadrada
lib.raiz_quadrada.restype = ctypes.c_double
lib.raiz_quadrada.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função sin
lib.seno.restype = ctypes.c_double
lib.seno.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função cos
lib.cosseno.restype = ctypes.c_double
lib.cosseno.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função tan
lib.tangente.restype = ctypes.c_double
lib.tangente.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função log
lib.logaritmo_natural.restype = ctypes.c_double
lib.logaritmo_natural.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função log10
lib.log_base_10.restype = ctypes.c_double
lib.log_base_10.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função cosh
lib.cosseno_hiperbolica.restype = ctypes.c_double
lib.cosseno_hiperbolica.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função sinh
lib.seno_hiperbolica.restype = ctypes.c_double
lib.seno_hiperbolica.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função tanh
lib. tangente_hiper.restype = ctypes.c_double
lib. tangente_hiper.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função acos
lib.arco_cossen.restype = ctypes.c_double
lib.arco_cossen.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função asin
lib.arco_sen.restype = ctypes.c_double
lib.arco_sen.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função atan
lib.arco_tang.restype = ctypes.c_double
lib.arco_tang.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função atan2
lib.arco_tang2.restype = ctypes.c_double
lib.arco_tang2.argtypes = [ctypes.c_double, ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função exp
lib.exponencial.restype = ctypes.c_double
lib.exponencial.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função log1p
lib.log_natural_mais_um.restype = ctypes.c_double
lib.log_natural_mais_um.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função fabs
lib.modulo.restype = ctypes.c_double
lib.modulo.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função log2
lib.log_na_base2.restype = ctypes.c_double
lib.log_na_base2.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função floor
lib.piso.restype = ctypes.c_double
lib.piso.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função round
lib.arredonda.restype = ctypes.c_double
lib.arredonda.argtypes = [ctypes.c_double]

# Definir o tipo de retorno e os tipos de argumentos para a função ceil
lib.teto.restype = ctypes.c_double
lib.teto.argtypes = [ctypes.c_double]

lib.media.restype = ctypes.c_double
lib.media.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.comparar.restype = ctypes.c_double
lib.comparar.argtypes = [ctypes.c_double]

lib.mediana.restype = ctypes.c_double
lib.mediana.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.moda.restype = ctypes.c_double
lib.moda.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.desvio_padrao.restype = ctypes.c_double
lib.desvio_padrao.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.desvio_medio.restype = ctypes.c_double
lib.desvio_medio.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.variancia.restype = ctypes.c_double
lib.variancia.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.comparar.restype = ctypes.c_int
lib.comparar.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

# Define o tipo de retorno e os tipos de argumentos para a função media_ponderada
lib.media_ponderada.restype = ctypes.c_double
lib.media_ponderada.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

lib.media_geometrica.restype = ctypes.c_double
lib.media_geometrica.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.media_quadratica.restype = ctypes.c_double
lib.media_quadratica.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.intervalo_medio.restype = ctypes.c_double
lib.intervalo_medio.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.intervalo_medio_entre_dois_numeros.restype = ctypes.c_double
lib.intervalo_medio_entre_dois_numeros.argtypes = (ctypes.c_double, ctypes.c_double)

lib.amplitude.restype = ctypes.c_double
lib.amplitude.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.quartil_inferior.restype = ctypes.c_double
lib.quartil_inferior.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.quartil_superior.restype = ctypes.c_double
lib.quartil_superior.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.amplitude_interquartil.restype = ctypes.c_double
lib.amplitude_interquartil.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.coeficiente_correlacao.restype = ctypes.c_double
lib.coeficiente_correlacao.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)

# Definição da struct RegressaoLinear
class RegressaoLinear(ctypes.Structure):
    _fields_ = [("a", ctypes.c_double), ("b", ctypes.c_double)]

lib.regressao_linear.restype = RegressaoLinear
lib.regressao_linear.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.coeficiente_variacao.restype = ctypes.c_double
lib.coeficiente_variacao.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.media_harmonica.restype = ctypes.c_double
lib.media_harmonica.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

# Definição da struct Frequencia
class Frequencia(ctypes.Structure):
    _fields_ = [("classe", ctypes.c_double), ("frequencia", ctypes.c_double)]

lib.distribuicao_frequencia.restype = ctypes.POINTER(Frequencia)
lib.distribuicao_frequencia.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int)

lib.intervalo_confianca.restype = ctypes.c_double
lib.intervalo_confianca.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double)


lib.coeficiente_assimetria.restype = ctypes.c_double
lib.coeficiente_assimetria.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.curtose.restype = ctypes.c_double
lib.curtose.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)

lib.coeficiente_correlacao_pearson.restype = ctypes.c_double
lib.coeficiente_correlacao_pearson.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)

# Função para realizar o Teste t
lib.teste_t.restype = ctypes.c_int
lib.teste_t.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int)

# Função para realizar o Teste de Qui-Quadrado
lib.teste_qui_quadrado.restype = ctypes.c_int
lib.teste_qui_quadrado.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int)

# Função para realizar a Análise de Variância (ANOVA)
lib.analise_variancia.restype = ctypes.c_int
lib.analise_variancia.argtypes = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int), ctypes.c_int)


# Função para calcular o fatorial de um número inteiro
def fatorial(n):
    try:
         return lib.factoriall(n)
    except Exception as e:
        return e

# Função para calcular a potência de um número inteiro
def potencia(base, exponent):
    try:
        return lib.exponencial(base, exponent)
    except Exception as e:
        return e

# Função para calcular o máximo entre dois números inteiros
def valor_maximo(a, b):
    try:
       return lib.maximo(a, b)
    except Exception as e:
        return e
      
# Função para calcular o mínimo entre dois números inteiros
def valor_minimo(a, b):
    try:
        return lib.minimo(a, b)
    except Exception as e:
        return e

# Função para calcular a raiz quadrada de um número
def raiz_quadrada(num):
    try:
        return lib.raiz_quadrada(num)
    except Exception as e:
        return e

# Função para calcular o seno de um ângulo em radianos
def seno(angle):
    try:
        return lib.seno(angle)
    except Exception as e:
        return e

# Função para calcular o cosseno de um ângulo em radianos
def cosseno(angle):
    try:
        return lib.cosseno(angle)
    except Exception as e:
        return e

# Função para calcular a tangente de um ângulo em radianos
def tangente(angle):
    try:
        return lib.tangente(angle)
    except Exception as e:
        return e

# Função para calcular o logaritmo natural de um número
def logaritmo_natural(num):
    try:
        return lib.logaritmo_natural(num)
    except Exception as e:
        return e

# Função para calcular o logaritmo na base 10 de um número
def logaritmo_base10(num):
    try:
       return lib.log_base_10(num)
    except Exception as e:
        return e

# Função para calcular o cosseno hiperbólico de um número
def cosseno_hiperbolico(num):
    try:
        return lib.cosseno_hiperbolica(num)
    except Exception as e:
        return e

# Função para calcular o seno hiperbólico de um número
def seno_hiperbolico(num):
    try:
        return lib.seno_hiperbolica(num)
    except Exception as e:
        return e

# Função para calcular a tangente hiperbólica de um número
def tangente_hiperbolica(num):
    try:
        return lib.tanh(num)
    except Exception as e:
        return e

# Função para calcular o arco cosseno de um número
def arco_cosseno(num):
    try:
        return lib.arco_cossen(num)
    except Exception as e:
        return e

# Função para calcular o arco seno de um número
def arco_seno(num):
    try:
        return lib.arco_sen(num)
    except Exception as e:
        return e

# Função para calcular o arco tangente de um número
def arco_tangente(num):
    try:
        return lib.arco_tang(num)
    except Exception as e:
        return e

# Função para calcular o arco tangente de um número com dois argumentos (y, x)
def arco_tangente2(y, x):
    try:
        return lib.arco_tang2(y, x)
    except Exception as e:
        return e

# Função para calcular a exponencial de um número
def exponencial(num):
    try:
        return lib.exponencial(num)
    except Exception as e:
        return e

# Função para calcular o logaritmo natural de um número + 1
def logaritmo_natural_mais_1(num):
    try:
        return lib.log_natural_mais_um(num)
    except Exception as e:
        return e

# Função para calcular o valor absoluto de um número
def modulo(num):
    try:
        return lib.modulo(num)
    except Exception as e:
        return e

# Função para calcular o logaritmo na base 2 de um número
def logaritmo_base2(num):
    try:
        return lib.log_na_base2(num)
    except Exception as e:
        return e

# Função para calcular o piso de um número
def piso(num):
    try:
        return lib.piso(num)
    except Exception as e:
        return e

# Função para calcular o arredondamento de um número para o inteiro mais próximo
def arredondamento(num):
    try:
        return lib.arredonda(num)
    except Exception as e:
        return e

# Função para calcular o teto de um número
def teto_do_numero(num):
    try:
        return lib.teto(num)
    except Exception as e:
        return e
    
def equacaoPrimeiroGrauEx(a, b, c):
    try:
        if a == 0:
            return 0
        else:
            x = (c - b) /a
            sinal = '+' if b >= 0 else ''
            expl= f"{a}x {sinal}{b} = {c}\n{b} vai trocar de lado e vai no lado do {c}\nmais vai trocar de sinal\nvai ficar {a}x = {c} - ({sinal}{b})\n{a}x = {c-b}\nx = {c-b}/{a}\nx = {x}"
            return f"{a}x {sinal}{b} = {c}  (x: {x})\n--EXPLICAÇÃO--\n{expl}"
    except Exception as e:
        return e
    
def equacaoSegundoGrauEx(a, b, c):
    if a == 0:
        return "A equação não é do segundo grau."

    delta = b**2 - 4*a*c

    if delta < 0:
        return "A equação não possui raízes reais."
    elif delta == 0:
        x = -b / (2*a)
        return f"A equação possui uma raiz real: x = {x}"
    else:
        sinalb = '+' if b >=0 else ''
        sinalc = '+' if c >=0 else ''
        x1 = (-b + raiz_quadrada(delta)) / (2*a)
        x2 = (-b - raiz_quadrada(delta)) / (2*a)
        exp = f"delta = {b}² - 4*{a}*{c}\nse a delta é menor que 0, a equação não possui raiz reais\nsenão vai ser:\nx = {sinalb}{b} / (2*{a})\nx1 = ({sinalb}{b} + √{delta} / 2*{a})\nx2 = ({sinalb}{b} - √{delta} / 2*{a})\ne x1 = {x1}, x2 = {x2}"
    
        return f"A equação {a}x² {sinalb}{b}x {sinalc}{c} = 0 possui duas raízes reais: [x1 = {x1}, x2 = {x2}]\n--EXPLICAÇÂO--\n{exp}"


def equacaoPrimeiroGrau(a, b, c):
    try:
        if a == 0:
            return 0
        else:
            x = (c - b) /a
            sinal = '+' if b >= 0 else ''
            return f"{a}x {sinal}{b} = {c}  (x: {x})\n"
    except Exception as e:
        return e
    

def equacaoSegundoGrau(a, b, c):
    try:
        if a == 0:
            return "A equação não é do segundo grau."

        delta = b**2 - 4*a*c

        if delta < 0:
            return "A equação não possui raízes reais."
        elif delta == 0:
            x = -b / (2*a)
            return f"A equação possui uma raiz real: x = {x}"
        else:
            sinalb = '+' if b >=0 else ''
            sinalc = '+' if c >=0 else ''
            x1 = (-b + raiz_quadrada(delta)) / (2*a)
            x2 = (-b - raiz_quadrada(delta)) / (2*a)
        
            return f" [x1 = {x1}, x2 = {x2}]\n"
    except Exception as e:
        return e

def media(*args):
    try:
        arr = (ctypes.c_double * len(args))(*args)
        return f"{lib.media(arr, len(args)):.2f}"
    except Exception as e:
        return e
    

def mediana(*args):
    try:
        arr = (ctypes.c_double * len(args))(*args)
        return f"{lib.mediana(arr, len(args)):.2f}"
    except Exception as e:
        return e
    

def moda(*args):
    # Converte a lista Python para um array C
    array_c = (ctypes.c_double * len(args))(*args)

    # Chama a função moda da biblioteca C
    result = lib.moda(array_c, len(args))
    
    return f"{result:.1f}"

def desvio_padrao(*args):

    array_c = (ctypes.c_double * len(args))(*args)

    result = lib.desvio_padrao(array_c, len(args))

    return f"{result:.2f}"

def desvio_medio(*args):
    array_c = (ctypes.c_double * len(args))(*args)

    result = lib.desvio_medio(array_c, len(args))

    return f"{result:.2f}"


def variancia(*args):
    array_c = (ctypes.c_double * len(args))(*args)

    result = lib.variancia(array_c, len(args))

    return f"{result:.2f}"


def comparar(a, b):
    # Converte as listas de Python para arrays de C
    a_c = (ctypes.c_double * len(a))(*a)
    b_c = (ctypes.c_double * len(b))(*b)
    # Chama a função em C e retorna o resultado
    return lib.comparar(a_c, b_c)

def media_ponderada(valores, pesos):
    try:
        if len(valores) != len(pesos):
            raise ValueError("Os arrays de valores e pesos devem ter o mesmo tamanho.")
        
        # Chama a função media_ponderada em C
        resultado = lib.media_ponderada((ctypes.c_double * len(valores))(*valores),
                                            (ctypes.c_double * len(pesos))(*pesos),
                                            len(valores))
        
        return resultado
    except Exception as e:
        return e

def media_geometrica(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.media_geometrica(array_c, size)

# Função para calcular a média quadrática de um array de números
def media_quadratica(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.media_quadratica(array_c, size)

# Função para calcular o intervalo médio de um array de números
def intervalo_medio(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.intervalo_medio(array_c, size)

# Função para calcular o intervalo médio entre dois números
def intervalo_medio_entre_dois_numeros(a, b):
    return lib.intervalo_medio_entre_dois_numeros(a, b)

# Função para calcular a amplitude de um array de números
def amplitude(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.amplitude(array_c, size)

# Função para calcular o quartil inferior de um array de números
def quartil_inferior(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.quartil_inferior(array_c, size)

# Função para calcular o quartil superior de um array de números
def quartil_superior(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.quartil_superior(array_c, size)

# Função para calcular o IQR (Amplitude interquartil) de um array de números
def amplitude_interquartil(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.amplitude_interquartil(array_c, size)

# Função para calcular o coeficiente de correlação entre dois arrays de números
def coeficiente_correlacao(x, y):
    size = len(x)
    x_c = (ctypes.c_double * size)(*x)
    y_c = (ctypes.c_double * size)(*y)
    return lib.coeficiente_correlacao(x_c, y_c, size)

# Função para calcular a regressão linear entre dois arrays de números
def regressao_linear(x, y):
    size = len(x)
    x_c = (ctypes.c_double * size)(*x)
    y_c = (ctypes.c_double * size)(*y)
    result = lib.regressao_linear(x_c, y_c, size)
    return result.a, result.b

# Função para calcular o coeficiente de variação de um array de números
def coeficiente_variacao(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.coeficiente_variacao(array_c, size)

# Função para calcular a média harmônica de um array de números
def media_harmonica(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.media_harmonica(array_c, size)

# Função para calcular a distribuição de frequência em intervalos de um array de números
def distribuicao_frequencia(dados, num_classes):
    size = len(dados)
    dados_c = (ctypes.c_double * size)(*dados)
    frequencias_c = lib.distribuicao_frequencia(dados_c, size, num_classes)
    frequencias_py = [(frequencias_c[i].classe, frequencias_c[i].frequencia) for i in range(num_classes)]
    return frequencias_py

# Função para calcular o intervalo de confiança de um array de números
def intervalo_confianca(dados, nivel_confianca):
    # Converta a lista de números em um array do NumPy
    amostra_c = np.array(dados, dtype=np.double)

    # Chame a função C passando o array de double como argumento
    resultado_intervalo = lib.intervalo_confianca(amostra_c.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(amostra_c), nivel_confianca)

    # Imprima o resultado ou faça o que desejar com ele
    return resultado_intervalo

# Função para calcular o coeficiente de assimetria de um array de números
def coeficiente_assimetria(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.coeficiente_assimetria(array_c, size)

# Função para calcular a curtose de um array de números
def curtose(*args):
    size = len(args)
    array_c = (ctypes.c_double * size)(*args)
    return lib.curtose(array_c, size)

# Função para calcular o coeficiente de correlação de Pearson entre dois arrays de números
def coeficiente_correlacao_pearson(x, y):
    size = len(x)
    x_c = (ctypes.c_double * size)(*x)
    y_c = (ctypes.c_double * size)(*y)
    return lib.coeficiente_correlacao_pearson(x_c, y_c, size)

# Função para realizar o Teste t em uma amostra e verificar a hipótese nula
def teste_t(amostra1, amostra2):
    size1 = len(amostra1)
    size2 = len(amostra2)
    amostra1_c = (ctypes.c_double * size1)(*amostra1)
    amostra2_c = (ctypes.c_double * size2)(*amostra2)
    return lib.teste_t(amostra1_c, size1, amostra2_c, size2)

# Função para realizar o Teste de Qui-Quadrado em uma tabela de frequência observada e esperada
def teste_qui_quadrado(freq_obs, freq_esp):
    size = len(freq_obs)
    freq_obs_c = (ctypes.c_double * size)(*freq_obs)
    freq_esp_c = (ctypes.c_double * size)(*freq_esp)
    return lib.teste_qui_quadrado(freq_obs_c, freq_esp_c, size)

# Função para realizar a Análise de Variância (ANOVA) em um conjunto de amostras
def analise_variancia(*args):
    num_amostras = len(args)
    sizes = [len(amostra) for amostra in args]
    amostras_c = [(ctypes.c_double * len(amostra))(*amostra) for amostra in args]
    array_c = (ctypes.POINTER(ctypes.c_double) * num_amostras)(*amostras_c)
    sizes_c = (ctypes.c_int * num_amostras)(*sizes)
    return f"{lib.analise_variancia(array_c, sizes_c, num_amostras):.2f}"

