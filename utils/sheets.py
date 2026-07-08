import streamlit as st
import pandas as pd
import gspread
import json
import os

from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

@st.cache_resource
def conectar_gsheet():
    # Intentar obtener credenciales desde variable de entorno (Render)
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    if creds_json:
        # Usar credenciales desde variable de entorno
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        # Usar archivo local (desarrollo)
        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
        )
    
    cliente = gspread.authorize(creds)
    return cliente.open_by_key("1E-pObaKgYJpkJ7olPoe0swKq4ds9tKvFqKtG5wJ63l0")

@st.cache_resource
def obtener_hoja(nombre_hoja):

    libro = conectar_gsheet()

    return libro.worksheet(nombre_hoja)

@st.cache_data(ttl=300)
def leer_hoja(nombre_hoja):
    hoja = obtener_hoja(nombre_hoja)
    return pd.DataFrame(hoja.get_all_records())

def limpiar_cache():
    """
    Limpia el caché de todas las funciones decoradas con @st.cache_data
    """
    leer_hoja.clear()

# ==========================================
# BANCOS
# ==========================================

def actualizar_banco(
    id_banco,
    fecha,
    empresa,
    galicia_saldo,
    galicia_fci,
    macro_saldo,
    macro_fci,
    credicoop_saldo,
    credicoop_fci,
    santander_saldo,
    santander_fci
):

    hoja = obtener_hoja("Bancos")

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_banco:

            hoja.update(
                f"A{i}:K{i}",
                [[
                    id_banco,
                    fecha,
                    empresa,
                    galicia_saldo,
                    galicia_fci,
                    macro_saldo,
                    macro_fci,
                    credicoop_saldo,
                    credicoop_fci,
                    santander_saldo,
                    santander_fci
                ]]
            )

            break

    limpiar_cache()

def eliminar_banco(id_banco):

    hoja = obtener_hoja("Bancos")

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_banco:

            hoja.delete_rows(i)

            break

    limpiar_cache()

# ==========================================
# QUILMES
# ==========================================

def actualizar_quilmes(
    id_quilmes,
    fecha,
    empresa,
    deuda,
    promesa_nc,
    cheques,
    depositos,
    efectivo
):

    hoja = obtener_hoja("Quilmes")

    necesidad = (
        deuda
        - (
            promesa_nc
            + cheques
            + depositos
            + efectivo
        )
    )

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_quilmes:

            hoja.update(
                f"A{i}:I{i}",
                [[
                    id_quilmes,
                    fecha,
                    empresa,
                    deuda,
                    promesa_nc,
                    cheques,
                    depositos,
                    efectivo,
                    necesidad
                ]]
            )

            break

    limpiar_cache()

def eliminar_quilmes(id_quilmes):

    hoja = obtener_hoja("Quilmes")

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_quilmes:

            hoja.delete_rows(i)

            break

    limpiar_cache()

# ==========================================
# PLAZOS FIJOS
# ==========================================

def actualizar_plazo_fijo(
    id_pf,
    fecha,
    empresa,
    banco,
    capital,
    tasa,
    vencimiento
):

    hoja = obtener_hoja("PlazosFijos")

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_pf:

            hoja.update(
                f"A{i}:G{i}",
                [[
                    id_pf,
                    fecha,
                    empresa,
                    banco,
                    capital,
                    tasa,
                    vencimiento
                ]]
            )

            break

    limpiar_cache()

def eliminar_plazo_fijo(id_pf):

    hoja = obtener_hoja("PlazosFijos")

    registros = hoja.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if fila["ID"] == id_pf:

            hoja.delete_rows(i)

            break

    limpiar_cache()

# ==========================================
# CONFIGURACIÓN
# ==========================================

def generar_id_config():
    """
    Genera un nuevo ID para la tabla de configuración
    """
    hoja = obtener_hoja("Config")
    
    registros = hoja.get_all_records()
    
    if not registros:
        return 1
    
    ids = []
    for fila in registros:
        try:
            ids.append(int(fila["ID"]))
        except:
            pass
    
    return max(ids) + 1 if ids else 1

def actualizar_config_por_id(id_registro, tipo, nuevo_valor, nuevo_extra, activo):
    """
    Actualiza una configuración existente por su ID
    """
    hoja = obtener_hoja("Config")
    
    registros = hoja.get_all_records()
    
    for i, fila in enumerate(registros, start=2):
        if str(fila["ID"]) == str(id_registro):
            hoja.update(
                f"A{i}:E{i}",
                [[
                    id_registro,
                    tipo,
                    nuevo_valor,
                    nuevo_extra,
                    activo
                ]]
            )
            break
    
    limpiar_cache()

