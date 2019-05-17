SELECT
    prediction,
    MAX(
        CASE
            WHEN actualSource = "BBC" THEN title
            ELSE ""
        END
    ) AS bbcPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Breitbart" THEN title
            ELSE ""
        END
    ) AS breitbartPrototypical,
    MAX(
        CASE
            WHEN actualSource = "CNN" THEN title
            ELSE ""
        END
    ) AS cnnPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Daily Mail" THEN title
            ELSE ""
        END
    ) AS dailyMailPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Drudge Report" THEN title
            ELSE ""
        END
    ) AS drudgeReportPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Fox" THEN title
            ELSE ""
        END
    ) AS foxPrototypical,
    MAX(
        CASE
            WHEN actualSource = "NPR" THEN title
            ELSE ""
        END
    ) AS nprPrototypical,
    MAX(
        CASE
            WHEN actualSource = "New York Times" THEN title
            ELSE ""
        END
    ) AS newYorkTimesPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Vox" THEN title
            ELSE ""
        END
    ) AS voxPrototypical,
    MAX(
        CASE
            WHEN actualSource = "Wall Street Journal" THEN title
            ELSE ""
        END
    ) AS wallStreetJournalPrototypical
FROM
    prototypical
GROUP BY
    prediction
