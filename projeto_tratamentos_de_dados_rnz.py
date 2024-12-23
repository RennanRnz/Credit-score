# -*- coding: utf-8 -*-
"""Projeto_tratamentos_de_dados.rnz

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VEUm8k9G_rkdLdgqsWT7CI_4JH_cxIaW

*   **TRATAMENTO DE DADOS**

*   Clientes adimplentes (default = 0)
*   Clientes inadimplentes (default = 1)

O atributo de interesse (default) é conhecido como variável resposta ou variável dependente, já os demais atributos que buscam explicá-la (idade, salário etc.) são conhecidas como variáveis explicativas, variáveis independentes ou até variáveis preditoras.
"""

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/develop/dataset/credito.csv', na_values='na')
# Importando o banco de dados que iremos utilizar.

df.head(n=7)

df.shape # retorna uma tupla (qtd linhas, qtd colunas).

df[df['default'] == 0].shape # filtrando a quantidade de clientes adimplentes.

df[df['default'] == 1].shape # filtrando a quantidade de cliente inadimplentes.

qtd_total, _ = df.shape
qtd_adimplentes, _ = df[df['default'] == 0].shape
qtd_inadimplentes, _ = df[df['default'] == 1].shape

print(f"A proporcão clientes adimplentes é de {round(100 * qtd_adimplentes / qtd_total, 2)}%")
print(f"A proporcão clientes inadimplentes é de {round(100 * qtd_inadimplentes / qtd_total, 2)}%")

df.dtypes # tipo de dado de cada coluna (object = string).

df.select_dtypes('object').describe().transpose() # utlizando o describe nas colunas de formado 'object'.

df.drop('id', axis=1).select_dtypes('number').describe().transpose() # utlizando o describe nas colunas de formado 'number'.

df.head() # Verificando quais colunas possuem dados faltantes.

df.isna().any() # Verificando quais colunas possuem dados faltantes.

def stats_dados_faltantes(df: pd.DataFrame) -> None:

  # Definindo uma função para imprimir a quantidade de dados faltantes e sua porcentagem respectivamente.

  stats_dados_faltantes = []
  for col in df.columns:
    if df[col].isna().any():
      qtd, _ = df[df[col].isna()].shape
      total, _ = df.shape
      dict_dados_faltantes = {col: {'quantidade': qtd, "porcentagem": round(100 * qtd/total, 2)}}
      stats_dados_faltantes.append(dict_dados_faltantes)

  for stat in stats_dados_faltantes:
    print(stat)

stats_dados_faltantes(df=df)

stats_dados_faltantes(df=df[df['default'] == 0]) # Dados faltantes dos clientes adimplentes.

stats_dados_faltantes(df=df[df['default'] == 1]) # Dados faltantes dos clientes inadimplentes.

df[['limite_credito', 'valor_transacoes_12m']].dtypes

df[['limite_credito', 'valor_transacoes_12m']].head(n=5)

# Devido ao formato numerico das colunas estar escrito com "." e "," o pyton entende estes dados como string e precisamos transformalos em float.

fn = lambda valor: float(valor.replace(".", "").replace(",", "."))
# Limpando os caracteres indesejados(. e ,).

valores_originais = ['12.691,51', '8.256,96', '3.418,56', '3.313,03', '4.716,22']
valores_limpos = list(map(fn, valores_originais))
# Utilizando a função map para limpar os caracteres indesejados.

print(valores_originais)
print(valores_limpos) # Mostra os valores ja tratados.

df['valor_transacoes_12m'] = df['valor_transacoes_12m'].apply(fn)
# Utilizando a função apply para aplicar a função lambda nas colunas desejadas.

df['limite_credito'] = df['limite_credito'].apply(fn)

df[['limite_credito', 'valor_transacoes_12m']].dtypes
# Colunas transformadas em float.

df.select_dtypes('object').describe().transpose()

df.drop('id', axis=1).select_dtypes('number').describe().transpose()

df.dropna(inplace=True)
# Removendo linhas com dados faltantes(na)

df.shape
# Verificando novamente a quantidade de linhas e colunas(após exclusão de dados faltantes).

df[df['default'] == 0].shape
# Clientes adimplentes.

df[df['default'] == 1].shape
# Cliente inadimplentes.

qtd_total_novo, _ = df.shape
qtd_adimplentes_novo, _ = df[df['default'] == 0].shape
qtd_inadimplentes_novo, _ = df[df['default'] == 1].shape

print(f"A proporcão adimplentes ativos é de {round(100 * qtd_adimplentes / qtd_total, 2)}%")
print(f"A nova proporcão de clientes adimplentes é de {round(100 * qtd_adimplentes_novo / qtd_total_novo, 2)}%")
print("")
print(f"A proporcão clientes inadimplentes é de {round(100 * qtd_inadimplentes / qtd_total, 2)}%")
print(f"A nova proporcão de clientes inadimplentes é de {round(100 * qtd_inadimplentes_novo / qtd_total_novo, 2)}%")

"""Os dados estão prontos, vamos criar diversas visualizações para correlacionar variáveis explicativas com a variável resposta para buscar entender qual fator leva um cliente a inadimplencia. E para isso, vamos sempre comparar a base com todos os clientes com a base de adimplentes e inadimplentes."""

