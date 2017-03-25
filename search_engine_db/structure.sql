# Structure of PostgreSQL DB on AWS RDS

BEGIN;
DROP TABLE IF EXISTS ucl_sites;

CREATE TABLE ucl_sites (
	url VARCHAR,
	title VARCHAR
);

END;