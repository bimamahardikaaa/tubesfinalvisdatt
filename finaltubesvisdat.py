# -*- coding: utf-8 -*-
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Category20_16
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import show
from bokeh.io import curdoc
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

# Read data
temp = pd.read_csv("./data/covid19indonesia.csv")

# Mengubah nilai kolom date dari object menjadi datetime
temp["Date"] = pd.to_datetime(temp["Date"])
temp

# Mendrop baris indonesia
data = temp[temp["Location"].str.contains("Indonesia")==False]

# Mengambil data yang diperlukan
data = data[['Date', 'Location', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']]
data

# Membuat list untuk location
lokasi = list(data.Location.unique())

# Membuat list tiap kolom
col_list = list(data.columns)

# Method untuk pembuatan dataset yang akan di select nanti
def buat_dataset(lokasi, feature):
    x_list = []
    y_list = []
    colors = []
    labels = []

    for i, lokasi in enumerate(lokasi):

        df = data[data['Location'] == lokasi].reset_index(drop = True)
        
        x = list(df['Date'])
        y = list(df[feature])
        
        x_list.append(list(x))
        y_list.append(list(y))

        colors.append(Category20_16[i])
        labels.append(lokasi)

    new_src = ColumnDataSource(data={'x': x_list, 'y': y_list, 'color': colors, 'label': labels})

    return new_src

# Method untuk pembuatan multiple line plot yang akan di select nanti
def buat_plot(src, feature):
    
    p = figure(plot_width = 700, plot_height = 400, 
            title = 'Covid19-Indonesia All Time Series',
            x_axis_label = 'Date', y_axis_label = 'Feature Selected')

    p.multi_line('x', 'y', color = 'color', legend_field = 'label', line_width = 2, source = src)

    tooltips = [
            ('Date','$x'),
            ('Total', '$y'),
           ]
           
    p.add_tools(HoverTool(tooltips=tooltips)) #hover

    return p

# Method callback untuk interaktif checkbox
def update_lokasi(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]

    new_src = buat_dataset(lokasi_plot, feature_select.value)

    src.data.update(new_src.data)

# Method callback untuk interaktif dropdown
def update_fitur(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]
    
    feature = feature_select.value
    
    new_src = buat_dataset(lokasi_plot, feature)

    src.data.update(new_src.data)

# Pembuatan checkboxgroup berdasarkan provinsi/lokasi
lokasi_selection = CheckboxGroup(labels=lokasi, active = [0])
lokasi_selection.on_change('active', update_lokasi)

# Pembuatan fitur select dropdown
feature_select = Select(options = col_list[2:], value = 'Total Cases', title = 'Feature Select')
feature_select.on_change('value', update_fitur)

lokasi_now = [lokasi_selection.labels[i] for i in lokasi_selection.active]

src = buat_dataset(lokasi_now, feature_select.value)

# Pemanggilan method plot
p = buat_plot(src, feature_select.value)

# Pemasangan widget untuk interaktive visualisasi
controls = WidgetBox(feature_select, lokasi_selection)

layout = row(controls, p)

curdoc().add_root(layout)
