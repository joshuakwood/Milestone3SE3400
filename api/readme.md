# Heads-up API

## GET
### /data 
- "Returns default filter data from server"
(Takes no inputs)

### /sessions 
- "Returns user data if the user is logged into an account."
(Takes no inputs)

## POST
### /sessions 
- "Logs the user into the system, returning a session cookie"
email = string
password = string

/users 
- "Creates a new user, does not create a login cookie"
first_name = string
last_name = string
email = string  (NOTE: the api does not have any validation for emails)
password = string

/filters 
- "If the user is logged in, creates a new filter for website)
website = string    (NOTE: the api does not have validation for urls)
default filters for everything is set to false initially

## PUT
### /users/filter-settings 
- "If the user is logged in and filter (website) exists, this changes filter settings for a specific webiste on the users account"
website = string    (NOTE: the api does not have validation for urls)
new_filter_settings = string in json format 

(example: {"ads": 1,"cookies": 1,"paywall": 0,"bias-source": 1,"cyber_safety": 0,"subscription": 0,"family_friendly": 1})

The filter settings string must include each of the columns for filter flags
Namely:
    ads  
    cookies
    paywall
    bias-source
    cyber_safety
    subscription
    family_friendly
the number 1 = True, the number 0 = False

### /users/account-settings 
- "If the user is logged in, changes account details"
first_name = string
last_name = string
email = string  (NOTE: the api does not have any validation for emails)  

### /users/change-password
- "If the user is logged in, changes account password"
new_password = string

## DELETE
### /users/account 
- "If user is logged in, Perminently deletes user account"
(Takes no inputs)

### /users/filters 
- "If user is logged in and website exists, Perminently deletes selected website filter settings"
website = string    (NOTE: the api does not have validation for urls)