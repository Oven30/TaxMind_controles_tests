import sys
import os
import pandas as pd
 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from behave import *
from procesos.utils.validations import Validations
from procesos.utils.functions import Functions
from behave.runner import Context

#Cuit limpio
@given('tengo un CUIT "{cuit}"')
def step_given_tengo_un_cuit(context, cuit):
    #cuit=20-12345678-9
    context.cuit = cuit
@when('limpio el CUIT')
def step_when_limpio_el_cuit(context):
    df = pd.DataFrame({'CUIT': [context.cuit]})
    validador = Validations(df)
    df_limpio = validador.limpiar_cuit('CUIT')
    context.cuit_limpio = df_limpio.loc[0, 'CUIT']
@then('el CUIT limpio debe ser "{esperado}"')
def step_then_el_cuit_limpio_debe_ser(context, esperado):
    assert context.cuit_limpio == esperado, f"Esperado '{esperado}', pero fue '{context.cuit_limpio}'"
#Cuit tamaño
@given('tengo un CUIT ya limpio')
def step_given_tengo_un_cuit_ya_limpio(context):
    # Asignar un CUIT ya limpio a la variable de contexto
    context.cuit_limpio = "20123456789"
@then('el CUIT mide exactamente 11 caracteres')
def step_then_el_cuit_mide_exactamente_11_caracteres(context):
    assert len(context.cuit_limpio) == 11, f"El CUIT '{context.cuit_limpio}' no tiene 11 caracteres, tiene {len(context.cuit_limpio)}"


#Fecha OK
@given('tengo una fecha "{fecha}"')
def step_given_tengo_una_fecha(context, fecha):
    # Asignar la fecha al contexto
    context.fecha = fecha
@when('valido y formateo la fecha')
def step_when_valido_y_formateo_la_fecha(context):
    df = pd.DataFrame({'fecha': [context.fecha]})
    validador = Validations(df)
    df_limpio = validador.validar_fecha('fecha')
    context.fecha_formateada = df_limpio.loc[0, 'fecha']
@then('la fecha formateada debe ser "{esperado}"')
def step_then_la_fecha_formateada_debe_ser(context, esperado):
    assert context.fecha_formateada == esperado, f"Esperado '{esperado}', pero fue '{context.fecha_formateada}'"    

#Fecha invalida
@given('tengo una fecha no válida "{fecha}"')
def step_given_tengo_una_fecha_no_valida(context, fecha):
    context.fecha = fecha
    context.error = None
@when('valido y formateo la fecha no válida')
def step_when_valido_una_fecha_no_valida(context):
    try:
        step_when_valido_y_formateo_la_fecha(context)
    except Exception as e:
        context.error = str(e)
        context.fecha_formateada = None
@then('debería ocurrir un error de fecha no válida')
def step_then_ocurrir_error_fecha_no_valida(context):
    assert context.fecha_formateada is None, "Se esperaba un error de fecha no válida, pero se obtuvo una fecha formateada."
    assert context.error is not None, "Se esperaba un error de fecha no válida, pero no se capturó ningún error."


@given('tengo una fecha valida con puntos "{fecha}"')
def step_given_tengo_una_fecha_valida_con_puntos(context, fecha):
    context.fecha = fecha
    context.error = None
@when('valido y formateo la fecha con puntos')
def step_when_valido_y_formateo_la_fecha_con_puntos(context):
    try:
        context.fecha_formateada = Validations.validar_fecha(context.fecha)
        context.error = None
    except ValueError as e:
        context.error = str(e)
@then('la fecha formateada con puntos debe ser "{esperado}"')
def step_then_la_fecha_formateada_con_puntos_debe_ser(context, esperado):
    assert context.fecha_formateada == esperado, f"Esperado '{esperado}', pero fue '{context.fecha_formateada}'"
# Fecha con comas
@given('tengo una fecha con comas "{fecha}"')
def step_given_tengo_una_fecha_con_comas(context, fecha):
    context.df = pd.DataFrame({'fecha': [fecha]})
    context.validations = Validations(context.df)
    context.error = None

@when('valido y formateo la fecha con comas')
def step_when_valido_y_formateo_la_fecha_con_comas(context):
    try:
        context.df = context.validations.validar_fecha('fecha')
    except ValueError as e:
        context.error = str(e)
@then('la fecha con comas formateada debería dar un error de fecha no válida')
def step_then_la_fecha_con_comas_formateada_deberia_dar_error(context):
    assert context.error == "Fecha no válida", f"Esperado 'Fecha no válida', pero fue '{context.error}'"


