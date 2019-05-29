CREATE VIEW prototypical_general_original_title AS
SELECT
    prototypical_general.prediction AS prediction,
    prototypical_general.actualSource AS actualSource,
    transformation_bridge.originalTitle AS title,
    prototypical_general.predictionScore AS predictionScore
FROM
    prototypical_general
LEFT JOIN
    transformation_bridge
ON
    transformation_bridge.newTitle = prototypical_general.title
    AND transformation_bridge.source = prototypical_general.actualSource
