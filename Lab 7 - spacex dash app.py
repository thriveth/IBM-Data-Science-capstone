# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

launch_sites = spacex_df["Launch Site"].unique()
launch_site_dict = [{'label': a, 'value': a} for a in launch_sites]
launch_site_dict.insert(0, {'label': 'All sites', 'value': 'ALL'})
print(launch_site_dict)



# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id='site-dropdown',
            options=launch_site_dict,
            placeholder='Select a launch site here',
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(
            dcc.Graph(
                id='success-pie-chart'
            ),
        ),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        html.Div(
            dcc.RangeSlider(
                id='payload-slider',
                min=0, max=10000, step=1000,
                marks={int(0): '0', int(2500): '2500', int(5000): '5000',
                       int(7500): '7500', 10000: '10000'},
                value=[0, 10000],
                # style={"padding-left": "10%"}
            ),
            style={"width": "80%", "align": "center", "align-items": "center", "justify-content": "center"},
        ),
        html.Br(),
        html.Br(),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(
                id='success-payload-scatter-chart'
            ),
        ),
        html.Br(),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df, values='class',
            names='Launch Site',
            title='Total success launches by site',
        )
    else:
        use_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        fig = px.pie(
            use_df['class'].value_counts().to_frame("Success").reset_index(),
            values='Success',
            names='index',
            title=f'Total success launches for site {entered_site}',
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        use_df = spacex_df
    else:
        use_df = spacex_df[spacex_df["Launch Site"]==entered_site]
    use_df = use_df[use_df["Payload Mass (kg)"].between(payload_range[0], payload_range[1])]
    fig = px.scatter(
        use_df,
        x="Payload Mass (kg)", y='class', color='Booster Version Category'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
