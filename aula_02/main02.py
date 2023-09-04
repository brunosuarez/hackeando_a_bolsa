from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

local_tabela = '/html/body/div[1]/div[2]/table'
tabela = driver.find_element('xpath', local_tabela)
html_tabela = tabela.get_attribute('outerHTML')
tabela = pd.read_html(str(html_tabela), thousands = '.', decimal = ',')[0]
tabela

tabela = tabela.set_index("Papel")
tabela = tabela[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]
tabela

tabela['ROIC'] = tabela['ROIC'].str.replace('%', '')
tabela['ROIC'] = tabela['ROIC'].str.replace('.', '')
tabela['ROIC'] = tabela['ROIC'].str.replace(',', '.')
tabela['ROIC'] = tabela['ROIC'].astype(float)
tabela

tabela = tabela[tabela['Liq.2meses'] > 1000000]
tabela

tabela = tabela[tabela['EV/EBIT'] > 0]
tabela = tabela[tabela['ROIC'] > 0]
tabela

tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending = True)
tabela['ranking_roic'] = tabela['ROIC'].rank(ascending = False)
tabela['ranking_final'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic']
tabela

tabela = tabela.sort_values('ranking_final')
tabela.head(10)
