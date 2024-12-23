"""
Script to modify the met_em files for the different domains and times
(initialisation, nudging times) in an efficient way.
"""

from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import CubicSpline
import os

def perturb_atm_temp(met_em_file,delta_T_profile,x_length,y_length):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_profile : numpy array
        Warming(/cooling) profile that should be added to the atmospheric
        temperature profile.
    x_length : int
        Domain length in x-direction (zonal).
    y_length : int
        Domain length in y-direction (meridional).

    Returns
    -------
    None.

    """
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["TT"][:]
    pres = data.variables["PRES"][:]
    pres_mean = np.mean(pres, axis=(2,3))

    pressure = np.array([100000., 92500., 85000., 70000., 60000., 50000.,  40000.,
                30000.,  25000., 20000., 15000., 10000., 7000.,  5000., 
                3000.,   2000.,   1000.,   500.,   100.])

    warming_signal = CubicSpline(-pressure,delta_T_profile)
    delta_T_WRF = warming_signal(-pres_mean)

    # print(delta_T_WRF)
    # print(temp)
    
    new_temp = temp
    
    # i,j, ranges for following loops:
    # for d01: (89,119)
    # for d02: (96,102)
    # for d03: (100,100)
    
    for i in range(x_length):        # shape met_em_file [2]
        for j in range(y_length):    # shape met_em_file [3]
            new_temp[:,:,i,j] += delta_T_WRF
            
    # print(new_temp)

    data["TT"][:] = new_temp[:]
    
def perturb_sea_surf_temp(met_em_file,delta_T):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T : float
        SST change to be added.

    Returns
    -------
    None.

    """
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["SST"][:]
    new_temp = temp
    new_temp[new_temp!=0.] += delta_T    
    
    data["SST"][:] = new_temp[:]
    
def perturb_snow_depth(met_em_file,delta_snow_depth):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_snow_depth : float
        Snow depth change to be added.

    Returns
    -------
    None.

    """
    data = Dataset(met_em_file,mode='r+')
    snowh = data.variables["SNOWH"][:]
    new_snowh = snowh
    new_snowh[new_snowh!=0.] += delta_snow_depth
    
    new_snowh[new_snowh<0.] = 0.
    
    data["SNOWH"][:] = new_snowh[:]
    
def perturb_snow_equivalent(met_em_file,delta_snow_equivalent):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_snow_equivalent : float
        Snow equivalent change to be added.

    Returns
    -------
    None.

    """
    data = Dataset(met_em_file,mode='r+')
    snow = data.variables["SNOW"][:]
    new_snow = snow
    new_snow[new_snow!=0.] += delta_snow_equivalent
    
    new_snow[new_snow<0.] = 0.
    
    data["SNOW"][:] = new_snow[:]  

def perturb_first_soil_layer_temp(met_em_file,delta_T_soil):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_soil : float
        Soil temperature change to be added (first layer).

    Returns
    -------
    None.

    """
    delta_T = delta_T_soil[0]
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["ST000007"][:]
    new_temp = temp
    new_temp += delta_T
    
    data["ST000007"][:] = new_temp[:]
    
def perturb_second_soil_layer_temp(met_em_file,delta_T_soil):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_soil : float
        Soil temperature change to be added (second layer).

    Returns
    -------
    None.
    """
    delta_T = delta_T_soil[1]
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["ST007028"][:]
    new_temp = temp
    new_temp += delta_T
    
    data["ST007028"][:] = new_temp[:]
    
def perturb_third_soil_layer_temp(met_em_file,delta_T_soil):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_soil : float
        Soil temperature change to be added (third layer).

    Returns
    -------
    None.
    """
    delta_T = delta_T_soil[2]
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["ST028100"][:]
    new_temp = temp
    new_temp += delta_T
    
    data["ST028100"][:] = new_temp[:]
    
def perturb_fourth_soil_layer_temp(met_em_file,delta_T_soil):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_soil : float
        Soil temperature change to be added (fourth layer).

    Returns
    -------
    None.
    """
    
    delta_T = delta_T_soil[3]
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["ST100289"][:]
    new_temp = temp
    new_temp += delta_T
    
    data["ST100289"][:] = new_temp[:]
    
def perturb_deep_soil_layer_temp(met_em_file,delta_T_soil):
    """
    Parameters
    ----------
    met_em_file : string
        Path to WRF met_em file (intermediate WRF input file).
    delta_T_soil : float
        Soil temperature change to be added (deep soil layer).

    Returns
    -------
    None.
    """
    delta_T = delta_T_soil[4]
    data = Dataset(met_em_file,mode='r+')
    temp = data.variables["SOILTEMP"][:]
    new_temp = temp
    new_temp += delta_T
    
    data["SOILTEMP"][:] = new_temp[:]
    
# -4K warming signal from NorESM2 experiment historical, years 1955-1964 averaged:
# atmosphere warming:
# delta_T_GCM = np.array([-3.9959671, -2.7646043, -2.1577177, -1.5982894,
#                         -1.6356778,  -1.694097, -1.6750995, -1.2128505,
#                         -0.50441015, 0.60257196, 1.0941533,  1.0762644,
#                         1.5456204,  2.1369917,   3.1071632,  3.8283486,
#                         4.704578,    4.3778434,  3.5943215 ])
# # sea surface warming:
# delta_SST = -4.0

