import streamlit as st
import pandas as pd

from datetime import date, datetime

from utils.sheets import (
    obtener_hoja,
    obtener_dataframe,
    actualizar_plazo_fijo,
    eliminar_plazo_fijo
)
from utils.layout import mostrar_sidebar

# ✅ Configurar la página
st.set_page_config(
    page_title="Tesorería - Plazos Fijos",
    page_icon="📈",
    layout="wide"
)

# ✅ Mostrar el sidebar
mostrar_sidebar()

st.title("📈 Plazos Fijos")

# ============================================
# FUNCIONES
# ============================================

def convertir_importe(valor):
    if valor is None:
        return 0
    valor = str(valor).strip()
    if valor == "":
        return 0
    return float(valor.replace(".", "").replace(",", "."))

def formato_moneda(valor):
    return f"$ {float(valor):,.0f}".replace(",", ".")

# ============================================
# ESTADOS
# ============================================

if "editando_pf" not in st.session_state:
    st.session_state.editando_pf = None

if "eliminar_pf" not in st.session_state:
    st.session_state.eliminar_pf = None

if "mensaje_pf" in st.session_state:
    st.success(st.session_state["mensaje_pf"])
    st.balloons()
    del st.session_state["mensaje_pf"]

# ============================================
# INICIALIZAR HOJAS
# ============================================

hoja_pf = obtener_hoja("PlazosFijos")

empresas = ["Venier", "Venbiere", "CV Trade"]
bancos_pf = ["Galicia", "Macro", "Credicoop", "Santander Rio", "Provincia", "BBVA", "ICBC"]

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
    background:#00838F !important;
    color:white !important;
    border:none;
}
</style>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "🏢 Venier",
    "🍺 Venbiere",
    "📦 CV Trade"
])

