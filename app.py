import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import MinMaxScaler


url_dataset = './assets/weather_dataset.csv'

df = pd.read_csv(url_dataset)

# create dictionary of list
location_dict = df[['Location', 'Lat', 'Lon']]
list_location = location_dict.set_index('Location')[['Lat', 'Lon']].T.to_dict('dict')

# create dictionary of list agriculture
agri_dict = df[['Location', 'Agriculture']]
list_agri = agri_dict.set_index('Location')[['Agriculture']].T.to_dict('dict')

# Converting date column from string to proper date format
df['DateTime'] = pd.to_datetime(df['DateTime'])

app = dash.Dash(__name__)
# app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo.png'),
                     id='corona-image',
                     style={
                         "height": "100px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("Weather Analysis", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Temperature Forecast in VietNam", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6("Last Updated: " + df['DateTime'].iloc[-1].strftime("%B %d, %Y"),
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='Average Temperature',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{df['Temp'].mean():,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Period',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P("Start: " + df['DateTime'].iloc[0].strftime("%B %d, %Y"),
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 20}
                   ),

            html.P("End: " + df['DateTime'].iloc[-1].strftime("%B %d, %Y"),
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 20}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Maximum Temperature',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{df['Temp'].max():,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Minimum Temperature ',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{df['Temp'].min():,.2f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   )], className="card_container three columns")

    ], className="row flex-display"),

    html.Div([
        html.Div([dcc.Graph(
                        id='sunburst-graph',
                        figure=px.sunburst(
                            df,
                            path=['Region', 'Location'],
                            values='Temp',
                            height=500,
                            color='Temp',
                            color_continuous_scale='thermal',
                            color_continuous_midpoint=np.mean(df['Temp']),
                            labels={'Temp': 'Temperature (°C)'},
                        )),
                              ], className="create_container four columns"),
        html.Div([
            dcc.Graph(
                id='scatter-mapbox',
                figure=go.Figure(px.scatter_mapbox(
                    df,
                    lat="Lat",
                    lon="Lon",
                    color="Temp",
                    color_continuous_scale=px.colors.cyclical.IceFire,
                    hover_name='Location',
                    labels={
                        'Lat': 'Latitude',
                        'Lon': 'Longitude',
                        'Temp': 'Temperature (°C)',
                    },
                    height=600,
                    # width=1300
                )).update_layout(
                    mapbox_style='open-street-map',
                    title="Temperature Map",
                    hovermode='closest',
                    mapbox=dict(
                        bearing=0,
                        center=go.layout.mapbox.Center(
                            lat=16.5,
                            lon=110
                        ),
                        pitch=0,
                        zoom=4
                    )))
        ], className="create_container five columns")
            ], className="row flex-display"),
    
    html.Div([
        html.Div([

                    html.P('Select Country:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='w_countries',
                                  multi=False,
                                  clearable=True,
                                  value='AnGiang',
                                  placeholder='Select Countries',
                                  options=[{'label': c, 'value': c}
                                           for c in (df['Location'].unique())], className='dcc_compon'),

                    #  html.P('New Cases : ' + '  ' + ' ' + str(covid_data_2['date'].iloc[-1].strftime("%B %d, %Y")) + '  ', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
                    #  dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon',
                    #  style={'margin-top': '20px'},
                    #  ),

                    #   dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc_compon',
                    #   style={'margin-top': '20px'},
                    #   ),

                    #   dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc_compon',
                    #   style={'margin-top': '20px'},
                    #   ),

                    #   dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                    #   style={'margin-top': '20px'},
                    #   ),

        ], className="create_container three columns", id="cross-filter-options"),

        html.Div([
            html.H6(children='Coordinates',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(id='long_content',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 20}
                   ),
            html.P(id='lat_content',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 20}
                   )], className="create_container three columns",
        ),
        html.Div([
            html.H6(children='Agriculture',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(id='agri_content',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   )], className="create_container three columns",
        ),
           
        ], className="row flex-display"),

html.Div([
        html.Div([
            dcc.Graph(id="line_chart")], className="create_container1 twelve columns"),

            ], className="row flex-display"),
html.Div([
        html.Div([
            dcc.Graph(id="polar_scatter_plot")], className="create_container nine columns"),
        html.Div([
            dcc.Graph(id="humidity_plot")], className="create_container nine columns"),

            ], className="row flex-display"),
html.Div([
        html.Div([
            dcc.Graph(id="spider_chart")], className="create_container1 twelve columns"),

            ], className="row flex-display"),
    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})

#Update long coordinates
@app.callback(
    Output('long_content', 'children'),
    [Input('w_countries', 'value')])

def update_text_content(w_countries):
    text = "Longitude: " + str(list_location[w_countries]['Lon'])
    return text
