"""
Script to plot soil warming profiles corresponding to the analyzed surface
warming levels. Different colors indicate different warming levels.
"""

import numpy as np, matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import CubicSpline
import functions as fct

fct.plotstyle_serif()

# Warming levels for atmosphere, SST and soil temperature per analyzed warming level:

# -4K warming signal from NorESM2 experiment historical, years 1955-1964 averaged:
# atmosphere warming:
delta_T_GCM_minus4 = np.array([-3.9959671, -2.7646043, -2.1577177, -1.5982894,
                        -1.6356778,  -1.694097, -1.6750995, -1.2128505,
                        -0.50441015, 0.60257196, 1.0941533,  1.0762644,
                        1.5456204,  2.1369917,   3.1071632,  3.8283486,
                        4.704578,    4.3778434,  3.5943215 ])
# # sea surface warming:
delta_SST = -4.0

# soil warming per layer:
delta_T_soil_layers_minus4 = np.array([0.87295063, 0.73391387,	0.26603221,
                                -0.49049036, -0.66583268])


# -2K warming signal from NorESM2 experiment historical, years 1963-1972 averaged:
# atmosphere warming:
delta_T_GCM_minus2 = np.array([-2.0670912, -1.4418576, -1.1163058, -0.658173,
                        -0.8166948, -0.9986917, -1.1037993, -0.9801041,
                        -0.55176675, 0.35387996, 1.0059272,  1.3865416,
                        1.9378971,   2.4863195,  3.2429523,  3.6357505,
                        3.740048,    3.0787163,  2.1879618 ])
# # sea surface warming:
# delta_SST = -2.0

# soil warming per layer:
delta_T_soil_layers_minus2 = np.array([1.07386211,	0.93494854,	0.45583987,
                                -0.35740515, -0.9044792])


# +2K warming signal from NorESM2 experiment ssp585, years 2040-2049 averaged:
# atmosphere warming:
delta_T_GCM_plus2 = np.array([2.0029247, 1.7917556, 1.6507587, 1.6291691,
                        1.5999215, 1.6391481, 1.6124507, 1.2912582,
                        1.0339572, 1.0892695, 1.5864465, 2.1504672,
                        2.4661186, 2.531306,  2.1998725, 1.7825944,
                        0.9965908, 0.59062594, 0.37031284])
# # sea surface warming:
# delta_SST = 2.0

# # soil warming per layer:
delta_T_soil_layers_plus2 = np.array([1.41575828, 1.39206544, 1.301411,
                                0.94954788, 0.34596505])

# +4K warming_signal from NorESM2 experiment ssp585, years 2047-2056 averaged:
# atmosphere warming:
delta_T_GCM_plus4 = np.array([3.950453, 2.8764946, 2.1521933, 1.5129342, 
                        1.2777321, 1.2162087, 1.2087686, 0.9396713,
                        0.7794749, 0.9603075, 1.4605988, 1.8673905,
                        1.9292654, 1.6518413, 0.67105913, -0.2509483,
                        -1.7348034, -2.2221045, -2.297453])
# sea surface warming:
# delta_SST = 4.0

# soil warming per layer:
delta_T_soil_layers_plus4 = np.array([3.55641179, 3.54640474, 3.50849511, 
                                2.66003793, 1.05349265])


# +6K warming signal from NorESM2 experiment ssp585, years 2058-2067 averaged:
# atmosphere warming:
delta_T_GCM_plus6 = np.array([5.700079, 3.9012942, 2.6720777, 1.4589857,
                        1.310517, 1.3398547, 1.3253641, 0.7276636,
                        0.080419, -0.7028041, -1.0362593, -0.6750148,
                        -0.80173016, -1.3064933, -2.4018993, -3.1721463,
                        -4.4073796,  -4.686991, -4.532767 ])
# sea surface warming:
# delta_SST = 6.0

# soil warming per layer:
delta_T_soil_layers_plus6 = np.array([5.35247425, 5.41100253, 5.5025648,
                                4.25167636, 2.06164913])


plotpath = "/nird/projects/NS9600K/brittsc/plots_PGW_paper/"

# layers:
edges = [-27,-20,-15,-10,-5,0]
# edges = [-300,-289,-100,-28,-7,0]

fig, ax1 = plt.subplots(figsize=[6.4, 2.8]) 

ax1.stairs(delta_T_soil_layers_minus4[::-1], edges, orientation='horizontal', label="SST-4K")
ax1.stairs(delta_T_soil_layers_minus2[::-1], edges, orientation='horizontal', label="SST-2K")
ax1.stairs(delta_T_soil_layers_plus2[::-1], edges, orientation='horizontal', label="SST+2K")
ax1.stairs(delta_T_soil_layers_plus4[::-1], edges, orientation='horizontal', label="SST+4K")
ax1.stairs(delta_T_soil_layers_plus6[::-1], edges, orientation='horizontal', label="SST+6K")

ax1.set_ylabel("Depth [cm]")
ax1.set_ylim(-25,0)
ax1.set_yticks(edges[1:])
ax1.set_yticklabels([289,100,28,7,0])
ax1.set_xlim(-7,10)
ax1.set_xlabel("$\Delta$T [K]")

# ax1.legend()

ax2=ax1.twinx()
ax2.grid(visible=False)
ax2.set_yticks([-20])
ax2.set_yticklabels([1000])
ax2.set_ylabel("Text",color='white')
ax2.yaxis.label.set_color('white')
ax2.tick_params(axis='y', colors='white')

plt.tight_layout()
plt.savefig(plotpath+"delta_T_soil.png")
plt.savefig(plotpath+"delta_T_soil.pdf")
plt.savefig(plotpath+"delta_T_soil.svg")