# # snow depth change:
# delta_SNOWH = 1.0585738
# delta_SNOW  = delta_SNOWH*250.

# # soil warming per layer:
# delta_T_soil_layers = np.array([0.87295063, 0.73391387,	0.26603221,
#                                 -0.49049036, -0.66583268])


# -2K warming signal from NorESM2 experiment historical, years 1963-1972 averaged:
# atmosphere warming:
# delta_T_GCM = np.array([-2.0670912, -1.4418576, -1.1163058, -0.658173,
#                         -0.8166948, -0.9986917, -1.1037993, -0.9801041,
#                         -0.55176675, 0.35387996, 1.0059272,  1.3865416,
#                         1.9378971,   2.4863195,  3.2429523,  3.6357505,
#                         3.740048,    3.0787163,  2.1879618 ])
# # sea surface warming:
# delta_SST = -2.0

# # snow depth change:
# delta_SNOWH = 1.3034445
# delta_SNOW  = delta_SNOWH*250.

# # soil warming per layer:
# delta_T_soil_layers = np.array([1.07386211,	0.93494854,	0.45583987,
#                                 -0.35740515, -0.9044792])


# +2K warming signal from NorESM2 experiment ssp585, years 2040-2049 averaged:
# atmosphere warming:
# delta_T_GCM = np.array([2.0029247, 1.7917556, 1.6507587, 1.6291691,
#                         1.5999215, 1.6391481, 1.6124507, 1.2912582,
#                         1.0339572, 1.0892695, 1.5864465, 2.1504672,
#                         2.4661186, 2.531306,  2.1998725, 1.7825944,
#                         0.9965908, 0.59062594, 0.37031284])
# # sea surface warming:
# delta_SST = 2.0

# # snow depth change:
# delta_SNOWH = -0.42189258
# delta_SNOW  = delta_SNOWH*250.

# # soil warming per layer:
# delta_T_soil_layers = np.array([1.41575828, 1.39206544, 1.301411,
#                                 0.94954788, 0.34596505])

# +4K warming_signal from NorESM2 experiment ssp585, years 2047-2056 averaged:
# atmosphere warming:
# delta_T_GCM = np.array([3.950453, 2.8764946, 2.1521933, 1.5129342, 
#                         1.2777321, 1.2162087, 1.2087686, 0.9396713,
#                         0.7794749, 0.9603075, 1.4605988, 1.8673905,
#                         1.9292654, 1.6518413, 0.67105913, -0.2509483,
#                         -1.7348034, -2.2221045, -2.297453])
# # sea surface warming:
# delta_SST = 4.0

# # snow depth change:
# delta_SNOWH = -0.6820114
# delta_SNOW  = delta_SNOWH*250.

# # soil warming per layer:
# delta_T_soil_layers = np.array([3.55641179, 3.54640474, 3.50849511, 
#                                 2.66003793, 1.05349265])


# +6K warming signal from NorESM2 experiment ssp585, years 2058-2067 averaged:
# atmosphere warming:
delta_T_GCM = np.array([5.700079, 3.9012942, 2.6720777, 1.4589857,
                        1.310517, 1.3398547, 1.3253641, 0.7276636,
                        0.080419, -0.7028041, -1.0362593, -0.6750148,
                        -0.80173016, -1.3064933, -2.4018993, -3.1721463,
                        -4.4073796,  -4.686991, -4.532767 ])
# sea surface warming:
delta_SST = 6.0

# snow depth change:
delta_SNOWH = -1.6792828
delta_SNOW  = delta_SNOWH*250.

# soil warming per layer:
delta_T_soil_layers = np.array([5.35247425, 5.41100253, 5.5025648,
                                4.25167636, 2.06164913])


path = "/nird/projects/NS9600K/brittsc/xxx/met_em_files/"

for file in os.listdir(path):
    # print(file)
    
    if "d01" in file:
        perturb_atm_temp(path+file, delta_T_GCM,89,119)
        perturb_sea_surf_temp(path+file, delta_SST)
        perturb_first_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_second_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_third_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_fourth_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_deep_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_snow_depth(path+file, delta_SNOWH)
        perturb_snow_equivalent(path+file, delta_SNOW)
        
    elif "d02" in file:
        perturb_atm_temp(path+file, delta_T_GCM,96,102)
        perturb_sea_surf_temp(path+file, delta_SST)
        perturb_first_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_second_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_third_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_fourth_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_deep_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_snow_depth(path+file, delta_SNOWH)
        perturb_snow_equivalent(path+file, delta_SNOW)        

    elif "d03" in file:
        perturb_atm_temp(path+file, delta_T_GCM,100,100)
        perturb_sea_surf_temp(path+file, delta_SST)
        perturb_first_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_second_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_third_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_fourth_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_deep_soil_layer_temp(path+file, delta_T_soil_layers)
        perturb_snow_depth(path+file, delta_SNOWH)
        perturb_snow_equivalent(path+file, delta_SNOW)        

        
