import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from bs4 import BeautifulSoup

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")


# streamlit run D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\Home.py
# https://streamlit.io/
# pipreqs --encoding utf-8 "D:\Dropbox\Empresa\Buydepa\PROYECTOS\APPCOLOMBIA"

st.cache_data()
def getdata(yy):
    path = "data/BogotaGrid.shp"
    path = r"D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\data\BogotaGrid.shp"
    datamap = gpd.read_file(path,encoding = 'utf-8')
    
    path = r"D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\data\data_transacciones"
    data = pd.read_pickle(path)
    
    variable  = 'color_transacciones' #['color_proporcion','color_transacciones']
    datayy    = data[data['year']==yy]
    datamapyy = datamap.merge(datayy[['id_map',variable]],on='id_map',how='left',validate='1:1')
    datamapyy = datamapyy[datamapyy[variable].notnull()]
    
    path         = r'D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\data\data_analisis'
    datagraficas = pd.read_pickle(path)
    datagraficas = datagraficas[datagraficas['year']==yy]

    datapredios = pd.read_pickle(r'D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\data\data_predios')
    datapredios = datamap.merge(datapredios,on='id_map',how='left',validate='1:1')
    datapredios = datapredios[datapredios['color'].notnull()]
    
    dataventas = pd.read_pickle(r'D:\Dropbox\Empresa\Buydepa\COLOMBIA\ANALISIS_MERCADO\app\data\data_oferta')

    return datamap,data,datamapyy,datagraficas,datapredios,dataventas

def style_function(feature):
    return {
        "fillColor": feature["properties"]["color_transacciones"],
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    }

def style_function_sp(feature):
    return {
        "fillColor": feature["properties"]["color"],
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    }

datamap,data,datamapyy,datagraficas,datapredios,dataventas = getdata(2023)

latitud  =  4.688637
longitud = -74.054521


html = """
<!DOCTYPE html>
<html>
<head>
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet" />
  <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
</head>
<body>
<div class="container-fluid py-4">
  <div class="row" style="margin-bottom: -30px;">
    <div class="card-body p-3">
      <div class="row">
        <div class="numbers">
          <h3 class="font-weight-bolder mb-0" style="text-align: center; font-size: 1.5rem;border-bottom: 0.5px solid #ccc; padding-bottom: 8px;">Trasnacciones depas 2023</h3>
        </div>
      </div>
    </div>
  </div>
</div>   
</body>
</html>
"""
texto = BeautifulSoup(html, 'html.parser')
st.markdown(texto, unsafe_allow_html=True)

m = folium.Map(location=[latitud, longitud], zoom_start=11,tiles="cartodbpositron")
folium.GeoJson(datamapyy,style_function=style_function).add_to(m)
st_map = st_folium(m,width=2000,height=800)


html = """
<!DOCTYPE html>
<html>
<head>
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet" />
  <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
</head>
<body>
<div class="container-fluid py-4">
  <div class="row" style="margin-bottom: -30px;">
    <div class="card-body p-3">
      <div class="row">
        <div class="numbers">
          <h3 class="font-weight-bolder mb-0" style="text-align: center; font-size: 1.5rem;border-bottom: 0.5px solid #ccc; padding-bottom: 8px;">Sweet spot</h3>
        </div>
      </div>
    </div>
  </div>
</div>   
</body>
</html>
"""
texto = BeautifulSoup(html, 'html.parser')
st.markdown(texto, unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    df               = datagraficas[datagraficas['variable']=='estrato']
    df.index         = range(len(df))
    df['porcentaje'] = df['porcentaje']*100
    indice           = df["porcentaje"].idxmax()
    fig              = px.bar(df, x="label", y="porcentaje", text="porcentaje", title="Transacciones por estrato")
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside', marker_color=['#98ff96' if i == indice else '#3A5AFF' for i in range(len(df))])
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)
    
with col2:
    df               = datagraficas[datagraficas['variable']=='cuantia']
    df.index         = range(len(df))
    df['porcentaje'] = df['porcentaje']*100
    indice           = df["porcentaje"].idxmax()
    fig              = px.bar(df, x="label", y="porcentaje", text="porcentaje", title="Transacciones por Valor del inmueble")
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside', marker_color=['#98ff96' if i == indice else '#3A5AFF' for i in range(len(df))])
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)   
    
    
with col1:
    df               = datagraficas[datagraficas['variable']=='areaconstruida']
    df.index         = range(len(df))
    df['porcentaje'] = df['porcentaje']*100
    indice           = df["porcentaje"].idxmax()
    fig              = px.bar(df, x="label", y="porcentaje", text="porcentaje", title="Transacciones por Area construida")
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside', marker_color=['#98ff96' if i == indice else '#3A5AFF' for i in range(len(df))])
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)
    
with col2:
    df               = datagraficas[datagraficas['variable']=='tiempodeconstruido']
    df.index         = range(len(df))
    df['porcentaje'] = df['porcentaje']*100
    indice           = df["porcentaje"].idxmax()
    fig              = px.bar(df, x="label", y="porcentaje", text="porcentaje", title="Transacciones por Tiempo de construido")
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside', marker_color=['#98ff96' if i == indice else '#3A5AFF' for i in range(len(df))])
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)   
    
    
html = """
<!DOCTYPE html>
<html>
<head>
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet" />
  <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet" />
  <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
</head>
<body>
<div class="container-fluid py-4">
  <div class="row" style="margin-bottom: -30px;">
    <div class="card-body p-3">
      <div class="row">
        <div class="numbers">
          <h3 class="font-weight-bolder mb-0" style="text-align: center; font-size: 1.5rem;border-bottom: 0.5px solid #ccc; padding-bottom: 8px;">Depas en el sweet spot</h3>
        </div>
      </div>
    </div>
  </div>
</div>   
</body>
</html>
"""
texto = BeautifulSoup(html, 'html.parser')
st.markdown(texto, unsafe_allow_html=True)

col1, col2 = st.columns([5,1])
with col1:

    m = folium.Map(location=[latitud, longitud], zoom_start=11,tiles="cartodbpositron")
    folium.GeoJson(datapredios,style_function=style_function_sp).add_to(m)
    st_map = st_folium(m,width=2000,height=800)


with col2: 
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet" />
      <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet" />
      <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
    </head>
    <body>
 
    <div class="container-fluid py-1">
      <div class="card" style="margin-bottom:20px">
        <div class="card-body p-4">
          <div class="row">
            <div class="col-xl-6 col-sm-0 mb-xl-4 mb-0">
              <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 3rem;">{int(datapredios['predios'].sum())}</h3>
            </div>              
          </div>
          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.2rem;color:grey;">Censo de depas</h3>
        </div>
      </div>
    </div>
    <div class="container-fluid py-1">
      <div class="card" style="margin-bottom:20px">
        <div class="card-body p-4">
          <div class="row">
            <div class="col-xl-6 col-sm-0 mb-xl-4 mb-0">
              <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 3rem;">{len(dataventas)}</h3>
            </div>              
          </div>
          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.2rem;color:grey;">Depas en oferta</h3>
        </div>
      </div>
    </div>
    </body>
    </html>
    """
    texto = BeautifulSoup(html, 'html.parser')
    st.markdown(texto, unsafe_allow_html=True)