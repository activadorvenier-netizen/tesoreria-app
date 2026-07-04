import streamlit as st

def configurar_pagina():
    """Configuración común para todas las páginas"""
    st.set_page_config(
        page_title="Tesorería",
        page_icon="💰",
        layout="wide"
    )
    
    # Ocultar menú automático
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stFooter"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)