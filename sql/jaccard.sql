CREATE VIEW jaccards AS
SELECT
	with_totals.source1 AS source1,
	with_totals.source2 AS source2,
	(with_totals.overlapCount + 0.0) / with_totals.totalCount AS jaccardIndex,
	with_totals.overlapCount AS overlapCount,
	with_totals.totalCount AS totalCount
FROM
	(
		SELECT
			with_partial_totals.source1 AS source1,
			with_partial_totals.source2 AS source2,
			sum(with_partial_totals.overlapCount) AS overlapCount,
			sum(with_partial_totals.totalCount + counts_2.totalCount) AS totalCount
		FROM
			(
				SELECT
					overlaps.source1 AS source1,
					overlaps.source2 AS source2,
					overlaps.overlapCount AS overlapCount,
					counts_1.totalCount AS totalCount
				FROM
					(
						SELECT
							unordered_unsummed.source1 AS source1,
							unordered_unsummed.source2 AS source2,
							sum(overlapCount) AS overlapCount
						FROM
							(
								SELECT
									(
										CASE
											WHEN source1 < source2 THEN source1
											ELSE source2
										END
									) AS source1,
									(
										CASE
											WHEN source1 > source2 THEN source1
											ELSE source2
										END
									) AS source2,
									overlapCount
								FROM
									(
										SELECT
											count(1) AS overlapCount,
											prediction AS source1,
											actualSource AS source2
										FROM
											predictions
										GROUP BY
											prediction,
											actualSource
									) ordered_overlap
							) unordered_unsummed
						WHERE
							source1 != source2
						GROUP BY
							unordered_unsummed.source1,
							unordered_unsummed.source2
					) overlaps
				INNER JOIN
					(
						SELECT
							prediction AS source,
							count(1) AS totalCount
						FROM
							predictions
						GROUP BY
							prediction
					) counts_1
				ON
					overlaps.source1 = counts_1.source
			) with_partial_totals
		INNER JOIN
			(
				SELECT
					prediction AS source,
					count(1) AS totalCount
				FROM
					predictions
				GROUP BY
					prediction
			) counts_2
		GROUP BY
			source1, source2
	) with_totals;
