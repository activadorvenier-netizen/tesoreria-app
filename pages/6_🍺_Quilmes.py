import streamlit as st
import pandas as pd

from datetime import date, datetime

from utils.layout import mostrar_sidebar
from utils.sheets import (
    obtener_hoja,
    obtener_dataframe,
    actualizar_quilmes,
    eliminar_quilmes
)

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

from utils.menu import mostrar_menu

# ✅ Mostrar el menú
mostrar_menu()

st.title("🍺 Quilmes")

# ============================================
# FUNCIONES
# ============================================

def formato_moneda(valor):
    return f"$ {float(valor):,.0f}".replace(",", ".")

# ============================================
# ESTADOS
# ============================================

if "editando_quilmes" not in st.session_state:
    st.session_state.editando_quilmes = None

if "eliminar_quilmes" not in st.session_state:
    st.session_state.eliminar_quilmes = None

if "mensaje_quilmes" in st.session_state:
    st.success(st.session_state["mensaje_quilmes"])
    st.balloons()
    del st.session_state["mensaje_quilmes"]

# ============================================
# INICIALIZAR HOJAS
# ============================================

sheet = obtener_hoja("Quilmes")

# ============================================
# EMPRESAS (DEFINIDAS ANTES DE LOS TABS)
# ============================================

