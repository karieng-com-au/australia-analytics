SELECT *
FROM {{ source("au_raw_data", "australia_age_gender_population")}}
