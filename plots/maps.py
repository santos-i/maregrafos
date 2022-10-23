import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from urllib.request import urlopen
import pandas as pd


def rjMap(tideGauges):    
    
    url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
    with urlopen(url) as response:
        brazil = json.load(response)
    
    state_id_map = {}
    for feature in brazil['features']:
        feature['id'] = feature['properties']['name']
        state_id_map[feature['properties']['sigla']] = feature['id']
    
    estado = ['Rio de Janeiro']
    unit = [0]
    df = pd.DataFrame()
    df['estado'] = estado
    df['unit'] = unit
    
    fig = px.choropleth(df,
        locations = df['estado'], #define the limits on the map/geography
        geojson = brazil, #shape information
        color = df['unit'], #defining the color of the scale through the database
        color_continuous_scale="Blues",
        hover_name=['Rio de Janeiro'],
        hover_data={'estado':False, 'unit':False},
    )
    
    fig.update_geos(fitbounds = "locations", visible = False)

    for tideG in tideGauges:
        fig.add_trace(
            go.Scattergeo(
                lat = [tideG.lat],
                lon = [tideG.lon],
                mode = 'markers+text',
                text = [f"<a href='tideGauge{tideG.id}' target='_self'>  </a>"],
                textposition="middle center",
                marker = dict(
                    color = 'red',
                    size=10,
                ),
                hovertemplate=
                f"<b>Maregrafo de {tideG.name}</b><br>" +
                "última medição: 12:50<br>" +
                "Temperatura: 21ºC <br>" +
                "Altura: 0.5m" +
                "<extra></extra>",
            )
        )
    
    fig.update_layout(
        coloraxis_showscale=False,
        autosize=False,
        width=1300,
        margin=dict(l=1, r=1, t=10, b=10),
        showlegend=False
        )

    mapa = fig.to_html(full_html=False, div_id='tideGaugesMap',config= dict(
            displayModeBar = False))
    with open('plots/mapa.txt', 'w') as f:
        f.write(mapa)



def dataGraphs(dataTide):
    df = pd.DataFrame()
    temp, nivel, timestamp = [],[],[]
    for data in dataTide:
        temp.append(data.temp)
        nivel.append(data.nivel)
        timestamp.append(data.timeStamp)

    if len(temp) > 0:
        df['temp'] = temp
        df['nivel'] = nivel
        df['tsp'] = timestamp

        df.set_index('tsp')


        temp_fig = px.line(df, x=df.index, y=df['temp']) 
        tide_fig = px.line(df, x=df.index, y=df['nivel']) 
        
        tempGraph = temp_fig.to_html(full_html=False,config= dict(displayModeBar = False))
        tideGraph = tide_fig.to_html(full_html=False,config= dict(displayModeBar = False))
        
        with open(f'plots/temp{data.tideGauge_id}.txt', 'w') as f:
            f.write(tempGraph)
        
        with open(f'plots/tide{data.tideGauge_id}.txt', 'w') as f:
            f.write(tideGraph)

