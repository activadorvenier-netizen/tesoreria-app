import streamlit as st
import pandas as pd

def mostrar_tarjeta_bancos(empresa, bancos_empresa):
    """Muestra la tarjeta de bancos en la página de Bancos"""
    
    st.subheader("🏦 Bancos")

    with st.container(border=True):

        # ✅ 5 columnas: Banco | Saldo | FCI | Total Disponible | Plazo Fijo
        h1, h2, h3, h4, h5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

        h1.markdown("**Banco**")
        h2.markdown("**Saldo**")
        h3.markdown("**FCI**")
        h4.markdown("**Total Disponible**")
        h5.markdown("**Plazo Fijo**")

        st.divider()

        # ✅ Lista de bancos con los nombres EXACTOS de las claves
        bancos = [
            {
                "nombre": "Galicia",
                "saldo": bancos_empresa.get("GaliciaSaldo", 0),
                "fci": bancos_empresa.get("GaliciaFCI", 0),
                "pf": bancos_empresa.get("pf_galicia", 0)
            },
            {
                "nombre": "Macro",
                "saldo": bancos_empresa.get("MacroSaldo", 0),
                "fci": bancos_empresa.get("MacroFCI", 0),
                "pf": bancos_empresa.get("pf_macro", 0)
            },
            {
                "nombre": "Credicoop",
                "saldo": bancos_empresa.get("CredicoopSaldo", 0),
                "fci": bancos_empresa.get("CredicoopFCI", 0),
                "pf": bancos_empresa.get("pf_credicoop", 0)
            },
            {
                "nombre": "Santander",
                "saldo": bancos_empresa.get("SantanderSaldo", 0),
                "fci": bancos_empresa.get("SantanderFCI", 0),
                "pf": bancos_empresa.get("pf_santander", 0)
            },
        ]

        # ✅ Inicializar totales
        total_saldo = 0
        total_fci = 0
        total_disponible = 0
        total_pf = 0

        # ✅ Mostrar cada banco
        for banco in bancos:
            disponible = banco["saldo"] + banco["fci"]
            
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

            c1.write(f"🏦 {banco['nombre']}")
            c2.write(f"$ {banco['saldo']:,.0f}".replace(",", "."))
            c3.write(f"$ {banco['fci']:,.0f}".replace(",", "."))
            c4.markdown(f"**$ {disponible:,.0f}**".replace(",", "."))
            c5.write(f"$ {banco['pf']:,.0f}".replace(",", "."))
            
            total_saldo += banco["saldo"]
            total_fci += banco["fci"]
            total_disponible += disponible
            total_pf += banco["pf"]

        # ✅ Buscar OTROS bancos (Provincia, BBVA, ICBC, etc.)
        otros_bancos = []
        for key in bancos_empresa.keys():
            # Si la clave termina en "Saldo" y no es de los bancos principales
            if key.endswith("Saldo") and key not in ["GaliciaSaldo", "MacroSaldo", "CredicoopSaldo", "SantanderSaldo"]:
                nombre = key.replace("Saldo", "")
                fci_key = f"{nombre}FCI"
                pf_key = f"pf_{nombre.lower()}"
                
                saldo = bancos_empresa.get(key, 0)
                fci = bancos_empresa.get(fci_key, 0)
                pf = bancos_empresa.get(pf_key, 0)
                
                # Solo mostrar si tiene algún valor > 0
                if saldo > 0 or fci > 0 or pf > 0:
                    otros_bancos.append({
                        "nombre": nombre,
                        "saldo": saldo,
                        "fci": fci,
                        "pf": pf
                    })
                    total_saldo += saldo
                    total_fci += fci
                    total_disponible += saldo + fci
                    total_pf += pf

        # ✅ Mostrar otros bancos
        if otros_bancos:
            for otro in otros_bancos:
                disponible = otro["saldo"] + otro["fci"]
                c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])
                c1.write(f"🏦 {otro['nombre']}")
                c2.write(f"$ {otro['saldo']:,.0f}".replace(",", "."))
                c3.write(f"$ {otro['fci']:,.0f}".replace(",", "."))
                c4.markdown(f"**$ {disponible:,.0f}**".replace(",", "."))
                c5.write(f"$ {otro['pf']:,.0f}".replace(",", "."))

        # ✅ Totales
        st.divider()
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])
        c1.markdown("**TOTAL**")
        c2.markdown(f"**$ {total_saldo:,.0f}**".replace(",", "."))
        c3.markdown(f"**$ {total_fci:,.0f}**".replace(",", "."))
        c4.markdown(f"**$ {total_disponible:,.0f}**".replace(",", "."))
        c5.markdown(f"**$ {total_pf:,.0f}**".replace(",", "."))