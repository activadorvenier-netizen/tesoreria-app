import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from utils.sheets import (
    obtener_hoja,
    leer_hoja,
    obtener_dataframe,
    limpiar_cache
)
from utils.layout import mostrar_sidebar

# ✅ Configurar la página
st.set_page_config(
    page_title="Tesorería - Créditos",
    page_icon="📊",
    layout="wide"
)

mostrar_sidebar()

st.title("📊 Créditos")

# ============================================
# FUNCIONES CON CACHÉ
# ============================================

@st.cache_data(ttl=60)
def obtener_creditos():
    """Obtiene todos los créditos con caché"""
    hoja = obtener_hoja("Creditos")
    return pd.DataFrame(hoja.get_all_records())

@st.cache_data(ttl=60)
def obtener_amortizacion():
    """Obtiene todas las amortizaciones con caché"""
    hoja = obtener_hoja("Amortizacion")
    return pd.DataFrame(hoja.get_all_records())

def limpiar_cache_creditos():
    """Limpia el caché de créditos y amortización"""
    obtener_creditos.clear()
    obtener_amortizacion.clear()
    st.cache_data.clear()

# ============================================
# FUNCIONES
# ============================================

def limpiar_numero(valor):
    """
    Limpia un valor para convertirlo a float.
    Maneja strings con $, comas, puntos, etc.
    """
    if valor is None:
        return 0.0
    
    if isinstance(valor, (int, float)):
        return float(valor)
    
    if isinstance(valor, str):
        valor = valor.replace("$", "").strip()
        if valor == "":
            return 0.0
        valor = valor.replace(",", "").replace(".", "")
        try:
            return float(valor)
        except:
            return 0.0
    
    return 0.0

def formato_moneda(valor):
    """
    Convierte un valor a formato de moneda.
    """
    valor = limpiar_numero(valor)
    return f"$ {valor:,.0f}".replace(",", ".")

def calcular_cuota(monto, tasa, cuotas):
    """
    Calcula la cuota mensual de un préstamo usando la fórmula de interés compuesto (método francés)
    """
    monto = limpiar_numero(monto)
    tasa = limpiar_numero(tasa)
    cuotas = int(limpiar_numero(cuotas)) if cuotas else 0
    
    if monto == 0 or cuotas == 0:
        return 0
        
    if tasa == 0:
        return monto / cuotas
    tasa_mensual = tasa / 100 / 12
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** cuotas) / ((1 + tasa_mensual) ** cuotas - 1)
    return cuota

def generar_amortizacion(monto, tasa, cuotas, fecha_inicio):
    """
    Genera el cronograma de amortización
    """
    monto = limpiar_numero(monto)
    tasa = limpiar_numero(tasa)
    cuotas = int(limpiar_numero(cuotas)) if cuotas else 0
    
    if monto == 0 or cuotas == 0:
        return []
        
    cuota_mensual = calcular_cuota(monto, tasa, cuotas)
    saldo = monto
    amortizacion = []
    tasa_mensual = tasa / 100 / 12 if tasa > 0 else 0
    
    for i in range(cuotas):
        fecha = fecha_inicio + relativedelta(months=i+1)
        if tasa > 0:
            interes = saldo * tasa_mensual
            capital = cuota_mensual - interes
        else:
            capital = cuota_mensual
            interes = 0
        saldo -= capital
        amortizacion.append({
            "Fecha": fecha,
            "Cuota": cuota_mensual,
            "Capital": capital,
            "Interes": interes,
            "Saldo": max(saldo, 0),
            "Pagada": "NO"
        })
    
    return amortizacion

def asegurar_tipos_nativos(valor):
    """
    Convierte un valor a un tipo nativo de Python (int, float, str)
    para evitar errores de serialización JSON.
    """
    if isinstance(valor, (np.int64, np.int32)):
        return int(valor)
    elif isinstance(valor, (np.float64, np.float32)):
        return float(valor)
    elif isinstance(valor, np.bool_):
        return bool(valor)
    elif isinstance(valor, np.datetime64):
        return str(valor)
    else:
        return valor

# ============================================
# INICIALIZAR HOJAS
# ============================================

hoja_creditos = obtener_hoja("Creditos")
hoja_amortizacion = obtener_hoja("Amortizacion")

empresas = ["Venier", "Venbiere", "NRV"]
bancos = ["Santander", "BBVA", "Galicia", "Macro", "Credicoop"]
destinos = ["Camión", "Efectivo", "Inversión", "Otro"]

# ============================================
# ESTADOS
# ============================================

if "editando_credito" not in st.session_state:
    st.session_state.editando_credito = None

if "eliminar_credito" not in st.session_state:
    st.session_state.eliminar_credito = None

if "credito_seleccionado" not in st.session_state:
    st.session_state.credito_seleccionado = None

if "confirmar_credito" not in st.session_state:
    st.session_state.confirmar_credito = None

if "cuotas_manuales" not in st.session_state:
    st.session_state.cuotas_manuales = []

