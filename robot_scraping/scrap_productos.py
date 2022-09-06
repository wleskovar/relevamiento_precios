import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from typing import Optional
import logging
import pandas as pd

from robot_scraping.datos_DB import datos_DB

def scrap_productos(driver):
    
    engine = datos_DB()
    query = 'SELECT `codigo_categoria` FROM `categorias`'
    df_codigos_categorias = pd.read_sql(query, engine)
    print(df_codigos_categorias)