#COMPARAR
@given('tengo un DataFrame con la columna "CUIT"')
def step_given_df1(context):
    # Usa los encabezados y filas de la tabla de Behave
    context.df1 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df1["CUIT"] = context.df1["CUIT"].astype(str)
@given('el segundo DataFrame tiene la columna "CUIT"')
def step_given_df2(context):
    context.df2 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df2["CUIT"] = context.df2["CUIT"].astype(str)
@when('comparo la columna "CUIT" y marco en "NoEncontrado"')
def step_when_comparo_cuits(context):
    f = Functions(context.df1)
    f.columns_comparator(context.df2, "CUIT", "NoEncontrado")
    context.resultado = f.df
@then('la columna "NoEncontrado" debe ser')
def step_then_columna_noencontrado(context):
    esperado = [int(row["NoEncontrado"]) for row in context.table]
    # Ordena por CUIT para asegurar el mismo orden
    context.resultado = context.resultado.sort_values("CUIT").reset_index(drop=True)
    obtenido = context.resultado["NoEncontrado"].tolist()
    print("Esperado:", esperado)
    print("Obtenido:", obtenido)
    print(context.resultado)
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


@given('tengo un DataFrame con la columna "CUIT" 2')
def step_given_df1(context):
    context.df1 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df1["CUIT"] = context.df1["CUIT"].astype(str)
@given('el segundo DataFrame tiene la columna "CUIT" 2')
def step_given_df2(context):
    context.df2 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df2["CUIT"] = context.df2["CUIT"].astype(str)
@when('comparo la columna "CUIT" y marco en "NoEncontrado" 2')
def step_when_comparo_cuits(context):
    f = Functions(context.df1)
    f.columns_comparator(context.df2, "CUIT", "NoEncontrado")
    context.resultado = f.df
@then('la columna "NoEncontrado" debe ser 2')
def step_then_columna_noencontrado(context):
    esperado = [int(row["NoEncontrado"]) for row in context.table]
    context.resultado = context.resultado.sort_values("CUIT").reset_index(drop=True)
    obtenido = context.resultado["NoEncontrado"].tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


@given('tengo un DataFrame con la columna "CUIT" 3')
def step_given_df1(context):
    context.df1 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df1["CUIT"] = context.df1["CUIT"].astype(str)
@given('el segundo DataFrame tiene la columna "CUIT" 3')
def step_given_df2(context):
    context.df2 = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df2["CUIT"] = context.df2["CUIT"].astype(str)
@when('comparo la columna "CUIT" y marco en "NoEncontrado" 3')
def step_when_comparo_cuits(context):
    f = Functions(context.df1)
    f.columns_comparator(context.df2, "CUIT", "NoEncontrado")
    context.resultado = f.df
@then('la columna "NoEncontrado" debe ser 3')
def step_then_columna_noencontrado(context):
    esperado = [int(row["NoEncontrado"]) for row in context.table]
    context.resultado = context.resultado.sort_values("CUIT").reset_index(drop=True)
    obtenido = context.resultado["NoEncontrado"].tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


