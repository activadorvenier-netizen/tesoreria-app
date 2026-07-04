import streamlit as st
import pandas as pd

from datetime import date
from dateutil.relativedelta import relativedelta

from utils.layout import mostrar_sidebar
from utils.sheets import (
    obtener_hoja,
    obtener_dataframe,
    generar_id_config,
    actualizar_config_por_id,
    eliminar_cierres_antiguos,
    eliminar_bancos_antiguos,
    eliminar_quilmes_antiguos
)

from utils.config import configurar_pagina
from utils.layout import mostrar_sidebar

configurar_pagina()
mostrar_sidebar()

st.title("⚙️ Administración")

# ====================================
# CARGA CONFIG
# ====================================

config_sheet = obtener_hoja("Config")

config = config_sheet.get_all_records()

df = pd.DataFrame(config)

# ====================================
# FUNCION GENERICA
# ====================================

def mostrar_seccion(
    titulo,
    tipo,
    permite_extra=False
):

    st.subheader(titulo)

    datos = df[
        df["Tipo"] == tipo
    ].copy()

    if datos.empty:

        st.info("Sin registros")

    else:

        for _, fila in datos.iterrows():

            id_registro = fila["ID"]

            valor = fila["Valor"]

            extra = (
                fila["Extra"]
                if "Extra" in fila
                else ""
            )

            activo = fila["Activo"]

            if (
                st.session_state.get(
                    f"edit_{tipo}"
                )
                == id_registro
            ):

                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )

                with col1:

                    nuevo_valor = st.text_input(
                        "",
                        value=valor,
                        key=f"valor_{id_registro}"
                    )

                with col2:

                    if permite_extra:

                        empresas_activas = df[
                            df["Tipo"] == "Empresa"
                        ].copy()

                        empresas_activas["Activo"] = (
                            empresas_activas["Activo"]
                            .astype(str)
                            .str.strip()
                            .str.upper()
                        )

                        lista_empresas = sorted(
                            empresas_activas[
                                empresas_activas["Activo"] == "SI"
                            ]["Valor"].tolist()
                        )

                        indice = 0

                        if extra in lista_empresas:
                            indice = lista_empresas.index(extra)

                        nuevo_extra = st.selectbox(
                            "",
                            lista_empresas,
                            index=indice,
                            key=f"extra_{id_registro}"
                        )

                    else:

                        nuevo_extra = extra

                with col3:

                    if st.button(
                        "💾",
                        key=f"save_{id_registro}"
                    ):

                        actualizar_config_por_id(
                            id_registro,
                            tipo,
                            nuevo_valor,
                            nuevo_extra,
                            activo
                        )

                        del st.session_state[
                            f"edit_{tipo}"
                        ]

                        st.rerun()

            else:

                col1, col2, col3, col4 = st.columns(
                    [4, 2, 1, 1]
                )

                with col1:

                    activo_normalizado = (
                        str(activo)
                        .strip()
                        .upper()
                    )

                    texto = valor

                    if activo_normalizado == "SI":

                        texto += " ✅"

                    else:

                        texto += " 🚫"

                    st.write(texto)

                with col2:

                    if permite_extra:

                        st.caption(extra)

                with col3:

                    if st.button(
                        "✏️",
                        key=f"edit_{id_registro}"
                    ):

                        st.session_state[
                            f"edit_{tipo}"
                        ] = id_registro

                        st.rerun()

                with col4:

                    etiqueta = (
                        "🚫"
                        if activo == "SI"
                        else "✅"
                    )

                    if st.button(
                        etiqueta,
                        key=f"toggle_{id_registro}"
                    ):

                        nuevo_estado = (
                            "NO"
                            if activo == "SI"
                            else "SI"
                        )

                        hoja = obtener_hoja(
                            "Config"
                        )

                        registros = (
                            hoja.get_all_values()
                        )

                        for i in range(
                            1,
                            len(registros)
                        ):

                            if str(
                                registros[i][0]
                            ) == str(
                                id_registro
                            ):

                                hoja.update(
                                    f"A{i+1}:E{i+1}",
                                    [[
                                        registros[i][0],
                                        registros[i][1],
                                        registros[i][2],
                                        registros[i][3],
                                        nuevo_estado
                                    ]]
                                )

                                break

                        st.rerun()

    st.divider()

    st.markdown("### ➕ Nuevo")

    col1, col2 = st.columns(2)

    with col1:

        etiqueta = (
            "Usuario"
            if tipo == "Usuario"
            else "Valor"
        )

        nuevo_valor = st.text_input(
            etiqueta,
            key=f"nuevo_{tipo}"
        )

    if permite_extra:

        with col2:

            lista_empresas = sorted(
                df[
                    (df["Tipo"] == "Empresa")
                    &
                    (df["Activo"] == "SI")
                ]["Valor"].tolist()
            )

            nuevo_extra = st.selectbox(
                "Empresa",
                ["Seleccione una empresa..."] + lista_empresas,
                index=0,
                key=f"empresa_{tipo}"
            )

    else:

        nuevo_extra = ""

    if st.button(
        f"➕ Agregar {tipo}",
        key=f"btn_{tipo}"
    ):

        if nuevo_valor:

            nuevo_id = generar_id_config()

            config_sheet.append_row([
                nuevo_id,
                tipo,
                nuevo_valor,
                nuevo_extra,
                "SI"
            ])

            st.success(
                "Registro agregado."
            )

            st.rerun()


