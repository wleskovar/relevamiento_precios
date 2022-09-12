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

from robot_scraping.home_to_categorias import home_to_categorias
from robot_scraping.init_browser import init_browser
from robot_scraping.grabar_DB_subcategorias import grabar_DB_subcategorias


SECCIONES = '//section[@class="section"]'
SUB_CATEGORIA = './/h2[@class="section__header headline1-b"]'
# Para la categoria 31 Pescado Fresco, tienen una pagina difernte al resto.
PESCADO_FRESCO = '//div[@class="category-section"]'
PESCADO_FRESCO_SUB_CATEGORIA = './/h3[@class="category-section__name title1-b"]'

def obtener_datos_categoria(driver, datos_categoria):

  lista_subcategorias = []
  
  if( datos_categoria['codigo_categoria'] != 31 ):
    # obtiene los datos de las subcategorias y los productos
    secciones = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, SECCIONES))
          )
    y = 0
    for seccion in secciones:
      subcategoria = {
        'codigo_categoria': datos_categoria['codigo_categoria'],
        'categoria': datos_categoria['categoria'],
        'subcategoria': '',
        'descripcion_grupo': datos_categoria['descripcion_grupo']
      }
      sleep(random.uniform(2.0, 8.0))
      sub_categoria = WebDriverWait(seccion, 15).until(
            EC.presence_of_element_located((By.XPATH, SUB_CATEGORIA))
          )
      subcategoria['subcategoria'] = sub_categoria.text
      print(f'Categoria {datos_categoria["codigo_categoria"]} = Subcategoria: {sub_categoria.text}')
      y = y + 1
      lista_subcategorias.append(subcategoria)
    print(f'Esta categoria tiene: {y} subcategorias')
  else:
    # Se procesa la informacion de la categoria Pescado Fresco 31 por tener una pagina diferente a las demas
    divisiones = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, PESCADO_FRESCO))
          )
    k = 0
    for division in divisiones:
      subcategoria = {
        'codigo_categoria': datos_categoria['codigo_categoria'],
        'categoria': datos_categoria['categoria'],
        'subcategoria': '',
        'descripcion_grupo': datos_categoria['descripcion_grupo']
      }
      sleep(random.uniform(2.0, 8.0))
      pescado_fresco_sub_categoria = WebDriverWait(division, 15).until(
            EC.presence_of_element_located((By.XPATH, PESCADO_FRESCO_SUB_CATEGORIA))
          )
      subcategoria['subcategoria'] = pescado_fresco_sub_categoria.text
      print(f'Categoria {datos_categoria["codigo_categoria"]} = Subcategoria: {pescado_fresco_sub_categoria.text}')
      k = k + 1
      lista_subcategorias.append(subcategoria)
    print(f'Esta categoria tiene: {k} subcategorias')
  
  grabar_DB_subcategorias(lista_subcategorias)
  print('------- subcategorias -------')
  print(lista_subcategorias)


MENU_GRUPO_CATEGORIAS = '//div[@class="grid-layout__sidebar"]//ul[@class="category-menu"]'
ITEMS_GRUPO_CATEGORIAS = './/li[contains(@class, "category-menu__item")]'
TITULO_GRUPO_CATEGORIA = './/label[@class="subhead1-r"]'
BUTTON_GRUPO_CATEGORIA = './/button'
CATEGORIAS = '//li[@class="category-menu__item open"]'
TITULOS_CATEGORIA = './/li[contains(@class, "subhead1-r category-item")]'
BUTTON_CATEGORIA = './/button[@class="category-item__link"]'

def scrap_categorias():

  driver = init_browser()
  logger = logging.getLogger()
  try:
      driver.get(config('MERCADONA'))
      logger.info('se cargo correctamente la pagina del Mercadona')
      driver_categorias = home_to_categorias(driver)
      sleep(random.uniform(6.0, 15.0))
      logger.info('se navego la pagina hasta las categorias')
  except Exception as ex:
      logger.error(f'Problema para cargar la pagina del Mercadona')
      logger.error(ex)
      raise ex

  menu_grupo_categorias = WebDriverWait(driver_categorias, 15).until(
        EC.presence_of_element_located((By.XPATH, MENU_GRUPO_CATEGORIAS))
      )
  # obtengo todos las categorias para el grupo seleccionado
  items_grupo_categorias = WebDriverWait(menu_grupo_categorias, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, ITEMS_GRUPO_CATEGORIAS))
      )

  # me muevo por cada uno de los grupos, obtengo cada uno de los grupo que componen el menu (grilla)
  for grupo in items_grupo_categorias:
      sleep(random.uniform(2.0, 8.0))
      titulo_grupo_categoria = WebDriverWait(grupo, 15).until(
        EC.presence_of_element_located((By.XPATH, TITULO_GRUPO_CATEGORIA))
      )
      button_grupo_categoria = WebDriverWait(grupo, 15).until(
        EC.presence_of_element_located((By.XPATH, BUTTON_GRUPO_CATEGORIA))
      )
      # hago click en el grupo para abrir las categorias, emergen los items de las categorias que componen el grupo
      button_grupo_categoria.click()
      sleep(random.uniform(6.0, 8.0))
      
    
      categorias = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, CATEGORIAS))
      )
      # submenu del grupo con la lista de categorias, busco todas la categorias
      titulos_categoria = WebDriverWait(categorias, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, TITULOS_CATEGORIA))
      )
      
      print(f'Grupo: {titulo_grupo_categoria.text}')
      # recorro el grupo abierto, obteniendo los datos de cada de las categorias que componen el grupo
      for titulo_categoria in titulos_categoria:
          sleep(random.uniform(6.0, 8.0))
          titulo_categoria = WebDriverWait(titulo_categoria, 15).until(
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
                  'codigo_categoria': codigo,
                  'categoria': titulo_categoria.text,
                  'descripcion_grupo': titulo_grupo_categoria.text
          }
          print(f'Categoria: {datos_categoria["categoria"]} Codigo: {datos_categoria["codigo_categoria"]}')
          # proceso cada categoria en busqueda de las subcategorias
          obtener_datos_categoria(driver, datos_categoria)

scrap_categorias()