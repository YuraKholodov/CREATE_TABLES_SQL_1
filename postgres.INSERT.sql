INSERT INTO executors (nickname) 
VALUES ('Высоцкий'), ('Земфира'), ('Цой'), ('ДЕЦЛ');

INSERT INTO genres (genre) 
VALUES ('Попса'), ('Хип-Хоп'), ('Русский рок'), ('Поп-рок'), ('Инди рок'), ('Авторская песня');

INSERT INTO executors_genres (executor_id, genre_id) 
VALUES (1, 6), (2, 3), (2, 4), (2, 5), (3, 3), (3, 6), (4, 2);

INSERT INTO albums (album_title, year_of_release)
VALUES ('Сентиментальный боксёр', 1967), ('Кони привередливые', 1973), ('Грустный романс', 1992), 
('Бордерлайн', 2021), ('Вендетта', 2005),
('Звезда по имени солнце', 1989), ('Ночь', 1986),
('Кто ты?', 2000), ('Уличный боец', 2001);

INSERT INTO albums (album_title, year_of_release) VALUES ('Земфира не плачет', 2020);


INSERT INTO tracks (track_name, duration, album_id)
VALUES ('Шляпник', 250, 1), ('Баллада о бане', 219, 2), 
('Без шансов', 185, 4), ('Снег', 197, 5), 
('Игра', 180, 7), ('Камчатка', 185 ,6), 
('Вечеринка у ДеЦла', 190, 8), ('Принцесса', 175, 9);


INSERT INTO tracks (track_name, duration, album_id) VALUES ('Любимый мой!', 230, 2);
INSERT INTO tracks (track_name, duration, album_id) VALUES ('Мойщик намой мне купола!', 220, 1);


INSERT INTO music_collections (title, year_of_release)
VALUES ('Каспийский груз', 2008), ('Посидим, помолчим', 2020), 
('Сборник рока', 2021), ('ИнАгент', 2023), ('Оохох', 2015)


INSERT INTO music_collections_tracks (music_collection_id, track_id)
VALUES (1, 7), (1, 8), (2, 5), (2, 6), (3, 3), (3, 4), (4, 2);

INSERT INTO albums_executors (album_id, executor_id)
VALUES (1, 1), (2, 1), (3, 2), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4), (9, 4);

INSERT INTO albums_executors (album_id, executor_id) VALUES (10, 2);


