"""
Script for plotting tendencies of secondary ice production processes.
"""

import functions as fct
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

fct.plotstyle_sansserif()

plotpath="/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/plot/"

def multi_color_TimePlot(wrfOutputFile,var1,var2,var3=None,lat=60,lon=55,savefig=0):
    """
    
    Parameters
    ----------
    wrfOutputFile : Dataset
        NetCDF dataset of WRF output file.
    var1 : string
        Name of first variable to plot.
    var2 : string
        Name of second variable to plot.
    var3 : string, optional
        Name of third variable to plot. The default is None.
        OBS: If third variable is droplet shattering, write 'DS1',
        then both modes (DS1, DS2) will be automatically added together.
    lat : int, optional
        Latitude index. The default is 60.
    lon : int, optional
        Longitude index. The default is 55.
    savefig : int, optional
        1 for saving the plot, 0 for not saving. The default is 0.

    Returns
    -------
    None.

    """
    
    # Compute altitude axis:
    PH = wrfOutputFile.variables["PH"][288,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][288,:,lat,lon]
    
    H = np.zeros(len(PH)-1)
    for k in range(len(H)):
        H[k] = 0.5*(PHB[k] + PH[k] + PHB[k+1] + PH[k+1])/9.81
        
    # Initialize figure:
    fig = plt.figure(figsize=(18,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    # Plot first variable:    
    plot1 = ax.pcolor(wrfOutputFile.variables["XTIME"][144:],H,
                      wrfOutputFile.variables[var1][144:,:,lat,lon].T,
                      cmap='Blues',shading='nearest',
                      norm = mpl.colors.LogNorm())
    
    # plot1 = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H,
    #                    wrfOutputFile.variables[var1][144:,:,lat,lon].T,
    #                    levels=[1e-15,1e-12,1e-9,1e-6,1e-3,1,1e+3,1e+4],
    #                    cmap='Blues',norm = mpl.colors.LogNorm())
    
    # Create the colorbar
    cb1 = plt.colorbar(plot1,shrink=0.85, aspect=35, pad=-0.06)
    cb1.ax.tick_params(labelsize=15)
    # cb1.set_label("DNI_BR [kg$^{-1}$s$^{-1}$]",fontsize=15)
    plot1.set_clim(1e-15,1e+4)
    
    # Plot second variable:    
    plot2 = ax.pcolor(wrfOutputFile.variables["XTIME"][144:],H,
                      wrfOutputFile.variables[var2][144:,:,lat,lon].T,
                      cmap='Reds',shading='nearest',
                      norm = mpl.colors.LogNorm())
    
    # plot2 = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H,
    #                    wrfOutputFile.variables[var2][144:,:,lat,lon].T,
    #                    levels=[1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100],
    #                    cmap='Reds',norm = mpl.colors.LogNorm())
    
    # Create the colorbar
    cb2 = plt.colorbar(plot2,shrink=0.85, aspect=35, pad=-0.05)
    cb2.ax.tick_params(labelsize=15)
    # cb2.set_label(var2+' ['+wrfOutputFile.variables[var2].units+']',fontsize=15)
    # cb2.set_label("DNI_RS [kg$^{-1}$s$^{-1}$]",fontsize=15)
    plot2.set_clim(1e-5,100)
    
    # (Optional:) Plot third variable
    if var3=="DNI_DS1":        
        plot3 = ax.pcolor(wrfOutputFile.variables["XTIME"][144:],H,
                          wrfOutputFile.variables[var3][144:,:,lat,lon].T+wrfOutputFile.variables["DNI_DS2"][144:,:,lat,lon].T,
                          cmap='Greys',shading='nearest',
                          norm = mpl.colors.LogNorm(),alpha=0.7)
        
        # plot3 = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H,
        #                   wrfOutputFile.variables[var3][144:,:,lat,lon].T+wrfOutputFile.variables["DNI_DS2"][144:,:,lat,lon].T,
        #                   levels=[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1],
        #                   cmap='Greys',norm = mpl.colors.LogNorm(),
        #                   alpha=0.7)
        
        # Create the colorbar
        cb3 = plt.colorbar(plot3,shrink=0.85, aspect=35, pad=0.02)
        cb3.ax.tick_params(labelsize=15)
        # cb3.set_label("DNI_DS [kg$^{-1}$s$^{-1}$]",fontsize=15)
        plot3.set_clim(1e-7,1)
        
    elif var3==None:
        print("var3 not given")
    else:
        plot3 = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H, wrfOutputFile.variables[var3][144:,:,lat,lon].T,cmap='Greys',shading='gouraud',norm = mpl.colors.LogNorm())    
        # Create the colorbar
        cb3 = plt.colorbar(plot3,shrink=0.85, aspect=35, pad=0.02)
        cb3.ax.tick_params(labelsize=15)
        # cb3.set_label("DNI_DS [kg$^{-1}$s$^{-1}$]",fontsize=15)
        plot3.set_clim(1e-7,1)


    # Set axis labels etc.:
    ax.set_ylim(0,3500)
    ax.set_xlabel('Time [UTC]',fontsize=17)# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]',fontsize=17)
    ax.set_yticks([0,500,1000,1500,2000,2500,3000])
    ax.set_yticklabels([0,500,1000,1500,2000,2500,3000],fontsize=17)
    ax.set_xticks([720,1080,1440,1800])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'],fontsize=17)
    
    if savefig==1:
        plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_pcolor_nearest_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
        plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_pcolor_nearest_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png',dpi=500)
        plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_pcolor_nearest_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')
        # plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_contourf_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
        # plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_contourf_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        # plt.savefig(plotpath+var1+'_'+var2+'_'+str(var3)+'_contourf_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')


if __name__=="__main__":
    file=Dataset("/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
            
    # multi_color_TimePlot(file,"DNI_BR","DNI_HM",lat=60,lon=55,savefig=1)
    # multi_color_TimePlot(file,"DNI_DS1","DNI_DS2",lat=60,lon=55,savefig=1)
    
    multi_color_TimePlot(file,"DNI_BR","DNI_HM",var3="DNI_DS1", lat=60, lon=55,savefig=1)
