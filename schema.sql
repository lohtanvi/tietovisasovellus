CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    visible INTEGER
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes,
    question TEXT,
    qvisible INTEGER
);

CREATE TABLE qanswers (
    id SERIAL PRIMARY KEY,
    quest_id INTEGER REFERENCES questions,
    answer TEXT,
    correct INTEGER
);