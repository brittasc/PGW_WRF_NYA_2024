import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import matplotlib.patches as mpatches

wrfout_data01 = Dataset("/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data01 = wrfout_data01.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data01 = wrfout_data01.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data01 = wrfout_data01.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data01 = wrfout_data01.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data01 = wrfout_data01.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data01 = wrfout_data01.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data01 = acc_rain_24_data01-acc_rain_00_data01
acc_snow_data01 = acc_snow_24_data01-acc_snow_00_data01
acc_graupel_data01 = acc_graupel_24_data01-acc_graupel_00_data01
acc_frozen_data01 = acc_graupel_data01+acc_snow_data01

acc_rain_domain_data01 = np.average(acc_rain_data01)
acc_frozen_domain_data01 = np.average(acc_frozen_data01)
# print(acc_rain_domain_data01,acc_frozen_domain_data01)

wrfout_data02 = Dataset("/nird/projects/NS9600K/brittsc/240131_WRF_NYA_T-2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data02 = wrfout_data02.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data02 = wrfout_data02.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data02 = wrfout_data02.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data02 = wrfout_data02.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data02 = wrfout_data02.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data02 = wrfout_data02.variables["GRAUPELNC"][-1,5:-5,5:-5]


acc_rain_data02 = acc_rain_24_data02-acc_rain_00_data02
acc_snow_data02 = acc_snow_24_data02-acc_snow_00_data02
acc_graupel_data02 = acc_graupel_24_data02-acc_graupel_00_data02
acc_frozen_data02 = acc_graupel_data02+acc_snow_data02

acc_rain_domain_data02 = np.average(acc_rain_data02)
acc_frozen_domain_data02 = np.average(acc_frozen_data02)


wrfout_data1 = Dataset("/nird/projects/NS9600K/brittsc/240128_CTRL_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data1 = wrfout_data1.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data1 = wrfout_data1.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data1 = wrfout_data1.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data1 = wrfout_data1.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data1 = wrfout_data1.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data1 = wrfout_data1.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data1 = acc_rain_24_data1-acc_rain_00_data1
acc_snow_data1 = acc_snow_24_data1-acc_snow_00_data1
acc_graupel_data1 = acc_graupel_24_data1-acc_graupel_00_data1
acc_frozen_data1 = acc_graupel_data1+acc_snow_data1

acc_rain_domain_data1 = np.average(acc_rain_data1)
acc_frozen_domain_data1 = np.average(acc_frozen_data1)


wrfout_data2 = Dataset("/nird/projects/NS9600K/brittsc/240130_WRF_NYA_T+2_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data2 = wrfout_data2.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data2 = wrfout_data2.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data2 = wrfout_data2.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data2 = wrfout_data2.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data2 = wrfout_data2.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data2 = wrfout_data2.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data2 = acc_rain_24_data2-acc_rain_00_data2
acc_snow_data2 = acc_snow_24_data2-acc_snow_00_data2
acc_graupel_data2 = acc_graupel_24_data2-acc_graupel_00_data2
acc_frozen_data2 = acc_graupel_data2+acc_snow_data2

acc_rain_domain_data2 = np.average(acc_rain_data2)
acc_frozen_domain_data2 = np.average(acc_frozen_data2)


wrfout_data3 = Dataset("/nird/projects/NS9600K/brittsc/240130_WRF_NYA_T+4_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data3 = wrfout_data3.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data3 = wrfout_data3.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data3 = wrfout_data3.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data3 = wrfout_data3.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data3 = wrfout_data3.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data3 = wrfout_data3.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data3 = acc_rain_24_data3-acc_rain_00_data3
acc_snow_data3 = acc_snow_24_data3-acc_snow_00_data3
acc_graupel_data3 = acc_graupel_24_data3-acc_graupel_00_data3
acc_frozen_data3 = acc_graupel_data3+acc_snow_data3

acc_rain_domain_data3 = np.average(acc_rain_data3)
acc_frozen_domain_data3 = np.average(acc_frozen_data3)


wrfout_data4 = Dataset("/nird/projects/NS9600K/brittsc/240129_WRF_NYA_T+6_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data4 = wrfout_data4.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data4 = wrfout_data4.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data4 = wrfout_data4.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data4 = wrfout_data4.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data4 = wrfout_data4.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data4 = wrfout_data4.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data4 = acc_rain_24_data4-acc_rain_00_data4
acc_snow_data4 = acc_snow_24_data4-acc_snow_00_data4
acc_graupel_data4 = acc_graupel_24_data4-acc_graupel_00_data4
acc_frozen_data4 = acc_graupel_data4+acc_snow_data4

acc_rain_domain_data4 = np.average(acc_rain_data4)
acc_frozen_domain_data4 = np.average(acc_frozen_data4)


wrfout_data5 = Dataset("/nird/projects/NS9600K/brittsc/240204_NoINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data5 = wrfout_data5.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data5 = wrfout_data5.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data5 = wrfout_data5.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data5 = wrfout_data5.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data5 = wrfout_data5.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data5 = wrfout_data5.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data5 = acc_rain_24_data5-acc_rain_00_data5
acc_snow_data5 = acc_snow_24_data5-acc_snow_00_data5
acc_graupel_data5 = acc_graupel_24_data5-acc_graupel_00_data5
acc_frozen_data5 = acc_graupel_data5+acc_snow_data5

acc_rain_domain_data5 = np.average(acc_rain_data5)
acc_frozen_domain_data5 = np.average(acc_frozen_data5)


wrfout_data6 = Dataset("/nird/projects/NS9600K/brittsc/250328_MoreINP100_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data6 = wrfout_data6.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data6 = wrfout_data6.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data6 = wrfout_data6.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data6 = wrfout_data6.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data6 = wrfout_data6.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data6 = wrfout_data6.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data6 = acc_rain_24_data6-acc_rain_00_data6
acc_snow_data6 = acc_snow_24_data6-acc_snow_00_data6
acc_graupel_data6 = acc_graupel_24_data6-acc_graupel_00_data6
acc_frozen_data6 = acc_graupel_data6+acc_snow_data6

acc_rain_domain_data6 = np.average(acc_rain_data6)
acc_frozen_domain_data6 = np.average(acc_frozen_data6)


wrfout_data7 = Dataset("/nird/projects/NS9600K/brittsc/240204_MoreINP_corrected_SST/wrfout_d03_2019-11-11_12:00:00")

acc_rain_00_data7 = wrfout_data7.variables["RAINNC"][144,5:-5,5:-5]
acc_rain_24_data7 = wrfout_data7.variables["RAINNC"][-1,5:-5,5:-5]
acc_snow_00_data7 = wrfout_data7.variables["SNOWNC"][144,5:-5,5:-5]
acc_snow_24_data7 = wrfout_data7.variables["SNOWNC"][-1,5:-5,5:-5]
acc_graupel_00_data7 = wrfout_data7.variables["GRAUPELNC"][144,5:-5,5:-5]
acc_graupel_24_data7 = wrfout_data7.variables["GRAUPELNC"][-1,5:-5,5:-5]

acc_rain_data7 = acc_rain_24_data7-acc_rain_00_data7
acc_snow_data7 = acc_snow_24_data7-acc_snow_00_data7
acc_graupel_data7 = acc_graupel_24_data7-acc_graupel_00_data7
acc_frozen_data7 = acc_graupel_data7+acc_snow_data7

acc_rain_domain_data7 = np.average(acc_rain_data7)
acc_frozen_domain_data7 = np.average(acc_frozen_data7)



                    
plt.figure(figsize=(8,3))
plt.bar([0.8,1.2,1.8,2.2,2.8,3.2,3.8,4.2,4.8,5.2,5.8,6.2,6.8,7.2,7.8,8.2,8.8,9.2],
        [acc_rain_domain_data01,acc_frozen_domain_data01,
         acc_rain_domain_data02,acc_frozen_domain_data02,
         acc_rain_domain_data1,acc_frozen_domain_data1,
         acc_rain_domain_data2,acc_frozen_domain_data2,
         acc_rain_domain_data3,acc_frozen_domain_data3,
         acc_rain_domain_data4,acc_frozen_domain_data4,#,3.0,2.4],
         acc_rain_domain_data5,acc_frozen_domain_data5,
         acc_rain_domain_data6,acc_frozen_domain_data6,
         acc_rain_domain_data7,acc_frozen_domain_data7],
        color=['blue','green','blue','green','blue','green','blue','green','blue','green','blue','green','blue','green','blue','green','blue','green'],
        width=0.4,
        tick_label=["      CTRL$_\mathrm{T-4}$","","       CTRL$_\mathrm{T-2}$","",
                    "       CTRL$_\mathrm{T}$","","       CTRL$_\mathrm{T+2}$","",
                    "       CTRL$_\mathrm{T+4}$",'',"       CTRL$_\mathrm{T+6}$",'',
                    "      NoINP",'',"       INPx1e2",'',"       INPx1e4",''])

blue_patch = mpatches.Patch(color='blue', label='liquid')
green_patch = mpatches.Patch(color='green', label='frozen')
# grey_patch = mpatches.Patch(color='grey', label='total')
# lightgrey_patch = mpatches.Patch(color='lightgrey', label='undercatch adjustment')
second_legend = plt.legend(handles=[blue_patch,green_patch],loc='upper left')

plt.ylabel("24h accumulated precipitation [mm]")
plt.savefig("/nird/projects/NS9600K/brittsc/precip_plots/precip_barplot_PGW+INP_domain_revised.png")
plt.savefig("/nird/projects/NS9600K/brittsc/precip_plots/precip_barplot_PGW+INP_domain_revised.pdf")
plt.savefig("/nird/projects/NS9600K/brittsc/precip_plots/precip_barplot_PGW+INP_domain_revised.svg")

