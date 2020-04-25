CREATE TABLE cities (
  id INT(11) NOT NULL,
  city_name VARCHAR(50) NOT NULL,
  country_id INT(11) NOT NULL,
  PRIMARY KEY(id)
  );

CREATE TABLE countries (
  id INT(11) NOT NULL,
  country_name VARCHAR(50) NOT NULL,
  continent_id INT(11) NOT NULL,
  PRIMARY KEY(id)
  );

CREATE TABLE continents (
  id INT(11) NOT NULL,
  continent_name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
 );

CREATE TABLE artists (
  id INT(11) NOT NULL,
  artist_name VARCHAR(100) NOT NULL,
  popularity INT(11) NOT NULL,
  followers BIGINT(20) NOT NULL,
  img_link TEXT,
  description TEXT,
  PRIMARY KEY (id)
  );

CREATE TABLE genres (
  id INT(11) NOT NULL,
  genre_name VARCHAR(50) NOT NULL,
  popularity INT(11),
  PRIMARY KEY (id)
  );

CREATE TABLE players (
  id INT(11) NOT NULL,
  player_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
  );

CREATE TABLE events (
  id INT(11) NOT NULL,
  event_name VARCHAR(200) NOT NULL,
  popularity FLOAT
  date DATE
  kick_link VARCHAR(400)
  venue_id INT(11),
  PRIMARY KEY (id)
  );

CREATE TABLE venues (
  id INT(11) NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  lat VARCHAR(50),
  lng VARCHAR(50),
  city_id INT(11) NOT NULL,
  PRIMARY KEY (id)
  );

CREATE TABLE artist_event (
  artist_id INT(11) NOT NULL,
  event_id INT(11) NOT NULL,
  is_headline INT(11) NOT NULL,
  PRIMARY KEY (artist_id, event_id)
  );

CREATE TABLE artist_player (
  artist_id INT(11) NOT NULL,
  player_id INT(11) NOT NULL,
  PRIMARY KEY (artist_id, player_id)
  );

CREATE TABLE artist_genre (
  artist_id INT(11) NOT NULL,
  genre_id INT(11) NOT NULL,
  PRIMARY KEY (artist_id, genre_id)
  );

ALTER TABLE events ADD FOREIGN KEY (venue_id) REFERENCES venues (id);
ALTER TABLE venues ADD FOREIGN KEY (city_id) REFERENCES cities (id);
ALTER TABLE cities ADD FOREIGN KEY (country_id) REFERENCES countries (id);
ALTER TABLE countries ADD FOREIGN KEY (continent_id) REFERENCES continents (id);
ALTER TABLE artist_event ADD FOREIGN KEY (artist_id) REFERENCES artists (id);
ALTER TABLE artist_event ADD FOREIGN KEY (event_id) REFERENCES events (id);
ALTER TABLE artist_player ADD FOREIGN KEY (artist_id) REFERENCES artists (id);
ALTER TABLE artist_player ADD FOREIGN KEY (player_id) REFERENCES players (id);
ALTER TABLE artist_genre ADD FOREIGN KEY (artist_id) REFERENCES artists (id);
ALTER TABLE artist_genre ADD FOREIGN KEY (genre_id) REFERENCES genres (id);

CREATE UNIQUE INDEX events_id_date ON events (id, date);
CREATE UNIQUE INDEX events_id_popularity ON events (id, popularity);
CREATE UNIQUE INDEX venues_id_city ON venues (id, city_id);
CREATE UNIQUE INDEX artists_id_popularity ON artists (id, popularity);
CREATE UNIQUE INDEX artists_id_followers ON artists (id, followers);
CREATE UNIQUE INDEX city_country_key ON cities (id, country_id);
CREATE UNIQUE INDEX country_continent_key ON countries (id, continent_id);
CREATE UNIQUE INDEX players_id_name ON players (id, player_name);
CREATE UNIQUE INDEX genre_id_name ON genres (id, genre_name);
CREATE UNIQUE INDEX genre_id_popularity ON genres (id, popularity);
CREATE UNIQUE INDEX artist_to_event ON artist_event (event_id, artist_id, is_headline);
CREATE UNIQUE INDEX artist_to_player ON artist_player (artist_id, player_id);
CREATE UNIQUE INDEX artist_to_genre ON artist_genre (artist_id, genre_id);
CREATE UNIQUE INDEX fulltext_venue_desc ON venues (description);
CREATE UNIQUE INDEX fulltext_artist_desc ON artists (description);