from dash import html, dcc
import plotly.graph_objects as go

def exploration():
    return dcc.Markdown("I have been in Australia since 2007 When I immigrated, however I have never fully understood "
                        "how the preferential voting system works here. In Australia's preferential voting system, "
                        "voters rank candidates in order of preference rather than simply choosing one. If no "
                        "candidate receives more than 50 percent of first preferences, the candidate with the fewest "
                        "votes is eliminated and their votes are redistributed to each ballot's next preferred candidate. "
                        "This process continues until one candidate achieves a majority. The system means that "
                        "even if your first choice is unlikely to win, your vote still influences the outcome through "
                        "your lower preferences. It also tends to favour major parties that are the 'least disliked' "
                        "second option—which explains why the ALP, positioned closer to the political centre-left, "
                        "often benefits from Greens preferences, while the Coalition, positioned on the centre-right, "
                        "has fewer natural preference partners.")

def analysis():
    return dcc.Markdown("In the last House of Representatives election in 2025, the Australian Labor Party (ALP) "
                        "received the most first preferences in 86 electorates. It lost only 5 of those. "
                        "That means in 17 electorates where the ALP wasn't people's first preference, it went on to "
                        "win because preferential voting worked in its favour—especially preferences flowing from the "
                        "Australian Greens and other parties that are philosophically more aligned with it."
                        " "
                        "In contrast, the Coalition-comprising the Liberal Party, the Nationals, the Liberal National "
                        "Party (Queensland), and the Country Liberal Party (NT) - received the highest first preference "
                        "count in 56 electorates. However, it could only hold 33 of them, as preferential voting worked "
                        "against it. That's an astounding 41 percent of its leading positions lost to vote transfers.")


def first_preference_result(dataframe):
    winners = dataframe[dataframe["Victorious"] == "Y"].sort_values("Counts", ascending=False).copy()
    losers = dataframe[dataframe["Victorious"] == "N"].sort_values("Counts", ascending=False).copy()

    return dcc.Graph(
        figure={
            "data": [
                {"x": winners["PartyAb"], "y": winners["Counts"], "type": "bar", "name": "Won", "text": winners["Counts"], "textposition": "outside"},
                {"x": losers["PartyAb"], "y": losers["Counts"], "type": "bar", "name": "Lost", "text": losers["Counts"], "textposition": "outside"}
            ],
            "layout": {
                "title": {
                    "text": (
                        "Preferential Voting Outcomes: The 2025 House of Representatives Election"
                        "<br><sup>Number of electorates won and lost by each party "
                        "after leading on first preference count</sup>"
                    ),
                    "x": 0,
                    "xanchor": "left",
                },
                "yaxis": {"title": {"text": "Number of Electorates/Districts", "standoff": 10}},
                "xaxis": {"title": {"text": "Party", "standoff": 20}},
                "margin": {"l": 80, "b": 80},
            }
        }
    )

def lollipop_charts_election_result(dataframe):
    party_colors = {
        "ALP": "#DE3533",
        "LNP": "#0047AB",
        "LP": "#1E90FF",
        "NP": "#4169E1",
        "GRN": "#10C25B",
        "XEN": "#FF6300",
        "KAP": "#8B0000",
        "IND": "teal",
    }

    df = dataframe.sort_values("WinCount", ascending=True)

    fig = go.Figure()

    # Stems and dots per party for individual colours
    for _, row in df.iterrows():
        color = party_colors.get(row["PartyAb"], "gray")
        fig.add_trace(go.Scatter(
            x=[0, row["WinCount"]],
            y=[row["PartyAb"], row["PartyAb"]],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[row["WinCount"]],
            y=[row["PartyAb"]],
            mode="markers+text",
            marker=dict(size=12, color=color),
            text=[str(row["WinCount"])],
            textposition="middle right",
            textfont=dict(size=11),
            showlegend=False,
        ))

    # Majority line at 75 seats
    fig.add_vline(
        x=75,
        line_width=2,
        line_dash="dash",
        line_color="grey",
    )
    fig.add_annotation(
        x=75,
        y=1.05,
        yref="paper",
        text="75 — Majority required to form government",
        showarrow=False,
        font=dict(size=11, color="grey"),
        xanchor="left",
    )

    fig.update_layout(
        title={
            "text": (
                "Seats Won by Party"
                "<br><sup>Total electorates won by each party in the 2025 election</sup>"
            ),
            "x": 0,
            "xanchor": "left",
        },
        template="simple_white",
        xaxis={
            "title": {"text": "Seats Won", "standoff": 20},
            "gridcolor": "#f0f0f0",
            "showgrid": True,
            "zeroline": False,
        },
        yaxis={
            "title": {"text": "Party", "standoff": 10},
            "gridcolor": "#f0f0f0",
            "showgrid": True,
        },
        margin={"l": 80, "b": 80, "t": 80},
        height=400,
    )

    return dcc.Graph(figure=fig)
