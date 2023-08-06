import numpy as np
from scipy import stats
import statistics
import math

# Função para calcular o fatorial de um número inteiro
def fatorial(n):
    try:
         return math.factorial(n)
    except Exception as e:
        return e

# Função para calcular a potência de um número inteiro
def potencia(base, exponent):
    try:
        return base ** exponent
    except Exception as e:
        return e

# Função para calcular o máximo entre dois números inteiros
def valor_maximo(a, b):
    try:
        return max(a, b)
    except Exception as e:
        return e
      
# Função para calcular o mínimo entre dois números inteiros
def valor_minimo(a, b):
    try:
        return min(a, b)
    except Exception as e:
        return e

# Função para calcular a raiz quadrada de um número
def raiz_quadrada(num):
    try:
        return math.sqrt(num)
    except Exception as e:
        return e
    
def somar(*args):
    try:
        return sum(args)
    except Exception as e:
        return e

# Classe Trigonometria
class Trigonometria:
    # Função para calcular o seno de um ângulo em radianos
    def seno(angle):
        try:
            return math.sin(angle)
        except Exception as e:
            return e

    # Função para calcular o cosseno de um ângulo em radianos
    def cosseno(angle):
        try:
            return math.cos(angle)
        except Exception as e:
            return e

    # Função para calcular a tangente de um ângulo em radianos
    def tangente(angle):
        try:
            return math.tan(angle)
        except Exception as e:
            return e

    # Função para calcular o cosseno hiperbólico de um número
    def cosseno_hiperbolico(num):
        try:
            return math.cosh(num)
        except Exception as e:
            return e

    # Função para calcular o seno hiperbólico de um número
    def seno_hiperbolico(num):
        try:
            return math.sinh(num)
        except Exception as e:
            return e

    # Função para calcular a tangente hiperbólica de um número
    def tangente_hiperbolica(num):
        try:
            return math.tanh(num)
        except Exception as e:
            return e

    # Função para calcular o arco cosseno de um número
    def arco_cosseno(num):
        try:
            return math.acos(num)
        except Exception as e:
            return e

    # Função para calcular o arco seno de um número
    def arco_seno(num):
        try:
            return math.asin(num)
        except Exception as e:
            return e

    # Função para calcular o arco tangente de um número
    def arco_tangente(num):
        try:
            return math.atan(num)
        except Exception as e:
            return e

    # Função para calcular o arco tangente de um número com dois argumentos (y, x)
    def arco_tangente2(y, x):
        try:
            return math.atan2(y, x)
        except Exception as e:
            return e

# Função para calcular o logaritmo natural de um número
def logaritmo_natural(num):
    try:
        return math.log(num)
    except Exception as e:
        return e

# Função para calcular o logaritmo na base 10 de um número
def logaritmo_base10(num):
    try:
        return math.log10(num)
    except Exception as e:
        return e

# Função para calcular a exponencial de um número
def exponencial(num):
    try:
        return math.exp(num)
    except Exception as e:
        return e
    
def PI():
    try:
        from mpmath import mp
        mp.dps = 20
        pi_value = mp.pi
        return pi_value
    except Exception as e:
        return e

def PI_Long():
    try:
        from mpmath import mp
        mp.dps = 200
        pi_value = mp.pi
        return pi_value
    except Exception as e: return e

def E_long():
    try:
        from mpmath import mp
        mp.dps = 200
        euler_value = mp.e
        return euler_value
    except Exception as e:
        return e

def E():
    try:
        from mpmath import mp
        # Define a precisão para 200 casas decimais
        mp.dps = 20

        # Obtém o valor de e com 200 casas decimais
        euler_value = mp.e

        return euler_value
    except Exception as e: return e


def Num_Au_long():
    try:
        from mpmath import mp
        mp.dps = 200
        phi = (1 + mp.sqrt(5)) / 2
        return phi
    except Exception as e: return e

def Num_Au():
    try:
        from mpmath import mp
        mp.dps = 20
        phi = (1 + mp.sqrt(5)) / 2
        return phi
    except Exception as e: return e



def Num_catalan():
    try:
        from mpmath import mp
        mp.dps = 20
        catalan = mp.catalan
        return catalan
    except Exception as e: return e

