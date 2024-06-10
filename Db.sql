CREATE DATABASE RaceDb;

CREATE TABLE Circuits (
    circuitId INT PRIMARY KEY,
    circuitRef VARCHAR(255),
    circuitName VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255),
    lat FLOAT,
    lng FLOAT,
    alt INT,
    url VARCHAR(255)
);

CREATE TABLE Races (
    raceId INT PRIMARY KEY,
    year INT,
    round INT,
    circuitId INT,
    name VARCHAR(255),
    date DATE,
    time TIME,
    url VARCHAR(255),
    fp1_date DATE,
    fp1_time TIME,
    fp2_date DATE,
    fp2_time TIME,
    fp3_date DATE,
    fp3_time TIME,
    quali_date DATE,
    quali_time TIME,
    sprint_date DATE,
    sprint_time TIME,
    FOREIGN KEY (circuitId) REFERENCES Circuits(circuitId)
);

CREATE TABLE Drivers (
    driverId INT PRIMARY KEY,
    driverRef VARCHAR(255),
    number INT,
    code VARCHAR(3),
    forename VARCHAR(255),
    surname VARCHAR(255),
    dob DATE,
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE Constructors (
    constructorId INT PRIMARY KEY,
    constructorRef VARCHAR(255),
    name VARCHAR(255),
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE Status (
    statusId INT PRIMARY KEY,
    status VARCHAR(255)
);

CREATE TABLE Results (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number INT,
    grid INT,
    position INT,
    positionText VARCHAR(255),
    positionOrder INT,
    points FLOAT,
    laps INT,
    time VARCHAR(255),
    milliseconds INT,
    fastestLap INT,
    rank INT,
    fastestLapTime TIME,
    fastestLapSpeed FLOAT,
    statusId INT,
    FOREIGN KEY (raceId) REFERENCES Races(raceId),
    FOREIGN KEY (driverId) REFERENCES Drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES Constructors(constructorId),
    FOREIGN KEY (statusId) REFERENCES Status(statusId)
);

CREATE TABLE PitStops (
    raceId INT,
    driverId INT,
    stop INT,
    lap INT,
    time TIME,
    duration TIME,
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, stop),
    FOREIGN KEY (raceId) REFERENCES Races(raceId),
    FOREIGN KEY (driverId) REFERENCES Drivers(driverId)
);

CREATE TABLE LapTimes (
    raceId INT,
    driverId INT,
    lap INT,
    position INT,
    time TIME,
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, lap),
    FOREIGN KEY (raceId) REFERENCES Races(raceId),
    FOREIGN KEY (driverId) REFERENCES Drivers(driverId)
);

CREATE TABLE DriverStandings (
    driverStandingsId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    points FLOAT,
    position INT,
    positionText VARCHAR(255),
    wins INT,
    FOREIGN KEY (raceId) REFERENCES Races(raceId),
    FOREIGN KEY (driverId) REFERENCES Drivers(driverId)
);

CREATE TABLE ConstructorStandings (
    constructorStandingsId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points FLOAT,
    position INT,
    positionText VARCHAR(255),
    wins INT,
    FOREIGN KEY (raceId) REFERENCES Races(raceId),
    FOREIGN KEY (constructorId) REFERENCES Constructors(constructorId)
);


CREATE TABLE Weather (
    weatherId INT PRIMARY KEY,
    circuitId INT,
    country VARCHAR(255),
    location VARCHAR(255),
    date DATE,
    time TIME,
    tempMax FLOAT,
    tempMin FLOAT,
    temp FLOAT,
    feelsLikeMax FLOAT,
    feelsLikeMin FLOAT,
    feelsLike FLOAT,
    dew FLOAT,
    humidity FLOAT,
    precip FLOAT,
    precipProb FLOAT,
    precipCover FLOAT,
    precipType VARCHAR(50),
    snow FLOAT,
    snowDepth FLOAT,
    windGust FLOAT,
    windSpeed FLOAT,
    windDir INT,
    seaLevelPressure FLOAT,
    cloudCover FLOAT,
    visibility FLOAT,
    solarRadiation FLOAT,
    solarEnergy FLOAT,
    uvIndex INT,
    severeRisk INT,
    conditions VARCHAR(255),
    description TEXT,
    icon VARCHAR(50),
    stations TEXT,
    FOREIGN KEY (circuitId) REFERENCES Circuits (circuitId)
);