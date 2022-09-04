from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from typing import Optional
import logging
from decouple import config

MARCO_COOKIE = '//*[@class="cookie-banner__actions"]'
BUTTON_COOKIE = './/button[@class="ui-button ui-button--small ui-button--primary ui-button--positive"]'

def aceptando_cookies(driver:Optional[object]) -> None:
    marco = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, MARCO_COOKIE))
        )
    boton_cookie = WebDriverWait(marco, 10).until(
          EC.presence_of_element_located((By.XPATH, BUTTON_COOKIE))
        )
    boton_cookie.click()


FORMULARIO = '//form[@class="postal-code-checker"]'
FIELD = './/input[@class="ym-hide-content"]'
CODIGO_POSTAL_CORNELLA = '08940'
BUTTON_POSTAL = './/button[@class="button button-primary button-big"]'

def ingresando_codigo(driver:Optional[object]) -> None:
    formulario = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, FORMULARIO))
        )
    campo = WebDriverWait(formulario, 10).until(
          EC.presence_of_element_located((By.XPATH, FIELD))
        )
    campo.send_keys(CODIGO_POSTAL_CORNELLA)

    boton_codigo = WebDriverWait(formulario, 10).until(
          EC.presence_of_element_located((By.XPATH, BUTTON_POSTAL))
        )
    boton_codigo.click()

CATEGORIAS = '//a[@href="/categories"]'


def home_to_categorias(driver:Optional[object]) -> int:
    aceptando_cookies(driver)
    ingresando_codigo(driver)

    categorias = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, CATEGORIAS))
        )
    categorias.send_keys("webdriver" + Keys.ENTER)

    sleep(12.0)

    
        
    return driver



    # url_categoria = driver.current_url
    # url_parceada = urlparse(url_categoria)
    # url_path = url_parceada[2].split("/")
    # codigo = int(url_path[2])
    # print(codigo)
    # driver.close() 
   
   # carga todos los grupos de categorias y la retorna para su tratamiento 
    

