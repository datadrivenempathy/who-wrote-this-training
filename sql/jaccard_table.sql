SELECT
    source1,
    MAX(
        CASE
            WHEN source2 = "BBC" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS bbcPrototypical,
    MAX(
        CASE
            WHEN source2 = "Breitbart" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS breitbartPrototypical,
    MAX(
        CASE
            WHEN source2 = "CNN" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS cnnPrototypical,
    MAX(
        CASE
            WHEN source2 = "Daily Mail" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS dailyMailPrototypical,
    MAX(
        CASE
            WHEN source2 = "Drudge Report" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS drudgeReportPrototypical,
    MAX(
        CASE
            WHEN source2 = "Fox" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS foxPrototypical,
    MAX(
        CASE
            WHEN source2 = "NPR" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS nprPrototypical,
    MAX(
        CASE
            WHEN source2 = "New York Times" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS newYorkTimesPrototypical,
    MAX(
        CASE
            WHEN source2 = "Vox" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS voxPrototypical,
    MAX(
        CASE
            WHEN source2 = "Wall Street Journal" THEN jaccardIndex * 100
            ELSE 0
        END
    ) AS wallStreetJournalPrototypical
FROM
    jaccards
GROUP BY
    source1
