/*
Script Name: db_schema.sql
Author: Surekha Gaikwad
Date: Aug 01, 2024
Description:
This SQL script creates visa_db schema and assosciated table.
Usage:
- Run this script in a SQL environment with appropriate privileges to create and ingest data.
*/


DO $$
DECLARE
    schema VARCHAR(50) := 'visa_db';
BEGIN
    EXECUTE 'DROP SCHEMA IF EXISTS ' || schema || ' CASCADE';
    EXECUTE 'CREATE SCHEMA ' || schema || ' AUTHORIZATION postgres';
    EXECUTE 'COMMENT ON SCHEMA ' || schema || ' IS ''standard public postgres''';
    EXECUTE 'GRANT ALL ON SCHEMA ' || schema || ' TO PUBLIC';
    EXECUTE 'GRANT ALL ON SCHEMA ' || schema || ' TO postgres';

    EXECUTE 'DROP TABLE IF EXISTS ' || schema || '.visadata';
    EXECUTE 'CREATE UNLOGGED TABLE ' || schema || '.visadata(
                        case_id                 VARCHAR(30) PRIMARY KEY,
                        continent               VARCHAR(50),
                        education_of_employee   VARCHAR(50),
                        has_job_experience      VARCHAR(10),
                        requires_job_training   VARCHAR(10),
                        no_of_employees         INTEGER,
                        yr_of_estab             INTEGER,
                        region_of_employment    VARCHAR(50),
                        prevailing_wage         NUMERIC,
                        unit_of_wage            VARCHAR(30),
                        full_time_position      VARCHAR(10),
                        case_status             VARCHAR(30)
                    )';

END $$;
