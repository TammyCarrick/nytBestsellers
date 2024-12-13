CREATE DATABASE IF NOT EXISTS nyt_best_sellers;

USE nyt_best_sellers;

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
 
CREATE USER 'root'@'%' IDENTIFIED BY 'RE3Dmysql';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';

ALTER TABLE lists_info
CHANGE oldest_published_draw_dataate oldest_published_date DATE;