def Num_catalan_long():
    try:
        from mpmath import mp
        mp.dps = 200
        catalan = mp.catalan
        return catalan
    except Exception as e: return e


def feigenbaum_delta_long():
    try:
        from mpmath import mp
        mp.dps = 200
        feigenbaum_delta = 4.669201609102990671853203821578
        return feigenbaum_delta
    except Exception as e: return e

def feigenbaum_delta():
    try:
        from mpmath import mp
        mp.dps = 20
        feigenbaum_delta = 4.669201609102990671853203821578
        return feigenbaum_delta
    except Exception as e: return e


def feigenbaum_alfa():
   try:
        from mpmath import mp
        mp.dps = 20
        feigenbaum_alfa = 2.502907875095892822283902873218
        return feigenbaum_alfa
   except Exception as e: return e


def feigenbaum_alfa_long():
   try:
        from mpmath import mp
        mp.dps = 200
        feigenbaum_alfa = 2.502907875095892822283902873218
        return feigenbaum_alfa
   except Exception as e: return e


def Constante_de_Brun():
    from mpmath import mp
    mp.dps = 200
    brun = 1.9021605823
    return brun

# Função para calcular o logaritmo natural de um número + 1
def logaritmo_natural_mais_1(num):
    try:
        return math.log1p(num)
    except Exception as e:
        return e

# Função para calcular o valor absoluto de um número
def modulo(num):
    try:
        return abs(num)
    except Exception as e:
        return e

# Função para calcular o logaritmo na base 2 de um número
def logaritmo_base2(num):
    try:
        return math.log2(num)
    except Exception as e:
        return e

# Função para calcular o piso de um número
def piso(num):
    try:
        return math.floor(num)
    except Exception as e:
        return e

# Função para calcular o arredondamento de um número para o inteiro mais próximo
def arredondamento(num):
    try:
        return round(num)
    except Exception as e:
        return e

# Função para calcular o teto de um número
def teto_do_numero(num):
    try:
        return math.ceil(num)
    except Exception as e:
        return e

def equacaoPrimeiroGrauEx(a, b, c):
    try:
        if a == 0:
            return "A equação não é do primeiro grau."
        else:
             x = (c - b) /a
             sinal = '+' if b >= 0 else ''
             expl= f"{a}x {sinal}{b} = {c}\n{b} vai trocar de lado e vai no lado do {c}\nmais vai trocar de sinal\nvai ficar {a}x = {c} - ({sinal}{b})\n{a}x = {c-b}\nx = {c-b}/{a}\nx = {x}"
             return f"{a}x {sinal}{b} = {c}  (x: {x})\n--EXPLICAÇÃO--\n{expl}"
    except Exception as e:
        return e

def equacaoSegundoGrauEx(a, b, c):
    try:
        if a == 0:
            return "A equação não é do segundo grau."

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return "A equação não possui raízes reais."
        elif delta == 0:
            x = -b / (2 * a)
            return f"A equação possui uma raiz real: x = {x}"
        else:
             sinalb = '+' if b >=0 else ''
             sinalc = '+' if c >=0 else ''
             x1 = (-b + math.sqrt(delta)) / (2*a)
             x2 = (-b - math.sqrt(delta)) / (2*a)
             exp = f"delta = {b}² - 4*{a}*{c}\nse a delta é menor que 0, a equação não possui raiz reais\nsenão vai ser:\nx = {sinalb}{b} / (2*{a})\nx1 = ({sinalb}{b} + √{delta} / 2*{a})\nx2 = ({sinalb}{b} - √{delta} / 2*{a})\ne x1 = {x1}, x2 = {x2}"
        
             return f"A equação {a}x² {sinalb}{b}x {sinalc}{c} = 0 possui duas raízes reais: [x1 = {x1}, x2 = {x2}]\n--EXPLICAÇÂO--\n{exp}"
    except Exception as e:
        return e

def equacaoPrimeiroGrau(a, b, c):
    try:
        if a == 0:
            return "A equação não é do primeiro grau."
        else:
            x = (c - b) / a
            return x
    except Exception as e:
        return e

