CREATE ROLE root WITH LOGIN SUPERUSER PASSWORD 'superuserpassword';
CREATE USER admin WITH PASSWORD 'supersecretpwd';
CREATE DATABASE zarplata;
GRANT ALL ON DATABASE zarplata TO admin;
ALTER DATABASE zarplata OWNER TO admin;