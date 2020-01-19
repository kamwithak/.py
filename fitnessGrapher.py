# Fitness Understanding Tool - V1
# Currently deployed @ https://health-grapher.herokuapp.com/ (Please wait ~ 30 seconds to load)
# Daily steps, heart rate, distance travelled, and caloric output were some of the metrics explored
# Full stack application available upon request (including Fitbit JSON Requests)
# ~~~
# Developer: Kamran Choudhry

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from fitnessFetcher import collectHeartRateInformation, collectCaloricInformation, collectDistanceInformation

def masterApplication(mainApp):
    bpmDict, dateOptions = collectHeartRateInformation()
    caloricDict = collectCaloricInformation()
    distanceDict = collectDistanceInformation()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, server=mainApp, routes_pathname_prefix='/fitnessGrapher/', external_stylesheets=external_stylesheets)
    
    colors = {
        'background': 'white',
        'text': 'red'
    }

    app.layout = html.Div(
        style={'backgroundColor': colors['background']},
        children=[
        html.H2(
            children='Fitness Understanding Tool (V1)',
            style={
                'text-align': 'center',
                'color': colors['text']
                }
            ),
        html.Div(children='Please input a valid date:', style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='chosenDate',
            options=dateOptions,
            value='2019-07-11'
        ),
        html.Hr(),
        html.Div(id="output-graph"),
        html.Div(children='Daily Metrics:', style={'text-align': 'center', 'color': colors['text']}),
        html.Div(id='dateOutput', style={'font-weight': 'bold'}),
        dash_table.DataTable(
            id='table',
            columns=[
                     {"name": 'Max Heart Rate (BPM)', "id": 'col1'},
                     {"name": 'Cumulative Distance (KM)', "id": 'col2'},
                     {"name": 'Cumulative Calories Burned', "id": 'col3'}
                     ],
            style_cell={'textAlign': 'center'},
            data=[{'col1': 0, 'col2': 0, 'col3': 0}]
            )
        ]
    )

    def log(msg):
        mainApp.logger.info(msg)

    @app.callback(
        Output('dateOutput', 'children'),
        [Input('chosenDate', 'value')]
    )
    def loading_date(value):
        return value + ':'

    @app.callback(
        Output('table', 'data'),
        [Input('chosenDate', 'value')]
    )
    def loading_data(value):
        x = max(list(bpmDict[value][1]))
        y = distanceDict[value] / 100000
        z = caloricDict[value]
        return [{'col1': x, 'col2': y, 'col3': z}]

    @app.callback(
        Output("output-graph", "children"),
        [Input('chosenDate', 'value')])
    def update_output(chosenDate):
        masterData = [{'x': list(bpmDict[chosenDate][0]), 'y': list(bpmDict[chosenDate][1]), 'type': 'line', 'name': 'BPM'}]
        
        if (chosenDate == '2019-07-11'):
            masterData.append({'x': ['07/11/19 23:26:22', '07/11/19 23:26:22'], 'y': [50, 170], 'name': 'Begin Workout', 'marker': {'color':'green'}})
            masterData.append({'x': ['07/12/19 00:40:36', '07/12/19 00:40:36'], 'y': [50, 170], 'name': 'End Workout', 'marker': {'color':'green'}})                       

        #log(chosenDate)
        return dcc.Graph(
            id='firstGraph',
            figure={
                'data': masterData,
                'layout': {
                    'title': 'Heart Rate ~ Beats per minute : ' + chosenDate,
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'xaxis': {
                        'tickvals': [],
                    },
                    'yaxis':{
                        'title':'BPM'
                    },
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
