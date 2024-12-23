import functions as fct
import cartopy.crs as crs
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.api as sm

from cartopy.feature import NaturalEarthFeature

from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim)

fct.plotstyle_serif()

def plot_3D_var_24h_averaged(file,var,title,vmin=165,vmax=233,plot=True,colorbar=True):
    """
    Used for greyscale plot of OLR and GLW in CTRL simulation.

    Parameters
    ----------
    file : Dataset
        NetCDF dataset of WRF output file.
    var : string
        Variable name of variable to be extracted.
    title : string
        Plot title.
    vmin : float or int, optional
        Colorbar minimum value. The default is 165.
    vmax : float or int, optional
        Colorbar maximum value. The default is 233.
    plot : bool, optional
        Whether to plot a map of the 24h-averaged variable. If True, the
        plot s saved as well, if False only the values are returned.
        The default is True.
    colorbar : bool, optional
        Whether to plot the colorbar. The default is True.

    Returns
    -------
    avg : numpy array
        2D (horizontal) array of 24h-averaged variable.
    [mean of avg] : float
        Mean of avg (scalar).
    """
    
    # Extract variable, i.e. OLR or GLW
    data = file.variables[var][144:]

    # Average var over 24h
    avg = np.mean(data,axis=0)
    # std = np.std(data,axis=0)

    # Get the lat/lon coordinates
    lats, lons = latlon_coords(ht_500)
    # print(lats,lons)
    
    # Get the map projection information
    cart_proj = get_cartopy(ht_500)

    # Create the figure
    fig = plt.figure(figsize=(12,9))
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
                                 facecolor="none",
                                 name="admin_1_states_provinces")
    ax.add_feature(states, linewidth=0.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    if plot==True:
        olr_map =plt.pcolormesh(to_np(lons[50]), to_np(lats[:,50]),
                                to_np(avg),
                                vmin=vmin,vmax=vmax,
                                shading='gouraud',#'nearest',
                                cmap='gray_r',
                                transform=crs.PlateCarree())
        
        if colorbar==True:
            # cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", pad=.05)
            cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", shrink=0.6,aspect=12, pad=.05)
            cbar.ax.set_xlabel(str(var)+" [W m$^{-2}$]")

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(ht_500[:,5:-5])) #leave out outer 5 grid points in plot
        ax.set_ylim(cartopy_ylim(ht_500[5:-5,:]))

        ax.gridlines()

        plt.title(title)
        if colorbar==False:
            plt.savefig(plotpath+str(var)+'_avg_24h_without_colorbar.png')
            plt.savefig(plotpath+str(var)+'_avg_24h_without_colorbar.pdf')
        if colorbar==True:
            plt.savefig(plotpath+str(var)+'_avg_24h_slim_colorbar.png')
            plt.savefig(plotpath+str(var)+'_avg_24h_slim_colorbar.pdf')
        
    return avg,np.mean(avg[5:-5,5:-5])#,std,np.mean(std[5:-5,5:-5])

def plot_3D_var_24h_averaged_diff(file1,file2,var,title,vmin=-7,vmax=7,plot=True,colorbar=True):
    """
    Plot without indication of significance of differences. Not used
    in paper.
    
    Parameters
    ----------
    file1 : netCDF4 Dataset
        CTRL simulation. Present day temperatures and INPs.
    file2 : netCDF4 Dataset
        Perturbed simulation. 
    var : string
        Variable name in nc-file. Needs to be 3D variable.
    title : string
        Plot title.
    vmin : float, optional
        Lower limit for colorbar. The default is -7.
    vmax : float, optional
        Upper limit for colorbar. The default is 7.
    plot : bool, optional
        Whether to plot a figure. The default is True.
    colorbar : bool, optional
        Whether the colorbar should be shown. The default is True.

    Returns
    -------
    avg2-avg1 : numpy array (2D)
        24hour-averaged difference between the values of var in file2 and file1.
    """
    
    # Extract variable, i.e. OLR or GLW
    data1 = file1.variables[var][144:]
    data2 = file2.variables[var][144:]

    # Average var over 24h
    avg1 = np.mean(data1,axis=0)
    avg2 = np.mean(data2,axis=0)

    # Get the lat/lon coordinates
    lats, lons = latlon_coords(ht_500)
    # print(lats,lons)
    
    # Get the map projection information
    cart_proj = get_cartopy(ht_500)

    # Create the figure
    fig = plt.figure(figsize=(12,9))
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
                                 facecolor="none",
                                 name="admin_1_states_provinces")
    ax.add_feature(states, linewidth=0.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    if plot==True:
        olr_map =plt.pcolormesh(to_np(lons[50]), to_np(lats[:,50]),
                                to_np(avg2-avg1),
                                vmin=vmin,vmax=vmax,
                                shading='gouraud',#'nearest',
                                cmap='RdBu_r',
                                transform=crs.PlateCarree())
        
        if colorbar==True:
            cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", pad=.05)
            cbar.ax.set_xlabel("$\Delta$"+str(var)+" [W m$^{-2}$]")

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(ht_500[:,5:-5])) #leave out outer 5 grid points in plot
        ax.set_ylim(cartopy_ylim(ht_500[5:-5,:]))

        ax.gridlines()

        plt.title(title)
        if colorbar==False:
            plt.savefig(plotpath+str(var)+'_diff_avg_24h_without_colorbar.png')
            plt.savefig(plotpath+str(var)+'_diff_avg_24h_without_colorbar.pdf')
        if colorbar==True:
            plt.savefig(plotpath+str(var)+'_diff_avg_24h_Delta.png')
            plt.savefig(plotpath+str(var)+'_diff_avg_24h_Delta.pdf')
        
    return avg2-avg1

