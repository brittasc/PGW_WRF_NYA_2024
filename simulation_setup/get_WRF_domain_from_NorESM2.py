from netCDF4 import Dataset
import numpy as np

def get_domain_polygon(met_em_file):
    """
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
    print(data)
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

def create_domain_geometry(polygon):
    """
    Parameters
    ----------
    polygon : numpy array
        Output from get_domain_polygon.

    Returns
    -------
    None.
    """
    
    import geopandas
    # import rioxarray
    
    # geometry = geopandas.points_from_xy([lon_1,lon_2,lon_3,lon_4], [lat_1,lat_2,lat_3,lat_4], crs = "epsg:4326")
    # print(geometry)
    geometries = [
        {'type': 'Polygon',
        'coordinates': [    polygon      ]}
        ]
    print(geometries)


met_em_testfile = "/nird/projects/NS9600K/brittsc/xxx/met_em.d01.2019-11-11_12:00:00.nc"
poly = get_domain_polygon(met_em_testfile)

create_domain_geometry(poly)
