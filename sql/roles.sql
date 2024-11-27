GRANT SELECT, UPDATE ON employee TO employee;
GRANT SELECT, INSERT ON fulfilled_order TO employee;
GRANT SELECT, INSERT ON vacation TO employee;

GRANT SELECT ON employee TO accounting;
GRANT SELECT, INSERT, UPDATE ON payrate TO accounting;
GRANT SELECT, INSERT, UPDATE ON receipt TO accounting;
GRANT SELECT, INSERT, UPDATE ON salary TO accounting;
GRANT SELECT ON vacation TO accounting;