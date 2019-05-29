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
			predictions_orig_title.title AS title,
		    (
		        CASE
		            WHEN links_grouped.link isnull THEN ''
		            ELSE links_grouped.link
		        END
		    ) AS link,
			predictions_orig_title.actualSource AS actualSource,
			predictions_orig_title.prediction AS predictedSource,
			predictions_orig_title.cnnScore AS cnnScore,
			predictions_orig_title.foxScore AS foxScore,
			predictions_orig_title.dailyMailScore AS dailyMailScore,
			predictions_orig_title.drudgeReportScore AS drudgeReportScore,
			predictions_orig_title.newYorkTimesScore AS newYorkTimesScore,
			predictions_orig_title.bbcScore AS bbcScore,
			predictions_orig_title.breitbartScore AS breitbartScore,
			predictions_orig_title.wallStreetJournalScore AS wallStreetJournalScore,
			predictions_orig_title.voxScore AS voxScore,
			predictions_orig_title.nprScore AS nprScore
		FROM
			(
				SELECT
					transformation_bridge.originalTitle AS title,
					predictions.actualSource AS actualSource,
					predictions.prediction AS prediction,
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
					transformation_bridge
				ON
					transformation_bridge.newTitle = predictions.title
					AND transformation_bridge.source = predictions.actualSource
				GROUP BY
					transformation_bridge.originalTitle,
					predictions.actualSource
			) predictions_orig_title
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
		    predictions_orig_title.title = links_grouped.title
		    AND predictions_orig_title.actualSource = links_grouped.source
	) joined
WHERE
	joined.predictedSource = joined.actualSource
ORDER BY
	score DESC, length(title) DESC
