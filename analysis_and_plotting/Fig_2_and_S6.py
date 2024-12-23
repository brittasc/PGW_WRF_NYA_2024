import functions as fct
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

fct.plotstyle_serif()

plotpath="/nird/projects/NS9600K/brittsc/xxx/plot/"

def TimePlot_qnice_tot(wrfOutputFile,lat,lon,contourf=True,savefig=0):
    """
    Parameters
    ----------
    wrfOutputFile : Dataset
        Netcdf-dataset of WRF output file.
    lat : int
        Latitude index.
    lon : int
        Longitude index.
    contourf : bool, optional
        Whether contourplot should be applied. If False, pcolormesh is
        used. The default is True.
    savefig : int, optional
        0 for not saving, 1 for saving. The default is 0.

    Returns
    -------
    None.
    """
    
    ## Create a color plot of a timeline of variable var above Ny-Ålesund
    
    PH = wrfOutputFile.variables["PH"][288,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][288,:,lat,lon]
    H = (PH+PHB)/9.81
#    print(np.shape(H),np.shape(wrfOutputFile.variables["XTIME"][144:]))

    # Create the figure and add axes
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    if contourf==False:
        plot = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H[1:],
                         wrfOutputFile.variables["QNICE"][144:,:,lat,lon].T+wrfOutputFile.variables["QNSNOW"][144:,:,lat,lon].T+wrfOutputFile.variables["QNGRAUPEL"][144:,:,lat,lon].T,
                         cmap='viridis',shading='gouraud',
                         norm = mpl.colors.LogNorm())
    elif contourf==True:
        plot = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H[1:],
                         wrfOutputFile.variables["QNICE"][144:,:,lat,lon].T+wrfOutputFile.variables["QNSNOW"][144:,:,lat,lon].T+wrfOutputFile.variables["QNGRAUPEL"][144:,:,lat,lon].T,
                         cmap='viridis',
                         levels = [1e-2,1e-1,1e+0,1e+1,1e+2,1e+3,1e+4,1e+5,1e+6],
                         norm = mpl.colors.LogNorm())
        
    # Create the colorbar
    cb = plt.colorbar(plot)#plot,"bottom", size="5%", pad="5%")
    cb.set_label("Total ice number"+' ['+wrfOutputFile.variables["QNICE"].units+']')
    plot.set_clim(1e-2,1e+6)#1e-6)

    # Set the plot title
    # ax.set_title('latitude: '+str(wrfOutputFile.variables["XLONG"][0,lat,lon])+', longitude: '+str(wrfOutputFile["XLAT"][0,lat,lon])+', '+"total ice number")
    ax.set_ylim(0,3500)
#    ax.set_xlabel('Time [minutes since 2019-11-11 12:00:00]')
    ax.set_xlabel('Time [UTC]')# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]')
    ax.set_xticks([720,1080,1440,1800])
#    ax.set_xticklabels(['18:00','00:00','06:00','12:00','18:00'])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'])
    if savefig==1:
        plt.savefig(plotpath+"qnice_tot"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
        plt.savefig(plotpath+"qnice_tot"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        plt.savefig(plotpath+"qnice_tot"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')

def TimePlot_qnice_tot_with_temp_contours(wrfOutputFile,lat,lon,contourf=True,savefig=0):
    """
    Parameters
    ----------
    wrfOutputFile : Dataset
        Netcdf-dataset of WRF output file.
    lat : int
        Latitude index.
    lon : int
        Longitude index.
    contourf : bool, optional
        Whether contourplot should be applied. If False, pcolormesh is
        used. The default is True.
    savefig : int, optional
        0 for not saving, 1 for saving. The default is 0.

    Returns
    -------
    None.
    """
    
    ## Create a color plot of a timeline of total ICNC above Ny-Ålesund
    
    PH = wrfOutputFile.variables["PH"][288,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][288,:,lat,lon]
    H = (PH+PHB)/9.81
#    print(np.shape(H),np.shape(wrfOutputFile.variables["XTIME"][144:]))

    # Create the figure and add axes
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    if contourf==False:
        plot = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H[1:],
                         wrfOutputFile.variables["QNICE"][144:,:,lat,lon].T+wrfOutputFile.variables["QNSNOW"][144:,:,lat,lon].T+wrfOutputFile.variables["QNGRAUPEL"][144:,:,lat,lon].T,
                         cmap='viridis',shading='gouraud',
                         norm = mpl.colors.LogNorm())
    elif contourf==True:
        plot = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H[1:],
                         wrfOutputFile.variables["QNICE"][144:,:,lat,lon].T+wrfOutputFile.variables["QNSNOW"][144:,:,lat,lon].T+wrfOutputFile.variables["QNGRAUPEL"][144:,:,lat,lon].T,
                         cmap='viridis',
                         levels = [1e-2,1e-1,1e+0,1e+1,1e+2,1e+3,1e+4,1e+5,1e+6],
                         norm = mpl.colors.LogNorm())
        
    # Create the colorbar
    cb = plt.colorbar(plot)#plot,"bottom", size="5%", pad="5%")
    # cb.set_label("Total ice number "+'['+wrfOutputFile.variables["QNICE"].units+']')
    cb.set_label("ICNC "+'[kg$^{-1}$]')
    plot.set_clim(1e-2,1e+6)#1e-6)

    # Set the plot title
    # ax.set_title('latitude: '+str(wrfOutputFile.variables["XLONG"][0,lat,lon])+', longitude: '+str(wrfOutputFile["XLAT"][0,lat,lon])+', '+"total ice number")
    ax.set_ylim(0,3500)
#    ax.set_xlabel('Time [minutes since 2019-11-11 12:00:00]')
    ax.set_xlabel('Time [UTC]')# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]')
    ax.set_xticks([720,1080,1440,1800])
#    ax.set_xticklabels(['18:00','00:00','06:00','12:00','18:00'])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'])
    
    # Add grey or red contours for temperatures:
    # Get temperature:
    P = wrfOutputFile.variables["P"][144:,:,lat,lon]+wrfOutputFile.variables["PB"][144:,:,lat,lon]
    pot_T = wrfOutputFile["T"][144:,:,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    plot2 = ax.contour(wrfOutputFile.variables["XTIME"][144:],H[1:],T.T,
                       levels=[258.15,263.15,268.15,273.15],
                       # colors=['lightgrey','darkgrey','grey'])
                       colors=['red','red','red'])
    
    #This paragraph enables personalized contour labels (in Celsius):
    fmt = {}
    strs = ['-15', '-10', '-5', '0']
    for l, s in zip(plot2.levels, strs):
        fmt[l] = s
    
    ax.clabel(plot2, plot2.levels[:], inline=True, fmt=fmt, fontsize=22)
    
    
    
    if savefig==1:
        plt.savefig(plotpath+"qnice_tot_with_red_temp_contours"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
        plt.savefig(plotpath+"qnice_tot_with_red_temp_contours"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        plt.savefig(plotpath+"qnice_tot_with_red_temp_contours"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')


if __name__=="__main__":
    file1=Dataset("/nird/projects/NS9600K/brittsc/xxx/wrfout_d03_2019-11-11_12:00:00")

    TimePlot_qnice_tot(file1,60,55,savefig=1)
    TimePlot_qnice_tot_with_temp_contours(file1,60,55,savefig=1)
