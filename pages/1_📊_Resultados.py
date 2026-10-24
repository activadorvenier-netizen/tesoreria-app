import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.sheets import leer_hoja, guardar_necesidad_manual

# ✅ Configurar la página
st.set_page_config(
    page_title="Tesorería - Resultados",
    page_icon="📊",
    layout="wide"
)

# ✅ LIMPIAR CACHÉ AUTOMÁTICAMENTE AL CARGAR LA PÁGINA
st.cache_data.clear()

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.image(
        "assets/logo_grupo_venier.png",
        use_container_width=True
    )
    
    st.divider()
    
    st.markdown("""
    <style>
        .st-emotion-cache-1wivap2 {
            display: none !important;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stFooter"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Resultados", key="menu_resultados", use_container_width=True):
        st.switch_page("pages/1_📊_Resultados.py")
        
    if st.button("🏢 Detalle Empresa", key="menu_detalle_empresa", use_container_width=True):
        st.switch_page("pages/8_🏢_Detalle_Empresa.py")
    
    if st.button("💰 Cierre de Caja", key="menu_cierre", use_container_width=True):
        st.switch_page("pages/2_💰_Cierre_Caja.py")
    
    if st.button("🏦 Bancos", key="menu_bancos", use_container_width=True):
        st.switch_page("pages/3_🏦_Bancos.py")
    
    if st.button("📈 Plazos Fijos", key="menu_pf", use_container_width=True):
        st.switch_page("pages/4_📈_Plazos_Fijos.py")
    
    if st.button("📊 Créditos", key="menu_creditos", use_container_width=True):
        st.switch_page("pages/5_📊_Creditos.py")
    
    if st.button("🍺 Quilmes", key="menu_quilmes", use_container_width=True):
        st.switch_page("pages/6_🍺_Quilmes.py")
    
    if st.button("⚙️ Administración", key="menu_admin", use_container_width=True):
        st.switch_page("pages/7_⚙️_Administracion.py")
    
    st.divider()
    
    st.markdown("""
    <div style="text-align: center; padding: 5px 0; margin-bottom: 5px;">
        <a href="https://venier.chesserp.com/AR173/#/dashboard" 
           target="_blank" 
           style="
               display: inline-block;
               background-color: #1f77b4;
               color: white;
               padding: 8px 16px;
               text-decoration: none;
               border-radius: 6px;
               font-weight: 500;
               font-size: 13px;
               transition: all 0.3s;
               width: 100%;
               text-align: center;
           "
           onmouseover="this.style.backgroundColor='#145a8a'"
           onmouseout="this.style.backgroundColor='#1f77b4'">
           🔗 Ir a ChessERP
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.caption("By Pato Frangi")

# ============================================
# ENCABEZADO
# ============================================

col1, col2 = st.columns([3,1])

with col1:
    st.title("📊 Resultados y Necesidades")

with col2:
    st.caption("Actualizado")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M"))

# ============================================
# FECHA DE CONSULTA
# ============================================

col_fecha, _ = st.columns([1,3])
with col_fecha:
    fecha_consulta = st.date_input("📅 Fecha", value=date.today())

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def limpiar_numero(valor):
    if valor is None or pd.isna(valor):
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        valor = valor.replace("$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(valor)
        except:
            return 0.0
    return 0.0

# ============================================
# CARGA DE DATOS (Para calcular Patrimonio y Quilmes)
# ============================================

caja = leer_hoja("CierreCaja")
bancos_df = leer_hoja("Bancos")
plazos_fijos_df = leer_hoja("PlazosFijos")
quilmes = leer_hoja("Quilmes")

if caja.empty:
    caja = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Efectivo", "Cheques", "Echeq"])
if bancos_df.empty:
    bancos_df = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "GaliciaSaldo", "GaliciaFCI", "MacroSaldo", "MacroFCI", "CredicoopSaldo", "CredicoopFCI", "SantanderSaldo", "SantanderFCI"])
if plazos_fijos_df.empty:
    plazos_fijos_df = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Banco", "Capital", "Tasa", "Vencimiento"])
