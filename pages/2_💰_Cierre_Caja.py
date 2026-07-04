import streamlit as st
import pandas as pd

from datetime import date, datetime

from utils.layout import mostrar_sidebar
from utils.sheets import (
    obtener_hoja,
    leer_hoja,
    guardar_cierre_caja,
    actualizar_cierre_caja,
    eliminar_cierre_caja,
    obtener_todas_cajas
)

from utils.config import configurar_pagina
from utils.layout import mostrar_sidebar

configurar_pagina()
mostrar_sidebar()

st.title("💰 Cierre de Caja")

# =====================================
# FUNCIONES
# =====================================

def formato_moneda(valor):
    return f"$ {float(valor):,.0f}".replace(",", ".")

# =====================================
# ESTADOS
# =====================================

if "editando_cierre" not in st.session_state:
    st.session_state.editando_cierre = None

if "eliminar_cierre" not in st.session_state:
    st.session_state.eliminar_cierre = None

if "mensaje_cierre" in st.session_state:
    st.success(st.session_state["mensaje_cierre"])
    st.balloons()
    del st.session_state["mensaje_cierre"]

# =====================================
# DATOS
# =====================================

hoja = obtener_hoja("CierreCaja")
df = pd.DataFrame(hoja.get_all_records())

if df.empty:
    df = pd.DataFrame(
        columns=[
            "ID",
            "Fecha",
            "Empresa",
            "Efectivo",
            "Cheques",
            "Echeq"
        ]
    )

# =====================================
# EMPRESAS
# =====================================

empresas = [
    "Venier",
    "Venbiere",
    "CV Trade"
]

# =====================================
# TABS POR EMPRESA
# =====================================

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

tabs = st.tabs([
    "🏢 Venier",
    "🍺 Venbiere",
    "📦 CV Trade"
])

