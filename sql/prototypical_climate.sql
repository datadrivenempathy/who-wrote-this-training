CREATE TABLE prototypical_climate AS
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "BBC"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Breitbart"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "CNN"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Daily Mail"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Drudge Report"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "NPR"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "New York Times"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Vox"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Wall Street Journal"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_climate (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Fox"
    AND lower(title) like "%climate%"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;
