WITH first_count_results AS (
  SELECT
    StateAb,
    DivisionId,
    DivisionNm,
    CountNum,
    CandidateId,
    SUM(CalculationValue) FirstCountTotalVotes
  FROM {{ ref('stg_election_distribution')}}
  WHERE CountNum = 0 AND CalculationType = 'Preference Count'
  GROUP BY StateAb, DivisionId, DivisionNm, CountNum, CandidateId
),
ranked_results AS (
SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY StateAb, DivisionId, DivisionNm, CountNum ORDER BY FirstCountTotalVotes DESC) AS RankingNumber
FROM first_count_results
),
district_total_votes AS (
SELECT StateAb, DivisionId, DivisionNm, SUM(FirstCountTotalVotes) DistrictTotalVotes
FROM ranked_results
GROUP BY StateAb, DivisionId, DivisionNm
)
SELECT r.*, d.DistrictTotalVotes FROM ranked_results r
JOIN district_total_votes d ON r.StateAb = d.StateAb AND r.DivisionId = d.DivisionId
