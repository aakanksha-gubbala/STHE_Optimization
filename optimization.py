import numpy as np
import scipy.optimize
from scipy.constants import R, g
import pandas as pd

tube_layout = [30, 45, 90]
NP = [1, 2, 4]
L = np.arange(2.5, 6.0 + 0.5, 0.5)
do = np.array([0.75, 1, 1.25, 1.5, 2]) * 0.0254
# BWG = np.arange(7, 16 + 1, 1)
# di = do - 2 * getBWG(BWG) * 1e-3
C_sb = 1e-3 * np.array([1, 2, 3, 4, 5])
C_tb = 1e-3 * np.array([1, 2, 3, 4, 5])
baffle_cut = 1e-2 * np.arange(15, 25 + 5, 5)
# baffle_spacing_factor = np.arange(0.1, 0.5 + 0.1, 0.1)

# def costFunc(X):
#     sthe = STHE()
#     sthe.tube_layout = X[0]
#     sthe.NP = X[1]
#     sthe.L = X[2]
#     sthe.do = X[3]
#     sthe.di = sthe.do - 2 * getBWG(X[4]) * 1e-3
#     sthe.C_sb = X[5]
#     sthe.C_tb = X[6]
#     sthe.baffle_cut = X[7]
#     sthe.baffle_spacing_factor = X[8]
#
#     sthe.Costing()
#     return 1e3 * (1 / sthe.TC)


def getQuantities(sthe, X):
    sthe.tube_layout = X[0]
    sthe.NP = X[1]
    sthe.L = X[2]
    sthe.do = X[3]
    sthe.C_sb = X[4]
    sthe.C_tb = X[5]
    sthe.baffle_cut = X[6]

    sthe.Costing()
    return [sthe.TC, sthe.U_calc, sthe.A_calc, sthe.A_actual, sthe.dPs_calc, sthe.dPt_calc]


# X0 = [30, 1, 4.5, 19e-3, 15e-3, 10e-3, 15e-2, 0.5]


def getDataFrame(sthe):
    df = pd.DataFrame()
    n = len(tube_layout) * len(NP) * len(L) * len(do) * len(C_sb) * len(C_tb) * len(baffle_cut)
    i = 0
    x1_array = np.zeros(n)
    x2_array = np.zeros(n)
    x3_array = np.zeros(n)
    x4_array = np.zeros(n)
    x5_array = np.zeros(n)
    x6_array = np.zeros(n)
    x7_array = np.zeros(n)
    TC_array = np.zeros(n)
    UCalc_array = np.zeros(n)
    ACalc_array = np.zeros(n)
    A_array = np.zeros(n)
    dPsCalc_array = np.zeros(n)
    dPtCalc_array = np.zeros(n)
    for x1 in tube_layout:
        for x2 in NP:
            for x3 in L:
                for x4 in do:
                    for x5 in C_sb:
                        for x6 in C_tb:
                            for x7 in baffle_cut:
                                X = [x1, x2, x3, x4, x5, x6, x7]
                                x1_array[i] = x1
                                x2_array[i] = x2
                                x3_array[i] = x3
                                x4_array[i] = x4
                                x5_array[i] = x5
                                x6_array[i] = x6
                                x7_array[i] = x7
                                [TC, UCalc, ACalc, A, dPsCalc, dPtCalc] = getQuantities(sthe, X)
                                TC_array[i] = TC
                                UCalc_array[i] = UCalc
                                ACalc_array[i] = ACalc
                                A_array[i] = A
                                dPsCalc_array[i] = dPsCalc
                                dPtCalc_array[i] = dPtCalc
                                i += 1

    df["tube_layout"] = x1_array
    df["NP"] = x2_array
    df["L"] = x3_array
    df["do"] = x4_array
    df["C_sb"] = x5_array
    df["C_tb"] = x6_array
    df["baffle_cut"] = x7_array
    df["total_cost"] = TC_array
    df["Ucalculated"] = UCalc_array
    df["A_calc"] = ACalc_array
    df["A"] = A_array
    df["dPs"] = dPsCalc_array
    df["dPt"] = dPtCalc_array
    return df
# df.to_csv("array.csv")
# print(df)
