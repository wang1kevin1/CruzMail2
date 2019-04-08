# To manually create/use a database:
# usage: terminal/command line
# create a database:
# type: 'mysql -u root' to launch mysql terminal
# CREATE DATABASE db_name;
# You can type 'show databases;' to make sure your db has been successfully created.
# mysql -u root -A db_name < cruzmail_db.sql
# Make sure you are using the correct database.
# Type 'USE db_name;' to use the right db.
#
# May have to edit a configuration file in Django to connect to this database.

DROP DATABASE IF EXISTS cruzmail_db;
CREATE DATABASE IF NOT EXISTS cruzmail_db CHARACTER SET utf8;
USE cruzmail_db;

DROP TABLE IF EXISTS mailstops_master,
                     people_master,
                     packages_master;

CREATE TABLE mailstops_master (
  mailstop VARCHAR(15) NOT NULL,
  ms_name VARCHAR(30) NOT NULL,
  ms_route ENUM('W','C','E') NOT NULL,
  ms_route_order VARCHAR(3) NOT NULL,
  ms_status ENUM('Active','Inactive') NOT NULL,
  PRIMARY KEY (mailstop)
);

CREATE TABLE people_master (
  name VARCHAR(20) NOT NULL,
  ppl_email VARCHAR(40) NOT NULL,
  ppl_status ENUM('Available', 'Away') NOT NULL,
  mailstop VARCHAR(20) NOT NULL,
  FOREIGN KEY (mailstop) REFERENCES mailstops_master(mailstop) ON UPDATE CASCADE,
  PRIMARY KEY (name, mailstop)
);

CREATE TABLE packages_master (
  pkg_tracking VARCHAR(20) NOT NULL,
  name VARCHAR(20) NOT NULL,
  mailstop VARCHAR(20) NOT NULL,
  pkg_status ENUM('received','delivered') NOT NULL,
  pkg_sign ENUM('yes','no') NOT NULL DEFAULT 'no',
  pkg_email ENUM('yes','no') NOT NULL DEFAULT 'yes',
  pkg_weight ENUM('1 to 5','6 to 15','over 16'),
  pkg_date_rec DATE NOT NULL,
  pkg_date_del DATE NOT NULL,
  pkg_remarks VARCHAR(144),
  FOREIGN KEY (name) REFERENCES people_master(name) ON UPDATE CASCADE,
  FOREIGN KEY (mailstop) REFERENCES mailstops_master(mailstop) ON UPDATE CASCADE,
  PRIMARY KEY (pkg_tracking)
);
