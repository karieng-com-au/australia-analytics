SELECT *
FROM {{ source("au_raw_data", "australia_population")}}
