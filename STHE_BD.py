# import streamlit as st
import numpy as np
import scipy.optimize
from scipy.constants import R, g

# np.seterr(divide='ignore', invalid='ignore')


# def main():
#     # st.title("STHE Classes")
#     st.subheader("Operation : cool hot organic using water")
#     st.write(r"All temperatures in $^o$C")
#     x1, x2 = st.beta_columns(2)
#     a1, a2 = st.beta_columns(2)
#     b1, b2 = st.beta_columns(2)
#     c1, c2 = st.beta_columns(2)
#     x1.write("Hot fluid on shell side")
#     x2.write("Cold fluid on tube side")
#     T_h_in = a1.number_input("Hot fluid inlet temperature", format="%.2f")
#     T_c_in = a2.number_input("Cold fluid inlet temperature", format="%.2f")
#     T_h_out = b1.number_input("Hot fluid outlet temperature", format="%.2f")
#     T_c_out = b2.number_input("Cold fluid outlet temperature", format="%.2f")
#     m_h = c1.number_input("Hot fluid flow rate in kg/h", format="%.3f")
#     Cp_h = 2.093
#     Cp_c = 4.175
#     rho__h = 840
#     rho__c = 993
#     mu_h = 0.34e-3
#     mu_c = 0.8e-3
#     U = 407
#     m_c = m_h * Cp_h * (T_h_in - T_h_out) / (Cp_c * (T_c_out - T_c_in)) / 3600
#     c2.write("Cold fluid flow rate in kg/h")
#     c2.write("%0.3f kg/h" % (m_c * 3600))
#
#     Q = m_h * Cp_h * 1e3 * (T_h_in - T_h_out) / 3600
#     lmtd = ((T_h_in - T_c_out) - (T_h_out - T_c_in)) / np.log((T_h_in - T_c_out) / (T_h_out - T_c_in))
#     U = 407
#     A_assumed = Q / (U * lmtd)
#     di = 15.7
#     do = 19
#     L = 3
#     Nt = np.ceil(A_assumed / (np.pi * do * 1e-3 * L))
#     At = Nt * np.pi * 0.25 * (di * 1e-3) ** 2
#     vt = (m_c / rho__c) / At
#     Re = di * 1e-3 * vt * rho__c / mu_c
#     f = 0.079 * Re ** (-0.25)
#     dP = 2 * f * vt ** 2 * L * rho__c / (do * 1e-3 * g)
# h = hot, c = cold
# Temp in C, flow-rates in kg/h, Cp in kJ/kg.degC
