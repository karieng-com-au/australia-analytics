WITH au_overall  AS (
    {{ dbt_utils.unpivot(
        relation=ref('stg_au_births_deaths'),
        cast_to='integer',
        exclude=['name'],
        field_name='data_type',
        value_name='value'
    ) }}
)
SELECT
    PARSE_DATE('%Y-%m-%d 00:00:00', name) date,
    data_type,
    value
FROM au_overall
ORDER BY date, data_type
