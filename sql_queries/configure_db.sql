CREATE DATABASE IF NOT EXISTS nyt_best_sellers;

USE nyt_best_sellers;

CREATE USER 'root'@'%' IDENTIFIED BY 'RE3Dmysql';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';

-- creating a user that can only select and insert, no deleting
CREATE USER 'connect'@'localhost' IDENTIFIED BY 'nytconnect';
GRANT SELECT, INSERT ON nyt_best_sellers.* TO 'connect'@'localhost';

CREATE TABLE IF NOT EXISTS raw_data (
	title VARCHAR(150) NOT NULL,
    rank_ INT NOT NULL,
    prev_rank INT,
    num_weeks INT,
    author VARCHAR(150),
    publisher VARCHAR(150),
    description_ VARCHAR(250),
    -- prob convert to boolean during cleaning
    dagger INT,
    amazon_url VARCHAR(100)
);

 CREATE TABLE IF NOT EXISTS lists_info (
	type_ VARCHAR(100) PRIMARY KEY,
    oldest_published_draw_date DATE,
    newest_published_date DATE,
    updated VARCHAR(50)
 );
 

-- rename column
ALTER TABLE lists_info
CHANGE oldest_published_draw_dataate oldest_published_date DATE;

-- add priority column to determine order of which data is pulled
ALTER TABLE lists_info
ADD COLUMN priority INT;

-- add date column to raw data table (so we know when the book was on the list and at what rank)
ALTER TABLE nyt_best_sellers.raw_data
-- ADD COLUMN date_on_list DATE,
ADD COLUMN type_ VARCHAR(100);

ALTER TABLE nyt_best_sellers.raw_data
MODIFY amazon_url VARCHAR(300);

ALTER TABLE nyt_best_sellers.raw_data
MODIFY description_ VARCHAR(500);

USE nyt_best_sellers;

CREATE TABLE IF NOT EXISTS volumeID (
	volumeid VARCHAR(70),
    author VARCHAR(200),
    title VARCHAR (200),
	title_rslt VARCHAR(250),
	first_name VARCHAR(150),
	middle_name VARCHAR(150),
	last_name VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS troubleshoot_id(
	volumeID VARCHAR(50),
    author VARCHAR(100),
    title VARCHAR (200),
    first_name VARCHAR(150),
	middle_name VARCHAR(150),
	last_name VARCHAR(150)
);

ALTER TABLE troubleshoot_id
ADD COLUMN date_on_list DATE;

-- adding primary keys to the tables
ALTER TABLE volumeid 
ADD PRIMARY KEY (volumeid);

ALTER TABLE verified_ids 
ADD PRIMARY KEY (volumeID);

CREATE TABLE IF NOT EXISTS verified_ids(
	volumeID VARCHAR(50),
    verified TINYINT
);

ALTER TABLE raw_data_searchable
RENAME COLUMN date_on_list TO first_date_on_list;

CREATE TABLE IF NOT EXISTS metadata (
	volumeid VARCHAR(70),
    author VARCHAR(300),
    description_ VARCHAR(3000),
    pg_count INT,
    printed_pg_count INT,
    genre1 VARCHAR(100),
    genre2 VARCHAR(100),
    genre3 VARCHAR(100),
    genre4 VARCHAR(100),
    genre5 VARCHAR(100),
    img_url VARCHAR(600),
    maturity_rating  TINYINT
); 

ALTER TABLE metadata 
ADD COLUMN all_genres VARCHAR(140);
-- MODIFY COLUMN ISBN10 VARCHAR(30),
-- MODIFY COLUMN ISBN13 VARCHAR(45);
-- MODIFY COLUMN published_date VARCHAR(100);
-- MODIFY COLUMN published_date VARCHAR(20); -- changed date because some of the published dates returned from the goolge api not in the right format (were throwing errors)
-- MODIFY COLUMN ISBN10 VARCHAR(10),
-- MODIFY COLUMN ISBN13 VARCHAR(13);
-- ADD COLUMN title VARCHAR(200);
-- ADD COLUMN ISBN10 INT,
-- ADD COLUMN ISBN13 INT;
-- ADD COLUMN published_date DATE; 
-- ADD COLUMN publisher VARCHAR(200);
-- ADD COLUMN genre6 VARCHAR(100),
-- ADD COLUMN genre7 VARCHAR(100);


