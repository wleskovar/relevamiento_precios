from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from typing import Optional
import logging
from decouple import config
import pandas as pd


GRUPO_CATEGORIAS = '//div[@class="grid-layout__sidebar"]//ul[@class="category-menu"]'
ITEMS_CATEGORIAS = './/li[contains(@class, "category-menu__item")]'
TITULO_GRUPO_CATEGORIA = './/label[@class="subhead1-r"]'
BUTTON_GRUPO_CATEGORIA = './/button'
CATEGORIAS = '//li[@class="category-menu__item open"]'
TITULOS_CATEGORIA = './/li[contains(@class, "subhead1-r category-item")]'
BUTTON_CATEGORIA = './/button[@class="category-item__link"]'

def scrap_categorias_productos(driver:Optional[object]) -> None:

    grupo_categorias = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, GRUPO_CATEGORIAS))
        )

    items_categorias = WebDriverWait(grupo_categorias, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, ITEMS_CATEGORIAS))
        )

    i = 0
    lista_datos = []
    for item in items_categorias:

        titulo_grupo_categoria = WebDriverWait(item, 10).until(
          EC.presence_of_element_located((By.XPATH, TITULO_GRUPO_CATEGORIA))
        )

        button_grupo_categoria = WebDriverWait(item, 10).until(
          EC.presence_of_element_located((By.XPATH, BUTTON_GRUPO_CATEGORIA))
        )
        button_grupo_categoria.click()
        sleep(6.0)
        url_categoria = driver.current_url
        url_parceada = urlparse(url_categoria)
        url_path = url_parceada[2].split("/")
        codigo = int(url_path[2])

        # Abro las categorias del grupo
        
        categorias = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, CATEGORIAS))
        )
        titulos_categoria = WebDriverWait(categorias, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, TITULOS_CATEGORIA))
        )
        i = i + 1
        print(i)
        z = 0
        print(titulo_grupo_categoria.text)
        for titulo_categoria in titulos_categoria:
            titulo_categoria = WebDriverWait(titulo_categoria, 10).until(
                EC.presence_of_element_located((By.XPATH, BUTTON_CATEGORIA))
            )
            
            print(titulo_categoria.text)
            z = z + 1
            titulo_categoria.click()
            sleep(4.0)
            
            # obtener el div categoria detail content y de ese todoso los section con los titulos de las sub_categorias



        print(f'para este grupo la cantidad de categorias es: {z}')


    
    #     lista_datos.append(
    #         {
    #             'codigo_grupo': codigo,
    #             'descripcion_grupo': titulo_grupo_categoria.text,
    #             'categoria':,
    #             'subcategoria':
    #         }
    #     )
    
    # df = pd.DataFrame(lista_datos)
    # print(df)
        
        