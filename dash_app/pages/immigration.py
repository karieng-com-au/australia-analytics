import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dotenv import load_dotenv
import os
from google.cloud import bigquery #, storage
from google.oauth2 import service_account
from functools import lru_cache

dash.register_page(__name__, path="/immigration", name="Immigration Analysis")

load_dotenv()

credential_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credential_file and os.path.exists(credential_file):
    credentials = service_account.Credentials.from_service_account_file(credential_file)
    project_id = os.getenv("GOOGLE_PROJECT_ID")
else:
    import google.auth
    credentials, project_id = google.auth.default()

client = bigquery.Client(credentials=credentials, project=project_id)

def layout():
    return html.Div([
        html.H2("Australia's Silver Tsunami: The Demographic Case for Immigration"),
        html.P("Immigration remains a contentious political issue in Australia. But what does the data actually say? Examining Australian Bureau of Statistics figures reveals demographic trends that frame immigration not as a political choice, but as an economic necessity."),

        html.H3("The Demographic Crossover"),
        dcc.Graph(figure=scatter_graph(), style={'height': '700px'}),
        html.P("Since 2012, Australia's birth rate has declined by approximately 1,525 births annually, while deaths have increased by roughly 3,375 per year. The graph projects a critical inflection point around 2040, when deaths are forecast to exceed births for the first time in modern Australian history. Beyond this crossover, Australia will experience natural population decline—where deaths outpace births—making immigration essential for any population growth. The full force of the 'Silver Tsunami' accelerates through the 2040s, when the aging population will place unprecedented strain on healthcare, aged care, and social services while the working-age population shrinks relative to retirees."),
        html.P("It is worth noting that this projection extrapolates 25 years from roughly 13 data points. The widening confidence intervals reflect this uncertainty. However, the underlying trend—declining births and rising deaths—is consistent with patterns observed across comparable developed nations."),

        html.H3("Net Migration Trends"),
        dcc.Graph(figure=net_migration_lollipop_horizontal(), style={'height': '400px'}),
        html.P("The government's target of 239,000 net migrants annually appears designed to offset this demographic shift. The elevated migration figures of 438,000 (2022), 531,000 (2023), and 330,000 (2024) represent a correction following pandemic-era border closures in 2020-2021, when migration nearly ceased. These elevated numbers suggest the government is attempting to build demographic resilience ahead of the projected crossover point."),

        html.H3("Immigration and Birth Rates: Is There a Link?"),
        html.P(["Interestingly, birth rates remained stable—even slightly increasing by approximately 15,000 in 2021—during the period of lowest immigration. ", html.B("This suggests that births are driven primarily by existing citizens and permanent residents rather than recent arrivals, raising a critical question: what pronatalist policies might encourage higher birth rates among the established population?")]),

        html.H3("Did the Baby Bonus Work?"),
        dcc.Graph(figure=scatter_graph_no_projection(), style={'height': '600px'}),
        html.P("Australia has experimented with pronatalist policies before. The government introduced a $3,000 lump sum baby bonus in 2004, which correlated with an increase of 15,000 births in subsequent years. When the bonus rose to $4,000 in 2006, births increased by nearly 19,000 in 2007. A further increase to $5,000 in 2008, however, produced no dramatic rise. Birth rates plateaued with modest increases until peaking in 2012 at approximately 315,000 births—the highest point visible on the graph. In 2014, citing sustainability concerns, the government replaced the $5,000 lump sum with a reduced payment of $2,000-$3,000 distributed over 13 weeks. Since then, birth rates have been in gradual decline, reaching approximately 290,000 by 2024."),
        html.P("The timing is notable: birth rates peaked while the bonus was at its highest and declined after it was reduced. However, correlation does not establish causation. The diminishing returns from successive bonus increases—particularly the lack of any spike after the 2008 increase to $5,000—indicate that cash payments alone cannot overcome deeper structural barriers to having children. Housing costs, childcare affordability, and career disruption are likely stronger determinants of family size decisions than one-off payments."),

        html.H3("A Global Pattern"),
        html.P("Australia's fertility decline is not unique. South Korea, Singapore, and Japan have all implemented aggressive pronatalist policies—including cash bonuses, subsidised childcare, and housing assistance—yet none has succeeded in reversing fertility decline to replacement rate (2.1 births per woman). This global pattern suggests that declining birth rates in developed economies are driven by structural shifts in how people live and work, not simply by insufficient financial incentives."),

        html.H3("What Lies Ahead"),
        html.P(["The projections carry substantial uncertainty, particularly beyond 2030, as shown by the widening confidence intervals. However, even the most optimistic scenarios show continued divergence between births and deaths. ", html.B("The evidence suggests that immigration itself has minimal impact on birth rates."), " Unless the government addresses fundamental cost-of-living and housing affordability issues—the structural factors that likely explain why larger baby bonuses lost effectiveness—declining fertility will persist regardless of migration levels."]),
        html.P("Realistically, Australia will likely need both strategies simultaneously: pronatalist policies that address the economic barriers to family formation, and sustained immigration to fill the gap that policy alone cannot close. No developed country has solved this problem with one approach alone. Current trends suggest the government has leaned heavily toward immigration, but the political sustainability of high immigration levels remains uncertain. Without a dual strategy, Australia faces the full force of the Silver Tsunami in the 2040s."),
        html.P(["Source code: ", html.A("GitHub repository", href="https://github.com/karieng-com-au/australia-analytics")]),
    ])

