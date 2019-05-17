SELECT
	joined.title AS title,
	joined.link AS link,
	joined.actualSource AS actualSource,
	(
		CASE
			WHEN joined.actualSource = "CNN" THEN joined.cnnScore
			WHEN joined.actualSource = "Fox" THEN joined.foxScore
			WHEN joined.actualSource = "Daily Mail" THEN joined.dailyMailScore
			WHEN joined.actualSource = "Drudge Report" THEN joined.drudgeReportScore
			WHEN joined.actualSource = "New York Times" THEN joined.newYorkTimesScore
			WHEN joined.actualSource = "BBC" THEN joined.bbcScore
			WHEN joined.actualSource = "Breitbart" THEN joined.breitbartScore
			WHEN joined.actualSource = "Wall Street Journal" THEN joined.wallStreetJournalScore
			WHEN joined.actualSource = "Vox" THEN joined.voxScore
			WHEN joined.actualSource = "NPR" THEN joined.nprScore
			ELSE -1
		END
	) AS score
FROM
	(
		SELECT
			predictions.title AS title,
		    (
		        CASE
		            WHEN links_grouped.link isnull THEN ''
		            ELSE links_grouped.link
		        END
		    ) AS link,
			predictions.actualSource AS actualSource,
			predictions.prediction AS predictedSource,
			predictions.cnnScore AS cnnScore,
			predictions.foxScore AS foxScore,
			predictions.dailyMailScore AS dailyMailScore,
			predictions.drudgeReportScore AS drudgeReportScore,
			predictions.newYorkTimesScore AS newYorkTimesScore,
			predictions.bbcScore AS bbcScore,
			predictions.breitbartScore AS breitbartScore,
			predictions.wallStreetJournalScore AS wallStreetJournalScore,
			predictions.voxScore AS voxScore,
			predictions.nprScore AS nprScore
		FROM
			predictions
		INNER JOIN
		    (
		        SELECT
		            title,
		            source,
		            link
		        FROM
		            articles
		        GROUP BY
		            title,
		            source
		    ) links_grouped
		ON
		    predictions.title = links_grouped.title
		    AND predictions.actualSource = links_grouped.source
	) joined
WHERE
	joined.predictedSource = joined.actualSource
