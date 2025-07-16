from utils.functions import read_xlsx_file, Functions
from utils.validations import Validations
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
input_path = os.getenv("input_path")
output_path = os.getenv("output_path")
cuit_receptor = os.getenv("cuit_receptor")

df = read_xlsx_file(input_path, sheet="Datos")

if df is not None:
    validations = Validations(df)
    validations.validar_fecha(columna_fecha="Fecha")
    validations.validar_fecha(columna_fecha="Fecha del Vto. del CAE")
    validations.limpiar_cuit(columna_cuit="Cuit del receptor")
    validations.cuit_controller(cuit_receptor, columna_cuit="Cuit del receptor", columna_control="Cuit Receptor Usuario")
    
    df_procesado = validations.df
        
    if df_procesado is not None:  
        df_procesado.to_excel(output_path, index=False)