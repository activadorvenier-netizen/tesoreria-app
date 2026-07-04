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

        # ✅ CSS para el menú con RESULTADOS en VERDE
        st.markdown("""
        <style>
            /* Menú personalizado */
            .custom-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .custom-menu li {
                padding: 10px 14px;
                margin: 4px 0;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 500;
                transition: all 0.2s ease;
                cursor: pointer;
            }
            .custom-menu li a {
                text-decoration: none;
                color: #262730;
                display: block;
                width: 100%;
            }
            .custom-menu li:hover {
                background-color: #f0f0f0;
            }
            .custom-menu .destacado {
                background-color: #2e7d32 !important;
                color: white !important;
                font-weight: 600;
                border-left: 4px solid #1b5e20;
            }
            .custom-menu .destacado a {
                color: white !important;
            }
            .custom-menu .destacado:hover {
                background-color: #1b5e20 !important;
            }
        </style>
        
        <ul class="custom-menu">
            <li class="destacado"><a href="/pages/1_📊_Resultados">📊 Resultados</a></li>
            <li><a href="/pages/3_🏦_Bancos">🏦 Bancos</a></li>
            <li><a href="/pages/4_🍺_Quilmes">🍺 Quilmes</a></li>
            <li><a href="/pages/5_💰_Cierre_Caja">💰 Cierre de Caja</a></li>
            <li><a href="/pages/6_📈_Plazos_Fijos">📈 Plazos Fijos</a></li>
            <li><a href="/pages/8_📊_Creditos">📊 Créditos</a></li>
            <li><a href="/pages/7_⚙️_Administracion">⚙️ Administración</a></li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.caption("By Pato Frangi")