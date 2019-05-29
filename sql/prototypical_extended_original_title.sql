CREATE VIEW prototypical_extended_original_title AS
SELECT
    prototypical_extended.prediction AS prediction,
    prototypical_extended.actualSource AS actualSource,
    transformation_bridge.originalTitle AS title,
    prototypical_extended.predictionScore AS predictionScore
FROM
    prototypical_extended
LEFT JOIN
    transformation_bridge
ON
    transformation_bridge.newTitle = prototypical_extended.title
    AND transformation_bridge.source = prototypical_extended.actualSource
