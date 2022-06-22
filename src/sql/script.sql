CREATE USER oluwasayo WITH PASSWORD password CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE <DB> TO oluwasayo;
CREATE DATABASE oluwasayo_serverless_workflow WITH OWNER = oluwasayo;

-- \c oluwasayo_serverless_workflow;
CREATE SCHEMA IF NOT EXISTS business_data;


CREATE TABLE business_data.user(
	uuid varchar(8) PRIMARY KEY NOT NULL,
  	first_name varchar(100) NOT NULL,
  	last_name varchar(100) NOT NULL,
  	email_address varchar(255) NOT NULL
)

CREATE TABLE business_data.visit(
    user_id varchar(8) not null,
    number_of_visits int not null,
    time_spent float not null,
    amount_spent float not null,
    date_of_visits date not null,
    foreign key user_id references business_data.user(uuid)
)
