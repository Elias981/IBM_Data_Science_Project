import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
import pandas as pd 



np.random.seed(50)
x_rand = np.random.randint(1,61,60)
y_rand = np.random.randint(1,61,60)


colors = {'text' : '#cb3234',
          'plot_color' : '#000000',
          'paper_color' : '#008f39',
          'font_color' : '#000000'
            }

app = dash.Dash()
app.layout = html.Div([
    html.H1(children = "Hello Dash",
            style={
                'textAlign': 'center',
                'color' : colors['text']
            }
            ),  

    html.Div(children = 'Dash - a data product development framework plotly',
             style={
                'textAlign' : 'center',
                'color' : colors['text']
            }
            ),
    
    html.Br(),

    # html.Label('Chose a city'),

    dcc.Dropdown(
        id = 'drop',
        options = [
            {'label' : 'San Fransisco', 'value': 'SF' },
            {'label' : 'Guadalajara', 'value': 'G' },
            {'label' : 'Mexico', 'value': 'M' }
        ],
        # value = 'G',
        placeholder='Select a City'
    ),

    dcc.Slider(
        min = 0,
        max = 100,
        value = 50,
        marks = {i : i for i in range(0,101)}
        
    ),
    
    html.Label('This is a range slider'),

    dcc.RangeSlider(
        id = '1-rrange-slider',
        min=1,
        max=10,
        step=0.5,
        value= [3,7],
        marks = {i:i for i in range(0,11)}
    ),

    # note dcc.Graph(id = 'string', figure = {data : [{},...,{}], layout : {}})
    dcc.Graph(
        id='sample_graph',
        figure = {
            'data' : [
                {'x' : [5,6,7], 'y' : [12,15,17], 'type' : 'bar', 'name' : 'first_chart'},
                {'x' : [5,6,7], 'y' : [10,50,100], 'type' : 'bar', 'name' : 'second_chart'}
            ],
            'layout' : {

                'title' : 'barchart',
                'font' : {
                    'color' : colors['text']
                },
                'paper_bgcolor': colors['paper_color'], # verde
                'plot_bgcolor' : colors['plot_color'] # negro

            }
        }   
    ),
    
    dcc.Graph(
        id = 'scatter-chart',
        figure= {
            'data' : [
            go.Scatter(x = x_rand,
                       y = y_rand,
                       mode='markers'
                    )
            ], 
        'layout' : go.Layout(
            title = 'Scatter plot 60 random values',
            xaxis  = {'title' : 'Random x values'},
            yaxis = {'title' : 'Random y values'}
            )
            
        }

    )
])

if __name__ == '__main__':
    app.run()