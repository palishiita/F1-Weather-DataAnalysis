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
