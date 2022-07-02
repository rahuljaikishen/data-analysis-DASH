import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from common.functions import get_match_data_set, get_matches_played_on_ground, get_stadium_statistics

IPL_LOGO = 'assets/logo.png'
CSS_REF = 'assets/style.css'
ALL_YEARS = [i for i in range(2008, 2021)]
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

match_dataset = get_match_data_set()

app.title = 'Indian Premier League'
navbar = dbc.Navbar(
    children=[
        html.Img(src=IPL_LOGO, height="70px")
    ],
    class_name="navbar navbar-expand-lg custom-navbar"

)
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href=CSS_REF
    ),
    navbar,
    html.Div([
        dcc.RangeSlider(2008, 2020, 1, value=[2020], id='year-range-slider',
                        marks={i: '{}'.format(i) for i in ALL_YEARS},
                        tooltip={"placement": "bottom", "always_visible": True}),
        html.Div(id='output-container-range-slider')
    ]),
    dcc.Graph(
        id='matches'
    ),
    html.Div(id='stadium_stats')

]
)


@app.callback(
    Output('matches', 'figure'),
    [Input('year-range-slider', 'value')])
def update_output(value):
    ALL_YEARS = value
    matches_played_on_ground = get_matches_played_on_ground(match_dataset, value)
    fig = px.scatter_geo(matches_played_on_ground, lat="Lat", lon="Long", color="venue",
                         hover_name="venue", hover_data=['city', 'No. of Matches'], size="No. of Matches",
                         center={'lat': 20.5937, 'lon': 78.9629})
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output(component_id='stadium_stats', component_property='children'),
    Input(component_id='matches', component_property='clickData')
)
def stadium_statistics(input_value):
    stats = ''
    if input_value is not None:
        stats = get_stadium_statistics(match_dataset, ALL_YEARS, input_value['points'][0]['customdata'][0])
    return stats


if __name__ == '__main__':
    app.run_server(debug=True)
