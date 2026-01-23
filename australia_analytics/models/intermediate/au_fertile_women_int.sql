WITH au_pop AS (
    SELECT PARSE_DATE('%Y-%m-%d 00:00:00', date) AS stat_date, state, gender, age, count
    FROM {{ ref('stg_au_age_gender_population') }}
    WHERE gender = 'female' AND (age >= 15 AND age <= 49)
),
au_pop_int AS (
SELECT
    EXTRACT(YEAR FROM stat_date) AS year,
    EXTRACT(MONTH FROM stat_date) AS month,
    state,
    gender,
    age,
    count
FROM au_pop
)
SELECT
    year,
    state,
    gender,
    SUM(count) qty
FROM au_pop_int
GROUP BY year, state, gender
ORDER BY year, state, gender

