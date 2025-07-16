import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
input_path = os.getenv("input_path")
output_path = os.getenv("output_path")


def read_xlsx_file(file_path, sheet=0, columns=None, skiprows=None):
    """Lee un archivo XLSX con pandas.

    Args:
        file_path (str): La ruta al archivo XLSX.
        sheet (int o str): El nombre de la Sheet a leer. Por defecto es 0 (lee la primer hoja).
        columns (list): Una lista de nombres de columna a leer. Por defecto es None (lee todas las columnas).
        skiprows (list o int): Filas a saltar al leer el archivo.  Puede ser una lista de índices de fila o un entero que indica el número de filas a saltar desde el principio. Por defecto None (no salta filas).
        convert_dates (bool): Si es True, intenta convertir las columnas de formato fechas a tipo datetime. Por defecto True.

    Returns:
        pandas.DataFrame: DataFrame con los datos del archivo XLSX.
    """
    try:
        df = pd.read_excel(
            file_path,
            sheet_name=sheet,
            usecols=columns,
            skiprows=skiprows,
            engine="openpyxl",  
        )
            
        return df
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {file_path}")
        return None
    except ValueError as e:
        if "Worksheet named" in str(e):
            print(f"Error: Hoja '{sheet}' no encontrada en el archivo.")
        elif "Usecols do not match columns" in str(e):
            print(f"Error: Las columnas indicadas no coinciden con las columnas del archivo.")
        else:
            print(f"Error al leer el archivo XLSX: {e}")
        return None
    except Exception as e:
        print(f"Error al leer el archivo XLSX: {e}")
        return None



class Functions:
    """Clase que contiene funciones para procesar DataFrames."""
    def __init__(self, df):
        self.df = df

    def check_duplicates(self, columna_factura, columna_cuit, columna_duplicado):
        """
        Identifica filas duplicadas basándose en la combinación de las columnas "Nro. de Factura" y "Cuit del Emisor".

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columna_factura (str): Nombre de la columna con el número de factura.
            columna_cuit (str): Nombre de la columna con el CUIT del emisor.
            columna_duplicado (str): Nombre de la columna donde se marcarán los duplicados.

        Returns:
            pd.DataFrame: DataFrame indicado em la columna "Duplicado" con 0 (no duplicado) o 1(duplicado).
        """
        try:
            if not all(col in self.df.columns for col in [columna_factura, columna_cuit]):
                raise ValueError(f"Advertencia: Las columnas '{columna_factura}' y '{columna_cuit}' deben existir en el DataFrame.")

            self.df[columna_duplicado] = (
                self.df.duplicated(subset=[columna_factura, columna_cuit], keep=False)
                .astype(int)
            )
            
            return self.df
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    def columns_separator(self, columna_factura):
        """
        Extrae el punto de venta y el numero de comprobante, del número de factura.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columna_factura (str): Nombre de la columna con el número de factura.

        Returns:
            pd.DataFrame: El DataFrame con la columna "Punto de Venta" y "Numero de Comprobante".
        """
        try:
            if columna_factura not in self.df.columns:
                raise ValueError(f"Advertencia: La columna '{columna_factura}' no existe.")

            # Extraer punto de venta y número de comprobante
            self.df[["Punto de Venta", "Numero de Comprobante"]] = self.df[columna_factura].astype(str).str.extract(r"(\d+)(?:[-\s\D]+)?(\d+)?")

            # Convertir a enteros
            self.df["Punto de Venta"] = pd.to_numeric(self.df["Punto de Venta"], errors='coerce').astype('Int64')
            self.df["Numero de Comprobante"] = pd.to_numeric(self.df["Numero de Comprobante"], errors='coerce').astype('Int64')
            
            return self.df

        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    def columns_concatenator(self, columnas, nueva_columna, separador=None):
        """
        Concatena múltiples columnas de un DataFrame.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columnas (list): Una lista de columnas a concatenar.
            nueva_columna (str, optional): El nombre de la nueva columna concatenada.
            separador (str, optional): El separador a usar entre las columnas.

        Returns:
            pd.DataFrame: El DataFrame con la nueva columna concatenada.
        """
        try:
            if not all(col in self.df.columns for col in columnas):
                raise ValueError("Todas las columnas especificadas deben existir en el DataFrame.")

            self.df[nueva_columna] = self.df[columnas].astype(str).apply(lambda x: separador.join(x), axis=1)
            return self.df

        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    def columns_comparator(self, df2, column1, column2):
        """
        Compara una columna de 2 dataframes.

        Args:
            df2 (pd.DataFrame): El segundo dataframe.
            column1 (str): Nombre de la columna a comparar
            column2 (str): Nombre de la columna a completar.

        Returns:
            None
        """
        try:
            if column1 not in self.df.columns or column1 not in df2.columns:
                raise ValueError("La columna 'Concatenado' debe existir en ambos DataFrames.")

            self.df[column2] = (~self.df[column1].isin(df2[column1])).astype(int)

        except ValueError as e:
            print(f"Error: {e}")
            
    def columns_eliminator(self, columnas):
        """
        Elimina las columnas de un DataFrame.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            columnas (list): Una lista de nombres de columna a eliminar.

        Returns:
            pd.DataFrame: El DataFrame con las columnas eliminadas.
        """
        try:
            if not isinstance(columnas, list):
                raise TypeError("El argumento 'columnas' debe ser una lista.")

            columnas_no_existentes = [col for col in columnas if col not in self.df.columns]
            if columnas_no_existentes:
                raise ValueError(f"Las siguientes columnas no existen en el DataFrame: {columnas_no_existentes}")

            self.df = self.df.drop(columns=columnas)
            return self.df

        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            return None

    
