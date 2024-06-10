-- DIM TABLES AND FACT TABLE

-- DimDate table
CREATE TABLE DimDate (
    Date DATE PRIMARY KEY,
    Year INT,
    Month INT,
    MonthName VARCHAR(20),
    Day INT
);

-- DimCircuit table
CREATE TABLE DimCircuit (
    CircuitID INT PRIMARY KEY,
    CircuitRef VARCHAR(50),
    Name VARCHAR(100),
    City VARCHAR(50),
    Country VARCHAR(50)
);

-- DimConstructor table
CREATE TABLE DimConstructor (
    ConstructorID INT PRIMARY KEY,
    ConstructorRef VARCHAR(50),
    Name VARCHAR(100),
    Nationality VARCHAR(50)
);

-- DimDriver table
CREATE TABLE DimDriver (
    DriverID INT PRIMARY KEY,
    DriverRef VARCHAR(50),
    Number VARCHAR(10),
    Code VARCHAR(10),
    Forename VARCHAR(50),
    Surname VARCHAR(50),
    DOB DATE,
    Nationality VARCHAR(50)
);

-- DimRace
CREATE TABLE DimRace (
    RaceID INT PRIMARY KEY,
    Raceound INT,
    RaceDate DATE,
);


-- DimWeather
CREATE TABLE DimWeather (
    WeatherID INT PRIMARY KEY,
    TempMax FLOAT,           -- °C
    TempMin FLOAT,           -- °C
    TempAvg FLOAT,           -- °C
    FeelsLikeMax FLOAT,      -- °C
    FeelsLikeMin FLOAT,      -- °C
    FeelsLikeAvg FLOAT,      -- °C
    DewPoint FLOAT,          -- °C
    Humidity FLOAT,          -- %
    Precipitation FLOAT,     -- mm
    PrecipitationCover FLOAT,-- %
    SnowDepth FLOAT,         -- cm
    WindGust FLOAT,          -- km/h
    WindSpeed FLOAT,         -- km/h
    WindDirection INT,       -- °
    SeaLevelPressure FLOAT,  -- hPa
    Visibility FLOAT,        -- km
    Description VARCHAR(255) -- text
);


-- FactRacePerformance 
CREATE TABLE FactRacePerformance (
    racePerformanceId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    weatherId INT,
    circuitId INT,
    date DATE,
    laps INT,
    fastestLap INT,
    fastestLapRank INT,
    fastestLapSpeed FLOAT,
    raceTime INT,
    avgLapTime FLOAT,
    minLapTime INT,
    maxLapTime INT,
    pitStopCount INT,
    avgPitStopTime FLOAT,
    maxPitStopTime INT,
    minPitStopTime INT,
    constructorPosition INT,
    driverPosition INT,
    status VARCHAR(255),
    FOREIGN KEY (date) REFERENCES DimDate(Date),
    FOREIGN KEY (raceId) REFERENCES DimRace(RaceID),
    FOREIGN KEY (driverId) REFERENCES DimDriver(DriverID),
    FOREIGN KEY (constructorId) REFERENCES DimConstructor(ConstructorID),
    FOREIGN KEY (weatherId) REFERENCES DimWeather(WeatherID),
    FOREIGN KEY (circuitId) REFERENCES DimCircuit(CircuitID)
);

