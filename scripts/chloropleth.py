
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
from bokeh.layouts import column, row, WidgetBox
import json

from bokeh.plotting import figure
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox



def chloropleth(geodata):
    vaccines = ['BCG', 'DTP1', 'DTP3', 'HEPB3', 'HEPBB', 'HIB3', 'IPV1', 'MCV1', 'MCV2', 'PCV3', 'POL3', 'RCV1',
                'ROTAC', 'YFV']
    initial_year = 1980
    active_vaccine_idx = [7]

    title = 'Immunization % for the year 1980'

    def df2json(df):
        print("in df2json")
        merged_json = json.loads(df.to_json())
        #merged_json = json.loads(df)
        json_data = json.dumps(merged_json)
        return json_data

    def make_chloropleth(geosource):
        print("in make_chloropleth : geosource = \n", geosource)

        palette = brewer['YlGnBu'][8]
        # Reverse color order so that dark blue is highest immunization.
        palette = palette[::-1]
        tick_labels = {'0': '0%', '10': '10%', '20': '20%', '30': '30%', '40': '>40%', '50': '50%', '60': '60%',
                       '70': '70%', '80': '80%', '90': '90%', '100': '100%'}
        color_mapper = LinearColorMapper(palette=palette, low=0, high=100, nan_color='#d9d9d9')
        hover = HoverTool(tooltips=[('Country/region', '@iso3'), ('Immunization %', '@year'), ('Vaccine', '@vaccine')])

        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                             border_line_color=None, location=(0, 0), orientation='horizontal',
                             major_label_overrides=tick_labels)

        p = figure(title= title, plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        # Specify layout
        p.patches('xs', 'ys', source=geosource, fill_color={'field': 'year', 'transform': color_mapper},
                  line_color='black', line_width=0.25, fill_alpha=1)

        p.add_layout(color_bar, 'below')

        return p

    def make_dataset(active_vaccines, selected_year = initial_year):
        display_dataset = geodata[geodata['vaccine'].isin( active_vaccines )].copy()
        print ('selected_year = ', selected_year)
        display_dataset['year'] = geodata[str(selected_year)].copy()
        print('display_dataset = ', display_dataset['year'] )
        #return ColumnDataSource(display_dataset)
        geosource = GeoJSONDataSource(geojson=df2json(display_dataset))
        return geosource

    def update(attr, old, new):
        print('In update')
        if len (vaccine_selection.active) == 0:
            vaccine_selection.active = [7]
        else:
            vaccines_to_plot = [vaccine_selection.labels[i] for i in vaccine_selection.active]

            new_src = make_dataset(vaccines_to_plot,
                                   selected_year=year_select.value)
            #print('OLD SRC : \n ', src.head())
            #src.update(new_src)
            #print('NEW SRC : \n ', new_src)
            #geosource = GeoJSONDataSource(geojson=df2json(new_src))
            p = make_chloropleth(new_src)
            p.title.text = f'Immunization % for the year {year_select.value}'
            layout = row(vaccine_selection, p, year_select)
            #tab = Panel(child=layout, title='GeoData')
            curdoc().clear()
            curdoc().add_root(layout)

    vaccine_selection = CheckboxGroup(labels=vaccines, orientation='vertical',
                                      active=active_vaccine_idx)

    vaccine_selection.on_change('active', update)

    year_select = Slider(start=1980, end=2019,  orientation='vertical',
                             step=1, value=initial_year,
                             title='Year')

    year_select.on_change('value', update)
    initial_vaccine = [vaccine_selection.labels[i] for i in vaccine_selection.active]

    src = make_dataset(initial_vaccine, year_select.value)

    p = make_chloropleth(src)
    layout = row(vaccine_selection, p, year_select)

    tab = Panel(child= layout, title='GeoData')

    return layout

