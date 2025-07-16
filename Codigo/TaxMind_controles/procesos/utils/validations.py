import pandas as pd
from dotenv import load_dotenv
import os
import re

load_dotenv()
input_path = os.getenv("input_path")
output_path = os.getenv("output_path")



class Validations:
    """Clase que contiene funciones de validación para DataFrames."""
    def __init__(self, df):
        self.df = df
           
    def limpiar_cuit(self, columna_cuit=None):
        """
        Elimina espacios en blanco y guiones de la columna de CUIT.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columna_cuit (str, optional): El nombre de la columna de CUIT.

        Returns:
            pd.DataFrame: El DataFrame con la columna de CUIT limpia.
        """
        try:
            if columna_cuit not in self.df.columns:
                raise ValueError(f"Advertencia: La columna '{columna_cuit}' no existe en el DataFrame.")

            # Eliminar espacios y guiones
            self.df[columna_cuit] = self.df[columna_cuit].astype(str).str.replace(r"[-\s]", "", regex=True)

            return self.df
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    # def limpiar_cuit(self, cuit: str, columna_cuit: str = None) -> str:
    #     """
    #     Limpia un CUIT eliminando guiones y espacios.

    #     Args:
    #         cuit (str): El CUIT a limpiar.
    #         columna_cuit (str, optional): Solo para mantener compatibilidad o logging.

    #     Returns:
    #         str: El CUIT limpio.
    #     """
    #     cuit_limpio = re.sub(r"[-\s]", "", cuit)
       # return cuit_limpio

    def validar_fecha(self, columna_fecha):
        """
        Valida que la columna de fecha esté en formato datetime.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columna_fecha (str): El nombre de la columna de fecha.

        Returns:
            pd.DataFrame: El DataFrame con la columna de fecha validada.
        """

        if columna_fecha not in self.df.columns:
            print(f"Advertencia: La columna '{columna_fecha}' no existe.")
            return

        if not pd.api.types.is_datetime64_any_dtype(self.df[columna_fecha]):
            # Crear una copia de la columna original
            columna_original = self.df[columna_fecha].copy()

            # Intentar convertir a datetime, ignorando errores
            self.df[columna_fecha] = pd.to_datetime(self.df[columna_fecha], errors='coerce', format="%d/%m/%Y")

            # Identificar fechas inválidas (NaT)
            fechas_invalidas = self.df[self.df[columna_fecha].isnull()]

            if not fechas_invalidas.empty:
                print(f"Advertencia: Las siguientes fechas en '{columna_fecha}' no se pudieron convertir:")
                print(fechas_invalidas[columna_fecha])

                # Restaurar las fechas inválidas al valor original
                self.df.loc[self.df[columna_fecha].isnull(), columna_fecha] = columna_original[self.df[columna_fecha].isnull()]

            # Formatear las fechas válidas (no NaT)
            self.df.loc[~self.df[columna_fecha].isnull(), columna_fecha] = self.df.loc[~self.df[columna_fecha].isnull(), columna_fecha].dt.strftime("%d/%m/%Y")

        
        self.df[columna_fecha] = self.df[columna_fecha].dt.strftime("%d/%m/%Y")
        
            
        return self.df
    
    def total_controller(self, columnas_a_sumar, columna_total, columna_control):
        """
        Suma columnas y verifica si el resultado coincide con la columna "Total".

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columnas_a_sumar (list): Lista de nombres de columna a sumar.
            columna_total (str, optional): Nombre de la columna "Total".
            columna_control (str, optional): Nombre de la columna de control.

        Returns:
            pd.DataFrame: El DataFrame con la columna de control.
        """
        try:
            if not all(col in self.df.columns for col in columnas_a_sumar + [columna_total]):
                raise ValueError("Todas las columnas deben existir en el DataFrame.")

            # Calcular la suma de las columnas especificadas
            self.df['Suma'] = self.df[columnas_a_sumar].sum(axis=1)

            # Comparar la suma con la columna "Total" y crear la columna de control
            self.df[columna_control] = (self.df['Suma'] != self.df[columna_total]).astype(int)

            self.df = self.df.drop(columns=['Suma']) # Eliminar la columna 'Suma' auxiliar

            return self.df

        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    def cuit_controller(self, cuit_receptor, columna_cuit="Cuit del Receptor", columna_control="Cuit Receptor Usuario"):
        """
        Verifica si el CUIT del receptor es DIFERENTE a un CUIT específico.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            cuit_receptor (str): El CUIT del receptor a buscar.
            columna_cuit (str, optional): El nombre de la columna con el CUIT del receptor.
            columna_control (str, optional): El nombre columna con la coincidencia.

        Returns:
            pd.DataFrame: DataFrame indicado em la columna_control con 0 (sin diferencia) o 1(diferencia).
        """
        try:
            if columna_cuit not in self.df.columns:
                raise ValueError(f"La columna '{columna_cuit}' no existe en el DataFrame.")

            # Verificar si el CUIT del receptor es DIFERENTE y crear la nueva columna
            self.df[columna_control] = (self.df[columna_cuit] != cuit_receptor).astype(int)

            return self.df

        except ValueError as e:
            print(f"Error: {e}")
            return None

                
            