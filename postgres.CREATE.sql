CREATE TABLE IF NOT EXISTS genres (
    id serial PRIMARY KEY,
    genre varchar(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS executors (
    id serial PRIMARY KEY,
    nickname varchar(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS executors_genres (
    executor_id INT NOT NULL REFERENCES executors(id),
    genre_id INT NOT NULL REFERENCES genres(id),
    CONSTRAINT executor_genre_pk PRIMARY KEY (executor_id, genre_id)
);


CREATE TABLE IF NOT EXISTS albums (
    id serial PRIMARY KEY,
    album_title varchar(50) NOT NULL,
    year_of_release INT NOT NULL
);


CREATE TABLE IF NOT EXISTS albums_executors (
    album_id INT NOT NULL REFERENCES albums(id),
    executor_id INT NOT NULL REFERENCES executors(id),
    CONSTRAINT album_executor_pk PRIMARY KEY (album_id, executor_id)
);


CREATE TABLE IF NOT EXISTS tracks (
    id serial PRIMARY KEY,
    track_name varchar(50) NOT NULL,
    duration INT,
    album_id INT NOT NULL REFERENCES albums(id)
);


CREATE TABLE IF NOT EXISTS music_collections (
    id serial PRIMARY KEY,
    title varchar(50) NOT NULL,
    year_of_release INT NOT NULL
);


CREATE TABLE IF NOT EXISTS music_collections_tracks (
    music_collection_id INT NOT NULL REFERENCES music_collections(id),
    track_id INT NOT NULL REFERENCES tracks(id),
    CONSTRAINT music_collection_track_pk PRIMARY KEY (music_collection_id, track_id)
);

