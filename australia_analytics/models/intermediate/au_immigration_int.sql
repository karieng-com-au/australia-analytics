WITH au_immi AS (
SELECT
PARSE_DATE('%Y-%m-%d 00:00:00', name) AS date,
oversea_arrival,
oversea_departure,
migration_adjustment,
(oversea_arrival - oversea_departure + migration_adjustment) AS net_migration
FROM `australia.stg_au_births_deaths`
),
au_annual_immigration AS (
    SELECT date,
    EXTRACT(YEAR FROM date) AS year,
    oversea_arrival,
    oversea_departure,
    migration_adjustment,
    net_migration
    FROM au_immi
)
SELECT
    year,
    SUM(oversea_arrival) oversea_arrival,
    SUM(oversea_departure) oversea_departure,
    SUM(migration_adjustment) migration_adjustment,
    SUM(net_migration) net_migration
FROM au_annual_immigration
GROUP BY year
ORDER BY year
