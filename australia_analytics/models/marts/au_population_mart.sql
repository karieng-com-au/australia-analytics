
WITH au_pops AS (
    SELECT * FROM `australia.au_population_int`
),
au_pops_int AS (
  SELECT
      EXTRACT(YEAR FROM date) AS year,
      EXTRACT(MONTH FROM date) AS month,
      state,
      male,
      female,
      total
  FROM au_pops
),
au_pops_sum AS (
SELECT year, month, SUM(male) male, SUM(female) female, SUM(total) total
FROM au_pops_int
WHERE month = 12
GROUP BY year, month
), au_pops_final AS (
SELECT
  year,
  CAST(male AS INT64) male,
  CAST(female AS INT64) female,
  CAST(total AS INT64) total
FROM au_pops_sum
),
au_births_deaths AS (
    SELECT year, births, deaths FROM {{ ref("au_annual_births_int") }}
),
au_immigration AS (
    SELECT year, oversea_arrival, oversea_departure, migration_adjustment, net_migration FROM {{ ref("au_immigration_int") }}
),
fertile_women AS (
SELECT * FROM `australia.au_fertile_women_int`
), fertile_women_int AS (
SELECT year, SUM(qty) women_15_to_49
FROM fertile_women GROUP BY year
)
SELECT p.year,
       male,
       female,
       women_15_to_49,
       total,
       births,
       deaths,
       oversea_arrival,
       oversea_departure,
       migration_adjustment,
       net_migration

FROM au_pops_final p
JOIN au_births_deaths b
ON p.year = b.year
JOIN au_immigration i
ON p.year = i.year
JOIN fertile_women_int f
ON p.year = f.year
ORDER BY p.year
