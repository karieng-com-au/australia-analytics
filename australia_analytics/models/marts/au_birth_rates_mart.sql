WITH au_women AS (
    SELECT * FROM {{ ref("au_fertile_women_int") }}
),
au_births AS (
    SELECT * FROM {{ ref("au_annual_births_int") }}
),
au_women_agg AS (
    SELECT year, SUM(qty) num_women
    FROM au_women
    GROUP BY year
)
SELECT w.year,
num_women,
births,
(births/num_women) as birth_rate
FROM au_women_agg w
JOIN au_births b
ON w.year = b.year
ORDER BY w.year

