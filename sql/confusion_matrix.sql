SELECT
    counts.prediction,
    100 * counts.bbcCount / counts.total AS bbcPercent,
    100 * counts.breitbartCount / counts.total AS breitbartPercent,
    100 * counts.cnnCount / counts.total AS cnnPercent,
    100 * counts.dailyMailCount / counts.total AS dailyMailPercent,
    100 * counts.drudgeReportCount / counts.total AS drudgeReportPercent,
    100 * counts.nprCount / counts.total AS nprPercent,
    100 * counts.newYorkTimesCount / counts.total AS newYorkTimesPercent,
    100 * counts.voxCount / counts.total AS voxPercent,
    100 * counts.wallStreetJournalCount / counts.total AS wallStreetJournalPercent,
	100 * counts.foxCount / counts.total AS foxPercent
FROM
    (
        SELECT
            prediction,
        	SUM(
        		CASE
        			WHEN actualSource = "BBC" THEN 1
        			ELSE 0
        		END
        	) AS bbcCount,
        	SUM(
        		CASE
        			WHEN actualSource = "Breitbart" THEN 1
        			ELSE 0
        		END
        	) AS breitbartCount,
        	SUM(
        		CASE
        			WHEN actualSource = "CNN" THEN 1
        			ELSE 0
        		END
        	) AS cnnCount,
        	SUM(
        		CASE
        			WHEN actualSource = "Daily Mail" THEN 1
        			ELSE 0
        		END
        	) AS dailyMailCount,
        	SUM(
        		CASE
        			WHEN actualSource = "Drudge Report" THEN 1
        			ELSE 0
        		END
        	) AS drudgeReportCount,
            SUM(
        		CASE
        			WHEN actualSource = "Fox" THEN 1
        			ELSE 0
        		END
        	) AS foxCount,
        	SUM(
        		CASE
        			WHEN actualSource = "NPR" THEN 1
        			ELSE 0
        		END
        	) AS nprCount,
        	SUM(
        		CASE
        			WHEN actualSource = "New York Times" THEN 1
        			ELSE 0
        		END
        	) AS newYorkTimesCount,
        	SUM(
        		CASE
        			WHEN actualSource = "Vox" THEN 1
        			ELSE 0
        		END
        	) AS voxCount,
        	SUM(
        		CASE
        			WHEN actualSource = "Wall Street Journal" THEN 1
        			ELSE 0
        		END
        	) AS wallStreetJournalCount,
        	count(1) + 0.0 AS total
        FROM
        	predictions
        GROUP BY
        	prediction
    ) counts
