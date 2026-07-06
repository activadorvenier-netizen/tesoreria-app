import streamlit as st

st.set_page_config(
    page_title="Tesorería",
    page_icon="💰",
    layout="wide"
)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.image(
        "assets/logo_grupo_venier.png",
        use_container_width=True
    )
    
    st.divider()
    
    # ✅ CSS para ocultar "app" y menú automático
    st.markdown("""
    <style>
        /* Ocultar el enlace "app" */
        .st-emotion-cache-1wivap2 {
            display: none !important;
        }
        /* Ocultar menú automático de Streamlit */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stFooter"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ✅ RESULTADOS en VERDE (con type="primary")
    if st.button("📊 Resultados", key="menu_resultados", use_container_width=True, type="primary"):
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
    
    st.caption("By Pato Frangi")

# ============================================
# CONTENIDO PRINCIPAL
# ============================================

st.switch_page("pages/1_📊_Resultados.py")