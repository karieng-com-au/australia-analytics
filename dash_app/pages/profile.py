import dash
from dash import html

dash.register_page(__name__, path="/", name="Profile")

layout = html.Div([
    html.H2("Profile"),
    html.P("Welcome to the Australian Data Analytics dashboard."),
])
