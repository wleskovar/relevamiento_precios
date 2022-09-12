from time import sleep
import pandas as pd

from robot_scraping.datos_DB import datos_DB
from robot_scraping.scrap_productos import scrap_productos
from robot_scraping.grabar_DB_productos import grabar_DB_productos

from robot_scraping.procesar_productos import procesar_productos

# armar un dataframe con las categorias de productos

def extraer_productos(codigo_categoria= None):
    
    engine = datos_DB()
    query = 'SELECT `id`, `codigo_categoria`, `categoria`, `subcategoria`, `descripcion_grupo` FROM `categorias`'
    df_categorias = pd.read_sql(query, engine)
    df_categorias.sort_values(['codigo_categoria', 'id'], inplace=True)
    categorias = df_categorias.codigo_categoria.unique()

    
    lista_categorias_a_procesar = [ 31, 
                
                  
                  
         103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 115,
       116, 117, 118, 120, 121, 122, 123, 126, 127, 129, 130, 132, 133,
       135, 138, 140, 142, 143, 145, 147, 148, 149, 150, 151, 152, 154,
       155, 156, 158, 159, 161, 162, 163, 164, 166, 168, 169, 170, 171,
       173, 174, 181, 185, 186, 187, 188, 189, 190, 191, 192, 194, 196,
       198, 199, 201, 202, 203, 205, 206, 207, 208, 210, 212, 213, 214,
       216, 217, 218, 219, 221, 222, 225, 226, 229, 230, 231, 232, 233,
       234, 235, 237, 238, 239, 241, 243, 244, 782, 789, 884]
    lista_categorias_procesadas = [ 27,  28,  29, 32,  33, 34,  36,  37, 38,  40, 42, 43, 44, 45, 46,  47, 48,  49,
                                    50,  51, 52,  53, 54,  56, 58, 59, 60,  62, 64,  65, 66,  68, 69,  71, 72,  75,
                                    77,  78, 79,  80, 81,  83, 84, 86, 88, 89,  90, 92,  95, 97,  98]
    

    #for categoria in categorias:
    for categoria in [99, 100 ]:
        # data es un array con las subcategorias de la categoria que se esta procesando
        data = df_categorias.subcategoria[df_categorias.codigo_categoria == categoria]
        z = 0
        for i in range(len(data)):
            # datos a enviar para la extraccion de los productos de un subgrupo de la categoria procesada
            data_full = df_categorias[df_categorias.codigo_categoria == categoria].iloc[i]
            dic_subcategoria = data_full.to_dict()
            lista_productos = procesar_productos(dic_subcategoria)
            print(lista_productos)
            grabar_DB_productos(lista_productos, i)
            if ( z == 2):
                sleep(300.0)
                z = 0
            else:
                z = z + 1
                sleep(60.0)

            
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n============ MUCHO LABURO PERO TERMINE ==========\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

extraer_productos()