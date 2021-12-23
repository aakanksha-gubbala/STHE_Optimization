import streamlit as st


def main():
    st.title("STHE Classes")
    st.subheader("Problem Solving Approach")
    st.image('diagram.png')
    st.write("Objective : Minimize total cost of STHE")
    st.write("Constraints : ")
    st.write(r"1. $\Delta P_s < \Delta P_{s, permissible}$")
    st.write(r"2. $\Delta P_t < \Delta P_{t, permissible}$")
    st.write(r"3. $A_{calculated} < A_{available}$")
    st.write("Subject to variables : ")
    st.write(r"1. Tube layout = [Triangular 30 deg, Rotated square 45 deg, Square 90 deg]")
    st.write(r"2. Number of tube passes = [1, 2, 4]")
    st.write(r"3. Baffle cut = 15% to 25%")
    st.write(r"4. Length of tube = 2.5 to 6 m")
    st.write(r"5. Outer diameter of tube = 0.75 in, 1 in, 1.25 in, 1.5 in, 2 in")
    st.write(r"6. Shell-baffle clearance = 5 to 25 mm")
    st.write(r"7. Tube-baffle clearance = 5 to 25 mm")
    st.write("Assumptions")
    st.write(r"1. Tube Thickness is 16 BWG")
    st.write(r"2. Baffle spacing = 0.5D$_s$")
    st.write(r"3. Constant specific heat capacity in the temperature range")
    st.write("References")
    st.write("1) Fettaka, S., Thibault, J., & Gupta, Y. (2013). "
             "Design of shell-and-tube heat exchangers using multiobjective optimization."
             " International Journal of Heat and Mass Transfer, 60, 343–354.")
    st.write("2) Hewitt, Geoffrey F., Theodore R. Bott, and G. L. Shires (1994) Process Heat Transfer. CRC Press.")
