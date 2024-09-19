'''Trigger para logs de alterações'''
CREATE TRIGGER before_filme_update
BEFORE UPDATE ON filme
FOR EACH ROW
BEGIN
    -- Exemplo: Registro de uma alteração em um log (caso o título original mude)
    IF OLD.titulo_original != NEW.titulo_original THEN
        INSERT INTO filme_log (num_filme, old_titulo, new_titulo, data_alteracao)
        VALUES (OLD.num_filme, OLD.titulo_original, NEW.titulo_original, NOW());
    END IF;
END;

'''Trigger para logs de exclusões'''
CREATE TRIGGER after_filme_delete
AFTER DELETE ON filme
FOR EACH ROW
BEGIN
    -- Exemplo: Registro de uma exclusão em um log
    INSERT INTO filme_log (num_filme, old_titulo, new_titulo, data_alteracao)
    VALUES (OLD.num_filme, OLD.titulo_original, NULL, NOW());
END;

-- Cria uma nova coluna para armazenar a quantidade de exibições no filme
ALTER TABLE filme ADD COLUMN qtd_exibicoes INT DEFAULT 0;

-- Trigger para atualizar o número de exibições de um filme
CREATE TRIGGER update_exibicoes_count
AFTER INSERT ON exibicao
FOR EACH ROW
BEGIN
    UPDATE filme 
    SET qtd_exibicoes = qtd_exibicoes + 1
    WHERE num_filme = NEW.num_filme;
END;

'''Trigger para evitar inserção de exibições no passado'''
CREATE TRIGGER prevent_past_exibicao
BEFORE INSERT ON exibicao
FOR EACH ROW
BEGIN
    IF NEW.data < NOW() THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Não é permitido inserir uma exibição com data no passado.';
    END IF;
END;
'''Trigger para logs de alterações'''
CREATE TABLE log_exibicao (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    num_filme INT,
    num_canal INT,
    data_antiga DATETIME,
    data_nova DATETIME,
    data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER log_exibicao_changes
AFTER UPDATE ON exibicao
FOR EACH ROW
BEGIN
    INSERT INTO log_exibicao (num_filme, num_canal, data_antiga, data_nova)
    VALUES (OLD.num_filme, OLD.num_canal, OLD.data, NEW.data);
END;

'''Trigger para evitar inserção de filmes com duração inferior a 40 minutos'''
CREATE TRIGGER check_film_duration
BEFORE INSERT ON filme
FOR EACH ROW
BEGIN
    IF NEW.duracao < 40 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'A duração do filme não pode ser inferior a 40 minutos.';
    END IF;
END;

'''Trigger para deletar filmes em cascata'''
CREATE TRIGGER delete_exibicoes_on_filme_delete
AFTER DELETE ON filme
FOR EACH ROW
BEGIN
    DELETE FROM exibicao WHERE num_filme = OLD.num_filme;
END;

'''Trigger para atualizar a sigla do canal'''
CREATE TRIGGER update_canal_sigla
BEFORE UPDATE ON canal
FOR EACH ROW
BEGIN
    SET NEW.sigla = LEFT(NEW.nome, 3);
END;

