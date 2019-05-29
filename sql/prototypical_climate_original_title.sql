CREATE VIEW prototypical_climate_original_title AS
SELECT
    prototypical_climate.prediction AS prediction,
    prototypical_climate.actualSource AS actualSource,
    transformation_bridge.originalTitle AS title,
    prototypical_climate.predictionScore AS predictionScore
FROM
    prototypical_climate
LEFT JOIN
    transformation_bridge
ON
    transformation_bridge.newTitle = prototypical_climate.title
    AND transformation_bridge.source = prototypical_climate.actualSource
