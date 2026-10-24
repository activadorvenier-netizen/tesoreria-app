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
    st.image("assets/logo_grupo_venier.png", use_container_width=True)
    st.divider()
    st.markdown("""
    <style>
        .st-emotion-cache-1wivap2 { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stFooter"] { display: none !important; }
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
        <a href="https://venier.chesserp.com/AR173/#/dashboard" target="_blank" 
           style="display: inline-block; background-color: #1f77b4; color: white; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 13px; width: 100%; text-align: center;">
           🔗 Ir a ChessERP
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.caption("By Pato Frangi")

# ============================================
# ENCABEZADO Y FECHA
# ============================================

col1, col2 = st.columns([3,1])
with col1:
    st.title("📊 Resultados y Necesidades")
with col2:
    st.caption("Actualizado")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M"))

col_fecha, _ = st.columns([1,3])
with col_fecha:
    fecha_consulta = st.date_input("📅 Fecha", value=date.today())

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def limpiar_numero(valor):
    if valor is None or pd.isna(valor): return 0.0
    if isinstance(valor, (int, float)): return float(valor)
    if isinstance(valor, str):
        valor = valor.replace("$", "").replace(".", "").replace(",", ".").strip()
        try: return float(valor)
        except: return 0.0
    return 0.0

# ============================================
# CARGA DE DATOS
# ============================================

caja = leer_hoja("CierreCaja")
bancos_df = leer_hoja("Bancos")
plazos_fijos_df = leer_hoja("PlazosFijos")
quilmes = leer_hoja("Quilmes")

if caja.empty: caja = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Efectivo", "Cheques", "Echeq"])
if bancos_df.empty: bancos_df = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "GaliciaSaldo", "GaliciaFCI", "MacroSaldo", "MacroFCI", "CredicoopSaldo", "CredicoopFCI", "SantanderSaldo", "SantanderFCI"])
if plazos_fijos_df.empty: plazos_fijos_df = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Banco", "Capital", "Tasa", "Vencimiento"])
if quilmes.empty: quilmes = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "DeudaPagar", "PromesaNC", "ChequesEmitidos", "Depositos", "Efectivo", "NecesidadQuilmes"])

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
    total_caja = (float(caja_emp.iloc[0]["Efectivo"]) + float(caja_emp.iloc[0]["Cheques"]) + float(caja_emp.iloc[0]["Echeq"])) if not caja_emp.empty else 0

    # Bancos
    bancos_emp = bancos_df[(bancos_df["Empresa"] == emp) & (bancos_df["Fecha"] <= fecha_consulta)].sort_values("Fecha", ascending=False)
    total_bancos = 0
    if not bancos_emp.empty:
        u = bancos_emp.iloc[0]
        total_bancos = sum(float(u.get(col, 0)) for col in u.index if (col.endswith("Saldo") or col.endswith("FCI")) and not pd.isna(u.get(col, 0)))

    # Plazos Fijos
    pf_emp = plazos_fijos_df[plazos_fijos_df["Empresa"] == emp]
    total_pf = pf_emp["Capital"].apply(limpiar_numero).sum() if not pf_emp.empty else 0

    # Patrimonio
    patrimonio = total_caja + total_bancos + total_pf

    # Quilmes
    quilmes_emp = quilmes[(quilmes["Empresa"] == emp) & (quilmes["Fecha"] <= fecha_consulta)].sort_values("Fecha", ascending=False)
    nec_quilmes = float(quilmes_emp.iloc[0].get("NecesidadQuilmes", 0)) if not quilmes_emp.empty else 0

    totales_empresa[emp] = {"caja": total_caja, "bancos": total_bancos, "pf": total_pf, "patrimonio": patrimonio, "quilmes": nec_quilmes}

# Carga Manuales
df_necesidades = leer_hoja("Necesidades_Manuales")
if df_necesidades.empty: df_necesidades = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Concepto", "Importe"])

valores_manuales = {emp: {c: 0.0 for c in ["F931", "F2051 IVA", "Sueldos", "Consignaciones"]} for emp in empresas}
for _, row in df_necesidades.iterrows():
    emp = row.get("Empresa")
    concepto = row.get("Concepto")
    if emp in valores_manuales and concepto in valores_manuales[emp]:
        valores_manuales[emp][concepto] = limpiar_numero(row.get("Importe", 0))

# ============================================
# 1. RESUMEN TOTAL (KPIs arriba)
# ============================================

tot_caja_global = sum(totales_empresa[e]["caja"] for e in empresas)
tot_bancos_global = sum(totales_empresa[e]["bancos"] for e in empresas)
tot_pf_global = sum(totales_empresa[e]["pf"] for e in empresas)
tot_patrimonio_global = sum(totales_empresa[e]["patrimonio"] for e in empresas)

# Para la necesidad global, sumamos Quilmes + Manuales de todas las empresas
nec_quilmes_global = sum(totales_empresa[e]["quilmes"] for e in empresas)
nec_manuales_global = sum(sum(valores_manuales[e].values()) for e in empresas)
tot_necesidad_global = nec_quilmes_global + nec_manuales_global

st.subheader("📊 Resumen Total Empresas")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("💵 Caja Total", formato_moneda(tot_caja_global))
with kpi2:
    st.metric("🏦 Bancos", formato_moneda(tot_bancos_global))
with kpi3:
    st.metric("📈 Plazos Fijos", formato_moneda(tot_pf_global))
with kpi4:
    st.metric("💎 Patrimonio", formato_moneda(tot_patrimonio_global))
with kpi5:
    st.metric("🚨 Necesidad Total", formato_moneda(tot_necesidad_global))

st.divider()

# ============================================
# 2. DETALLE VISUAL (No tabla)
# ============================================

st.markdown("### 📋 Detalle por Empresa")

# Estilos para que quede como una grilla elegante
st.markdown("""
<style>
    .fila-concepto { font-weight: 600; font-size: 1.1rem; padding-top: 10px; color: #333; }
    .valor-fijo { font-size: 1.2rem; color: #555; margin-bottom: 10px;}
    .titulo-empresa { text-align: center; font-weight: 800; font-size: 1.2rem; color: #2e7d32; background: #e8f5e9; padding: 10px; border-radius: 8px; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# Encabezados de las columnas
c_emp, c_ven, c_vb, c_cv = st.columns([1.5, 1, 1, 1])

with c_ven: st.markdown("<div class='titulo-empresa'>VENIER</div>", unsafe_allow_html=True)
with c_vb: st.markdown("<div class='titulo-empresa'>VENBIERE</div>", unsafe_allow_html=True)
with c_cv: st.markdown("<div class='titulo-empresa'>CV TRADE</div>", unsafe_allow_html=True)

# Función para dibujar una fila fija
def render_fila_fija(titulo, clave_dict):
    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c1: st.markdown(f"<div class='fila-concepto'>{titulo}</div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='valor-fijo'>{formato_moneda(totales_empresa['Venier'][clave_dict])}</div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='valor-fijo'>{formato_moneda(totales_empresa['Venbiere'][clave_dict])}</div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='valor-fijo'>{formato_moneda(totales_empresa['CV Trade'][clave_dict])}</div>", unsafe_allow_html=True)

render_fila_fija("💵 CAJA TOTAL", "caja")
render_fila_fija("🏦 BANCOS", "bancos")
render_fila_fija("📈 PLAZOS FIJOS", "pf")
render_fila_fija("💎 PATRIMONIO", "patrimonio")
render_fila_fija("🍺 NECESIDAD QUILMES", "quilmes")

st.markdown("---")
st.markdown("#### ✍️ Conceptos Editables")

# Diccionario temporal para guardar los inputs del usuario
inputs_actuales = {emp: {} for emp in empresas}

# Función para dibujar una fila editable
def render_fila_editable(titulo, clave_concepto):
    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c1: 
        st.markdown(f"<div class='fila-concepto' style='padding-top:20px;'>{titulo}</div>", unsafe_allow_html=True)
    with c2:
        inputs_actuales['Venier'][clave_concepto] = st.number_input(f"Edit {titulo} Venier", value=float(valores_manuales['Venier'][clave_concepto]), step=1000.0, format="%0.0f", label_visibility="collapsed", key=f"in_{clave_concepto}_Venier")
    with c3:
        inputs_actuales['Venbiere'][clave_concepto] = st.number_input(f"Edit {titulo} Venbiere", value=float(valores_manuales['Venbiere'][clave_concepto]), step=1000.0, format="%0.0f", label_visibility="collapsed", key=f"in_{clave_concepto}_Venbiere")
    with c4:
        inputs_actuales['CV Trade'][clave_concepto] = st.number_input(f"Edit {titulo} CV Trade", value=float(valores_manuales['CV Trade'][clave_concepto]), step=1000.0, format="%0.0f", label_visibility="collapsed", key=f"in_{clave_concepto}_CV Trade")

render_fila_editable("📄 F931", "F931")
render_fila_editable("🧾 F2051 IVA", "F2051 IVA")
render_fila_editable("💼 SUELDOS", "Sueldos")
render_fila_editable("📦 CONSIGNACIONES", "Consignaciones")

# Botón de guardar
col_btn, _ = st.columns([1, 4])
with col_btn:
    if st.button("💾 Guardar Cambios Manuales", type="primary", use_container_width=True):
        cambios = 0
        for emp in empresas:
            for concepto in ["F931", "F2051 IVA", "Sueldos", "Consignaciones"]:
                nuevo = inputs_actuales[emp][concepto]
                viejo = valores_manuales[emp][concepto]
                if nuevo != viejo:
                    guardar_necesidad_manual(emp, concepto, nuevo)
                    cambios += 1
        if cambios > 0:
            st.success("✅ Guardado en Google Sheets.")
            st.rerun()
        else:
            st.info("No hubo cambios.")

st.divider()

# ============================================
# 3. COBERTURA (Semáforos y Barras)
# ============================================

st.markdown("### 🚦 Resumen de Cobertura")

# Hacemos tres columnas para poner una empresa en cada una
cob1, cob2, cob3 = st.columns(3)

def mostrar_cobertura(col, emp):
    with col:
        nec_manuales = sum(valores_manuales[emp].values())
        nec_total = totales_empresa[emp]["quilmes"] + nec_manuales
        patrimonio = totales_empresa[emp]["patrimonio"]
        cobertura = patrimonio - nec_total
        
        st.markdown(f"#### {emp.upper()}")
        
        # Semáforo
        if cobertura >= 0:
            st.success(f"🟢 **CUBIERTO** por {formato_moneda(abs(cobertura))}")
            st.progress(1.0, text="100% Cubierto")
        else:
            st.error(f"🔴 **DÉFICIT** de {formato_moneda(abs(cobertura))}")
            porcentaje = (patrimonio / nec_total) if nec_total > 0 else 1.0
            porcentaje = max(0.0, min(1.0, porcentaje))
            st.progress(porcentaje, text=f"{porcentaje * 100:.1f}% Cubierto")
            
        st.caption(f"Patrimonio: {formato_moneda(patrimonio)}")
        st.caption(f"Necesidad: {formato_moneda(nec_total)}")

mostrar_cobertura(cob1, "Venier")
mostrar_cobertura(cob2, "Venbiere")
mostrar_cobertura(cob3, "CV Trade")