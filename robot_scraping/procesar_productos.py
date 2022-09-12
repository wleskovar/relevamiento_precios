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
ENVASE_PRESENTACION_PRECIO_MEDIDA = '//div[@class="product-format product-format__size"]/span[@class="headline1-r"]'
PRECIO_UNIDAD = '//p[@class="product-price__unit-price large-b"]'
UNIDAD = '//p[@class="product-price__extra-price title1-r"]'



def extraer_datos_producto(driver, pagina, dic_subcategoria):
    
    dic_producto = {
        "prod_codigo_categoria": dic_subcategoria.get('codigo_categoria'),
        "prod_categoria": dic_subcategoria.get('categoria'),
        "prod_sub_categoria": dic_subcategoria.get('subcategoria'),
        "prod_descripcion_grupo": dic_subcategoria.get('descripcion_grupo'),
        "prod_descripcion": '',
        "prod_envase": '',
        "prod_presentacion": '',
        "prod_precio_unidad": '',
        "prod_unidad": '',
        "prod_precio_unidad_comercial": '',
        "prod_unidad_comercial": '' ,
        "prod_codigo_web": ''  
    }

    descripcion = WebDriverWait(pagina, 10).until(
                  EC.presence_of_element_located((By.XPATH, DESCRIPCION))
              )
    envase_presentacion_precio_medida = WebDriverWait(pagina, 10).until(
                  EC.presence_of_all_elements_located((By.XPATH, ENVASE_PRESENTACION_PRECIO_MEDIDA))
              )
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

      envase = envase_presentacion_precio_medida[0].text
      presentacion = envase_presentacion_precio_medida[1].text
      precio_medida_comercial = envase_presentacion_precio_medida[2].text
      dic_producto["prod_envase"] = envase

    else:

      presentacion = envase_presentacion_precio_medida[0].text
      precio_medida_comercial = envase_presentacion_precio_medida[1].text
      dic_producto["prod_envase"] = ''

    dic_producto["prod_presentacion"] = presentacion
    precio_medida_comercial = (precio_medida_comercial).replace('| ', '').split()
    precio_unidad_comercial = float(precio_medida_comercial[0].replace(',', '.'))
    unidad_comercial = precio_medida_comercial[1].replace('€/', '')
    dic_producto["prod_precio_unidad_comercial"] = precio_unidad_comercial
    dic_producto["prod_unidad_comercial"] = unidad_comercial

    return dic_producto



SECCIONES_SUBCATEGORIA = '//div[@class="category-detail__content"]'
SUBCATEGORIA = './/section[@class="section"]'
BUTTON_PRODUCTO = './/button[@class="product-cell__content-link"]'
CLOSE_BUTTON = '//button[@data-test="modal-close-button"]'

def procesar_productos(dic_subcategoria):

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

    # Navego hasta la categoria segun 'codigo_categoria'
    codigo = dic_subcategoria.get("codigo_categoria")
    url = urljoin('https://tienda.mercadona.es/categories/', str(codigo))
    driver_categorias.get(url)
    sleep(random.uniform(6.0, 10.0))

    # Estando en la categoria busco todos los elementos con producto de la subcategoria. Se hace por posicion en la pagina
    div_secciones_subcategorias = WebDriverWait(driver_categorias, 15).until(
          EC.presence_of_element_located((By.XPATH, SECCIONES_SUBCATEGORIA))
        )
    secciones_subcategorias = WebDriverWait(div_secciones_subcategorias, 15).until(
          EC.presence_of_all_elements_located((By.XPATH, SUBCATEGORIA))
        )
    
    
    # Teniedo todas las secciones de las subcategorias, proceso la que corresponde al indice recibido como parametro
    indice = dic_subcategoria.get('id')
    titulo_subcategoria = WebDriverWait(secciones_subcategorias[indice], 15).until(
          EC.presence_of_element_located((By.XPATH, './/h2[@class="section__header headline1-b"]'))
        )
    # Extraer los productos de la subcategoria
    print(titulo_subcategoria.text)
    productos_subcategoria = WebDriverWait(secciones_subcategorias[indice], 15).until(
          EC.presence_of_all_elements_located((By.XPATH, './/div[@class="product-cell"]'))
        )
    print(len(productos_subcategoria))
    # procesar cada uno de los productos
    lista_productos = []
    for k in range(len(productos_subcategoria)):
        producto = WebDriverWait(productos_subcategoria[k], 10).until(
            EC.presence_of_element_located((By.XPATH, BUTTON_PRODUCTO))
        )
        producto.click()
        # Extraer los datos
        lista_productos.append( extraer_datos_producto(driver_categorias, producto, dic_subcategoria) )
        
        
        sleep(random.uniform(6.0, 10.0))
        button_producto = WebDriverWait(producto, 10).until(
          EC.presence_of_element_located((By.XPATH, CLOSE_BUTTON))
        )
        
        button_producto.click()
    
    
    print('------------------------------------------------------')
    driver_categorias.close()
    return lista_productos
