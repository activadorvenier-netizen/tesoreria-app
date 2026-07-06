import streamlit as st

def mostrar_sidebar():
    """Muestra el sidebar con logo, menú y enlaces"""
    
    with st.sidebar:
        st.image(
            "assets/logo_grupo_venier.png",
            use_container_width=True
        )
        
        st.divider()
        
        # ✅ CSS MEJORADO para ocultar "app" y menú automático
        st.markdown("""
        <style>
            /* === OCULTAR "app" DEL SIDEBAR === */
            /* Selector principal del enlace "app" */
            .st-emotion-cache-1wivap2 {
                display: none !important;
            }
            .st-emotion-cache-1wivap2 a {
                display: none !important;
            }
            
            /* Selector alternativo para Streamlit más reciente */
            .st-emotion-cache-1wivap2 {
                display: none !important;
            }
            
            /* Cualquier enlace que contenga "app" en el sidebar */
            .stSidebar a[href*="app"] {
                display: none !important;
            }
            .stSidebar a[href*="app.py"] {
                display: none !important;
            }
            
            /* Elemento contenedor del enlace "app" */
            .stSidebar .st-emotion-cache-1wivap2 {
                display: none !important;
            }
            .stSidebar .st-emotion-cache-1wivap2 a {
                display: none !important;
            }
            
            /* === OCULTAR MENÚ AUTOMÁTICO === */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            [data-testid="stSidebarNav"] a {
                display: none !important;
            }
            
            /* === OCULTAR FOOTER === */
            [data-testid="stFooter"] {
                display: none !important;
            }
            
            /* === ESTILO PARA RESULTADOS EN VERDE === */
            button[data-testid="baseButton-secondary"][aria-label="📊 Resultados"] {
                background-color: #2e7d32 !important;
                color: white !important;
                font-weight: 600 !important;
            }
            button[data-testid="baseButton-secondary"][aria-label="📊 Resultados"]:hover {
                background-color: #1b5e20 !important;
            }
            
            /* === OCULTAR CUALQUIER OTRO ENLACE NO DESEADO === */
            .stSidebar .st-emotion-cache-1wivap2 {
                display: none !important;
            }
            .stSidebar .st-emotion-cache-1wivap2 a {
                display: none !important;
            }
            
            /* === OCULTAR EL TEXTO "app" EN CUALQUIER LUGAR === */
            .stSidebar a:contains("app") {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # ✅ Menú lateral - RESULTADOS en VERDE
        if st.button("📊 Resultados", key="menu_resultados", use_container_width=True):
            st.switch_page("app.py")
        
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