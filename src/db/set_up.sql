DROP TABLE IF EXISTS user_table cascade;
DROP TABLE IF EXISTS inventory_table cascade;


--    Creates a User table
--    containing user

CREATE TABLE user_table(
    user_id SERIAL PRIMARY KEY ,
    phone_number varchar(10),
    email varchar(100),
    firstname TEXT NOT NULL ,
    lastname varchar(50),
    username varchar(50),
    user_password varchar(255),
    session_key  varchar(255)
);


--    Creates a User table
--    containing user
CREATE TABLE inventory_table(
    book_id  SERIAL PRIMARY KEY,
    title varchar(255),
    genre varchar(255),
    publish_date varchar(255),
    author varchar(255),
    quanity INT NOT NULL,
    user_id INT NULL,
    FOREIGN KEY (user_id) REFERENCES user_table(user_id)

 );





