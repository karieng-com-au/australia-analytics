import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


dash.register_page(__name__, path="/", name="Profile")

layout = html.Div([
    html.H2("Jack Toke"),
    html.H4("Data/Analytics Engineer - Software Engineer"),
    html.P("IT professional with two years' experience in software development and formal qualifications in data engineering and analytics. Track record of building solutions that enhance efficiency and deliver measurable cost savings. Looking to contribute technical and analytical capabilities as a Data/Analytics Engineer."),
    html.Hr(),
    dcc.Markdown("""
    ### SKILLS

    #### AI Engineering

    * **AI Engineering**: Generative AI, RAG, MCP Server development with Java Spring Boot/Python

    #### Data Analytics

    * **Statistical Analysis**: Linear Regression, Chi-Square, ANOVA
    * **Visualisation**: Streamlit, Tableau
    * **Story Telling**: Story telling with data

    #### Data Engineering

    * **Pipelines & Orchestration**: Dagster, Airflow, dbt, AWS Glue
    * **Data Wrangling**: Python, PySpark, Pandas, Polars
    * **Data Modelling & Architecture**: DuckDB, Snowflake, PostgreSQL, BigQuery, Redshift, Cassandra

    #### Software Engineering

    * **API Development**: RESTful/SOAP APIs, MCP servers (Java Spring Boot)
    * **Mobile Development**: Native Android (Kotlin Compose)
    """),
    html.Hr(),
    html.H3("EDUCATION & TRAININGS"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/unisq-logo.jpg", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Master of AI & ML"),
                html.H6("Southern Queensland University"),
                html.P("JUL 2025 - PRESENT")
            ]),
        ], className="h-100"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/qut-logo-og-1200.jpg", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Graduate Certificate IT (Data Analytics)"),
                html.H6("Queensland University of Technology"),
                html.P("MAR 2025 - December 2025")
            ]),
        ], className="h-100"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/lewagon.jpg", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Data Engineering Bootcamp"),
                html.H6("Le Wagon"),
                html.P("MAR 2025 - JUN 2025")
            ]),
        ], className="h-100"), md=4),

    ], className="g-3 mb-3"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/RMIT-Logo.jpg", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Data Engineering with AWS"),
                html.H6("RMIT"),
                html.P("MAR 2025 - APR 2025")
            ]),
        ], className="h-100"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/coder-academy.png", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Web Development (Bootcamp)"),
                html.H6("Coder Academy"),
                html.P("AUG 2019 - FEB 2020")
            ]),
        ], className="h-100"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardImg(src="assets/Victoria_University_Australia_Logo.png", style={"height": "200px", "objectFit": "contain", "objectPosition": "center", "backgroundColor": "#f8f9fa", "padding": "10px"}),
            dbc.CardBody([
                html.H5("Bachelor of Science in Computer Science"),
                html.H6("Victoria University"),
                html.P("FEB 2008 - FEB 2010")
            ]),
        ], className="h-100"), md=4),
    ], className="g-3")
])
