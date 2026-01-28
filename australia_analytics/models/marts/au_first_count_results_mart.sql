WITH first_count_results AS (
    SELECT * FROM {{ ref("au_first_count_results_int") }}
),
final_results AS (
    SELECT * FROM {{ ref("au_election_final_results_mart") }}
),
candidates AS (
    SELECT * FROM {{ ref("au_election_candidates") }}
)
SELECT
a.StateAb,
a.DivisionId,
a.DivisionNm,
a.CountNum,
a.CandidateId,
c.Surname,
c.GivenNm,
c.PartyAb,
c.PartyNm,
c.SittingMemberFl,
a.FirstCountTotalVotes,
a.RankingNumber FirstRoundRanking,
b.NumberOfVotes NumberOfVotes,
b.DistrictTotalVotes DistrictTotalVotes,
b.FinalRanking,
b.Victorious
FROM first_count_results a
LEFT JOIN final_results b ON a.CandidateId = b.CandidateId AND a.StateAb = b.StateAb AND a.DivisionId = b.DivisionId
LEFT JOIN candidates c ON a.CandidateId = c.CandidateId
ORDER BY StateAb, DivisionNm, RankingNumber
