from utils.functions import read_xlsx_file, Functions
from utils.validations import Validations
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
input_path = os.getenv("input_path")
output_path = os.getenv("output_path")

df = read_xlsx_file(input_path, sheet="Datos")

if df is not None:
    validations = Validations(df)
    validations.total_controller(
        columnas_a_sumar=["Importe neto de Impuestos", "Iva", "Percepciones de IVA", "Percepciones de IIGG", "Percepciones de Ingresos Brutos", "Impuestos Internos", "Otros Impuestos"],
        columna_total="Total",
        columna_control="Total Control"
    )
    validations.validar_fecha(columna_fecha="Fecha")
    validations.validar_fecha(columna_fecha="Fecha del Vto. del CAE")
    
    df_procesado = validations.df
        
    if df_procesado is not None:  
        df_procesado.to_excel(output_path, index=False)