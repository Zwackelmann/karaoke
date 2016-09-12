CREATE TABLE artist(
    id SERIAL,
    name TEXT,
    PRIMARY KEY(id)
);

CREATE INDEX artist_trgm_idx ON artist USING GIN (name gin_trgm_ops);
CREATE INDEX artist_name_idx ON artist(name);

CREATE TABLE song(
    id SERIAL,
    artist INT NOT NULL,
    title TEXT,
    artist_title TEXT,
    FOREIGN KEY (artist) REFERENCES artist
);

CREATE INDEX song_title_trgm_idx ON song USING GIN (title gin_trgm_ops);
CREATE INDEX song_title_artist_trgm_idx ON song USING GIN (artist_title gin_trgm_ops);
CREATE INDEX song_artist ON song(artist);