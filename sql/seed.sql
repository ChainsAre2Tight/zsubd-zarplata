TRUNCATE employee, workday, vacation, fulfilled_order, payrate, salary, receipt;

INSERT INTO employee (fio, payment_method, receipt_address)
    VALUES ('Gofmann Igor Avraalovich', 'card 1234 5678 9012 3456', 'kvartira na peisah');

INSERT INTO vacation (employee_id, begin_date, end_date)
    VALUES (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        CURRENT_DATE + INTERVAL '61 days',
        CURRENT_DATE + INTERVAL '68 days'
    );

INSERT INTO fulfilled_order (employee_id, amount, fullfillment_date)
    VALUES (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        123456.78,
        CURRENT_DATE
    ), (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        19876.32,
        CURRENT_DATE + INTERVAL '19 hours'
    );

INSERT INTO workday (employee_id, workday_date, entry_time, exit_time)
    VALUES (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        CURRENT_DATE,
        '09:32:06 MSK',
        '13:29:54 MSK'
    ), (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        CURRENT_DATE,
        '15:02:07 MSK',
        '18:05:46 MSK'
    ), (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        CURRENT_DATE + INTERVAL '1 day',
        '10:11:19 MSK',
        '17:08:23 MSK'
    );

INSERT INTO payrate (base_rate, commission, salaty_type, payment_period)
    VALUES (
        500.00,
        0.05,
        'hourly',
        'monthly'
    );

INSERT INTO salary (employee_id, payrate_id)
    VALUES (
        (SELECT id
            FROM employee
            WHERE fio = 'Gofmann Igor Avraalovich'
            LIMIT 1),
        (SELECT id
            FROM payrate
            WHERE commission = 0.05 AND salaty_type = 'hourly'
            LIMIT 1)
    );

INSERT INTO receipt (salary_id, payment_date, base_amount, comission_amount)
    VALUES (
        (
            SELECT salary.id FROM salary JOIN employee
            ON salary.employee_id = employee.id
            WHERE employee.fio = 'Gofmann Igor Avraalovich'
        ),
        CURRENT_DATE,
        (
            SELECT (
                extract(
                    hour FROM sum(workday.exit_time::time
                    - workday.entry_time::time)::interval)*60
                + extract(
                    minutes FROM sum(workday.exit_time::time
                    - workday.entry_time::time)::interval)) / 60
                as total_hours
            FROM workday
            JOIN employee ON workday.employee_id = employee.id
            WHERE
                employee.fio = 'Gofmann Igor Avraalovich'
                AND (DATE_PART('year', CURRENT_DATE::date)-DATE_PART('year', workday.workday_date::date))*12-(DATE_PART('month', CURRENT_DATE::date)-DATE_PART('month', workday.workday_date::date)) < 1
            GROUP BY employee.id
            LIMIT 1
        ) * (
            SELECT payrate.base_rate
            FROM salary
                JOIN employee ON salary.employee_id = employee.id
                JOIN payrate ON salary.payrate_id = payrate.id
            WHERE employee.fio = 'Gofmann Igor Avraalovich'
            LIMIT 1
        ), (
            SELECT sum(fulfilled_order.amount)
            FROM fulfilled_order
            JOIN employee ON fulfilled_order.employee_id = employee.id
            WHERE
                employee.fio = 'Gofmann Igor Avraalovich'
                AND (DATE_PART('year', CURRENT_DATE::date)-DATE_PART('year', fulfilled_order.fullfillment_date::date))*12-(DATE_PART('month', CURRENT_DATE::date)-DATE_PART('month', fulfilled_order.fullfillment_date::date)) < 1
            GROUP BY employee.id
            LIMIT 1
        ) * (
            SELECT payrate.commission
            FROM salary
                JOIN employee ON salary.employee_id = employee.id
                JOIN payrate ON salary.payrate_id = payrate.id
            WHERE employee.fio = 'Gofmann Igor Avraalovich'
            LIMIT 1
        )
    );

-- SELECT * FROM employee;
-- SELECT * FROM vacation;
-- SELECT * FROM fulfilled_order;
-- SELECT * FROM workday;
-- SELECT * FROM payrate;
-- SELECT * FROM salary;
SELECT * FROM receipt;