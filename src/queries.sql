-- Consulta para obter todos os filmes exibidos por um canal específico
SELECT f.titulo_brasil, c.nome, e.data
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
JOIN canal c ON e.num_canal = c.num_canal
WHERE c.nome = 'Canal Exemplo';

-- Consulta para contar quantas vezes um filme foi exibido
SELECT f.titulo_brasil, COUNT(e.num_filme) AS numero_exibicoes
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
GROUP BY f.titulo_brasil;

-- Consulta para obter a duração média dos filmes por categoria
SELECT f.categoria, AVG(f.duracao) AS duracao_media
FROM filme f
GROUP BY f.categoria;
