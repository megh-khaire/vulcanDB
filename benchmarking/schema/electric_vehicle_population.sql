-- Link - https://catalog.data.gov/dataset/electric-vehicle-population-data

--Location Table
CREATE TABLE Location (
    location_id SERIAL PRIMARY KEY,
    county VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    zip_code CHAR(5) NOT NULL CHECK (zip_code ~ '^\d{5}$'),
    legislative_district VARCHAR(255) NOT NULL,
    _2020_census_tract VARCHAR(255) NOT NULL,
    UNIQUE (county, city, state, zip_code, legislative_district, _2020_census_tract)
);

--VehicleRegistry Table
CREATE TABLE VehicleRegistry (
    dol_vehicle_id VARCHAR(255) NOT NULL PRIMARY KEY,
    vin_1_10 VARCHAR(10) NOT NULL UNIQUE,
    model_year VARCHAR(255) NOT NULL CHECK (model_year ~ '^\d{4}$'),
    make VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    ev_type VARCHAR(255) NOT NULL,
    cafv_type VARCHAR(255) NOT NULL,
    electric_range INT CHECK (electric_range >= 0),
    base_msrp DECIMAL(10, 2) CHECK (base_msrp >= 0),
    geocoded_column POINT,
    electric_utility TEXT,
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
);
