CREATE USER kisadmin WITH PASSWORD 'kadmin';
CREATE USER dmkadmin WITH PASSWORD 'dadmin';
CREATE DATABASE kis;
CREATE DATABASE dmk;
GRANT ALL ON DATABASE kis TO kisadmin;
GRANT ALL ON DATABASE dmk TO dmkadmin;

\c dmk

ALTER SCHEMA public OWNER TO dmkadmin;
GRANT ALL PRIVILEGES ON SCHEMA public TO dmkadmin;

\c kis

CREATE SCHEMA mm;
ALTER SCHEMA mm OWNER TO kisadmin;
GRANT ALL PRIVILEGES ON SCHEMA mm TO kisadmin;


\c kis kisadmin

-- KIS DB Profiles
CREATE TABLE mm.profile_med
(
id SERIAL PRIMARY KEY,
name VARCHAR (255) NOT NULL
);


INSERT INTO mm.profile_med (name)
VALUES
('хирургии'),
('терапии'),
('неврологии'),
('урологии'),
('кардиологии'),
('скорой помощи');


-- KIS DB hospitalized by depts
CREATE TABLE mm.dept_hosp
(
    id SERIAL PRIMARY KEY,
    profile_id SMALLINT REFERENCES mm.profile_med(id),
    amount SMALLINT NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.dept_hosp (profile_id, amount, dates)
VALUES

(1, 13, LOCALTIMESTAMP - INTERVAL '6 DAY'),
(2, 24, LOCALTIMESTAMP - INTERVAL '6 DAY'),
(3, 16, LOCALTIMESTAMP - INTERVAL '6 DAY'),
(4, 11, LOCALTIMESTAMP - INTERVAL '6 DAY'),
(5, 8, LOCALTIMESTAMP - INTERVAL '6 DAY'),
(6, 27, LOCALTIMESTAMP - INTERVAL '6 DAY'),

(1, 14, LOCALTIMESTAMP - INTERVAL '5 DAY'),
(2, 26, LOCALTIMESTAMP - INTERVAL '5 DAY'),
(3, 16, LOCALTIMESTAMP - INTERVAL '5 DAY'),
(4, 13, LOCALTIMESTAMP - INTERVAL '5 DAY'),
(5, 12, LOCALTIMESTAMP - INTERVAL '5 DAY'),
(6, 9, LOCALTIMESTAMP - INTERVAL '5 DAY'),

(1, 16, LOCALTIMESTAMP - INTERVAL '4 DAY'),
(2, 23, LOCALTIMESTAMP - INTERVAL '4 DAY'),
(3, 17, LOCALTIMESTAMP - INTERVAL '4 DAY'),
(4, 19, LOCALTIMESTAMP - INTERVAL '4 DAY'),
(5, 23, LOCALTIMESTAMP - INTERVAL '4 DAY'),
(6, 13, LOCALTIMESTAMP - INTERVAL '4 DAY'),

(1, 22, LOCALTIMESTAMP - INTERVAL '3 DAY'),
(2, 16, LOCALTIMESTAMP - INTERVAL '3 DAY'),
(3, 18, LOCALTIMESTAMP - INTERVAL '3 DAY'),
(4, 3, LOCALTIMESTAMP - INTERVAL '3 DAY'),
(5, 28, LOCALTIMESTAMP - INTERVAL '3 DAY'),
(6, 17, LOCALTIMESTAMP - INTERVAL '3 DAY'),


(1, 18, LOCALTIMESTAMP - INTERVAL '2 DAY'),
(2, 14, LOCALTIMESTAMP - INTERVAL '2 DAY'),
(3, 11, LOCALTIMESTAMP - INTERVAL '2 DAY'),
(4, 6, LOCALTIMESTAMP - INTERVAL '2 DAY'),
(5, 14, LOCALTIMESTAMP - INTERVAL '2 DAY'),
(6, 25, LOCALTIMESTAMP - INTERVAL '2 DAY'),

(1, 9, LOCALTIMESTAMP - INTERVAL '1 DAY'),
(2, 13, LOCALTIMESTAMP - INTERVAL '1 DAY'),
(3, 11, LOCALTIMESTAMP - INTERVAL '1 DAY'),
(4, 14, LOCALTIMESTAMP - INTERVAL '1 DAY'),
(5, 21, LOCALTIMESTAMP - INTERVAL '1 DAY'),
(6, 16, LOCALTIMESTAMP - INTERVAL '1 DAY'),

(1, 15, LOCALTIMESTAMP),
(2, 23, LOCALTIMESTAMP),
(3, 12, LOCALTIMESTAMP),
(4, 19, LOCALTIMESTAMP),
(5, 17, LOCALTIMESTAMP),
(6, 21, LOCALTIMESTAMP);



-- KIS DB all arrived patients
CREATE TABLE mm.arrived (
    id SERIAL PRIMARY KEY,
    status SMALLINT NOT NULL,
    dept VARCHAR (255) NOT NULL,
    channel VARCHAR (50) NOT NULL,
    patient_type VARCHAR (30) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.arrived (status, dept, channel, patient_type, dates)
VALUES

(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),
(0, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),
(0, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),
(1, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),
(1, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),
(1, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '6 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),
(1, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),
(1, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),
(1, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),
(0, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),
(0, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '5 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),
(1, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),
(1, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),
(1, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),
(1, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),
(1, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '4 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),
(0, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),
(0, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),
(0, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),
(0, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),
(1, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '3 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),
(0, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),
(1, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),
(0, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),
(1, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),
(0, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '2 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),
(1, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),
(1, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),
(1, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),
(1, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),
(1, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP - INTERVAL '1 DAY'),


(1, 'ОРИТ №1', '103', 'ЗЛ', LOCALTIMESTAMP),
(1, 'ОРИТ №2', '103', 'ЗЛ', LOCALTIMESTAMP),
(1, 'ОРИТ №3', '103', 'ЗЛ', LOCALTIMESTAMP),
(1, 'Хирургическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP),
(1, 'Терапевтическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP),
(1, 'Кардиологическое отделение', '103', 'ЗЛ', LOCALTIMESTAMP);



-- KIS DB all signot patients
CREATE TABLE mm.signout
(
    id SERIAL PRIMARY KEY,
    dept VARCHAR (255) NOT NULL,
    status VARCHAR (40) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.signout (dept, status, dates)
VALUES
('Хирургическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Хирургическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '6 DAY'),
('ОРИТ №3', 'Умер', LOCALTIMESTAMP - INTERVAL '6 DAY'),

('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Терапевтическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '5 DAY'),
('Хирургическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '5 DAY'),

('Хирургическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '4 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '4 DAY'),

('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),
('Хирургическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '3 DAY'),

('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Терапевтическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №2', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №2', 'Умер', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ОРИТ №3', 'Умер', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '2 DAY'),

('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Терапевтическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №2', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №3', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №1', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Терапевтическое отделение', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №2', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ОРИТ №3', 'Умер', LOCALTIMESTAMP - INTERVAL '1 DAY'),

('Хирургическое отделение', 'Выписан', LOCALTIMESTAMP),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP),
('Кардиологическое отделение', 'Выписан', LOCALTIMESTAMP),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP),
('ОРИТ №2', 'Умер', LOCALTIMESTAMP),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP),
('Хирургическое отделение', 'Умер', LOCALTIMESTAMP),
('Терапевтическое отделение', 'Выписан', LOCALTIMESTAMP),
('Кардиологическое отделение', 'Умер', LOCALTIMESTAMP),
('ОРИТ №1', 'Выписан', LOCALTIMESTAMP),
('ОРИТ №2', 'Умер', LOCALTIMESTAMP),
('ОРИТ №3', 'Выписан', LOCALTIMESTAMP);


-- KIS DB deads patients
CREATE TABLE mm.deads
(
    id SERIAL PRIMARY KEY,
    pat_fio VARCHAR (255) NOT NULL,
    ib_num VARCHAR (20) NOT NULL,
    sex VARCHAR (5) NOT NULL,
    agee SMALLINT NOT NULL,
    arriving_dt TIMESTAMP,
    state VARCHAR (25) NOT NULL,
    dept VARCHAR (255) NOT NULL,
    days SMALLINT NOT NULL,
    diag_arr VARCHAR (15) NOT NULL,
    diag_dead VARCHAR (15) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.deads (pat_fio, ib_num, sex, agee, arriving_dt, state, dept, days, diag_arr, diag_dead, dates)
VALUES
('ТЛЯЧЕВ А.С.', '25649-2024', 'муж', 38, '2024-03-16', 'средней тяжести', 'Терапевтическое отделение', 18, 'U07.1', 'K52.8', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('КАШИН П.В.', '26748-2024', 'муж', 42, '2024-03-19', 'тяжелое', 'Хирургическое отделение', 8, 'U07.2', 'K52.8', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('КОЛОВ К.Т.', '26114-2024', 'муж', 37, '2024-03-22', 'крайне тяжелое', 'Кардиологическое отделение', 3, 'J06.1', 'E73.2', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ПАВЛОВ Р.Н.', '25497-2024', 'муж', 29, '2024-03-17', 'средней тяжести', 'Терапевтическое отделение', 12, 'U07.1', 'I46', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('СЕРГЕЕВ В.Б.', '25864-2024', 'муж', 62, '2024-03-25', 'тяжелое', 'Хирургическое отделение', 9, 'I56.4', 'K70.2', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ТУРТ Д.Ф.', '26108-2024', 'муж', 74, '2024-03-28', 'тяжелое', 'Кардиологическое отделение', 4, 'K18.1', 'E82', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('РОК Т.У.', '26041-2024', 'муж', 43, '2024-03-21', 'средней тяжести', 'Хирургическое отделение', 6, 'J06.1', 'U07.2', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('ФАЙЗИЛОВ К.П.', '25997-2024', 'муж', 54, '2024-03-18', 'крайне тяжелое', 'Кардиологическое отделение', 11, 'J06.1', 'U07.2', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('МАНИЛОВА Т.У.', '26041-2024', 'жен', 71, '2024-03-21', 'средней тяжести', 'Хирургическое отделение', 6, 'J18.1', 'I96', LOCALTIMESTAMP - INTERVAL '2 DAY'),
('КУРСКАЯ К.П.', '25997-2024', 'жен', 58, '2024-03-18', 'крайне тяжелое', 'Кардиологическое отделение', 11, 'O.18', 'K17.2', LOCALTIMESTAMP - INTERVAL '2 DAY'),

('МОНИН А.С.', '26348-2024', 'муж', 38, '2024-03-16', 'средней тяжести', 'Терапевтическое отделение', 18, 'U07.1', 'K52.8', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ТЕРПОВ П.В.', '26378-2024', 'муж', 42, '2024-03-19', 'тяжелое', 'Хирургическое отделение', 8, 'U07.2', 'K52.8', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('БАГРАК К.Т.', '26319-2024', 'муж', 37, '2024-03-22', 'крайне тяжелое', 'Кардиологическое отделение', 3, 'J06.1', 'E73.2', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('КИТАЕВА Р.Н.', '26354-2024', 'жен', 29, '2024-03-17', 'средней тяжести', 'Терапевтическое отделение', 12, 'U07.1', 'I46', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('СЕРГЕЕВ В.Б.', '26778-2024', 'муж', 62, '2024-03-25', 'тяжелое', 'Хирургическое отделение', 9, 'I56.4', 'K70.2', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('КЕРН Д.Ф.', '26412-2024', 'муж', 74, '2024-03-28', 'тяжелое', 'Кардиологическое отделение', 4, 'K18.1', 'E82', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('ФАЛА Т.У.', '26406-2024', 'муж', 43, '2024-03-21', 'средней тяжести', 'Хирургическое отделение', 6, 'J06.1', 'U07.2', LOCALTIMESTAMP - INTERVAL '1 DAY'),
('СМУТОВ К.П.', '25908-2024', 'муж', 54, '2024-03-18', 'крайне тяжелое', 'Кардиологическое отделение', 11, 'J06.1', 'U07.2', LOCALTIMESTAMP - INTERVAL '1 DAY'),

('КИДОЕВ А.С.', '27089-2024', 'муж', 38, '2024-03-16', 'средней тяжести', 'Терапевтическое отделение', 18, 'U07.1', 'K52.8', LOCALTIMESTAMP),
('ТРЕХОВА П.В.', '27112-2024', 'жен', 42, '2024-03-19', 'тяжелое', 'Хирургическое отделение', 8, 'U07.2', 'K52.8', LOCALTIMESTAMP),
('КОПАЛЬ К.Т.', '27264-2024', 'жен', 37, '2024-03-22', 'крайне тяжелое', 'Кардиологическое отделение', 3, 'J06.1', 'E73.2', LOCALTIMESTAMP),
('ПАВЛОВА Т.У.', '27322-2024', 'жен', 71, '2024-03-21', 'средней тяжести', 'Хирургическое отделение', 6, 'J18.1', 'I96', LOCALTIMESTAMP),
('ТАМАНСКАЯ К.П.', '26942-2024', 'жен', 58, '2024-03-18', 'крайне тяжелое', 'Кардиологическое отделение', 11, 'O.18', 'K17.2', LOCALTIMESTAMP);



-- KIS DB all reanimations arrived patients
CREATE TABLE mm.oar_arrived (
    id SERIAL PRIMARY KEY,
    pat_fio VARCHAR (255) NOT NULL,
    ib_num VARCHAR (20) NOT NULL,
    ages SMALLINT NOT NULL,
    dept VARCHAR (255) NOT NULL,
    doc_fio VARCHAR (50) NOT NULL,
    diag_start VARCHAR (15) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.oar_arrived (pat_fio, ib_num, ages, dept, doc_fio, diag_start, dates)
VALUES
('ТЛЯЧЕВ А.С.', '25649-2024', 38, 'ОРИТ №1', 'Рак В.А.', 'U07.1', LOCALTIMESTAMP),
('КАШИН П.В.', '26748-2024', 42, 'ОРИТ №1', 'Плюмов С.Е.', 'U07.2', LOCALTIMESTAMP),
('КОЛОВ К.Т.', '26114-2024', 37, 'ОРИТ №1', 'Каширин В.В.', 'J06.1', LOCALTIMESTAMP),
('РАЗУМОВА Р.Н.', '25469-2024', 29, 'ОРИТ №2', 'Бунин А.С.', 'U07.1', LOCALTIMESTAMP),
('КОЗЛОВА А.С.', '25647-2024', 38, 'ОРИТ №2', 'Рак В.А.', 'U07.1', LOCALTIMESTAMP),
('ПЕРОВ П.В.', '26775-2024', 42, 'ОРИТ №2', 'Плюмов С.Е.', 'U07.2', LOCALTIMESTAMP),
('АТАЛА К.Т.', '26173-2024', 37, 'ОРИТ №2', 'Каширин В.В.', 'J06.1', LOCALTIMESTAMP),
('КИРУНОВА Р.Н.', '25452-2024', 29, 'ОРИТ №2', 'Бунин А.С.', 'U07.1', LOCALTIMESTAMP),
('СЕРЫЙ А.С.', '25614-2024', 38, 'ОРИТ №2', 'Рак В.А.', 'U07.1', LOCALTIMESTAMP),
('ВОЛКОВ П.В.', '26776-2024', 42, 'ОРИТ №3', 'Плюмов С.Е.', 'U07.2', LOCALTIMESTAMP),
('АВДЕЕВ К.Т.', '26257-2024', 37, 'ОРИТ №3', 'Каширин В.В.', 'J06.1', LOCALTIMESTAMP),
('ФРОЛОВА Р.Н.', '25447-2024', 29, 'ОРИТ №3', 'Бунин А.С.', 'U07.1', LOCALTIMESTAMP),
('АТАЛА К.Т.', '26173-2024', 37, 'ОРИТ №3', 'Каширин В.В.', 'J06.1', LOCALTIMESTAMP),
('КИРУНОВА Р.Н.', '25452-2024', 29, 'ОРИТ №3', 'Бунин А.С.', 'U07.1', LOCALTIMESTAMP),
('СЕРЫЙ А.С.', '25614-2024', 38, 'ОРИТ №3', 'Рак В.А.', 'U07.1', LOCALTIMESTAMP),
('ВОЛКОВ П.В.', '26776-2024', 42, 'ОРИТ №3', 'Плюмов С.Е.', 'U07.2', LOCALTIMESTAMP),
('АВДЕЕВ К.Т.', '26257-2024', 37, 'ОРИТ №3', 'Каширин В.В.', 'J06.1', LOCALTIMESTAMP),
('ФРОЛОВА Р.Н.', '25447-2024', 29, 'ОРИТ №1', 'Бунин А.С.', 'U07.1', LOCALTIMESTAMP);



-- KIS DB all reanimations moved out patients
CREATE TABLE mm.oar_moved (
    id SERIAL PRIMARY KEY,
    pat_fio VARCHAR (255) NOT NULL,
    ib_num VARCHAR (20) NOT NULL,
    ages SMALLINT NOT NULL,
    dept VARCHAR (255) NOT NULL,
    doc_fio VARCHAR (50) NOT NULL,
    move_date TIMESTAMP NOT NULL,
    diag_start VARCHAR (15) NOT NULL,
    from_dept VARCHAR (255) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.oar_moved (pat_fio, ib_num, ages, dept, doc_fio, move_date, from_dept, diag_start, dates)
VALUES
('ТЛЯЧЕВ А.С.', '25649-2024', 38, 'ОРИТ №1', 'Рак В.А.', '2024-04-01', 'Кардиологическое отделение', 'U07.1', LOCALTIMESTAMP),
('ФРОЛОВА Р.Н.', '25447-2024', 29, 'ОРИТ №2', 'Бунин А.С.', '2024-04-05', 'Хирургическое отделение', 'U07.1', LOCALTIMESTAMP),
('ВОЛКОВ П.В.', '26776-2024', 42, 'ОРИТ №1', 'Плюмов С.Е.', '2024-03-21', 'Терапевтическое отделение', 'U07.1', LOCALTIMESTAMP),
('КОЛОВ К.Т.', '26114-2024', 37, 'ОРИТ №1', 'Каширин В.В.', '2024-03-15', 'Хирургическое отделение', 'U07.1', LOCALTIMESTAMP),
('СЕРЫЙ А.С.', '25614-2024', 38, 'ОРИТ №1', 'Рак В.А.', '2024-03-19', 'Хирургическое отделение', 'U07.1', LOCALTIMESTAMP),
('АВДЕЕВ К.Т.', '26257-2024', 37, 'ОРИТ №3', 'Каширин В.В.', '2024-03-29', 'Терапевтическое отделение', 'U07.1', LOCALTIMESTAMP),
('РАЗУМОВА Р.Н.', '25469-2024', 29, 'ОРИТ №3', 'Бунин А.С.', '2024-04-02', 'Кардиологическое отделение', 'U07.1', LOCALTIMESTAMP);


-- KIS DB all reanimations current patients
CREATE TABLE mm.oar_current (
    id SERIAL PRIMARY KEY,
    pat_fio VARCHAR (255) NOT NULL,
    ib_num VARCHAR (20) NOT NULL,
    ages SMALLINT NOT NULL,
    dept VARCHAR (255) NOT NULL,
    doc_fio VARCHAR (50) NOT NULL,
    days SMALLINT NOT NULL,
    diag_start VARCHAR (15) NOT NULL,
    dates TIMESTAMP NOT NULL
);


INSERT INTO mm.oar_current (pat_fio, ib_num, ages, dept, doc_fio, days, diag_start, dates)
VALUES
('ТЛЯЧЕВ А.С.', '25649-2024', 38, 'ОРИТ №1', 'Рак В.А.', 5, 'U07.1', LOCALTIMESTAMP),
('КАШИН П.В.', '26748-2024', 42, 'ОРИТ №1', 'Плюмов С.Е.', 8, 'U07.2', LOCALTIMESTAMP),
('КОЛОВ К.Т.', '26114-2024', 37, 'ОРИТ №1', 'Каширин В.В.', 4, 'J06.1', LOCALTIMESTAMP),
('РАЗУМОВА Р.Н.', '25469-2024', 29, 'ОРИТ №2', 'Бунин А.С.', 1, 'U07.1', LOCALTIMESTAMP),
('КОЗЛОВА А.С.', '25647-2024', 38, 'ОРИТ №2', 'Рак В.А.', 6, 'U07.1', LOCALTIMESTAMP),
('ПЕРОВ П.В.', '26775-2024', 42, 'ОРИТ №2', 'Плюмов С.Е.', 9, 'U07.2', LOCALTIMESTAMP),
('АТАЛА К.Т.', '26173-2024', 37, 'ОРИТ №2', 'Каширин В.В.', 12, 'J06.1', LOCALTIMESTAMP);


CREATE TABLE mm.waitings (
	id serial4 NOT NULL,
	fio_pat varchar(50) NULL,
	ib_num varchar(10) NULL,
	dept varchar(50) NULL,
	waiting_time time NULL,
	doc_fio varchar(50) NULL
);

INSERT INTO mm.waitings (fio_pat,ib_num,dept,waiting_time,doc_fio)
VALUES
('Карпов В.В.','316-24','Неврологическое отделение','01:16:03','Рыков О.В.'),
('Титов А.К.','346-24','Кардиологическое отделение','02:43:18','Аясов Т.У.');


CREATE TABLE mm.total_refuse (
	id serial4 NOT NULL,
	fio_doc varchar(50) NULL,
	total_refuse int2 NULL,
	CONSTRAINT total_refuse_pkey PRIMARY KEY (id)
);


INSERT INTO mm.total_refuse (fio_doc,total_refuse)
VALUES
('Дробинов В.В.',1),
('Кашин Е.С.',2),
('Ломов Б.В.',1);


CREATE TABLE mm.refuse (
	id serial4 NOT NULL,
	fio_pat varchar(50) NULL,
	ib_num varchar(10) NULL,
	diag varchar(50) NULL,
	refuse_reason varchar(50) NULL,
	refuse_date timestamp NULL,
	fio_doc varchar(50) NULL,
	CONSTRAINT refuse_pkey PRIMARY KEY (id)
);


INSERT INTO mm.refuse (fio_pat,ib_num,diag,refuse_reason,refuse_date,fio_doc)
VALUES
('Мылашева О.В.','230','E53.1 Инсульт','Не соответствует профилю стационара','2024-05-16 02:06:23.000','Дробинов В.В.'),
('Сергеев П.М.','264','K78.2 Камни в почках','Не соответствует профилю стационара','2024-05-16 14:16:44.000','Кашин Е.С.'),
('Попова К.В.','274','J16.5 Отит','Не соответствует профилю стационара','2024-05-14 19:54:32.000','Ломов Б.В.'),
('Тлячев О.В.','269','B06.2 Сальмонеллез','Не соответствует профилю стационара','2024-05-12 05:47:26.000','Кашин Е.С.');
