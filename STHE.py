import numpy as np
from scipy.constants import R, g
import pandas as pd
from optimization import *


def getReClasses(Re):
    i = 0
    if Re >= 1e4 and Re <= 1e5:
        i = 1
    elif Re >= 1e3 and Re <= 1e4:
        i = 2
    elif Re >= 1e2 and Re < 1e3:
        i = 3
    elif Re > 1e1 and Re < 1e2:
        i = 4
    elif Re < 1e1:
        i = 5
    else:
        i = 1
    return i


def getColburnCoeffs(i, tube_layout):
    if tube_layout == 30:
        switcher = {
            1: [0.321, -0.388, 1.450, 0.519, 0.372, -0.123, 7.00, 0.500],
            2: [0.321, -0.388, 0, 0, 0.486, 0.152, 0, 0],
            3: [0.593, -0.477, 0, 0, 4.570, -0.476, 0, 0],
            4: [1.360, -0.657, 0, 0, 45.100, -0.973, 0, 0],
            5: [1.400, -0.667, 0, 0, 48.000, -1.00, 0, 0]
        }
    elif tube_layout == 45:
        switcher = {
            1: [0.370, -0.396, 1.930, 0.500, 0.303, -0.126, 6.59, 0.520],
            2: [0.370, -0.396, 0, 0, 0.333, -0.136, 0, 0],
            3: [0.730, -0.500, 0, 0, 3.500, 0.476, 0, 0],
            4: [0.498, -0.656, 0, 0, 26.200, -0.913, 0, 0],
            5: [1.550, -0.667, 0, 0, 32.000, -1.00, 0, 0]
        }
    elif tube_layout == 90:
        switcher = {
            1: [0.370, -0.395, 1.187, 0.370, 0.319, -0.148, 6.3, 0.378],
            2: [0.107, -0.266, 0, 0, 0.0815, 0.022, 0, 0],
            3: [0.408, -0.460, 0, 0, 6.090, -0.602, 0, 0],
            4: [0.900, -0.631, 0, 0, 32.100, -0.963, 0, 0],
            5: [0.970, -0.667, 0, 0, 35.000, -1.00, 0, 0]
        }
    return switcher.get(i, [0.321, -0.388, 1.450, 0.519, 0.372, -0.123, 7.00, 0.500])


def getBWG(i):
    switcher = {
        7: 4.572,
        8: 4.191,
        9: 3.759,
        10: 3.404,
        11: 3.048,
        12: 2.769,
        13: 2.413,
        14: 2.108,
        15: 1.829,
        16: 1.651
    }
    return switcher.get(i, 3)


def F_EvenTube(NP, R, S):
    F_even = np.sqrt((R ** 2 + 1) * np.log((1 - S) / (1 - R * S))) / (
            (R - 1) * np.log((2 - S * (R + 1 - np.sqrt(R ** 2 + 1))) / (2 - S * (R + 1 + np.sqrt(R ** 2 + 1)))))
    switcher = {
        1: 1,
        2: F_even,
        4: F_even
    }
    return switcher.get(NP, 1)


def get_Dbt_params(NP, tube_layout):
    if tube_layout == 30:
        switcher = {
            1: [0.319, 2.142],
            2: [0.249, 2.207],
            4: [0.175, 2.285]
        }
    else:
        switcher = {
            1: [0.215, 2.207],
            2: [0.156, 2.291],
            4: [0.158, 2.263]
        }
    return switcher.get(NP, [1, 1])


def getA_cr(self):
    if self.tube_layout == 30:
        A_cr = self.baffle_spacing * (self.Ds - self.Dbt + ((self.Dbt - self.do) / self.pt) * (self.pt - self.do))
    elif self.tube_layout == 45:
        A_cr = self.baffle_spacing * (
                self.Ds - self.Dbt + ((self.Dbt - self.do) / (0.707 * self.pt)) * (self.pt - self.do))
    elif self.tube_layout == 90:
        A_cr = self.baffle_spacing * (self.Ds - self.Dbt + ((self.Dbt - self.do) / self.pt) * (self.pt - self.do))
    return A_cr