#Receptor
@given('tengo un DataFrame con la columna "Cuit del Receptor"')
def step_given_df_cuit_receptor(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df["Cuit del Receptor"] = context.df["Cuit del Receptor"].astype(str)
@when('controlo el CUIT receptor con "{cuit_esperado}"')
def step_when_cuit_controller(context, cuit_esperado):
    validador = Validations(context.df)
    context.df = validador.cuit_controller(cuit_esperado, columna_cuit="Cuit del Receptor", columna_control="Cuit Receptor Usuario")
@then('la columna "Cuit Receptor Usuario" debe ser')
def step_then_columna_control(context):
    esperado = [int(row["Cuit Receptor Usuario"]) for row in context.table]
    obtenido = context.df["Cuit Receptor Usuario"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"

@given('tengo un DataFrame con la columna "Cuit del Receptor" 2')
def step_given_df_cuit_receptor(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df["Cuit del Receptor"] = context.df["Cuit del Receptor"].astype(str)
@when('controlo el CUIT receptor con "{cuit_esperado}" 2')
def step_when_cuit_controller(context, cuit_esperado):
    validador = Validations(context.df)
    context.df = validador.cuit_controller(cuit_esperado, columna_cuit="Cuit del Receptor", columna_control="Cuit Receptor Usuario")
@then('la columna "Cuit Receptor Usuario" debe ser 2')
def step_then_columna_control(context):
    esperado = [int(row["Cuit Receptor Usuario"]) for row in context.table]
    obtenido = context.df["Cuit Receptor Usuario"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


@given('tengo un DataFrame con la columna "Cuit del Receptor" 3')
def step_given_df_cuit_receptor(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    context.df["Cuit del Receptor"] = context.df["Cuit del Receptor"].astype(str)
@when('controlo el CUIT receptor con "{cuit_esperado}" 3')
def step_when_cuit_controller(context, cuit_esperado):
    validador = Validations(context.df)
    context.df = validador.cuit_controller(cuit_esperado, columna_cuit="Cuit del Receptor", columna_control="Cuit Receptor Usuario")
@then('la columna "Cuit Receptor Usuario" debe ser 3')
def step_then_columna_control(context):
    esperado = [int(row["Cuit Receptor Usuario"]) for row in context.table]
    obtenido = context.df["Cuit Receptor Usuario"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


#Total
@given('tengo un DataFrame con las columnas "A", "B" y "Total"')
def step_given_df_total(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    # Convierte las columnas numéricas a int
    for col in ["A", "B", "Total"]:
        context.df[col] = context.df[col].astype(int)
@when('controlo la suma de ["A", "B"] contra "Total" en "Control"')
def step_when_total_controller(context):
    validador = Validations(context.df)
    context.df = validador.total_controller(["A", "B"], "Total", "Control")
@then('la columna "Control" debe ser')
def step_then_columna_control(context):
    esperado = [int(row["Control"]) for row in context.table]
    obtenido = context.df["Control"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


@given('tengo un DataFrame con las columnas "A", "B" y "Total" negativo')
def step_given_df_total(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    for col in ["A", "B", "Total"]:
        context.df[col] = context.df[col].astype(int)
@when('controlo la suma de ["A", "B"] contra "Total" en "Control" negativo')
def step_when_total_controller(context):
    validador = Validations(context.df)
    context.df = validador.total_controller(["A", "B"], "Total", "Control")
@then('la columna "Control" debe ser negativo')
def step_then_columna_control(context):
    esperado = [int(row["Control"]) for row in context.table]
    obtenido = context.df["Control"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"



@given('tengo un DataFrame con las columnas "A", "B" y "Total" mixto')
def step_given_df_total(context):
    context.df = pd.DataFrame([list(row.cells) for row in context.table], columns=context.table.headings)
    for col in ["A", "B", "Total"]:
        context.df[col] = context.df[col].astype(int)

@when('controlo la suma de ["A", "B"] contra "Total" en "Control" mixto')
def step_when_total_controller(context):
    validador = Validations(context.df)
    context.df = validador.total_controller(["A", "B"], "Total", "Control")

@then('la columna "Control" debe ser mixto')
def step_then_columna_control(context):
    esperado = [int(row["Control"]) for row in context.table]
    obtenido = context.df["Control"].astype(int).tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


#Concateneitor
@given('que tengo un DataFrame con las columnas "A" y "B"')
def step_given_dataframe_ab(context):
    data = [row.as_dict() for row in context.table]
    data = [{k.strip(): v.strip() for k, v in row.items()} for row in data]
    context.df = pd.DataFrame(data)
@when('concateno las columnas ["A", "B"] en "Concatenado" usando el separador "-"')
def step_when_concateno_ab(context):
    funciones = Functions(context.df)
    context.df = funciones.columns_concatenator(["A", "B"], "Concatenado", "-")
@then('la columna "Concatenado" debe ser')
def step_then_concatenado(context):
    esperado = [row["Concatenado"] for row in context.table]
    obtenido = context.df["Concatenado"].tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"


@given('que tengo un DataFrame con las columnas "X", "Y", "Z"')
def step_given_dataframe_xyz(context):
    data = [row.as_dict() for row in context.table]
    data = [{k.strip(): v.strip() for k, v in row.items()} for row in data]
    context.df = pd.DataFrame(data)
@when('concateno las columnas ["X", "Y", "Z"] en "Junto" usando el separador ""')
def step_when_concateno_xyz(context):
    funciones = Functions(context.df)
    context.df = funciones.columns_concatenator(["X", "Y", "Z"], "Junto", "")
@then('la columna "Junto" debe ser')
def step_then_junto(context):
    esperado = [row["Junto"] for row in context.table]
    obtenido = context.df["Junto"].tolist()
    assert esperado == obtenido, f"Esperado {esperado}, pero fue {obtenido}"