if quilmes.empty:
    quilmes = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "DeudaPagar", "PromesaNC", "ChequesEmitidos", "Depositos", "Efectivo", "NecesidadQuilmes"])

# Limpieza de fechas
caja["Fecha"] = pd.to_datetime(caja["Fecha"], errors='coerce').dt.date
if not bancos_df.empty: bancos_df["Fecha"] = pd.to_datetime(bancos_df["Fecha"], errors='coerce').dt.date
if not quilmes.empty: quilmes["Fecha"] = pd.to_datetime(quilmes["Fecha"], errors='coerce').dt.date

empresas = ["Venier", "Venbiere", "CV Trade"]

# ============================================
# CÁLCULOS BASE
# ============================================

totales_empresa = {}

for emp in empresas:
    # Caja
    caja_emp = caja[(caja["Empresa"] == emp) & (caja["Fecha"] <= fecha_consulta)].sort_values("Fecha", ascending=False)
    total_caja = 0
    if not caja_emp.empty:
        total_caja = float(caja_emp.iloc[0]["Efectivo"]) + float(caja_emp.iloc[0]["Cheques"]) + float(caja_emp.iloc[0]["Echeq"])

    # Bancos
    bancos_emp = bancos_df[(bancos_df["Empresa"] == emp) & (bancos_df["Fecha"] <= fecha_consulta)].sort_values("Fecha", ascending=False)
    total_bancos = 0
    if not bancos_emp.empty:
        u = bancos_emp.iloc[0]
        total_bancos = sum(float(u.get(col, 0)) for col in u.index if col.endswith("Saldo") or col.endswith("FCI") and not pd.isna(u.get(col, 0)))

    # Plazos Fijos
    pf_emp = plazos_fijos_df[plazos_fijos_df["Empresa"] == emp]
    total_pf = pf_emp["Capital"].apply(limpiar_numero).sum() if not pf_emp.empty else 0

    # Patrimonio
    patrimonio = total_caja + total_bancos + total_pf

    # Quilmes
    quilmes_emp = quilmes[(quilmes["Empresa"] == emp) & (quilmes["Fecha"] <= fecha_consulta)].sort_values("Fecha", ascending=False)
    nec_quilmes = 0
    if not quilmes_emp.empty:
        nec_quilmes = float(quilmes_emp.iloc[0].get("NecesidadQuilmes", 0))

    totales_empresa[emp] = {
        "caja": total_caja,
        "bancos": total_bancos,
        "pf": total_pf,
        "patrimonio": patrimonio,
        "quilmes": nec_quilmes
    }

# ============================================
# CARGA DE NECESIDADES MANUALES
# ============================================

df_necesidades = leer_hoja("Necesidades_Manuales")
if df_necesidades.empty:
    df_necesidades = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Concepto", "Importe"])

# Diccionario para acceder rápido a los valores manuales
valores_manuales = {emp: {concepto: 0.0 for concepto in ["F931", "F2051 IVA", "Sueldos", "Consignaciones"]} for emp in empresas}

for _, row in df_necesidades.iterrows():
    emp = row["Empresa"]
    concepto = row["Concepto"]
    if emp in valores_manuales and concepto in valores_manuales[emp]:
        valores_manuales[emp][concepto] = limpiar_numero(row["Importe"])

# ============================================
# CONSTRUCCIÓN DE LA TABLA (DATA EDITOR)
# ============================================

st.subheader("Detalle de Necesidades y Cobertura")

# Armamos la estructura de datos para la tabla
data = {
    "Concepto": ["CAJA TOTAL", "BANCOS", "PLAZOS FIJOS", "PATRIMONIO", "NECESIDAD QUILMES", "F931", "F2051 IVA", "SUELDOS", "CONSIGNACIONES"]
}

for emp in empresas:
    data[emp] = [
        totales_empresa[emp]["caja"],
        totales_empresa[emp]["bancos"],
        totales_emp[emp]["pf"],
        totales_emp[emp]["patrimonio"],
        totales_emp[emp]["quilmes"],
        valores_manuales[emp]["F931"],
        valores_manuales[emp]["F2051 IVA"],
        valores_manuales[emp]["Sueldos"],
        valores_manuales[emp]["Consignaciones"]
    ]

