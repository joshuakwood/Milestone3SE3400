DROP DATABASE IF EXISTS `headsup_data`;

CREATE DATABASE IF NOT EXISTS `headsup_data`;

CREATE TABLE IF NOT EXISTS `headsup_data`.`users` (
	user_id INT AUTO_INCREMENT,
	first_name VARCHAR(200),
    last_name VARCHAR(200),
    email VARCHAR(300),
    encrypted_password VARCHAR(500),
    PRIMARY KEY (user_id)
    );
    
CREATE USER IF NOT EXISTS `client`@`localhost` IDENTIFIED BY 'clientPassword5!';
GRANT ALL ON `headsup_data`.* TO `client`@`localhost`;
FLUSH PRIVILEGES;


    