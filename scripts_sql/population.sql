Use iaad;
INSERT INTO canal Values
(001,'HBO','HBO'),
(002, 'Telecine', 'TC'),
(003, 'MegaPix','MP'),
(004, 'Fox', 'FX'),
(005, 'Cinemax', 'CM'), 
(006,'Paramount', 'PM'),
(007, 'TNT', 'TNT'),
(008, 'Space', 'SP'),
(009, 'Warner', 'WR'),
(010, 'MAX', 'MAX');

INSERT INTO filme Values
(01,'Justice League','Liga da Justiça',2017,'EUA','Ação',120, 'Zack Snyder'),
(02, 'The Exorcist: Believer', 'O Exorcista: O Devoto', 2023, 'EUA', 'Terror', 105, 'David Gordon Green'),
(03, 'Tô Ryca! 2', 'Tô Ryca! 2', 2020, 'Brasil', 'Comédia', 102, 'Pedro Antônio'),
(04, 'Maze Runner: The Scorch Trials', 'Maze Runner - Prova de Fogo', 2015, 'EUA', 'Ficção científica', 133, 'Wes Ball'),
(05, 'Spy Kids', 'Pequenos Espiões', 2001, 'EUA', 'Aventura', 90, 'Robert Rodriguez'),
(06, 'Mean Girls', 'Meninas Malvadas', 2004, 'EUA', 'Comédia', 96, 'Mark Waters'),
(07, '2 Filhos de Francisco: A História de Zezé di Camargo & Luciano', '2 Filhos de Francisco: A História de Zezé di Camargo & Luciano', 2005, 'Brasil', 'Drama', 132, 'Breno Silveira'),
(08, 'Pacific Rim', 'Círculo de Fogo', 2013, 'EUA', 'Ficção científica', 131, 'Guillermo del Toro'),
(09, 'It Chapter Two', 'It - Capítulo 2', 2019, 'EUA', 'Terror', 170, 'Andy Muschietti'),
(10, 'The Suicide Squad', 'O Esquadrão Suicida', 2021, 'EUA', 'Comédia', 132, 'James Gunn');


INSERT INTO exibicao VALUES 
(01, 001,'2024-09-11 18:30:00'),
(02,002,'2024-09-11 19:00:00'),
(03,003,'2024-09-12 15:45:30'),
(04,004,'2024-09-13 20:00:20'),
(05,005,'2024-09-13 16:30:00'),
(06,006,'2024-09-13 17:00:30'),
(07,007,'2024-09-14 14:20:00'),
(08,008,'2024-09-15 18:00:00'),
(09,009,'2024-09-15 21:45:30'),
(10,010,'2024-09-15 20:30:00');

INSERT INTO diretor VALUES
('Zack Snyder', 01),
('David Gordon Green', 02),
('Pedro Antônio', 03),
('Wes Ball', 04),
('Robert Rodriguez', 05),
('Mark Waters', 06),
('Breno Silveira', 07),
('Guillermo del Toro', 08),
('Andy Muschietti', 09),
('James Gunn', 10);