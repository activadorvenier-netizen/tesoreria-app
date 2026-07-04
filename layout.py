import streamlit as st

def mostrar_sidebar():

    with st.sidebar:

        st.image(
            "assets/logo_grupo_venier.png",
            use_container_width=True
        )

        st.markdown("---")

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

        st.markdown("---")

        # ✅ Menú lateral con "Resultados" coloreado
        st.markdown("""
        <style>
            .menu-item {
                padding: 8px 12px;
                margin: 2px 0;
                border-radius: 6px;
                font-size: 14px;
                text-decoration: none;
                display: block;
                color: #262730;
                background-color: transparent;
            }
            .menu-item:hover {
                background-color: #f0f0f0;
            }
            .menu-destacado {
                background-color: #2e7d32 !important;
                color: white !important;
                font-weight: 600;
            }
            .menu-destacado:hover {
                background-color: #1b5e20 !important;
            }
            .menu-link {
                color: #262730;
                text-decoration: none;
            }
            .menu-destacado .menu-link {
                color: white !important;
            }
        </style>
        
        <a href="/pages/1_📊_Resultados" class="menu-item menu-destacado">📊 Resultados</a>
        <a href="/pages/3_🏦_Bancos" class="menu-item">🏦 Bancos</a>
        <a href="/pages/4_🍺_Quilmes" class="menu-item">🍺 Quilmes</a>
        <a href="/pages/5_💰_Cierre_Caja" class="menu-item">💰 Cierre de Caja</a>
        <a href="/pages/6_📈_Plazos_Fijos" class="menu-item">📈 Plazos Fijos</a>
        <a href="/pages/8_📊_Creditos" class="menu-item">📊 Créditos</a>
        <a href="/pages/7_⚙️_Administracion" class="menu-item">⚙️ Administración</a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.caption("By Pato Frangi")