# Milestone3SE3400
implementation of our chrome extension

# Purpose
This is a simple chrome extension that helps researches know important information about a webpage in the google search results before they click on it.  This extension searches each link, placing an icon for the following issues:
1. Web Security
1. Exsesive Ads
1. Family Friendly Content
1. Cookies
1. Journaling Bias
1. Pay walls
1. Subscriptions

# Development

## Api
This system uses a simple api to store custom user settings.  Setting up an account is not requred to use this tool, however if you would like to use custom settings you will need to setup an account.  Accounts only require a first and last name, and email, and a password.

The user settings are stored in a mysql database.  More information on the api is avaible on the api readme.

## Extension
The extension hosts the user settings pages/popups and the code required to loop through google search results pages.  
