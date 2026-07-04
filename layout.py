import streamlit as st

def mostrar_sidebar():
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
        
        # ✅ Menú lateral con "Resultados" coloreado
        st.markdown("""
        <style>
            /* Estilo para el menú lateral */
            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .sidebar-menu li {
                padding: 8px 12px;
                margin: 4px 0;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                transition: all 0.2s;
            }
            .sidebar-menu li a {
                text-decoration: none;
                color: #262730;
                display: block;
            }
            .sidebar-menu li:hover {
                background-color: #f0f0f0;
            }
            .sidebar-menu .destacado {
                background-color: #2e7d32 !important;
                color: white !important;
                font-weight: 600;
            }
            .sidebar-menu .destacado a {
                color: white !important;
            }
            .sidebar-menu .destacado:hover {
                background-color: #1b5e20 !important;
            }
        </style>
        <ul class="sidebar-menu">
            <li class="destacado">📊 Resultados</li>
            <li>🏦 Bancos</li>
            <li>🍺 Quilmes</li>
            <li>💰 Cierre de Caja</li>
            <li>📈 Plazos Fijos</li>
            <li>📊 Créditos</li>
            <li>⚙️ Administración</li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.caption("By Pato Frangi")