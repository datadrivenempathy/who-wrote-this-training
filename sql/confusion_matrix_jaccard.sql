SELECT
    prediction,
    SUM(
        CASE
            WHEN actualSource = "BBC" THEN jaccardIndex
            ELSE 0
        END
    ) AS bbcIdx,
    SUM(
        CASE
            WHEN actualSource = "Breitbart" THEN jaccardIndex
            ELSE 0
        END
    ) AS breitbartIdx,
    SUM(
        CASE
            WHEN actualSource = "CNN" THEN jaccardIndex
            ELSE 0
        END
    ) AS cnnIdx,
    SUM(
        CASE
            WHEN actualSource = "Daily Mail" THEN jaccardIndex
            ELSE 0
        END
    ) AS dailyMailIdx,
    SUM(
        CASE
            WHEN actualSource = "Drudge Report" THEN jaccardIndex
            ELSE 0
        END
    ) AS drudgeReportIdx,
    SUM(
        CASE
            WHEN actualSource = "Fox" THEN jaccardIndex
            ELSE 0
        END
    ) AS foxIdx,
    SUM(
        CASE
            WHEN actualSource = "NPR" THEN jaccardIndex
            ELSE 0
        END
    ) AS nprIdx,
    SUM(
        CASE
            WHEN actualSource = "New York Times" THEN jaccardIndex
            ELSE 0
        END
    ) AS newYorkTimesIdx,
    SUM(
        CASE
            WHEN actualSource = "Vox" THEN jaccardIndex
            ELSE 0
        END
    ) AS voxIdx,
    SUM(
        CASE
            WHEN actualSource = "Wall Street Journal" THEN jaccardIndex
            ELSE 0
        END
    ) AS wallStreetJournalIdx
FROM
    jaccards
GROUP BY
    prediction
