"""Calculations for shortwave cloud optical depth, in-cloud water path
and hydrometeor particle sizes"""

import numpy as np, matplotlib.pyplot as plt
from scipy.special import gamma
import scipy.integrate as integrate
from netCDF4 import Dataset
import number_size_distributions as nsd

def vertical_average_r_eff_droplets(start_time,end_time,max_level,lat,lon,r,N,q,P,T):
    q_cloud = q
    r_matrix = np.zeros(np.shape(q_cloud))
    for i in range(np.shape(q_cloud)[0]):
        for j in range(np.shape(q_cloud)[1]):
            if q_cloud[i,j] == 0:
                r_matrix[i,j] = np.nan     
            elif q_cloud[i,j] > 0:
                r_matrix[i,j] = nsd.r_eff_droplets(r, N, q[i,j], P[i,j], T[i,j])
    return np.nanmean(r_matrix,axis=1)

def water_path(wrfout,var,lat,lon,max_level,start_time,end_time):
    PH = wrfout.variables["PH"][288,:max_level+1,lat,lon]
    PHB = wrfout.variables["PHB"][288,:max_level+1,lat,lon]

    H = np.zeros(len(PH)-1)
    for k in range(len(H)):
        H[k] = 0.5*(PHB[k] + PH[k] + PHB[k+1] + PH[k+1])/9.81
        
    # Get pressure, temperature and cloud properties at location of Ny-Ålesund, in time and altitude up to ca. 3 km:
    P = wrfout.variables["P"][start_time:end_time,:max_level,lat,lon]+wrfout.variables["PB"][start_time:end_time,:max_level,lat,lon]
    pot_T = wrfout.variables["T"][start_time:end_time,:max_level,lat,lon]+300
    T = pot_T*(P/100000)**0.2854

    WC = wrfout.variables[var][start_time:end_time,:max_level,lat,lon]*P/(287.058*T)
    # print(np.shape(WC),np.shape(H))
    WP = integrate.trapezoid(WC,x=H,axis=1)
    return WP

def cod_one_category(water_path,r_eff,density):
    a = 3*water_path
    b = 2*r_eff*density
    tau = a/b
    return tau
    
