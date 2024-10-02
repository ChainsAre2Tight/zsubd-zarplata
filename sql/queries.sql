SELECT employee.id, employee.fio
FROM employee
    JOIN salary on employee.id = salary.employee_id
    JOIN payrate on salary.payrate_id = payrate.id
WHERE payrate.job_title = 'Worker'
ORDER BY 2;



SELECT
    employee.fio,
    (extract(
        hour FROM sum(workday.exit_time::time
        - workday.entry_time::time)::interval)*60
    + extract(
        minutes FROM sum(workday.exit_time::time
        - workday.entry_time::time)::interval)) / 60
    as total_hours
FROM workday
    JOIN employee ON employee.id = workday.employee_id
    JOIN salary ON employee.id = salary.employee_id
    JOIN payrate ON salary.payrate_id = payrate.id
WHERE
    employee.fio = 'Gofmann Igor Avraalovich'
    AND payrate.job_title = 'Worker'
    AND (DATE_PART('year', CURRENT_DATE::date)
    -DATE_PART('year', workday.workday_date::date))*12
    -(DATE_PART('month', CURRENT_DATE::date)
    -DATE_PART('month', workday.workday_date::date)) < 1
GROUP BY employee.fio;



SELECt * FROM fulfilled_order
WHERE fulfilled_order.employee_id = (
    SELECT employee.id FROM employee
    WHERE employee.fio = 'Gofmann Igor Avraalovich'
    LIMIT 1
);