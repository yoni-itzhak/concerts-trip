CREATE TABLE cities {
  id INT(11) NOT NULL,
  city_name VARCHAR(50) NOT NULL,
  country_id INT(11) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY (country_id) REFERENCES countries (id)
}

CREATE TABLE countries {
  id INT(11) NOT NULL,
  country_name VARCHAR(50) NOT NULL,
  continent_id INT(11) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY (continent_id) REFERENCES continents (id)
 }

CREATE TABLE continents {
  id INT(11) NOT NULL,
  continent_name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
 }

CREATE TABLE artists {
  id INT(11) NOT NULL,
  artist_name VARCHAR(100) NOT NULL,
  popularity INT(11) NOT NULL,
  followers BIGINT(20) NOT NULL,
  img_link TEXT,
  img_height INT(11),
  img_width INT(11),
  description TEXT,
  PRIMARY KEY (id)
}

CREATE TABLE genres {
  id INT(11) NOT NULL,
  genre_name VARCHAR(50) NOT NULL,
  popularity INT(11),
  PRIMARY KEY (id)
 }

CREATE TABLE players {
  id INT(11) NOT NULL,
  player_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
 }

CREATE TABLE events {
  id INT(11) NOT NULL,
  event_name VARCHAR(200) NOT NULL,
  popularity FLOAT
  date DATE
  time TIME
  kick_link VARCHAR(400)
  venue_id INT(11),
  PRIMARY KEY (id),
  FOREIGN KEY(venue_id) REFERENCES venues (id)
}

CREATE TABLE venues {
  id INT(11) NOT NULL,
  name VARCHAR(200) NOT NULL,
  lat VARCHAR(50),
  lng VARCHAR(50),
  description TEXT,
  address VARCHAR(200),
  website VARCHAR(200),
  capacity INT(11),
  phone VARCHAR(50),
  city_id INT(11) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY(city_id) REFERENCES cities (id)
}

CREATE TABLE artist_event {
  artist_id INT(11) NOT NULL,
  event_id INT(11) NOT NULL,
  is_headline INT(11) NOT NULL,
  FOREIGN KEY(artist_id) REFERENCES artists (id)
  FOREIGN KEY(event_id) REFERENCES events (id)
}

CREATE TABLE artist_player {
  artist_id INT(11) NOT NULL,
  player_id INT(11) NOT NULL,
  FOREIGN KEY(artist_id) REFERENCES artists (id)
  FOREIGN KEY(player_id) REFERENCES players (id)
}

CREATE TABLE artist_genre {
  artist_id INT(11) NOT NULL,
  genre_id INT(11) NOT NULL,
  FOREIGN KEY(artist_id) REFERENCES artists (id)
  FOREIGN KEY(genre_id) REFERENCES genres (id)
}