from typing import Optional
import logging
from decouple import config
import pandas as pd
from sqlalchemy import create_engine, Integer, String, DateTime

def _get_config():
    # Python_decouple
    confi = {
        "engine": config("ENGINE"),
        "usr": config("USR"),
        "password": config("PASSWORD"),
        "port": config("PORT"),
        "database": config("DATABASE"),
    }
    return confi


def _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE):
    """Se genera la coneccion a la base de datos correspondiente

    Returns:
        _type_: se retorna la coneccion para operar con la base de datos.
    """
    return create_engine(f"{ENGINE}+pymysql://{USR}:{PASSWORD}@localhost:{PORT}/{DATABASE}")

def datos_DB():
    confi = _get_config()

    ENGINE = confi.get("engine")
    USR = confi.get("usr")
    PASSWORD = confi.get("password")
    PORT = confi.get("port")
    DATABASE = confi.get("database")

    logger = logging.getLogger()
    try:
        # genero un objeto con la coneccion a la base de datos
        engine = _get_connection(ENGINE, USR, PASSWORD, PORT, DATABASE)
        logger.info(
            f"Coneccion exitosa a la base de datos: {DATABASE} por el puerto: {PORT}"
        )
                
        # para el logging
        logging.info(
            "Se actualizaron las tablas de espacios y provincias en la base de datos"
        )
        return engine
    except Exception as ex:
        logger.error(
            f"La coneccion a la base de datos: {DATABASE}, no se pudo realizar"
        )
        logger.error(ex)
        raise ex