Descrição para o PyPI:

# Anybomt - Biblioteca C para Estatística

A biblioteca **Anybomt** é uma implementação em C de diversas funções estatísticas e matemáticas, projetada para ser usada em conjunto com o Python. Ela oferece um conjunto de funções eficientes para cálculos estatísticos, como média, mediana, moda, desvio padrão, regressão linear, coeficiente de correlação e muito mais.

A biblioteca possui uma interface C que pode ser carregada no Python usando a biblioteca **ctypes**, permitindo que você utilize todas as funcionalidades de forma simples e rápida.

## Principais Funções Disponíveis

A **Anybomt** oferece um conjunto de funções estatísticas e matemáticas essenciais para análises e cálculos numéricos. Algumas das principais funções disponíveis incluem:

- **Média**: `media(*args)` - Calcula a média dos valores passados como argumentos.
- **Mediana**: `mediana(*args)` - Calcula a mediana dos valores passados como argumentos.
- **Moda**: `moda(*args)` - Calcula a moda dos valores passados como argumentos.
- **Desvio Padrão**: `desvio_padrao(*args)` - Calcula o desvio padrão dos valores passados como argumentos.
- **Regressão Linear**: `regressao_linear(x, y)` - Calcula a regressão linear entre dois arrays de números `x` e `y`.
- **Coeficiente de Correlação**: `coeficiente_correlacao(x, y)` - Calcula o coeficiente de correlação entre dois arrays de números `x` e `y`.
- **Intervalo de Confiança**: `intervalo_confianca(dados, nivel_confianca)` - Calcula o intervalo de confiança para uma amostra de dados e um determinado nível de confiança.
- **Coeficiente de Assimetria**: `coeficiente_assimetria(*args)` - Calcula o coeficiente de assimetria dos valores passados como argumentos.
- **Curtose**: `curtose(*args)` - Calcula a curtose dos valores passados como argumentos.
- **Análise de Variância (ANOVA)**: `analise_variancia(*args)` - Realiza a análise de variância para um conjunto de amostras.

## Como Instalar

Para instalar a biblioteca **Anybomt**, você pode usar o gerenciador de pacotes `pip`:

```bash
pip install anybomt
```

## Como Usar

Após a instalação, você pode importar as funções da biblioteca em seu código Python:

```python
import anybomt

# Exemplo: calcular a média de um conjunto de valores
dados = [10.2, 12.5, 15.8, 20.1, 18.6]
media = anybomt.media(*dados)
print(f"Média: {media}")

# Exemplo: calcular a regressão linear entre dois arrays de números
x = [1.0, 2.0, 3.0, 4.0, 5.0]
y = [2.5, 3.8, 4.9, 6.2, 7.6]
a, b = anybomt.regressao_linear(x, y)
print(f"Coeficiente 'a': {a}")
print(f"Coeficiente 'b': {b}")
```

## Nota

A biblioteca **Anybomt** foi desenvolvida em C e possui uma interface Python usando a biblioteca `ctypes`. É importante garantir que a biblioteca C (`anybomt.so`) esteja disponível no diretório correto antes de executar os códigos Python.

## Referências

Para mais informações e detalhes sobre cada função disponível na biblioteca **Anybomt**, consulte a documentação oficial.

## Licença

A biblioteca **Anybomt** é distribuída sob a Licença MIT. Você pode encontrar mais informações na licença incluída no pacote.