def equacaoSegundoGrau(a, b, c):
    try:
        if a == 0:
            return "A equação não é do segundo grau."

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return "A equação não possui raízes reais."
        elif delta == 0:
            x = -b / (2 * a)
            return f"A equação possui uma raiz real: x = {x}"
        else:
            x1 = (-b + raiz_quadrada(delta)) / (2 * a)
            x2 = (-b - raiz_quadrada(delta)) / (2 * a)
            return f"A equação possui duas raízes reais: x1 = {x1}, x2 = {x2}"
    except Exception as e:
        return e

class Estatistica:
    def media(*args):
        try:
            return sum(args) / len(args)
        except Exception as e:
            return e

    def mediana(*args):
        try:
            sorted_args = sorted(args)
            n = len(sorted_args)
            if n % 2 == 0:
                return (sorted_args[n // 2 - 1] + sorted_args[n // 2]) / 2
            else:
                return sorted_args[n // 2]
        except Exception as e:
            return e

    def moda(*args):
        try:
            counter = {}
            for num in args:
                if num in counter:
                    counter[num] += 1
                else:
                    counter[num] = 1
            max_count = max(counter.values())
            return [num for num, count in counter.items() if count == max_count]
        except Exception as e:
            return e

    def desvio_padrao(self,*args):
        try:
            n = len(args)
            if n == 0:
                raise ValueError("A lista de valores não pode ser vazia.")
            mean = sum(args) / n
            squared_diff_sum = sum((x - mean) ** 2 for x in args)
            variance = squared_diff_sum / n
            return math.sqrt(variance)
        except Exception as e:
            return e

    def desvio_medio(*args):
        try:
            n = len(args)
            if n == 0:
                raise ValueError("A lista de valores não pode ser vazia.")
            return sum(abs(x - sum(args) / n) for x in args) / n
        except Exception as e:
            return e

    def variancia(*args):
        try:
            n = len(args)
            if n == 0:
                raise ValueError("A lista de valores não pode ser vazia.")
            mean = sum(args) / n
            squared_diff_sum = sum((x - mean) ** 2 for x in args)
            return squared_diff_sum / n
        except Exception as e:
            return e

    def comparar(a, b):
        try:
            if len(a) != len(b):
                raise ValueError("As listas de valores devem ter o mesmo tamanho.")
            n = len(a)
            diff_sum = sum(abs(a[i] - b[i]) for i in range(n))
            return diff_sum / n
        except Exception as e:
            return e

    def media_ponderada(valores, pesos):
        try:
            if len(valores) != len(pesos):
                raise ValueError("As listas de valores e pesos devem ter o mesmo tamanho.")
            weighted_sum = sum(valores[i] * pesos[i] for i in range(len(valores)))
            sum_of_weights = sum(pesos)
            return weighted_sum / sum_of_weights
        except Exception as e:
            return e

    def media_geometrica(*args):
        try:
            product = 1
            for num in args:
                product *= num
            return product ** (1 / len(args))
        except Exception as e:
            return e

    def media_quadratica(*args):
        try:
            squared_sum = sum(x ** 2 for x in args)
            return math.sqrt(squared_sum / len(args))
        except Exception as e:
            return e

    def intervalo_medio(*args):
        try:
            sorted_args = sorted(args)
            return (sorted_args[0] + sorted_args[-1]) / 2
        except Exception as e:
            return e

    def intervalo_medio_entre_dois_numeros(a, b):
        try:
            return (a + b) / 2
        except Exception as e:
            return e

    def amplitude(*args):
        try:
            return max(args) - min(args)
        except Exception as e:
            return e

    def quartis(self, *args):
        try:
            q1 = statistics.percentile(args, 25)
            q2 = statistics.median(args)
            q3 = statistics.percentile(args, 75)
            return q1, q2, q3
        except Exception as e:
            return e

    def amplitude_interquartil(self, *args):
        try:
            q1, _, q3 = self.quartis(*args)
            return q3 - q1
        except Exception as e:
            return e

    

    def coeficiente_correlacao(x, y):
        try:
            if len(x) != len(y):
                raise ValueError("As listas de valores devem ter o mesmo tamanho.")
            n = len(x)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x = sum(x)
            sum_y = sum(y)
            sum_x_squared = sum(x[i] ** 2 for i in range(n))
            sum_y_squared = sum(y[i] ** 2 for i in range(n))
            numerator = n * sum_xy - sum_x * sum_y
            denominator = math.sqrt((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2))
            return numerator / denominator
        except Exception as e:
            return e

    def regressao_linear(x, y):
        try:
            if len(x) != len(y):
                raise ValueError("As listas de valores devem ter o mesmo tamanho.")
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_x_squared = sum(x[i] ** 2 for i in range(n))
            sum_xy = sum(x[i] * y[i] for i in range(n))

            a = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
            b = (sum_y - a * sum_x) / n

            return a, b
        except Exception as e:
            return e

    def coeficiente_variacao(*args):
        try:
            mean = statistics.mean(args)
            std_deviation = statistics.stdev(args)
            return (std_deviation / mean) * 100
        except Exception as e:
            return e

    def media_harmonica(*args):
        try:
            reciprocal_sum = sum(1 / num for num in args)
            return len(args) / reciprocal_sum
        except Exception as e:
            return e
        
    def distribuicao_frequencia(dados, num_classes):
        try:
            sorted_data = sorted(dados)
            min_value = sorted_data[0]
            max_value = sorted_data[-1]
            range_value = max_value - min_value
            class_width = range_value / num_classes

            frequency_table = {}
            for i in range(num_classes):
                lower_bound = min_value + i * class_width
                upper_bound = lower_bound + class_width
                frequency_table[(lower_bound, upper_bound)] = 0

            for value in sorted_data:
                for interval in frequency_table.keys():
                    lower_bound, upper_bound = interval
                    if lower_bound <= value < upper_bound:
                        frequency_table[interval] += 1
                        break

            return frequency_table
        except Exception as e:
            return e

    def intervalo_confianca(dados, nivel_confianca):
        try:
            n = len(dados)
            mean = statistics.mean(dados)
            std_deviation = statistics.stdev(dados)
            t_value = stats.t.ppf((1 + nivel_confianca) / 2, n - 1)
            margin_of_error = t_value * (std_deviation / math.sqrt(n))
            lower_bound = mean - margin_of_error
            upper_bound = mean + margin_of_error
            return lower_bound, upper_bound
        except Exception as e:
            return e

    def coeficiente_assimetria(*args):
        try:
            n = len(args)
            mean = sum(args) / n
            variance = sum((x - mean) ** 2 for x in args) / n
            std_deviation = math.sqrt(variance)
            cubed_deviations = [(num - mean) ** 3 for num in args]
            sum_cubed_deviations = sum(cubed_deviations)
            skewness = (sum_cubed_deviations / (n * std_deviation ** 3))
            return skewness
        except Exception as e:
            return e


    def curtose(*args):
        try:
            n = len(args)
            mean = sum(args) / n
            variance = sum((x - mean) ** 2 for x in args) / n
            fourth_power_deviations = [(num - mean) ** 4 for num in args]
            sum_fourth_power_deviations = sum(fourth_power_deviations)
            kurtosis = (sum_fourth_power_deviations / (n * variance ** 2)) - 3
            return kurtosis
        except Exception as e:
            return e


    def coeficiente_correlacao_pearson(x, y):
        try:
            if len(x) != len(y):
                raise ValueError("As listas de valores devem ter o mesmo tamanho.")
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_x_squared = sum(x[i] ** 2 for i in range(n))
            sum_y_squared = sum(y[i] ** 2 for i in range(n))
            sum_xy = sum(x[i] * y[i] for i in range(n))

            numerator = n * sum_xy - sum_x * sum_y
            denominator = math.sqrt((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2))
            pearson_correlation = numerator / denominator
            return pearson_correlation
        except Exception as e:
            return e

   

    def teste_t(amostra1, amostra2):
        try:
            if len(amostra1) != len(amostra2):
                raise ValueError("As amostras devem ter o mesmo tamanho.")

            n1 = len(amostra1)
            n2 = len(amostra2)

            mean1 = sum(amostra1) / n1
            mean2 = sum(amostra2) / n2

            variance1 = sum((x - mean1) ** 2 for x in amostra1) / (n1 - 1)
            variance2 = sum((x - mean2) ** 2 for x in amostra2) / (n2 - 1)

            pooled_variance = ((n1 - 1) * variance1 + (n2 - 1) * variance2) / (n1 + n2 - 2)
            pooled_std_deviation = math.sqrt(pooled_variance)

            t_value = (mean1 - mean2) / (pooled_std_deviation * math.sqrt(1 / n1 + 1 / n2))
            return t_value
        except Exception as e:
            return e


    def teste_qui_quadrado(freq_obs, freq_esp):
        try:
            if len(freq_obs) != len(freq_esp):
                raise ValueError("As tabelas de frequência devem ter o mesmo tamanho.")
            n = len(freq_obs)
            chi_squared = sum((freq_obs[i] - freq_esp[i]) ** 2 / freq_esp[i] for i in range(n))
            return chi_squared
        except Exception as e:
            return e

    def analise_variancia(*args):
        try:
            num_amostras = len(args)
            sizes = [len(amostra) for amostra in args]
            grand_mean = sum(sum(amostra) for amostra in args) / sum(sizes)
            total_ss = sum(sum((x - grand_mean) ** 2 for x in amostra) for amostra in args)
            df_total = sum(size - 1 for size in sizes)
            df_between = num_amostras - 1
            df_within = df_total - df_between
            ss_between = sum(size * (sum(amostra) / size - grand_mean) ** 2 for size, amostra in zip(sizes, args))
            ms_between = ss_between / df_between
            ss_within = total_ss - ss_between
            ms_within = ss_within / df_within
            f_value = ms_between / ms_within
            return f_value
        except Exception as e:
            return e
        
    

    def teste_normalidade(amostra, alpha=0.05):
        from scipy.stats import chi2
        n = len(amostra)
        mean = np.mean(amostra)
        std_deviation = np.std(amostra, ddof=1)
        z_score = (amostra - mean) / std_deviation
        squared_z_score = z_score ** 2
        chi_square = np.sum(squared_z_score)
        critical_value = chi2.ppf(1 - alpha, df=n - 1)

        return chi_square <= critical_value
    
    def teste_homogeneidade(*grupos, alpha=0.05):
        from scipy.stats import f
        """
        Testa a homogeneidade de variâncias entre diferentes grupos.

        Parâmetros:
        *grupos (list): Cada argumento é uma lista contendo os valores de um grupo.
        alpha (float): Nível de significância. Valor padrão é 0.05.

        Retorna:
        bool: True se as variâncias são homogêneas entre os grupos, False caso contrário.
        """
        n_grupos = len(grupos)
        n_total = np.sum([len(grupo) for grupo in grupos])
        mean_total = np.mean(np.concatenate(grupos))
        squared_deviations_total = np.sum([(x - mean_total) ** 2 for grupo in grupos for x in grupo])
        squared_deviations_between = np.sum([len(grupo) * (np.mean(grupo) - mean_total) ** 2 for grupo in grupos])

        df_between = n_grupos - 1
        df_within = n_total - n_grupos

        mean_squared_deviations_between = squared_deviations_between / df_between
        mean_squared_deviations_within = squared_deviations_total / df_within

        f_statistic = mean_squared_deviations_between / mean_squared_deviations_within
        critical_value = f.ppf(1 - alpha, dfn=df_between, dfd=df_within)

        return f_statistic <= critical_value

class Calculo:
   

    def derivada(expressao, variavel):
        from sympy import symbols, diff
        x = symbols(variavel)
        return diff(expressao, x)


    def integral_definida(expressao, variavel, limite_inferior, limite_superior):
        from sympy import symbols, integrate
        x = symbols(variavel)
        return integrate(expressao, (x, limite_inferior, limite_superior))



    

    def integral_indefinida(expressao, variavel):
        from sympy import symbols, integrate
        x = symbols(variavel)
        return integrate(expressao, x)


    
    def limite(expressao, variavel, ponto):
        from sympy import symbols, limit
        x = symbols(variavel)
        return limit(expressao, x, ponto)


    def derivada_parcial(expressao, variaveis):
        from sympy import symbols, diff
        vars = symbols(variaveis)
        return diff(expressao, *vars)

    
    def laplace(expressao, variavel, s):
        from sympy import symbols, laplace_transform
        t = symbols(variavel)
        return laplace_transform(expressao, t, s)


    

    def inversa_laplace(expressao, s, t):
        from sympy import symbols, inverse_laplace_transform
        t = symbols(t)
        return inverse_laplace_transform(expressao, s, t)



   
    def transformada_fourier(expressao, variavel, w):
        from sympy import symbols, fourier_transform
        t = symbols(variavel)
        return fourier_transform(expressao, t, w)

    

    def inversa_fourier(expressao, w, t):
        from sympy import symbols, inverse_fourier_transform
        w = symbols(w)
        return inverse_fourier_transform(expressao, w, t)



    

    def soma_riemann(expressao, variavel, limite_inferior, limite_superior, numero_particoes):
        from sympy import symbols, summation
        x = symbols(variavel)
        delta_x = (limite_superior - limite_inferior) / numero_particoes
        pontos = [limite_inferior + i * delta_x for i in range(numero_particoes)]
        return summation(expressao, (x, pontos[0], pontos[-1]), delta_x)



    

    def produto_riemann(expressao, variavel, limite_inferior, limite_superior, numero_particoes):
        from sympy import symbols, product
        x = symbols(variavel)
        delta_x = (limite_superior - limite_inferior) / numero_particoes
        pontos = [limite_inferior + i * delta_x for i in range(numero_particoes)]
        return product(expressao, (x, pontos[0], pontos[-1]), delta_x)


   

    def limite_lateral(expressao, variavel, ponto, lado='right'):
        from sympy import symbols, limit
        x = symbols(variavel)
        return limit(expressao, x, ponto, dir=lado)


    def derivada_numerica_progressiva(expressao, variavel, ponto, h=1e-6):
        from sympy import symbols
        x = symbols(variavel)
        f_x = expressao.subs(x, ponto)
        f_xh = expressao.subs(x, ponto + h)
        return (f_xh - f_x) / h


   

    def derivada_numerica_regressiva(expressao, variavel, ponto, h=1e-6):
        from sympy import symbols
        x = symbols(variavel)
        f_x = expressao.subs(x, ponto)
        f_xh = expressao.subs(x, ponto - h)
        return (f_x - f_xh) / h



    def derivada_numerica_central(expressao, variavel, ponto, h=1e-6):
        from sympy import symbols
        x = symbols(variavel)
        f_xh = expressao.subs(x, ponto + h)
        f_xh2 = expressao.subs(x, ponto - h)
        return (f_xh - f_xh2) / (2 * h)


  
    def integral_numerica_trapezio(expressao, variavel, limite_inferior, limite_superior, numero_particoes):
        from sympy import symbols
        x = symbols(variavel)
        h = (limite_superior - limite_inferior) / numero_particoes
        pontos = [limite_inferior + i * h for i in range(numero_particoes + 1)]
        integral = 0
        for i in range(1, numero_particoes):
            integral += expressao.subs(x, pontos[i])
        integral += (expressao.subs(x, limite_inferior) + expressao.subs(x, limite_superior)) / 2
        integral *= h
        return integral



    def integral_numerica_simpson(expressao, variavel, limite_inferior, limite_superior, numero_particoes):
        from sympy import symbols
        x = symbols(variavel)
        h = (limite_superior - limite_inferior) / numero_particoes
        pontos = [limite_inferior + i * h for i in range(numero_particoes + 1)]
        integral = 0
        for i in range(1, numero_particoes):
            if i % 2 == 0:
                integral += 2 * expressao.subs(x, pontos[i])
            else:
                integral += 4 * expressao.subs(x, pontos[i])
        integral += expressao.subs(x, limite_inferior) + expressao.subs(x, limite_superior)
        integral *= h / 3
        return integral


  
    

    def serie_taylor(expressao, variavel, ponto, ordem):
        from sympy import symbols, series
        x = symbols(variavel)
        return series(expressao, x, x0=ponto, n=ordem).removeO()

    

    def transformada_laplace(expressao, variavel, s):
        from sympy import symbols, laplace_transform
        t = symbols(variavel)
        return laplace_transform(expressao, t, s, noconds=True)


  

    def inversa_transformada_laplace(expressao, variavel, t):
        from sympy import symbols, inverse_laplace_transform
        s = symbols(variavel)
        return inverse_laplace_transform(expressao, s, t)

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("As matrizes devem ter o mesmo tamanho para soma.")
        
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)
    
    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("As matrizes devem ter o mesmo tamanho para subtração.")
        
        result = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = [[self.data[i][j] * other for j in range(self.cols)] for i in range(self.rows)]
        elif isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("O número de colunas da primeira matriz deve ser igual ao número de linhas da segunda matriz para multiplicação.")
            
            result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)]
        else:
            raise TypeError("Multiplicação não suportada entre matriz e outro tipo.")
        
        return Matrix(result)

    def transposta(self):
        result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(result)

    def determinante(self):
        if self.rows != self.cols:
            raise ValueError("O determinante só pode ser calculado para matrizes quadradas.")
        
        return self._determinant_recursive(self.data)

    def _determinant_recursive(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sub_det = self._determinant_recursive(submatrix)
            det += matrix[0][j] * sub_det * (-1 if j % 2 != 0 else 1)

        return det

class AlgebraLinear:
    # Função para multiplicar uma matriz por um escalar
    @staticmethod
    def multiplicar_matriz_por_escalar(matriz, escalar):
        resultado = []
        for linha in matriz:
            nova_linha = [elemento * escalar for elemento in linha]
            resultado.append(nova_linha)
        return resultado

    # Função para dividir uma matriz por um escalar
    @staticmethod
    def dividir_matriz_por_escalar(matriz, escalar):
        if escalar == 0:
            raise ValueError("Não é possível dividir uma matriz por zero.")
        return AlgebraLinear.multiplicar_matriz_por_escalar(matriz, 1 / escalar)

    # Função para multiplicar uma matriz por um vetor
    @staticmethod
    def multiplicar_matriz_por_vetor(matriz, vetor):
        if len(matriz[0]) != len(vetor):
            raise ValueError("O número de colunas da matriz deve ser igual ao tamanho do vetor.")
        resultado = []
        for linha in matriz:
            soma = sum(elemento * vetor[i] for i, elemento in enumerate(linha))
            resultado.append(soma)
        return resultado


    # Função para resolver um sistema de equações lineares utilizando matrizes
    @staticmethod
    def resolver_sistema_linear(coeficientes, constantes):
        import copy
        matriz_coeficientes = copy.deepcopy(coeficientes)
        matriz_constantes = [[float(constante)] for constante in constantes]
        inversa_coeficientes = AlgebraLinear.matriz_inversa(matriz_coeficientes)

        # Multiplicar a matriz inversa pelos vetores constantes corretamente
        solucao = AlgebraLinear.multiplicar_matriz(inversa_coeficientes, matriz_constantes)

        return [f"{item[0]:.2f}" for item in solucao]


    # Função para calcular a matriz inversa
    @staticmethod
    def matriz_inversa(matriz):
        n = len(matriz)
        identidade = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        matriz_aumentada = [linha + identidade[i] for i, linha in enumerate(matriz)]
        for i in range(n):
            pivo = matriz_aumentada[i][i]
            if pivo == 0:
                raise ValueError("A matriz não possui inversa.")
            for j in range(i, n * 2):
                matriz_aumentada[i][j] /= pivo
            for k in range(n):
                if k != i:
                    fator = matriz_aumentada[k][i]
                    for j in range(i, n * 2):
                        matriz_aumentada[k][j] -= fator * matriz_aumentada[i][j]
        matriz_inversa = [linha[n:] for linha in matriz_aumentada]
        return matriz_inversa

    # Função para elevar uma matriz a uma potência inteira
    @staticmethod
    def potencia_matriz(matriz, potencia):
        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada para ser elevada a uma potência.")
        if potencia == 0:
            n = len(matriz)
            return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        if potencia < 0:
            matriz = AlgebraLinear.matriz_inversa(matriz)
            potencia *= -1
        resultado = matriz
        for _ in range(potencia - 1):
            resultado = AlgebraLinear.multiplicar_matriz(resultado, matriz)
        return resultado

    # Função para calcular os autovalores e autovetores de uma matriz
    @staticmethod
    def autovalores_autovetores(matriz):
        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada para calcular os autovalores e autovetores.")
        # Implementação dos cálculos dos autovalores e autovetores (pode ser feito com o método que preferir)

    # Função para realizar a decomposição LU de uma matriz
    @staticmethod
    def decomposicao_lu(matriz):
        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada para realizar a decomposição LU.")
        # Implementação da decomposição LU (pode ser feita com o método que preferir)

    # Função para realizar a decomposição QR de uma matriz
    @staticmethod
    def decomposicao_qr(matriz):
        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada para realizar a decomposição QR.")
        # Implementação da decomposição QR (pode ser feita com o método que preferir)

    # Função para realizar a decomposição de Cholesky de uma matriz simétrica positiva definida
    @staticmethod
    def decomposicao_cholesky(matriz):
        if len(matriz) != len(matriz[0]):
            raise ValueError("A matriz deve ser quadrada para realizar a decomposição de Cholesky.")
        # Implementação da decomposição de Cholesky (pode ser feita com o método que preferir)

    # Função para resolver um sistema de equações lineares usando o método de Gauss-Seidel
    @staticmethod
    def gauss_seidel(coeficientes, constantes, iteracoes=100, precisao=1e-9):
        if len(coeficientes) != len(coeficientes[0]) or len(coeficientes) != len(constantes):
            raise ValueError("As dimensões da matriz de coeficientes e do vetor de constantes devem ser compatíveis.")
        # Implementação do

    @staticmethod
    def interpolar_polinomial(pontos):
        n = len(pontos)
        if n < 2:
            raise ValueError("A interpolação polinomial requer pelo menos 2 pontos.")
        
        # Separa os pontos em listas de x e y
        x, y = zip(*pontos)
        
        # Implementação da interpolação polinomial utilizando o método de Lagrange
        def lagrange_basis(i):
            def basis(x_value):
                result = 1.0
                for j in range(n):
                    if i != j:
                        result *= (x_value - x[j]) / (x[i] - x[j])
                return result
            return basis

        def polynomial_interpolation(x_value):
            interpolation = 0.0
            for i in range(n):
                interpolation += y[i] * lagrange_basis(i)(x_value)
            return interpolation
        
        return polynomial_interpolation

    # Função para ajuste de curvas usando regressão linear
    @staticmethod
    def regressao_linear(pontos):
        n = len(pontos)
        if n < 2:
            raise ValueError("O ajuste de curvas por regressão linear requer pelo menos 2 pontos.")
        
        # Separa os pontos em listas de x e y
        x, y = zip(*pontos)

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        sum_xy = sum(xi * yi for xi, yi in pontos)
        sum_x_squared = sum(xi ** 2 for xi in x)

        slope = (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)
        intercept = mean_y - slope * mean_x

        def linear_regression(x_value):
            return slope * x_value + intercept
        
        return linear_regression

    # Função para calcular integrais definidas usando o método do trapézio
    @staticmethod
    def integracao_trapezio(funcao, limite_inferior, limite_superior, numero_trapezios):
        if numero_trapezios < 1:
            raise ValueError("O número de trapézios deve ser pelo menos 1.")

        h = (limite_superior - limite_inferior) / numero_trapezios
        integral = (funcao(limite_inferior) + funcao(limite_superior)) / 2

        for i in range(1, numero_trapezios):
            x = limite_inferior + i * h
            integral += funcao(x)

        integral *= h
        return integral

    # Função para resolver equações diferenciais usando o método de Euler
    @staticmethod
    def metodo_euler(derivada, condicao_inicial, intervalo, passo):
        t = intervalo[0]
        y = condicao_inicial
        resultado = [(t, y)]
        
        while t + passo <= intervalo[1]:
            y += passo * derivada(t, y)
            t += passo
            resultado.append((t, y))
        
        return resultado
    
    @staticmethod
    def multiplicar_matriz(matriz1, matriz2):
        if len(matriz1[0]) != len(matriz2):
            raise ValueError("O número de colunas da matriz1 deve ser igual ao número de linhas da matriz2.")
        resultado = []
        for i in range(len(matriz1)):
            linha_resultado = []
            for j in range(len(matriz2[0])):
                elemento = sum(matriz1[i][k] * matriz2[k][j] for k in range(len(matriz2)))
                linha_resultado.append(elemento)
            resultado.append(linha_resultado)
        return resultado