@lru_cache(maxsize=1)
def get_births_deaths_data():
    sql = "SELECT year, births, deaths FROM `australia.au_population_mart` WHERE year >= 2012"
    return client.query(sql).to_dataframe()

@lru_cache(maxsize=1)
def get_net_immigration_data():
    sql = "SELECT year, net_migration FROM `australia.au_population_mart`"
    return client.query(sql).to_dataframe()

@lru_cache(maxsize=1)
def get_births_deaths_data_2000():
    sql = "SELECT year, births, deaths FROM `australia.au_population_mart` WHERE year >= 2000"
    return client.query(sql).to_dataframe()

def scatter_graph():
    births_n_deaths_df = get_births_deaths_data()
    fig = px.scatter(births_n_deaths_df, x="year", y="births", trendline="ols", color_discrete_sequence=["#167d7f"])
    fig.data[0].name = "Births"
    fig.data[0].showlegend = True
    fig.data[1].name = "Births Trend"
    fig.data[1].showlegend = True
    deaths_trace = px.scatter(births_n_deaths_df, x="year", y="deaths", trendline="ols", color_discrete_sequence=["red"])
    deaths_trace.data[0].name = "Deaths"
    deaths_trace.data[0].showlegend = True
    deaths_trace.data[1].name = "Deaths Trend"
    deaths_trace.data[1].showlegend = True
    fig.add_trace(deaths_trace.data[0])
    fig.add_trace(deaths_trace.data[1])

    # Forecast births and deaths for the next 10 years
    years = births_n_deaths_df["year"].values
    max_year = int(years.max())
    forecast_years = np.arange(max_year + 1, max_year + 25)

    births_coeffs = np.polyfit(years, births_n_deaths_df["births"].values, 1)
    deaths_coeffs = np.polyfit(years, births_n_deaths_df["deaths"].values, 1)

    births_forecast = np.polyval(births_coeffs, forecast_years)
    deaths_forecast = np.polyval(deaths_coeffs, forecast_years)

    # Calculate confidence intervals based on residual std error
    # Uncertainty grows with distance from the historical data
    births_residuals = births_n_deaths_df["births"].values - np.polyval(births_coeffs, years)
    deaths_residuals = births_n_deaths_df["deaths"].values - np.polyval(deaths_coeffs, years)
    births_std = np.std(births_residuals)
    deaths_std = np.std(deaths_residuals)

    # Expanding uncertainty: 1.96 * std * sqrt(1 + years ahead / n)
    n = len(years)
    years_ahead = np.arange(1, len(forecast_years) + 1)
    births_margin = 1.96 * births_std * np.sqrt(1 + years_ahead / n)
    deaths_margin = 1.96 * deaths_std * np.sqrt(1 + years_ahead / n)

    # Births forecast with confidence band
    fig.add_trace(go.Scatter(
        x=forecast_years, y=births_forecast, mode="markers+lines",
        name="Births Forecast", marker=dict(color="#167d7f", symbol="diamond"),
        line=dict(dash="dash", color="#167d7f"),
    ))
    fig.add_trace(go.Scatter(
        x=np.concatenate([forecast_years, forecast_years[::-1]]),
        y=np.concatenate([births_forecast + births_margin, (births_forecast - births_margin)[::-1]]),
        fill="toself", fillcolor="rgba(22,125,127,0.1)", line=dict(color="rgba(0,0,0,0)"),
        name="Births 95% CI", showlegend=True,
    ))

    # Deaths forecast with confidence band
    fig.add_trace(go.Scatter(
        x=forecast_years, y=deaths_forecast, mode="markers+lines",
        name="Deaths Forecast", marker=dict(color="red", symbol="diamond"),
        line=dict(dash="dash", color="red"),
    ))
    fig.add_trace(go.Scatter(
        x=np.concatenate([forecast_years, forecast_years[::-1]]),
        y=np.concatenate([deaths_forecast + deaths_margin, (deaths_forecast - deaths_margin)[::-1]]),
        fill="toself", fillcolor="rgba(245,73,39,0.1)", line=dict(color="rgba(0,0,0,0)"),
        name="Deaths 95% CI", showlegend=True,
    ))

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 80},
        title="Australian Births and Deaths — Historical & Forecast",
        height=700,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="left",
            x=0.2
        )
    )
    return fig

