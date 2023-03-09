## DDL
```
CREATE TABLE `airline` (
  `airlineID` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`airlineID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
```
CREATE TABLE `airports` (
  `airportID` varchar(45) NOT NULL,
  `AIRPORT` varchar(45) DEFAULT NULL,
  `CITY` varchar(45) DEFAULT NULL,
  `STATE` varchar(45) DEFAULT NULL,
  `COUNTRY` varchar(45) DEFAULT NULL,
  `LATITUDE` double DEFAULT NULL,
  `LONGITUDE` double DEFAULT NULL,
  PRIMARY KEY (`airportID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
```
CREATE TABLE `cancellations` (
  `type` int NOT NULL,
  `reason` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
```
CREATE TABLE `delays` (
  `DATE` date NOT NULL,
  `AIRLINE` varchar(45) NOT NULL,
  `FLIGHT_NUMBER` int NOT NULL,
  `SCHEDULED_DEPARTURE` int NOT NULL,
  `AIR_SYSTEM_DELAY` int DEFAULT NULL,
  `SECURITY_DELAY` int DEFAULT NULL,
  `AIRLINE_DELAY` int DEFAULT NULL,
  `LATE_AIRCRAFT_DELAY` int DEFAULT NULL,
  `WEATHER_DELAY` int DEFAULT NULL,
  PRIMARY KEY (`DATE`,`AIRLINE`,`FLIGHT_NUMBER`,`SCHEDULED_DEPARTURE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
```
CREATE TABLE `flights` (
  `DATE` date NOT NULL,
  `AIRLINE` varchar(45) NOT NULL,
  `FLIGHT_NUMBER` int NOT NULL,
  `TAIL_NUMBER` varchar(6) DEFAULT NULL,
  `ORIGIN_AIRPORT` varchar(3) NOT NULL,
  `DESTINATION_AIRPORT` varchar(3) DEFAULT NULL,
  `SCHEDULED_DEPARTURE` int NOT NULL,
  `SCHEDULED_ARRIVAL` int NOT NULL,
  `CANCELLATION_TYPE` int DEFAULT NULL,
  PRIMARY KEY (`DATE`,`AIRLINE`,`FLIGHT_NUMBER`,`ORIGIN_AIRPORT`,`SCHEDULED_DEPARTURE`,`SCHEDULED_ARRIVAL`),
  KEY `AIRLINE_idx` (`AIRLINE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
```
CREATE TABLE `planes` (
  `AIRLINE` varchar(45) NOT NULL,
  `TAIL_NUMBER` varchar(45) NOT NULL,
  PRIMARY KEY (`AIRLINE`,`TAIL_NUMBER`),
  CONSTRAINT `AIRLINE` FOREIGN KEY (`AIRLINE`) REFERENCES `airline` (`airlineID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```
## Adding Data to Tables
Only displaying the tables with over 1000 rows:
<img src="images/delays count.png" width="100">
<img src="images/flights count.png" width="100">
<img src="images/planes count.png" width="100">

## Advanced Queries

Total Number of Cancelled Flights for Each Airport:

<img src="images/advanced query 1.png" width="600">

Average Delay Time for Each Airline

<img src="images/advanced query 2.png" width="600">
