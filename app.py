import streamlit as st

st.set_page_config(
    page_title="Tesorería",
    page_icon="💰",
    layout="wide"
)

# ============================================
# SIDEBAR CON LOGO, ENLACE A CHESSERP Y MENÚ
# ============================================

with st.sidebar:
    st.image(
        "assets/logo_grupo_venier.png",
        use_container_width=True
    )
    
    st.divider()
    
    # Enlace a ChessERP
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
    
    # ✅ Ocultar menú automático de Streamlit
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stFooter"] {
            display: none !important;
        }
        /* Estilo para el botón de Resultados en VERDE */
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
    
    # ✅ Menú lateral - RESULTADOS en VERDE
    if st.button("📊 Resultados", key="menu_resultados", use_container_width=True):
        st.switch_page("pages/1_📊_Resultados.py")
    
    if st.button("🏦 Bancos", key="menu_bancos", use_container_width=True):
        st.switch_page("pages/3_🏦_Bancos.py")
    
    if st.button("🍺 Quilmes", key="menu_quilmes", use_container_width=True):
        st.switch_page("pages/4_🍺_Quilmes.py")
    
    if st.button("💰 Cierre de Caja", key="menu_cierre", use_container_width=True):
        st.switch_page("pages/5_💰_Cierre_Caja.py")
    
    if st.button("📈 Plazos Fijos", key="menu_pf", use_container_width=True):
        st.switch_page("pages/6_📈_Plazos_Fijos.py")
    
    if st.button("📊 Créditos", key="menu_creditos", use_container_width=True):
        st.switch_page("pages/8_📊_Creditos.py")
    
    if st.button("⚙️ Administración", key="menu_admin", use_container_width=True):
        st.switch_page("pages/7_⚙️_Administracion.py")
    
    st.divider()
    
    st.caption("By Pato Frangi")

# ============================================
# CONTENIDO PRINCIPAL - REDIRIGIR A RESULTADOS
# ============================================

# Redirigir automáticamente a Resultados
st.switch_page("pages/1_📊_Resultados.py")