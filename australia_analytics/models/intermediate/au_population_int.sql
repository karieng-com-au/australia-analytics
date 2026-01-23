WITH au_pops AS (
    SELECT * FROM {{ ref("stg_au_population") }}
)
SELECT
    PARSE_DATE('%Y-%m-%d 00:00:00', date) date,
    'population' as type,
    state,
    'australia' as country,
    male_population as male,
    female_population as female,
    total_population as total
FROM au_pops


