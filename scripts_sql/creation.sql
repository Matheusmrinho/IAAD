use iaad;

CREATE TABLE diretor (
    nome_diretor VARCHAR(100),
    num_diretor INT,
	PRIMARY KEY (nome_diretor, num_diretor)
);

CREATE TABLE canal (
    num_canal INT PRIMARY KEY,
    nome VARCHAR(50),
    sigla VARCHAR(25)
);

CREATE TABLE filme (
    num_filme INT PRIMARY KEY,
    titulo_original VARCHAR(80) NOT NULL,
    titulo_brasil VARCHAR(80),
    ano_lancamento YEAR NOT NULL,
    pais_origem VARCHAR(30),
    categoria VARCHAR(25),
    duracao INT NOT NULL,
    nome_diretor VARCHAR(100)
    -- FOREIGN KEY (nome_diretor) REFERENCES diretor(nome_diretor)
);

CREATE TABLE exibicao (
    num_filme INT,
    num_canal INT,
    data DATETIME,
    PRIMARY KEY (num_filme, num_canal, data),
    FOREIGN KEY (num_filme) REFERENCES filme(num_filme),
    FOREIGN KEY (num_canal) REFERENCES canal(num_canal)
);


ALTER TABLE filme ADD FOREIGN KEY (nome_diretor) REFERENCES diretor(nome_diretor);