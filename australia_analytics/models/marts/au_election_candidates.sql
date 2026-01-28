WITH all_candidates AS (
    SELECT StateAb, DivisionId, DivisionNm, CandidateId, Surname, GivenNm, PartyAb, PartyNm, SittingMemberFl
    FROM {{ ref("stg_election_distribution") }}
)
SELECT DISTINCT *
FROM all_candidates
ORDER BY StateAb, DivisionId, DivisionNm, CandidateId, Surname
