WITH au_births AS (
    select
        PARSE_DATE('%Y-%m-%d 00:00:00', name) as date,
        CAST(birth AS INT64) as birth,
        CAST(death AS INT64) as death
    from {{ ref('stg_au_births_deaths') }}
),
au_births_int AS (
SELECT
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    birth,
    death
FROM au_births
)
SELECT
    year,
    SUM(birth) births,
    SUM(death) deaths
FROM au_births_int
GROUP BY year
ORDER BY year

