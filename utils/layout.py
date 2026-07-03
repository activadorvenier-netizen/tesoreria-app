import streamlit as st

def mostrar_sidebar():

    with st.sidebar:

        st.image(
            "assets/logo_grupo_venier.png",
            use_container_width=True
        )

        st.markdown("---")

        st.caption("By Pato Frangi")