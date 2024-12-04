ALTER TABLE employee DISABLE ROW LEVEL SECURITY;
ALTER TABLE vacation DISABLE ROW LEVEL SECURITY;
ALTER TABLE fulfilled_order DISABLE ROW LEVEL SECURITY;

DROP POLICY employee_select_own ON employee;
DROP POLICY employee_update_own ON employee;
DROP POLICY vacation_select_own ON vacation;
DROP POLICY vacation_insert_own ON vacation;
DROP POLICY fulfilled_select_own ON fulfilled_order;
DROP POLICY fulfilled_insert_own ON fulfilled_order;
DROP POLICY employee_user_select_own ON employee_user;
DROP POLICY account_select_all on employee;
DROP POLICY fulfilled_select_all on fulfilled_order;
DROP POLICY vacation_select_future on vacation;