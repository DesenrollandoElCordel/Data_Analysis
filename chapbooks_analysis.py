import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
from shapely import wkt

cluster = pd.read_csv('IndexChapbooksAll.csv')
# print(cluster.head())

# Répartition des documents par date
histoDate = px.histogram(cluster, x="date", text_auto=True, title="Répartition par date",
                         labels={'date': 'Date'}, color_discrete_sequence=['ForestGreen'])
histoDate.update_layout(bargap=0.1)
# histoDate.show()
# histoDate.write_html('html/01-ChapbooksPerDate.html', auto_open=True)

# Villes qui apparaissent le plus dans le corpus
cluster['city_count'] = cluster.groupby('ville')['id'].transform('count')
cluster.sort_values(by=['city_count'], ascending=False, inplace=True)
cluster_cityMax = cluster[cluster['city_count'] >= 10]
pieCityMax = px.pie(cluster_cityMax, names="ville",
                    title="Villes les plus représentées dans le corpus genevois (>= 10)")
# pieCityMax.show()
# pieCityMax.write_html('html/02-CitiesMax.html', auto_open=True)

# Villes qui apparaissent le moins dans le corpus
cluster_cityMin = cluster[cluster['city_count'] < 10]
pieCityMin = px.pie(cluster_cityMin, names="ville",
                    title="Villes les moins représentées dans le corpus genevois (< 10)")
# pieCityMin.show()
# pieCityMin.write_html('html/03-CitiesMin.html', auto_open=True)

# Projection sur une carte
cluster['wkt'] = cluster['wkt'].astype("string")
cluster['wkt'] = cluster.wkt.apply(wkt.loads)
gdf = gpd.GeoDataFrame(cluster, geometry='wkt')
gdf['lon'] = gdf['wkt'].x
gdf['lat'] = gdf['wkt'].y

carte = px.scatter_geo(gdf, lat="lat", lon="lon",
                     hover_name="ville", size="city_count",
                     projection="natural earth", color="city_count")
carte.update_layout(
    title="Répartition géographique du corpus genevois",
    geo=dict(scope='europe'))
# carte.show()
# carte.write_html('html/04-CitiesMap.html', auto_open=True)

# Imprimeurs les plus représentés dans le corpus
cluster['printer_count'] = cluster.groupby('imprimeur')['id'].transform('count')
cluster.sort_values(by=['printer_count'], ascending=False, inplace=True)
cluster_printerMax = cluster[cluster['printer_count'] >= 10]
PrinterPieMax = px.pie(cluster_printerMax, names="imprimeur",
                    title="Imprimeurs les plus représentés dans le corpus (plus de 10 documents)")
# PrinterPieMax.show()
# PrinterPieMax.write_html('html/05-MainPrinters.html', auto_open=True)

# Répartition par date et par imprimeur
histoDatePrinter = make_subplots(rows=1, cols=2,
                                 subplot_titles=("José María Moreno", "José María Marés"))
MorenoCluster = cluster.query("imprimeur == 'José María Moreno'")
MaresCluster = cluster.query("imprimeur == 'José María Marés'")

histoDatePrinter.add_trace(
    go.Histogram(x=MorenoCluster["date"]),
    row=1, col=1
)
histoDatePrinter.add_trace(
    go.Histogram(x=MaresCluster["date"]),
    row=1, col=2
)
histoDatePrinter.update_layout(height=600, width=800,
                               title_text="Activité des imprimeurs dans le corpus genevois")
# histoDatePrinter.show()
# histoDatePrinter.write_html('html/06-PrintersActivities.html', auto_open=True)

# Répartition par nombre de pages
pagePie = px.pie(cluster, names="nb_page", title="Nombre de pages par documents")
# pagePie.show()
# pagePie.write_html('html/07-PageNumber.html', auto_open=True)

# [Corpus Moreno] Types de texte les plus représentés
cluster['typeText_count'] = cluster.groupby('type_texte')['id'].transform('count')
cluster.sort_values(by=['typeText_count'], ascending=False, inplace=True)
cluster_typeTextMax = cluster[cluster['typeText_count'] >= 10]
histoTypeTextMax = px.pie(cluster_typeTextMax, names="type_texte",
                       title="Types de texte les plus présents dans le corpus Moreno")
# histoTypeTextMax.show()
# histoTypeTextMax.write_html('html/08-MorenoTypeTextMax.html', auto_open=True)

# [Corpus Moreno] Types de texte les moins représentés
cluster_typeTextMin = cluster[cluster['typeText_count'] < 10]
histoTypeTextMin = px.pie(cluster_typeTextMin, names="type_texte",
                       title="Types de texte les moins représentés dans le corpus Moreno")
# histoTypeTextMin.show()
# histoTypeTextMin.write_html('html/09-MorenoTypeTextMin.html', auto_open=True)

# [Corpus Moreno] Chronologie des types de texte les plus représentés
histoDateText = make_subplots(rows=3, cols=2,
                                 subplot_titles=("Romances", "Relaciones", "Pasillos", "Sainetes", "Coplas", "Trovos"))
RomancesClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Romances'")
RelacionesClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Relaciones'")
PasillosClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Pasillos'")
SainetesClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Sainetes'")
CoplasClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Coplas'")
TrovosClusterM = cluster.query("imprimeur == 'José María Moreno'").query("type_texte == 'Trovos'")

histoDateText.add_trace(
    go.Histogram(x=RomancesClusterM["date"]),
    row=1, col=1
)
histoDateText.add_trace(
    go.Histogram(x=RelacionesClusterM["date"]),
    row=1, col=2
)
histoDateText.add_trace(
    go.Histogram(x=PasillosClusterM["date"]),
    row=2, col=1
)
histoDateText.add_trace(
    go.Histogram(x=SainetesClusterM["date"]),
    row=2, col=2
)
histoDateText.add_trace(
    go.Histogram(x=CoplasClusterM["date"]),
    row=3, col=1
)
histoDateText.add_trace(
    go.Histogram(x=TrovosClusterM["date"]),
    row=3, col=2
)

histoDateText.update_layout(height=600, width=800,
                               title_text="Chronologie des types de texte (Corpus Moreno)")
# histoDateText.show()
histoDateText.write_html('html/10-MorenoTextThroughTime.html', auto_open=True)
