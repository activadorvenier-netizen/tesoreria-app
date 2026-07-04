import streamlit as st
import pandas as pd

def formato_moneda(valor):
    return f"$ {float(valor):,.0f}".replace(",", ".")

def mostrar_tarjeta_bancos(empresa, bancos_empresa):
    """
    Muestra la tarjeta de bancos con: Banco, Cuenta, FCI, Disponible (coloreado) y Plazos Fijos
    """
    st.markdown("### 🏦 Bancos")
    
    # Crear DataFrame con los datos
    datos_bancos = []
    
    # Galicia
    datos_bancos.append({
        "Banco": "Galicia",
        "Cuenta": bancos_empresa.get("galicia", 0) - bancos_empresa.get("pf_galicia", 0),
        "FCI": bancos_empresa.get("pf_galicia", 0),
        "Disponible": bancos_empresa.get("galicia", 0),
        "Plazos Fijos": bancos_empresa.get("pf_galicia", 0)
    })
    
    # Macro
    datos_bancos.append({
        "Banco": "Macro",
        "Cuenta": bancos_empresa.get("macro", 0) - bancos_empresa.get("pf_macro", 0),
        "FCI": bancos_empresa.get("pf_macro", 0),
        "Disponible": bancos_empresa.get("macro", 0),
        "Plazos Fijos": bancos_empresa.get("pf_macro", 0)
    })
    
    # Credicoop
    datos_bancos.append({
        "Banco": "Credicoop",
        "Cuenta": bancos_empresa.get("credicoop", 0) - bancos_empresa.get("pf_credicoop", 0),
        "FCI": bancos_empresa.get("pf_credicoop", 0),
        "Disponible": bancos_empresa.get("credicoop", 0),
        "Plazos Fijos": bancos_empresa.get("pf_credicoop", 0)
    })
    
    # Santander
    datos_bancos.append({
        "Banco": "Santander",
        "Cuenta": bancos_empresa.get("santander", 0) - bancos_empresa.get("pf_santander", 0),
        "FCI": bancos_empresa.get("pf_santander", 0),
        "Disponible": bancos_empresa.get("santander", 0),
        "Plazos Fijos": bancos_empresa.get("pf_santander", 0)
    })
    
    # Mostrar tabla con estilo mejorado
    st.markdown("""
    <style>
        .banco-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .banco-table th {
            background-color: #f0f2f6;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #d0d0d0;
        }
        .banco-table td {
            padding: 8px 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        .banco-table tr:hover {
            background-color: #f8f9fa;
        }
        .disponible-positivo {
            color: #2e7d32;
            font-weight: 600;
        }
        .disponible-negativo {
            color: #d32f2f;
            font-weight: 600;
        }
        .banco-table .total-row {
            background-color: #e8f5e9;
            font-weight: 600;
        }
        .banco-table .total-row td {
            border-top: 2px solid #2e7d32;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Construir tabla HTML
    html = """
    <table class="banco-table">
        <thead>
            <tr>
                <th>Banco</th>
                <th>Cuenta</th>
                <th>FCI</th>
                <th>Disponible</th>
                <th>Plazos Fijos</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for banco in datos_bancos:
        disponible = banco["Disponible"]
        clase_disponible = "disponible-positivo" if disponible >= 0 else "disponible-negativo"
        
        html += f"""
            <tr>
                <td><strong>{banco['Banco']}</strong></td>
                <td>{formato_moneda(banco['Cuenta'])}</td>
                <td>{formato_moneda(banco['FCI'])}</td>
                <td class="{clase_disponible}">{formato_moneda(disponible)}</td>
                <td>{formato_moneda(banco['Plazos Fijos'])}</td>
            </tr>
        """
    
    # Total general
    total_cuenta = sum(b["Cuenta"] for b in datos_bancos)
    total_fci = sum(b["FCI"] for b in datos_bancos)
    total_disponible = sum(b["Disponible"] for b in datos_bancos)
    total_pf = sum(b["Plazos Fijos"] for b in datos_bancos)
    
    html += f"""
        <tr class="total-row">
            <td><strong>TOTAL</strong></td>
            <td>{formato_moneda(total_cuenta)}</td>
            <td>{formato_moneda(total_fci)}</td>
            <td>{formato_moneda(total_disponible)}</td>
            <td>{formato_moneda(total_pf)}</td>
        </tr>
    </tbody>
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def mostrar_tarjeta_pf(detalle_pf):
    """
    Muestra la tarjeta de Plazos Fijos
    """
    if detalle_pf.empty:
        st.info("📭 No hay plazos fijos registrados")
        return
    
    st.markdown("### 📈 Plazos Fijos")
    
    # Crear tabla de plazos fijos
    st.dataframe(
        detalle_pf[["Banco", "Capital", "Tasa", "Vencimiento"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Banco": "Banco",
            "Capital": st.column_config.NumberColumn("Capital", format="$ %.0f"),
            "Tasa": "Tasa (%)",
            "Vencimiento": "Vencimiento"
        }
    )

    st.divider()