import streamlit as st

# ✅ Configurar la página (necesario para que no aparezca el menú nativo de Streamlit)
st.set_page_config(
    page_title="Tesorería",
    page_icon="💰",
    layout="wide"
)

# ============================================
# SIDEBAR (Idéntico al resto de las páginas)
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
# REDIRECCIÓN A RESULTADOS
# ============================================

# Como este archivo es la "puerta de entrada", redirigimos automáticamente a Resultados
st.switch_page("pages/1_📊_Resultados.py")