import streamlit as st
import numpy as np
from scipy.constants import R, g
from STHE import *

np.seterr(divide='ignore', invalid='ignore')


def main():
    # st.title("STHE Classes")
    st.write(r"All temperatures in $^o$C")
    x1, x2 = st.beta_columns(2)
    a1, a2 = st.beta_columns(2)
    b1, b2 = st.beta_columns(2)
    c1, c2 = st.beta_columns(2)
    d1, d2 = st.beta_columns(2)
    e1, e2 = st.beta_columns(2)
    f1, f2 = st.beta_columns(2)
    g1, g2 = st.beta_columns(2)
    h1, h2 = st.beta_columns(2)
    i1, i2 = st.beta_columns(2)
    x1.write("Shell side")
    x2.write("Tube side")
    T_s_in = a1.number_input("Shell-side fluid inlet temperature", format="%.2f", value=125.00)
    T_t_in = a2.number_input("Tube-side fluid inlet temperature", format="%.2f", value=30.00)
    T_s_out = b1.number_input("Shell-side fluid outlet temperature", format="%.2f", value=40.00)
    T_t_out = b2.number_input("Tube-side fluid outlet temperature", format="%.2f", value=42.00)
    rho_s = f1.number_input("Shell-side fluid density (kg/m^3)", format="%.1f", value=840.0)
    rho_t = f2.number_input("Tube-side fluid density (kg/m^3)", format="%.1f", value=993.0)
    Cp_s = d1.number_input("Shell-side specific heat capacity (kJ/kg/K)", format="%.3f", value=2.093)
    Cp_t = d2.number_input("Tube-side specific heat capacity (kJ/kg/K)", format="%.3f", value=4.175)
    mu_s = e1.number_input("Shell-side viscosity (cP)", format="%.3f", value=0.340)
    mu_t = e2.number_input("Tube-side viscosity (cP)", format="%.3f", value=0.800)
    k_s = g1.number_input("Shell-side thermal conductivity (W/m^2/K)", format="%.3f", value=0.115)
    k_t = g2.number_input("Tube-side thermal conductivity (W/m^2/K)", format="%.3f", value=0.623)
    Rs = h1.number_input("Shell-side fouling resistance (m^2/K/W)", format="%.2e", value=1.81e-4)
    Rt = h2.number_input("Tube-side fouling resistance (m^2/K/W)", format="%.2e", value=3.01e-4)
    U = i1.number_input("Assumed overall heat transfer coefficient (U) (W/m^2/K)", format="%.2f", value=407.00)
    m_s = c1.number_input("Shell-side fluid flow rate in kg/s", format="%.3f", value=0.579)
    sthe = STHE()
    sthe.T_s_in = T_s_in
    sthe.T_t_in = T_t_in
    sthe.T_s_out = T_s_out
    sthe.T_t_out = T_t_out
    sthe.Cp_s = Cp_s * 1e3
    sthe.Cp_t = Cp_t * 1e3
    sthe.rho_s = rho_s
    sthe.rho_t = rho_t
    sthe.mu_s = mu_s * 1e-3
    sthe.mu_t = mu_t * 1e-3
    sthe.k_s = k_s
    sthe.k_t = k_t
    sthe.Rs = Rs
    sthe.Rt = Rt
    sthe.U = U
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

    sthe.tube_layout = sol_array[0]
    sthe.NP = sol_array[1]
    sthe.L = sol_array[2]
    sthe.do = sol_array[3]
    sthe.C_sb = sol_array[4]
    sthe.C_tb = sol_array[5]
    sthe.baffle_cut = sol_array[6]
    sthe.Costing()
    c2.write("Tube-side fluid flow rate")
    c2.write("%0.3f kg/s" % (sthe.m_t))
    st.success("Optimized variables")
    col1, col2 = st.beta_columns(2)
    col2.info("Tube side")
    col1.error("Shell side")
    col2.write(r"Tube layout = %s %d$^o$" % (getLayout_str(sol_array[0]), sol_array[0]))
    col2.write(r"Number of tube passes = %d" % sol["NP"])
    col2.write(r"Tube length = %.1f m" % sol["L"])
    col2.write(r"Outer diameter of tube = %.2f mm" % (sol["do"] * 1e3))
    col2.write(r"$\Delta P$ on shell side = %.1f Pa" % sol["dPs"])
    col2.write(r"Tube-side h = %.2f W/(m$^2$K)" % sthe.hi)
    col2.write(r"Tube and baffle spacing = %.2f mm" % (sol["C_tb"] * 1e3))
    col2.write(r"Number of tubes = %.0f" % sthe.Nt)
    col1.write(r"Diameter of shell = %.2f mm" % (sthe.Ds * 1e3))
    col1.write(r"Shell and baffle spacing = %.2f mm" % (sol["C_sb"] * 1e3))
    col1.write(r"Baffle spacing = %.2f mm" % (sthe.baffle_spacing * 1e3))
    col1.write(r"Baffle cut = %.0f%%" % (sol["baffle_cut"] * 100))
    col1.write(r"$\Delta P$ on tube side = %.1f Pa" % sol["dPt"])
    col1.write(r"Shell-side h = %.2f W/(m$^2$K)" % sthe.ho)
    st.success(r"Total cost = $%.2f/year" % sol["total_cost"])
    i2.write(r"Calculated overall heat transfer coefficient")
    i2.write(r"%.1f W/(m$^2$K)" % sol["Ucalculated"])
    st.write(r"Area required = %.2f m$^2$" % sol["A_calc"])
    st.write(r"Area available = %.2f m$^2$" % sol["A"])
