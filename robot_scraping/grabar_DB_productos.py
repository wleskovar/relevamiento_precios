import pandas as pd
from datetime import date as dt_date
import logging
from sqlalchemy import Integer, String, Float

from robot_scraping.datos_DB import datos_DB



def grabar_DB_productos(registros_producto, grupo):

    engine = datos_DB()

    fecha_grabacion = dt_date.today()
    fecha_grabacion_txt = dt_date.strftime(fecha_grabacion, '%Y-%m-%d')
    planilla_excel_productos = 'productos_' + fecha_grabacion_txt + '_' + str(grupo) +'.xlsx'
    # armo el data frame para grabar la base de datos
    df_productos = pd.DataFrame(data=registros_producto, index=None) 
    df_productos.to_excel(planilla_excel_productos)
        
    logger = logging.getLogger()
    try:
        logger.info(
            f"Grbando en la base de datos - tanda index: {grupo}"
        )
        df_productos.to_sql(
            con=engine,
            name="productos",
            if_exists="append",
            index=True,
            index_label="id",
            dtype={
                "prod_codigo_categoria": Integer,
                "prod_categoria": String(150),
                "prod_sub_categoria": String(150),
                "prod_descripcion_grupo": String(150),
                "prod_descripcion": String(500),
                "prod_envase": String(50),
                "prod_presentacion": String(30),
                "prod_precio_unidad": Float,
                "prod_unidad": String(10),
                "prod_precio_unidad_comercial": Float,
                "prod_unidade_comercial": String(30),
                "prod_codigo_web": String(10)  
            },
            method="multi",
        )
        
        # para el logging
        logging.info(
            "Se actualizo la tabla de productos en la base de datos"
        )
    except Exception as ex:
        logger.error(
            f"** ERROR ** - No se actualizo la tabla de productos en la base de datos"
        )
        logger.error(ex)
        raise ex