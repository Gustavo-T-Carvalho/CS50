SELECT title FROM movies WHERE id IN (
    SELECT BradleyMovies.movie_id FROM
    (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Bradley Cooper")) BradleyMovies
    JOIN
    (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = "Jennifer Lawrence")) JenniferMovies
    ON JenniferMovies.movie_id = BradleyMovies.movie_id
);


-- WITH filmes_jen AS (
--     SELECT m.title
--     FROM movies m
--     LEFT JOIN stars s ON m.id = s.movie_id
--     LEFT JOIN people p ON s.person_id = p.id
--     WHERE p.name = 'Jennifer Lawrence'
-- )
-- SELECT DISTINCT m.title
-- FROM movies m
-- LEFT JOIN stars s ON m.id = s.movie_id
-- LEFT JOIN people p ON s.person_id = p.id
-- WHERE p.name = 'Bradley Cooper'
--   AND m.title IN (SELECT title FROM filmes_jen);
