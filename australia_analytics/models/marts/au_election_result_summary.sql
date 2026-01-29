WITH winners AS (
  SELECT *
  FROM `australia.au_first_count_results_mart`
  WHERE Victorious = 'Y'
)
SELECT PartyAb, COUNT(*) AS WinCount
FROM winners GROUP BY PartyAb ORDER BY WinCount DESC, PartyAb