if "mensaje_creditos" in st.session_state:
    st.success(st.session_state["mensaje_creditos"])
    st.balloons()
    del st.session_state["mensaje_creditos"]

# ============================================
# TABS POR EMPRESA
# ============================================

st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"]{
    gap:10px;
}
.stTabs [data-baseweb="tab"]{
    height:52px;
    padding-left:25px;
    padding-right:25px;
    border-radius:12px 12px 0 0;
    background:#F5F6F8;
    border:1px solid #D9D9D9;
    font-weight:600;
}
.stTabs [aria-selected="true"]{
    background:#6A1B9A !important;
    color:white !important;
    border:none;
}
/* Estilos para tablero compacto */
div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 2px 0;
}
div[data-testid="metric-container"] label {
    font-size: 12px !important;
    color: #555 !important;
}
div[data-testid="metric-container"] div {
    font-size: 18px !important;
    font-weight: bold !important;
}
/* Evitar truncamiento de texto */
div[data-testid="stMarkdownContainer"] p {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    word-break: break-word !important;
}
/* Tarjetas más compactas */
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
    gap: 2px !important;
}
div[data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}
div[data-testid="column"] {
    padding: 0 4px !important;
}
</style>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "🏢 Venier",
    "🍺 Venbiere",
    "📦 NRV"
])

