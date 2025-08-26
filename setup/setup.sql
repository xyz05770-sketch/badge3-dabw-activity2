-- Create the employee_crud database in snowflake
create database employee_crud;


-- Load data into table employee_crud.public.employee

CREATE TABLE "EMPLOYEE_CRUD"."PUBLIC"."employee" ( ID NUMBER(38, 0) , FirstName VARCHAR , LastName VARCHAR , DOB DATE , Gender VARCHAR , Department VARCHAR , Salary NUMBER(38, 0) ); 

CREATE TEMP FILE FORMAT "EMPLOYEE_CRUD"."PUBLIC"."temp_file_format_2025-08-26T16:26:54.339Z"
	TYPE=CSV
    SKIP_HEADER=1
    FIELD_DELIMITER=','
    TRIM_SPACE=TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY='"'
    REPLACE_INVALID_CHARACTERS=TRUE
    DATE_FORMAT=AUTO
    TIME_FORMAT=AUTO
    TIMESTAMP_FORMAT=AUTO; 

COPY INTO "EMPLOYEE_CRUD"."PUBLIC"."employee" 
FROM (SELECT $1, $2, $3, $4, $5, $6, $7
	FROM '@"EMPLOYEE_CRUD"."PUBLIC"."__snowflake_temp_import_files__"') 
FILES = ('2025-08-26T16:26:28.864Z/employees.csv') 
FILE_FORMAT = '"EMPLOYEE_CRUD"."PUBLIC"."temp_file_format_2025-08-26T16:26:54.339Z"' 
ON_ERROR=ABORT_STATEMENT
