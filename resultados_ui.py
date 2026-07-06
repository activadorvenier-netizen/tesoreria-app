import streamlit as st
import pandas as pd

def mostrar_tarjeta_bancos(
    empresa,
    bancos_empresa
):

    st.subheader("🏦 Bancos")

    with st.container(border=True):

        # ✅ 5 columnas: Banco, Saldo, FCI, Total Disponible, PF
        h1, h2, h3, h4, h5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

        h1.markdown("**Banco**")
        h2.markdown("**Saldo**")
        h3.markdown("**FCI**")
        h4.markdown("**Total Disponible**")
        h5.markdown("**Plazo Fijo**")

        st.divider()

        # ✅ Bancos definidos
        bancos_definidos = ["Galicia", "Macro", "Credicoop", "Santander"]
        
        # ✅ Diccionario para almacenar todos los datos
        datos_bancos = {}
        total_saldo = 0
        total_fci = 0
        total_disponible = 0
        total_pf = 0
        
        # ✅ Procesar bancos definidos
        for banco in bancos_definidos:
            # Obtener saldo y FCI del banco
            saldo = bancos_empresa.get(banco.lower(), 0)
            pf = bancos_empresa.get(f"pf_{banco.lower()}", 0)
            
            # Calcular FCI (la diferencia entre Total y Saldo)
            # En tu estructura, galicia = Saldo + FCI, y pf_galicia = PF
            # Por lo tanto, FCI = galicia - (galicia - pf_galicia) ??? 
            # Mejor: asumimos que el campo "galicia" ya incluye FCI
            # Necesitamos saber cómo se estructura
            
            # Como no tenemos FCI separado, lo calculamos como la diferencia
            # entre el total del banco y el saldo de cuenta
            # Para simplificar, usamos 0 si no hay FCI
            fci = 0  # Por ahora, lo dejamos en 0
            
            # O usar la estructura que tengas:
            # Si tienes galicia_saldo y galicia_fci por separado
            # fci = bancos_empresa.get(f"fci_{banco.lower()}", 0)
            
            datos_bancos[banco] = {
                "saldo": saldo - pf,  # Saldo es Total - PF (asumiendo que Total incluye PF)
                "fci": 0,  # A ajustar según tu estructura
                "disponible": saldo,
                "pf": pf
            }
            
            total_saldo += datos_bancos[banco]["saldo"]
            total_fci += datos_bancos[banco]["fci"]
            total_disponible += datos_bancos[banco]["disponible"]
            total_pf += datos_bancos[banco]["pf"]

        # ✅ Procesar otros bancos (los que no están en la lista)
        # Buscar en bancos_empresa las claves que no sean bancos definidos
        otras_llaves = [
            k for k in bancos_empresa.keys() 
            if k not in [b.lower() for b in bancos_definidos] 
            and k not in [f"pf_{b.lower()}" for b in bancos_definidos]
            and k not in ["total_bancos", "total_pf", "detalle_pf"]
        ]
        
        # Filtrar solo las que parecen ser bancos (nombres de bancos)
        otros_bancos = []
        for llave in otras_llaves:
            # Si la llave parece un nombre de banco (no contiene "pf_")
            if not llave.startswith("pf_"):
                valor = bancos_empresa.get(llave, 0)
                pf = bancos_empresa.get(f"pf_{llave}", 0)
                if valor > 0 or pf > 0:
                    otros_bancos.append({
                        "nombre": llave.capitalize(),
                        "saldo": valor - pf,
                        "fci": 0,
                        "disponible": valor,
                        "pf": pf
                    })
                    total_saldo += valor - pf
                    total_disponible += valor
                    total_pf += pf

        # ✅ Mostrar bancos definidos
        for banco in bancos_definidos:
            datos = datos_bancos[banco]
            
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

            c1.write(f"🏦 {banco}")
            c2.write(f"$ {datos['saldo']:,.0f}".replace(",", "."))
            c3.write(f"$ {datos['fci']:,.0f}".replace(",", "."))
            
            # ✅ Total Disponible en NEGRITA
            c4.markdown(
                f"**$ {datos['disponible']:,.0f}**".replace(",", ".")
            )
            
            c5.write(f"$ {datos['pf']:,.0f}".replace(",", "."))

        # ✅ Mostrar "Otros Bancos" si hay
        if otros_bancos:
            for otro in otros_bancos:
                c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

                c1.write(f"🏦 {otro['nombre']}")
                c2.write(f"$ {otro['saldo']:,.0f}".replace(",", "."))
                c3.write(f"$ {otro['fci']:,.0f}".replace(",", "."))
                c4.markdown(
                    f"**$ {otro['disponible']:,.0f}**".replace(",", ".")
                )
                c5.write(f"$ {otro['pf']:,.0f}".replace(",", "."))

        # ✅ Totales
        st.divider()

        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

        c1.markdown("**TOTAL**")
        c2.markdown(f"**$ {total_saldo:,.0f}**".replace(",", "."))
        c3.markdown(f"**$ {total_fci:,.0f}**".replace(",", "."))
        c4.markdown(f"**$ {total_disponible:,.0f}**".replace(",", "."))
        c5.markdown(f"**$ {total_pf:,.0f}**".replace(",", "."))

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
            [1.1, 1.2, 1.2, 1, 1]
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
                [1.1, 1.2, 1.2, 1, 1]
            )

            c[0].write(
                fila["Empresa"]
            )

            c[1].write(
                fila["Banco"]
            )

            c[2].write(
                f"$ {float(fila['Capital']):,.0f}".replace(",", ".")
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
            f"### Total PF: $ {total:,.0f}".replace(",", ".")
        )