from typing import Optional
import logging
from decouple import config
from robot_scraping.log_configuracion import configure_logger
from robot_scraping.home_to_categorias import home_to_categorias


def mercadona(driver:Optional[object]) ->None:
    logger = logging.getLogger()
    try:
        driver.get(config('MERCADONA'))
        logger.info('se cargo correctamente la pagina del Mercadona')
    except Exception as ex:
        logger.error(f'Problema para cargar la pagina del Mercadona')
        logger.error(ex)
        raise ex

    home_to_categorias(driver)