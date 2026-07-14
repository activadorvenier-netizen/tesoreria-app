import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.sheets import leer_hoja
from utils.resultados_ui import mostrar_tarjeta_bancos, mostrar_tarjeta_pf

# ✅ Configurar la página
st.set_page_config(
    page_title="Tesorería - Resultados",
    page_icon="💰",
    layout="wide"
)

# ✅ LIMPIAR CACHÉ AL INICIO DE LA APLICACIÓN
# Usamos un flag en session_state para que solo se ejecute una vez por sesión
if "cache_limpiado" not in st.session_state:
    st.cache_data.clear()
    st.session_state.cache_limpiado = True

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
        button[data-testid="baseButton-secondary"][aria-label="📊 Resultados"] {
            background-color: #2e7d32 !important;
            color: white !important;
            font-weight: 600 !important;
        }
        button[data-testid="baseButton-secondary"][aria-label="📊 Resultados"]:hover {
            background-color: #1b5e20 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Resultados", key="menu_resultados", use_container_width=True):
        st.switch_page("inicio.py")
    
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
    st.title("📊 Resultados")

with col2:
    st.caption("Actualizado")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M"))

# ============================================
# ESTILOS
# ============================================

st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# FECHA DE CONSULTA
# ============================================

col_fecha, _ = st.columns([1,3])

with col_fecha:
    fecha_consulta = st.date_input("📅 Fecha", value=date.today())

# ============================================
# FUNCIONES
# ============================================

def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def limpiar_numero_local(valor):
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

def calcular_saldos_empresa(empresa, fecha_consulta, caja):
    caja_emp = caja[
        (caja["Empresa"] == empresa) &
        (caja["Fecha"] <= fecha_consulta)
    ].copy()

    if caja_emp.empty:
        return {
            "efectivo": 0,
            "cheques": 0,
            "echeq": 0,
            "total": 0,
            "fecha_caja": None
        }

    caja_emp = caja_emp.sort_values("Fecha", ascending=False)
    ultimo = caja_emp.iloc[0]

    efectivo = float(ultimo["Efectivo"])
    cheques = float(ultimo["Cheques"])
    echeq = float(ultimo["Echeq"])

    return {
        "efectivo": efectivo,
        "cheques": cheques,
        "echeq": echeq,
        "total": efectivo + cheques + echeq,
        "fecha_caja": ultimo["Fecha"]
    }

def calcular_bancos_empresa(empresa, fecha_consulta, bancos, plazos_fijos):
    bancos_emp = bancos[
        (bancos["Empresa"] == empresa) &
        (bancos["Fecha"] <= fecha_consulta)
    ].copy()

    galicia_saldo = 0
    galicia_fci = 0
    macro_saldo = 0
    macro_fci = 0
    credicoop_saldo = 0
    credicoop_fci = 0
    santander_saldo = 0
    santander_fci = 0
    otros_bancos = {}

    if not bancos_emp.empty:
        bancos_emp = bancos_emp.sort_values("Fecha", ascending=False)
        ultimo = bancos_emp.iloc[0]

        galicia_saldo = float(ultimo["GaliciaSaldo"])
        galicia_fci = float(ultimo["GaliciaFCI"])
        macro_saldo = float(ultimo["MacroSaldo"])
        macro_fci = float(ultimo["MacroFCI"])
        credicoop_saldo = float(ultimo["CredicoopSaldo"])
        credicoop_fci = float(ultimo["CredicoopFCI"])
        santander_saldo = float(ultimo["SantanderSaldo"])
        santander_fci = float(ultimo["SantanderFCI"])
        
        for col in ultimo.index:
            if col.endswith("Saldo") and col not in ["GaliciaSaldo", "MacroSaldo", "CredicoopSaldo", "SantanderSaldo"]:
                nombre = col.replace("Saldo", "")
                fci_col = f"{nombre}FCI"
                saldo = float(ultimo[col]) if ultimo[col] else 0
                fci = float(ultimo[fci_col]) if fci_col in ultimo and ultimo[fci_col] else 0
                if saldo > 0 or fci > 0:
                    otros_bancos[nombre] = {"saldo": saldo, "fci": fci}

    detalle_pf = pd.DataFrame()
    pf_galicia = 0
    pf_macro = 0
    pf_credicoop = 0
    pf_santander = 0
    pf_otros = {}

    if not plazos_fijos.empty:
        detalle_pf = plazos_fijos[plazos_fijos["Empresa"] == empresa].copy()
        if not detalle_pf.empty:
            detalle_pf["Capital"] = detalle_pf["Capital"].astype(float)
            pf_galicia = detalle_pf.loc[detalle_pf["Banco"] == "Galicia", "Capital"].sum()
            pf_macro = detalle_pf.loc[detalle_pf["Banco"] == "Macro", "Capital"].sum()
            pf_credicoop = detalle_pf.loc[detalle_pf["Banco"] == "Credicoop", "Capital"].sum()
            pf_santander = detalle_pf.loc[detalle_pf["Banco"] == "Santander", "Capital"].sum()
            for banco in detalle_pf["Banco"].unique():
                if banco not in ["Galicia", "Macro", "Credicoop", "Santander"]:
                    pf_otros[banco] = detalle_pf.loc[detalle_pf["Banco"] == banco, "Capital"].sum()

    total_bancos = galicia_saldo + galicia_fci + macro_saldo + macro_fci + credicoop_saldo + credicoop_fci + santander_saldo + santander_fci
    total_pf = pf_galicia + pf_macro + pf_credicoop + pf_santander + sum(pf_otros.values())

    return {
        "GaliciaSaldo": galicia_saldo,
        "GaliciaFCI": galicia_fci,
        "MacroSaldo": macro_saldo,
        "MacroFCI": macro_fci,
        "CredicoopSaldo": credicoop_saldo,
        "CredicoopFCI": credicoop_fci,
        "SantanderSaldo": santander_saldo,
        "SantanderFCI": santander_fci,
        "pf_galicia": pf_galicia,
        "pf_macro": pf_macro,
        "pf_credicoop": pf_credicoop,
        "pf_santander": pf_santander,
        "otros_bancos": otros_bancos,
        "pf_otros": pf_otros,
        "total_bancos": total_bancos,
        "total_pf": total_pf,
        "detalle_pf": detalle_pf
    }

def calcular_quilmes_empresa(empresa, fecha_consulta, quilmes):
    if quilmes.empty:
        return {"deuda": 0, "nc": 0, "cobertura": 0, "necesidad": 0}

    datos = quilmes[
        (quilmes["Empresa"] == empresa) &
        (quilmes["Fecha"] <= fecha_consulta)
    ].copy()

    if datos.empty:
        return {"deuda": 0, "nc": 0, "cobertura": 0, "necesidad": 0}

    datos = datos.sort_values("Fecha", ascending=False)
    ultimo = datos.iloc[0]

    deuda = float(ultimo["DeudaPagar"])
    nc = float(ultimo["PromesaNC"])
    cobertura = (
        float(ultimo["PromesaNC"]) +
        float(ultimo["ChequesEmitidos"]) +
        float(ultimo["Depositos"]) +
        float(ultimo["Efectivo"])
    )
    necesidad = float(ultimo["NecesidadQuilmes"])

    return {"deuda": deuda, "nc": nc, "cobertura": cobertura, "necesidad": necesidad}

# ============================================
# CARGA DE DATOS
# ============================================

# ✅ Siempre cargar datos frescos
caja = leer_hoja("CierreCaja")
bancos_df = leer_hoja("Bancos")
plazos_fijos_df = leer_hoja("PlazosFijos")
quilmes = leer_hoja("Quilmes")

# ============================================
# VALIDACIÓN DE DATAFRAMES VACÍOS
# ============================================

if caja.empty:
    caja = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Efectivo", "Cheques", "Echeq"])

if bancos_df.empty:
    bancos_df = pd.DataFrame(columns=[
        "ID", "Fecha", "Empresa", "GaliciaSaldo", "GaliciaFCI",
        "MacroSaldo", "MacroFCI", "CredicoopSaldo", "CredicoopFCI",
        "SantanderSaldo", "SantanderFCI"
    ])

if plazos_fijos_df.empty:
    plazos_fijos_df = pd.DataFrame(columns=["ID", "Fecha", "Empresa", "Banco", "Capital", "Tasa", "Vencimiento"])

if quilmes.empty:
    quilmes = pd.DataFrame(columns=[
        "ID", "Fecha", "Empresa", "DeudaPagar", "PromesaNC",
        "ChequesEmitidos", "Depositos", "Efectivo", "NecesidadQuilmes"
    ])

# ============================================
# VALIDACIONES
# ============================================

if caja.empty:
    st.warning("No existe ningún Cierre de Caja cargado.")

# ============================================
# FECHAS
# ============================================

caja["Fecha"] = pd.to_datetime(caja["Fecha"]).dt.date

if not bancos_df.empty:
    bancos_df["Fecha"] = pd.to_datetime(bancos_df["Fecha"]).dt.date

if not quilmes.empty:
    quilmes["Fecha"] = pd.to_datetime(quilmes["Fecha"]).dt.date

# ============================================
# EMPRESAS
# ============================================

empresas = ["Venier", "Venbiere", "CV Trade"]
if "Venier" in empresas:
    empresas.remove("Venier")
    empresas.insert(0, "Venier")

# ============================================
# RESUMEN GENERAL
# ============================================

total_caja = 0
total_bancos = 0
total_necesidad = 0

for empresa in empresas:
    saldos = calcular_saldos_empresa(empresa, fecha_consulta, caja)
    bancos_empresa = calcular_bancos_empresa(empresa, fecha_consulta, bancos_df, plazos_fijos_df)
    quilmes_empresa = calcular_quilmes_empresa(empresa, fecha_consulta, quilmes)

    total_caja += saldos["total"]
    total_bancos += bancos_empresa["total_bancos"]
    total_necesidad += quilmes_empresa["necesidad"]

patrimonio_total = total_caja + total_bancos

st.subheader("📊 Resumen Total Empresas")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("💵 Caja Total", formato_moneda(total_caja))

with kpi2:
    st.metric("🏦 Bancos", formato_moneda(total_bancos))

with kpi3:
    st.metric("💎 Patrimonio", formato_moneda(patrimonio_total))

with kpi4:
    st.metric("🍺 Necesidad Quilmes", formato_moneda(total_necesidad))

# ============================================
# RESULTADOS POR EMPRESA (TABS)
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
    background:#D32F2F !important;
    color:white !important;
    border:none;
}
</style>
""", unsafe_allow_html=True)

tabs = st.tabs(["🏢 Venier", "🍺 Venbiere", "📦 CV Trade"])

for tab, empresa in zip(tabs, empresas):
    with tab:
        saldos = calcular_saldos_empresa(empresa, fecha_consulta, caja)
        bancos_empresa = calcular_bancos_empresa(empresa, fecha_consulta, bancos_df, plazos_fijos_df)
        quilmes_empresa = calcular_quilmes_empresa(empresa, fecha_consulta, quilmes)

        with st.container(border=True):
            st.subheader(f"🏢 {empresa.upper()}")

            if saldos["fecha_caja"] is not None:
                st.caption(f"Cierre de Caja utilizado: {saldos['fecha_caja'].strftime('%d/%m/%Y')}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("💵 Efectivo", formato_moneda(saldos["efectivo"]))
            with col2:
                st.metric("📄 Cheques", formato_moneda(saldos["cheques"]))
            with col3:
                st.metric("🏦 Echeq", formato_moneda(saldos["echeq"]))
            with col4:
                st.metric("💰 Total", formato_moneda(saldos["total"]))

            st.divider()

            mostrar_tarjeta_bancos(empresa, bancos_empresa)
            mostrar_tarjeta_pf(bancos_empresa["detalle_pf"])

            # ============================================
            # RESUMEN DE CRÉDITOS - CUOTAS DEL MES
            # ============================================
            
            st.divider()
            st.subheader("📊 Resumen de Créditos - Cuotas del Mes")
            
            df_creditos_all = leer_hoja("Creditos")
            df_amort_all = leer_hoja("Amortizacion")
            
            if not df_creditos_all.empty and not df_amort_all.empty:
                mes_seleccionado = fecha_consulta.strftime("%Y-%m")
                cuotas_mes = []
                
                for _, credito in df_creditos_all.iterrows():
                    if credito["Empresa"] == empresa:
                        df_amort_cred = df_amort_all[df_amort_all["ID Credito"] == credito["ID"]]
                        if not df_amort_cred.empty:
                            for _, cuota in df_amort_cred.iterrows():
                                fecha_cuota = pd.to_datetime(cuota["Fecha"]).strftime("%Y-%m")
                                if fecha_cuota == mes_seleccionado:
                                    esta_pagada = cuota.get("Pagada", "NO") == "SI"
                                    cuotas_mes.append({
                                        "Banco": credito["Banco"],
                                        "Fecha": cuota["Fecha"],
                                        "Monto": limpiar_numero_local(cuota["Cuota"]),
                                        "Pagada": "✅ Pagada" if esta_pagada else "⏳ Pendiente"
                                    })
                
                if cuotas_mes:
                    df_cuotas = pd.DataFrame(cuotas_mes)
                    total_mes = df_cuotas["Monto"].sum()
                    pagadas = df_cuotas[df_cuotas["Pagada"] == "✅ Pagada"]
                    pendientes = df_cuotas[df_cuotas["Pagada"] == "⏳ Pendiente"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("💰 Total Cuotas Mes", formato_moneda(total_mes))
                    with col2:
                        st.metric("✅ Pagadas", len(pagadas))
                    with col3:
                        st.metric("⏳ Pendientes", len(pendientes))
                    
                    st.dataframe(
                        df_cuotas[["Fecha", "Banco", "Monto", "Pagada"]],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Fecha": "Fecha",
                            "Banco": "Banco",
                            "Monto": st.column_config.NumberColumn("Monto", format="$ %.0f"),
                            "Pagada": "Estado"
                        }
                    )
                else:
                    st.info(f"📭 No hay cuotas para el mes de {fecha_consulta.strftime('%B %Y')} para {empresa}")
            else:
                st.info("📭 No hay créditos o cuotas registradas aún.")

        # ============================================
        # QUILMES
        # ============================================

        with st.container(border=True):
            st.markdown("### 🍺 Quilmes")
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Deuda", formato_moneda(quilmes_empresa["deuda"]))
            with col2:
                st.metric("Promesa NC", formato_moneda(quilmes_empresa["nc"]))
            with col3:
                st.metric("Cobertura", formato_moneda(quilmes_empresa["cobertura"]))
            with col4:
                st.metric("Necesidad", formato_moneda(quilmes_empresa["necesidad"]))

            if quilmes_empresa["necesidad"] > 0:
                st.error(f"🔴 Necesidad Quilmes: {formato_moneda(quilmes_empresa['necesidad'])}")
            else:
                st.success(f"🟢 Cubierto por {formato_moneda(abs(quilmes_empresa['necesidad']))}")