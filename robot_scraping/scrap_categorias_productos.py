import random
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


SECCIONES = '//section[@class="section"]'
#SECCIONES = '//div[@class="category-detail__content"]'
#SECCIONES = '//*[contains(@class, "category-detail__content") or contains(@class, "category-section")]'
SUB_CATEGORIA = './/h2[@class="section__header headline1-b"]'

def obtener_datos_categoria(driver, datos_categoria):

  if( datos_categoria['codigo_categoria'] != 31 ):
    # obtiene los datos de las subcategorias y los productos
    secciones = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, SECCIONES))
          )
    y = 0
    for seccion in secciones:
      sleep(random.uniform(2.0, 8.0))
      sub_categoria = WebDriverWait(seccion, 10).until(
            EC.presence_of_element_located((By.XPATH, SUB_CATEGORIA))
          )
      print(f'Categoria {datos_categoria["codigo_categoria"]} = Subcategoria: {sub_categoria.text}')
      y = y + 1
    print(f'Esta categoria tiene: {y} subcategorias')
  else:
    print(f'GRUPO DE PESCADO FRESCO 31 {datos_categoria["codigo_categoria"]}\n\n\n\n')
  
  return datos_categoria







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

    # me muevo por cada uno de los grupos, obtengo cada uno de los items que componen el grupo
    for item in items_categorias:
        sleep(random.uniform(2.0, 8.0))

        titulo_grupo_categoria = WebDriverWait(item, 10).until(
          EC.presence_of_element_located((By.XPATH, TITULO_GRUPO_CATEGORIA))
        )

        button_grupo_categoria = WebDriverWait(item, 10).until(
          EC.presence_of_element_located((By.XPATH, BUTTON_GRUPO_CATEGORIA))
        )
        # hago click en el grupo para abrir las categorias, emergen los items de las categorias que componen el grupo
        button_grupo_categoria.click()
        sleep(random.uniform(6.0, 8.0))
        
      
        categorias = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, CATEGORIAS))
        )
        titulos_categoria = WebDriverWait(categorias, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, TITULOS_CATEGORIA))
        )
        i = i + 1
        z = 0
        print(f'Grupo: {titulo_grupo_categoria.text}')

        # recorro el grupo abierto, obteniendo los datos de cada uno de los items que componen el grupo
        for titulo_categoria in titulos_categoria:
            sleep(random.uniform(6.0, 8.0))
            titulo_categoria = WebDriverWait(titulo_categoria, 10).until(
                EC.presence_of_element_located((By.XPATH, BUTTON_CATEGORIA))
            )
            # hacien click en cada uno de los items que componen el grupo, en la pagina aparece el contenedor con los subitems y los producto
            titulo_categoria.click()
            sleep(random.uniform(6.0, 8.0))
            url_categoria = driver.current_url
            url_parceada = urlparse(url_categoria)
            url_path = url_parceada[2].split("/")
            # obtengo el codigo de la categoria
            codigo = int(url_path[2])
            datos_categoria = {
                    'descripcion_grupo': titulo_grupo_categoria.text,
                    'codigo_categoria': codigo,
                    'categoria': titulo_categoria.text,
                    'subcategoria': ''
            }
            print(f'Categoria: {datos_categoria["categoria"]} Codigo: {datos_categoria["codigo_categoria"]}')
            lista_datos.append(obtener_datos_categoria(driver, datos_categoria))

            z = z + 1
            # titulo_categoria.click()
            # sleep(4.0)
        print(f'para este grupo la cantidad de categorias es: {z} \n')
    print(f'La cantidad de grupos es: {i}')