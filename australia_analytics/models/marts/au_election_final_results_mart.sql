WITH final_total_scores AS (
  SELECT * FROM {{ ref('au_election_results_mart')}}
  WHERE LastRoundTotalValue > 0
), final_results AS (
SELECT
  StateAb,
  DivisionId,
  DivisionNm,
  CandidateId,
  Surname,
  GivenNm,
  PartyAb,
  PartyNm,
  SUM(LastRoundTotalValue) TotalVotes
FROM final_total_scores
GROUP BY StateAb, DivisionId, DivisionNm, CandidateId, Surname,
  GivenNm,
  PartyAb,
  PartyNm
), final_ranking AS (
  SELECT *,
  ROW_NUMBER() OVER (PARTITION BY StateAb,
    DivisionId,
    DivisionNm ORDER BY TotalVotes DESC
  ) AS FinalRanking
FROM final_results
), final_ranking_with_victory AS (
SELECT *,
CASE
    WHEN FinalRanking = 1 THEN 'Y'
    ELSE 'N'
END AS Victorious
FROM final_ranking ORDER BY StateAb,
  DivisionId,
  DivisionNm,
  FinalRanking
),
district_total_votes AS (
    SELECT StateAb,
    DivisionId,
    DivisionNm,
    SUM(TotalVotes) DistrictTotalVotes
    FROM final_ranking_with_victory
    GROUP BY StateAb,
    DivisionId,
    DivisionNm
)
SELECT f.StateAb,
  f.DivisionId,
  f.DivisionNm,
  f.CandidateId,
  f.Surname,
  f.GivenNm,
  f.PartyAb,
  f.PartyNm,
  f.TotalVotes NumberOfVotes,
  t.DistrictTotalVotes,
  f.FinalRanking,
  f.Victorious
FROM final_ranking_with_victory f
JOIN district_total_votes t ON f.DivisionId = t.DivisionId
