import streamlit as st
import numpy as np
from scipy.constants import R, g
from STHE import *

np.seterr(divide='ignore', invalid='ignore')


def main():
    # st.title("STHE Classes")
    st.subheader("Operation : Cooling of hot organic solvent using water")
    st.write(r"All temperatures in $^o$C")
    x1, x2 = st.beta_columns(2)
    a1, a2 = st.beta_columns(2)
    b1, b2 = st.beta_columns(2)
    c1, c2 = st.beta_columns(2)
    x1.write("Hot ethylbenzene")
    x2.write("Cold water")
    T_s_in = a1.number_input("Hot fluid inlet temperature", format="%.2f", value=135.00)
    T_t_in = a2.number_input("Cold fluid inlet temperature", format="%.2f", value=30.00)
    T_s_out = b1.number_input("Hot fluid outlet temperature", format="%.2f", value=40.00)
    T_t_out = b2.number_input("Cold fluid outlet temperature", format="%.2f", value=45.00)
    m_s = c1.number_input("Hot fluid flow rate in kg/s", format="%.3f", value=0.579)
    sthe = STHE()
    sthe.T_s_in = T_s_in
    sthe.T_t_in = T_t_in
    sthe.T_s_out = T_s_out
    sthe.T_t_out = T_t_out
    sthe.m_s = m_s
    sthe.Costing()
    sthe.Optimize()
    sol = sthe.solution
    sol_array = sol.to_numpy()[0]

    def getLayout_str(num):
        if num == 90:
            name = "Square"
        elif num == 45:
            name = "Rotated square"
        else:
            name = "Triangular"
        return name

    new = STHE()
    new.tube_layout = sol_array[0]
    new.NP = sol_array[1]
    new.L = sol_array[2]
    new.do = sol_array[3]
    new.C_sb = sol_array[4]
    new.C_tb = sol_array[5]
    new.baffle_cut = sol_array[6]
    new.Costing()
    c2.write("Cold fluid flow rate in kg/s")
    c2.write("%0.3f kg/h" % (sthe.m_t))
    st.success("Optimized design parameters")
    col1, col2 = st.beta_columns(2)
    col1.info("Tube side")
    col2.error("Shell side")
    col1.write(r"Tube layout = %s %d$^o$" % (getLayout_str(sol_array[0]), sol_array[0]))
    col1.write(r"Number of tube passes = %d" % sol["NP"])
    col1.write(r"Tube length = %.1f m" % sol["L"])
    col1.write(r"Outer diameter of tube = %.2f mm" % (sol["do"] * 1e3))
    col1.write(r"$\Delta P$ on shell side = %.1f Pa" % sol["dPs"])
    col1.write(r"Tube and baffle spacing = %.2f mm" % (sol["C_tb"] * 1e3))
    col1.write(r"Number of tubes = %.0f" % new.Nt)
    col2.write(r"Diameter of shell = %.2f mm" % (new.Ds * 1e3))
    col2.write(r"Shell and baffle spacing = %.2f mm" % (sol["C_sb"] * 1e3))
    col2.write(r"Baffle spacing = %.2f mm" % (new.baffle_spacing * 1e3))
    col2.write(r"Baffle cut = %.0f%%" % (sol["baffle_cut"] * 100))
    col2.write(r"$\Delta P$ on tube side = %.1f Pa" % sol["dPt"])
    st.success(r"Total cost = $%.2f/year" % sol["total_cost"])
    st.write(r"Calculated overall heat transfer coefficient = %.1f W/(m$^2$K)" % sol["Ucalculated"])
    st.write(r"Area required = %.2f m$^2$" % sol["A_calc"])
    st.write(r"Area available = %.2f m$^2$" % sol["A"])


