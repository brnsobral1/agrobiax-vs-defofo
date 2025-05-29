import streamlit as st

# Dados dos tubos
agrobiax = {
    100: {"d1": 112.2, "c1": 150},
    150: {"d1": 161.6, "c1": 150},
    200: {"d1": 211.2, "c1": 150},
    250: {"d1": 260.6, "c1": 150},
    300: {"d1": 310.0, "c1": 150},
    350: {"d1": 359.6, "c1": 150},
    400: {"d1": 408.0, "c1": 150}
}

defofo = {
    100: {"d2": 108.4, "c2": 142},
    150: {"d2": 156.4, "c2": 142},
    200: {"d2": 204.2, "c2": 142},
    250: {"d2": 251.0, "c2": 142},
    300: {"d2": 299.8, "c2": 142},
    350: {"d2": 347.6, "c2": 142},
    400: {"d2": 394.6, "c2": 142}
}

# Fórmula para perda de carga HM
def calcular_HM(L, Q, C, D):
    return (10.67 * L * ((Q / 3600) ** 1.852)) / ((C ** 1.852) * ((D / 1000) ** 4.87))

st.title("💧 Comparador de Eficiência: Agrobiax x Defofo")

# Inicializar os valores padrões usando st.session_state
if "reset" not in st.session_state:
    st.session_state.reset = False

if st.button("🔄 Limpar"):
    st.session_state.reset = True
    st.experimental_rerun()

L = st.number_input("📏 Comprimento da tubulação (m):", min_value=0.0, value=0.0 if st.session_state.reset else 100.0, key="L")
Q = st.number_input("💦 Vazão (m³/h):", min_value=0.0, value=0.0 if st.session_state.reset else 30.0, key="Q")
h = st.number_input("📉 Desnível (m):", min_value=0.0, value=0.0 if st.session_state.reset else 5.0, key="h")
PS = st.number_input("⚙️ Pressão de serviço (m.c.a.):", min_value=0.0, value=0.0 if st.session_state.reset else 10.0, key="PS")
DN = st.selectbox("📐 Diâmetro Nominal (DN):", options=sorted(agrobiax.keys()), index=0, key="DN")

# Reset completo
st.session_state.reset = False

if st.button("📊 Calcular Eficiência"):
    try:
        d1, c1 = agrobiax[DN]["d1"], agrobiax[DN]["c1"]
        d2, c2 = defofo[DN]["d2"], defofo[DN]["c2"]

        HM1 = calcular_HM(L, Q, c1, d1)
        HM2 = calcular_HM(L, Q, c2, d2)

        P1 = (HM1 + h + PS) * 1.05
        P2 = (HM2 + h + PS) * 1.05

        eficiencia = 100 - ((P1 / P2) * 100)

        st.success(f"✅ Eficiência energética do Agrobiax em relação ao Defofo: **{eficiencia:.2f}%**")
        with st.expander("🔍 Detalhes do cálculo"):
            st.write(f"HM Agrobiax: {HM1:.2f} m.c.a.")
            st.write(f"HM Defofo: {HM2:.2f} m.c.a.")
            st.write(f"P1 (Agrobiax): {P1:.2f} m.c.a.")
            st.write(f"P2 (Defofo): {P2:.2f} m.c.a.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
  
