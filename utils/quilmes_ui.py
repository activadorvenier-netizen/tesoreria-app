import streamlit as st
import pandas as pd

from datetime import date, timedelta

from utils.sheets import (
    obtener_hoja,
    actualizar_quilmes,
    eliminar_quilmes
)

def formato_moneda(valor):

    return f"$ {float(valor):,.0f}".replace(",", ".")

def mostrar_quilmes():

    if "quilmes_editar" not in st.session_state:
        st.session_state.quilmes_editar = None

    if "eliminar_quilmes" not in st.session_state:
        st.session_state.eliminar_quilmes = None

    quilmes_sheet = obtener_hoja("Quilmes")

    quilmes_df = pd.DataFrame(
        quilmes_sheet.get_all_records()
    )

    if quilmes_df.empty:

        st.info("No existen registros cargados.")

        return

    st.subheader("🍺 Quilmes")

    col1, col2, col3 = st.columns([1,1,1.5])

    with col1:

        fecha_desde = st.date_input(
            "Desde",
            value=date.today()-timedelta(days=30),
            key="desde_quilmes"
        )

    with col2:

        fecha_hasta = st.date_input(
            "Hasta",
            value=date.today(),
            key="hasta_quilmes"
        )

    with col3:

        empresa_filtro = st.selectbox(
            "Empresa",
            ["Todas"] +
            sorted(
                quilmes_df["Empresa"]
                .dropna()
                .unique()
                .tolist()
            ),
            key="empresa_quilmes"
        )

    quilmes_df["Fecha"] = pd.to_datetime(
        quilmes_df["Fecha"]
    )

    quilmes_df = quilmes_df[
        (quilmes_df["Fecha"].dt.date >= fecha_desde)
        &
        (quilmes_df["Fecha"].dt.date <= fecha_hasta)
    ]

    if empresa_filtro != "Todas":

        quilmes_df = quilmes_df[
            quilmes_df["Empresa"] == empresa_filtro
        ]

    quilmes_df = quilmes_df.sort_values(
        "Fecha",
        ascending=False
    ).head(15)

    h1,h2,h3,h4,h5,h6,h7,h8 = st.columns(
        [1.1,1,1,1,1,1,0.45,0.45]
    )

    h1.markdown("**Fecha**")
    h2.markdown("**Empresa**")
    h3.markdown("**Deuda**")
    h4.markdown("**NC**")
    h5.markdown("**Cobertura**")
    h6.markdown("**Necesidad**")
    h7.markdown("")
    h8.markdown("")

    st.divider()

    for _, fila in quilmes_df.iterrows():

        cobertura = (
            float(fila["PromesaNC"])
            +
            float(fila["ChequesEmitidos"])
            +
            float(fila["Depositos"])
            +
            float(fila["Efectivo"])
        )

        necesidad = (
            float(fila["NecesidadQuilmes"])
        )

        c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(
            [1.1,1,1,1,1,1,0.45,0.45]
        )

        c1.write(
            fila["Fecha"].strftime("%d/%m/%Y")
        )

        c2.write(
            fila["Empresa"]
        )

        c3.write(
            formato_moneda(fila["DeudaPagar"])
        )

        c4.write(
            formato_moneda(fila["PromesaNC"])
        )

        c5.write(
            formato_moneda(cobertura)
        )

        c6.write(
            f"**{formato_moneda(necesidad)}**"
        )

        with c7:

            if st.button(
                "✏️",
                key=f"edit_quilmes_{fila['ID']}"
            ):

                st.session_state.quilmes_editar = fila["ID"]
                st.rerun()

        with c8:

            if (
                st.session_state.get("eliminar_quilmes")
                ==
                fila["ID"]
            ):

                col_si, col_no = st.columns(2)

                with col_si:

                    if st.button(
                        "✅",
                        key=f"ok_quilmes_{fila['ID']}"
                    ):

                        eliminar_quilmes(
                            fila["ID"]
                        )

                        st.session_state.eliminar_quilmes = None
                        st.rerun()

                with col_no:

                    if st.button(
                        "❌",
                        key=f"cancel_quilmes_{fila['ID']}"
                    ):

                        st.session_state.eliminar_quilmes = None
                        st.rerun()

            else:

                if st.button(
                    "🗑️",
                    key=f"del_quilmes_{fila['ID']}"
                ):

                    st.session_state.eliminar_quilmes = fila["ID"]
                    st.rerun()

        st.divider()

    if st.session_state.get("quilmes_editar") == fila["ID"]:

        with st.container(border=True):

            st.subheader(
                f"✏️ Editando Quilmes - {fila['Empresa']}"
            )

            fecha_edit = st.date_input(
                "Fecha",
                value=fila["Fecha"].date(),
                key=f"fecha_q_{fila['ID']}"
            )

            deuda = st.number_input(
                "Deuda a Pagar",
                value=float(fila["DeudaPagar"]),
                key=f"deuda_{fila['ID']}"
            )

            nc = st.number_input(
                "Promesa NC",
                value=float(fila["PromesaNC"]),
                key=f"nc_{fila['ID']}"
            )

            cheques = st.number_input(
                "Cheques Emitidos",
                value=float(fila["ChequesEmitidos"]),
                key=f"cheques_{fila['ID']}"
            )

            depositos = st.number_input(
                "Depósitos",
                value=float(fila["Depositos"]),
                key=f"depositos_{fila['ID']}"
            )

            efectivo = st.number_input(
                "Efectivo",
                value=float(fila["Efectivo"]),
                key=f"efectivo_{fila['ID']}"
            )

            necesidad = (
                deuda
                -
                (
                    nc
                    + cheques
                    + depositos
                    + efectivo
                )
            )

            st.metric(
                "Necesidad Quilmes",
                formato_moneda(necesidad)
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Guardar",
                    key=f"save_q_{fila['ID']}"
                ):

                    actualizar_quilmes(
                        fila["ID"],
                        fecha_edit.strftime("%Y-%m-%d"),
                        fila["Empresa"],
                        deuda,
                        nc,
                        cheques,
                        depositos,
                        efectivo
                    )

                    st.session_state.quilmes_editar = None

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Cancelar",
                    key=f"cancel_q_{fila['ID']}"
                ):

                    st.session_state.quilmes_editar = None

                    st.rerun()