for tab, empresa in zip(tabs, empresas):
    with tab:
        
        # ==========================================
        # BOTÓN PARA LIMPIAR CACHÉ
        # ==========================================
        
        col1, col2 = st.columns([6, 3])
        with col2:
            if st.button("🔄 Limpiar Caché", key=f"clear_cache_{empresa}", use_container_width=True):
                limpiar_cache_creditos()
                st.rerun()
        
        st.divider()
        
        # ==========================================
        # FORMULARIO NUEVO CRÉDITO POR EMPRESA
        # ==========================================
        
        with st.container(border=True):
            st.subheader(f"➕ Nuevo Crédito - {empresa}")
            
            # Verificar si hay un crédito pendiente de confirmación
            if st.session_state.confirmar_credito and st.session_state.confirmar_credito.get("empresa") == empresa:
                
                # ==========================================
                # MODO CONFIRMACIÓN
                # ==========================================
                
                credito_data = st.session_state.confirmar_credito
                
                st.info("📋 Revisa los datos del crédito antes de confirmar")
                
                # Si el crédito tiene interés y no tiene cuotas manuales cargadas, ofrecer la opción
                if credito_data['tasa'] > 0 and not credito_data.get('cuotas_manual', False):
                    with st.expander("📋 Cargar Cuotas Manualmente", expanded=True):
                        st.info("Ingresa las cuotas que el banco te ha proporcionado")
                        
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            fecha_cuota = st.date_input(
                                "Fecha",
                                value=date.today(),
                                key=f"fecha_cuota_manual_confirm_{empresa}"
                            )
                        
                        with col2:
                            monto_cuota = st.number_input(
                                "Monto",
                                min_value=0.0,
                                value=0.0,
                                step=1000.0,
                                key=f"monto_cuota_manual_confirm_{empresa}"
                            )
                        
                        with col3:
                            if st.button("➕ Agregar Cuota", key=f"agregar_cuota_confirm_{empresa}", use_container_width=True):
                                if monto_cuota > 0:
                                    st.session_state.cuotas_manuales.append({
                                        "fecha": fecha_cuota.strftime("%Y-%m-%d"),
                                        "monto": monto_cuota
                                    })
                                    st.rerun()
                        
                        if st.session_state.cuotas_manuales:
                            st.divider()
                            st.markdown("**📋 Cuotas cargadas:**")
                            
                            df_cuotas = pd.DataFrame(st.session_state.cuotas_manuales)
                            df_cuotas["Monto"] = df_cuotas["monto"].apply(lambda x: formato_moneda(x))
                            
                            st.dataframe(
                                df_cuotas[["fecha", "Monto"]],
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "fecha": "Fecha",
                                    "Monto": "Monto"
                                }
                            )
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Usar Cuotas Manuales", type="primary", key=f"usar_cuotas_manuales_{empresa}", use_container_width=True):
                                    credito_data['cuotas_manual'] = True
                                    credito_data['cuotas_manual_list'] = st.session_state.cuotas_manuales.copy()
                                    st.session_state.confirmar_credito = credito_data
                                    st.rerun()
                            
                            with col2:
                                if st.button("🗑️ Limpiar Cuotas", key=f"limpiar_cuotas_confirm_{empresa}", use_container_width=True):
                                    st.session_state.cuotas_manuales = []
                                    st.rerun()
                        else:
                            st.info("No hay cuotas cargadas aún. Agrega las cuotas manualmente.")
                
                # Mostrar resumen
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏦 Datos del Crédito**")
                    st.write(f"Empresa: {credito_data['empresa']}")
                    st.write(f"Banco: {credito_data['banco']}")
                    st.write(f"Monto: {formato_moneda(credito_data['monto'])}")
                    st.write(f"Cuotas: {credito_data['cuotas']}")
                    st.write(f"Tasa: {credito_data['tasa']}%")
                    st.write(f"Fecha Inicio: {credito_data['fecha_inicio']}")
                    st.write(f"Destino: {credito_data['destino']}")
                
                with col2:
                    st.markdown("**💰 Resumen**")
                    if credito_data.get('cuotas_manual', False):
                        st.write("📋 **Cuotas cargadas manualmente**")
                        st.write(f"Total de cuotas: {len(credito_data['cuotas_manual_list'])}")
                        total_cuotas = sum([c['monto'] for c in credito_data['cuotas_manual_list']])
                        st.write(f"Total a Pagar: {formato_moneda(total_cuotas)}")
                    else:
                        cuota_mensual = calcular_cuota(credito_data['monto'], credito_data['tasa'], credito_data['cuotas'])
                        total = cuota_mensual * credito_data['cuotas']
                        st.write(f"Cuota Mensual: {formato_moneda(cuota_mensual)}")
                        st.write(f"Total a Pagar: {formato_moneda(total)}")
                        st.write(f"Interés Total: {formato_moneda(total - credito_data['monto'])}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Confirmar Carga", type="primary", use_container_width=True):
                        registros = hoja_creditos.get_all_records()
                        if registros:
                            ids = []
                            for r in registros:
                                try:
                                    if str(r["ID"]).strip() != "":
                                        ids.append(int(r["ID"]))
                                except:
                                    pass
                            ultimo_id = max(ids) + 1 if ids else 1
                        else:
                            ultimo_id = 1
                        
                        fecha_inicio = datetime.strptime(credito_data['fecha_inicio'], "%Y-%m-%d").date()
                        fecha_fin = fecha_inicio + relativedelta(months=int(credito_data['cuotas']))
                        
                        hoja_creditos.append_row([
                            int(ultimo_id),
                            str(credito_data['empresa']),
                            str(credito_data['banco']),
                            float(credito_data['monto']),
                            int(credito_data['cuotas']),
                            float(credito_data['tasa']),
                            fecha_inicio.strftime("%Y-%m-%d"),
                            fecha_fin.strftime("%Y-%m-%d"),
                            str(credito_data['destino'])
                        ])
                        
                        if credito_data.get('cuotas_manual', False):
                            for cuota in credito_data['cuotas_manual_list']:
                                hoja_amortizacion.append_row([
                                    int(ultimo_id),
                                    cuota['fecha'],
                                    float(cuota['monto']),
                                    0,
                                    "NO"
                                ])
                                time.sleep(0.1)
                        else:
                            amortizacion = generar_amortizacion(
                                credito_data['monto'], 
                                credito_data['tasa'], 
                                credito_data['cuotas'], 
                                fecha_inicio
                            )
                            for item in amortizacion:
                                hoja_amortizacion.append_row([
                                    int(ultimo_id),
                                    item["Fecha"].strftime("%Y-%m-%d"),
                                    float(item["Cuota"]),
                                    float(item["Saldo"]),
                                    "NO"
                                ])
                                time.sleep(0.1)
                        
                        limpiar_cache_creditos()
                        st.session_state.confirmar_credito = None
                        st.session_state.cuotas_manuales = []
                        st.session_state["mensaje_creditos"] = f"✅ Crédito para {empresa} guardado correctamente!"
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.confirmar_credito = None
                        st.session_state.cuotas_manuales = []
                        st.rerun()
            
            else:
                
                # ==========================================
                # MODO FORMULARIO
                # ==========================================
                
                with st.form(key=f"form_credito_{empresa}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        banco = st.selectbox(
                            "Banco",
                            options=[""] + bancos,
                            key=f"banco_{empresa}"
                        )
                        
                        monto = st.number_input(
                            "Monto del Préstamo",
                            min_value=0.0,
                            value=None,
                            step=100000.0,
                            key=f"monto_{empresa}",
                            placeholder="0.00"
                        )
                        
                        cuotas = st.number_input(
                            "Cantidad de Cuotas",
                            min_value=1,
                            value=None,
                            step=1,
                            key=f"cuotas_{empresa}",
                            placeholder="12"
                        )
                    
                    with col2:
                        tasa = st.number_input(
                            "Tasa Anual (%)",
                            min_value=0.0,
                            value=None,
                            step=0.1,
                            key=f"tasa_{empresa}",
                            placeholder="0.00",
                            help="Ej: 26% → ingresar 26"
                        )
                        
                        fecha_inicio = st.date_input(
                            "Fecha de Inicio",
                            value=None,
                            key=f"fecha_inicio_{empresa}"
                        )
                        
                        destino = st.selectbox(
                            "Destino del Crédito",
                            options=[""] + destinos,
                            key=f"destino_{empresa}"
                        )
                    
                    # Mostrar resumen del crédito (solo si hay datos)
                    if monto and cuotas and monto > 0 and cuotas > 0:
                        tasa_valor = tasa if tasa else 0
                        cuota_mensual = calcular_cuota(monto, tasa_valor, cuotas)
                        st.divider()
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("💰 Cuota Mensual", formato_moneda(cuota_mensual))
                        with col2:
                            st.metric("📊 Total a Pagar", formato_moneda(cuota_mensual * cuotas))
                        with col3:
                            st.metric("💸 Interés Total", formato_moneda((cuota_mensual * cuotas) - monto))
                    
                    if st.form_submit_button("💾 Guardar Crédito", type="primary", use_container_width=True):
                        if not banco:
                            st.error("⚠️ Por favor seleccione un banco")
                        elif not monto or monto <= 0:
                            st.error("⚠️ Por favor ingrese un monto válido")
                        elif not cuotas or cuotas <= 0:
                            st.error("⚠️ Por favor ingrese la cantidad de cuotas")
                        elif tasa is None:
                            st.error("⚠️ Por favor ingrese la tasa")
                        elif not fecha_inicio:
                            st.error("⚠️ Por favor seleccione una fecha de inicio")
                        elif not destino:
                            st.error("⚠️ Por favor seleccione un destino")
                        else:
                            st.session_state.confirmar_credito = {
                                "empresa": empresa,
                                "banco": banco,
                                "monto": monto,
                                "cuotas": cuotas,
                                "tasa": tasa,
                                "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                                "destino": destino,
                                "cuotas_manual": False,
                                "cuotas_manual_list": []
                            }
                            st.session_state.cuotas_manuales = []
                            st.rerun()
        
        # ==========================================
        # TABLERO DE CONTROL (SOLO VIGENTES)
        # ==========================================
        
        st.subheader("📊 Tablero de Control - Créditos Vigentes")
        
        df_creditos_all = obtener_creditos()
        df_amort_all = obtener_amortizacion()
        
        if not df_creditos_all.empty:
            
            df_creditos_emp = df_creditos_all[df_creditos_all["Empresa"] == empresa]
            
            # Filtrar solo créditos vigentes (con cuotas pendientes)
            creditos_vigentes = []
            for _, credito in df_creditos_emp.iterrows():
                df_amort_cred = df_amort_all[df_amort_all["ID Credito"] == credito["ID"]]
                if not df_amort_cred.empty:
                    cuotas_pendientes = df_amort_cred[df_amort_cred.get("Pagada", "NO") != "SI"]
                    if not cuotas_pendientes.empty:
                        creditos_vigentes.append(credito)
            
            if creditos_vigentes:
                df_vigentes = pd.DataFrame(creditos_vigentes)
                
                total_creditos = len(df_vigentes)
                montos = [limpiar_numero(m) for m in df_vigentes["Monto"]]
                monto_total = sum(montos)
                
                saldo_total = 0
                for _, credito in df_vigentes.iterrows():
                    df_amort_cred = df_amort_all[df_amort_all["ID Credito"] == credito["ID"]]
                    if not df_amort_cred.empty:
                        df_amort_cred_pendientes = df_amort_cred[df_amort_cred.get("Pagada", "NO") != "SI"]
                        saldo_total += df_amort_cred_pendientes["Cuota"].sum() if not df_amort_cred_pendientes.empty else 0
                
                pct_pagado = ((monto_total - saldo_total) / monto_total * 100) if monto_total > 0 else 0
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("📊 Créditos Vigentes", total_creditos)
                    st.metric("💰 Monto Total", formato_moneda(monto_total))
                
                with col2:
                    st.metric("💸 Saldo Total", formato_moneda(saldo_total))
                    st.metric("📈 % Pagado", f"{pct_pagado:.1f}%")
            else:
                st.info("✅ No hay créditos vigentes para esta empresa")
        else:
            st.info("📭 No hay créditos registrados aún.")
        
        # ==========================================
        # TABLERO DE PROYECCIÓN DE PAGOS
        # ==========================================

        st.divider()
        st.subheader("📅 Proyección de Pagos Mensuales")

        df_creditos_all = obtener_creditos()
        df_amort_all = obtener_amortizacion()

        if not df_creditos_all.empty and not df_amort_all.empty:
            
            # Obtener todas las cuotas pendientes
            cuotas_pendientes = []
            
            for _, credito in df_creditos_all.iterrows():
                df_amort_cred = df_amort_all[df_amort_all["ID Credito"] == credito["ID"]]
                if not df_amort_cred.empty:
                    # Filtrar solo cuotas pendientes
                    cuotas_pendientes_cred = df_amort_cred[df_amort_cred.get("Pagada", "NO") != "SI"]
                    for _, cuota in cuotas_pendientes_cred.iterrows():
                        cuotas_pendientes.append({
                            "ID Credito": credito["ID"],
                            "Empresa": credito["Empresa"],
                            "Banco": credito["Banco"],
                            "Fecha": cuota["Fecha"],
                            "Cuota": limpiar_numero(cuota["Cuota"])
                        })
            
            if cuotas_pendientes:
                df_cuotas = pd.DataFrame(cuotas_pendientes)
                df_cuotas["Fecha"] = pd.to_datetime(df_cuotas["Fecha"])
                df_cuotas["Mes"] = df_cuotas["Fecha"].dt.strftime("%Y-%m")
                df_cuotas["Mes_Texto"] = df_cuotas["Fecha"].dt.strftime("%B %Y")
                
                # Crear opciones de meses disponibles
                meses_disponibles = sorted(df_cuotas["Mes"].unique(), reverse=True)
                opciones_meses = []
                for mes in meses_disponibles:
                    fecha_temp = datetime.strptime(mes, "%Y-%m")
                    opciones_meses.append({
                        "key": mes,
                        "label": fecha_temp.strftime("%B %Y")
                    })
                
                # Selector de mes
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    # ✅ Clave única por empresa
                    mes_seleccionado_key = st.selectbox(
                        "Seleccionar Mes",
                        options=[m["key"] for m in opciones_meses],
                        format_func=lambda x: next(m["label"] for m in opciones_meses if m["key"] == x),
                        key=f"mes_proyeccion_{empresa}"
                    )
                
                # Filtrar cuotas del mes seleccionado
                df_cuotas_mes = df_cuotas[df_cuotas["Mes"] == mes_seleccionado_key]
                
                if not df_cuotas_mes.empty:
                    
                    # Calcular total por empresa
                    total_por_empresa = df_cuotas_mes.groupby("Empresa")["Cuota"].sum().reset_index()
                    total_general = df_cuotas_mes["Cuota"].sum()
                    
                    # Mostrar resumen
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric(
                            "💰 Total Cuotas del Mes",
                            formato_moneda(total_general)
                        )
                    
                    with col2:
                        st.markdown("**📊 Desglose por Empresa**")
                        cols = st.columns(len(total_por_empresa))
                        for i, (_, row) in enumerate(total_por_empresa.iterrows()):
                            with cols[i]:
                                st.metric(
                                    f"🏢 {row['Empresa']}",
                                    formato_moneda(row['Cuota'])
                                )
                    
                    # Agregar detalle de cuotas del mes
                    with st.expander("📋 Ver detalle de cuotas del mes", expanded=False):
                        df_detalle = df_cuotas_mes.copy()
                        df_detalle["Cuota"] = df_detalle["Cuota"].apply(lambda x: formato_moneda(x))
                        df_detalle["Fecha"] = df_detalle["Fecha"].dt.strftime("%d/%m/%Y")
                        
                        st.dataframe(
                            df_detalle[["Fecha", "Empresa", "Banco", "Cuota"]],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Fecha": "Fecha",
                                "Empresa": "Empresa",
                                "Banco": "Banco",
                                "Cuota": "Cuota"
                            }
                        )
                    
                else:
                    st.info(f"📭 No hay cuotas pendientes para el mes seleccionado")
                    
                    # Mostrar próximos meses con cuotas
                    st.markdown("**📅 Próximos meses con cuotas pendientes:**")
                    meses_futuros = sorted(df_cuotas["Mes"].unique())
                    for mes in meses_futuros[:6]:
                        fecha_temp = datetime.strptime(mes, "%Y-%m")
                        count = len(df_cuotas[df_cuotas["Mes"] == mes])
                        st.write(f"🗓️ {fecha_temp.strftime('%B %Y')}: {count} cuotas pendientes")
            else:
                st.success("✅ No hay cuotas pendientes en ningún crédito")
        else:
            st.info("📭 No hay créditos o cuotas registradas aún.")
        
        st.divider()
        
        # ==========================================
        # LISTADO CON BUSCADOR
        # ==========================================
        
        st.subheader(f"📋 Créditos - {empresa}")
        
        df_creditos = obtener_creditos()
        
        if df_creditos.empty or 'Empresa' not in df_creditos.columns:
            st.info(f"📭 No hay créditos para {empresa}")
        else:
            df_creditos_emp = df_creditos[df_creditos["Empresa"] == empresa]
            
            if df_creditos_emp.empty:
                st.info(f"📭 No hay créditos para {empresa}")
            else:
                if 'Fecha Inicio' in df_creditos_emp.columns:
                    df_creditos_emp = df_creditos_emp.sort_values("Fecha Inicio", ascending=False)
                
                if 'Monto' in df_creditos_emp.columns:
                    df_creditos_emp['Monto'] = df_creditos_emp['Monto'].apply(limpiar_numero)
                if 'Cuotas' in df_creditos_emp.columns:
                    df_creditos_emp['Cuotas'] = df_creditos_emp['Cuotas'].apply(limpiar_numero)
                if 'Tasa' in df_creditos_emp.columns:
                    df_creditos_emp['Tasa'] = df_creditos_emp['Tasa'].apply(limpiar_numero)
                
                opciones = ["-- Seleccione un crédito --"]
                for _, fila in df_creditos_emp.iterrows():
                    monto_limpio = limpiar_numero(fila['Monto'])
                    fecha_str = fila['Fecha Inicio'].strftime("%Y-%m-%d") if hasattr(fila['Fecha Inicio'], 'strftime') else str(fila['Fecha Inicio'])
                    opciones.append(f"{fila['Banco']} - ${monto_limpio:,.0f} - {fecha_str}")
                
                seleccion = st.selectbox(
                    "🔍 Buscar crédito",
                    options=opciones,
                    key=f"selector_{empresa}"
                )
                
                credito_seleccionado_id = None
                if seleccion and seleccion != "-- Seleccione un crédito --":
                    for _, fila in df_creditos_emp.iterrows():
                        monto_limpio = limpiar_numero(fila['Monto'])
                        fecha_str = fila['Fecha Inicio'].strftime("%Y-%m-%d") if hasattr(fila['Fecha Inicio'], 'strftime') else str(fila['Fecha Inicio'])
                        opcion = f"{fila['Banco']} - ${monto_limpio:,.0f} - {fecha_str}"
                        if opcion == seleccion:
                            credito_seleccionado_id = fila["ID"]
                            break
                
                if credito_seleccionado_id:
                    
                    fila = df_creditos_emp[df_creditos_emp["ID"] == credito_seleccionado_id].iloc[0]
                    
                    df_amort = obtener_amortizacion()
                    
                    if not df_amort.empty and 'ID Credito' in df_amort.columns:
                        df_amort_cred = df_amort[df_amort["ID Credito"] == fila["ID"]]
                    else:
                        df_amort_cred = pd.DataFrame()
                    
                    monto_valor = limpiar_numero(fila['Monto'])
                    cuotas_valor = int(limpiar_numero(fila['Cuotas'])) if limpiar_numero(fila['Cuotas']) > 0 else 0
                    tasa_valor = limpiar_numero(fila['Tasa'])
                    cuota_mensual = calcular_cuota(monto_valor, tasa_valor, cuotas_valor)
                    
                    if st.session_state.editando_credito == fila["ID"]:
                        
                        st.subheader(f"✏️ Editando Crédito {fila['ID']}")
                        
                        with st.form(key=f"edit_cred_form_{fila['ID']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                banco_edit = st.selectbox(
                                    "Banco",
                                    options=bancos,
                                    index=bancos.index(fila["Banco"]) if fila["Banco"] in bancos else 0,
                                    key=f"banco_edit_{fila['ID']}"
                                )
                                
                                monto_edit = st.number_input(
                                    "Monto del Préstamo",
                                    min_value=0.0,
                                    value=float(limpiar_numero(fila["Monto"])),
                                    step=100000.0,
                                    key=f"monto_edit_{fila['ID']}"
                                )
                                
                                cuotas_edit = st.number_input(
                                    "Cantidad de Cuotas",
                                    min_value=1,
                                    value=int(limpiar_numero(fila["Cuotas"])) if limpiar_numero(fila["Cuotas"]) > 0 else 12,
                                    step=1,
                                    key=f"cuotas_edit_{fila['ID']}"
                                )
                            
                            with col2:
                                tasa_edit = st.number_input(
                                    "Tasa Anual (%)",
                                    min_value=0.0,
                                    value=float(limpiar_numero(fila["Tasa"])),
                                    step=0.1,
                                    key=f"tasa_edit_{fila['ID']}"
                                )
                                
                                fecha_inicio_edit = st.date_input(
                                    "Fecha de Inicio",
                                    value=pd.to_datetime(fila["Fecha Inicio"]).date() if 'Fecha Inicio' in fila and fila["Fecha Inicio"] else date.today(),
                                    key=f"fecha_inicio_edit_{fila['ID']}"
                                )
                                
                                destino_edit = st.selectbox(
                                    "Destino del Crédito",
                                    options=destinos,
                                    index=destinos.index(fila["Destino"]) if fila["Destino"] in destinos else 0,
                                    key=f"destino_edit_{fila['ID']}"
                                )
                            
                            col_guardar, col_cancelar = st.columns(2)
                            
                            with col_guardar:
                                if st.form_submit_button("💾 Guardar", use_container_width=True):
                                    fecha_fin_edit = fecha_inicio_edit + relativedelta(months=int(cuotas_edit))
                                    
                                    registros = hoja_creditos.get_all_records()
                                    for i, r in enumerate(registros, start=2):
                                        if r["ID"] == fila["ID"]:
                                            hoja_creditos.update(
                                                f"A{i}:I{i}",
                                                [[
                                                    int(fila["ID"]),
                                                    str(fila["Empresa"]),
                                                    str(banco_edit),
                                                    float(monto_edit),
                                                    int(cuotas_edit),
                                                    float(tasa_edit),
                                                    fecha_inicio_edit.strftime("%Y-%m-%d"),
                                                    fecha_fin_edit.strftime("%Y-%m-%d"),
                                                    str(destino_edit)
                                                ]]
                                            )
                                            break
                                    
                                    if not df_amort_cred.empty:
                                        for idx in reversed(df_amort_cred.index.tolist()):
                                            hoja_amortizacion.delete_rows(idx + 2)
                                            time.sleep(0.1)
                                    
                                    nueva_amort = generar_amortizacion(monto_edit, tasa_edit, cuotas_edit, fecha_inicio_edit)
                                    for item in nueva_amort:
                                        hoja_amortizacion.append_row([
                                            int(fila["ID"]),
                                            item["Fecha"].strftime("%Y-%m-%d"),
                                            float(item["Cuota"]),
                                            float(item["Saldo"]),
                                            "NO"
                                        ])
                                        time.sleep(0.1)
                                    
                                    limpiar_cache_creditos()
                                    st.session_state.editando_credito = None
                                    st.session_state["mensaje_creditos"] = f"✅ Crédito para {empresa} actualizado correctamente!"
                                    st.rerun()
                            
                            with col_cancelar:
                                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                    st.session_state.editando_credito = None
                                    st.rerun()
                    
                    else:
                        
                        # TARJETA SUPERIOR - DATOS DEL CRÉDITO
                        with st.container(border=True):
                            
                            st.markdown(f"### 🏦 {fila['Banco']}")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("**📅 Fechas**")
                                st.write(f"Inicio: {fila['Fecha Inicio']}")
                                st.write(f"Fin: {fila['Fecha Fin']}")
                                st.write(f"Destino: {fila['Destino']}")
                            
                            with col2:
                                st.markdown("**💰 Montos**")
                                st.write(f"Monto: {formato_moneda(monto_valor)}")
                                if tasa_valor > 0:
                                    st.write(f"Cuota (estimada): {formato_moneda(cuota_mensual)}")
                                total = cuota_mensual * cuotas_valor
                                st.write(f"Total estimado: {formato_moneda(total)}")
                            
                            with col3:
                                st.markdown("**📊 Detalles**")
                                st.write(f"Cuotas: {cuotas_valor}")
                                st.write(f"Tasa: {tasa_valor}%")
                                if tasa_valor > 0:
                                    st.write(f"Interés estimado: {formato_moneda(total - monto_valor)}")
                                else:
                                    st.write("Sin interés")
                            
                            col1, col2 = st.columns([6, 1])
                            with col2:
                                if st.button("✏️", key=f"edit_cred_{fila['ID']}", use_container_width=True):
                                    st.session_state.editando_credito = fila["ID"]
                                    st.rerun()
                                
                                if st.session_state.eliminar_credito == fila["ID"]:
                                    col_si, col_no = st.columns(2)
                                    with col_si:
                                        if st.button("✅", key=f"ok_cred_{fila['ID']}", use_container_width=True):
                                            if not df_amort_cred.empty:
                                                df_amort_del = df_amort[df_amort["ID Credito"] == fila["ID"]]
                                                for idx in reversed(df_amort_del.index.tolist()):
                                                    hoja_amortizacion.delete_rows(idx + 2)
                                                    time.sleep(0.1)
                                            
                                            registros = hoja_creditos.get_all_records()
                                            for i, r in enumerate(registros, start=2):
                                                if r["ID"] == fila["ID"]:
                                                    hoja_creditos.delete_rows(i)
                                                    break
                                            
                                            limpiar_cache_creditos()
                                            st.session_state.eliminar_credito = None
                                            st.session_state["mensaje_creditos"] = f"✅ Crédito para {empresa} eliminado correctamente!"
                                            st.rerun()
                                    with col_no:
                                        if st.button("❌", key=f"cancel_cred_{fila['ID']}", use_container_width=True):
                                            st.session_state.eliminar_credito = None
                                            st.rerun()
                                else:
                                    if st.button("🗑️", key=f"del_cred_{fila['ID']}", use_container_width=True):
                                        st.session_state.eliminar_credito = fila["ID"]
                                        st.rerun()
                        
                        # TARJETA INFERIOR - AMORTIZACIÓN
                        st.subheader("📋 Detalle de Amortización")
                        
                        if not df_amort_cred.empty:
                            
                            if "Pagada" not in df_amort_cred.columns:
                                df_amort_cred["Pagada"] = "NO"
                            
                            cuotas_pagadas_df = df_amort_cred[df_amort_cred["Pagada"] == "SI"]
                            cuotas_pendientes_df = df_amort_cred[df_amort_cred["Pagada"] != "SI"]
                            
                            total_pagado = cuotas_pagadas_df["Cuota"].sum() if not cuotas_pagadas_df.empty else 0
                            saldo_actual = cuotas_pendientes_df["Cuota"].sum() if not cuotas_pendientes_df.empty else 0
                            total_a_pagar = total_pagado + saldo_actual
                            
                            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
                            
                            with col1:
                                st.metric("💰 Saldo Actual", formato_moneda(saldo_actual))
                            
                            with col2:
                                if total_a_pagar > 0:
                                    pct = max(0, min(100, (total_pagado / total_a_pagar * 100)))
                                else:
                                    pct = 0
                                st.metric("📈 % Pagado", f"{pct:.1f}%")
                                st.progress(min(max(pct/100, 0), 1.0))
                            
                            with col3:
                                st.metric("⏳ Cuotas Pendientes", len(cuotas_pendientes_df))
                            
                            with col4:
                                st.metric("✅ Cuotas Pagadas", len(cuotas_pagadas_df))
                            
                            st.divider()
                            
                            df_amort_ordenado = df_amort_cred.sort_values("Fecha", ascending=True)
                            
                            st.markdown("**📅 Todas las Cuotas**")
                            
                            for idx, cuota in df_amort_ordenado.iterrows():
                                fecha_cuota = cuota["Fecha"]
                                esta_pagada = cuota.get("Pagada", "NO") == "SI"
                                
                                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                                
                                with col1:
                                    st.write(f"🗓️ {fecha_cuota}")
                                
                                with col2:
                                    st.write(f"💰 {formato_moneda(cuota['Cuota'])}")
                                
                                with col3:
                                    if esta_pagada:
                                        st.success("✅ Pagada")
                                    else:
                                        st.warning("⏳ Pendiente")
                                
                                with col4:
                                    if not esta_pagada:
                                        if st.button("💵 Pagar", key=f"pagar_{idx}_{fila['ID']}"):
                                            registros_amort = hoja_amortizacion.get_all_records()
                                            for i, r in enumerate(registros_amort, start=2):
                                                if r["ID Credito"] == fila["ID"] and r["Fecha"] == fecha_cuota:
                                                    hoja_amortizacion.update(f"E{i}", [["SI"]])
                                                    break
                                            limpiar_cache_creditos()
                                            st.rerun()
                        else:
                            st.info("No hay datos de amortización para este crédito")
                
                else:
                    st.info("🔍 Seleccione un crédito para ver su detalle")

