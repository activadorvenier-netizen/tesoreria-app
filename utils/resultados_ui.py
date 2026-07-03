import streamlit as st
import pandas as pd

def mostrar_tarjeta_bancos(
    empresa,
    bancos_empresa
):

    st.subheader("🏦 Bancos")

    with st.container(border=True):

        h1,h2,h3 = st.columns([2,1.2,1.2])

        h1.markdown("**Banco**")
        h2.markdown("**Disponible**")
        h3.markdown("**Plazo Fijo**")

        st.divider()

        bancos = [
            (
                "Galicia",
                bancos_empresa["galicia"],
                bancos_empresa["pf_galicia"]
            ),
            (
                "Macro",
                bancos_empresa["macro"],
                bancos_empresa["pf_macro"]
            ),
            (
                "Credicoop",
                bancos_empresa["credicoop"],
                bancos_empresa["pf_credicoop"]
            ),
            (
                "Santander",
                bancos_empresa["santander"],
                bancos_empresa["pf_santander"]
            )
        ]

        for nombre, disponible, pf in bancos:

            c1,c2,c3 = st.columns([2,1.2,1.2])

            c1.write(f"🏦 {nombre}")

            c2.write(
                f"$ {disponible:,.0f}".replace(",",".")
            )

            c3.write(
                f"$ {pf:,.0f}".replace(",",".")
            )

        st.divider()

        c1,c2,c3 = st.columns([2,1.2,1.2])

        c1.markdown("**TOTAL**")

        c2.markdown(
            f"**$ {bancos_empresa['total_bancos']:,.0f}**".replace(",",".")
        )

        c3.markdown(
            f"**$ {bancos_empresa['total_pf']:,.0f}**".replace(",",".")
        )

def mostrar_tarjeta_pf(
    detalle_pf
):

    st.subheader("📈 Plazos Fijos")

    with st.container(border=True):

        if detalle_pf.empty:

            st.info(
                "No existen Plazos Fijos."
            )

            return

        cab = st.columns(
            [1.1,1.2,1.2,1,1]
        )

        cab[0].markdown("**Empresa**")
        cab[1].markdown("**Banco**")
        cab[2].markdown("**Capital**")
        cab[3].markdown("**Tasa**")
        cab[4].markdown("**Vencimiento**")

        st.divider()

        total = 0

        for _, fila in detalle_pf.iterrows():

            total += float(
                fila["Capital"]
            )

            c = st.columns(
                [1.1,1.2,1.2,1,1]
            )

            c[0].write(
                fila["Empresa"]
            )

            c[1].write(
                fila["Banco"]
            )

            c[2].write(
                f"$ {float(fila['Capital']):,.0f}".replace(",",".")
            )

            c[3].write(
                f"{float(fila['Tasa'])}%"
            )

            c[4].write(
                pd.to_datetime(
                    fila["Vencimiento"]
                ).strftime("%d/%m/%Y")
            )

        st.divider()

        st.markdown(
            f"### Total PF: $ {total:,.0f}".replace(",",".")
        )