for tab, empresa in zip(tabs, empresas):
    with tab:
        
        # ==========================================
        # FORMULARIO NUEVO PLAZO FIJO POR EMPRESA
        # ==========================================
        
        with st.container(border=True):
            st.subheader(f"➕ Nuevo Plazo Fijo - {empresa}")
            
            with st.form(key=f"form_pf_{empresa}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    banco_pf = st.selectbox(
                        "Banco",
                        options=[""] + bancos_pf,
                        key=f"banco_pf_{empresa}"
                    )
                    
                    capital_pf = st.text_input(
                        "Capital",
                        value="",
                        key=f"capital_pf_{empresa}",
                        placeholder="0.00"
                    )
                
                with col2:
                    tasa_pf = st.number_input(
                        "Tasa (%)",
                        min_value=0.0,
                        value=None,
                        step=0.1,
                        key=f"tasa_pf_{empresa}",
                        placeholder="Ingrese la tasa"
                    )
                    
                    vencimiento_pf = st.date_input(
                        "Vencimiento",
                        value=None,
                        key=f"vencimiento_pf_{empresa}"
                    )
                
                if st.form_submit_button("💾 Guardar Plazo Fijo", type="primary", use_container_width=True):
                    if not banco_pf:
                        st.error("⚠️ Por favor seleccione un banco")
                    elif not capital_pf:
                        st.error("⚠️ Por favor ingrese el capital")
                    elif tasa_pf is None:
                        st.error("⚠️ Por favor ingrese la tasa")
                    elif vencimiento_pf is None:
                        st.error("⚠️ Por favor seleccione una fecha de vencimiento")
                    else:
                        nuevo_id = "PF" + datetime.now().strftime("%Y%m%d%H%M%S")
                        
                        hoja_pf.append_row([
                            nuevo_id,
                            date.today().strftime("%Y-%m-%d"),
                            empresa,
                            banco_pf,
                            convertir_importe(capital_pf),
                            tasa_pf,
                            vencimiento_pf.strftime("%Y-%m-%d")
                        ])
                        
                        st.session_state["mensaje_pf"] = f"✅ Plazo fijo para {empresa} agregado correctamente!"
                        st.rerun()
        
        # ==========================================
        # LISTADO DE PLAZOS FIJOS POR EMPRESA
        # ==========================================
        
        st.subheader(f"📋 Plazos Fijos - {empresa}")
        
        df_pf = pd.DataFrame(hoja_pf.get_all_records())
        
        # Validar que el DataFrame no esté vacío y tenga la columna 'Empresa'
        if df_pf.empty or 'Empresa' not in df_pf.columns:
            st.info(f"📭 No hay plazos fijos para {empresa}")
        else:
            df_pf_emp = df_pf[df_pf["Empresa"] == empresa]
            
            if df_pf_emp.empty:
                st.info(f"📭 No hay plazos fijos para {empresa}")
            else:
                # Ordenar por vencimiento (más cercano primero)
                df_pf_emp = df_pf_emp.sort_values("Vencimiento", ascending=True)
                
                for _, fila in df_pf_emp.iterrows():
                    
                    with st.container(border=True):
                        
                        # ==========================
                        # MODO VISUALIZACIÓN
                        # ==========================
                        
                        if st.session_state.editando_pf != fila["ID"]:
                            
                            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1.5, 0.8])
                            
                            with col1:
                                st.markdown(f"**🏦 {fila['Banco']}**")
                                st.markdown(f"**💰 Capital**")
                                st.markdown(f"{formato_moneda(fila['Capital'])}")
                            
                            with col2:
                                st.markdown(f"**📊 Tasa**")
                                st.markdown(f"{fila['Tasa']}%")
                            
                            with col3:
                                st.markdown(f"**📅 Vencimiento**")
                                st.markdown(f"{fila['Vencimiento']}")
                            
                            with col4:
                                # Calcular días restantes
                                try:
                                    fecha_venc = pd.to_datetime(fila['Vencimiento']).date()
                                    dias_restantes = (fecha_venc - date.today()).days
                                    if dias_restantes < 0:
                                        st.error(f"🔴 Vencido hace {abs(dias_restantes)} días")
                                    elif dias_restantes <= 30:
                                        st.warning(f"⚠️ Vence en {dias_restantes} días")
                                    else:
                                        st.success(f"✅ Vence en {dias_restantes} días")
                                except:
                                    pass
                            
                            with col5:
                                if st.button("✏️", key=f"edit_pf_{fila['ID']}", use_container_width=True):
                                    st.session_state.editando_pf = fila["ID"]
                                    st.rerun()
                                
                                if st.session_state.eliminar_pf == fila["ID"]:
                                    col_si, col_no = st.columns(2)
                                    with col_si:
                                        if st.button("✅", key=f"ok_pf_{fila['ID']}", use_container_width=True):
                                            eliminar_plazo_fijo(fila["ID"])
                                            st.session_state.eliminar_pf = None
                                            st.session_state["mensaje_pf"] = f"✅ Plazo fijo para {empresa} eliminado correctamente!"
                                            st.rerun()
                                    with col_no:
                                        if st.button("❌", key=f"cancel_pf_{fila['ID']}", use_container_width=True):
                                            st.session_state.eliminar_pf = None
                                            st.rerun()
                                else:
                                    if st.button("🗑️", key=f"del_pf_{fila['ID']}", use_container_width=True):
                                        st.session_state.eliminar_pf = fila["ID"]
                                        st.rerun()
                        
                        # ==========================
                        # MODO EDICIÓN
                        # ==========================
                        
                        else:
                            
                            st.subheader(f"✏️ Editando PF {fila['ID']}")
                            
                            with st.form(key=f"edit_pf_form_{fila['ID']}"):
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    bancos_con_vacio = [""] + bancos_pf
                                    banco_edit = st.selectbox(
                                        "Banco",
                                        options=bancos_con_vacio,
                                        index=bancos_con_vacio.index(fila["Banco"]) if fila["Banco"] in bancos_con_vacio else 0,
                                        key=f"banco_edit_{fila['ID']}"
                                    )
                                    
                                    capital_edit = st.number_input(
                                        "Capital",
                                        value=float(fila["Capital"]),
                                        step=1000.0,
                                        key=f"capital_edit_{fila['ID']}"
                                    )
                                
                                with col2:
                                    tasa_edit = st.number_input(
                                        "Tasa (%)",
                                        min_value=0.0,
                                        value=float(fila["Tasa"]),
                                        step=0.1,
                                        key=f"tasa_edit_{fila['ID']}"
                                    )
                                    
                                    vencimiento_edit = st.date_input(
                                        "Vencimiento",
                                        value=pd.to_datetime(fila["Vencimiento"]).date(),
                                        key=f"vencimiento_edit_{fila['ID']}"
                                    )
                                
                                col_guardar, col_cancelar = st.columns(2)
                                
                                with col_guardar:
                                    if st.form_submit_button("💾 Guardar", use_container_width=True):
                                        actualizar_plazo_fijo(
                                            fila["ID"],
                                            date.today().strftime("%Y-%m-%d"),
                                            fila["Empresa"],
                                            banco_edit,
                                            capital_edit,
                                            tasa_edit,
                                            vencimiento_edit.strftime("%Y-%m-%d")
                                        )
                                        st.session_state.editando_pf = None
                                        st.session_state["mensaje_pf"] = f"✅ Plazo fijo para {empresa} actualizado correctamente!"
                                        st.rerun()
                                
                                with col_cancelar:
                                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                        st.session_state.editando_pf = None
                                        st.rerun()