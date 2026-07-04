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
    
    # ✅ Ocultar menú automático de Streamlit
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stFooter"] {
            display: none !important;
        }
        /* Estilos para los botones del menú */
        .menu-btn {
            display: block;
            width: 100%;
            padding: 10px 14px;
            margin: 4px 0;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
            text-decoration: none;
            color: #262730;
            background-color: transparent;
            transition: all 0.2s ease;
        }
        .menu-btn:hover {
            background-color: #f0f0f0;
        }
        .menu-btn-destacado {
            background-color: #2e7d32 !important;
            color: white !important;
            font-weight: 600;
        }
        .menu-btn-destacado:hover {
            background-color: #1b5e20 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ✅ Menú con botones - RESULTADOS en VERDE
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

st.title("💰 Tesorería Grupo Venier")

st.info(
    "Seleccione una opción del menú lateral para gestionar la tesorería del grupo."
)

# ============================================
# ACCESOS RÁPIDOS EN 6 COLUMNAS
# ============================================

st.divider()
st.subheader("📌 Accesos Rápidos")

st.markdown("""
<style>
    .stButton button {
        font-weight: 500 !important;
        font-size: 12px !important;
        padding: 4px 8px !important;
        min-height: 32px !important;
        height: 32px !important;
    }
    .stLinkButton button {
        font-weight: 500 !important;
        font-size: 12px !important;
        padding: 4px 8px !important;
        min-height: 32px !important;
        height: 32px !important;
    }
    div[data-testid="column"] {
        min-width: 100px !important;
        padding: 0 4px !important;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

with col1:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #2e7d32; font-size: 28px;">📊</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Resultados</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Resumen</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "📈 Ir",
            key="btn_resultados",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/1_📊_Resultados.py")

with col2:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #d32f2f; font-size: 28px;">💰</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Cierre Caja</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Cierres</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "💰 Ir",
            key="btn_cierre_caja",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/5_💰_Cierre_Caja.py")

with col3:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #f57c00; font-size: 28px;">🏦</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Bancos</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Posición</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "🏦 Ir",
            key="btn_bancos",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/3_🏦_Bancos.py")

with col4:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #00838f; font-size: 28px;">📈</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Plazos Fijos</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Inversiones</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "📈 Ir",
            key="btn_plazos_fijos",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/6_📈_Plazos_Fijos.py")

with col5:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #6a1b9a; font-size: 28px;">📊</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Créditos</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Gestión</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "📊 Ir",
            key="btn_creditos",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/8_📊_Creditos.py")

with col6:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 5px 0;">
            <h2 style="margin: 0; color: #6a1b9a; font-size: 28px;">🍺</h2>
            <h4 style="margin: 4px 0; font-weight: 600; font-size: 13px;">Quilmes</h4>
            <p style="color: #666; font-size: 10px; margin: 2px 0 8px 0;">Deuda</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "🍺 Ir",
            key="btn_quilmes",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page("pages/4_🍺_Quilmes.py")

st.caption("💡 Los accesos rápidos están disponibles para agilizar tu trabajo diario.")