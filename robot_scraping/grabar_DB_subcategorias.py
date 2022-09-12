import re
import pandas as pd
from datetime import date as dt_date
import logging
from sqlalchemy import Integer, String

from robot_scraping.datos_DB import datos_DB



def grabar_DB_subcategorias(registros_subcategorias):

    engine = datos_DB()

    fecha_grabacion = dt_date.today()
    fecha_grabacion_txt = dt_date.strftime(fecha_grabacion, '%Y-%m-%d')
    planilla_excel_subcategorias = 'subcategorias_' + registros_subcategorias[0]['categoria'] + '_' + fecha_grabacion_txt + '.xlsx'
    # armo el data frame para grabar la base de datos
    df_subcategorias = pd.DataFrame(data=registros_subcategorias, index=None) 
    df_subcategorias.to_excel(planilla_excel_subcategorias)
        
    logger = logging.getLogger()
    try:
        logger.info(
            f"Grabando en la base de datos - tanda de subcategorias"
        )
        df_subcategorias.to_sql(
            con=engine,
            name="categorias",
            if_exists="append",
            index=True,
            index_label="id",
            dtype={
                "codigo_categoria": Integer,
                "categoria": String(150),
                "sub_categoria": String(150),
                "descripcion_grupo": String(150), 
            },
            method="multi",
        )
        
        # para el logging
        logging.info(
            "Se actualizo la tabla de categorias en la base de datos"
        )
    except Exception as ex:
        logger.error(
            f"** ERROR ** - No se actualizo la tabla de categorias en la base de datos"
        )
        logger.error(ex)
        raise ex