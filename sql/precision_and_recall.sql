SELECT
	source_totals.source AS source,
	(prediction_totals.correctCount + 0.0) / prediction_totals.totalCnt AS precision,
	(prediction_totals.correctCount + 0.0) / source_totals.totalCnt AS recall,
	prediction_totals.correctCount AS correctCount,
	prediction_totals.totalCnt AS totalPredictions,
	source_totals.totalCnt AS totalInSource
FROM
	(
		SELECT
			actualSource AS source,
			count(1) AS totalCnt
		FROM
			predictions
		WHERE
			setAssignment = "validation"
		GROUP BY
			actualSource
	) source_totals
LEFT JOIN
	(
		SELECT
			prediction AS source,
			sum(
				CASE
					WHEN prediction = actualSource THEN 1
					ELSE 0
				END
			) AS correctCount,
			count(1) AS totalCnt
		FROM
			predictions
		WHERE
			setAssignment = "validation"
		GROUP BY
			prediction
	) prediction_totals
ON
	source_totals.source = prediction_totals.source
	
