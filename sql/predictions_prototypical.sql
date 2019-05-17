DROP TABLE prototypical;
CREATE TABLE prototypical AS
SELECT
    incorrect_predictions_selected.prediction AS prediction,
    incorrect_predictions_selected.actualSource AS actualSource,
    incorrect_predictions_selected.title AS title,
    incorrect_predictions_selected.predictionScore AS predictionScore
FROM
    incorrect_predictions
AS
    incorrect_predictions_selected
WHERE
    incorrect_predictions_selected.title IN (
        SELECT
            incorrect_predictions_candidate.title
        FROM
            incorrect_predictions
        AS
            incorrect_predictions_candidate
        WHERE
            incorrect_predictions_candidate.prediction = incorrect_predictions_selected.prediction
            AND incorrect_predictions_candidate.actualSource = incorrect_predictions_selected.actualSource
        ORDER BY incorrect_predictions_candidate.predictionScore DESC
        LIMIT 1
    );

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;

INSERT INTO prototypical (prediction, actualSource, title, predictionScore)
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
ORDER BY predictionScore DESC
LIMIT 1;