def var_std_error(file,var,title,vmin=0,vmax=15,plot=True,colorbar=True):
    """
    Calculate standard error of the 24h-mean of the variable 'var', not
    taking into account possible correlations in the timeseries.

    Parameters
    ----------
    file : Dataset
        NetCDF dataset of WRF output file.
    var : string
        Variable name in nc-file. Needs to be 3D variable.
    title : string
        Plot title.
    vmin : float, optional
        Lower limit for colorbar. The default is 0.
    vmax : float, optional
        Upper limit for colorbar. The default is 15.
    plot : bool, optional
        Whether to plot a figure. The default is True.
    colorbar : bool, optional
        Whether the colorbar should be shown. The default is True.

    Returns
    -------
    avg : numpy array (2D)
        24h-mean of variable var.
    SE : numpy array (2D)
        standard error of the 24h-mean of var.

    """
    # Extract variable, i.e. OLR or GLW
    data = file.variables[var][144:]
    
    # Average var over 24h
    avg = np.mean(data,axis=0)

    # Standard deviation of variable at each grid point:
    sigma = np.std(data,axis=0)
    
    # lag-1 autocorrelation
    # lags = [0,1,2]
    
    # r1 = np.zeros_like(avg)
    SE = np.zeros_like(avg)
    
    for i in range(np.shape(avg)[0]):
        for j in range(np.shape(avg)[1]):
            # acorr = sm.tsa.acf(data[:,i,j], nlags = len(lags)-1)
            # print("autocorr.: ",acorr)
            # r1[i,j] = acorr[1]
    
            # standard error:
            N = np.shape(data)[0]
            # A = (1 + acorr[1])/(1 - acorr[1])# =N/N_eff
            # print("N: ,",N," N_eff: ",N/A)
            SE[i,j] = sigma[i,j]/np.sqrt(N)#*np.sqrt(A)

    if plot==True:
    
        # Get the lat/lon coordinates
        lats, lons = latlon_coords(ht_500)
        # print(lats,lons)
        
        # Get the map projection information
        cart_proj = get_cartopy(ht_500)
        
        # Create the figure
        fig = plt.figure(figsize=(12,9))
        ax = plt.axes(projection=cart_proj)
        
        # Download and add the states and coastlines
        states = NaturalEarthFeature(category="cultural", scale="50m",
                                     facecolor="none",
                                     name="admin_1_states_provinces")
        ax.add_feature(states, linewidth=0.5, edgecolor="black")
        ax.coastlines('50m', linewidth=0.8)

        olr_map =plt.pcolormesh(to_np(lons[50]), to_np(lats[:,50]),
                                to_np(SE),
                                vmin=vmin,vmax=vmax,
                                shading='gouraud',#'nearest',
                                cmap='gray_r',#'RdBu_r',
                                transform=crs.PlateCarree())
        
        if colorbar==True:
            cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", pad=.05)
            cbar.ax.set_xlabel("Standard error "+str(var)+" [W m$^{-2}$]")

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(ht_500[:,5:-5])) #leave out outer 5 grid points in plot
        ax.set_ylim(cartopy_ylim(ht_500[5:-5,:]))

        ax.gridlines()

        plt.title(title)
        
        if colorbar==True:
            plt.savefig(plotpath+str(var)+'_SE_24h.png')
            plt.savefig(plotpath+str(var)+'_SE_24h.pdf')
    
    return avg, SE

