import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urljoin
from typing import Optional
import logging
from decouple import config
from urllib.parse import urlparse
from robot_scraping.home_to_categorias import home_to_categorias
from robot_scraping.init_browser import init_browser


DESCRIPCION =  '//h1[@class="title2-r private-product-detail__description"]'
ENVASE_PRESENTACION_PRECIO_MEDIDA = '//div[@class="product-format product-format__size"]/span'

PRESENTACION = '//div[@class="product-format product-format__size"]/span[2]'
PRECIO_MEDIDA = '//div[@class="product-format product-format__size"]/span[3]'
PRECIO_UNIDAD = '//p[1]'
UNIDAD = '//p[2]'


def extraer_datos_producto(driver, pagina, dic_producto):

  descripcion = WebDriverWait(pagina, 10).until(
                EC.presence_of_element_located((By.XPATH, DESCRIPCION))
            )
  envase_presentacion_precio_medida = WebDriverWait(pagina, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, ENVASE_PRESENTACION_PRECIO_MEDIDA))
            )
  sleep(random.uniform(6.0, 10.0))
  precio_unidad = WebDriverWait(pagina, 10).until(
                EC.presence_of_element_located((By.XPATH, PRECIO_UNIDAD))
            )
  unidad = WebDriverWait(pagina, 10).until(
                EC.presence_of_element_located((By.XPATH, UNIDAD))
            )

  url_producto = driver.current_url
  url_parceada = urlparse(url_producto)
  url_path = url_parceada[2].split("/")
  # obtengo el codigo del producto en la Web
  codigo = url_path[2]

  dic_producto["prod_descripcion"] = descripcion.text
  precio_unidad = (precio_unidad.text).split()
  precio_unidad = float(precio_unidad[0].replace(',', '.'))
  dic_producto["prod_precio_unidad"] = precio_unidad
  unidad = (unidad.text).replace('/', '')
  dic_producto["prod_unidad"] = unidad
  dic_producto["prod_codigo_web"] = codigo # Es un string, no usar numerico por como vienen los codigos

  if ( len(envase_presentacion_precio_medida) == 3 ):

    envase = WebDriverWait(envase_presentacion_precio_medida[0], 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="headline1-r"]'))
            )
    presentacion = WebDriverWait(envase_presentacion_precio_medida[1], 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="headline1-r"]'))
            )
    precio_medida = WebDriverWait(envase_presentacion_precio_medida[2], 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="headline1-r"]'))
            )
    dic_producto["prod_envase"] = envase.text

  else:

    presentacion = WebDriverWait(envase_presentacion_precio_medida[0], 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="headline1-r"]'))
            )
    precio_medida = WebDriverWait(envase_presentacion_precio_medida[1], 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="headline1-r"]'))
            )
    dic_producto["prod_envase"] = ''

  dic_producto["prod_presentacion"] = presentacion.text
  precio_medida = (precio_medida.text).replace('| ', '')
  dic_producto["prod_precio_medida"] = precio_medida

  return dic_producto

GRID_PRODUCTOS = '//div[@class="grid-layout__content"]'
PRODUCTOS = '//div[@class="product-cell"]'
BUTTON_PRODUCTO = './/button[@class="product-cell__content-link"]'
CLOSE_BUTTON = '//button[@data-test="modal-close-button"]'

def scrap_productos(dic_producto):

    driver = init_browser()
    logger = logging.getLogger()
    try:
        driver.get(config('MERCADONA'))
        logger.info('se cargo correctamente la pagina del Mercadona')
        driver_categorias = home_to_categorias(driver)
        sleep(random.uniform(6.0, 10.0))
        logger.info('se navego la pagina hasta las categorias')
    except Exception as ex:
        logger.error(f'Problema para cargar la pagina del Mercadona')
        logger.error(ex)
        raise ex

    codigo = dic_producto.get("prod_codigo_categoria")
    url = urljoin('https://tienda.mercadona.es/categories/', str(codigo))
    driver_categorias.get(url)
    sleep(random.uniform(6.0, 10.0))
    grid_productos = WebDriverWait(driver_categorias, 10).until(
          EC.presence_of_element_located((By.XPATH, GRID_PRODUCTOS))
        )
    sleep(random.uniform(6.0, 10.0))
    productos = WebDriverWait(grid_productos, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, PRODUCTOS))
        )
    list_productos = []
    for producto in productos:
        button_producto = WebDriverWait(producto, 10).until(
          EC.presence_of_element_located((By.XPATH, BUTTON_PRODUCTO))
        )
        sleep(random.uniform(6.0, 10.0))
        button_producto.click()
        # Extraer los datos
        list_productos.append( extraer_datos_producto(driver_categorias, button_producto, dic_producto) )
        print(list_productos)
        close_button = WebDriverWait(button_producto, 10).until(
          EC.presence_of_element_located((By.XPATH, CLOSE_BUTTON))
        )
        close_button.click()
        sleep(random.uniform(6.0, 10.0))
    print('------------------------------------------------------')
    driver_categorias.close()
    return list_productos