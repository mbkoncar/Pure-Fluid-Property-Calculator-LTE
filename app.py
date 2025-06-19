import streamlit as st
import CoolProp.CoolProp as CP
from PIL import Image

# Page config
st.set_page_config(page_title="CoolProp Property Calculator", layout="centered")
st.title("Pure Fluid Property Calculator")

# Header and fluid info link
st.markdown("""
<div style="text-align: center;">
    <br>
    List of all available fluids is available 
    <a href="http://www.coolprop.org/fluid_properties/PurePseudoPure.html" target="_blank">here</a>.
</div>
""", unsafe_allow_html=True)



# Conversion functions
def convert_input(name, value):
    if name == 'T':
        return value + 273.15
    elif name == 'P':
        return value * 1e5
    elif name in ['H', 'S']:
        return value * 1e3
    return value

def convert_output(name, value):
    if name == 'T':
        return value - 273.15
    elif name == 'P':
        return value / 1e5
    elif name in ['H', 'S']:
        return value / 1e3
    return value

# Property label mapping
property_labels = {
    "T": "temperature [°C]",
    "P": "pressure [bar]",
    "H": "enthalpy [kJ/kg]",
    "S": "entropy [kJ/(kg K)]",
    "Q": "vapour mass frac. [-]",
    "D": "density [kg/m3]",
    "V": "viscosity [Pa s]",
    "L": "thermal cond. [W/(m K)]",
    "C": "spec. heat at const. p [J/(kg K)]",
    "CVMASS": "spec. heat at const. V [J/(kg K)]"
}

# Block 1
with st.expander("🔹 Subcooled Liquid / Superheated Vapour"):
    with st.form("block1"):
        fluid = st.text_input("Fluid", "Water")
        col1, col2 = st.columns(2)
        with col1:
            input1 = st.selectbox("Property 1", ["T", "P", "H", "S"], format_func=lambda x: property_labels[x], key="b1_input1")
            value1 = st.number_input(f"Value:", value=100.0, key="b1_value1")
        with col2:
            input2 = st.selectbox("Property 2", ["P", "T", "S", "H"], format_func=lambda x: property_labels[x], key="b1_input2")
            value2 = st.number_input(f"Value:", value=1.0, key="b1_value2")
        output = st.selectbox("Output Property", ["H", "S", "T", "P", "D", "V", "L", "C", "CVMASS"], format_func=lambda x: property_labels[x], key="b1_output")
        submitted1 = st.form_submit_button("Calculate")
        if submitted1:
            try:
                v1 = convert_input(input1, value1)
                v2 = convert_input(input2, value2)
                result = CP.PropsSI(output, input1, v1, input2, v2, fluid)
                result = convert_output(output, result)
                st.success(f"{property_labels[output]} = {result:.5f}")
            except Exception as e:
                st.error(f"Error: {e}")

# Block 2
with st.expander("🔹 Multiphase / Mixture Region"):
    with st.form("block2"):
        fluid = st.text_input("Fluid", "Water", key="b2_fluid")
        col1, col2 = st.columns(2)
        with col1:
            input1 = st.selectbox("Property 1", ["T", "P", "H", "S", "Q"], format_func=lambda x: property_labels[x], key="b2_input1")
            value1 = st.number_input(f"Value:", value=100.0, key="b2_value1")
        with col2:
            input2 = st.selectbox("Property 2", ["P", "T", "S", "H", "Q"], format_func=lambda x: property_labels[x], key="b2_input2")
            value2 = st.number_input(f"Value:", value=1.0, key="b2_value2")
        output = st.selectbox("Output Property", ["H", "S", "T", "P", "Q", "D", "V", "L", "C", "CVMASS"], format_func=lambda x: property_labels[x], key="b2_output")
        submitted2 = st.form_submit_button("Calculate")
        if submitted2:
            try:
                v1 = convert_input(input1, value1)
                v2 = convert_input(input2, value2)
                result = CP.PropsSI(output, input1, v1, input2, v2, fluid)
                result = convert_output(output, result)
                st.success(f"{property_labels[output]} = {result:.5f}")
            except Exception as e:
                st.error(f"Error: {e}")

# Block 3
with st.expander("🔹 Saturation Conditions (Q = 0)"):
    with st.form("block3"):
        fluid = st.text_input("Fluid", "Water", key="b3_fluid")
        input1 = st.selectbox("Known Property", ["P", "T"], format_func=lambda x: property_labels[x], key="b3_input1")
        value1 = st.number_input(f"Value:", value=100.0, key="b3_value1")
        submitted3 = st.form_submit_button("Calculate")
        if submitted3:
            try:
                v1 = convert_input(input1, value1)
                if input1 == "T":
                    result = CP.PropsSI("P", "T", v1, "Q", 0, fluid) / 1e5
                    st.success(f"Saturation Pressure at {value1} °C: {result:.3f} bar")
                else:
                    result = CP.PropsSI("T", "P", v1, "Q", 0, fluid) - 273.15
                    st.success(f"Saturation Temperature at {value1} bar: {result:.3f} °C")
            except Exception as e:
                st.error(f"Error: {e}")

# Block 4
with st.expander("🔹 Critical Temperature and Pressure"):
    with st.form("block4"):
        fluid = st.text_input("Fluid", "Water", key="b4_fluid")
        submitted4 = st.form_submit_button("Get Critical Properties")
        if submitted4:
            try:
                Tcrit = CP.PropsSI('Tcrit', fluid) - 273.15
                Pcrit = CP.PropsSI('Pcrit', fluid) / 1e5

                st.markdown(
                    f"""
                    <div style="background-color:#d4edda; padding:10px; border-radius:5px; border:1px solid #c3e6cb; color:#155724;">
                    <b>Critical Temperature:</b> {Tcrit:.2f} °C<br>
                    <b>Critical Pressure:</b> {Pcrit:.2f} bar
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error: {e}")


# Footer
# Logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.markdown("""
<hr>
<div style="text-align: center;">
    <small>Developed by Mihael Boštjan Končar<br>
    Powered by CoolProp</small>
</div>
""", unsafe_allow_html=True)

