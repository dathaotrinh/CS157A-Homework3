CREATE USER IF NOT EXISTS 'username'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON WaterCarrier.* TO 'username'@'localhost';
USE MYSQL;

CREATE DATABASE WaterCarrier;

USE WaterCarrier;

CREATE TABLE user (
	userid	INT AUTO_INCREMENT,
	username	VARCHAR(50) NOT NULL UNIQUE,
	firstname	VARCHAR(50) NOT NULL,
	lastname	VARCHAR(50) NOT NULL,
	email	VARCHAR(50) NOT NULL UNIQUE,
	password	VARCHAR(50) NOT NULL,
	PRIMARY KEY(userid)
);

CREATE TABLE event (
	eventid	INT AUTO_INCREMENT,
	difficulty	VARCHAR(50) NOT NULL,
	duration	VARCHAR(50) NOT NULL,
	score		FLOAT NOT NULL,
	userid	INT NOT NULL,
	result	INT NOT NULL,
	FOREIGN KEY(userid) REFERENCES user(userid),
	PRIMARY KEY(eventid)
);