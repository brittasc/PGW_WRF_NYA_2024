"""
Script for plotting liquid water, ice water and total water content from
WRF output as timeline at one given location.
Optionally, the balloon flight tracks can be plotted in addition.
"""

import functions as fct
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

fct.plotstyle_serif()

plotpath="/nird/projects/NS9600K/brittsc/240204_NoINP_corrected_SST/plot/"


def flight_tracks(date,flight_no,time_res):
    """
    Extract flight tracks (time, altitude) from HoloBalloon data.
    
    Parameters
    ----------
    date : int
        Date given as YYMMDD.
    flight_no : int
        Flight number (1, 2 or 3).
    time_res : int
        Temporal resolution of HoloBalloon data.

    Returns
    -------
    None.
    """
    
    file = "/nird/projects/NS9600K/brittsc/NASCENT_data/HoloBalloon/HoloBalloon_t"+str(time_res)+"/"+str(date)+"_"+str(flight_no)+"_t"+str(time_res)+".nc"
    data = Dataset(file)
#    print(data)
    height = data.variables["instData_height"][:]
#    convert time from days since January 0, 0000 to minutes since 2019-11-11 12:00:
    time = data.variables["instData_timeGPS"][:]
    time = (time - 737740.5)*24*60
#    print(data.variables["instData_timeGPS"])
    return height,time

def liquid_water_content(wrfOutputFile,start_time,end_time,lat=60,lon=55,contourf=False,savefig=0,plot_flight_tracks=False):
    """
    Plotting liquid water content (sum of cloud water and rain water).

    Parameters
    ----------
    wrfOutputFile : Dataset
        NetCDF dataset from WRF output file.
    start_time : int
        Start time index.
    end_time : int
        End time index.
    lat : int, optional
        Latitude index. The default is 60.
    lon : int, optional
        Longitude index. The default is 55.
    contourf : bool, optional
        Whether to use filled contours instead of pcolor.
        The default is False.
    savefig : int, optional
        1 to save figure, 0 to not save. The default is 0.
    plot_flight_tracks : bool, optional
        Whether to plot flight tracks as lines. The default is False.

    Returns
    -------
    None.

    """
    mid_time = int((start_time+end_time)/2)
#    print(wrfOutputFile["PH"])
    PH = wrfOutputFile.variables["PH"][mid_time,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][mid_time,:,lat,lon]
    H = (PH+PHB)/9.81
    P = wrfOutputFile.variables["P"][144:,:,lat,lon]+wrfOutputFile.variables["PB"][144:,:,lat,lon]
    pot_T = wrfOutputFile["T"][144:,:,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    LWC = (wrfOutputFile.variables["QCLOUD"][144:,:,lat,lon]+wrfOutputFile.variables["QRAIN"][144:,:,lat,lon])*P/(287.058*T)
    
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
#    ax.plot(LWC[mid_time+2,:],H[1:])
    
    # Default plotting with pcolormesh:
    if contourf==False:
        plot = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H[1:], LWC.T, cmap='viridis',
                             shading='gouraud',
                             norm = mpl.colors.LogNorm())
    
    # Try contourf instead of pcolormesh:
    elif contourf==True:
        plot = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H[1:], LWC.T, cmap='viridis',
#                         levels = [1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3],
                            levels = [1e-12,3e-12,1e-11,3e-11,1e-10,3e-10,1e-9,3e-9,1e-8,3e-8,1e-7,3e-7,1e-6,3e-6,1e-5,3e-5,1e-4,3e-4,1e-3],
                            norm = mpl.colors.LogNorm())

    # Create the colorbar
    cb = plt.colorbar(plot)#plot,"bottom", size="5%", pad="5%")
    cb.set_label('Liquid water content [kg m$^{-3}$]')
    plot.set_clim(1e-12,1e-3)
    
    # Set the plot title
#    ax.set_title('latitude: '+str(wrfOutputFile.variables["XLONG"][0,lat,lon])+', longitude: '+str(wrfOutputFile["XLAT"][0,lat,lon])+', '+"Total LWC")
    ax.set_ylim(0,2500)
#    ax.set_xlabel('Time [minutes since 2019-11-11 12:00:00]')
    ax.set_xlabel('Time [UTC]')# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]')
    ax.set_xticks([720,1080,1440,1800])