for tab, empresa in zip(tabs, empresas):
    with tab:
        
        empresa_df = df[df["Empresa"] == empresa]
        
        # ==========================
        # FORMULARIO PARA NUEVO CIERRE
        # ==========================
        
        with st.container(border=True):
            st.subheader(f"📊 Nuevo Cierre - {empresa}")
            
            with st.form(key=f"form_cierre_{empresa}"):
                fecha_nueva = st.date_input(
                    "Fecha Cierre",
                    value=date.today(),
                    key=f"fecha_nueva_{empresa}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    efectivo_nuevo = st.number_input(
                        "💵 Efectivo",
                        min_value=0.0,
                        value=0.0,
                        step=1000.0,
                        key=f"ef_nuevo_{empresa}"
                    )
                
                with col2:
                    cheques_nuevo = st.number_input(
                        "📄 Cheques",
                        min_value=0.0,
                        value=0.0,
                        step=1000.0,
                        key=f"ch_nuevo_{empresa}"
                    )
                
                with col3:
                    echeq_nuevo = st.number_input(
                        "🏦 Echeq",
                        min_value=0.0,
                        value=0.0,
                        step=1000.0,
                        key=f"ec_nuevo_{empresa}"
                    )
                
                total_nuevo = efectivo_nuevo + cheques_nuevo + echeq_nuevo
                
                st.success(f"💰 Total Cierre: {formato_moneda(total_nuevo)}")
                
                if st.form_submit_button("💾 Guardar Cierre", type="primary", use_container_width=True):
                    guardar_cierre_caja(
                        fecha_nueva,
                        empresa,
                        efectivo_nuevo,
                        cheques_nuevo,
                        echeq_nuevo
                    )
                    st.session_state["mensaje_cierre"] = f"✅ Cierre de caja para {empresa} guardado correctamente!"
                    st.rerun()
        
        # ==========================
        # HISTORIAL DE CIERRES
        # ==========================
        
        st.subheader(f"📋 Historial - {empresa}")
        
        if empresa_df.empty:
            st.info(f"📭 No hay cierres de caja para {empresa}")
        else:
            empresa_df = empresa_df.sort_values("Fecha", ascending=False)
            
            for _, fila in empresa_df.iterrows():
                
                with st.container(border=True):
                    
                    # ==========================
                    # MODO VISUALIZACIÓN
                    # ==========================
                    
                    if st.session_state.editando_cierre != fila["ID"]:
                        
                        total = float(fila["Efectivo"]) + float(fila["Cheques"]) + float(fila["Echeq"])
                        
                        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 0.8])
                        
                        with col1:
                            st.markdown(f"**📅 {fila['Fecha']}**")
                        
                        with col2:
                            st.markdown(f"💵 {formato_moneda(fila['Efectivo'])}")
                        
                        with col3:
                            st.markdown(f"📄 {formato_moneda(fila['Cheques'])}")
                        
                        with col4:
                            st.markdown(f"🏦 {formato_moneda(fila['Echeq'])}")
                        
                        with col5:
                            st.markdown(f"**💰 {formato_moneda(total)}**")
                            if st.button("✏️", key=f"edit_cierre_{fila['ID']}", use_container_width=True):
                                st.session_state.editando_cierre = fila["ID"]
                                st.rerun()
                            
                            if st.session_state.eliminar_cierre == fila["ID"]:
                                col_si, col_no = st.columns(2)
                                with col_si:
                                    if st.button("✅", key=f"ok_cierre_{fila['ID']}", use_container_width=True):
                                        eliminar_cierre_caja(fila["ID"])
                                        st.session_state.eliminar_cierre = None
                                        st.session_state["mensaje_cierre"] = f"✅ Cierre de caja para {empresa} eliminado correctamente!"
                                        st.rerun()
                                with col_no:
                                    if st.button("❌", key=f"cancel_cierre_{fila['ID']}", use_container_width=True):
                                        st.session_state.eliminar_cierre = None
                                        st.rerun()
                            else:
                                if st.button("🗑️", key=f"del_cierre_{fila['ID']}", use_container_width=True):
                                    st.session_state.eliminar_cierre = fila["ID"]
                                    st.rerun()
                    
                    # ==========================
                    # MODO EDICIÓN
                    # ==========================
                    
                    else:
                        
                        st.subheader(f"✏️ Editando {fila['ID']}")
                        
                        with st.form(key=f"edit_cierre_form_{fila['ID']}"):
                            
                            fecha_edit = st.date_input(
                                "Fecha",
                                value=pd.to_datetime(fila["Fecha"]).date(),
                                key=f"fecha_edit_{fila['ID']}"
                            )
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                efectivo_edit = st.number_input(
                                    "💵 Efectivo",
                                    value=float(fila["Efectivo"]),
                                    step=1000.0,
                                    key=f"ef_edit_{fila['ID']}"
                                )
                            
                            with col2:
                                cheques_edit = st.number_input(
                                    "📄 Cheques",
                                    value=float(fila["Cheques"]),
                                    step=1000.0,
                                    key=f"ch_edit_{fila['ID']}"
                                )
                            
                            with col3:
                                echeq_edit = st.number_input(
                                    "🏦 Echeq",
                                    value=float(fila["Echeq"]),
                                    step=1000.0,
                                    key=f"ec_edit_{fila['ID']}"
                                )
                            
                            col_guardar, col_cancelar = st.columns(2)
                            
                            with col_guardar:
                                if st.form_submit_button("💾 Guardar", use_container_width=True):
                                    actualizar_cierre_caja(
                                        fila["ID"],
                                        fecha_edit,
                                        fila["Empresa"],
                                        efectivo_edit,
                                        cheques_edit,
                                        echeq_edit
                                    )
                                    st.session_state.editando_cierre = None
                                    st.session_state["mensaje_cierre"] = f"✅ Cierre de caja para {empresa} actualizado correctamente!"
                                    st.rerun()
                            
                            with col_cancelar:
                                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                    st.session_state.editando_cierre = None
                                    st.rerun()