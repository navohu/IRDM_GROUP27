# Structure of PostgreSQL DB on AWS RDS

BEGIN;
DROP TABLE IF EXISTS cs_sites;
DROP TABLE IF EXISTS cs_dictionary;
DROP TABLE IF EXISTS cs_dictionary_raw;

CREATE TABLE cs_sites (
	id INTEGER NOT NULL,
	title VARCHAR,
	link VARCHAR,
	stemmed_length BIGINT);
CREATE TABLE cs_dictionary (
	word TEXT NOT NULL,
	word_id BIGINT NOT NULL,
	freq BIGINT);
CREATE TABLE cs_dictionary_raw (
	word TEXT NOT NULL,
	word_id BIGINT NOT NULL,
	freq BIGINT);
CREATE TABLE cs_word_occurrences (
	word_id BIGINT NOT NULL,
	document_id BIGINT NOT NULL,
	occurrences INTEGER);
CREATE TABLE cs_word_occurrences_raw (
	word_id BIGINT NOT NULL,
	document_id BIGINT NOT NULL,
	occurrences INTEGER);

END;