def var_std_err_lag_corr(file,var,title,vmin=0,vmax=15,plot=True,colorbar=True):
    """
    Calculate standard error of the 24h-mean of the variable 'var',
    corrected for lag-1 correlation in time series.

    Parameters
    ----------
    file : Dataset
        NetCDF dataset of WRF output file.
    var : string
        Variable name in nc-file. Needs to be 3D variable.
    title : string
        Plot title.
    vmin : float, optional
        Lower limit for colorbar. The default is 0.
    vmax : float, optional
        Upper limit for colorbar. The default is 15.
    plot : bool, optional
        Whether to plot a figure. The default is True.
    colorbar : bool, optional
        Whether the colorbar should be shown. The default is True.

    Returns
    -------
    avg : numpy array (2D)
        24h-mean of variable var.
    SE : numpy array (2D)
        standard error of the 24h-mean of var, corrected for lag-correlation.

    """
    # Extract variable, i.e. OLR or GLW
    data = file.variables[var][144:]
    
    # Average var over 24h
    avg = np.mean(data,axis=0)

    # Standard deviation of variable at each grid point:
    sigma = np.std(data,axis=0)
    
    # lag-1 autocorrelation
    lags = [0,1,2]
    
    r1 = np.zeros_like(avg)
    SE = np.zeros_like(avg)
    
    for i in range(np.shape(avg)[0]):
        for j in range(np.shape(avg)[1]):
            acorr = sm.tsa.acf(data[:,i,j], nlags = len(lags)-1)
            # print("autocorr.: ",acorr)
            r1[i,j] = acorr[1]
    
            # standard error:
            N = np.shape(data)[0]
            A = (1 + acorr[1])/(1 - acorr[1])# =N/N_eff
            # print("N: ,",N," N_eff: ",N/A)
            SE[i,j] = sigma[i,j]/np.sqrt(N)*np.sqrt(A)

    if plot==True:
    
        # Get the lat/lon coordinates
        lats, lons = latlon_coords(ht_500)
        # print(lats,lons)
        
        # Get the map projection information
        cart_proj = get_cartopy(ht_500)
        
        # Create the figure
        fig = plt.figure(figsize=(12,9))
        ax = plt.axes(projection=cart_proj)
        
        # Download and add the states and coastlines
        states = NaturalEarthFeature(category="cultural", scale="50m",
                                     facecolor="none",
                                     name="admin_1_states_provinces")
        ax.add_feature(states, linewidth=0.5, edgecolor="black")
        ax.coastlines('50m', linewidth=0.8)

        olr_map =plt.pcolormesh(to_np(lons[50]), to_np(lats[:,50]),
                                to_np(SE),
                                vmin=vmin,vmax=vmax,
                                shading='gouraud',#'nearest',
                                cmap='gray_r',#'RdBu_r',
                                transform=crs.PlateCarree())
        
        if colorbar==True:
            cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", pad=.05)
            cbar.ax.set_xlabel("Standard error "+str(var)+" [W m$^{-2}$]")

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(ht_500[:,5:-5])) #leave out outer 5 grid points in plot
        ax.set_ylim(cartopy_ylim(ht_500[5:-5,:]))

        ax.gridlines()

        plt.title(title)
        
        if colorbar==True:
            plt.savefig(plotpath+str(var)+'_SE_24h.png')
            plt.savefig(plotpath+str(var)+'_SE_24h.pdf')
    
    return avg, SE

