import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
from dotenv import load_dotenv
import os
from google.cloud import bigquery
from google.oauth2 import service_account
import json
from election_exploration import exploration, analysis, first_preference_result, lollipop_charts_election_result

dash.register_page(__name__, path="/election", name="Election Analysis")

load_dotenv()

sql_query = """
SELECT * FROM `australia.au_first_count_results_mart` WHERE Victorious = 'Y'
"""

first_preference_sql = """
SELECT * FROM `australia.au_first_preference_results_mart`;
"""

election_result_summary_sql = """SELECT * FROM `australia.au_election_result_summary`;"""

project_id = os.getenv("GOOGLE_PROJECT_ID")
credential_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
credentials = service_account.Credentials.from_service_account_file(credential_file)

client = bigquery.Client(credentials=credentials, project=project_id)

election_result_df = client.query(sql_query).to_dataframe()
first_preferences = client.query(first_preference_sql).to_dataframe()
election_result_summary = client.query(election_result_summary_sql).to_dataframe()

# Load GeoJSON
with open("dash_app/election_map/cec_districts_map.geojson", "r") as f:
    geojson_data = json.load(f)

# Define party colors (adjust party names to match your data)
party_colors = {
    "Australian Labor Party": "#DE3533",
    "Liberal Party of Australia": "#0047AB",
    "Liberal National Party of Queensland": "#0047AB",
    "National Party of Australia": "#006644",
    "Australian Greens": "#10C25B",
    "Independent": "#808080",
    "Katter's Australian Party": "#8B0000",
    "Centre Alliance": "#FF6300",
}

states = sorted(election_result_df["StateAb"].unique())

state_centers = {
    "NSW": {"lat": -32.0, "lon": 147.0, "zoom": 5},
    "VIC": {"lat": -37.0, "lon": 144.5, "zoom": 6},
    "QLD": {"lat": -22.0, "lon": 145.0, "zoom": 4},
    "WA": {"lat": -26.0, "lon": 121.0, "zoom": 4},
    "SA": {"lat": -30.0, "lon": 136.0, "zoom": 5},
    "TAS": {"lat": -42.0, "lon": 146.5, "zoom": 6},
    "NT": {"lat": -19.5, "lon": 133.0, "zoom": 5},
    "ACT": {"lat": -35.5, "lon": 149.0, "zoom": 9},
}

layout = html.Div([
    html.H2(children="Australian Election (2025)", style={"textAlign": "center"}),
    html.Label("Select State:"),
    dcc.Dropdown(
        id="state-dropdown",
        options=[{"label": s, "value": s} for s in states],
        value=states[0] if states else None,
        clearable=False
    ),
    dcc.Graph(id="election-map", style={'height': '700px'}),
    html.H2(children="Election Data Exploration"),
    lollipop_charts_election_result(election_result_summary),
    exploration(),
    first_preference_result(first_preferences),
    analysis()
])


@callback(
    Output("election-map", "figure"),
    Input("state-dropdown", "value")
)
def update_map(selected_state):
    # Filter election data by state
    filtered_df = election_result_df[election_result_df["StateAb"] == selected_state]

    # Filter GeoJSON to only include divisions in the filtered data
    division_names = set(filtered_df["DivisionNm"].unique())
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": [
            f for f in geojson_data["features"]
            if f["properties"]["CED_NAME25"] in division_names
        ]
    }

    # Get center coordinates for selected state
    center = state_centers.get(selected_state, {"lat": -25.5, "lon": 134.5, "zoom": 4})

    fig = px.choropleth_map(
        filtered_df,
        geojson=filtered_geojson,
        locations="DivisionNm",
        featureidkey="properties.CED_NAME25",
        color="PartyNm",
        color_discrete_map=party_colors,
        center={"lat": center["lat"], "lon": center["lon"]},
        zoom=center["zoom"],
        hover_data=["DivisionNm", "PartyNm", "GivenNm", "Surname", "Victorious"]
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title=f"Australian Federal Election 2025 - {selected_state}",
        height=700,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.02,
            xanchor="left",
            x=0
        )
    )

    return fig
