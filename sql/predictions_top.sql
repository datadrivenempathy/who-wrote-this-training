DROP VIEW predictions_top_score;
CREATE VIEW predictions_top_score AS
SELECT
	unordered.prediction AS prediction,
	unordered.actualSource AS actualSource,
	unordered.title AS title,
	unordered.predictionScore AS predictionScore
FROM
	(
		SELECT
			prediction,
			actualSource,
			title,
			(
				CASE
					WHEN prediction = "BBC" THEN bbcScore
					WHEN prediction = "Breitbart" THEN breitbartScore
					WHEN prediction = "CNN" THEN cnnScore
					WHEN prediction = "Daily Mail" THEN dailyMailScore
					WHEN prediction = "Drudge Report" THEN drudgeReportScore
					WHEN prediction = "NPR" THEN nprScore
					WHEN prediction = "New York Times" THEN newYorkTimesScore
					WHEN prediction = "Vox" THEN voxScore
					WHEN prediction = "Wall Street Journal" THEN wallStreetJournalScore
					WHEN prediction = "Fox" THEN foxScore
					ELSE -1
				END
			) AS predictionScore
		FROM
			predictions
		ORDER BY predictionScore DESC
	) unordered
ORDER BY predictionScore DESC;


DROP VIEW incorrect_predictions;
CREATE VIEW incorrect_predictions AS
SELECT
	prediction,
	actualSource,
	title,
	predictionScore
FROM
	predictions_top_score
WHERE
	prediction != actualSource;
