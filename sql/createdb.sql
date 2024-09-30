
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS workday;
DROP TABLE IF EXISTS vacation;
DROP TABLE IF EXISTS fulfilled_order;
DROP TABLE IF EXISTS payrate CASCADE;
DROP TABLE IF EXISTS salary CASCADE;
DROP TABLE IF EXISTS receipt;

CREATE TABLE employee (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fio VARCHAR(32) NOT NULL,
    payment_method text,
    receipt_address text
);

CREATE TABLE workday (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID references employee(id),
    workday_date DATE NOT NULL DEFAULT CURRENT_DATE,
    entry_time TIME WITH TIME ZONE NOT NULL,
    exit_time TIME WITH TIME ZONE,
    CONSTRAINT valid_period CHECK (
        (exit_time IS NULL)
        OR (exit_time > entry_time))
);

CREATE TABLE vacation (
    id SERIAL PRIMARY KEY,
    employee_id UUID references employee(id),
    begin_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT valid_period CHECK (end_date::date - begin_date::date > 0),
    CONSTRAINT not_exceeding_limit CHECK (end_date::date - begin_date::date < 28)
);

CREATE TABLE fulfilled_order (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID REFERENCES employee(id),
    amount NUMERIC(10,2) NOT NULL,
    fullfillment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT valid_amount CHECK (amount > 0),
    CONSTRAINT valid_date CHECK (abs(CURRENT_DATE::date - fullfillment_date::date) < 1)
);

CREATE TABLE payrate (
    id SERIAL PRIMARY KEY,
    base_rate NUMERIC(8, 2) NOT NULL,
    commission NUMERIC(3,2) NOT NULL DEFAULT (0.00),
    salaty_type VARCHAR(16) NOT NULL,
    payment_period VARCHAR(16) NOT NULL,
    CONSTRAINT allowed_base_rate CHECK (base_rate >= 0),
    CONSTRAINT allowed_comissions CHECK (commission = ANY(ARRAY[0.00, 0.01, 0.03, 0.05])),
    CONSTRAINT allowed_salary_types CHECK (salaty_type = ANY('{hourly, fixed}'::text[])),
    CONSTRAINT allowed_payment_periods CHECK (payment_period = ANY('{monthly, biweekly}'::text[]))
);

CREATE TABLE salary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID REFERENCES employee(id),
    payrate_id INTEGER REFERENCES payrate(id)
);

CREATE TABLE receipt (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salary_id UUID REFERENCES salary(id),
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    base_amount NUMERIC(8,2) NOT NULL,
    comission_amount NUMERIC(8,2) NOT NULL,
    receipt_text TEXT,
    CONSTRAINT valid_amount CHECK (base_amount >= 0)
);