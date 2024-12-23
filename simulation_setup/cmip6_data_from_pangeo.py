# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 20:16:37 2023

@author: brittsc

Script for near-surface and atmospheric temperature changes between
assessed period (historic, future) and reference period (present day) 
from NorESM2 simulations.

Starting point for script development (latest accessed 30 July 2024):
https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html
"""

import pandas as pd
import numpy as np
from netCDF4 import Dataset
import gcsfs
import xarray as xr
import matplotlib.pyplot as plt
import geojson
import cartopy.crs as ccrs

# for Google Cloud:
df = pd.read_csv("https://cmip6.storage.googleapis.com/pangeo-cmip6.csv")
# for AWS S3:
# df = pd.read_csv("https://cmip6-pds.s3.amazonaws.com/pangeo-cmip6.csv")

# df_subset = df.query("activity_id=='CMIP' & source_id=='NorESM2-LM' & experiment_id=='historical' & table_id=='Amon' & variable_id=='tas' ")
# df_subset = df.query("activity_id=='ScenarioMIP' & source_id=='NorESM2-LM' & experiment_id=='ssp585' & variable_id=='tsl' ")
# print(df_subset)


# Connect to Google Cloud Storage
fs = gcsfs.GCSFileSystem(token='anon', access='read_only')


def get_area_per_grid_point(met_em_file,
                            activity_id='ScenarioMIP',
                            institution_id='NCC',
                            source_id='NorESM2-LM',
                            experiment_id='ssp585',
                            variable_id='areacella',
                            plot=False):
    """

    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    activity_id : string
        CMIP6 intercomparison project. The default is 'ScenarioMIP'.
    institution_id : string
        ID of institution maintaining the selected CMIP6 model. The
        default is 'NCC'.
    source_id : string
        CMIP6 model name and configuration. The default is 'NorESM2-LM'.
    experiment_id : string
        CMIP6 modeling experiment ID. The default is 'ssp585'.
    variable_id : string
        Variable containing the area per grid point from the CMIP6 model
        output. The default is 'areacella' (and should not be changed).
        
    Returns
    -------
    area_nya : xarray
        Containing the area per grid point in the CMIP6 model output
        for the domain given by the met_em file.

    """
    
    df_subset = df.query("activity_id==@activity_id & institution_id==@institution_id & source_id==@source_id & experiment_id==@experiment_id & variable_id==@variable_id")
    # df_subset = df.query("activity_id==@activity_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # print(df_subset)
    
    # get the path to a specific zarr store
    zstore = df_subset.zstore.values[-1]
    mapper = fs.get_mapper(zstore)

    # open using xarray
    ds = xr.open_zarr(mapper, consolidated=True)
    
    # select data from outer model domain:
    # transform lon coordinate from 0,360 to -180,180 and reorder the whole dataset:
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    # extract variable from Dataset (becomes then a DataArray):
    ds = ds[variable_id]
    
    
    # SELECT AREA
    # prepare DataArray for extraction of a certain geometry
    # (assign correct dimension names and Coordinate Reference System):    
    ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    ds.rio.write_crs("epsg:4326",inplace=True)  

    # select grid point closest to Ny-Ålesund
    # ta_nya = ds.sel(lat='78.95',lon='11.33',method='nearest')
    # OR
    # select data from outer WRF domain
    # (Obs: Domain geometry is currently hardcoded and not actually taken
    # from the met_em_file passed.)
    geometries = create_domain_geometry(met_em_file)[1]
    geometry_ds = geojson.loads(geometries)
    
    # Perform the clipping (keep only area given by geometries):    
    area_nya = ds.rio.clip(geometries=[geometry_ds],crs="epsg:4326",drop=True)
    
    return area_nya
  
def calc_avg_surface_warming(model_present,model_future,model_area):
    """
    
    Parameters
    ----------
    model_present : xarray
        Output from present_GCM_tas_from_WRF_domain.
    model_future : xarray
        Output from future_GCM_tas_from_WRF_domain.
    model_area : xarray
        Output from get_area_per_grid_point.
        
    Returns
    -------
    warming_level : float
        Surface warming between future and present period
        averaged across the given model domain.

    """
    
    diff = model_future-model_present
        
    total_area = model_area.sum(dim=['lon','lat'],skipna=True)
    
    warming_level = (((diff*model_area).sum(dim=['lon','lat'],skipna=True))/total_area).values
    # print(warming_level)
        
    return warming_level

def get_domain_polygon(met_em_file):
    """
    Probably not really used at the moment since domain is taken from
    get_WRF_domain_from_NorESM2.py.
    
    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).

    Returns
    -------
    polygon_2 : numpy array
        Containing the border coordinates of the domain of the
        met_em file.
    """
    
    data = Dataset(met_em_file)
    
    lons = data.variables["XLONG_M"][0]     # index 0 removes time dimension
    lats = data.variables["XLAT_M"][0]      # index 0 removes time dimension

    polygon_lons = np.concatenate((lons[0].filled(),
                                  lons[:,-1].filled(),
                                  np.flip(lons[-1]).filled(),
                                  np.flip(lons[:,0]).filled()))

    polygon_lats = np.concatenate((lats[0].filled(),
                                  lats[:,-1].filled(),
                                  np.flip(lats[-1]).filled(),
                                  np.flip(lats[:,0]).filled()))

    polygon = [polygon_lons,polygon_lats]
    polygon_2 = np.transpose(polygon)
    
    return polygon_2
    
def create_domain_geometry(met_em_file):
    """

    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).

    Returns
    -------
    geometries : dictionary list
        Border of met_em file domain.
    geometries_string : dictionary string
        Border of met_em file domain. Coordinates currently hardcoded
        (output of get_WRF_domain_from_NorESM2.py).
    """
    
    # geometry = geopandas.points_from_xy([lon_1,lon_2,lon_3,lon_4], [lat_1,lat_2,lat_3,lat_4], crs = "epsg:4326")
    # print(geometry)
    polygon = get_domain_polygon(met_em_file)
    
    geometries = [
        {'type': 'Polygon',
        'coordinates': [    polygon      ]}
        ]
    geometries_string = '''
        {"type": "Polygon",
        "coordinates": [
            [[-14.23761   ,  71.22893   ],
             [-13.858948  ,  71.284836  ],
             [-13.478027  ,  71.33996   ],
             [-13.094879  ,  71.39429   ],
             [-12.709503  ,  71.44781   ],
             [-12.32193   ,  71.50052   ],
             [-11.932159  ,  71.55242   ],
             [-11.540192  ,  71.6035    ],
             [-11.146088  ,  71.65374   ],
             [-10.749817  ,  71.703156  ],
             [-10.35144   ,  71.75172   ],
             [ -9.950928  ,  71.79942   ],
             [ -9.54837   ,  71.84628   ],
             [ -9.143738  ,  71.89227   ],
             [ -8.737091  ,  71.937386  ],
             [ -8.3284    ,  71.98162   ],
             [ -7.9177246 ,  72.02497   ],
             [ -7.5050964 ,  72.06743   ],
             [ -7.0905457 ,  72.108986  ],
             [ -6.6740723 ,  72.149635  ],
             [ -6.2557373 ,  72.189384  ],
             [ -5.8355713 ,  72.2282    ],
             [ -5.413574  ,  72.266106  ],
             [ -4.989807  ,  72.30307   ],
             [ -4.56427   ,  72.3391    ],
             [ -4.1370544 ,  72.37419   ],
             [ -3.70813   ,  72.40833   ],
             [ -3.277588  ,  72.44151   ],
             [ -2.8454285 ,  72.47375   ],
             [ -2.4117126 ,  72.505005  ],
             [ -1.976471  ,  72.53529   ],
             [ -1.5397644 ,  72.56461   ],
             [ -1.101593  ,  72.59295   ],
             [ -0.66204834,  72.6203    ],
             [ -0.22113037,  72.64666   ],
             [  0.22109985,  72.67202   ],
             [  0.6646118 ,  72.69638   ],
             [  1.109314  ,  72.71975   ],
             [  1.5552063 ,  72.742096  ],
             [  2.0022278 ,  72.76344   ],
             [  2.4503174 ,  72.78377   ],
             [  2.8994446 ,  72.80307   ],
             [  3.3495483 ,  72.82135   ],
             [  3.8005676 ,  72.83861   ],
             [  4.252472  ,  72.854836  ],
             [  4.7052    ,  72.870026  ],
             [  5.158722  ,  72.884186  ],
             [  5.6129456 ,  72.89731   ],
             [  6.0678406 ,  72.90938   ],
             [  6.523346  ,  72.92042   ],
             [  6.9794006 ,  72.93041   ],
             [  7.435974  ,  72.939354  ],
             [  7.892975  ,  72.94725   ],
             [  8.350403  ,  72.9541    ],
             [  8.808136  ,  72.95989   ],
             [  9.266174  ,  72.96464   ],
             [  9.724426  ,  72.96833   ],
             [ 10.182861  ,  72.97096   ],
             [ 10.641418  ,  72.97255   ],
             [ 11.100006  ,  72.973076  ],
             [ 11.558594  ,  72.97255   ],
             [ 12.017151  ,  72.97096   ],
             [ 12.475555  ,  72.96833   ],
             [ 12.933838  ,  72.96464   ],
             [ 13.391846  ,  72.95989   ],
             [ 13.849609  ,  72.9541    ],
             [ 14.307007  ,  72.94725   ],
             [ 14.764038  ,  72.939354  ],
             [ 15.220612  ,  72.93041   ],
             [ 15.676666  ,  72.92042   ],
             [ 16.132172  ,  72.90938   ],
             [ 16.587067  ,  72.89731   ],
             [ 17.04129   ,  72.884186  ],
             [ 17.494812  ,  72.870026  ],
             [ 17.94754   ,  72.854836  ],
             [ 18.399445  ,  72.83861   ],
             [ 18.850464  ,  72.82135   ],
             [ 19.300568  ,  72.80307   ],
             [ 19.749695  ,  72.78377   ],
             [ 20.197784  ,  72.76344   ],
             [ 20.644806  ,  72.742096  ],
             [ 21.090698  ,  72.71975   ],
             [ 21.5354    ,  72.69638   ],
             [ 21.978882  ,  72.67202   ],
             [ 22.421112  ,  72.64666   ],
             [ 22.86203   ,  72.6203    ],
             [ 23.301605  ,  72.59295   ],
             [ 23.739746  ,  72.56461   ],
             [ 24.176483  ,  72.53529   ],
             [ 24.611725  ,  72.505005  ],
             [ 25.04544   ,  72.47375   ],
             [ 25.4776    ,  72.44151   ],
             [ 25.908142  ,  72.40833   ],
             [ 26.337036  ,  72.37419   ],
             [ 26.764282  ,  72.3391    ],
             [ 27.189789  ,  72.30307   ],
             [ 27.613586  ,  72.266106  ],
             [ 28.035583  ,  72.2282    ],
             [ 28.45575   ,  72.189384  ],
             [ 28.874084  ,  72.149635  ],
             [ 29.290558  ,  72.108986  ],
             [ 29.705109  ,  72.06743   ],
             [ 30.117737  ,  72.02497   ],
             [ 30.528412  ,  71.98162   ],
             [ 30.937073  ,  71.937386  ],
             [ 31.34375   ,  71.89227   ],
             [ 31.748383  ,  71.84628   ],
             [ 32.15094   ,  71.79942   ],
             [ 32.551422  ,  71.75172   ],
             [ 32.94983   ,  71.703156  ],
             [ 33.34607   ,  71.65374   ],
             [ 33.740204  ,  71.6035    ],
             [ 34.13214   ,  71.55242   ],
             [ 34.521942  ,  71.50052   ],
             [ 34.909515  ,  71.44781   ],
             [ 35.29489   ,  71.39429   ],
             [ 35.67804   ,  71.33996   ],
             [ 36.05896   ,  71.284836  ],
             [ 36.437622  ,  71.22893   ],
             [ 36.437622  ,  71.22893   ],
             [ 36.61371   ,  71.35034   ],
             [ 36.792114  ,  71.47162   ],
             [ 36.97284   ,  71.592735  ],
             [ 37.155975  ,  71.7137    ],
             [ 37.341522  ,  71.83451   ],
             [ 37.52957   ,  71.95516   ],
             [ 37.720123  ,  72.075645  ],
             [ 37.91327   ,  72.19596   ],
             [ 38.10901   ,  72.3161    ],
             [ 38.307434  ,  72.436066  ],
             [ 38.508575  ,  72.55585   ],
             [ 38.712494  ,  72.67544   ],
             [ 38.91922   ,  72.79484   ],
             [ 39.128845  ,  72.91404   ],
             [ 39.34137   ,  73.033035  ],
             [ 39.556885  ,  73.151825  ],
             [ 39.77545   ,  73.2704    ],
             [ 39.99713   ,  73.38876   ],
             [ 40.221985  ,  73.5069    ],
             [ 40.450043  ,  73.6248    ],
             [ 40.681396  ,  73.74247   ],
             [ 40.916077  ,  73.85989   ],
             [ 41.154205  ,  73.97707   ],
             [ 41.395813  ,  74.093994  ],
             [ 41.64096   ,  74.21066   ],
             [ 41.88974   ,  74.32706   ],
             [ 42.142212  ,  74.44318   ],
             [ 42.398438  ,  74.55901   ],
             [ 42.65851   ,  74.67456   ],
             [ 42.922516  ,  74.78982   ],
             [ 43.19052   ,  74.90477   ],
             [ 43.462585  ,  75.01941   ],
             [ 43.73883   ,  75.13373   ],
             [ 44.019287  ,  75.24772   ],
             [ 44.304108  ,  75.361374  ],
             [ 44.593323  ,  75.47469   ],
             [ 44.887024  ,  75.587654  ],
             [ 45.185364  ,  75.70025   ],
             [ 45.488342  ,  75.81248   ],
             [ 45.796143  ,  75.92432   ],
             [ 46.108826  ,  76.035774  ],
             [ 46.426453  ,  76.14683   ],
             [ 46.749146  ,  76.25747   ],
             [ 47.077057  ,  76.36769   ],
             [ 47.410248  ,  76.47748   ],
             [ 47.74881   ,  76.58682   ],
             [ 48.092896  ,  76.69572   ],
             [ 48.442566  ,  76.80414   ],
             [ 48.797974  ,  76.91209   ],
             [ 49.15921   ,  77.01954   ],
             [ 49.52643   ,  77.12648   ],
             [ 49.89969   ,  77.23291   ],
             [ 50.279144  ,  77.33881   ],
             [ 50.664917  ,  77.44417   ],
             [ 51.05713   ,  77.548965  ],
             [ 51.455933  ,  77.65319   ],
             [ 51.86142   ,  77.75683   ],
             [ 52.273712  ,  77.859856  ],
             [ 52.692993  ,  77.962265  ],
             [ 53.119324  ,  78.06405   ],
             [ 53.552917  ,  78.16517   ],
             [ 53.993835  ,  78.265625  ],
             [ 54.44226   ,  78.365395  ],
             [ 54.898346  ,  78.464455  ],
             [ 55.362183  ,  78.5628    ],
             [ 55.833954  ,  78.66039   ],
             [ 56.31378   ,  78.75723   ],
             [ 56.80182   ,  78.85329   ],
             [ 57.298157  ,  78.94854   ],
             [ 57.80301   ,  79.04297   ],
             [ 58.316467  ,  79.13655   ],
             [ 58.838715  ,  79.22927   ],
             [ 59.369873  ,  79.321106  ],
             [ 59.910065  ,  79.41202   ],
             [ 60.459442  ,  79.50201   ],
             [ 61.018158  ,  79.591034  ],
             [ 61.586304  ,  79.67907   ],
             [ 62.164062  ,  79.7661    ],
             [ 62.751526  ,  79.8521    ],
             [ 63.348846  ,  79.937035  ],
             [ 63.956116  ,  80.02088   ],
             [ 64.57349   ,  80.10361   ],
             [ 65.20102   ,  80.1852    ],
             [ 65.83887   ,  80.26562   ],
             [ 66.48712   ,  80.34483   ],
             [ 67.14584   ,  80.42282   ],
             [ 67.815155  ,  80.49955   ],
             [ 68.49512   ,  80.57499   ],
             [ 68.49512   ,  80.57499   ],
             [ 68.03302   ,  80.68691   ],
             [ 67.559875  ,  80.798225  ],
             [ 67.07538   ,  80.908905  ],
             [ 66.5791    ,  81.01892   ],
             [ 66.07077   ,  81.12825   ],
             [ 65.54999   ,  81.23688   ],
             [ 65.01636   ,  81.344765  ],
             [ 64.46951   ,  81.4519    ],
             [ 63.909058  ,  81.558235  ],
             [ 63.334564  ,  81.66375   ],
             [ 62.745605  ,  81.76842   ],
             [ 62.141815  ,  81.8722    ],
             [ 61.522705  ,  81.97507   ],
             [ 60.887848  ,  82.07698   ],
             [ 60.236786  ,  82.17791   ],
             [ 59.56906   ,  82.27782   ],
             [ 58.884186  ,  82.376656  ],
             [ 58.181732  ,  82.47438   ],
             [ 57.46118   ,  82.57097   ],
             [ 56.722076  ,  82.66636   ],
             [ 55.96393   ,  82.76051   ],
             [ 55.18628   ,  82.85338   ],
             [ 54.38864   ,  82.944916  ],
             [ 53.570526  ,  83.035065  ],
             [ 52.731476  ,  83.12377   ],
             [ 51.871033  ,  83.21098   ],
             [ 50.98877   ,  83.296646  ],
             [ 50.08429   ,  83.38071   ],
             [ 49.157135  ,  83.4631    ],
             [ 48.20697   ,  83.543755  ],
             [ 47.23343   ,  83.62262   ],
             [ 46.236206  ,  83.69962   ],
             [ 45.215027  ,  83.774704  ],
             [ 44.169678  ,  83.847786  ],
             [ 43.099945  ,  83.91881   ],
             [ 42.005768  ,  83.98769   ],
             [ 40.887085  ,  84.054375  ],
             [ 39.743866  ,  84.118774  ],
             [ 38.576233  ,  84.180824  ],
             [ 37.38434   ,  84.24045   ],
             [ 36.168488  ,  84.29758   ],
             [ 34.928986  ,  84.35213   ],
             [ 33.66632   ,  84.40404   ],
             [ 32.381042  ,  84.453224  ],
             [ 31.073792  ,  84.499626  ],
             [ 29.745361  ,  84.54317   ],
             [ 28.396667  ,  84.58379   ],
             [ 27.028656  ,  84.62143   ],
             [ 25.642517  ,  84.65601   ],
             [ 24.23938   ,  84.68749   ],
             [ 22.820679  ,  84.71581   ],
             [ 21.387817  ,  84.74092   ],
             [ 19.942291  ,  84.76278   ],
             [ 18.485779  ,  84.78134   ],
             [ 17.019989  ,  84.79658   ],
             [ 15.546631  ,  84.80846   ],
             [ 14.067627  ,  84.81696   ],
             [ 12.584778  ,  84.82207   ],
             [ 11.100006  ,  84.82378   ],
             [  9.615234  ,  84.82207   ],
             [  8.132385  ,  84.81696   ],
             [  6.653351  ,  84.80846   ],
             [  5.180023  ,  84.79658   ],
             [  3.714203  ,  84.78134   ],
             [  2.2576904 ,  84.76278   ],
             [  0.8121948 ,  84.74092   ],
             [ -0.6206665 ,  84.71581   ],
             [ -2.0393982 ,  84.68749   ],
             [ -3.442505  ,  84.65601   ],
             [ -4.8286743 ,  84.62143   ],
             [ -6.1966553 ,  84.58379   ],
             [ -7.5453796 ,  84.54317   ],
             [ -8.873779  ,  84.499626  ],
             [-10.18103   ,  84.453224  ],
             [-11.466339  ,  84.40404   ],
             [-12.729004  ,  84.35213   ],
             [-13.968475  ,  84.29758   ],
             [-15.184357  ,  84.24045   ],
             [-16.37622   ,  84.180824  ],
             [-17.543854  ,  84.118774  ],
             [-18.687073  ,  84.054375  ],
             [-19.805786  ,  83.98769   ],
             [-20.899963  ,  83.91881   ],
             [-21.969666  ,  83.847786  ],
             [-23.015015  ,  83.774704  ],
             [-24.036194  ,  83.69962   ],
             [-25.033417  ,  83.62262   ],
             [-26.006958  ,  83.543755  ],
             [-26.957123  ,  83.4631    ],
             [-27.884277  ,  83.38071   ],
             [-28.788788  ,  83.296646  ],
             [-29.671051  ,  83.21098   ],
             [-30.531464  ,  83.12377   ],
             [-31.370514  ,  83.035065  ],
             [-32.18863   ,  82.944916  ],
             [-32.986298  ,  82.85338   ],
             [-33.763947  ,  82.76051   ],
             [-34.522095  ,  82.66636   ],
             [-35.26117   ,  82.57097   ],
             [-35.98175   ,  82.47438   ],
             [-36.684204  ,  82.376656  ],
             [-37.36905   ,  82.27782   ],
             [-38.036804  ,  82.17791   ],
             [-38.687866  ,  82.07698   ],
             [-39.322723  ,  81.97507   ],
             [-39.941833  ,  81.8722    ],
             [-40.545624  ,  81.76842   ],
             [-41.134552  ,  81.66375   ],
             [-41.709045  ,  81.558235  ],
             [-42.2695    ,  81.4519    ],
             [-42.816345  ,  81.344765  ],
             [-43.349976  ,  81.23688   ],
             [-43.87079   ,  81.12825   ],
             [-44.37912   ,  81.01892   ],
             [-44.875366  ,  80.908905  ],
             [-45.359894  ,  80.798225  ],
             [-45.833008  ,  80.68691   ],
             [-46.295105  ,  80.57499   ],
             [-46.295105  ,  80.57499   ],
             [-45.615143  ,  80.49955   ],
             [-44.94583   ,  80.42282   ],
             [-44.28711   ,  80.34483   ],
             [-43.638855  ,  80.26562   ],
             [-43.001007  ,  80.1852    ],
             [-42.373474  ,  80.10361   ],
             [-41.756104  ,  80.02088   ],
             [-41.148834  ,  79.937035  ],
             [-40.551544  ,  79.8521    ],
             [-39.96405   ,  79.7661    ],
             [-39.386322  ,  79.67907   ],
             [-38.818146  ,  79.591034  ],
             [-38.25946   ,  79.50201   ],
             [-37.710083  ,  79.41202   ],
             [-37.16986   ,  79.321106  ],
             [-36.638733  ,  79.22927   ],
             [-36.116486  ,  79.13655   ],
             [-35.603027  ,  79.04297   ],
             [-35.098175  ,  78.94854   ],
             [-34.601807  ,  78.85329   ],
             [-34.11377   ,  78.75723   ],
             [-33.633972  ,  78.66039   ],
             [-33.1622    ,  78.5628    ],
             [-32.698364  ,  78.464455  ],
             [-32.24228   ,  78.365395  ],
             [-31.793854  ,  78.265625  ],
             [-31.352905  ,  78.16517   ],
             [-30.919312  ,  78.06405   ],
             [-30.492981  ,  77.962265  ],
             [-30.0737    ,  77.859856  ],
             [-29.661407  ,  77.75683   ],
             [-29.25592   ,  77.65319   ],
             [-28.857147  ,  77.548965  ],
             [-28.464935  ,  77.44417   ],
             [-28.079132  ,  77.33881   ],
             [-27.699677  ,  77.23291   ],
             [-27.326416  ,  77.12648   ],
             [-26.959229  ,  77.01954   ],
             [-26.597961  ,  76.91209   ],
             [-26.242584  ,  76.80414   ],
             [-25.892883  ,  76.69572   ],
             [-25.548798  ,  76.58682   ],
             [-25.210236  ,  76.47748   ],
             [-24.877075  ,  76.36769   ],
             [-24.549164  ,  76.25747   ],
             [-24.22644   ,  76.14683   ],
             [-23.908813  ,  76.035774  ],
             [-23.59613   ,  75.92432   ],
             [-23.28836   ,  75.81248   ],
             [-22.985352  ,  75.70025   ],
             [-22.687042  ,  75.587654  ],
             [-22.39331   ,  75.47469   ],
             [-22.104095  ,  75.361374  ],
             [-21.819305  ,  75.24772   ],
             [-21.538818  ,  75.13373   ],
             [-21.262604  ,  75.01941   ],
             [-20.990509  ,  74.90477   ],
             [-20.722504  ,  74.78982   ],
             [-20.458527  ,  74.67456   ],
             [-20.198425  ,  74.55901   ],
             [-19.9422    ,  74.44318   ],
             [-19.689728  ,  74.32706   ],
             [-19.440948  ,  74.21066   ],
             [-19.1958    ,  74.093994  ],
             [-18.954193  ,  73.97707   ],
             [-18.716095  ,  73.85989   ],
             [-18.481384  ,  73.74247   ],
             [-18.25003   ,  73.6248    ],
             [-18.021973  ,  73.5069    ],
             [-17.79715   ,  73.38876   ],
             [-17.57547   ,  73.2704    ],
             [-17.356903  ,  73.151825  ],
             [-17.141357  ,  73.033035  ],
             [-16.928833  ,  72.91404   ],
             [-16.719238  ,  72.79484   ],
             [-16.512482  ,  72.67544   ],
             [-16.308594  ,  72.55585   ],
             [-16.107452  ,  72.436066  ],
             [-15.909027  ,  72.3161    ],
             [-15.713257  ,  72.19596   ],
             [-15.520142  ,  72.075645  ],
             [-15.329559  ,  71.95516   ],
             [-15.141541  ,  71.83451   ],
             [-14.955963  ,  71.7137    ],
             [-14.772827  ,  71.592735  ],
             [-14.592102  ,  71.47162   ],
             [-14.413696  ,  71.35034   ],
             [-14.23761   ,  71.22893   ]]]}'''
    # geometries.to_crs("epsg:4326")
    return geometries,geometries_string

def present_GCM_tas_from_WRF_domain(met_em_file,activity_id,institution_id,source_id,experiment_id,table_id,variable_id,plot=False):
    """

    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    activity_id : string
        CMIP6 intercomparison project, e.g. 'ScenarioMIP'.
    institution_id : string
        ID of institution maintaining the selected CMIP6 model, e.g. 'NCC'.
    source_id : string
        CMIP6 model name and configuration, e.g. 'NorESM2-LM'.
    experiment_id : string
        CMIP6 modeling experiment ID, e.g. 'ssp585'.
    table_id : string
        Specifying what kind of data, e.g. 'Amon' for monthly mean.
    variable_id : string
        Abbreviation for the variable to be extracted, here 'tas' for
        near-surface air temperature.
    plot : bool, optional
        Whether to plot a map of the time-averaged near-surface air
        temperature. The default is False.

    Returns
    -------
    tas_nya_present_mean : xarray
        Time-averaged array of near-surface air temperature in 2D.

    """
    import rioxarray,geojson
    
    # GET AND PREPARE DATASET
    df_subset = df.query("activity_id==@activity_id & source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # df_subset = df.query("source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # print(df_subset)
    
    # get the path to a specific zarr store
    zstore = df_subset.zstore.values[-1]
    mapper = fs.get_mapper(zstore)

    # open using xarray
    ds = xr.open_zarr(mapper)#, consolidated=True)
    
    # transform lon coordinate from 0,360 to -180,180 and reorder the whole dataset:
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    # extract variable from Dataset (becomes then a DataArray):
    ds = ds[variable_id]
    # print(ds)
    
    # SELECT AREA
    # prepare DataArray for extraction of a certain geometry
    # (assign correct dimension names and Coordinate Reference System):    
    ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    ds.rio.write_crs("epsg:4326",inplace=True)  

    # select grid point closest to Ny-Ålesund
    # ta_nya = ds.sel(lat='78.95',lon='11.33',method='nearest')
    # OR
    # select data from outer WRF domain
    # (Obs: Domain geometry is currently hardcoded and not actually taken
    # from the met_em_file passed.)
    geometries = create_domain_geometry(met_em_file)[1]
    geometry_ds = geojson.loads(geometries)
    
    # Perform the clipping (keep only area given by geometries):    
    tas_nya = ds.rio.clip(geometries=[geometry_ds],crs="epsg:4326",drop=True)


    # SELECT TIME
    # select all November data from a ten-year period:    
    tas_nya_present = tas_nya.sel(time=slice('2015-11-16T12:00:00','2025-11-16T12:00:00',12))
    # print(tas_nya_present)
    
    # TAKE TIME AVERAGE    
    tas_nya_present_mean = tas_nya_present.mean(dim='time')
    
    if plot==True:
        tas_nya_present_mean.plot()
        plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/tas_clipped_test.png")
        
    return tas_nya_present_mean
   
def future_GCM_tas_from_WRF_domain(start_year,met_em_file,activity_id,institution_id,source_id,experiment_id,table_id,variable_id,plot=False):
    """

    Parameters
    ----------
    start_year : int
        Start year of future 10-year period.
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    activity_id : string
        CMIP6 intercomparison project, e.g. 'ScenarioMIP'.
    institution_id : string
        ID of institution maintaining the selected CMIP6 model, e.g. 'NCC'.
    source_id : string
        CMIP6 model name and configuration, e.g. 'NorESM2-LM'.
    experiment_id : string
        CMIP6 modeling experiment ID, e.g. 'ssp585'.
    table_id : string
        Specifying what kind of data, e.g. 'Amon' for monthly mean.
    variable_id : string
        Abbreviation for the variable to be extracted, here 'tas' for
        near-surface air temperature.
    plot : bool, optional
        Whether to plot a map of the time-averaged near-surface air
        temperature. The default is False.

    Returns
    -------
    tas_nya_future_mean : xarray
        Time-averaged array of near-surface air temperature in 2D.

    """
    import rioxarray,geojson
    
    # GET AND PREPARE DATASET
    df_subset = df.query("activity_id==@activity_id & source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # df_subset = df.query("source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # print(df_subset)
    
    # get the path to a specific zarr store
    zstore = df_subset.zstore.values[-1]
    mapper = fs.get_mapper(zstore)

    # open using xarray
    ds = xr.open_zarr(mapper)#, consolidated=True)
    
    # transform lon coordinate from 0,360 to -180,180 and reorder the whole dataset:
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    # extract variable from Dataset (becomes then a DataArray):
    ds = ds[variable_id]
    
    
    # SELECT AREA
    # prepare DataArray for extraction of a certain geometry
    # (assign correct dimension names and Coordinate Reference System):    
    ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    ds.rio.write_crs("epsg:4326",inplace=True)  

    # select grid point closest to Ny-Ålesund
    # ta_nya = ds.sel(lat='78.95',lon='11.33',method='nearest')
    # OR
    # select data from outer WRF domain
    # (Obs: Domain geometry is currently hardcoded and not actually taken
    # from the met_em_file passed.)
    geometries = create_domain_geometry(met_em_file)[1]
    geometry_ds = geojson.loads(geometries)
    
    # Perform the clipping (keep only area given by geometries):    
    tas_nya = ds.rio.clip(geometries=[geometry_ds],crs="epsg:4326",drop=True)


    # SELECT TIME
    # select all November data from a ten-year period:
    start_time = str(start_year)+'-11-16T12:00:00'
    end_time = str(start_year+10)+'-11-16T12:00:00'
    tas_nya_future = tas_nya.sel(time=slice(start_time,end_time,12))
    # tas_nya_present = tas_nya.sel(time=slice('2015-11-16T12:00:00','2024-11-16T12:00:00',12))
    
    # TAKE TIME AVERAGE    
    tas_nya_future_mean = tas_nya_future.mean(dim='time')
    
    if plot==True:
        import matplotlib.pyplot as plt
        tas_nya_future_mean.plot()
        plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/tas_clipped_test.png")
        
    return tas_nya_future_mean
    
def present_GCM_ta_from_WRF_domain(met_em_file,activity_id,institution_id,source_id,experiment_id,table_id,variable_id,plot=False):
    """
    
    Parameters
    ----------
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    activity_id : string
        CMIP6 intercomparison project, e.g. 'ScenarioMIP'.
    institution_id : string
        ID of institution maintaining the selected CMIP6 model, e.g. 'NCC'.
    source_id : string
        CMIP6 model name and configuration, e.g. 'NorESM2-LM'.
    experiment_id : string
        CMIP6 modeling experiment ID, e.g. 'ssp585'.
    table_id : string
        Specifying what kind of data, e.g. 'Amon' for monthly mean.
    variable_id : string
        Abbreviation for the variable to be extracted, here 'ta' for
        atmospheric temperature.
    plot : bool, optional
        Whether to plot a map of the time-averaged near-surface air
        temperature. The default is False.

    Returns
    -------
    ta_nya_present_mean : xarray
        Time-averaged array of atmospheric temperature in 3D.

    """
    import rioxarray,geojson
    
    # GET AND PREPARE DATASET
    df_subset = df.query("activity_id==@activity_id & source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # df_subset = df.query("source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # print(df_subset)
    
    # get the path to a specific zarr store
    zstore = df_subset.zstore.values[-1]
    mapper = fs.get_mapper(zstore)

    # open using xarray
    ds = xr.open_zarr(mapper)#, consolidated=True)
    
    # transform lon coordinate from 0,360 to -180,180 and reorder the whole dataset:
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    # extract variable from Dataset (becomes then a DataArray):
    ds = ds[variable_id]
    # print(ds)
    
    # SELECT AREA
    # prepare DataArray for extraction of a certain geometry
    # (assign correct dimension names and Coordinate Reference System):    
    ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    ds.rio.write_crs("epsg:4326",inplace=True)  

    # select grid point closest to Ny-Ålesund
    # ta_nya = ds.sel(lat='78.95',lon='11.33',method='nearest')
    # OR
    # select data from outer WRF domain
    # (Caution: Domain geometry is currently hardcoded and not actually taken
    # from the met_em_file passed.)
    geometries = create_domain_geometry(met_em_file)[1]
    geometry_ds = geojson.loads(geometries)
    
    # Perform the clipping (keep only area given by geometries):    
    ta_nya = ds.rio.clip(geometries=[geometry_ds],crs="epsg:4326",drop=True)


    # SELECT TIME
    # select all November data from a ten-year period:    
    ta_nya_present = ta_nya.sel(time=slice('2015-11-16T12:00:00','2025-11-16T12:00:00',12))
    # print(tas_nya_present)
    
    # TAKE TIME AVERAGE    
    ta_nya_present_mean = ta_nya_present.mean(dim='time')
    
    if plot==True:
        import matplotlib.pyplot as plt
        ta_nya_present_mean.plot()
        plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/ta_clipped_test.png")
        
    return ta_nya_present_mean

def future_GCM_ta_from_WRF_domain(start_year,met_em_file,activity_id,institution_id,source_id,experiment_id,table_id,variable_id,plot=False):
    """

    Parameters
    ----------
    start_year : int
        Start year of future 10-year period.
    met_em_file : string
        Path to met_em file (intermediate WRF input file).
    activity_id : string
        CMIP6 intercomparison project, e.g. 'ScenarioMIP'.
    institution_id : string
        ID of institution maintaining the selected CMIP6 model, e.g. 'NCC'.
    source_id : string
        CMIP6 model name and configuration, e.g. 'NorESM2-LM'.
    experiment_id : string
        CMIP6 modeling experiment ID, e.g. 'ssp585'.
    table_id : string
        Specifying what kind of data, e.g. 'Amon' for monthly mean.
    variable_id : string
        Abbreviation for the variable to be extracted, here 'ta' for
        atmospheric temperature.
    plot : bool, optional
        Whether to plot a map of the time-averaged near-surface air
        temperature. The default is False.

    Returns
    -------
    ta_nya_future_mean : xarray
        Time-averaged array of atmospheric temperature in 3D.

    """
    import rioxarray,geojson
    
    # GET AND PREPARE DATASET
    df_subset = df.query("activity_id==@activity_id & source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # df_subset = df.query("source_id==@source_id & experiment_id==@experiment_id & table_id==@table_id & variable_id==@variable_id")
    # print(df_subset)
    
    # get the path to a specific zarr store
    zstore = df_subset.zstore.values[-1]
    mapper = fs.get_mapper(zstore)

    # open using xarray
    ds = xr.open_zarr(mapper)#, consolidated=True)
    
    # transform lon coordinate from 0,360 to -180,180 and reorder the whole dataset:
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    # extract variable from Dataset (becomes then a DataArray):
    ds = ds[variable_id]
    # print(ds)
    
    # SELECT AREA
    # prepare DataArray for extraction of a certain geometry
    # (assign correct dimension names and Coordinate Reference System):    
    ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    ds.rio.write_crs("epsg:4326",inplace=True)  

    # select grid point closest to Ny-Ålesund
    # ta_nya = ds.sel(lat='78.95',lon='11.33',method='nearest')
    # OR
    # select data from outer WRF domain
    # (Obs: Domain geometry is currently hardcoded and not actually taken
    # from the met_em_file passed.)
    geometries = create_domain_geometry(met_em_file)[1]
    geometry_ds = geojson.loads(geometries)
    
    # Perform the clipping (keep only area given by geometries):    
    ta_nya = ds.rio.clip(geometries=[geometry_ds],crs="epsg:4326",drop=True)


    # SELECT TIME
    # select all November data from a ten-year period:
    start_time = str(start_year)+'-11-16T12:00:00'
    end_time = str(start_year+10)+'-11-16T12:00:00'
    ta_nya_future = ta_nya.sel(time=slice(start_time,end_time,12))
    # tas_nya_present = tas_nya.sel(time=slice('2015-11-16T12:00:00','2024-11-16T12:00:00',12))
    
    # TAKE TIME AVERAGE    
    ta_nya_future_mean = ta_nya_future.mean(dim='time')
    
    if plot==True:
        import matplotlib.pyplot as plt
        ta_nya_future_mean.plot()
        plt.savefig("/nird/projects/NS9600K/brittsc/xxx.png")
        
    return ta_nya_future_mean

def get_warming_profile(ta_present,ta_future,model_area):
    """

    Parameters
    ----------
    ta_present : xarray
        Output from present_GCM_ta_from_WRF_domain.
    ta_future : xarray
        Output from future_GCM_ta_from_WRF_domain.
    model_area : xarray
        Output from get_area_per_grid_point.

    Returns
    -------
    warming_profile : xarray (float array)
        Warming profile averaged across the whole domain in 1D (vertical).

    """
    diff = ta_future-ta_present
        
    total_area = model_area.sum(dim=['lon','lat'],skipna=True)
    
    warming_profile = (((diff*model_area).sum(dim=['lon','lat'],skipna=True))/total_area).values
    
    return warming_profile


met_em_testfile = "/nird/projects/NS9600K/brittsc/xxx/met_em.d01.2019-11-11_12:00:00.nc"

start_year_warmed_period = 2047
start_year_hist_period = 1955

# NEAR-SURFACE TEMPERATURE

# NorESM2_present = present_GCM_tas_from_WRF_domain(met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'tas')
# print(NorESM2_present)

# NorESM2_future = future_GCM_tas_from_WRF_domain(start_year_warmed_period, met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'tas')
# print(NorESM2_future)

# NorESM2_historical = future_GCM_tas_from_WRF_domain(start_year_hist_period, met_em_testfile, 'CMIP', 'NCC', 'NorESM2-LM', 'historical', 'Amon', 'tas')


# area = get_area_per_grid_point(met_em_testfile)
# print(area)

# warming future period:
# print(calc_avg_surface_warming(NorESM2_present, NorESM2_future,area))

# p = (NorESM2_future-NorESM2_present).plot(
#     subplot_kws=dict(projection=ccrs.LambertConformal(central_longitude=12.0, central_latitude=39.0)),
#                       transform=ccrs.PlateCarree())
# p.axes.coastlines()
# plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/tas_diff_clipped_"+str(start_year_warmed_period)+".png")


# "cooling" historical period:
# print(calc_avg_surface_warming(NorESM2_present, NorESM2_historical, area))

# p = (NorESM2_historical-NorESM2_present).plot(
#     subplot_kws=dict(projection=ccrs.LambertConformal(central_longitude=12.0, central_latitude=39.0)),
#                      transform=ccrs.PlateCarree())
# p.axes.coastlines()
# plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/tas_diff_clipped_"+str(start_year_hist_period)+".png")


# ATMOSPHERIC PROFILE: calculate atmospheric warming profile from same period

# NorESM2_present_profile = present_GCM_ta_from_WRF_domain(met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'ta')

# NorESM2_future_profile = future_GCM_ta_from_WRF_domain(start_year_warmed_period,met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'ta')
# NorESM2_hist_profile = future_GCM_ta_from_WRF_domain(start_year_hist_period,met_em_testfile, 'CMIP', 'NCC', 'NorESM2-LM', 'historical', 'Amon', 'ta')

# print(get_warming_profile(NorESM2_present_profile, NorESM2_future_profile, area))
# print(get_warming_profile(NorESM2_present_profile, NorESM2_hist_profile, area))


# SURFACE (SKIN AND SEA) TEMPERATURE

present_surface_temp = present_GCM_tas_from_WRF_domain(met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'ts')
# print(present_surface_temp)

future_surface_temp = future_GCM_tas_from_WRF_domain(start_year_warmed_period, met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'ts')
# hist_surface_temp = future_GCM_tas_from_WRF_domain(start_year_hist_period, met_em_testfile, 'CMIP', 'NCC', 'NorESM2-LM', 'historical', 'Amon', 'ts')

area = get_area_per_grid_point(met_em_testfile)

print(calc_avg_surface_warming(present_surface_temp, future_surface_temp,area))

p = (future_surface_temp-present_surface_temp).plot(
    subplot_kws=dict(projection=ccrs.LambertConformal(central_longitude=12.0, central_latitude=39.0)),
                      transform=ccrs.PlateCarree())
p.axes.coastlines()
plt.savefig("/nird/projects/NS9600K/brittsc/xxx/plot/ts_diff_clipped_"+str(start_year_warmed_period)+".png")



# SOIL TEMPERATURE

# present_soil_temp = present_GCM_tas_from_WRF_domain(met_em_testfile, 'ScenarioMIP', 'NCC', 'NorESM2-LM', 'ssp585', 'Amon', 'mrsol')
# print(present_soil_temp)


# print(df['experiment_id'].unique())
# print(df['variable_id'].unique())
# print(df['institution_id'].unique())
