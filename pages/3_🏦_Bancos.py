import streamlit as st
import pandas as pd

from datetime import date, datetime

from utils.sheets import (
    obtener_hoja,
    obtener_dataframe,
    actualizar_banco,
    eliminar_banco
)

# ✅ Configurar la página
st.set_page_config(
    page_title="Tesorería - Bancos",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Bancos")

# ============================================
# FUNCIONES
# ============================================

def convertir_importe(valor):
    """
    Convierte un texto a float.
    Si está vacío devuelve 0.
    Acepta coma o punto decimal.
    """
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

if "editando_banco" not in st.session_state:
    st.session_state.editando_banco = None

if "eliminar_banco" not in st.session_state:
    st.session_state.eliminar_banco = None

if "mensaje_bancos" in st.session_state:
    st.success(st.session_state["mensaje_bancos"])
    st.balloons()
    del st.session_state["mensaje_bancos"]

# ============================================
# INICIALIZAR HOJAS
# ============================================

hoja_bancos = obtener_hoja("Bancos")

# ============================================
# EMPRESAS
# ============================================

empresas = [
    "Venier",
    "Venbiere",
    "CV Trade"
]

# ============================================
# TABS POR EMPRESA - BANCOS
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

tabs_bancos = st.tabs([
    "🏢 Venier",
    "🍺 Venbiere",
    "📦 CV Trade"
])

for tab, empresa in zip(tabs_bancos, empresas):
    with tab:
        
        # ============================================
        # FORMULARIO BANCOS POR EMPRESA
        # ============================================
        
        with st.container(border=True):
            st.subheader(f"💰 Posición Bancaria - {empresa}")
            
            with st.form(key=f"form_bancos_{empresa}"):
                fecha = st.date_input(
                    "Fecha",
                    value=date.today(),
                    key=f"fecha_{empresa}"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    galicia_saldo = st.text_input(
                        "Galicia Saldo",
                        value="",
                        key=f"{empresa}_gs"
                    )
                    macro_saldo = st.text_input(
                        "Macro Saldo",
                        value="",
                        key=f"{empresa}_ms"
                    )
                    credicoop_saldo = st.text_input(
                        "Credicoop Saldo",
                        value="",
                        key=f"{empresa}_cs"
                    )
                    santander_saldo = st.text_input(
                        "Santander Saldo",
                        value="",
                        key=f"{empresa}_ss"
                    )
                
                with col2:
                    galicia_fci = st.text_input(
                        "Galicia FCI",
                        value="",
                        key=f"{empresa}_gf"
                    )
                    macro_fci = st.text_input(
                        "Macro FCI",
                        value="",
                        key=f"{empresa}_mf"
                    )
                    credicoop_fci = st.text_input(
                        "Credicoop FCI",
                        value="",
                        key=f"{empresa}_cf"
                    )
                    santander_fci = st.text_input(
                        "Santander FCI",
                        value="",
                        key=f"{empresa}_sf"
                    )
                
                if st.form_submit_button("💾 Guardar Bancos", type="primary", use_container_width=True):
                    nuevo_id = "B" + datetime.now().strftime("%Y%m%d%H%M%S%f")
                    
                    hoja_bancos.append_row([
                        nuevo_id,
                        fecha.strftime("%Y-%m-%d"),
                        empresa,
                        convertir_importe(st.session_state[f"{empresa}_gs"]),
                        convertir_importe(st.session_state[f"{empresa}_gf"]),
                        convertir_importe(st.session_state[f"{empresa}_ms"]),
                        convertir_importe(st.session_state[f"{empresa}_mf"]),
                        convertir_importe(st.session_state[f"{empresa}_cs"]),
                        convertir_importe(st.session_state[f"{empresa}_cf"]),
                        convertir_importe(st.session_state[f"{empresa}_ss"]),
                        convertir_importe(st.session_state[f"{empresa}_sf"])
                    ])
                    
                    st.session_state["mensaje_bancos"] = f"✅ Posiciones bancarias para {empresa} guardadas correctamente!"
                    st.rerun()
        
        # ============================================
        # HISTORIAL BANCOS POR EMPRESA
        # ============================================
        
        st.subheader(f"📋 Historial Bancos - {empresa}")
        
        df_bancos = pd.DataFrame(hoja_bancos.get_all_records())
        
        # Validar que el DataFrame no esté vacío y tenga la columna 'Empresa'
        if df_bancos.empty or 'Empresa' not in df_bancos.columns:
            st.info(f"📭 No hay registros bancarios para {empresa}")
        else:
            df_bancos_emp = df_bancos[df_bancos["Empresa"] == empresa]
            
            if df_bancos_emp.empty:
                st.info(f"📭 No hay registros bancarios para {empresa}")
            else:
                df_bancos_emp = df_bancos_emp.sort_values("Fecha", ascending=False)
                
                for _, fila in df_bancos_emp.iterrows():
                    
                    with st.container(border=True):
                        
                        # ==========================
                        # MODO VISUALIZACIÓN
                        # ==========================
                        
                        if st.session_state.editando_banco != fila["ID"]:
                            
                            total_banco = (
                                fila['GaliciaSaldo'] + fila['GaliciaFCI'] +
                                fila['MacroSaldo'] + fila['MacroFCI'] +
                                fila['CredicoopSaldo'] + fila['CredicoopFCI'] +
                                fila['SantanderSaldo'] + fila['SantanderFCI']
                            )
                            
                            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1.5, 0.8])
                            
                            with col1:
                                st.markdown(f"**📅 {fila['Fecha']}**")
                                st.markdown(f"**🏦 Galicia**")
                                st.markdown(f"Saldo: {formato_moneda(fila['GaliciaSaldo'])}")
                                st.markdown(f"FCI: {formato_moneda(fila['GaliciaFCI'])}")
                                st.markdown(f"Total: {formato_moneda(fila['GaliciaSaldo'] + fila['GaliciaFCI'])}")
                            
                            with col2:
                                st.markdown(f"**🏦 Macro**")
                                st.markdown(f"Saldo: {formato_moneda(fila['MacroSaldo'])}")
                                st.markdown(f"FCI: {formato_moneda(fila['MacroFCI'])}")
                                st.markdown(f"Total: {formato_moneda(fila['MacroSaldo'] + fila['MacroFCI'])}")
                            
                            with col3:
                                st.markdown(f"**🏦 Credicoop**")
                                st.markdown(f"Saldo: {formato_moneda(fila['CredicoopSaldo'])}")
                                st.markdown(f"FCI: {formato_moneda(fila['CredicoopFCI'])}")
                                st.markdown(f"Total: {formato_moneda(fila['CredicoopSaldo'] + fila['CredicoopFCI'])}")
                            
                            with col4:
                                st.markdown(f"**🏦 Santander**")
                                st.markdown(f"Saldo: {formato_moneda(fila['SantanderSaldo'])}")
                                st.markdown(f"FCI: {formato_moneda(fila['SantanderFCI'])}")
                                st.markdown(f"Total: {formato_moneda(fila['SantanderSaldo'] + fila['SantanderFCI'])}")
                                st.markdown(f"**💰 Total General: {formato_moneda(total_banco)}**")
                            
                            with col5:
                                if st.button("✏️", key=f"edit_banco_{fila['ID']}", use_container_width=True):
                                    st.session_state.editando_banco = fila["ID"]
                                    st.rerun()
                                
                                if st.session_state.eliminar_banco == fila["ID"]:
                                    col_si, col_no = st.columns(2)
                                    with col_si:
                                        if st.button("✅", key=f"ok_banco_{fila['ID']}", use_container_width=True):
                                            eliminar_banco(fila["ID"])
                                            st.session_state.eliminar_banco = None
                                            st.session_state["mensaje_bancos"] = f"✅ Registro bancario para {empresa} eliminado correctamente!"
                                            st.rerun()
                                    with col_no:
                                        if st.button("❌", key=f"cancel_banco_{fila['ID']}", use_container_width=True):
                                            st.session_state.eliminar_banco = None
                                            st.rerun()
                                else:
                                    if st.button("🗑️", key=f"del_banco_{fila['ID']}", use_container_width=True):
                                        st.session_state.eliminar_banco = fila["ID"]
                                        st.rerun()
                        
                        # ==========================
                        # MODO EDICIÓN
                        # ==========================
                        
                        else:
                            
                            st.subheader(f"✏️ Editando ID: {fila['ID']}")
                            
                            with st.form(key=f"edit_banco_form_{fila['ID']}"):
                                
                                fecha_edit = st.date_input(
                                    "Fecha",
                                    value=pd.to_datetime(fila["Fecha"]).date(),
                                    key=f"fecha_edit_{fila['ID']}"
                                )
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    galicia_saldo_edit = st.number_input(
                                        "Galicia Saldo",
                                        value=float(fila["GaliciaSaldo"]),
                                        step=1000.0,
                                        key=f"gs_edit_{fila['ID']}"
                                    )
                                    macro_saldo_edit = st.number_input(
                                        "Macro Saldo",
                                        value=float(fila["MacroSaldo"]),
                                        step=1000.0,
                                        key=f"ms_edit_{fila['ID']}"
                                    )
                                    credicoop_saldo_edit = st.number_input(
                                        "Credicoop Saldo",
                                        value=float(fila["CredicoopSaldo"]),
                                        step=1000.0,
                                        key=f"cs_edit_{fila['ID']}"
                                    )
                                    santander_saldo_edit = st.number_input(
                                        "Santander Saldo",
                                        value=float(fila["SantanderSaldo"]),
                                        step=1000.0,
                                        key=f"ss_edit_{fila['ID']}"
                                    )
                                
                                with col2:
                                    galicia_fci_edit = st.number_input(
                                        "Galicia FCI",
                                        value=float(fila["GaliciaFCI"]),
                                        step=1000.0,
                                        key=f"gf_edit_{fila['ID']}"
                                    )
                                    macro_fci_edit = st.number_input(
                                        "Macro FCI",
                                        value=float(fila["MacroFCI"]),
                                        step=1000.0,
                                        key=f"mf_edit_{fila['ID']}"
                                    )
                                    credicoop_fci_edit = st.number_input(
                                        "Credicoop FCI",
                                        value=float(fila["CredicoopFCI"]),
                                        step=1000.0,
                                        key=f"cf_edit_{fila['ID']}"
                                    )
                                    santander_fci_edit = st.number_input(
                                        "Santander FCI",
                                        value=float(fila["SantanderFCI"]),
                                        step=1000.0,
                                        key=f"sf_edit_{fila['ID']}"
                                    )
                                
                                col_guardar, col_cancelar = st.columns(2)
                                
                                with col_guardar:
                                    if st.form_submit_button("💾 Guardar", use_container_width=True):
                                        actualizar_banco(
                                            fila["ID"],
                                            fecha_edit.strftime("%Y-%m-%d"),
                                            fila["Empresa"],
                                            galicia_saldo_edit,
                                            galicia_fci_edit,
                                            macro_saldo_edit,
                                            macro_fci_edit,
                                            credicoop_saldo_edit,
                                            credicoop_fci_edit,
                                            santander_saldo_edit,
                                            santander_fci_edit
                                        )
                                        st.session_state.editando_banco = None
                                        st.session_state["mensaje_bancos"] = f"✅ Registro bancario para {empresa} actualizado correctamente!"
                                        st.rerun()
                                
                                with col_cancelar:
                                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                        st.session_state.editando_banco = None
                                        st.rerun()