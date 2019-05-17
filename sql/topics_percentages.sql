DROP VIEW topics_percentages;
CREATE VIEW topics_percentages AS
SELECT
	percentages.maxTopic AS maxTopic,
	percentages.actualSource AS actualSource,
	percentages.percent AS percent
FROM
	(
			SELECT
				topics.maxTopic AS maxTopic,
				topics.actualSource AS actualSource,
				(topics.cnt + 0.0) / totals.cnt AS percent
			FROM
				(
					SELECT
						maxTopic,
						actualSource,
						count(1) AS cnt
					FROM
						topics_and_sentiment
                    WHERE
                        maxTopicProb > 0.7
					GROUP BY
						maxTopic,
						actualSource
				) topics
			INNER JOIN
				(
					SELECT
						actualSource,
						count(1) AS cnt
					FROM
						topics_and_sentiment
                    WHERE
                        maxTopicProb > 0.7
					GROUP BY
						actualSource
				) totals
			ON
				totals.actualSource = topics.actualSource
	) percentages
ORDER BY percent DESC
