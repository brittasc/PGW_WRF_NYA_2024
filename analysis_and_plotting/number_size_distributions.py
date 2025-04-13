# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 13:35:08 2023

@author: brittsc

This script is to calculate number size distributions from outputted number
concentration N and mass mixing ratio q, in first order for cloud droplets only.
"""

import numpy as np, matplotlib.pyplot as plt
from scipy.special import gamma
import scipy.integrate as integrate
from netCDF4 import Dataset


def shape_parameter(N,p,T):
    """
    N: cloud droplet number concentration
    p: pressure (in Pa)
    T: temperature
    """
    rho_air = p/(287.15*T)
    PGAM=0.0005714*(N/1e+6*rho_air)+0.2714
    PGAM=1./(PGAM**2)-1.
    PGAM=max(PGAM,2.)
    PGAM=min(PGAM,10.)
    return PGAM

def lambda_cloud(N,q,mu):
    rho_w = 997.
    c = rho_w*np.pi/6
    d = 3.
    a = c*N*gamma(mu+d+1)
    b = q*gamma(mu+1)
    e = (a/b)**(1/d)
    return e

def N_0(N,lam,mu):
    N_0 = N*lam**(mu+1)/gamma(mu+1)
    return N_0

def number_size_distribution(D,N,q,p,T):
    """
    Input:
        D: droplet diameter in m
        N: droplet number concentration in m-3
        q: cloud water mixing ratio in kg kg-1
        p: pressure in Pa
        T: temperature in Kelvin
    
    Output:
        N: cloud droplet size distribution in micrometer-1 m-3
    """
    mu = shape_parameter(N,p,T)
    lam = lambda_cloud(N,q,mu)
    N_zero = N_0(N,lam,mu)
    N = N_zero*np.exp(-lam*D)*(D**mu)*1e-6
    print("mu: ", mu, "; lam: ", lam, "; N_0: ", N_zero)
    return N

def r_eff_non_droplets(N,q):
    lam=lambda_cloud(N, q, 0)
    r_eff=3/(2*lam)
    return r_eff

def integrand_A(r,N,q,p,T):
    mu = shape_parameter(N,p,T)
    lam = lambda_cloud(N,q,mu)
    N_zero = N_0(N,lam,mu)
    return r**3*N_zero*np.exp(-lam*2*r)*((2*r)**mu)

def integrand_B(r,N,q,p,T):
    mu = shape_parameter(N,p,T)
    lam = lambda_cloud(N,q,mu)
    N_zero = N_0(N,lam,mu)
    C = r**2*N_zero*np.exp(-lam*2*r)*((2*r)**mu)
    # if C.all()==0:
        # print("N_zero: ", N_zero, ", lam: ", lam, ", mu: ", mu)
    return C

def r_eff_droplets(r,N,q,p,T):
    # A = integrate.quad(integrand_A, 0, np.inf, args=(N,q,p,T))[0]
    # B = integrate.quad(integrand_B, 0, np.inf, args=(N,q,p,T))[0]
    
    A = integrate.trapezoid(integrand_A(r, N, q, p, T),x=r)
    B = integrate.trapezoid(integrand_B(r, N, q, p, T),x=r)
    # print(A,B)
    return A/B


if __name__ == "__main__":
    
    """
    # plot number size distributions:

    N = 10.*1e+6 #in m-3
    lat = 60
    lon = 55
    timestep = 270
    level = 40
    
    wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/230331_WRF_NYA_191112/wrfout_d03_2019-11-11_12:00:00")
    figdir = '/nird/projects/NS9600K/brittsc/230331_WRF_NYA_191112/plot'
    
    P = wrfOutputFile.variables["P"][timestep,level,lat,lon]+wrfOutputFile.variables["PB"][timestep,level,lat,lon]
    pot_T = wrfOutputFile.variables["T"][timestep,level,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    q = wrfOutputFile.variables["QCLOUD"][timestep,level,lat,lon]
    
    diameters = np.arange(0,1e-4,2e-6) #up to 0.1mm in 2 micrometer steps
#    print(P,T,diameters,N,q)
    size_distr = number_size_distribution(diameters,N,q,P,T)
    
    plt.figure(figsize=(10,8))
    plt.plot(diameters*1e+6,size_distr,label='time='+str(timestep)+', level='+str(level))
    plt.yscale('log')
    plt.xlabel('Droplet diameter [$\mu$m]')
    plt.ylabel('Size distribution [$\mu$m$^{-1}$ m$^{-3}$]')
    plt.legend()
    fig_name = 'cloud_droplet_size_distr_time'+str(timestep)+'_level'+str(level)+'_20191112'+'.png'
    plt.savefig(figdir+'/'+ fig_name)
    print('plot saved: '+figdir+'/'+fig_name)
    """

    lat = 60
    lon = 55
    timestep = 270
    level = 40
    wrfOutputFile = Dataset("/nird/projects/NS9600K/brittsc/230916_MY_NYA_191112/wrfout_d03_2019-11-11_12:00:00")

    P = wrfOutputFile.variables["P"][timestep,level,lat,lon]+wrfOutputFile.variables["PB"][timestep,level,lat,lon]
    pot_T = wrfOutputFile.variables["T"][timestep,level,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    q_cloud = wrfOutputFile.variables["QCLOUD"][timestep,level,lat,lon]
    q_rain = wrfOutputFile.variables["QRAIN"][timestep,level,lat,lon]
    q_ice = wrfOutputFile.variables["QICE"][timestep,level,lat,lon]
    q_snow = wrfOutputFile.variables["QSNOW"][timestep,level,lat,lon]
    q_graupel = wrfOutputFile.variables["QGRAUP"][timestep,level,lat,lon]

    N_cloud = 9.*1e+6 #in m-3
    N_rain = wrfOutputFile.variables["QNRAIN"][timestep,level,lat,lon]
    N_ice = wrfOutputFile.variables["QNICE"][timestep,level,lat,lon]
    N_snow = wrfOutputFile.variables["QNSNOW"][timestep,level,lat,lon]
    N_graupel = wrfOutputFile.variables["QNGRAUPEL"][timestep,level,lat,lon]
    
    print(q_cloud,N_cloud,P,T)
    
    r_cloud = np.arange(0,5e-3,2e-6) #up to 5mm in 2 micrometer steps
    
    r_eff_cloud = r_eff_droplets(r_cloud, N_cloud, q_cloud, P, T)
    r_eff_rain = r_eff_non_droplets(N_rain, q_rain)
    r_eff_ice = r_eff_non_droplets(N_ice, q_ice)
    r_eff_snow = r_eff_non_droplets(N_snow, q_snow)
    r_eff_graupel = r_eff_non_droplets(N_graupel, q_graupel)
    
    print(r_eff_cloud)
    # print(r_eff_rain, r_eff_ice, r_eff_snow, r_eff_graupel)
    print(integrand_A(r_cloud,N_cloud,q_cloud,P,T))



    
    