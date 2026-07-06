import streamlit as st
import pandas as pd

def mostrar_tarjeta_bancos(empresa, bancos_empresa):
    """Muestra la tarjeta de bancos con Saldo, FCI, Total Disponible y Plazo Fijo"""
    
    st.subheader("🏦 Bancos")

    with st.container(border=True):

        # ✅ Estilos para la tabla
        st.markdown("""
        <style>
            .total-disponible {
                background-color: #e3f2fd !important;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: 600;
            }
            .total-row {
                background-color: #f5f5f5 !important;
                font-weight: 600;
            }
            .otros-bancos {
                background-color: #fff3e0 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # ✅ 5 columnas: Banco | Saldo | FCI | Total Disponible | Plazo Fijo
        h1, h2, h3, h4, h5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])

        h1.markdown("**Banco**")
        h2.markdown("**Saldo**")
        h3.markdown("**FCI**")
        h4.markdown("**Total Disponible**")
        h5.markdown("**Plazo Fijo**")

        st.divider()

        # ✅ Inicializar totales
        total_saldo = 0
        total_fci = 0
        total_disponible = 0
        total_pf = 0

        # ✅ Mostrar bancos principales
        bancos = [
            {"nombre": "Galicia", "saldo": "GaliciaSaldo", "fci": "GaliciaFCI", "pf": "pf_galicia"},
            {"nombre": "Macro", "saldo": "MacroSaldo", "fci": "MacroFCI", "pf": "pf_macro"},
            {"nombre": "Credicoop", "saldo": "CredicoopSaldo", "fci": "CredicoopFCI", "pf": "pf_credicoop"},
            {"nombre": "Santander", "saldo": "SantanderSaldo", "fci": "SantanderFCI", "pf": "pf_santander"},
        ]

        for banco in bancos:
            saldo = bancos_empresa.get(banco["saldo"], 0)
            fci = bancos_empresa.get(banco["fci"], 0)
            pf = bancos_empresa.get(banco["pf"], 0)
            disponible = saldo + fci
            
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])
            c1.write(f"🏦 {banco['nombre']}")
            c2.write(f"$ {saldo:,.0f}".replace(",", "."))
            c3.write(f"$ {fci:,.0f}".replace(",", "."))
            c4.markdown(
                f"<div class='total-disponible'>$ {disponible:,.0f}</div>".replace(",", "."),
                unsafe_allow_html=True
            )
            c5.write(f"$ {pf:,.0f}".replace(",", "."))
            
            total_saldo += saldo
            total_fci += fci
            total_disponible += disponible
            total_pf += pf

        # ✅ Mostrar "OTROS BANCOS" si existen
        otros_bancos = bancos_empresa.get("otros_bancos", {})
        pf_otros = bancos_empresa.get("pf_otros", {})
        
        if otros_bancos:
            # Línea separadora
            st.divider()
            
            # Título "Otros Bancos"
            st.markdown("**🏦 Otros Bancos**")
            
            for nombre, datos in otros_bancos.items():
                saldo = datos.get("saldo", 0)
                fci = datos.get("fci", 0)
                pf = pf_otros.get(nombre, 0)
                disponible = saldo + fci
                
                c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])
                c1.write(f"🏦 {nombre}")
                c2.write(f"$ {saldo:,.0f}".replace(",", "."))
                c3.write(f"$ {fci:,.0f}".replace(",", "."))
                c4.markdown(
                    f"<div class='total-disponible'>$ {disponible:,.0f}</div>".replace(",", "."),
                    unsafe_allow_html=True
                )
                c5.write(f"$ {pf:,.0f}".replace(",", "."))
                
                total_saldo += saldo
                total_fci += fci
                total_disponible += disponible
                total_pf += pf

        # ✅ Totales
        st.divider()
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2])
        c1.markdown("**TOTAL**")
        c2.markdown(f"**$ {total_saldo:,.0f}**".replace(",", "."))
        c3.markdown(f"**$ {total_fci:,.0f}**".replace(",", "."))
        c4.markdown(
            f"<div class='total-disponible'>$ {total_disponible:,.0f}</div>".replace(",", "."),
            unsafe_allow_html=True
        )
        c5.markdown(f"**$ {total_pf:,.0f}**".replace(",", "."))


def mostrar_tarjeta_pf(detalle_pf):
    """Muestra la tarjeta de Plazos Fijos"""

    st.subheader("📈 Plazos Fijos")

    with st.container(border=True):

        if detalle_pf.empty:
            st.info("No existen Plazos Fijos.")
            return

        cab = st.columns([1.1, 1.2, 1.2, 1, 1])
        cab[0].markdown("**Empresa**")
        cab[1].markdown("**Banco**")
        cab[2].markdown("**Capital**")
        cab[3].markdown("**Tasa**")
        cab[4].markdown("**Vencimiento**")

        st.divider()

        total = 0

        for _, fila in detalle_pf.iterrows():
            total += float(fila["Capital"])
            c = st.columns([1.1, 1.2, 1.2, 1, 1])
            c[0].write(fila["Empresa"])
            c[1].write(fila["Banco"])
            c[2].write(f"$ {float(fila['Capital']):,.0f}".replace(",", "."))
            c[3].write(f"{float(fila['Tasa'])}%")
            c[4].write(pd.to_datetime(fila["Vencimiento"]).strftime("%d/%m/%Y"))

        st.divider()
        st.markdown(f"### Total PF: $ {total:,.0f}".replace(",", "."))