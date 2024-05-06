-- Link - https://catalog.data.gov/dataset/crime-data-from-2020-to-present

-- Area Table
CREATE TABLE Area (
    area VARCHAR(2) NOT NULL PRIMARY KEY,
    area_name VARCHAR(255) NOT NULL
);

-- Crime Code Table
CREATE TABLE CrimeCode (
    crm_cd VARCHAR(255) NOT NULL PRIMARY KEY,
    crm_cd_desc VARCHAR(255) NOT NULL,
    crm_cd_1 VARCHAR(255),
    crm_cd_2 VARCHAR(255),
    crm_cd_3 VARCHAR(255),
    crm_cd_4 VARCHAR(255)
);

-- Crime Incident Table
CREATE TABLE CrimeIncident (
    dr_no VARCHAR(255) NOT NULL PRIMARY KEY,
    date_rptd TIMESTAMP NOT NULL,
    date_occ TIMESTAMP NOT NULL,
    time_occ TIME NOT NULL,
    area VARCHAR(2) NOT NULL,
    rpt_dist_no VARCHAR(4) NOT NULL,
    part_1_2 INT NOT NULL CHECK (part_1_2 IN (1, 2)),
    crm_cd VARCHAR(255) NOT NULL,
    mocodes TEXT,
    location VARCHAR(255),
    cross_street VARCHAR(255),
    lat DECIMAL(9,6),
    lon DECIMAL(9,6),
    status CHAR(2) DEFAULT 'IC',
    status_desc VARCHAR(255),
    FOREIGN KEY (area) REFERENCES Area(area),
    FOREIGN KEY (crm_cd) REFERENCES CrimeCode(crm_cd)
);



--Victim Table
CREATE TABLE Victim (
    victim_id SERIAL PRIMARY KEY,
    dr_no VARCHAR(255) NOT NULL,
    vict_age VARCHAR(2) CHECK (vict_age ~ '^\d{2}$'),
    vict_sex CHAR(1) CHECK (vict_sex IN ('F', 'M', 'X')),
    vict_descent CHAR(1) CHECK (vict_descent IN ('A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'O', 'P', 'S', 'U', 'V', 'W', 'X', 'Z')),
    FOREIGN KEY (dr_no) REFERENCES CrimeIncident(dr_no)
);

--Premise Table
CREATE TABLE Premises (
    premis_cd INT PRIMARY KEY,
    premis_desc VARCHAR(255)
);

--Weapon Table
CREATE TABLE Weapon (
    weapon_used_cd VARCHAR(255) PRIMARY KEY,
    weapon_desc VARCHAR(255)
);

