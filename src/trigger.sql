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