def tau_cloud(wrfout,lat=60,lon=55,start_time=144,end_time=-1,max_level=93):
    
    # Get pressure, temperature and cloud properties at location of Ny-Ålesund, in time and altitude up to ca. 3 km:
    P = wrfout.variables["P"][start_time:end_time,:max_level,lat,lon]+wrfout.variables["PB"][start_time:end_time,:max_level,lat,lon]
    pot_T = wrfout.variables["T"][start_time:end_time,:max_level,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    q_cloud = wrfout.variables["QCLOUD"][start_time:end_time,:max_level,lat,lon]
    q_rain = wrfout.variables["QRAIN"][start_time:end_time,:max_level,lat,lon]
    q_ice = wrfout.variables["QICE"][start_time:end_time,:max_level,lat,lon]
    q_snow = wrfout.variables["QSNOW"][start_time:end_time,:max_level,lat,lon]
    q_graupel = wrfout.variables["QGRAUP"][start_time:end_time,:max_level,lat,lon]

    N_cloud = 9.*1e+6 #in m-3
    N_rain = wrfout.variables["QNRAIN"][start_time:end_time,:max_level,lat,lon]
    N_ice = wrfout.variables["QNICE"][start_time:end_time,:max_level,lat,lon]
    N_snow = wrfout.variables["QNSNOW"][start_time:end_time,:max_level,lat,lon]
    N_graupel = wrfout.variables["QNGRAUPEL"][start_time:end_time,:max_level,lat,lon]
    
    # print(q_cloud,N_cloud,P,T)
    
    # r_cloud = np.arange(0,5e-4,2e-6) #up to 0.5mm in 2 micrometer steps
    r_cloud = np.array([0,5e-7,1e-6,2e-6,3e-6,4e-6,6e-6,8e-6,1e-5,1.4e-5,
                        1.8e-5,2.2e-5,2.6e-5,3.1e-5,3.6e-5,4.1e-5,4.7e-5,
                        5.3e-5,5.9e-5,6.5e-5,7.2e-5,7.9e-5,8.6e-5,9.4e-5,
                        1.2e-4,2.0e-4,2.8e-4,3.7e-4,4.6e-4,5.4e-4,6.4e-4,
                        7.4e-4,8.6e-4,1e-3])
    
    # Calculate effective radius:
    r_eff_rain = nsd.r_eff_non_droplets(N_rain, q_rain)
    r_eff_ice = nsd.r_eff_non_droplets(N_ice, q_ice)
    r_eff_snow = nsd.r_eff_non_droplets(N_snow, q_snow)
    r_eff_graupel = nsd.r_eff_non_droplets(N_graupel, q_graupel)

    # Average over altitude axis to get timeline of r_eff per category:
    r_eff_cloud_vert_avg = vertical_average_r_eff_droplets(start_time,end_time,max_level,lat,lon,r_cloud, N_cloud, q_cloud, P, T)
    r_eff_rain_vert_avg = np.mean(r_eff_rain, axis=1)
    r_eff_ice_vert_avg = np.mean(r_eff_ice, axis=1)
    r_eff_snow_vert_avg = np.mean(r_eff_snow, axis=1)
    r_eff_graupel_vert_avg = np.mean(r_eff_graupel, axis=1)
    
    # Calculate water path (vertically integrated water content) for all hydrometeor categories:
    CWP = water_path(wrfout, "QCLOUD",lat,lon,max_level,start_time,end_time)
    RWP = water_path(wrfout, "QRAIN",lat,lon,max_level,start_time,end_time)
    IWP = water_path(wrfout, "QICE",lat,lon,max_level,start_time,end_time)
    SWP = water_path(wrfout, "QSNOW",lat,lon,max_level,start_time,end_time)
    GWP = water_path(wrfout, "QGRAUP",lat,lon,max_level,start_time,end_time)

    # Calculate cloud optical depth for each hydrometeor category individually:
    cod_cloud = cod_one_category(CWP, r_eff_cloud_vert_avg, 1000.)
    cod_rain = cod_one_category(RWP, r_eff_rain_vert_avg, 1000.)
    cod_ice = cod_one_category(IWP, r_eff_ice_vert_avg, 500.)
    cod_snow = cod_one_category(SWP, r_eff_snow_vert_avg, 100.)
    cod_graupel = cod_one_category(GWP, r_eff_graupel_vert_avg, 900.)
    
    # Make optical depth zero where there's no cloud (of given hydrometeor type):
    cod_cloud = np.array(cod_cloud)
    cod_cloud = np.where(cod_cloud=='--',0,cod_cloud)
    cod_rain = np.array(cod_rain)
    cod_rain = np.where(cod_rain=='--',0,cod_rain)
    cod_ice = np.array(cod_ice)
    cod_ice = np.where(cod_ice=='--',0,cod_ice)
    cod_snow = np.array(cod_snow)
    cod_snow = np.where(cod_snow=='--',0,cod_snow)
    cod_graupel = np.array(cod_graupel)
    cod_graupel = np.where(cod_graupel=='--',0,cod_graupel)
    
    # Calculate total cloud optical depth and liquid and frozen/ice partition:
    cod_liquid = cod_cloud + cod_rain
    cod_frozen = cod_ice + cod_snow + cod_graupel
    cod_tot = cod_liquid + cod_frozen
    
    return cod_tot,cod_cloud,cod_ice,cod_liquid,cod_frozen,CWP,RWP,IWP,SWP,GWP,r_eff_cloud_vert_avg,r_eff_rain_vert_avg,r_eff_ice_vert_avg,r_eff_snow_vert_avg,r_eff_graupel_vert_avg

def tau_cloud_no_ice(wrfout,lat=60,lon=55,start_time=144,end_time=-1,max_level=93):
    
    # Get pressure, temperature and cloud properties at location of Ny-Ålesund, in time and altitude up to ca. 3 km:
    P = wrfout.variables["P"][start_time:end_time,:max_level,lat,lon]+wrfout.variables["PB"][start_time:end_time,:max_level,lat,lon]
    pot_T = wrfout.variables["T"][start_time:end_time,:max_level,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    q_cloud = wrfout.variables["QCLOUD"][start_time:end_time,:max_level,lat,lon]
    q_rain = wrfout.variables["QRAIN"][start_time:end_time,:max_level,lat,lon]

    N_cloud = 9.*1e+6 #in m-3
    N_rain = wrfout.variables["QNRAIN"][start_time:end_time,:max_level,lat,lon]
    
    # print(q_cloud,N_cloud,P,T)
    
    # r_cloud = np.arange(0,5e-4,2e-6) #up to 0.5mm in 2 micrometer steps
    r_cloud = np.array([0,5e-7,1e-6,2e-6,3e-6,4e-6,6e-6,8e-6,1e-5,1.4e-5,
                        1.8e-5,2.2e-5,2.6e-5,3.1e-5,3.6e-5,4.1e-5,4.7e-5,
                        5.3e-5,5.9e-5,6.5e-5,7.2e-5,7.9e-5,8.6e-5,9.4e-5,
                        1.2e-4,2.0e-4,2.8e-4,3.7e-4,4.6e-4,5.4e-4,6.4e-4,
                        7.4e-4,8.6e-4,1e-3])
    
    # Calculate effective radius:
    r_eff_rain = nsd.r_eff_non_droplets(N_rain, q_rain)

    # Average over altitude axis to get timeline of r_eff per category:
    r_eff_cloud_vert_avg = vertical_average_r_eff_droplets(start_time,end_time,max_level,lat,lon,r_cloud, N_cloud, q_cloud, P, T)
    r_eff_rain_vert_avg = np.mean(r_eff_rain, axis=1)
    
    # Calculate water path (vertically integrated water content) for all hydrometeor categories:
    CWP = water_path(wrfout, "QCLOUD",lat,lon,max_level,start_time,end_time)
    RWP = water_path(wrfout, "QRAIN",lat,lon,max_level,start_time,end_time)

    # Calculate cloud optical depth for each hydrometeor category individually:
    cod_cloud = cod_one_category(CWP, r_eff_cloud_vert_avg, 1000.)
    cod_rain = cod_one_category(RWP, r_eff_rain_vert_avg, 1000.)
    
    # Make optical depth zero where there's no cloud (of given hydrometeor type):
    cod_cloud = np.array(cod_cloud)
    cod_cloud = np.where(cod_cloud=='--',0,cod_cloud)
    cod_rain = np.array(cod_rain)
    cod_rain = np.where(cod_rain=='--',0,cod_rain)
    
    # Calculate total cloud optical depth and liquid and frozen/ice partition:
    cod_liquid = cod_cloud + cod_rain
    
    return cod_liquid
    
if __name__=="__main__":
    
    wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/240128_CTRL_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
    # wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/240204_NoINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
    # wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
    # wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
    # wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/240209_Morr2_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

    # cod_tot = np.zeros((288,100,100))
    # cod_liquid = np.zeros((288,100,100))
    # cod_frozen = np.zeros((288,100,100))
    
    # for k in range(100):
    #     for l in range(100):
    #         # cod_tot[:,k,l]=tau_cloud(wrfOutputFile,lat=k,lon=l)[0]
    #         cod_liquid[:,k,l]=tau_cloud_no_ice(wrfOutputFile,lat=k,lon=l)#[1]
    #         # cod_frozen[:,k,l]=tau_cloud(wrfOutputFile,lat=k,lon=l)[2]
    
    # cod_tot=tau_cloud(wrfOutputFile,lat=60,lon=55)[0]
    # cod_liquid=tau_cloud(wrfOutputFile,lat=60,lon=55)[1]
    # cod_frozen=tau_cloud(wrfOutputFile,lat=60,lon=55)[2]
    cod_tot,cod_cloud,cod_ice,cod_liquid,cod_frozen,CWP,RWP,IWP,SWP,GWP,r_eff_cloud_vert_avg,r_eff_rain_vert_avg,r_eff_ice_vert_avg,r_eff_snow_vert_avg,r_eff_graupel_vert_avg = tau_cloud(wrfOutputFile,start_time=144,lat=60,lon=55)
    
    
    print("cod_tot: ",np.mean(cod_tot))
    print("cod_cloud: ",np.mean(cod_cloud))
    print("cod_ice: ",np.mean(cod_ice))
    print("cod_liquid: ",np.mean(cod_liquid))
    print("cod_frozen: ", np.mean(cod_frozen))
    print("CWP: ",np.mean(CWP))
    print("RWP: ",np.mean(RWP))
    print("IWP: ",np.mean(IWP))
    print("SWP: ",np.mean(SWP))
    print("GWP: ",np.mean(GWP))
    print("r_eff_cloud: ",np.nanmean(r_eff_cloud_vert_avg))
    print("r_eff_rain: ",np.mean(r_eff_rain_vert_avg))
    print("r_eff_ice: ",np.mean(r_eff_ice_vert_avg))
    print("r_eff_snow: ",np.mean(r_eff_snow_vert_avg))
    print("r_eff_graupel: ",np.mean(r_eff_graupel_vert_avg))
