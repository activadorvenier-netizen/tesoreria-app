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
    
    # ✅ Menú con st.page_link (ESTO SIEMPRE FUNCIONA)
    st.page_link("pages/1_📊_Resultados.py", label="📊 Resultados", icon="📊")
    st.page_link("pages/3_🏦_Bancos.py", label="🏦 Bancos", icon="🏦")
    st.page_link("pages/4_🍺_Quilmes.py", label="🍺 Quilmes", icon="🍺")
    st.page_link("pages/5_💰_Cierre_Caja.py", label="💰 Cierre de Caja", icon="💰")
    st.page_link("pages/6_📈_Plazos_Fijos.py", label="📈 Plazos Fijos", icon="📈")
    st.page_link("pages/8_📊_Creditos.py", label="📊 Créditos", icon="📊")
    st.page_link("pages/7_⚙️_Administracion.py", label="⚙️ Administración", icon="⚙️")
    
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