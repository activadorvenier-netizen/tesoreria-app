import streamlit as st
import pandas as pd

from datetime import date, timedelta

from utils.sheets import (
    obtener_hoja,
    actualizar_banco,
    eliminar_banco
)

def formato_moneda(valor):

    return f"$ {float(valor):,.0f}".replace(",", ".")

def mostrar_bancos():
        
    if "banco_editar" not in st.session_state:
        st.session_state.banco_editar = None

    if "eliminar_banco" not in st.session_state:
        st.session_state.eliminar_banco = None

    bancos_sheet = obtener_hoja("Bancos")

    bancos_df = pd.DataFrame(
        bancos_sheet.get_all_records()
    )

    if bancos_df.empty:

        st.info("No hay posiciones bancarias cargadas.")

        return

    st.subheader("🏦 Bancos")

    if not bancos_df.empty:

        col1, col2, col3 = st.columns([1,1,1.5])

        with col1:

            fecha_desde = st.date_input(
            "Desde",
            value=date.today() - timedelta(days=30),
            key="desde_bancos"
        )

        with col2:

            fecha_hasta = st.date_input(
                "Hasta",
                value=date.today(),
                key="hasta_bancos"
            )

        with col3:

            empresa_filtro = st.selectbox(
                "Empresa",
                ["Todas"] +
                sorted(
                    bancos_df["Empresa"]
                    .dropna()
                    .unique()
                    .tolist()
                ),
                key="empresa_bancos"
            )

        bancos_df["Fecha"] = pd.to_datetime(
            bancos_df["Fecha"]
        )

        bancos_df = bancos_df[
            (bancos_df["Fecha"].dt.date >= fecha_desde)
            &
            (bancos_df["Fecha"].dt.date <= fecha_hasta)
        ]

        if empresa_filtro != "Todas":

            bancos_df = bancos_df[
                bancos_df["Empresa"] == empresa_filtro
            ]

        bancos_df = bancos_df.sort_values(
            "Fecha",
            ascending=False
        ).head(15)

        h1,h2,h3,h4,h5,h6,h7,h8,h9 = st.columns(
            [1.2,1,1.1,1.1,1.1,1.1,1,0.7,0.7]
        )

        h1.markdown("**Fecha**")
        h2.markdown("**Empresa**")
        h3.markdown("**Galicia**")
        h4.markdown("**Macro**")
        h5.markdown("**Credicoop**")
        h6.markdown("**Santander**")
        h7.markdown("**Total**")
        h8.markdown("")
        h9.markdown("")

        st.divider()

        bancos_df["Galicia"] = (
            bancos_df["GaliciaSaldo"].astype(float)
            + bancos_df["GaliciaFCI"].astype(float)
        )

        bancos_df["Macro"] = (
            bancos_df["MacroSaldo"].astype(float)
            + bancos_df["MacroFCI"].astype(float)
        )

        bancos_df["Credicoop"] = (
            bancos_df["CredicoopSaldo"].astype(float)
            + bancos_df["CredicoopFCI"].astype(float)
        )

        bancos_df["Santander"] = (
            bancos_df["SantanderSaldo"].astype(float)
            + bancos_df["SantanderFCI"].astype(float)
        )

        bancos_df["Total"] = (
            bancos_df["Galicia"]
            + bancos_df["Macro"]
            + bancos_df["Credicoop"]
            + bancos_df["Santander"]
        )

        for _, fila in bancos_df.iterrows():

            c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns(
                [1.1,1,1.1,1.1,1.1,1.1,1,0.5,0.5]
            )

            c1.write(fila["Fecha"].strftime("%d/%m/%Y"))
            c2.write(fila["Empresa"])
            c3.write(formato_moneda(fila["Galicia"]))
            c4.write(formato_moneda(fila["Macro"]))
            c5.write(formato_moneda(fila["Credicoop"]))
            c6.write(formato_moneda(fila["Santander"]))
            c7.write(f"**{formato_moneda(fila['Total'])}**")

            with c8:

                if st.button(
                    "✏️",
                    key=f"edit_banco_{fila['ID']}"
                ):

                    st.session_state.banco_editar = fila["ID"]
                    st.rerun()

            with c9:

                if (
                    st.session_state.get("eliminar_banco")
                    == fila["ID"]
                ):

                    col_si, col_no = st.columns(2)

                    with col_si:

                        if st.button(
                            "✅",
                            key=f"ok_banco_{fila['ID']}"
                        ):

                            eliminar_banco(fila["ID"])

                            st.session_state.eliminar_banco = None

                            st.rerun()

                    with col_no:

                        if st.button(
                            "❌",
                            key=f"cancel_banco_{fila['ID']}"
                        ):

                            st.session_state.eliminar_banco = None

                            st.rerun()

                else:

                    if st.button(
                        "🗑️",
                        key=f"del_banco_{fila['ID']}"
                    ):

                        st.session_state.eliminar_banco = fila["ID"]

                        st.rerun()

            st.divider()

            if st.session_state.get("banco_editar") == fila["ID"]:

                with st.container(border=True):

                    st.subheader(
                        f"✏️ Editando Bancos - {fila['Empresa']}"
                    )

                    fecha_edit = st.date_input(
                        "Fecha",
                        value=fila["Fecha"].date(),
                        key=f"fecha_{fila['ID']}"
                    )

                    st.divider()

                    h1,h2,h3 = st.columns([1.4,1,1])

                    h1.markdown("**Banco**")
                    h2.markdown("**Saldo Cuenta**")
                    h3.markdown("**FCI**")

                    st.divider()

                    bancos = [
                        ("Galicia","GaliciaSaldo","GaliciaFCI","gs","gf"),
                        ("Macro","MacroSaldo","MacroFCI","ms","mf"),
                        ("Credicoop","CredicoopSaldo","CredicoopFCI","cs","cf"),
                        ("Santander","SantanderSaldo","SantanderFCI","ss","sf")
                    ]

                    valores = {}

                    for nombre,col_saldo,col_fci,key_s,key_f in bancos:

                        c1,c2,c3 = st.columns([1.4,1,1])

                        c1.write(nombre)

                        with c2:

                            valores[col_saldo] = st.number_input(
                                "",
                                value=float(fila[col_saldo]),
                                key=f"{key_s}_{fila['ID']}",
                                label_visibility="collapsed"
                            )

                        with c3:

                            valores[col_fci] = st.number_input(
                                "",
                                value=float(fila[col_fci]),
                                key=f"{key_f}_{fila['ID']}",
                                label_visibility="collapsed"
                            )

                    st.divider()

                    b1,b2 = st.columns(2)

                    with b1:

                        if st.button(
                            "💾 Guardar",
                            key=f"save_{fila['ID']}"
                        ):

                            actualizar_banco(
                                fila["ID"],
                                fecha_edit.strftime("%Y-%m-%d"),
                                fila["Empresa"],
                                valores["GaliciaSaldo"],
                                valores["GaliciaFCI"],
                                valores["MacroSaldo"],
                                valores["MacroFCI"],
                                valores["CredicoopSaldo"],
                                valores["CredicoopFCI"],
                                valores["SantanderSaldo"],
                                valores["SantanderFCI"]
                            )

                            st.session_state.banco_editar = None
                            st.rerun()

                    with b2:

                        if st.button(
                            "❌ Cancelar",
                            key=f"cancel_{fila['ID']}"
                        ):

                            st.session_state.banco_editar = None
                            st.rerun()    