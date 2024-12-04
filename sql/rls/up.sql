ALTER TABLE employee ENABLE ROW LEVEL SECURITY;
ALTER TABLE vacation ENABLE ROW LEVEL SECURITY;
ALTER TABLE fulfilled_order ENABLE ROW LEVEL SECURITY;
ALTER TABLE employee_user ENABLE ROW LEVEL SECURITY;

CREATE POLICY employee_select_own ON employee FOR SELECT TO employee
	USING (id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY employee_update_own ON employee FOR UPDATE TO employee
	USING (id = (SELECT employee_id FROM employee_user WHERE username = current_user))
	WITH CHECK (id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY vacation_select_own ON vacation FOR SELECT TO employee
	USING (employee_id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY vacation_insert_own ON vacation FOR INSERT TO employee
    WITH CHECK (employee_id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY fulfilled_select_own ON fulfilled_order FOR SELECT TO employee
	USING (employee_id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY fulfilled_insert_own ON fulfilled_order FOR INSERT TO employee
	WITH CHECK (employee_id = (SELECT employee_id FROM employee_user WHERE username = current_user));

CREATE POLICY employee_user_select_own ON employee_user FOR SELECT
	TO employee
	USING (username = current_user);


CREATE POLICY account_select_all ON employee FOR SELECT
TO accounting
	USING (true);

CREATE POLICY fulfilled_select_all ON fulfilled_order FOR SELECT
TO accounting
	USING (true);

CREATE POLICY vacation_select_future ON vacation FOR SELECT
TO accounting
	USING (end_date - CURRENT_DATE > 0);
