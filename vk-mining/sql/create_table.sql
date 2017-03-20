DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Contacts;
DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Groups_members;
DROP TABLE IF EXISTS Links;
DROP TABLE IF EXISTS Users_friends;
DROP TABLE IF EXISTS Relatives;	
DROP TABLE IF EXISTS Group_count;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Messages_stats;

CREATE TABLE Users (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	uid INTEGER NOT NULL,
	is_actual INTEGER,
	date_actual TEXT,
	deactivated TEXT,
	first_name TEXT,
	last_name TEXT,
	bdate TEXT,
	sex INTEGER,
	country INTEGER,
	city INTEGER,
	political INTEGER,
	religion TEXT,
	people_main INTEGER,
	life_main INTEGER,
	alchohol INTEGER,
	smoking INTEGER
);

CREATE TABLE Groups (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	gid INTEGER NOT NULL,
	is_actual INTEGER,
	date_actual TEXT,
	name TEXT,
	screen_name TEXT,
	type TEXT,
	is_closed INTEGER,
	description TEXT
);

CREATE INDEX Groups_gid ON Groups(gid);

CREATE TABLE Links (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	group_id INTEGER,
	lid INTEGER NOT NULL,
	is_actual INTEGER,
	date_actual TEXT,
	url TEXT,
	name TEXT,
	desc TEXT 
);

CREATE INDEX Links_gid ON Links(group_id);

CREATE TABLE Contacts (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	user_id INTEGER,
	group_id INTEGER,
	is_actual INTEGER,
	date_actual TEXT,
	desc TEXT,
	phone TEXT,
	email TEXT
);

CREATE INDEX Contacts_gid ON Contacts(group_id);

CREATE TABLE Groups_members (
	id INTEGER NOT NULL PRIMARY KEY  UNIQUE,
	group_id INTEGER,
	user_id INTEGER,
	is_actual INTEGER,
	date_actual TEXT,
	status TEXT,
	source TEXT
);

CREATE INDEX Groups_members_gid ON Groups_members (group_id, user_id);

CREATE TABLE Users_friends (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	user_id INTEGER,
	friend_id INTEGER,
	is_actual INTEGER,
	date_actual TEXT,
	status TEXT(8)
);

CREATE TABLE Relatives (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	user_id INTEGER,
	relative_id INTEGER,
	is_actual INTEGER,
	date_actual TEXT,
	type TEXT(8),
	name TEXT
);

CREATE TABLE Group_count (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	group_id INTEGER,
	date_actual TEXT,
	count INTEGER
);

CREATE INDEX Group_count_gid ON Group_count (group_id);

CREATE TABLE Messages (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	mid INTEGER,
	from_id INTEGER,
	signer_id INTEGER,
	to_id INTEGER,
	date TEXT,
	text TEXT,
	marked_as_ads INTEGER
	is_actual INTEGER,
	date_actual TEXT,
	deleted INTEGER
);

CREATE TABLE Messages_stats (
	id INTEGER NOT NULL PRIMARY KEY UNIQUE,
	mid INTEGER,
	to_id INTEGER,
	reposts_count INTEGER,
	likes_count INTEGER,
	comments INTEGER,
	is_pinned INTEGER,
	is_actual INTEGER,
	date_actual TEXT
);