#    ax.set_xticklabels(['18:00','00:00','06:00','12:00','18:00'])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'])
    
    if plot_flight_tracks==True:
        height_1, time_1 = flight_tracks(191112,1,30)
        height_2, time_2 = flight_tracks(191112,2,30)
        height_3, time_3 = flight_tracks(191112,3,30)
        ax.plot(time_1,height_1,color='black')
        ax.plot(time_2,height_2,color='black')
        ax.plot(time_3,height_3,color='black')

    if savefig==1:
        if plot_flight_tracks==False:
            plt.savefig(plotpath+"LWC_tot_querformat_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
            plt.savefig(plotpath+"LWC_tot_querformat_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        elif plot_flight_tracks==True:
            if contourf==False:
                plt.savefig(plotpath+"LWC_with_flight_tracks_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+"LWC_with_flight_tracks_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+"LWC_with_flight_tracks_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')
            elif contourf==True:
                plt.savefig(plotpath+"LWC_with_flight_tracks_contourf"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+"LWC_with_flight_tracks_contourf"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+"LWC_with_flight_tracks_contourf"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')
                
    return LWC
    
def ice_water_content(wrfOutputFile,start_time,end_time,lat=60,lon=55,contourf=False,savefig=0,plot_flight_tracks=False):
    """
    Plotting ice water content (sum of cloud ice, snow and graupel).

    Parameters
    ----------
    wrfOutputFile : Dataset
        NetCDF dataset from WRF output file.
    start_time : int
        Start time index.
    end_time : int
        End time index.
    lat : int, optional
        Latitude index. The default is 60.
    lon : int, optional
        Longitude index. The default is 55.
    contourf : bool, optional
        Whether to use filled contours instead of pcolor.
        The default is False.
    savefig : int, optional
        1 to save figure, 0 to not save. The default is 0.
    plot_flight_tracks : bool, optional
        Whether to plot flight tracks as lines. The default is False.

    Returns
    -------
    None.

    """
    mid_time = int((start_time+end_time)/2)
#    print(wrfOutputFile["PH"])
    PH = wrfOutputFile.variables["PH"][mid_time,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][mid_time,:,lat,lon]
    H = (PH+PHB)/9.81
    P = wrfOutputFile.variables["P"][144:,:,lat,lon]+wrfOutputFile.variables["PB"][144:,:,lat,lon]
    pot_T = wrfOutputFile["T"][144:,:,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    IWC = (wrfOutputFile.variables["QICE"][144:,:,lat,lon]+wrfOutputFile.variables["QSNOW"][144:,:,lat,lon]+wrfOutputFile.variables["QGRAUP"][144:,:,lat,lon])*P/(287.058*T)
    
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
#    ax.plot(LWC[mid_time+2,:],H[1:])
    
    if contourf==False:
        plot = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H[1:], IWC.T, cmap='viridis',
                             shading='gouraud',
                             norm = mpl.colors.LogNorm())
    
    # Try contourf instead of pcolormesh:
    elif contourf==True:
        plot = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H[1:], IWC.T, cmap='viridis',
#                         levels = [1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3],
                         levels = [1e-12,3e-12,1e-11,3e-11,1e-10,3e-10,1e-9,3e-9,1e-8,3e-8,1e-7,3e-7,1e-6,3e-6,1e-5,3e-5,1e-4,3e-4,1e-3],
                         norm = mpl.colors.LogNorm())
     
    # Create the colorbar
    cb = plt.colorbar(plot)#plot,"bottom", size="5%", pad="5%")
    cb.set_label('Ice water content [kg m$^{-3}$]')
    plot.set_clim(1e-12,1e-3)
    
    # Set the plot title
#    ax.set_title('latitude: '+str(wrfOutputFile.variables["XLONG"][0,lat,lon])+', longitude: '+str(wrfOutputFile["XLAT"][0,lat,lon])+', '+"Total LWC")
    ax.set_ylim(0,2500)
#    ax.set_xlabel('Time [minutes since 2019-11-11 12:00:00]')
    ax.set_xlabel('Time [UTC]')# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]')
    ax.set_xticks([720,1080,1440,1800])
#    ax.set_xticklabels(['18:00','00:00','06:00','12:00','18:00'])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'])
    
    if plot_flight_tracks==True:
        height_1, time_1 = flight_tracks(191112,1,30)
        height_2, time_2 = flight_tracks(191112,2,30)
        height_3, time_3 = flight_tracks(191112,3,30)
        ax.plot(time_1,height_1,color='black')
        ax.plot(time_2,height_2,color='black')
        ax.plot(time_3,height_3,color='black')

    if savefig==1:
        if plot_flight_tracks==False:
            plt.savefig(plotpath+'IWC_tot_querformat_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
            plt.savefig(plotpath+'IWC_tot_querformat_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        elif plot_flight_tracks==True:
            if contourf==False:
                plt.savefig(plotpath+'IWC_with_flight_tracks_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+'IWC_with_flight_tracks_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+'IWC_with_flight_tracks_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')
            elif contourf==True:
                plt.savefig(plotpath+'IWC_with_flight_tracks_contourf_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+'IWC_with_flight_tracks_contourf_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+'IWC_with_flight_tracks_contourf_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')

    return IWC

def total_water_content(wrfOutputFile,start_time,end_time,lat=60,lon=55,contourf=False,savefig=0,plot_flight_tracks=False):
    """
    Plotting total water content (all hydrometeor categories).

    Parameters
    ----------
    wrfOutputFile : Dataset
        NetCDF dataset from WRF output file.
    start_time : int
        Start time index.
    end_time : int
        End time index.
    lat : int, optional
        Latitude index. The default is 60.
    lon : int, optional
        Longitude index. The default is 55.
    contourf : bool, optional
        Whether to use filled contours instead of pcolor.
        The default is False.
    savefig : int, optional
        1 to save figure, 0 to not save. The default is 0.
    plot_flight_tracks : bool, optional
        Whether to plot flight tracks as lines. The default is False.

    Returns
    -------
    None.

    """
    mid_time = int((start_time+end_time)/2)
#    print(wrfOutputFile["PH"])
    PH = wrfOutputFile.variables["PH"][mid_time,:,lat,lon]
    PHB = wrfOutputFile.variables["PHB"][mid_time,:,lat,lon]
    H = (PH+PHB)/9.81
    P = wrfOutputFile.variables["P"][144:,:,lat,lon]+wrfOutputFile.variables["PB"][144:,:,lat,lon]
    pot_T = wrfOutputFile["T"][144:,:,lat,lon]+300
    T = pot_T*(P/100000)**0.2854
    
    TWC = (wrfOutputFile.variables["QCLOUD"][144:,:,lat,lon]+wrfOutputFile.variables["QRAIN"][144:,:,lat,lon]+wrfOutputFile.variables["QICE"][144:,:,lat,lon]+wrfOutputFile.variables["QSNOW"][144:,:,lat,lon]+wrfOutputFile.variables["QGRAUP"][144:,:,lat,lon])*P/(287.058*T)
    
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
#    ax.plot(LWC[mid_time+2,:],H[1:])
    ax.set_ylim(0,3000)
    
    # Default plotting as pcolormesh:
    if contourf==False:
        plot = ax.pcolormesh(wrfOutputFile.variables["XTIME"][144:],H[1:], TWC.T, cmap='viridis',
                             shading='gouraud',
                             norm = mpl.colors.LogNorm())
    
    # Try contourf instead of pcolormesh:
    elif contourf==True:
        plot = ax.contourf(wrfOutputFile.variables["XTIME"][144:],H[1:], TWC.T, cmap='viridis',
#                         levels = [1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3],
                         levels = [1e-12,3e-12,1e-11,3e-11,1e-10,3e-10,1e-9,3e-9,1e-8,3e-8,1e-7,3e-7,1e-6,3e-6,1e-5,3e-5,1e-4,3e-4,1e-3],
                         norm = mpl.colors.LogNorm())
    
    # Create the colorbar
    cb = plt.colorbar(plot)#plot,"bottom", size="5%", pad="5%")
    cb.set_label('Total water content [kg m$^{-3}$]')
#    plot.set_clim(1e-12,5e-4)
    plot.set_clim(1e-12,1e-3) #for contourf-plot
    
    # Set the plot title
#    ax.set_title('latitude: '+str(wrfOutputFile.variables["XLONG"][0,lat,lon])+', longitude: '+str(wrfOutputFile["XLAT"][0,lat,lon])+', '+"Total LWC")
    ax.set_ylim(0,2500)
#    ax.set_xlabel('Time [minutes since 2019-11-11 12:00:00]')
    ax.set_xlabel('Time [UTC]')# on 11-12 Nov 2019')
    ax.set_ylabel('Altitude [m]')
    ax.set_xticks([720,1080,1440,1800])
#    ax.set_xticklabels(['18:00','00:00','06:00','12:00','18:00'])
    ax.set_xticklabels(['00:00','06:00','12:00','18:00'])
    
    if plot_flight_tracks==True:
        height_1, time_1 = flight_tracks(191112,1,30)
        height_2, time_2 = flight_tracks(191112,2,30)
        height_3, time_3 = flight_tracks(191112,3,30)
        ax.plot(time_1,height_1,color='dimgray')
        ax.plot(time_2,height_2,color='dimgray')
        ax.plot(time_3,height_3,color='dimgray')
        
    if savefig==1:
        if plot_flight_tracks==False:
            plt.savefig(plotpath+"TWC_tot_querformat_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
            plt.savefig(plotpath+"TWC_tot_querformat_"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
        elif plot_flight_tracks==True:
            if contourf==False:
                plt.savefig(plotpath+"TWC_with_flight_tracks"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+"TWC_with_flight_tracks"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+"TWC_with_flight_tracks"+'_TimePlot_191112_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')
            elif contourf==True:
                plt.savefig(plotpath+"TWC_with_flight_tracks_contourf_191112_"+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.pdf')
                plt.savefig(plotpath+"TWC_with_flight_tracks_contourf_191112_"+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.png')
                plt.savefig(plotpath+"TWC_with_flight_tracks_contourf_191112_"+str(np.mean(wrfOutputFile.variables["XLAT"][:,60,55]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,60,55]))[:5]+'.svg')

if __name__=="__main__":
    file=Dataset("/nird/projects/NS9600K/brittsc/240204_NoINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

#   Standard plotting for multi-panel LWC, IWC, TWC plots
    liquid_water_content(file,144,431,contourf=True,savefig=1,
                          plot_flight_tracks=True)
    
    ice_water_content(file,144,431,contourf=True,savefig=1,
                      plot_flight_tracks=True)
    
    total_water_content(file,144,431,contourf=True,savefig=1,
                        plot_flight_tracks=True)
