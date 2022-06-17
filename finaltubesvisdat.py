# Kelompok 7 Tubes Visdat
# Anggota : 
# 1. Bima Mahardika Wirawan 1301194304
# 2. Muhammad Rifqi Arrahim 1301190425 
# 3. Aini Nasywa 130

import pandas as pd
from bokeh.plotting import figure
from bokeh.plotting import show
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
from bokeh.layouts import column, row, WidgetBox

# Melakukan pembacaan data
indekscovid = pd.read_csv("./data/covid19indonesia.csv")

# Mengubah nilai dari kolom date dari object menjadi datetime
indekscovid["Date"] = pd.to_datetime(indekscovid["Date"])
indekscovid

# Melakukan drop baris pada indonesia
datacovid = indekscovid[indekscovid["Location"].str.contains("Indonesia")==False]

# Mengambil data yang diperlukan
datacovid = datacovid[['Date', 'Location', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']]
datacovid

# Membuat list untuk location yang ada
lokasi = list(datacovid.Location.unique())

# Membuat list tiap kolom yang ada
col_list = list(datacovid.columns)

# Method untuk pembuatan dataset yang akan di select nanti
def buatdataset(lokasi, feature):
    list_x = []
    list_y = []
    colors = []
    labels = []

    for i, lokasi in enumerate(lokasi):

        op = datacovid[datacovid['Location'] == lokasi].reset_index(drop = True)
        
        x = list(op['Date'])
        y = list(op[feature])
        
        list_x.append(list(x))
        list_y.append(list(y))

        colors.append(Category20_16[i])
        labels.append(lokasi)

    new_src = ColumnDataSource(datacovid={'x': list_x, 'y': list_y, 'color': colors, 'label': labels})

    return new_src

# Method untuk pembuatan multiple line plot yang akan di select nanti
def buatplot(src, feature):
    
    c = figure(plot_width = 700, plot_height = 400, 
            title = 'Covid19-Indonesia',
            x_axis_label = 'Date', y_axis_label = 'Feature Selected')

    c.multi_line('x', 'y', color = 'color', legend_field = 'label', line_width = 2, source = src)

    tooltips = [
            ('Date','$x'),
            ('Total', '$y'),
           ]
           
    c.add_tools(HoverTool(tooltips=tooltips)) # Melakukan hover

    return c

# Method callback untuk interaktif checkbox
def updatelokasi(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]

    new_src = buatdataset(lokasi_plot, feature_select.value)

    src.datacovid.update(new_src.datacovid)

# Method callback untuk interaktif dropdown
def updatefitur(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]
    
    feature = feature_select.value
    
    new_src = buatdataset(lokasi_plot, feature)

    src.datacovid.update(new_src.datacovid)

# Pembuatan checkboxgroup berdasarkan pada provinsi/lokasi
lokasi_selection = CheckboxGroup(labels=lokasi, active = [0])
lokasi_selection.on_change('active', updatelokasi)

# Pembuatan fitur select dropdown 
feature_select = Select(options = col_list[2:], value = 'Total Cases', title = 'Feature Select')
feature_select.on_change('value', updatefitur)

lokasi_now = [lokasi_selection.labels[i] for i in lokasi_selection.active]

src = buatdataset(lokasi_now, feature_select.value)

# Pemanggilan method plot
c = buatplot(src, feature_select.value)

# Pemasangan widget untuk interaktive visualisasi data covid
controls = WidgetBox(feature_select, lokasi_selection)

layout = row(controls, c)

curdoc().add_root(layout)