# ============================================
# HISTORIAL GENERAL DE TODOS LOS CRÉDITOS (fuera de tabs)
# ============================================

st.divider()
st.subheader("📋 Historial General de Créditos")

df_creditos_all = obtener_creditos()
df_amort_all = obtener_amortizacion()

if not df_creditos_all.empty:
    
    # Crear resumen por crédito
    resumen_creditos = []
    
    for _, credito in df_creditos_all.iterrows():
        monto_limpio = limpiar_numero(credito["Monto"])
        
        # Obtener estado del crédito
        df_amort_cred = df_amort_all[df_amort_all["ID Credito"] == credito["ID"]]
        estado = "Sin amortización"
        saldo = 0
        cuotas_pendientes = 0
        cuotas_totales = int(limpiar_numero(credito["Cuotas"])) if limpiar_numero(credito["Cuotas"]) > 0 else 0
        
        if not df_amort_cred.empty:
            cuotas_pagadas_df = df_amort_cred[df_amort_cred.get("Pagada", "NO") == "SI"]
            cuotas_pendientes_df = df_amort_cred[df_amort_cred.get("Pagada", "NO") != "SI"]
            
            cuotas_pendientes = len(cuotas_pendientes_df)
            saldo = cuotas_pendientes_df["Cuota"].sum() if not cuotas_pendientes_df.empty else 0
            
            if cuotas_pendientes == 0 and cuotas_totales > 0:
                estado = "✅ Finalizado"
            elif cuotas_pendientes > 0:
                estado = "🟢 Vigente"
            else:
                estado = "⚪ Sin datos"
        else:
            estado = "🔴 Sin cuotas"
        
        resumen_creditos.append({
            "ID": credito["ID"],
            "Empresa": credito["Empresa"],
            "Banco": credito["Banco"],
            "Monto": formato_moneda(monto_limpio),
            "Cuotas Pendientes": cuotas_pendientes,
            "Saldo Pendiente": formato_moneda(saldo),
            "Fecha Fin": credito["Fecha Fin"],
            "Estado": estado
        })
    
    if resumen_creditos:
        df_resumen = pd.DataFrame(resumen_creditos)
        df_resumen = df_resumen.sort_values("Fecha Fin", ascending=False)
        
        # 📊 Selector de cantidad de filas a mostrar
        col1, col2 = st.columns([3, 1])
        with col2:
            opciones_filas = [5, 10, 15, "Todos"]
            cantidad_seleccionada = st.selectbox(
                "Mostrar",
                options=opciones_filas,
                index=2,
                key="cantidad_historial"
            )
        
        if cantidad_seleccionada == "Todos":
            df_mostrar = df_resumen
            total_mostrados = len(df_resumen)
        else:
            df_mostrar = df_resumen.head(int(cantidad_seleccionada))
            total_mostrados = int(cantidad_seleccionada)
        
        st.caption(f"📊 Mostrando {total_mostrados} de {len(df_resumen)} créditos")
        
        st.dataframe(
            df_mostrar,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "ID": "ID",
                "Empresa": "Empresa",
                "Banco": "Banco",
                "Monto": "Monto",
                "Cuotas Pendientes": "Cuotas Pendientes",
                "Saldo Pendiente": "Saldo Pendiente",
                "Fecha Fin": "Fecha Fin",
                "Estado": "Estado"
            }
        )
    else:
        st.info("📭 No hay créditos para mostrar")
else:
    st.info("📭 No hay créditos registrados aún.")