# ====================================
# TABS
# ====================================

tab1, tab2, tab3 = st.tabs([
    "🏢 Empresas",
    "🏦 Bancos",
    "🗑️ Depuración"
])

# ====================================
# EMPRESAS
# ====================================

with tab1:

    mostrar_seccion(
        "Empresas",
        "Empresa"
    )

# ====================================
# BANCOS
# ====================================

with tab2:

    mostrar_seccion(
        "Bancos",
        "Banco"
    )

# ====================================
# DEPURACIÓN
# ====================================

with tab3:

    st.subheader("🗑️ Depuración de Datos Antiguos")

    st.info("""
    📅 **Período de conservación:** 3 meses
    
    Se conservarán todos los datos desde **3 meses atrás**.
    Se eliminarán todos los registros **anteriores** a esa fecha.
    """)

    hoy = date.today()
    fecha_base = date(
        hoy.year,
        hoy.month,
        1
    ) - relativedelta(months=3)

    st.metric(
        "📅 Fecha límite",
        fecha_base.strftime("%d/%m/%Y"),
        help="Todos los registros anteriores a esta fecha serán eliminados"
    )

    st.warning(
        "⚠️ Las acciones de depuración son **definitivas** y no se pueden deshacer."
    )

    st.divider()

    # ====================================
    # DEPURACIÓN DE CIERRE DE CAJA
    # ====================================

    with st.container(border=True):
        st.subheader("💰 Cierre de Caja")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"Eliminará todos los cierres anteriores a **{fecha_base.strftime('%d/%m/%Y')}**")

        with col2:
            if st.button(
                "🗑️ Depurar",
                type="primary",
                use_container_width=True,
                key="btn_cierres"
            ):
                st.session_state["confirmar_cierres"] = True

        with col3:
            if st.session_state.get("confirmar_cierres", False):
                if st.button(
                    "✅ Confirmar",
                    use_container_width=True,
                    key="ok_cierres"
                ):
                    cantidad = eliminar_cierres_antiguos(fecha_base)
                    st.session_state["confirmar_cierres"] = False
                    st.session_state["mensaje_depuracion"] = f"✅ {cantidad} cierres de caja eliminados correctamente."
                    st.rerun()

        if st.session_state.get("confirmar_cierres", False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❌ Cancelar",
                    use_container_width=True,
                    key="cancel_cierres"
                ):
                    st.session_state["confirmar_cierres"] = False
                    st.rerun()

    # ====================================
    # DEPURACIÓN DE BANCOS
    # ====================================

    with st.container(border=True):
        st.subheader("🏦 Bancos")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"Eliminará todos los registros bancarios anteriores a **{fecha_base.strftime('%d/%m/%Y')}**")

        with col2:
            if st.button(
                "🗑️ Depurar",
                type="primary",
                use_container_width=True,
                key="btn_bancos"
            ):
                st.session_state["confirmar_bancos"] = True

        with col3:
            if st.session_state.get("confirmar_bancos", False):
                if st.button(
                    "✅ Confirmar",
                    use_container_width=True,
                    key="ok_bancos"
                ):
                    cantidad = eliminar_bancos_antiguos(fecha_base)
                    st.session_state["confirmar_bancos"] = False
                    st.session_state["mensaje_depuracion"] = f"✅ {cantidad} registros bancarios eliminados correctamente."
                    st.rerun()

        if st.session_state.get("confirmar_bancos", False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❌ Cancelar",
                    use_container_width=True,
                    key="cancel_bancos"
                ):
                    st.session_state["confirmar_bancos"] = False
                    st.rerun()

    # ====================================
    # DEPURACIÓN DE QUILMES
    # ====================================

    with st.container(border=True):
        st.subheader("🍺 Quilmes")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"Eliminará todos los registros de Quilmes anteriores a **{fecha_base.strftime('%d/%m/%Y')}**")

        with col2:
            if st.button(
                "🗑️ Depurar",
                type="primary",
                use_container_width=True,
                key="btn_quilmes"
            ):
                st.session_state["confirmar_quilmes"] = True

        with col3:
            if st.session_state.get("confirmar_quilmes", False):
                if st.button(
                    "✅ Confirmar",
                    use_container_width=True,
                    key="ok_quilmes"
                ):
                    cantidad = eliminar_quilmes_antiguos(fecha_base)
                    st.session_state["confirmar_quilmes"] = False
                    st.session_state["mensaje_depuracion"] = f"✅ {cantidad} registros de Quilmes eliminados correctamente."
                    st.rerun()

        if st.session_state.get("confirmar_quilmes", False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❌ Cancelar",
                    use_container_width=True,
                    key="cancel_quilmes"
                ):
                    st.session_state["confirmar_quilmes"] = False
                    st.rerun()

    # ====================================
    # DEPURACIÓN COMPLETA
    # ====================================

    st.divider()

    with st.container(border=True):
        st.subheader("⚡ Depuración Completa")

        st.error("⚠️⚠️⚠️ Esto eliminará **TODOS** los datos antiguos de las tres secciones simultáneamente.")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"Eliminará datos de Cierre de Caja, Bancos y Quilmes anteriores a **{fecha_base.strftime('%d/%m/%Y')}**")

        with col2:
            if st.button(
                "🗑️ Depurar Todo",
                type="primary",
                use_container_width=True,
                key="btn_todo"
            ):
                st.session_state["confirmar_todo"] = True

        with col3:
            if st.session_state.get("confirmar_todo", False):
                if st.button(
                    "✅ Confirmar Todo",
                    use_container_width=True,
                    key="ok_todo"
                ):
                    total = 0
                    
                    c1 = eliminar_cierres_antiguos(fecha_base)
                    total += c1
                    
                    c2 = eliminar_bancos_antiguos(fecha_base)
                    total += c2
                    
                    c3 = eliminar_quilmes_antiguos(fecha_base)
                    total += c3
                    
                    st.session_state["confirmar_todo"] = False
                    st.session_state["mensaje_depuracion"] = f"✅ Depuración completa: {total} registros eliminados en total."
                    st.rerun()

        if st.session_state.get("confirmar_todo", False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❌ Cancelar Todo",
                    use_container_width=True,
                    key="cancel_todo"
                ):
                    st.session_state["confirmar_todo"] = False
                    st.rerun()

    # ====================================
    # MOSTRAR MENSAJES DE ÉXITO
    # ====================================

    if "mensaje_depuracion" in st.session_state:
        st.success(st.session_state["mensaje_depuracion"])
        st.balloons()
        del st.session_state["mensaje_depuracion"]