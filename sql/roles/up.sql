CREATE ROLE employee WITH NOLOGIN;
CREATE ROLE accounting WITH NOLOGIN;

CREATE USER employee_vasiliy WITH INHERIT LOGIN IN ROLE employee PASSWORD '1234';
CREATE USER accounting_anna WITH INHERIT LOGIN IN ROLE accounting PASSWORD '1234';

CREATE USER gofmannia WITH INHERIT LOGIN IN ROLE employee PASSWORD '1234';
CREATE USER ravellenpm WITH INHERIT LOGIN IN ROLE accounting PASSWORD '1234';

GRANT SELECT ON employee_user TO employee;
GRANT SELECT, UPDATE ON employee TO employee;
GRANT SELECT, INSERT ON fulfilled_order TO employee;
GRANT SELECT, INSERT ON vacation TO employee;
GRANT USAGE, SELECT ON SEQUENCE vacation_id_seq TO employee;

GRANT SELECT ON employee TO accounting;
GRANT SELECT, INSERT, UPDATE ON payrate TO accounting;
GRANT SELECT, INSERT, UPDATE ON receipt TO accounting;
GRANT SELECT, INSERT, UPDATE ON salary TO accounting;
GRANT SELECT ON vacation TO accounting;
GRANT SELECT ON fulfilled_order TO accounting;