def plot_3D_var_sign_diff(file1,file2,var,title,vmin,vmax,lag_corr=False,plot=True):
    """
    Plot significant difference between 24h-mean of var (not significant
    changes are hatched).

    Parameters
    ----------
    file1 : netCDF4 Dataset
        CTRL simulation. Present day temperatures and INPs.
    file2 : netCDF4 Dataset
        Perturbed simulation. 
    var : string
        Variable name in nc-file. Needs to be 3D variable.
    title : string
        Plot title.
    vmin : float, optional
        Lower limit for colorbar.
    vmax : float, optional
        Upper limit for colorbar.
    lag_corr : bool, optional
        Whether to plot a figure. The default is False.
    plot : bool, optional
        Whether to plot a figure. The default is True.

    Returns
    -------
    diff : numpy array (2D)
        24hour-averaged difference between the values of var in file2 and file1.
    diff_only_significant : numpy array (2D)
        as diff, but zero, where changes are insignificant.

    """
    if lag_corr==False:
        avg1,SE1 = var_std_error(file1, var, title,plot=False)
        avg2,SE2 = var_std_error(file2, var, title,plot=False)
    elif lag_corr==True:
        avg1,SE1 = var_std_err_lag_corr(file1, var, title,plot=False)
        avg2,SE2 = var_std_err_lag_corr(file2, var, title,plot=False)
    
    diff = avg2-avg1
    avg2_always_larger = np.where(avg2>avg1,avg2,avg1)
    avg1_always_smaller = np.where(avg1<avg2,avg1,avg2)
    diff_masked = np.where((avg2_always_larger-SE2)<(avg1_always_smaller+SE1),diff,np.nan)
    diff_only_significant = np.where((avg2_always_larger-SE2)>(avg1_always_smaller+SE1),diff,0)
    
    # print(avg1,SE1)
    # print(avg1+SE1)
    # print(diff_masked)    
    
    if plot==True:
        # Get the lat/lon coordinates
        lats, lons = latlon_coords(ht_500)
        # print(lats,lons)
        
        # Get the map projection information
        cart_proj = get_cartopy(ht_500)
        
        # Create the figure
        fig = plt.figure(figsize=(12,9))
        ax = plt.axes(projection=cart_proj)
        
        # Download and add the states and coastlines
        states = NaturalEarthFeature(category="cultural", scale="50m",
                                     facecolor="none",
                                     name="admin_1_states_provinces")
        ax.add_feature(states, linewidth=0.5, edgecolor="black")
        ax.coastlines('50m', linewidth=0.8)

        olr_map =plt.pcolormesh(to_np(lons[50]), to_np(lats[:,50]),
                                to_np(diff),
                                vmin=vmin,vmax=vmax,
                                shading='gouraud',#'nearest',
                                cmap='RdBu_r',
                                transform=crs.PlateCarree())
        plt.pcolor(to_np(lons[50]), to_np(lats[:,50]),to_np(diff_masked),
                    hatch='//',transform=crs.PlateCarree(),alpha=0.)
        
        cbar = plt.colorbar(olr_map, ax=ax, orientation="horizontal", pad=.05)
        cbar.ax.set_xlabel("$\Delta$"+str(var)+" [W m$^{-2}$]")

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(ht_500[:,5:-5])) #leave out outer 5 grid points in plot
        ax.set_ylim(cartopy_ylim(ht_500[5:-5,:]))

        ax.gridlines()

        plt.title(title)
        if lag_corr==False:
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_NO_lag_corr.png')
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_NO_lag_corr.pdf')
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_NO_lag_corr.svg')
        elif lag_corr==True:
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_with_lag_corr.png')
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_with_lag_corr.pdf')
            plt.savefig(plotpath+str(var)+'_diff_24h_hatched_with_lag_corr.svg')
    print(np.mean(diff[5:-5,5:-5]))   
    print(np.mean(diff_only_significant[5:-5,5:-5]))
    return diff,diff_only_significant

    

# plotpath="/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/plot/"
# plotpath="/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-4_corrected_SST/plot/"
plotpath="/nird/projects/NS9600K/brittsc/240212_NoSIP_T+6_corrected_SST/plot/"


# Open the NetCDF file
# ncfile1 = Dataset("/nird/projects/NS9600K/brittsc/240128_CTRL_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
ncfile1 = Dataset("/nird/projects/NS9600K/brittsc/240129_WRF_NYA_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
ncfile2 = Dataset("/nird/projects/NS9600K/brittsc/240212_NoSIP_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
# ncfile2 = Dataset("/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

# Extract the pressure, geopotential height, and wind variables
p = getvar(ncfile1, "pressure")
z = getvar(ncfile1, "z", units="dm")

# Interpolate geopotential height to 500 hPa
ht_500 = interplevel(z, p, 500)


# Used for paper: 
# olr = plot_3D_var_24h_averaged(ncfile1,"OLR", "CTRL")#,colorbar=False)
# print(olr[1])
# olr_2 = plot_3D_var_24h_averaged(ncfile2,"OLR", "SST+6")#,colorbar=False)
# print(olr_2[1])

# glw = plot_3D_var_24h_averaged(ncfile1,"GLW", "CTRL",vmin=180,vmax=320)#,colorbar=False)
# print(glw[1])
# glw_2 = plot_3D_var_24h_averaged(ncfile2,"GLW", "SST+6",vmin=180,vmax=320)#,colorbar=False)
# print(glw_2[1])

# Used for paper:
plot_3D_var_sign_diff(ncfile1, ncfile2, "OLR", "NoSIP_T+6 - CTRL_T+6", vmin=-10, vmax=10,lag_corr=False,plot=True)
plot_3D_var_sign_diff(ncfile1, ncfile2, "GLW", "NoSIP_T+6 - CTRL_T+6", vmin=-30, vmax=30,lag_corr=False,plot=True)

plot_3D_var_sign_diff(ncfile1, ncfile2, "OLR", "NoSIP_T+6 - CTRL_T+6", vmin=-10, vmax=10,lag_corr=True,plot=True)
plot_3D_var_sign_diff(ncfile1, ncfile2, "GLW", "NoSIP_T+6 - CTRL_T+6", vmin=-30, vmax=30,lag_corr=True,plot=True)
