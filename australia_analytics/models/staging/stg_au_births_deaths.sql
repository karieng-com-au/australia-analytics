SELECT *
FROM {{ source("au_raw_data", "australia_births_deaths")}}
