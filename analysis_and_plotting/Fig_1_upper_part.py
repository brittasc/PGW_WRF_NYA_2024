"""
Script to plot atmospheric warming profiles corresponding to the analyzed
surface warming levels. Different colors indicate different warming levels.
The plot includes two y-axis scales, showing altitude on the left and
pressure on the right hand side. The y-axis is linear in altitude from the
surface up to 3 km and logarithmic above.
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

def interpolate_temp_profile(met_em_file,delta_T_profile):
    """
    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    delta_T_profile : numpy array
        Warming profile (vertical) from global climate model.

    Returns
    -------
    pres_mean : numpy array (1D)
        Pressure levels averaged across the domain (2D).
    delta_T_WRF : numpy array
        Warming profifle (vertical) interpolated to WRF input levels.
    height_mean : numpy array (1D)
        Heights corresponding to the pressure levels in pres_mean.

    """
    data = Dataset(met_em_file,mode='r')
    pres = data.variables["PRES"][:]
    height = data.variables["GHT"][:]
    
    pres_mean = np.mean(pres, axis=(2,3))
    # print(pres_mean)
    height_mean = np.mean(height, axis=(2,3))
    # print(height_mean)

    pressure = np.array([100000., 92500., 85000., 70000., 60000., 50000.,  40000.,
                30000.,  25000., 20000., 15000., 10000., 7000.,  5000., 
                3000.,   2000.,   1000.,   500.,   100.])

    warming_signal = CubicSpline(-pressure,delta_T_profile)
    delta_T_WRF = warming_signal(-pres_mean)

    # print(delta_T_WRF)
    return pres_mean, delta_T_WRF, height_mean

met_em_testfile = "/nird/projects/NS9600K/brittsc/240106_WRF_NYA_T+4_without_soil_warming/met_em files before modification/met_em.d03.2019-11-11_12:00:00.nc"
plotpath = "/nird/projects/NS9600K/brittsc/plots_PGW_paper/"

minus4_pres, minus4_atm_temp, minus4_height = interpolate_temp_profile(met_em_testfile, delta_T_GCM_minus4)
minus2_pres, minus2_atm_temp, minus2_height = interpolate_temp_profile(met_em_testfile, delta_T_GCM_minus2)
plus2_pres, plus2_atm_temp, plus2_height = interpolate_temp_profile(met_em_testfile, delta_T_GCM_plus2)
plus4_pres, plus4_atm_temp, plus4_height = interpolate_temp_profile(met_em_testfile, delta_T_GCM_plus4)
plus6_pres, plus6_atm_temp, plus6_height = interpolate_temp_profile(met_em_testfile, delta_T_GCM_plus6)

# calculate height values for pressure labels (from which warming level
# does not make any difference):
height_function = CubicSpline(-minus2_pres[0][1:],minus2_height[0][1:])
pressure_tick_values = height_function([-100000,-90000,-80000,-70000,-50000,-20000,-5000,-1000,-100])
print(pressure_tick_values)

fig, ax1 = plt.subplots() 

# ax1.plot(minus4_atm_temp[0]+100,minus4_height[0])
ax1.plot(minus4_atm_temp[0],minus4_height[0], label="T - 4")
ax1.plot(minus2_atm_temp[0],minus2_height[0], label="T - 2")
ax1.plot(plus2_atm_temp[0],plus2_height[0], label="T+2")
ax1.plot(plus4_atm_temp[0],plus4_height[0], label="T+4")
ax1.plot(plus6_atm_temp[0],plus6_height[0], label="T+6")

ax1.set_ylabel("Altitude [km]")
ax1.set_ylim(0,42000)
ax1.set_yscale('symlog',linthresh=3000,linscale=0.8)
ax1.set_yticks([1000,2000,3000,5000,7500,10000,20000,30000,40000])
ax1.set_yticklabels([1,2,3,5,7.5,10,20,30,40])
ax1.set_xlim(-7,10)
ax1.set_xlabel("$\Delta$T [K]")

ax2 = ax1.twinx()

# ax2.plot(minus4_atm_temp[0],minus4_height[0], label="SST-4K")
# ax2.plot(minus2_atm_temp[0],minus2_height[0], label="SST-2K")
# ax2.plot(plus2_atm_temp[0],plus2_height[0], label="SST+2K")
# ax2.plot(plus4_atm_temp[0],plus4_height[0], label="SST+4K")
# ax2.plot(plus6_atm_temp[0],plus6_height[0], label="SST+6K")
ax2.set_yscale('symlog',linthresh=3000,linscale=0.8)
ax2.set_yticks(pressure_tick_values)
ax2.set_yticklabels([1000,900,800,700,500,200,50,10,1])
ax2.grid(visible=False)
ax2.set_ylabel("Pressure [hPa]")

ax1.legend(loc="center right")

plt.tight_layout()
plt.savefig(plotpath+"delta_T_atm_symlog3.png")
plt.savefig(plotpath+"delta_T_atm_symlog3.pdf")
plt.savefig(plotpath+"delta_T_atm_symlog3.svg")
