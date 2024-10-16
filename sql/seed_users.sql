DELETE FROM employee_user;

INSERT INTO employee_user (username, pwd, employee_id)
VALUES (
    'GofmannIA',
    '$2a$12$WvZel3D09DwRFKf.nPTdhOGlo9u3kj/Oellf0sYiTfH0cX4OxBnKe',
    -- bcrypt yanederevo 12 rounds
    (SELECT id FROM employee WHERE fio = 'Gofmann Igor Avraalovich' LIMIT 1)
);