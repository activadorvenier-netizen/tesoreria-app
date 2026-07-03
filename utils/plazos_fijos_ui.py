import streamlit as st
import pandas as pd

from datetime import date, timedelta

from utils.sheets import (
    obtener_hoja,
    actualizar_plazo_fijo,
    eliminar_plazo_fijo
)

def formato_moneda(valor):

    return f"$ {float(valor):,.0f}".replace(",", ".")

if "pf_editar" not in st.session_state:
    st.session_state.pf_editar = None

if "eliminar_pf" not in st.session_state:
    st.session_state.eliminar_pf = None

import streamlit as st
import pandas as pd

from datetime import date, timedelta

from utils.sheets import (
    obtener_hoja,
    actualizar_plazo_fijo,
    eliminar_plazo_fijo
)


def formato_moneda(valor):

    return f"$ {float(valor):,.0f}".replace(",", ".")


def mostrar_plazos_fijos():

    if "pf_editar" not in st.session_state:
        st.session_state.pf_editar = None

    if "eliminar_pf" not in st.session_state:
        st.session_state.eliminar_pf = None

    hoja = obtener_hoja("PlazosFijos")

    pf_df = pd.DataFrame(
        hoja.get_all_records()
    )

    if pf_df.empty:

        st.info(
            "No existen Plazos Fijos cargados."
        )

        return

    st.subheader("📈 Plazos Fijos")

    col1, col2, col3 = st.columns([1,1,1.5])

    with col1:

        fecha_desde = st.date_input(
            "Desde",
            value=date.today() - timedelta(days=30),
            key="desde_pf"
        )

    with col2:

        fecha_hasta = st.date_input(
            "Hasta",
            value=date.today(),
            key="hasta_pf"
        )

    with col3:

        empresa_filtro = st.selectbox(
            "Empresa",
            ["Todas"] +
            sorted(
                pf_df["Empresa"]
                .dropna()
                .unique()
                .tolist()
            ),
            key="empresa_pf"
        )

    pf_df["Fecha"] = pd.to_datetime(
        pf_df["Fecha"]
    )

    pf_df = pf_df[
        (pf_df["Fecha"].dt.date >= fecha_desde)
        &
        (pf_df["Fecha"].dt.date <= fecha_hasta)
    ]

    if empresa_filtro != "Todas":

        pf_df = pf_df[
            pf_df["Empresa"] == empresa_filtro
        ]

    pf_df = pf_df.sort_values(
        "Fecha",
        ascending=False
    ).head(15)

    h1,h2,h3,h4,h5,h6,h7,h8 = st.columns(
        [1.2,1,1.2,1.2,1,1.2,0.5,0.5]
    )

    h1.markdown("**Fecha**")
    h2.markdown("**Empresa**")
    h3.markdown("**Banco**")
    h4.markdown("**Capital**")
    h5.markdown("**Tasa**")
    h6.markdown("**Vencimiento**")
    h7.markdown("")
    h8.markdown("")

    st.divider()

    for _, fila in pf_df.iterrows():

        capital = float(fila["Capital"])

        c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(
            [1.2,1,1.2,1.2,1,1.2,0.5,0.5]
        )

        c1.write(
            fila["Fecha"].strftime("%d/%m/%Y")
        )

        c2.write(
            fila["Empresa"]
        )

        c3.write(
            fila["Banco"]
        )

        c4.write(
            formato_moneda(capital)
        )

        c5.write(
            f"{float(fila['Tasa']):.2f}%"
        )

        c6.write(
            pd.to_datetime(
                fila["Vencimiento"]
            ).strftime("%d/%m/%Y")
        )

        with c7:

            if st.button(
                "✏️",
                key=f"edit_pf_{fila['ID']}"
            ):

                st.session_state.pf_editar = fila["ID"]

                st.rerun()

        with c8:

            if (
                st.session_state.get("eliminar_pf")
                ==
                fila["ID"]
            ):

                col_si, col_no = st.columns(2)

                with col_si:

                    if st.button(
                        "✅",
                        key=f"ok_pf_{fila['ID']}"
                    ):

                        eliminar_plazo_fijo(
                            fila["ID"]
                        )

                        st.session_state.eliminar_pf = None

                        st.rerun()

                with col_no:

                    if st.button(
                        "❌",
                        key=f"cancel_del_pf_{fila['ID']}"
                    ):

                        st.session_state.eliminar_pf = None

                        st.rerun()

            else:

                if st.button(
                    "🗑️",
                    key=f"del_pf_{fila['ID']}"
                ):

                    st.session_state.eliminar_pf = fila["ID"]

                    st.rerun()

        st.divider()

        if st.session_state.get("pf_editar") == fila["ID"]:

            with st.container(border=True):

                st.subheader(
                    f"✏️ Editando Plazo Fijo - {fila['Banco']}"
                )

                fecha_edit = st.date_input(
                    "Fecha",
                    value=fila["Fecha"].date(),
                    key=f"fecha_pf_{fila['ID']}"
                )

                banco_edit = st.text_input(
                    "Banco",
                    value=fila["Banco"],
                    key=f"banco_pf_{fila['ID']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    capital_edit = st.number_input(
                        "Capital",
                        value=float(fila["Capital"]),
                        key=f"capital_pf_{fila['ID']}"
                    )

                with col2:

                    tasa_edit = st.number_input(
                        "Tasa",
                        value=float(fila["Tasa"]),
                        key=f"tasa_pf_{fila['ID']}"
                    )

                vencimiento_edit = st.date_input(
                    "Vencimiento",
                    value=pd.to_datetime(
                        fila["Vencimiento"]
                    ).date(),
                    key=f"vto_pf_{fila['ID']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "💾 Guardar",
                        key=f"save_pf_{fila['ID']}"
                    ):

                        actualizar_plazo_fijo(
                            fila["ID"],
                            fecha_edit.strftime("%Y-%m-%d"),
                            fila["Empresa"],
                            banco_edit,
                            capital_edit,
                            tasa_edit,
                            vencimiento_edit.strftime("%Y-%m-%d")
                        )

                        st.session_state.pf_editar = None

                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Cancelar",
                        key=f"cancel_pf_{fila['ID']}"
                    ):

                        st.session_state.pf_editar = None

                        st.rerun()