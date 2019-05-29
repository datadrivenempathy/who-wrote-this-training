CREATE TABLE prototypical_general AS
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "BBC"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Breitbart"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "CNN"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Daily Mail"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Drudge Report"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "NPR"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "New York Times"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Vox"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Wall Street Journal"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;

INSERT INTO prototypical_general (prediction, actualSource, title, predictionScore)
SELECT
    prediction,
    actualSource,
    title,
    predictionScore
FROM
    predictions_top_score
WHERE
    prediction = "Fox"
    AND prediction = actualSource
ORDER BY predictionScore DESC, length(title) DESC
LIMIT 1;
