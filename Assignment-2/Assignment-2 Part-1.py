from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service = service)
driver.get("https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050")
driver.implicitly_wait(10)
try:
    symbols = []
    opens = []
    highs = []
    lows = []
    prev_closes = []
    ltps = []
    changes = []
    pchanges = []
    volumes = []
    values = []
    year_highs = []
    year_lows = []
    change_30d = []
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'equityStockTable'))
    )
    soup = BeautifulSoup(driver.page_source , 'html.parser')
    table = soup.find('table', {'id': 'equityStockTable'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows[1:] :
        columns = row.find_all('td')
        if len(columns)>=13 :
            symbols.append(columns[0].text.strip())
            opens.append(columns[1].text.strip())
            highs.append(columns[2].text.strip())
            lows.append(columns[3].text.strip())
            prev_closes.append(columns[4].text.strip())
            ltps.append(columns[5].text.strip())
            changes.append(columns[6].text.strip())
            pchanges.append(columns[7].text.strip())
            volumes.append(columns[8].text.strip())
            values.append(columns[9].text.strip())
            year_highs.append(columns[10].text.strip())
            year_lows.append(columns[11].text.strip())
            change_30d.append(columns[12].text.strip())
    
    df = pd.DataFrame({
        'SYMBOL': symbols,
        'OPEN': opens,
        'HIGH': highs,
        'LOW': lows,
        'PREV. CLOSE': prev_closes,
        'LTP': ltps,
        'CHANGE': changes,
        'CHANGE %': pchanges,
        'VOLUME (Shares)': volumes,
        'VALUE (in Crores)': values,
        '52W H': year_highs,
        '52W L': year_lows,
        '30 D CHANGE %': change_30d
    })
    
    df.to_csv('Assignment-2_Part-1.csv', index=False)

finally:
    driver.quit()