# ==========================================
# CIERRE DE CAJA
# ==========================================

def actualizar_cierre_caja(
    id_caja,
    fecha,
    empresa,
    efectivo,
    cheques,
    echeq
):
    """
    Actualiza un registro de Cierre de Caja existente
    """
    hoja = obtener_hoja("CierreCaja")
    
    registros = hoja.get_all_records()
    
    # ✅ Convertir fecha a string
    fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, 'strftime') else str(fecha)
    
    for i, fila in enumerate(registros, start=2):
        if str(fila["ID"]) == str(id_caja):
            hoja.update(
                f"A{i}:F{i}",
                [[
                    id_caja,
                    fecha_str,  # ✅ Usar fecha_str
                    empresa,
                    efectivo,
                    cheques,
                    echeq
                ]]
            )
            break
    
    limpiar_cache()

def eliminar_cierre_caja(id_caja):
    """
    Elimina un registro de Cierre de Caja por su ID
    """
    hoja = obtener_hoja("CierreCaja")
    
    registros = hoja.get_all_records()
    
    for i, fila in enumerate(registros, start=2):
        if str(fila["ID"]) == str(id_caja):
            hoja.delete_rows(i)
            break
    
    limpiar_cache()

def guardar_cierre_caja(
    fecha,
    empresa,
    efectivo,
    cheques,
    echeq
):

    hoja = obtener_hoja("CierreCaja")

    registros = hoja.get_all_records()

    if registros:
        ultimo_id = max(
            int(f["ID"])
            for f in registros
            if str(f["ID"]).strip() != ""
        ) + 1
    else:
        ultimo_id = 1

    # ✅ Convertir fecha a string
    fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, 'strftime') else str(fecha)

    hoja.append_row([
        ultimo_id,
        fecha_str,
        empresa,
        efectivo,
        cheques,
        echeq
    ])

    limpiar_cache()

    return ultimo_id

def obtener_cierre_caja(id_caja):

    df = leer_hoja("CierreCaja")

    if df.empty:

        return None

    fila = df[
        df["ID"].astype(str) == str(id_caja)
    ]

    if fila.empty:

        return None

    return fila.iloc[0].to_dict()

def obtener_todas_cajas():
    """
    Obtiene todos los registros de Cierre de Caja
    """
    return leer_hoja("CierreCaja")

# ==========================================
# DEPURACIÓN MASIVA
# ==========================================

def eliminar_cierres_antiguos(fecha_limite):
    """
    Elimina todos los cierres de caja anteriores a una fecha límite
    Retorna la cantidad de registros eliminados
    """
    hoja = obtener_hoja("CierreCaja")
    
    registros = hoja.get_all_records()
    fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
    
    filas_eliminar = []
    
    for i, fila in enumerate(registros, start=2):
        try:
            fecha_reg = fila.get("Fecha", "")
            if fecha_reg and fecha_reg < fecha_limite_str:
                filas_eliminar.append(i)
        except:
            pass
    
    for fila in reversed(filas_eliminar):
        hoja.delete_rows(fila)
    
    limpiar_cache()
    
    return len(filas_eliminar)


def eliminar_bancos_antiguos(fecha_limite):
    """
    Elimina todos los registros bancarios anteriores a una fecha límite
    Retorna la cantidad de registros eliminados
    """
    hoja = obtener_hoja("Bancos")
    
    registros = hoja.get_all_records()
    fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
    
    filas_eliminar = []
    
    for i, fila in enumerate(registros, start=2):
        try:
            fecha_reg = fila.get("Fecha", "")
            if fecha_reg and fecha_reg < fecha_limite_str:
                filas_eliminar.append(i)
        except:
            pass
    
    for fila in reversed(filas_eliminar):
        hoja.delete_rows(fila)
    
    limpiar_cache()
    
    return len(filas_eliminar)


def eliminar_quilmes_antiguos(fecha_limite):
    """
    Elimina todos los registros de Quilmes anteriores a una fecha límite
    Retorna la cantidad de registros eliminados
    """
    hoja = obtener_hoja("Quilmes")
    
    registros = hoja.get_all_records()
    fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
    
    filas_eliminar = []
    
    for i, fila in enumerate(registros, start=2):
        try:
            fecha_reg = fila.get("Fecha", "")
            if fecha_reg and fecha_reg < fecha_limite_str:
                filas_eliminar.append(i)
        except:
            pass
    
    for fila in reversed(filas_eliminar):
        hoja.delete_rows(fila)
    
    limpiar_cache()
    
    return len(filas_eliminar)

# ==========================================
# UTILIDADES
# ==========================================

def obtener_dataframe(nombre_hoja):
    return leer_hoja(nombre_hoja)