df_tabla = pd.DataFrame(data)

# Definimos qué columnas y celdas se pueden editar
column_config = {
    "Concepto": st.column_config.TextColumn("Concepto", disabled=True),
    "Venier": st.column_config.NumberColumn("VENIER", format="$ %.0f"),
    "Venbiere": st.column_config.NumberColumn("VENBIERE", format="$ %.0f"),
    "CV Trade": st.column_config.NumberColumn("CV TRADE", format="$ %.0f"),
}

# Mostramos el editor. 
# Nota: Streamlit no permite bloquear celdas individuales, solo columnas enteras.
# Para que el usuario sepa qué editar, pintamos el fondo o dejamos que edite lo que quiera.
df_editado = st.data_editor(
    df_tabla,
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed"
)

# ============================================
# BOTÓN GUARDAR MANUALES
# ============================================

col_btn, _ = st.columns([1, 4])
with col_btn:
    if st.button("💾 Guardar Cambios Manuales", type="primary", use_container_width=True):
        # Identificamos qué filas son editables
        conceptos_editables = ["F931", "F2051 IVA", "SUELDOS", "CONSIGNACIONES"]
        
        # Validamos si hubo cambios reales
        cambios_guardados = 0
        
        for i, row in df_editado.iterrows():
            if row["Concepto"] in conceptos_editables:
                for emp in empresas:
                    nuevo_valor = row[emp]
                    valor_viejo = valores_manuales[emp].get(row["Concepto"].title(), 0) # .title() porque en dict es "Sueldos"
                    
                    # Si el usuario cambió el número, lo guardamos
                    if nuevo_valor != valor_viejo:
                        # Mapeamos el nombre del concepto para que coincida exacto con el dict
                        concepto_guardar = "Sueldos" if row["Concepto"] == "SUELDOS" else ("F931" if row["Concepto"] == "F931" else row["Concepto"].title())
                        guardar_necesidad_manual(emp, concepto_guardar, nuevo_valor)
                        cambios_guardados += 1
                        
        if cambios_guardados > 0:
            st.success("✅ Cambios guardados correctamente en Google Sheets.")
            st.rerun() # Recargamos para actualizar los cálculos
        else:
            st.info("No se detectaron cambios para guardar.")

st.divider()

# ============================================
# SECCIÓN DE NECESIDAD TOTAL Y COBERTURA
# ============================================

st.subheader("Resumen de Cobertura")

for emp in empresas:
    # Cálculo de la necesidad total sumando manuales
    nec_manuales = sum(valores_manuales[emp].values())
    nec_total = totales_empresa[emp]["quilmes"] + nec_manuales
    patrimonio = totales_empresa[emp]["patrimonio"]
    
    # Cobertura
    cobertura = patrimonio - nec_total
    
    with st.container(border=True):
        st.markdown(f"#### 🏢 {emp.upper()}")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.metric("Patrimonio", formato_moneda(patrimonio))
        with c2:
            st.metric("Necesidad Total", formato_moneda(nec_total))
        with c3:
            st.metric("Cobertura", formato_moneda(cobertura))
            
        # Lógica del Semáforo y Barra de Progreso
        if cobertura >= 0:
            st.success(f"🟢 **CUBIERTO.** El patrimonio cubre la necesidad total por {formato_moneda(abs(cobertura))}.")
            # Si está cubierto, la barra es 100%
            st.progress(1.0, text="Cobertura 100%")
        else:
            st.error(f"🔴 **DÉFICIT.** Faltan {formato_moneda(abs(cobertura))} para cubrir la necesidad.")
            # Calculamos el porcentaje de cobertura
            porcentaje = patrimonio / nec_total if nec_total > 0 else 1.0
            porcentaje = max(0.0, min(1.0, porcentaje)) # Limitamos entre 0 y 1
            st.progress(porcentaje, text=f"Cobertura {porcentaje * 100:.1f}%")