class STHE:
    def __init__(self):
        # All temperatures in deg C
        # All units of length is m
        # All units of power and energy are SI units
        # Units of Cp is kJ/kg/K
        # Units of density (rho) is kg/m^3
        # Units of viscosity (mu) = Pa.s
        # Thermal conductivity, U, h have SI units
        # Pressure is in Pa
        self.T_s_in = 135
        self.T_t_in = 30
        self.T_s_out = 40
        self.T_t_out = 40
        self.Cp_s = 2.093 * 1e3
        self.Cp_t = 4.175 * 1e3
        self.rho_s = 840
        self.rho_t = 993
        self.mu_s = 0.34e-3
        self.mu_t = 0.8e-3
        self.k_s = 0.115
        self.k_t = 0.623
        self.m_s = 50e3 / 24 / 3600
        self.U = 407
        self.NP = 4
        self.tube_layout = 30
        self.do = 0.75 * 0.0254
        self.di = self.do - 2 * getBWG(16) * 1e-3
        self.L = 5
        self.baffle_cut = 15e-2
        self.baffle_spacing_factor = 0.5
        self.C_sb = 20e-3
        self.C_tb = 10e-3
        self.dPt_perm = 15e3
        self.dPs_perm = 15e3
        self.Rs = 1.81e-4
        self.Rt = 3.01e-4

    def Initialize(self):
        # Energy balances to find mass flow rate of cold stream
        self.Q = self.m_s * self.Cp_s * (self.T_s_in - self.T_s_out)
        self.m_t = self.m_s * self.Cp_s * (self.T_s_in - self.T_s_out) / (
                self.Cp_t * (self.T_t_out - self.T_t_in))
        self.lmtd = ((self.T_s_in - self.T_t_out) - (self.T_s_out - self.T_t_in)) / np.log(
            (self.T_s_in - self.T_t_out) / (self.T_s_out - self.T_t_in))
        self.A_assumed = self.Q / (self.U * self.lmtd)

        # Mechanical design = number of tubes, shell diameter, tube bundle diameter, baffle spacing
        self.Nt_calc = np.ceil(self.A_assumed / (np.pi * self.do * self.L))
        if self.NP == 1:
            self.Nt = self.Nt_calc
        else:
            self.Nt = np.ceil(self.Nt_calc / self.NP) * self.NP
        self.pt = 1.25 * self.do
        [k1, n1] = get_Dbt_params(self.NP, self.tube_layout)
        self.Dbt = self.do * (self.Nt / k1) ** (1 / n1)
        self.Ds = self.Dbt / 0.95 + self.C_sb
        self.baffle_spacing = self.baffle_spacing_factor * self.Ds

        # Shell side heat transfer
        # ho = h_{ideal} * Jc * Jl * Jb
        # Get Js from Colburn coefficients - dependent on magnitude of Reynolds number
        # J = f(a1, a2, a3, a4)
        # Bell-Delaware method accounts for -
        # a) leakage between tubes & baffle and shell & baffle
        # b) bypass of flow between tube bundle and shell
        # c) baffle configuration (only a fraction of tubes are in cross-flow)
        A_cr = getA_cr(self)
        self.Pr_s = self.Cp_s * self.mu_s / self.k_s
        self.Re_s = self.m_s * self.do / (self.mu_s * A_cr)
        i_s = getReClasses(self.Re_s)
        [a1_s, a2_s, a3_s, a4_s, b1_s, b2_s, b3_s, b4_s] = getColburnCoeffs(i_s, self.tube_layout)
        a_s = a3_s / (1 + 0.14 * self.Re_s ** a4_s)
        j_s = a1_s * np.power(1.33 / (self.pt / self.do), a_s) * np.power(self.Re_s, a2_s)
        Lc = self.baffle_cut * self.Ds
        Fc = (1 / np.pi) * (np.pi + (2 * (self.Ds - 2 * Lc) / self.Dbt) * np.sin(
            np.arccos((self.Ds - 2 * Lc) / self.Dbt)) - 2 * np.arccos((self.Ds - 2 * Lc) / self.Dbt))
        A_sb = self.Ds * self.C_sb * (np.pi - np.arccos(1 - 2 * Lc / self.Ds))
        A_tb = np.pi * self.do * self.C_tb * self.Nt * (1 + Fc) / 2
        rs = A_sb / (A_sb + A_tb)
        rlm = (A_sb + A_tb) / A_cr
        A_bp = (self.Ds - self.Dbt) * self.baffle_spacing / A_cr
        if self.tube_layout == 30:
            ptp = 0.866 * self.pt
        elif self.tube_layout == 45:
            ptp = 0.707 * self.pt
        elif self.tube_layout == 90:
            ptp = self.pt
        Nc = self.Ds * (1 - 2 * Lc / self.Ds) / ptp
        Jc_s = 0.55 + 0.72 * Fc
        Jl_s = 0.44 * (1 - rs) + (1 - 0.44 * (1 - rs)) * np.exp(-2.2 / rlm)
        Nss = 0.2
        rb = A_cr / A_bp
        if self.Re_s <= 100:
            C = 1.35
        else:
            C = 1.25
        Jb_s = np.exp(-C * rb * (1 - (2 * Nss) ** (1 / 3)))
        hoid = j_s * self.m_s * self.Cp_s * self.Pr_s ** (-2 / 3) / A_cr
        self.ho = hoid * Jc_s * Jl_s * Jb_s

        # Tube side heat transfer
        self.At = np.pi * 0.25 * (self.di) ** 2
        self.vt = self.NP * (self.m_t / self.rho_t) / (self.Nt * self.At)
        self.Re_t = self.di * self.vt * self.rho_t / self.mu_t
        self.Pr_t = self.Cp_t * self.mu_t / self.k_t
        self.hi = 0.023 * (self.k_t / self.di) * np.power(self.Pr_t, 1 / 3) * np.power(self.Re_t, 0.8)

        # Overall heat transfer
        self.U_calc = 1 / (1 / self.ho + (self.do / self.di) / self.hi + self.Rs + self.Rt * (self.do / self.di))

        # Area Calculations
        # Multi-pass correction factor = F = from correlations
        self.R = (self.T_s_in - self.T_s_out) / (self.T_t_out - self.T_t_in)
        self.S = (self.T_t_out - self.T_t_in) / (self.T_s_in - self.T_t_in)
        self.F = F_EvenTube(self.NP, self.R, self.S)
        self.A_calc = self.Q / (self.U_calc * self.lmtd)
        self.A_actual = np.pi * self.do * self.L * self.Nt

        # Shell side pressure drop
        # dP = from correlations = f(b1, b2, b3, b4)
        b = b3_s / (1 + 0.14 * self.Re_s ** b4_s)
        Ncw = 0.8 * Lc / ptp
        A_w = 0.24 * self.Ds ** 2 * (np.arccos((self.Ds - 2 * Lc) / self.Ds) - ((self.Ds - 2 * Lc) / self.Ds) * np.sqrt(
            1 - ((self.Ds - 2 * Lc) / self.Ds) ** 2)) - self.Nt * 0.125 * (1 - Fc) * np.pi * self.do ** 2
        fs_id = b1_s * np.power((1.33 / (self.pt / self.do)), b) * np.power(self.Re_s, b2_s)
        dPs_bid = 2 * fs_id * np.power(self.m_s / A_cr, 2) * Nc / self.rho_s
        Nb = np.floor(self.L / self.baffle_spacing)
        zeta_l = np.exp(-1.33 * (1 + rs) * np.power(rlm, (-0.15 * (1 + rs) + 0.8)))
        zeta_b = np.exp(-3.7 * rb * (1 - (2 * Nss) ** (1 / 3)))
        dPs_wid = (2 + 0.6 * Ncw) * self.m_s ** 2 / (2 * self.rho_s * A_cr * A_w)
        self.dPs_calc = ((Nb - 1) * dPs_bid + Nb * dPs_wid) * zeta_l + 4 * dPs_bid * (1 + Ncw / Nc) * zeta_b

        # Tube side pressure drop
        # dP = 2 * Np * f * L * G^2 / (rho * di)
        ft = 0.046 * np.power(self.Re_t, -0.2)
        self.dPt_calc = 0.5 * self.NP * (ft * self.L / self.di) * np.power(self.NP * self.m_t / (self.Nt * self.At),
                                                                           2) / self.rho_t

    def Costing(self):
        # Shell = carbon steel
        # Tube = stainless steel
        self.Initialize()
        # Pump power = dP * flow-rate = to pump liquid through the module
        self.pump_power = (self.dPt_calc * self.m_t / self.rho_t + self.dPs_calc * self.m_s / self.rho_s) / 0.85
        # Correlations for costing of bare STHE module
        CP = np.power(10, 3.2138 + 0.2688 * np.log10(self.A_calc) + 0.07961 * (np.log10(self.A_calc)) ** 2)
        CBM = CP * (1.8 + 1.5 * 1.7)
        # Operating power = (pump power) * (electricity cost) * (operating hours per year ~ 49 weeks)
        self.OC = 8232 * self.pump_power * 0.1e-3
        # Annuities paid per year : interest/year is 5% and lifetime of STHE is assumed to be 10 years
        i = 0.05
        self.TC = CBM * (i * (1 + i) ** 10) / ((1 + i) ** 10 - 1) + self.OC

    def Optimize(self):
        # Discrete optimization method
        df = getDataFrame(self)
        df["Uerr"] = (1 - df["Ucalculated"] / self.U) * 100
        df_constrained = df[
            (1.1 * df["dPs"] < self.dPs_perm) &
            (1.1 * df["dPt"] < self.dPt_perm) &
            ((1.03 * df["A_calc"] < df["A"])) &
            (df["Uerr"] > 0) &
            (df["Uerr"] < 10)]
        self.solution = df_constrained[df_constrained["total_cost"] == df_constrained["total_cost"].min()]
        self.solution_max = df_constrained[df_constrained["total_cost"] == df_constrained["total_cost"].max()]

# sthe = STHE()
# sthe.Costing()
# sthe.Optimize()
# print(sthe.solution)
