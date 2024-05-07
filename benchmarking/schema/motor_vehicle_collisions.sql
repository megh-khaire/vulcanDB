-- Link - https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes
--Collisions Table
CREATE TABLE Collisions (
    collision_id INT PRIMARY KEY,
    crash_date TIMESTAMP NOT NULL,
    crash_time TIME NOT NULL,
    borough VARCHAR(255),
    zip_code CHAR(5),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    location POINT,
    number_of_persons_injured INT CHECK (number_of_persons_injured >= 0),
    number_of_persons_killed INT CHECK (number_of_persons_killed >= 0),
    number_of_pedestrians_injured INT CHECK (number_of_pedestrians_injured >= 0),
    number_of_pedestrians_killed INT CHECK (number_of_pedestrians_killed >= 0),
    number_of_cyclist_injured INT CHECK (number_of_cyclist_injured >= 0),
    number_of_cyclist_killed INT CHECK (number_of_cyclist_killed >= 0),
    number_of_motorist_injured INT CHECK (number_of_motorist_injured >= 0),
    number_of_motorist_killed INT CHECK (number_of_motorist_killed >= 0)
);

--Streets Table
CREATE TABLE Streets (
    collision_id INT,
    on_street_name VARCHAR(255),
    cross_street_name VARCHAR(255),
    off_street_name VARCHAR(255),
    FOREIGN KEY (collision_id) REFERENCES Collisions(collision_id)
);

--VehicleCollisions Table
CREATE TABLE VehicleCollisions (
    collision_id INT,
    vehicle_type_code VARCHAR(255),
    contributing_factor VARCHAR(255),
    FOREIGN KEY (collision_id) REFERENCES Collisions(collision_id)
);
