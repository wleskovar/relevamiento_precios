from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import argparse
from typing import Optional
import logging
from decouple import config

from robot_scraping.log_configuracion import configure_logger

def init_browser():
    """ Inicializa el robot al tipo de navegador y a la pagina

    Returns:
        objeto: retorna el driver a la pagina 
    """
    configure_logger()
    logger = logging.getLogger()

    # Definimos el User Agent en Selenium utilizando la clase Options
    opts = Options()
    #opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
    driver = webdriver.Chrome(config('DRIVER_CHROME'), chrome_options=opts)
    #driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver