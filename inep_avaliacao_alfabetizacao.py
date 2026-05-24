import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Carregando base de dados
base = pd.read_csv('C:\\Users\\Laura\\OneDrive\\Desktop\\br_inep_avaliacao_alfabetizacao_uf.csv\\br_inep_avaliacao_alfabetizacao_uf.csv')
print(base.head())

# Limpeza de dados
print(base.isnull().sum())  # Verificando valores nulos

# Temos muito valores nulos, não vou remover para não perder dados, e também não irei preencher, pois são dados sensíveis e não quero dados falsos na análise
# Irei prosseguir sem os nulos, usando apenas as colunas necessárias para uma análise sólida

# Estarei focando na seguinte pergunta: “Existem diferenças significativas de alfabetização entre estados e redes de ensino no Brasil?”

base = base.drop(columns=[
    'proporcao_aluno_nivel_0',
    'proporcao_aluno_nivel_1',
    'proporcao_aluno_nivel_2',
    'proporcao_aluno_nivel_3',
    'proporcao_aluno_nivel_4',
    'proporcao_aluno_nivel_5',
    'proporcao_aluno_nivel_6',
    'proporcao_aluno_nivel_7',
    'proporcao_aluno_nivel_8'
])

print(base.info())  # Verificando tipos de dados e colunas

# Transformando a coluna 'rede' e 'serie' para categoria, para melhor visualização

mapa = {
    2: 'Estadual',
    3: 'Municipal',
    5: 'Privada'
}

base['rede'] = base['rede'].map(mapa) 
 
base['serie'] = base['serie'].astype(str)

# Verificando os valores

print(base['rede'].unique())
print(base['serie'].unique())

print(base['rede'].isnull().sum())
print(base['serie'].isnull().sum())

base = base.drop(columns=['serie']) # Após verificar a coluna 'serie', percebi que são dados apenas do 2 ano, então posso excluir a coluna para melhor análise

base = base.dropna(subset=['rede']) # Excluindo o valor nulo de 'rede', afinal era apenas 1 linha

print(base.info()) 

# Agora temos uma base limpa, e posso seguir com a análise exploratória

print(base.describe())  # Verificando estatísticas descritivas

# Olhando esses números não vejo outliers, mas podemos perceber uma diferença grande entre min e max. alguns têm quase 3x mais alfabetização que outros

print(base.sort_values('taxa_alfabetizacao', ascending=False))

print(base.groupby('rede')['taxa_alfabetizacao'].mean())

# Ceará se mostrou acima da média no desempenho com média alfabetização geral ≈ 56% e Sergipe apareceu no oposto

# Na base analisada, as redes estaduais apresentaram maior média de alfabetização. E a privada e o municipal ficaram próximas

print(base.groupby('sigla_uf')['taxa_alfabetizacao'].mean()) # Para melhor visualização dos resultados

# Visualizações

# Gráfico de barras para comparar a taxa média de alfabetização por estado

media_estados = base.groupby('sigla_uf')[
    'taxa_alfabetizacao'
].mean().sort_values(ascending=False)

# Cores
cores = []

for estado in media_estados.index:
    if estado == 'CE':
        cores.append('green')
    elif estado == 'SE':
        cores.append('red')
    else:
        cores.append('skyblue')

plt.figure(figsize=(12,7))

media_estados.plot(kind='bar', color=cores)

plt.title('Taxa Média de Alfabetização por Estado (2023-2024)')
plt.xlabel('Estado')
plt.ylabel('Taxa de Alfabetização')

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

plt.figure(figsize=(8,6))

# Scatter plot para analisar a relação entre taxa de alfabetização e média em português

plt.scatter(
    base['taxa_alfabetizacao'],
    base['media_portugues']
)

plt.title('Relação entre Alfabetização e Desempenho em Português')

plt.xlabel('Taxa de Alfabetização')
plt.ylabel('Média em Português')

plt.grid(True)

plt.show()

# Correlação
correlacao = base[
    ['taxa_alfabetizacao', 'media_portugues']
].corr()

# Tamanho
plt.figure(figsize=(6,4))

# Heatmap
sns.heatmap(
    correlacao,
    annot=True,
    cmap='Blues'
)

# Título
plt.title('Mapa de Correlação')

plt.show()

# Com esse mapa, chegamos a conclusão que conforme melhor a alfabetização, maior o desempenho em português

# Boxplot por rede

plt.figure(figsize=(8,6))

base.boxplot(
    column='taxa_alfabetizacao',
    by='rede'
)

plt.title('Distribuição da Taxa de Alfabetização por Rede')
plt.suptitle('')

plt.xlabel('Rede')
plt.ylabel('Taxa de Alfabetização')

plt.show()

# As medianas estão todas meio próximas e existe bastante dispersão

# Histograma para analisar a distribuição da taxa de alfabetização

plt.figure(figsize=(8,6))

plt.hist(
    base['taxa_alfabetizacao'],
    bins=10
)

plt.title('Distribuição da Taxa de Alfabetização')

plt.xlabel('Taxa de Alfabetização')
plt.ylabel('Frequência')

plt.show()

# Com esse gráfico como observar que a maioria dos estados estão com desempenho intermediário

# Agora vamos comparar 2023 vs 2024

base.groupby('ano')[  # média por ano
    'taxa_alfabetizacao'
].mean()

media_ano = base.groupby('ano')[
    'taxa_alfabetizacao'
].mean()

plt.figure(figsize=(6,5))

media_ano.plot(kind='bar')

plt.title('Média da Taxa de Alfabetização por Ano')
plt.xlabel('Ano')
plt.ylabel('Taxa de Alfabetização')

plt.xticks(rotation=0)

plt.show()

# Mudou pouca coisa de 2023 para 2024, a alfabetização parece estável

# Vou salvar em csv para subir para o Power BI

base.to_csv(
    r'C:\Users\Laura\OneDrive\Desktop\base_alfabetizacao_tratada.csv',
    index=False,
    encoding='utf-8-sig'
)






