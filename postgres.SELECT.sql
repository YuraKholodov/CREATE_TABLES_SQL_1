SELECT track_name, duration
FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);


SELECT track_name
FROM tracks
WHERE duration >= 210;


SELECT title
FROM music_collections
WHERE year_of_release BETWEEN 2018 AND 2020;


SELECT nickname
FROM executors
WHERE nickname NOT LIKE '% %';


SELECT track_name
FROM tracks
WHERE track_name LIKE '%мой%' OR track_name LIKE '%my%';


SELECT gen.genre, COUNT(exe.nickname)
FROM genres as gen JOIN executors_genres as exe_gen ON gen.id = exe_gen.genre_id
JOIN executors as exe ON exe.id = exe_gen.executor_id
GROUP BY gen.genre;


SELECT COUNT(t.id)
FROM tracks as t JOIN albums as a ON t.album_id = a.id
WHERE a.year_of_release BETWEEN 2019 AND 2020;


SELECT a.album_title, AVG(t.duration)
FROM albums as a JOIN tracks as t ON a.id = t.album_id
GROUP BY a.album_title;


SELECT DISTINCT exe.nickname
FROM executors as exe JOIN albums_executors as al_exe ON exe.id = al_exe.executor_id
JOIN albums as a ON a.id = al_exe.album_id
WHERE a.year_of_release <> 2020;


SELECT DISTINCT mc.title
FROM music_collections AS mc JOIN music_collections_tracks as mc_tr ON mc.id = mc_tr.music_collection_id
JOIN tracks as t ON t.id = mc_tr.track_id
JOIN albums_executors as al_exe ON t.album_id = al_exe.album_id
JOIN executors as exe ON exe.id = al_exe.executor_id
WHERE exe.nickname = 'ДЕЦЛ';


