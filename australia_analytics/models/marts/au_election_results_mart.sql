WITH all_preferences AS (
    SELECT * FROM {{ ref('stg_election_distribution') }}
    WHERE CalculationType IN ('Transfer Count', 'Preference Count')
),
     sum_calculation_value AS (
         SELECT StateAb, DivisionId, DivisionNm, PPNm, CountNum, CandidateId, SUM(CalculationValue) SumCalculationValue
         FROM all_preferences
         GROUP BY StateAb, DivisionId, DivisionNm, PPNm, CountNum, CandidateId
     ),
     max_rounds AS (
         SELECT StateAb, DivisionId, DivisionNm, PPNm, Max(CountNum) MaxCountNum
         FROM all_preferences
         GROUP BY StateAb, DivisionId, DivisionNm, PPNm
     ),
     max_round_preferences AS (
         SELECT a.*, MaxCountNum FROM all_preferences a
                                          JOIN max_rounds m USING(StateAb, DivisionId, DivisionNm, PPNm)
     ),
     max_round_with_sum_calculation_value AS (
         SELECT a.*, b.SumCalculationValue FROM max_round_preferences a
                                                    JOIN sum_calculation_value b USING(StateAb, DivisionId, DivisionNm, PPNm, CountNum, CandidateId)
     ),
     first_round_results AS (
         SELECT RANK() OVER (PARTITION BY StateAb, DivisionId, DivisionNm, PPNm, CountNum ORDER BY SumCalculationValue DESC) AS FirstRoundRanking, *
         FROM max_round_with_sum_calculation_value
         WHERE CountNum = 0
     ),
     last_round_results AS (
         SELECT RANK() OVER (PARTITION BY StateAb, DivisionId, DivisionNm, PPNm, CountNum ORDER BY SumCalculationValue DESC) AS LastRoundRanking, *
         FROM max_round_with_sum_calculation_value
         WHERE CountNum = MaxCountNum
     )
SELECT DISTINCT f.StateAb,	f.DivisionId,	f.DivisionNm,	f.PPId,	f.PPNm,	f.BallotPosition,	f.CandidateId,	f.Surname,	GivenNm,	f.PartyAb,	f.PartyNm, f.FirstRoundRanking,	f.SumCalculationValue FirstRoundTotalValue, l.LastRoundRanking, l.SumCalculationValue LastRoundTotalValue FROM first_round_results f
                                                                                                                                                                                                                                                                                                                           JOIN last_round_results l USING(StateAb, DivisionId, DivisionNm, PPid, PPNm, BallotPosition, CandidateId, Surname, GivenNm, PartyAb, PartyNm)
ORDER BY f.StateAb,	f.DivisionId,	f.DivisionNm,	f.PPId,	f.PPNm, f.FirstRoundRanking, l.LastRoundRanking
