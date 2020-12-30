import pandas as pd
import geopandas as gpd

from scripts.chloropleth import *

vaccines = ['BCG','DTP1','DTP3','HEPB3','HEPBB','HIB3','IPV1','MCV1','MCV2','PCV3','POL3','RCV1','ROTAC','YFV']

def createDashboard():

    immun_df = pd.read_excel('bokeh-dashboard/data/immunization2019.xls', sheet_name = vaccines)

    all_df = pd.concat(immun_df, axis=0, ignore_index=True)

    shapefile = 'bokeh-dashboard/data/ne_110m_admin_0_countries.shp'
    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    #Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']
    #Drop row corresponding to 'Antarctica'
    gdf = gdf.drop(gdf.index[159])

    geodata = gdf.merge(all_df, left_on='country_code', right_on='iso3', how='left')

    tab1 = chloropleth(geodata)

    # Put the tab in the current document for display
    curdoc().add_root(tab1)


createDashboard()

