# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("plotly_proj/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# data to obtain the porcentage of success for all the sites
suc_lau_df = spacex_df.groupby('Launch Site',as_index= False)['class'].sum()
suc_lau_df.columns = ['Launch Site', 'success %']
suc_lau_df['success %'] =  suc_lau_df['success %']/suc_lau_df['success %'].sum()

# data for the pie charts of all individual sites
new_df = spacex_df[['Launch Site', 'class']].groupby('Launch Site', as_index = False).value_counts()
# pie_data = new_df.loc[new_df['Launch Site'] == f'{Site}']
# pie_data['count'] = pie_data['count']/pie_data['count'].sum()
# pie_data.columns = ['Launch Site', 'class','%']

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',   options=[{'label': 'All Sites', 'value': 'All Sites'},
                                                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                                             ],
                                                                             value = 'All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider( min_payload,max_payload, id='payload-slider', value = [min_payload,max_payload/2 ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(site):
    if site == 'All Sites':
        fig = px.pie(suc_lau_df, names= 'Launch Site', values='success %', title='% of success for all sites')
        print('1')
    else:
        pie_data = new_df.loc[new_df['Launch Site'] == site].copy()
        pie_data['count'] = pie_data['count']/pie_data['count'].sum()
        pie_data.columns = ['Launch Site', 'class','%']
        fig = px.pie(pie_data, names= 'class', values='%', title=f'Success vs. Failed counts for {site}')
        print('4')
    fig.update_layout()
    print('final')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( 
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
    )
def update_scatter(site_dropdown, slider_range):
    
    dataf_new = spacex_df[['Payload Mass (kg)','class','Launch Site']].copy()
    dataone = dataf_new.loc[dataf_new['class'] == 1].loc[dataf_new['Launch Site'] == site_dropdown]

    low, high = slider_range

    if site_dropdown == 'All Sites':
        mask = (dataf_new['Payload Mass (kg)'] > low) & (dataf_new['Payload Mass (kg)'] < high)
        fig = px.scatter(dataf_new[mask], x='Payload Mass (kg)', y="class", color="Launch Site",title = 'Scatterplot of result vs payload mass')
    else:
        # replace with your own data source
        mask = (dataone['Payload Mass (kg)'] > low) & (dataone['Payload Mass (kg)'] < high)
        fig = px.scatter(dataone[mask], x='Payload Mass (kg)', y="class", title = f'Scatterplot of success and failure with respect to the payload mass of {site_dropdown}')
        
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
