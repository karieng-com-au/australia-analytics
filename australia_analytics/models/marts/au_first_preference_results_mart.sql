WITH first_preferences AS (
  SELECT * FROM `australia.au_first_count_results_mart` WHERE FirstRoundRanking = 1
)
SELECT
  PartyAb,
  Victorious,
  COUNT(Victorious) Counts
FROM first_preferences
GROUP BY PartyAb, Victorious
ORDER BY PartyAb, Victorious DESC
