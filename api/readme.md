# Heads-up API

## Installation
### Server
The server runs natively on python. Rever to the python package requirements to ensure that each package is installed properly.  

packages are in requirements_dev.txt

### Database
This api stores data in a Mysql database.  Two tables are used.  The first is a normal mysql relational table, the second is a mysqlx collection. The responsibiliites of each are exmplained in the following subsections.

## Users Schema
### Purpose
To store user data for setting up an account. The id is auto generated and will match the id in the User Settings Schema.

### SQL 
NOTE: Please refer to the schema.sql file to initialize the database.  That file will setup this table as well as the client user account used by the server to manipulate the database.  
```
CREATE TABLE IF NOT EXISTS `headsup_data`.`users` (
	user_id INT AUTO_INCREMENT,
	first_name VARCHAR(200),
    last_name VARCHAR(200),
    email VARCHAR(300),
    encrypted_password VARCHAR(500),
    PRIMARY KEY (user_id)
    );
```
## User Settings Schema
### Purpose
To store user account settings in single json files.  This makes it possible to sync settings for users accross devices as well as alow us to collect data on which websites are flagged the most with issues.  We can use this data to improve the default settings over time.

### SQL
NOTE: This table is generated automatically by the server.  There is no need to run this script in the MySQL server.
```
CREATE TABLE `user_settings` (
  `doc` json DEFAULT NULL,
  `_id` varbinary(32) GENERATED ALWAYS AS (json_unquote(json_extract(`doc`,_utf8mb4'$._id'))) STORED NOT NULL,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  PRIMARY KEY (`_id`),
  CONSTRAINT `$val_strict_5892DC7B36E9B748D84B008DFAA80123C358E103` CHECK (json_schema_valid(`_json_schema`,`doc`)) /*!80016 NOT ENFORCED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## API Reference
Name | Method | Path | Returns | Notes
-|-|-|-|-
Get Data | GET | /data | None | Returns default filter data from server
Get User Settings | GET | /sessions | None | Returns user data if the user is logged into an account.
Login User | POST | /sessions | email:(str),  password:(str) | Logs the user into the system, returning a session cookie
Create User | POST | /users | first_name:(str), last_name:(str), email:(str), password:(str) | Creates a new user, does not create a login cookie.  (!IMPORTANT: the api does not have any validation for emails)
Create Filter | POST | /filters | website:(str),  | If the user is logged in, creates a new filter for website.  Default filters for everything is set to false initially. (!IMPORTANT: the api does not have validation for urls)
Change Filter | PUT | /users/filter-settings | website:(str), new_filter_settings:(str in json format) | If the user is logged in and filter (website) exists, this changes filter settings for a specific webiste on the users account. example: {"ads": 1,"cookies": 1,"paywall": 0,"bias-source": 1,"cyber_safety": 0,"subscription": 0,"family_friendly": 1} 
Change Account Details | PUT | /users/account-settings | first_name:(str), last_name:(str) | If the user is logged in, changes account details. 
Change User Password | PUT | /users/change-password | new_password:(str) | If the user is logged in, changes account password.
Delete User | DELETE | /users/account | None | If user is logged in, Perminently deletes user account.
Delete Filter | DELETE | /users/filters | website:(str) | If user is logged in and website exists, Perminently deletes selected website filter settings. !IMPORTANT: the api does not have validation for urls

The filter settings string must include each of the columns for filter flags.
Namely:
* ads  
* cookies
* paywall
* bias-source
* cyber_safety
* subscription
* family_friendly
The number 1 = True, the number 0 = False.

### Data Notes
All data should be x-www-form-urlenocoded data.  

## Cookies
This api uses a very simple cookie to store users logged in and authenticated state.  This is for the ease of the user so that a login is not required with every action.
