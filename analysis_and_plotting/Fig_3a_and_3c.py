"""
Script for box and whisker-plots of 1) downward longwave radiation at the
surface and 2) longwave cloud radiative effect at the surface.
The data is averaged over the whole domain (leaving out the five outermost
grid points in every direction to avoid issues at the domain border).
The whiskers show the temporal variability of the 24h timeseries.

The figure layout is optimized for this exact number and configuration of
simulations included (for publication in GRL 2024). Make a new script when
a different set of simulations should be shown.
"""

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import matplotlib.patches as mpatches
import functions as fct

fct.plotstyle_serif()

"""
In the following, avg_xx denotes the timeseries of domain-averaged
downward longwave radiation at the surface. cls_xx denotes the
(hypothetic) downward longwave radiation at the surface in clear-sky
conditions. The difference is used to calculate the cloud radiative effect.
"""

# Start and end time index of timeseries:
start_time = 144
end_time = -1

wrfout_data1 = Dataset("/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_1        = np.mean(wrfout_data1.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_1        = np.mean(wrfout_data1.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data2 = Dataset("/nird/projects/NS9600K/brittsc/240216_NoSIP_T-4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_2        = np.mean(wrfout_data2.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_2        = np.mean(wrfout_data2.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data3 = Dataset("/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_3        = np.mean(wrfout_data3.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_3        = np.mean(wrfout_data3.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data4 = Dataset("/nird/projects/NS9600K/brittsc/240815_NoSIP_T-2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_4        = np.mean(wrfout_data4.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_4        = np.mean(wrfout_data4.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data5 = Dataset("/nird/projects/NS9600K/brittsc/240128_CTRL_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_5        = np.mean(wrfout_data5.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_5        = np.mean(wrfout_data5.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data6 = Dataset("/nird/projects/NS9600K/brittsc/240213_NoSIP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_6        = np.mean(wrfout_data6.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_6        = np.mean(wrfout_data6.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data7 = Dataset("/nird/projects/NS9600K/brittsc/240130_WRF_NYA_T+2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_7        = np.mean(wrfout_data7.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_7        = np.mean(wrfout_data7.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data8 = Dataset("/nird/projects/NS9600K/brittsc/240816_NoSIP_T+2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_8        = np.mean(wrfout_data8.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_8        = np.mean(wrfout_data8.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data9 = Dataset("/nird/projects/NS9600K/brittsc/240130_WRF_NYA_T+4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_9        = np.mean(wrfout_data9.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_9        = np.mean(wrfout_data9.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data10 = Dataset("/nird/projects/NS9600K/brittsc/240819_NoSIP_T+4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_10        = np.mean(wrfout_data10.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_10        = np.mean(wrfout_data10.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data11 = Dataset("/nird/projects/NS9600K/brittsc/240129_WRF_NYA_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_11        = np.mean(wrfout_data11.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_11        = np.mean(wrfout_data11.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data12 = Dataset("/nird/projects/NS9600K/brittsc/240212_NoSIP_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_12        = np.mean(wrfout_data12.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_12        = np.mean(wrfout_data12.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data13 = Dataset("/nird/projects/NS9600K/brittsc/240204_NoINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_13        = np.mean(wrfout_data13.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_13        = np.mean(wrfout_data13.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))

wrfout_data14 = Dataset("/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")
avg_14        = np.mean(wrfout_data14.variables["GLW"][start_time:end_time,5:-5,5:-5],axis=(1,2))
cls_14        = np.mean(wrfout_data14.variables["LWDNBC"][start_time:end_time,5:-5,5:-5],axis=(1,2))


"""Observed GLW can be imported from read_AWIPEV_radiation.py"""

plt.figure(figsize=(10,4))

# Choose what to plot by selecting one of the top lines for the
# function call:
    
# Either plot GLW (downward longwave radiation at the surface):
bp_1 = plt.boxplot([avg_1,avg_2,avg_3,avg_4,avg_5,avg_6,avg_7,avg_8,
                    avg_9,avg_10,avg_11,avg_12,avg_13,avg_14],
                   
# or plot surface downward radiation in clear-sky conditions:
# bp_1 = plt.boxplot([cls_01,cls_02,cls_1,cls_2,cls_3,cls_4,cls_5,cls_6,
#                     cls_7,cls_8,cls_9],

# or plot Surface LW CRE:
# bp_1 = plt.boxplot([avg_1-cls_1,avg_2-cls_2,avg_3-cls_3,avg_4-cls_4,
#                     avg_5-cls_5,avg_6-cls_6,avg_7-cls_7,avg_8-cls_8,
#                     avg_9-cls_9,avg_10-cls_10,avg_11-cls_11,avg_12-cls_12,
#                     avg_13-cls_13,avg_14-cls_14],
            vert=True,patch_artist=True,
            medianprops=dict(color="black",linewidth=2),
            showmeans=True,
            meanprops=dict(color='darkred',linewidth=2),
            positions =[0.78,1.22,1.78,2.22,2.78,3.22,3.78,4.22,4.78,5.22,5.78,6.22,7.05,7.55],
            widths = 0.35,
            showfliers=False)

plt.xticks(ticks=[1.0,2.0,3.0,4.0,5.0,6.0,7.3],
           labels=["T-4","T-2","T","T+2","T+4","T+6","T"])

# Select either y-axis range for GLW:
plt.ylim(250,302)

# or y-axis range for Surface LW CRE:
# plt.ylim(48,95)


# fill with colors
colors = ['#CCE5FF','#FCE3E3','#CCE5FF','#FCE3E3','#CCE5FF','#FCE3E3',
          '#CCE5FF','#FCE3E3','#CCE5FF','#FCE3E3','#CCE5FF','#FCE3E3',
          '#FFFF99','#FFCC99']
for patch, color in zip(bp_1['boxes'], colors):
    patch.set_facecolor(color)

blue_patch = mpatches.Patch(color='#CCE5FF', linestyle='-', edgecolor='black', label='CTRL')
yellow_patch = mpatches.Patch(color='#FFFF99', label='NoINP')
orange_patch = mpatches.Patch(color='#FFCC99', label='MoreINP')
red_patch = mpatches.Patch(color='#FCE3E3', linestyle='-', edgecolor='black', label='NoSIP')
first_legend = plt.legend(handles=[blue_patch,red_patch],loc='upper left',fontsize=12)
second_legend = plt.legend(handles=[yellow_patch,orange_patch],loc='upper right',fontsize=12)
plt.gca().add_artist(first_legend)

# Select one of the two labeling and saving options:
# If plotting GLW, select:
plt.ylabel("Downward longwave radiation [Wm$^{-2}$]",fontsize=14)
plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW_boxplot_PGW+INP_domain_avg_timeseries_2.png")
plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW_boxplot_PGW+INP_domain_avg_timeseries_2.pdf")
plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW_boxplot_PGW+INP_domain_avg_timeseries_2.svg")

# If plotting Surface LW CRE, select:
# plt.ylabel("Surface LW CRE [Wm$^{-2}$]",fontsize=14)
# plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW-LWDNBC_boxplot_PGW+INP_domain_avg_timeseries_2.png")
# plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW-LWDNBC_boxplot_PGW+INP_domain_avg_timeseries_2.pdf")
# plt.savefig("/nird/projects/NS9600K/brittsc/plots_PGW_paper/GLW-LWDNBC_boxplot_PGW+INP_domain_avg_timeseries_2.svg")

