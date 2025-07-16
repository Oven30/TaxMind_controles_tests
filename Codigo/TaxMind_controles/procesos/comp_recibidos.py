from utils.functions import read_xlsx_file, Functions
from utils.validations import Validations
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
input_path = os.getenv("input_path")
input_path_mis_comprobantes = os.getenv("input_path_mis_comprobantes")
output_path_mis_comprobantes = os.getenv("output_path_mis_comprobantes")
output_path = os.getenv("output_path")

df = read_xlsx_file(input_path, sheet="Datos")
df_mis_comprobantes = read_xlsx_file(input_path_mis_comprobantes)

#df facturas_totales
if df is not None:
    validations = Validations(df)
    validations.limpiar_cuit(columna_cuit="Cuit del Emisor")
    validations.validar_fecha(columna_fecha="Fecha")
    validations.validar_fecha(columna_fecha="Fecha del Vto. del CAE")
    
    functions = Functions(validations.df)
    functions.columns_separator(columna_factura="Nro. de Factura")
    functions.columns_concatenator(columnas=["Punto de Venta", "Numero de Comprobante", "Cuit del Emisor"], nueva_columna="Concatenado", separador="-")
    
#df Mis Comprobantes Recibidos      
if df_mis_comprobantes is not None:
    validations_mis_comprobantes = Validations(df_mis_comprobantes)
    validations_mis_comprobantes.limpiar_cuit(columna_cuit="Nro.Doc.Emisor")
    validations_mis_comprobantes.validar_fecha(columna_fecha="Fecha")
    
    functions_mis_comprobantes = Functions(validations_mis_comprobantes.df)
    functions_mis_comprobantes.columns_concatenator(columnas=["Punto de Venta", "Número Desde", "Nro.Doc.Emisor"], nueva_columna="Concatenado", separador="-")
    df_procesado_mis_comprobantes = validations_mis_comprobantes.df
        
    
#control de duplicados entres df facturas_totales y df mis_comprobantes       
functions.columns_comparator(df_procesado_mis_comprobantes, column1="Concatenado", column2="Mis comprobantes")
functions.columns_eliminator(columnas=["Punto de Venta", "Numero de Comprobante", "Concatenado"])
functions_mis_comprobantes.columns_eliminator(columnas=["Concatenado"])

df_procesado = functions.df
df_procesado_mis_comprobantes = functions_mis_comprobantes.df

if df_procesado is not None:  
        df_procesado.to_excel(output_path, index=False)

if df_procesado_mis_comprobantes is not None:  
        df_procesado_mis_comprobantes.to_excel(output_path_mis_comprobantes, index=False)