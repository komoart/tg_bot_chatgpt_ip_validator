-- Создание таблиц
CREATE TABLE Department
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
);

CREATE TABLE Employee
(
    id SERIAL PRIMARY KEY,
    department_id INTEGER,
    chief_id INTEGER,
    name VARCHAR(200),
    salary INTEGER,
    FOREIGN KEY (department_id) REFERENCES Department (id),
    FOREIGN KEY (chief_id) REFERENCES (id),
)

-- Запрос
SELECT emp.name, dep.name
FROM Employee AS emp
INNER JOIN Department as dep ON emp.department_id = dep.id
INNER JOIN Employee as boss ON emp.chief_id = boss.id
WHERE boss.salary BETWEEN 1.5*(emp.salary) AND 2*(emp.salary)