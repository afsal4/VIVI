CREATE TABLE company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    job_description TEXT,
    email_id TEXT
);

CREATE TABLE candidate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    email TEXT,
    company_id INTEGER, 
    FOREIGN KEY(company_id) REFERENCES company(id)
);

create table qna(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    question TEXT,
    answer TEXT, 
    company_id INTEGER,
    candidate_id INTEGER,
    score INTEGER,
    FOREIGN KEY(company_id) REFERENCES company(id)
    FOREIGN KEY(candidate_id) REFERENCES candidate(id)
)