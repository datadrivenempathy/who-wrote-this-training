SELECT
	match.actualSource AS Source,
	match.prediction AS Target,
	round((match.matchCount + 0.0) / prediction_cnts.predictionCount * 100) AS Weight
FROM
	(
		SELECT
			actualSource,
			prediction,
			count(1) AS matchCount
		FROM
			predictions
		GROUP BY
			actualSource,
			prediction
	) match
INNER JOIN
	(
		SELECT
			prediction,
			count(1) AS predictionCount
		FROM
			predictions
		GROUP BY
			prediction
	) prediction_cnts
ON
	match.prediction = prediction_cnts.prediction
