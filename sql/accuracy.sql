SELECT
	sums.setAssignment AS setAssignment,
	sums.correctCnt / sums.totalCnt AS accuracy
FROM
	(
		SELECT
			setAssignment AS setAssignment,
			sum(
				CASE
					WHEN predictions.actualSource = predictions.prediction THEN 1.0
					ELSE 0.0
				END
			) AS correctCnt,
			count(1) AS totalCnt
		FROM
			predictions
		GROUP BY
			setAssignment
	) sums
ORDER BY sums.setAssignment
