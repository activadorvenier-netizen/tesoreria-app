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
        
        # ✅ Almacenar totales
        total_saldo = 0
        total_fci = 0
        total_disponible = 0
        total_pf = 0
        
        # ✅ Mostrar bancos definidos
        for banco in bancos_definidos:
            # Obtener saldo y FCI del banco (usando los nombres exactos de columnas)
            saldo_key = f"{banco}Saldo"
            fci_key = f"{banco}FCI"
            pf_key = f"pf_{banco.lower()}"
            
            saldo = bancos_empresa.get(saldo_key, 0)
            fci = bancos_empresa.get(fci_key, 0)
            pf = bancos_empresa.get(pf_key, 0)
            disponible = saldo + fci
            
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

            c1.write(f"🏦 {banco}")
            c2.write(f"$ {saldo:,.0f}".replace(",", "."))
            c3.write(f"$ {fci:,.0f}".replace(",", "."))
            c4.markdown(f"**$ {disponible:,.0f}**".replace(",", "."))
            c5.write(f"$ {pf:,.0f}".replace(",", "."))
            
            total_saldo += saldo
            total_fci += fci
            total_disponible += disponible
            total_pf += pf

        # ✅ Procesar otros bancos (Provincia, BBVA, ICBC, etc.)
        # Buscar en bancos_empresa las claves que terminen en "Saldo"
        otros_bancos = []
        for key in bancos_empresa.keys():
            # Si la clave termina en "Saldo" y no es de los bancos definidos
            if key.endswith("Saldo") and not any(banco in key for banco in bancos_definidos):
                nombre_banco = key.replace("Saldo", "")
                saldo = bancos_empresa.get(key, 0)
                fci_key = f"{nombre_banco}FCI"
                fci = bancos_empresa.get(fci_key, 0)
                pf_key = f"pf_{nombre_banco.lower()}"
                pf = bancos_empresa.get(pf_key, 0)
                disponible = saldo + fci
                
                if saldo > 0 or fci > 0 or pf > 0:
                    otros_bancos.append({
                        "nombre": nombre_banco,
                        "saldo": saldo,
                        "fci": fci,
                        "disponible": disponible,
                        "pf": pf
                    })
                    total_saldo += saldo
                    total_fci += fci
                    total_disponible += disponible
                    total_pf += pf

        # ✅ Mostrar "Otros Bancos" si hay
        if otros_bancos:
            for otro in otros_bancos:
                c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

                c1.write(f"🏦 {otro['nombre']}")
                c2.write(f"$ {otro['saldo']:,.0f}".replace(",", "."))
                c3.write(f"$ {otro['fci']:,.0f}".replace(",", "."))
                c4.markdown(f"**$ {otro['disponible']:,.0f}**".replace(",", "."))
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