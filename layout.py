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

        # ✅ Versión alternativa con botones de Streamlit
        st.markdown("""
        <style>
            .btn-resultados {
                background-color: #2e7d32 !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                margin: 4px 0 !important;
                display: block !important;
                text-decoration: none !important;
                border: none !important;
            }
            .btn-resultados:hover {
                background-color: #1b5e20 !important;
            }
            .btn-normal {
                background-color: transparent !important;
                color: #262730 !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                margin: 4px 0 !important;
                display: block !important;
                text-decoration: none !important;
                border: none !important;
            }
            .btn-normal:hover {
                background-color: #f0f0f0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<a href="/pages/1_📊_Resultados" class="btn-resultados">📊 Resultados</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/3_🏦_Bancos" class="btn-normal">🏦 Bancos</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/4_🍺_Quilmes" class="btn-normal">🍺 Quilmes</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/5_💰_Cierre_Caja" class="btn-normal">💰 Cierre de Caja</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/6_📈_Plazos_Fijos" class="btn-normal">📈 Plazos Fijos</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/8_📊_Creditos" class="btn-normal">📊 Créditos</a>', unsafe_allow_html=True)
        st.markdown('<a href="/pages/7_⚙️_Administracion" class="btn-normal">⚙️ Administración</a>', unsafe_allow_html=True)

        st.markdown("---")

        st.caption("By Pato Frangi")