#Update lat coordinates
@app.callback(
    Output('lat_content', 'children'),
    [Input('w_countries', 'value')])

def update_text_content(w_countries):
    text = "Latitude: " + str(list_location[w_countries]['Lat'])
    return text
#Update agriculture
@app.callback(
    Output('agri_content', 'children'),
    [Input('w_countries', 'value')])

def update_text_content(w_countries):
    text = str(list_agri[w_countries]['Agriculture'])
    return text



# Create bar chart (show new cases)
@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):

    return {
        'data': [go.Bar(x=df[df['Location'] == w_countries]['DateTime'],
                        y=df[df['Location'] == w_countries]['Temp'],

                        name='Temperature',
                        marker=dict(
                            color='orange'),
                        hoverinfo='text',
                        text=df[df['Location'] == w_countries]['DateTime'].dt.strftime('%Y-%m-%d') + '<br>' + 'Temperature: ' + df[df['Location'] == w_countries]['Temp'].astype(str) + '°C'
                        ),
                #  
                ],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Temperature during period in ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 25},

             hovermode='x',
             margin = dict(r = 0),
             xaxis=dict(title='<b>Date</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b>Temperature</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                ),

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),

                 )

    }

# Create polar scatter to plot wind
@app.callback(Output('polar_scatter_plot', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):

    return {
        'data': [go.Scatterpolar(
                        r=df[df['Location'] == w_countries]['WiSpeed2M'],
                        theta= df[df['Location'] == w_countries]['WiDirect2M'],
                        mode = 'markers',
                        hovertext= df[df['Location'] == w_countries]['DateTime'],
                        ),
                #  
                ],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Speed & direction of wind during period in ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 25},

             hovermode='x',
            #  margin = dict(r = 0),

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='orange'),

                 )

    }

# Create bar chart (show new cases)
@app.callback(Output('humidity_plot', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):

    return {
        'data': [go.Scattergl(
                        x= df[df['Location'] == w_countries]['DateTime'].sort_values(),
                        y= df[df['Location'] == w_countries]['SpecHumid2M'],
                        mode='lines',
                        ),
                #  
                ],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Specific humidity during period in ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 25},

             hovermode='x',
             margin = dict(r = 0),
             xaxis=dict(title='<b>Date</b>',
                        color='orange',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='orange'
                        )

                ),

             yaxis=dict(title='<b>Humidity</b>',
                        color='orange',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='orange'
                        )

                ),

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='orange'),

                 )

    }

data_scale = df.loc[:,['Location','DewFrost','WBulbTemp2M','EarthSkin','Precipitation','WSfSoil','SfPressure']]
feature_scale = ['DewFrost','WBulbTemp2M','EarthSkin','Precipitation','WSfSoil','SfPressure']
for item in feature_scale:
  scaler = MinMaxScaler()
  data_scale[item] =scaler.fit_transform(data_scale.loc[:,[item]])
mean_DewFrost_region = data_scale.groupby('Location')['DewFrost'].mean().reset_index()
mean_WBulbTemp2M_region = data_scale.groupby('Location')['WBulbTemp2M'].mean().reset_index()
mean_EarthSkin_region = data_scale.groupby('Location')['EarthSkin'].mean().reset_index()
# mean_Precipitation_region = data_scale.groupby('Location')['Precipitation'].mean().reset_index()
mean_WSfSoil_region = data_scale.groupby('Location')['WSfSoil'].mean().reset_index()
mean_SfPressure_region = data_scale.groupby('Location')['SfPressure'].mean().reset_index()



# Create spider chart
@app.callback(Output('spider_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):

    return {
        'data': [go.Scatterpolar(
                    r=[float(mean_DewFrost_region[mean_DewFrost_region['Location']==w_countries]['DewFrost']), float(mean_WBulbTemp2M_region[mean_WBulbTemp2M_region['Location']==w_countries]['WBulbTemp2M']), float(mean_EarthSkin_region[mean_EarthSkin_region['Location']==w_countries]['EarthSkin']), float(mean_WSfSoil_region[mean_WSfSoil_region['Location']==w_countries]['WSfSoil']), float(mean_SfPressure_region[mean_SfPressure_region['Location']==w_countries]['SfPressure'])],
                    theta=['Dew/Frost', 'Wet Bulb Temperature', 'Earth Skin Temperature', 'Surface Soil Wetness', 'Surface Pressure'],
                    fill='toself',
                        ),
                #  
                ],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Some other features during period in ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 25},

             hovermode='x',

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                font=dict(
                    family="sans-serif",
                    size=12,
                    color='orange'),
                polar=dict(
                    radialaxis=dict(
                    range=[0, 1], 
                )
            )
        )
    }


if __name__ == '__main__':
    app.run(debug=True)