import functions as fct
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

fct.plotstyle_serif()

def make_plot(wrfOutputFile,plotpath,start_time=144,end_time=-1,lat=60,lon=55,plot_cloud_base=False):
    """
    Parameters
    ----------
    wrfOutputFile : Dataset
        Netcdf-dataset from WRF output file.
    plotpath : string
        Where to save the figure. Only path, not including document name.
    start_time : int, optional
        Start time index. The default is 144 (i.e. 00 UTC).
    end_time : int, optional
        End time index. The default is -1.
    lat : int, optional
        Latitude index. The default is 60.
    lon : int, optional
        Longitude index. The default is 55.
    plot_cloud_base : bool, optional
        Whether to plot a horizontal line for the cloud base (only taking
        into account in-cloud hydrometeors). The default is False.

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
    LWC_avg24h = np.mean(LWC,axis=0)*1000 #factor 1000 for conversion to g
    
    IWC = (wrfOutputFile.variables["QICE"][144:,:,lat,lon]+wrfOutputFile.variables["QSNOW"][144:,:,lat,lon]+wrfOutputFile.variables["QGRAUP"][144:,:,lat,lon])*P/(287.058*T)
    IWC_avg24h = np.mean(IWC,axis=0)*1000 #factor 1000 for conversion to g
    
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_axes([0.15,0.1,0.8,0.8])
    
    y2 = np.zeros(len(LWC_avg24h))
    ax.plot(LWC_avg24h,H[1:],color='darkblue',label='liquid')
    ax.plot(IWC_avg24h,H[1:],color='lightblue',label='ice')
    
    ax.fill_betweenx(H[1:], LWC_avg24h, y2,color='darkblue')
    ax.fill_betweenx(H[1:], IWC_avg24h, y2, color='lightblue',alpha=0.8)
    
    ax.set_ylim(0,3500)
    ax.set_xlim(0,0.15)
    ax.set_xlabel('Cloud water content [g m$^{-3}$]')
    ax.set_ylabel('Altitude [m]')
    ax.grid(visible=False)
    plt.legend()
    
    #add temperature:
    ax2 = ax.twiny()
    T_avg24h = np.mean(T,axis=0)
    ax2.set_xlabel('Temperature [K]', color='red')  # we already handled the x-label with ax1
    ax2.plot(T_avg24h, H[1:], color='red')
    ax2.tick_params(axis='x', labelcolor='red')
    ax2.grid(visible=False)
    ax2.set_xlim(200,280)
    
    # add RS temperature range:
    T_masked = np.ma.masked_where((T_avg24h>265.13) & (T_avg24h<270.15),T_avg24h)
    # print(T_masked.mask)
    ax2.fill_betweenx(H[1:], 0, 1,
                     where = T_masked.mask,
                     color='lightgray',alpha=0.5,
                     transform=ax.get_yaxis_transform())
    
    if plot_cloud_base==True:            
        CWC = (wrfOutputFile.variables["QCLOUD"][144:,:,lat,lon]+wrfOutputFile.variables["QICE"][144:,:,lat,lon])*P/(287.058*T)
            
        cloud_base_index = np.zeros(288)
        cloud_base = np.zeros(288)
        for i in range(288):
            for j in np.arange(0,40):
                if CWC[i,j+1]-CWC[i,j]>0:
                    cloud_base_index[i] = j
                    cloud_base[i] = H[j]
                    break
        cbase_avg24h = np.mean(cloud_base)  #time in minutes since simulation start
        ax2.hlines(cbase_avg24h,200,280, linestyle='--',color='black')

        plt.savefig(plotpath+'LWC_IWC_avg24h_with_cbase_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.pdf')
        plt.savefig(plotpath+'LWC_IWC_avg24h_with_cbase_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.png')
        plt.savefig(plotpath+'LWC_IWC_avg24h_with_cbase_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.svg')
    
    elif plot_cloud_base==False:
        plt.savefig(plotpath+'LWC_IWC_avg24h_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.pdf')
        plt.savefig(plotpath+'LWC_IWC_avg24h_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.png')
        plt.savefig(plotpath+'LWC_IWC_avg24h_'+str(np.mean(wrfOutputFile.variables["XLAT"][:,lat,lon]))[:5]+'_'+str(np.mean(wrfOutputFile.variables["XLONG"][:,lat,lon]))[:5]+'.svg')



if __name__=="__main__":
    
    plotpath = "/nird/projects/NS9600K/brittsc/xxx/plot/"
  
    file = Dataset("/nird/projects/NS9600K/brittsc/xxx/wrfout_d03_2019-11-11_12:00:00")

    make_plot(file,plotpath,lat=60,lon=55,plot_cloud_base=True)