def get_birth_data_by_year(births_n_deaths_df, year):
    return births_n_deaths_df.loc[births_n_deaths_df["year"] == year, "births"].values[0]

def scatter_graph_no_projection():
    births_n_deaths_df = get_births_deaths_data_2000()
    fig = px.scatter(births_n_deaths_df, x="year", y="births", trendline="ols", color_discrete_sequence=["#167d7f"])
    fig.data[0].name = "Births"
    fig.data[0].showlegend = True
    fig.data[1].name = "Births Trend"
    fig.data[1].showlegend = True
    deaths_trace = px.scatter(births_n_deaths_df, x="year", y="deaths", trendline="ols", color_discrete_sequence=["red"])
    deaths_trace.data[0].name = "Deaths"
    deaths_trace.data[0].showlegend = True
    deaths_trace.data[1].name = "Deaths Trend"
    deaths_trace.data[1].showlegend = True
    fig.add_trace(deaths_trace.data[0])
    fig.add_trace(deaths_trace.data[1])

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 80},
        title="Australian Births and Deaths with Government Pronatal Policy",
        height=700,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.10,
            xanchor="left",
            x=0.2
        ),
        annotations=[
            dict(
                x=2004, y=get_birth_data_by_year(births_n_deaths_df, 2004),
                text="$3000 Baby Bonus Introduced",
                showarrow=True,
                arrowhead=2,
                ax=0, ay=40,
                font=dict(size=12, color="#167d7f"),
                arrowcolor="#167d7f",
            ),
            dict(
                x=2006, y=get_birth_data_by_year(births_n_deaths_df, 2006),
                text="Baby Bonus Increased to $4000",
                showarrow=True,
                arrowhead=2,
                ax=-80, ay=-40,
                font=dict(size=12, color="#167d7f"),
                arrowcolor="#167d7f",
            ),
            dict(
                x=2008, y=get_birth_data_by_year(births_n_deaths_df, 2008),
                text="Baby Bonus Increased to $5000",
                showarrow=True,
                arrowhead=2,
                ax=-40, ay=-40,
                font=dict(size=12, color="#167d7f"),
                arrowcolor="#167d7f",
            ),
            dict(
                x=2013, y=get_birth_data_by_year(births_n_deaths_df, 2013),
                text="$3000 Second Child Bonus Introduced",
                showarrow=True,
                arrowhead=2,
                ax=-40, ay=100,
                font=dict(size=12, color="#167d7f"),
                arrowcolor="#167d7f",
            ),
            dict(
                x=2014, y=get_birth_data_by_year(births_n_deaths_df, 2014),
                text="Baby Bonus Reduced to ~$2000--$3000 (13 weeks installment)",
                showarrow=True,
                arrowhead=2,
                ax=80, ay=140,
                font=dict(size=12, color="#167d7f"),
                arrowcolor="#167d7f",
            )
        ]
    )
    return fig


def net_migration_lollipop():
    df = get_net_immigration_data().sort_values("year")
    colors = ["#167d7f" if v >= 0 else "#e63946" for v in df["net_migration"]]

    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[0, row["net_migration"]], y=[row["year"], row["year"]],
            mode="lines", line=dict(color="grey", width=2), showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=df["net_migration"], y=df["year"], mode="markers",
        marker=dict(size=10, color=colors), name="Net Migration", showlegend=False,
    ))
    fig.update_layout(
        title="Australia Net Migration by Year",
        xaxis_title="Net Migration",
        yaxis_title="Year",
        height=700,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        yaxis=dict(dtick=1),
    )
    return fig


def net_migration_lollipop_horizontal():
    df = get_net_immigration_data().sort_values("year")
    colors = ["#167d7f" if v >= 0 else "#e63946" for v in df["net_migration"]]

    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["year"], row["year"]], y=[0, row["net_migration"]],
            mode="lines", line=dict(color="grey", width=2), showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["net_migration"], mode="markers",
        marker=dict(size=10, color=colors), name="Net Migration", showlegend=False,
    ))
    fig.update_layout(
        title="Australia Net Migration by Year",
        xaxis_title="Year",
        yaxis_title="Net Migration",
        height=400,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        xaxis=dict(dtick=1),
    )
    return fig
