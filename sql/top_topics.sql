SELECT
	topics_percentages.maxTopic AS maxTopic,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'BBC' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'BBC' THEN 1
                ELSE 0
            END
        )
    ) AS bbcPercent,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'Breitbart' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Breitbart' THEN 1
                ELSE 0
            END
        )
    ) AS brietbartPercent,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'CNN' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'CNN' THEN 1
                ELSE 0
            END
        )
    ) AS cnnPercent,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'Daily Mail' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Daily Mail' THEN 1
                ELSE 0
            END
        )
    ) AS dailyMailPercent,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'Drudge Report' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Drudge Report' THEN 1
                ELSE 0
            END
        )
    ) AS drudgeReportPercent,
    (
    	sum(
            CASE
                WHEN topics_percentages.actualSource = 'NPR' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'NPR' THEN 1
                ELSE 0
            END
        )
    ) AS nprPercent,
    (
        sum(
            CASE
                WHEN topics_percentages.actualSource = 'New York Times' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'New York Times' THEN 1
                ELSE 0
            END
        )
    ) AS newYorkTimesPercent,
    (
        sum(
            CASE
                WHEN topics_percentages.actualSource = 'Vox' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Vox' THEN 1
                ELSE 0
            END
        )
    ) AS voxPercent,
    (
        sum(
            CASE
                WHEN topics_percentages.actualSource = 'Wall Street Journal' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Wall Street Journal' THEN 1
                ELSE 0
            END
        )
    ) AS wallStreetJournalPercent,
    (
        sum(
            CASE
                WHEN topics_percentages.actualSource = 'Fox' THEN topics_percentages.percent
                ELSE 0
            END
        ) / sum(
            CASE
                WHEN topics_percentages.actualSource = 'Fox' THEN 1
                ELSE 0
            END
        )
    ) AS foxPercent
FROM
	topics_percentages
INNER JOIN
	(
		SELECT
			maxTopic
		FROM
			topics_percentages
		WHERE
			topics_percentages.percent >= 0.05
	) top_topics
ON
	top_topics.maxTopic = topics_percentages.maxTopic
GROUP BY topics_percentages.maxTopic
