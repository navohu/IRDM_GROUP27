# Structure of PostgreSQL DB on AWS RDS

BEGIN;
DROP TABLE IF EXISTS cs_sites;
DROP TABLE IF EXISTS cs_dictionary;
DROP TABLE IF EXISTS cs_dictionary_raw;

CREATE TABLE cs_sites (
	id INTEGER,
	title VARCHAR,
	link VARCHAR,
	stemmed_length BIGINT);
CREATE TABLE cs_dictionary (
	word TEXT,
	word_id BIGINT,
	freq BIGINT);
CREATE TABLE cs_dictionary_raw (
	word TEXT,
	word_id BIGINT,
	freq BIGINT);
CREATE TABLE cs_word_occurrences (
	word_id BIGINT,
	document_id BIGINT,
	occurrences INTEGER);

END;