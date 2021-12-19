CREATE DATABASE IF NOT EXISTS DATA;
CREATE TABLE IF NOT EXISTS DATA.SENSOR_DATA( 
	ID INT(6) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    DEV_EUI VARCHAR(20) NOT NULL,
    LATITUDE DECIMAL(11,7) NOT NULL,
    LONGITUDE DECIMAL(11,7) NOT NULL,
    LOCATION VARCHAR(30) NOT NULL,
    PUBLISH_TIME timestamp NOT NULL DEFAULT current_timestamp(),
    TEMP DECIMAL (3,1) NOT NULL
    );
    
-- Test 
#INSERT INTO DATA.SENSOR_DATA (DEV_EUI, LATITUDE, LONGITUDE, LOCATION, TEMP) VALUES ("6983F9D1BAF7C83C", 51.55871291510539, 4.57910418773288, "Antwerep", 8); 
#SELECT * FROM DATA.SENSOR_DATA;
-- SELECT * FROM DATA.SENSOR_DATA WHERE PUBLISH_TIME >= now() - INTERVAL 1 DAY;
-- SELECT DEV_EUI FROM DATA.SENSOR_DATA GROUP BY DEV_EUI;

-- SELECT DEV_EUI, CAST(LATITUDE AS CHAR) AS LATITUDE, CAST(LONGITUDE AS CHAR) AS LONGITUDE, LOCATION, CAST(PUBLISH_TIME AS CHAR) AS PUBLISH_TIME, CAST(TEMP AS CHAR) AS TEMP FROM DATA.SENSOR_DATA WHERE DEV_EUI="6081F9D1BAF7C83C";


