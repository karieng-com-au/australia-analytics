import polars as pl
from google.cloud import bigquery
from dotenv import load_dotenv
from google.oauth2 import service_account
import streamlit as st
import statsmodels.api as sm
import os
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Australia Population",
    layout="centered",
    initial_sidebar_state="expanded",
    )

def get_data():
    print("Loading environment variables...")
    load_dotenv()
    print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id
    )

    query = """
    SELECT * FROM `toke-analytics.australia.au_population_mart`
    """
    query_job = client.query(query)
    arrow_table = query_job.to_arrow()
    df = pl.from_arrow(arrow_table)
    return df

df = get_data()

def main():
    st.markdown("# Australian Population")


def plot_1():
    data_2012_df = df.filter(
        pl.col("year") >= 2012
    )

    unpivoted_df = data_2012_df.unpivot(
        index=["year"],
        on=["births", "deaths"],
        variable_name="type",
        value_name="quantity"
    )

    g = sns.lmplot(
        data=unpivoted_df,
        x="year",
        y="quantity",
        hue="type",
        palette="muted",
        ci=None,
        height=4,
        aspect=1.6,
        scatter_kws={"s": 100, "alpha": 1},
    )
    births_df = unpivoted_df.filter(
        pl.col("type") == "births"
    )
    deaths_df = unpivoted_df.filter(
        pl.col("type") == "deaths"
    )

    birth_model = sm.OLS(births_df["quantity"].to_numpy(), sm.add_constant(births_df["year"].to_numpy())).fit()
    birth_slope = birth_model.params[1]
    birth_intercept = birth_model.params[0]

    death_model = sm.OLS(deaths_df["quantity"].to_numpy(), sm.add_constant(deaths_df["year"].to_numpy())).fit()
    death_slope = death_model.params[1]
    death_intercept = death_model.params[0]

    for ax in g.axes.flat:
        equation = f"y = {birth_slope:.2f}year + {birth_intercept:.2f}"
        ax.text(0.05, 0.85, equation, transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7)
            )
        equation2 = f"y = {death_slope:.2f}year + {death_intercept:.2f}"
        ax.text(0.55, 0.35, equation2, transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7)
            )

    g.figure.suptitle("Births and Deaths in Australia 2012-2024", y=1.02)
    st.markdown("## Births and Deaths in Australia 2012-2024")
    st.pyplot(g)

def plot_population():
    data_1982_df = df.filter(
        pl.col("year") >= 1982
    )
    data_1982_df = data_1982_df.with_columns((pl.col("total") / 1e6).alias("pop_total"))

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(
        data=data_1982_df,
        x="year",
        y="pop_total",
        palette="muted",
        ax=ax
    )
    ax.set_title("Australian Population Growth Since 1982")
    ax.set_xlabel("Year")
    ax.set_ylabel("Population (millions)")
    st.header("Australian Population Since 1982")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
    plot_population()
    st.markdown("""
        The graph above shows that Australia's population has grown from approximately 15 million in 1982 to over 27 million in 2024. As the population increases, one would expect the number of births and deaths to rise accordingly.
        """)
    plot_1()
    st.markdown("""
        However, when we look at the trend shown above, the number of births has not increased with the population as expected since 2012. The number of deaths, on the other hand, increases as anticipated alongside population growth. This raises important questions: What are the major factors influencing Australians' decisions to have fewer children? Is it the cost of living? Changing attitudes toward family? Career priorities? A shift away from traditional values? Can we find answers to these questions through further data analysis?
        """)