# Importando os pacotes de visualização e separando os clientes adimplentes e inadimplentes.
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

df_adimplente = df[df['default'] == 0]
# Clientes adimplentes.

df_inadimplente = df[df['default'] == 1]
# Clientes inadimplentes.

# Vamos visualizar a relação entre a variável resposta "default" com os atributos categóricos.

df.select_dtypes('object').head(n=5)

"""

*   ESCOLARIDADE

"""

# Gerando graficos para visualização.
coluna = 'escolaridade'
titulos = ['Escolaridadedos Clientes', 'Escolaridade dos Clientes Adimplentes', 'Escolaridade dos Clientes Inadimplentes']
eixo= 0
max_y= 0

max =  df.select_dtypes('object').describe()[coluna]['freq'] *  1.1

figura, eixos = plt.subplots(1, 3, figsize=(20, 5), sharex=True)
max_y = 0

for eixo, dataframe in enumerate([df, df_adimplente, df_inadimplente]):
  df_to_plot = dataframe[coluna].value_counts().reset_index()
  df_to_plot.columns = [coluna, 'frequencia_absoluta']
  df_to_plot.sort_values(by=[coluna], inplace=True)

  f = sns.barplot(data=df_to_plot, x=coluna, y='frequencia_absoluta', ax=eixos[eixo])
  f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')
  f.set_xticklabels(labels=f.get_xticklabels(), rotation=90)

  _, max_y_f = f.get_ylim()
  max_y = max_y_f if max_y_f > max_y else max_y

for eixo in eixos:
  eixo.set(ylim=(0, max_y))

plt.show()

"""

*  SALÁRIO ANUAL

"""

coluna = 'salario_anual'
titulos = ['Salário Anual dos Clientes', 'Salário Anual dos Clientes Adimplentes', 'Salário Anual dos Clientes Inadimplentes']

eixo= 0
max_y= 0

max =  df.select_dtypes('object').describe()[coluna]['freq'] *  1.1

figura, eixos = plt.subplots(1, 3, figsize=(20, 5), sharex=True)
max_y = 0

for eixo, dataframe in enumerate([df, df_adimplente, df_inadimplente]):
  df_to_plot = dataframe[coluna].value_counts().reset_index()
  df_to_plot.columns = [coluna, 'frequencia_absoluta']
  df_to_plot.sort_values(by=[coluna], inplace=True)

  f = sns.barplot(data=df_to_plot, x=coluna, y='frequencia_absoluta', ax=eixos[eixo])
  f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')
  f.set_xticklabels(labels=f.get_xticklabels(), rotation=90)

  _, max_y_f = f.get_ylim()
  max_y = max_y_f if max_y_f > max_y else max_y

for eixo in eixos:
  eixo.set(ylim=(0, max_y))

plt.show()

"""

*   Visualizações numéricas

"""

df.drop(['id', 'default'], axis=1).select_dtypes('number').head(n=5)

""" - Quantidade de Transações nos Últimos 12 Meses"""

coluna = 'qtd_transacoes_12m'
titulos = ['Qtd. de Transações no Último Ano', 'Qtd. de Transações no Último Ano de Adimplentes', 'Qtd. de Transações no Último Ano de Inadimplentes']

eixo = 0
max_y = 0
figura, eixos = plt.subplots(1,3, figsize=(20, 5), sharex=True)

for dataframe in [df, df_adimplente, df_inadimplente]:

  f = sns.histplot(x=coluna, data=dataframe, stat='count', ax=eixos[eixo])
  f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')

  _, max_y_f = f.get_ylim()
  max_y = max_y_f if max_y_f > max_y else max_y
  f.set(ylim=(0, max_y))

  eixo += 1

figura.show()

# Se percebe que cliente na faixa de 20 até 80 transações tem maior tendencia a se tornar inadimplente (Recomendado estar tomando medidas de cautela com os clientes destas faixas).

""" - Valor das Transações nos Últimos 12 Meses

"""

coluna = 'valor_transacoes_12m'
titulos = ['Valor das Transações no Último Ano', 'Valor das Transações no Último Ano de Adimplentes', 'Valor das Transações no Último Ano de Inadimplentes']

eixo = 0
max_y = 0
figura, eixos = plt.subplots(1,3, figsize=(20, 5), sharex=True)

for dataframe in [df, df_adimplente, df_inadimplente]:

  f = sns.histplot(x=coluna, data=dataframe, stat='count', ax=eixos[eixo])
  f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')

  _, max_y_f = f.get_ylim()
  max_y = max_y_f if max_y_f > max_y else max_y
  f.set(ylim=(0, max_y))

  eixo += 1

figura.show()

# Os valores que nossa base de clientes mais movimenta é de 100 até 5000.

""" - Valor de Transações nos Últimos 12 Meses x Quantidade de Transações nos Últimos 12 Meses"""

f = sns.relplot(x='valor_transacoes_12m', y='qtd_transacoes_12m', data=df, hue='default')
_ = f.set(
    title='Relação entre Valor e Quantidade de Transações no Último Ano',
    xlabel='Valor das Transações no Último Ano',
    ylabel='Quantidade das Transações no Último Ano'
  )