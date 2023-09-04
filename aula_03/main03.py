from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.fundamentus.com.br/resultado.php'

driver.get(url)
local_tabela = '/html/body/div[1]/div[2]/table'
elemento = driver.find_element("xpath", local_tabela)
html_tabela = elemento.get_attribute('outerHTML')
tabela = pd.read_html(str(html_tabela), thousands = '.', decimal = ',')[0]

tabela = tabela.set_index("Papel")
tabela = tabela[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]
tabela['ROIC'] = tabela['ROIC'].str.replace("%", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(".", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(",", ".")
tabela['ROIC'] = tabela['ROIC'].astype(float)

tabela = tabela[tabela['Liq.2meses'] > 1000000]
tabela = tabela[tabela['EV/EBIT'] > 0]
tabela = tabela[tabela['ROIC'] > 0]

tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending = True)
tabela['ranking_roic'] = tabela['ROIC'].rank(ascending = False)
tabela['ranking_total'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic']

tabela = tabela.sort_values('ranking_total')

tabela = tabela.head(10)
tickers = tabela.index
tickers

import MetaTrader5 as mt5
mt5.initialize()

ticker = 'WEGE3'
info_acoes = mt5.symbol_info(ticker)
preco = mt5.symbol_info_tick(ticker)

for ticker in tickers:

    print(ticker)

    info_acoes = mt5.symbol_info(ticker)
    mt5.symbol_select(ticker)
    tick_min = mt5.symbol_info(ticker).point
    preco = mt5.symbol_info_tick(ticker).ask
    quantidade = 100.0
    ordem_compra = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker,
        "volume": quantidade,
        "type": mt5.ORDER_TYPE_BUY,
        "price": preco,
        "magic": 1,
        "comment": "Trades automáticos",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result_compra = mt5.order_send(ordem_compra)
    print(result_compra)

