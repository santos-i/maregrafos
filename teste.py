

def testando():    
    import plotly as plt
    import plotly.express as px
    import plotly.graph_objects as go
    import json
    from urllib.request import urlopen
    import pandas as pd
    
    
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

    d = {'lon': [-41.882242, -46.382242], 'lat': [-22.972739, -23.072739]}
    df = pd.DataFrame(data=d)

    for index, row in df.iterrows():
        fig.add_trace(
            go.Scattergeo(
                # lon = [-41.882242, -43.182242],
                # lat = [-22.372739, -22.972739],
                lat = [row['lat']],
                lon = [row['lon']],
                mode = 'markers+text',
                text = [f"<a href='maregrafo-{index}' target='_self'>  </a>"],
                textposition="middle center",
                marker = dict(
                    color = 'red',
                    size=10,
                ),
                hovertemplate=
                f"<b>Maregrafo {index}</b><br>" +
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

    mapa = fig.to_html(full_html=False, div_id='maregrafosMap',config= dict(
            displayModeBar = False))

    return mapa 


