# Pandas for data management
import pandas as pd

# Bokeh basics 
from bokeh.io import curdoc, save

import geopandas as gpd
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)

from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from scripts.chloropleth import *
from bokeh.layouts import column, row, WidgetBox
import json

from bokeh.plotting import figure

vaccines = ['BCG','DTP1','DTP3','HEPB3','HEPBB','HIB3','IPV1','MCV1','MCV2','PCV3','POL3','RCV1','ROTAC','YFV']



def createDashboard():
    print ("in createdashboard")

    print (" vaccines =  : \n", vaccines)

    immun_df = pd.read_excel('bokeh-dashboard/data/immunization2019.xls', sheet_name = vaccines)

    all_df = pd.concat(immun_df, axis=0, ignore_index=True)

    print ("immun_df \n", immun_df)
    print("ALL DF \n", all_df)

    print (" Loading shapefile : \n")

    shapefile = 'bokeh-dashboard/data/ne_110m_admin_0_countries.shp'
    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    #Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']
    #Drop row corresponding to 'Antarctica'
    gdf = gdf.drop(gdf.index[159])

    geodata = gdf.merge(all_df, left_on='country_code', right_on='iso3', how='left')

    tab1 = chloropleth(geodata)

    # Put all the tabs into one application
    #tabs = Tabs(tabs = [tab1]) #, tab3, tab4, tab5])

    # Put the tabs in the current document for display
    curdoc().add_root(tab1)

#if __name__ == '__main__':
#    print ("in Main")
createDashboard()