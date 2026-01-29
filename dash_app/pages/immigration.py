import dash
from dash import html

dash.register_page(__name__, path="/immigration", name="Immigration Analysis")

layout = html.Div([
    html.H2("Immigration Analysis"),
    html.P("Immigration analysis content coming soon."),
])
