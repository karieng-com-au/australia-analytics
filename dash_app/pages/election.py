import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
from dotenv import load_dotenv
import os
from functools import lru_cache
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import json
try:
    from dash_app.election_exploration import exploration, analysis, first_preference_result, lollipop_charts_election_result
except ModuleNotFoundError:
    from election_exploration import exploration, analysis, first_preference_result, lollipop_charts_election_result

dash.register_page(__name__, path="/election", name="Election Analysis")

load_dotenv()

credential_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credential_file and os.path.exists(credential_file):
    credentials = service_account.Credentials.from_service_account_file(credential_file)
    project_id = os.getenv("GOOGLE_PROJECT_ID")
else:
    import google.auth
    credentials, project_id = google.auth.default()

client = bigquery.Client(credentials=credentials, project=project_id)


@lru_cache(maxsize=1)
def get_election_results():
    sql = "SELECT * FROM `australia.au_first_count_results_mart` WHERE Victorious = 'Y'"
    return client.query(sql).result().to_dataframe()


@lru_cache(maxsize=1)
def get_first_preferences():
    sql = "SELECT * FROM `australia.au_first_preference_results_mart`"
    return client.query(sql).result().to_dataframe()


@lru_cache(maxsize=1)
def get_election_result_summary():
    sql = "SELECT * FROM `australia.au_election_result_summary`"
    return client.query(sql).result().to_dataframe()


# Normalise party names so colours are consistent across all states
party_name_map = {
    "Labor": "Australian Labor Party",
    "Liberal National": "Liberal National Party of Queensland",
    "Liberal": "Liberal Party of Australia",
    "National": "National Party of Australia",
    "Greens": "Australian Greens",
    "Independent": "Independent",
    "Katter": "Katter's Australian Party",
    "Centre Alliance": "Centre Alliance",
}

def normalise_party(name):
    for keyword, canonical in party_name_map.items():
        if keyword in name:
            return canonical
    return name


def load_geojson():
    local_path = os.path.join(os.path.dirname(__file__), "..", "election_map", "cec_districts_map.geojson")
    if os.path.exists(local_path):
        with open(local_path) as f:
            return json.load(f)
    bucket_name = os.getenv("GCS_BUCKET")
    blob_path = os.getenv("GCS_GEOJSON_PATH")
    if not bucket_name or not blob_path:
        raise RuntimeError("GCS_BUCKET and GCS_GEOJSON_PATH environment variables must be set")
    blob = storage.Client(credentials=credentials, project=project_id).bucket(bucket_name).blob(blob_path)
    return json.loads(blob.download_as_text())


@lru_cache(maxsize=1)
def load_all_data():
    """Lazy-load all data on first request so gunicorn can start immediately."""
    election_result_df = get_election_results()
    first_preferences = get_first_preferences()
    election_result_summary = get_election_result_summary()
    election_result_df["PartyNm"] = election_result_df["PartyNm"].apply(normalise_party)
    geojson_data = load_geojson()
    return election_result_df, first_preferences, election_result_summary, geojson_data


# Define party colors (adjust party names to match your data)
party_colors = {
    "Australian Labor Party": "#DE3533",
    "Liberal Party of Australia": "#1E90FF",
    "Liberal National Party of Queensland": "#0047AB",
    "National Party of Australia": "#4169E1",
    "Australian Greens": "#10C25B",
    "Independent": "teal",
    "Katter's Australian Party": "#8B0000",
    "Centre Alliance": "#FF6300",
}

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


def layout():
    election_result_df, first_preferences, election_result_summary, _ = load_all_data()
    states = sorted(election_result_df["StateAb"].unique())
    return html.Div([
        html.H2(children="Australian Election (2025)"),
        html.P("Labor has retained government in the 2025 federal election, with Anthony Albanese securing a second term as Prime Minister. But what does the data reveal about how Australians voted? In this analysis, we dig into the results to identify patterns across electorates. Explore the interactive map below to see which party won each seat — select a state from the dropdown to focus on the region that interests you."),
        html.Label("Select State:"),
        dcc.Dropdown(
            id="state-dropdown",
            options=[{"label": s, "value": s} for s in states],
            value=states[0] if states else None,
            clearable=False
        ),
        dcc.Graph(id="election-map", style={'height': '700px'}),
        html.P("Labor's landslide victory is starkly evident in the seat distribution. With 98 seats, the ALP holds a comfortable majority well beyond the 75 needed to govern. The combined Coalition forces — LNP (15), Liberal Party (11) and Nationals (9) — managed only 35 seats, representing a historically weak result for the centre-right. Notably, Independents secured 14 seats, continuing the trend of voters turning away from major parties in favour of local, issue-focused candidates. The Greens, despite their prominence in public discourse, won just one seat, suggesting their support remains geographically concentrated."),
        html.H2(children="How Preferential Voting Shaped the Result"),
        exploration(),
        first_preference_result(first_preferences),
        analysis(),
        lollipop_charts_election_result(election_result_summary)
    ])


@callback(
    Output("election-map", "figure"),
    Input("state-dropdown", "value")
)
def update_map(selected_state):
    election_result_df, _, _, geojson_data = load_all_data()

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
