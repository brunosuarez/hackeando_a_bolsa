import pandas as pd
import quantstats as qs

dados = pd.read_csv('dados_empresas.csv')
dados

dados = dados[dados['volume_negociado'] > 10000000]
dados

dados['retorno'] = dados.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
dados

dados['retorno'] = dados.groupby('ticker')['retorno'].shift(-1)
dados

dados['ranking_ebit_ev'] = dados.groupby('data')['ebit_ev'].rank(ascending = False)
dados['ranking_roic'] = dados.groupby('data')['roic'].rank(ascending = False)

dados['ranking_final'] = dados['ranking_ebit_ev'] + dados['ranking_roic']
dados['ranking_final'] = dados.groupby('data')['ranking_final'].rank()
dados

dados[dados['data'] == '2016-01-31'].sort_values('ranking_ebit_ev').head(10)

dados = dados[dados['ranking_final'] <= 10 ]
dados

rentabilidade_por_carteira = dados.groupby('data')['retorno'].mean()
rentabilidade_por_carteira = rentabilidade_por_carteira.to_frame()
rentabilidade_por_carteira

rentabilidade_por_carteira = dados.groupby('data')['retorno'].mean()
rentabilidade_por_carteira = rentabilidade_por_carteira.to_frame()
rentabilidade_por_carteira

rentabilidade_por_carteira['modelo'] = ( 1 + rentabilidade_por_carteira['retorno']).cumprod() - 1
rentabilidade_por_carteira = rentabilidade_por_carteira.shift(1)
rentabilidade_por_carteira = rentabilidade_por_carteira.dropna()
rentabilidade_por_carteira

ibov = pd.read_csv('ibov.csv')
retorno_ibov = ibov['fechamento'].pct_change().dropna()
retorno_acum_ibov = (1 + retorno_ibov).cumprod() - 1
rentabilidade_por_carteira['ibovespa'] = retorno_acum_ibov.values
rentabilidade_por_carteira = rentabilidade_por_carteira.drop('retorno', axis = 1)
rentabilidade_por_carteira

qs.extend_pandas()

rentabilidade_por_carteira.index = pd.to_datetime(rentabilidade_por_carteira.index)
rentabilidade_por_carteira['modelo'].plot_monthly_heatmap()
rentabilidade_por_carteira['ibovespa'].plot_monthly_heatmap()
rentabilidade_por_carteira.plot()