empresas = [
    "Venier",
    "Venbiere",
    "CV Trade"
]

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
        
        # ==========================================
        # FORMULARIO QUILMES POR EMPRESA
        # ==========================================
        
        with st.container(border=True):
            st.subheader(f"📊 Nueva Posición Quilmes - {empresa}")
            
            fecha = st.date_input(
                "Fecha",
                value=date.today(),
                key=f"fecha_quilmes_{empresa}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                deuda = st.text_input(
                    "Deuda a Pagar",
                    value="",
                    key=f"deuda_{empresa}",
                    placeholder="0.00"
                )
                
                promesa_nc = st.text_input(
                    "Promesa NC",
                    value="",
                    key=f"promesa_{empresa}",
                    placeholder="0.00"
                )
            
            with col2:
                cheques = st.text_input(
                    "Cheques Emitidos",
                    value="",
                    key=f"cheques_{empresa}",
                    placeholder="0.00"
                )
                
                depositos = st.text_input(
                    "Depósitos",
                    value="",
                    key=f"depositos_{empresa}",
                    placeholder="0.00"
                )
                
                efectivo = st.text_input(
                    "Efectivo",
                    value="",
                    key=f"efectivo_{empresa}",
                    placeholder="0.00"
                )
            
            # ==========================================
            # CÁLCULOS EN TIEMPO REAL
            # ==========================================
            
            deuda_num = convertir_importe(deuda)
            promesa_nc_num = convertir_importe(promesa_nc)
            cheques_num = convertir_importe(cheques)
            depositos_num = convertir_importe(depositos)
            efectivo_num = convertir_importe(efectivo)
            
            cobertura = promesa_nc_num + cheques_num + depositos_num + efectivo_num
            necesidad = deuda_num - cobertura
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Cobertura Total",
                    f"$ {cobertura:,.0f}".replace(",", ".")
                )
            
            with col2:
                st.metric(
                    "Necesidad Quilmes",
                    f"$ {necesidad:,.0f}".replace(",", ".")
                )
            
            if necesidad > 0:
                st.error(f"🔴 Faltan $ {necesidad:,.0f}".replace(",", "."))
            elif necesidad < 0:
                st.success(f"🟢 Cubierto por $ {abs(necesidad):,.0f}".replace(",", "."))
            else:
                st.info("⚪ Está exactamente cubierto")
            
            # ==========================================
            # BOTÓN GUARDAR
            # ==========================================
            
            with st.form(key=f"form_guardar_quilmes_{empresa}"):
                submitted = st.form_submit_button(
                    "💾 Guardar",
                    type="primary",
                    use_container_width=True
                )
                
                if submitted:
                    if deuda_num == 0 and promesa_nc_num == 0 and cheques_num == 0 and depositos_num == 0 and efectivo_num == 0:
                        st.error("⚠️ Por favor ingrese al menos un valor")
                    else:
                        registros = sheet.get_all_records()
                        
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
                        
                        sheet.append_row([
                            ultimo_id,
                            fecha.strftime("%Y-%m-%d"),
                            empresa,
                            deuda_num,
                            promesa_nc_num,
                            cheques_num,
                            depositos_num,
                            efectivo_num,
                            necesidad
                        ])
                        
                        st.session_state["mensaje_quilmes"] = f"✅ Registro Quilmes para {empresa} guardado correctamente!"
                        st.rerun()
        
        # ==========================================
        # HISTORIAL QUILMES POR EMPRESA
        # ==========================================
        
        st.subheader(f"📋 Historial Quilmes - {empresa}")
        
        df_quilmes = pd.DataFrame(sheet.get_all_records())
        
        # Validar que el DataFrame no esté vacío y tenga la columna 'Empresa'
        if df_quilmes.empty or 'Empresa' not in df_quilmes.columns:
            st.info(f"📭 No hay registros de Quilmes para {empresa}")
        else:
            df_quilmes_emp = df_quilmes[df_quilmes["Empresa"] == empresa]
            
            if df_quilmes_emp.empty:
                st.info(f"📭 No hay registros de Quilmes para {empresa}")
            else:
                df_quilmes_emp = df_quilmes_emp.sort_values("Fecha", ascending=False)
                
                for _, fila in df_quilmes_emp.iterrows():
                    
                    with st.container(border=True):
                        
                        # ==========================
                        # MODO VISUALIZACIÓN
                        # ==========================
                        
                        if st.session_state.editando_quilmes != fila["ID"]:
                            
                            cobertura_total = (
                                fila['PromesaNC'] + fila['ChequesEmitidos'] +
                                fila['Depositos'] + fila['Efectivo']
                            )
                            
                            col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 0.8])
                            
                            with col1:
                                st.markdown(f"**📅 {fila['Fecha']}**")
                                st.markdown(f"💰 Deuda: {formato_moneda(fila['DeudaPagar'])}")
                                st.markdown(f"📊 Cobertura: {formato_moneda(cobertura_total)}")
                            
                            with col2:
                                st.markdown("**📄 Detalle Cobertura**")
                                st.markdown(f"Promesa NC: {formato_moneda(fila['PromesaNC'])}")
                                st.markdown(f"Cheques: {formato_moneda(fila['ChequesEmitidos'])}")
                            
                            with col3:
                                st.markdown("**📄 Detalle Cobertura**")
                                st.markdown(f"Depósitos: {formato_moneda(fila['Depositos'])}")
                                st.markdown(f"Efectivo: {formato_moneda(fila['Efectivo'])}")
                                
                                necesidad = fila['NecesidadQuilmes']
                                if necesidad > 0:
                                    st.error(f"🔴 Necesidad: {formato_moneda(necesidad)}")
                                else:
                                    st.success(f"🟢 Cubierto: {formato_moneda(abs(necesidad))}")
                            
                            with col4:
                                if st.button("✏️", key=f"edit_quilmes_{fila['ID']}", use_container_width=True):
                                    st.session_state.editando_quilmes = fila["ID"]
                                    st.rerun()
                                
                                if st.session_state.eliminar_quilmes == fila["ID"]:
                                    col_si, col_no = st.columns(2)
                                    with col_si:
                                        if st.button("✅", key=f"ok_quilmes_{fila['ID']}", use_container_width=True):
                                            eliminar_quilmes(fila["ID"])
                                            st.session_state.eliminar_quilmes = None
                                            st.session_state["mensaje_quilmes"] = f"✅ Registro Quilmes para {empresa} eliminado correctamente!"
                                            st.rerun()
                                    with col_no:
                                        if st.button("❌", key=f"cancel_quilmes_{fila['ID']}", use_container_width=True):
                                            st.session_state.eliminar_quilmes = None
                                            st.rerun()
                                else:
                                    if st.button("🗑️", key=f"del_quilmes_{fila['ID']}", use_container_width=True):
                                        st.session_state.eliminar_quilmes = fila["ID"]
                                        st.rerun()
                        
                        # ==========================
                        # MODO EDICIÓN
                        # ==========================
                        
                        else:
                            
                            st.subheader(f"✏️ Editando ID: {fila['ID']}")
                            
                            with st.form(key=f"edit_quilmes_form_{fila['ID']}"):
                                
                                fecha_edit = st.date_input(
                                    "Fecha",
                                    value=pd.to_datetime(fila["Fecha"]).date(),
                                    key=f"fecha_edit_{fila['ID']}"
                                )
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    deuda_edit = st.number_input(
                                        "Deuda a Pagar",
                                        value=float(fila["DeudaPagar"]),
                                        step=1000.0,
                                        key=f"deuda_edit_{fila['ID']}"
                                    )
                                    promesa_nc_edit = st.number_input(
                                        "Promesa NC",
                                        value=float(fila["PromesaNC"]),
                                        step=1000.0,
                                        key=f"promesa_edit_{fila['ID']}"
                                    )
                                
                                with col2:
                                    cheques_edit = st.number_input(
                                        "Cheques Emitidos",
                                        value=float(fila["ChequesEmitidos"]),
                                        step=1000.0,
                                        key=f"cheques_edit_{fila['ID']}"
                                    )
                                    depositos_edit = st.number_input(
                                        "Depósitos",
                                        value=float(fila["Depositos"]),
                                        step=1000.0,
                                        key=f"depositos_edit_{fila['ID']}"
                                    )
                                    efectivo_edit = st.number_input(
                                        "Efectivo",
                                        value=float(fila["Efectivo"]),
                                        step=1000.0,
                                        key=f"efectivo_edit_{fila['ID']}"
                                    )
                                
                                col_guardar, col_cancelar = st.columns(2)
                                
                                with col_guardar:
                                    if st.form_submit_button("💾 Guardar", use_container_width=True):
                                        actualizar_quilmes(
                                            fila["ID"],
                                            fecha_edit.strftime("%Y-%m-%d"),
                                            fila["Empresa"],
                                            deuda_edit,
                                            promesa_nc_edit,
                                            cheques_edit,
                                            depositos_edit,
                                            efectivo_edit
                                        )
                                        st.session_state.editando_quilmes = None
                                        st.session_state["mensaje_quilmes"] = f"✅ Registro Quilmes para {empresa} actualizado correctamente!"
                                        st.rerun()
                                
                                with col_cancelar:
                                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                        st.session_state.editando_quilmes = None
                                        st.rerun()