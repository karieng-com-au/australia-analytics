import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, clientside_callback

dash.register_page(__name__, path="/services", name="Services")

layout = html.Div([
    html.H2("Services", className="mt-4"),
    dbc.Row([
        dbc.Col(dbc.CardImg(src="assets/data-engineering-2.png", style={"width": "350px", "objectFit": "cover", "objectPosition": "center"}),
                width="auto", style={"padding": "10px",}),
        dbc.Col([
           html.H5("Data Engineering"),
        html.P(
            "We build robust data pipelines that extract information from your existing systems, transform it into usable "
            "formats, and load it where you need it. Whether you're consolidating data from multiple sources or automating "
            "manual reporting processes, we'll create reliable infrastructure that keeps your data flowing and ready for analysis.",
            className="mt-3 mb-4",
        ),
        ], className="d-flex flex-column justify-content-center")
        ]),
    dbc.Row([
        dbc.Col([
           html.H5("Dashboards & Visualisation"),
        html.P(
            "We design clear, professional dashboards that give you real-time visibility into what matters most. "
           "From tracking business performance and sales figures to monitoring system health, we build visualisations "
           "that help you spot trends, identify issues early, and make informed decisions without digging through spreadsheets.",
            className="mt-3 mb-4",
        ),
        ], className="d-flex flex-column justify-content-center"),
        dbc.Col(dbc.CardImg(src="assets/data-visualisation.png", style={"width": "350px", "objectFit": "cover", "objectPosition": "center"}),
                width="auto", style={"padding": "10px",}),
        ]),
    dbc.Row([
        dbc.Col(dbc.CardImg(src="assets/business-analytics.png", style={"width": "350px", "objectFit": "cover", "objectPosition": "center"}),
                width="auto", style={"padding": "10px",}),
        dbc.Col([
           html.H5("Business Data Analysis"),
        html.P(
            "We help you make sense of the data you already have. Through careful analysis, we uncover patterns, answer "
           "specific business questions, and identify opportunities for improvement. Whether you need a one-off "
           "investigation or ongoing analytical support, we'll translate your data into actionable insights.",
            className="mt-3 mb-4",
        ),
        ], className="d-flex flex-column justify-content-center")
        ])
])


