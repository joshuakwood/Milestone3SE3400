HOST = 'localhost'
PORT = 33060
USER = 'client'
PASSWORD = 'clientPassword5!'
UPLOAD_FOLDER = '/mnt/s/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

import mysqlx
import json

from datetime import datetime
import socket
import logging
from inspect import currentframe, getframeinfo


class DataBase:

    def __init__(self):
        self.session = mysqlx.get_session(
            {'host': HOST, 'port': PORT, 'user': USER, 'password': PASSWORD})
        self.schema = self.session.get_schema('headsup_data')
        self.collection = self.schema.create_collection('user_settings', True)
        self.users = self.schema.get_table('users')
        return

    def createUser(self, first_name, last_name, email, encrypted_password):
        data = [first_name, last_name, email, encrypted_password]
        columns = ['first_name', 'last_name', 'email', 'encrypted_password']

        # save user login info in relational table
        self.session.start_transaction()
        result_rt = self.users.insert(columns).values(data).execute()
        row_id_rt = result_rt.get_autoincrement_value()
        warnings_rt = result_rt.get_warnings()
        rows_effected_rt = result_rt.get_affected_items_count()

        # Check if data was saved succesfully in relational table
        if warnings_rt != [] and rows_effected_rt != 1:
            self.session.rollback()
            self.session.close()
            error = "INSERT USER LOGIN DATA ERROR"
            for warning in warnings_rt:
                error += (warning + "\n")
            self.handleReports(error, getframeinfo(currentframe()), "error")
            return None

        # save user settings in collection
        f = open('data.json')
        default_data = json.load(f)
        settings_data = {'user_settings':{
                            'bias_source': 1,
                            'paywall':1,
                            'subscription':1,
                            'family_friendly':1,
                            'ads':1,
                            'cyber_safety':1,
                            'cookies':1
                             }, 
                        'websites':default_data}
        
        result_c = self.collection.add(
            {'_id': int(row_id_rt), 'doc': settings_data}).execute()
        collection_as_table = self.schema.get_collection_as_table('user_settings')
        row_id_c = int(collection_as_table.select(
            ["_id"]).where(("_id = '%s'" % row_id_rt)).execute().fetch_one()[0])
        warnings_c = result_c.get_warnings()
        rows_effected_c = result_c.get_affected_items_count()

        # Check if data was saved succesfully in collection
        if warnings_c != [] and rows_effected_c != 1:
            self.session.rollback()
            self.session.close()
            error = "INSERT USER SETTINGS ERROR"
            for warning in warnings_c:
                error += (warning + "\n")
            self.handleReports(error, getframeinfo(currentframe()), "error")
            return None

        # Check if id for relational table and id for colleciton match
        if row_id_c != row_id_rt:
            self.session.rollback()
            self.session.close()
            error = "INSERT ERROR - COLLECTIONS AND USER ID DO NOT MATCH"
            for warning in warnings_c:
                error += (warning + "\n")
            self.handleReports(error, getframeinfo(currentframe()), "error")
            return None

        # If checks pass, commit database changes and return new user id.
        self.session.commit()
        self.session.close()
        return row_id_c

    def findUserByEmail(self, email):
        result = self.users.select().where(("email = '%s'" % str(email))).execute()
        columns = list(result.get_columns())
        user = result.fetch_one()
        if user == None:
            return None
        user_list = list(user)
        user_dict = {}
        if len(columns) == len(user_list):
            for i in range(len(columns)):
                user_dict[columns[i].get_column_name()] = user_list[i]
        return user_dict

    def findUserById(self, user_id):
        result = self.users.select().where(("user_id = '%s'" % str(user_id))).execute()
        columns = list(result.get_columns())
        user = result.fetch_one()
        if user == None:
            return None
        user_list = list(user)
        user_dict = {}
        if len(columns) == len(user_list):
            for i in range(len(columns)):
                user_dict[columns[i].get_column_name()] = user_list[i]
        return user_dict

    def updateUser(self, user_id, first_name, last_name):
        self.session.start_transaction()
        updateStatement = self.users.update()
        updateStatement.set("first_name", str(first_name))
        updateStatement.set("last_name", str(last_name))
        updateStatement.where("user_id = %s"%user_id)
        result = updateStatement.execute()
        warnings = result.get_warnings()
        if warnings == []:
            self.session.commit()
            return True
        for warning in warnings:
            self.handleReports(warning, getframeinfo(currentframe()), "error")
        self.session.rollback()
        return False

    def updateUserPassword(self, user_id, password):
        self.session.start_transaction()
        updateStatement = self.users.update()
        updateStatement.set("encrypted_password", str(password))
        updateStatement.where("user_id = %s" % user_id)
        result = updateStatement.execute()
        warnings = result.get_warnings()
        if warnings == []:
            self.session.commit()
            return True
        for warning in warnings:
            self.handleReports(warning, getframeinfo(currentframe()), "error")
        self.session.rollback()
        return False

    def getUserData(self, email):
        # get user account data
        result = self.users.select().where(("email = '%s'" % str(email))).execute()
        columns = list(result.get_columns())
        user_account = result.fetch_one()
        if user_account == None:
            return None
        user_list = list(user_account)
        user_account_dict = {}
        if len(columns) == len(user_list):
            for i in range(len(columns)):
                user_account_dict[columns[i].get_column_name()] = user_list[i]

        # get user settings data
        user_settings = self.collection.get_one(user_account_dict["user_id"])

        # combine and return data
        user_settings["first_name"] = user_account_dict["first_name"]
        user_settings["last_name"] = user_account_dict["last_name"]
        user_settings["email"] = user_account_dict["email"]
        return dict(user_settings)

    def addFilter(self, website, email):
        user = self.findUserByEmail(email)
        user_settings = self.collection.get_one(user['user_id'])
        user_settings_dict = dict(user_settings)
        user_settings_dict["doc"]["websites"][website] = {
            "ads": 0,
            "cookies": 0,
            "paywall": 0,
            "bias_source": 0,
            "cyber_safety": 0,
            "subscription": 0,
            "family_friendly": 0
        }
        self.collection.add_or_replace_one(user["user_id"], user_settings_dict)

        user_settings = self.collection.get_one(user['user_id'])
        user_settings_dict = dict(user_settings)
        if website not in user_settings_dict["doc"]["websites"]:
            self.handleReports("Add Website Attempt Failed", getframeinfo(currentframe()), "error")
            return False
        return True

    def updateWebsiteSettings(self, website, email, new_filter_settings):
        filters = [ "ads",
                    "cookies",
                    "paywall",
                    "bias_source",
                    "cyber_safety",
                    "subscription",
                    "family_friendly"]

        user = self.findUserByEmail(email)
        user_settings = self.collection.get_one(user['user_id'])
        user_settings_dict = dict(user_settings)
        if website not in user_settings_dict["doc"]["websites"]:
            self.handleReports("Website does not exist to edit settings.", getframeinfo(currentframe()), "error")
            return False

        for i in range(len(filters)):
            user_settings_dict["doc"]["websites"][website][filters[i]] = new_filter_settings[filters[i]]
        self.collection.add_or_replace_one(user["user_id"], user_settings_dict)
        #TODO: Add method to check if edits were saved, return false if not save
        return True

    def updateFilterSettings(self, email, new_filter_settings):

        user = self.findUserByEmail(email)
        user_settings = self.collection.get_one(user['user_id'])
        user_settings_dict = dict(user_settings)

        user_settings_dict["doc"]["user_settings"] = dict(json.loads(new_filter_settings))
        self.collection.add_or_replace_one(user["user_id"], user_settings_dict)
        # TODO: Add method to check if edits were saved, return false if not save
        return True

    def deleteFilter(self, website, user_id):
        self.session.start_transaction()
        user_settings = self.collection.get_one(user_id)
        user_settings_dict = dict(user_settings)
        try:
            user_settings_dict["doc"]["websites"].pop(website)
            
        except KeyError:
            return True
        self.collection.add_or_replace_one(
            user_id, user_settings_dict)

        # check that the website filter settings were deleted
        user_settings = self.collection.get_one(user_id)
        user_settings_dict = dict(user_settings)
        if website in user_settings_dict["doc"]["websites"]:
            self.session.rollback()
            self.handleReports("Delete Website Settings Attempt Failed", getframeinfo(currentframe()), "error")
            return False
        self.session.commit()
        return True

    def deleteUser(self, user_id):
        self.session.start_transaction()

        # delete user
        self.users.delete().where(("user_id = '%s'" % str(user_id))).execute()

        if self.findUserById(user_id):
            self.handleReports("Delete User Attempt Failed", getframeinfo(currentframe()), "error")
            self.session.rollback()
            return False

        # delete user settings data
        collection_as_table = self.schema.get_collection_as_table("user_settings")
        collection_as_table.delete().where(("_id = '%s'" % str(user_id))).execute()

        user_exists = self.collection.get_one(user_id)
        if user_exists:
            self.handleReports("Delete User Settings Attempt Failed",
                               getframeinfo(currentframe()), "error")
            self.session.rollback()
            return False
            
        self.session.commit()
        return True
        
    def handleReports(self, string, frameInfo, type):
        ipAddress = str(socket.gethostbyname(socket.gethostname()))
        date_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        reportstring = (ipAddress + ' - - [' + date_time + ']  "' + string)
        #getframeinfo(currentframe())
        filename = frameInfo.filename
        linenumber = frameInfo.lineno
        logstring = filename + " | Line: " + \
            str(linenumber) + " | Report: " + reportstring
        logging.basicConfig(filename='AppErrors.log',
                            encoding='utf-8', level=logging.DEBUG)
        if type == "debug":
            logging.debug(logstring)
        elif type == "info":
            logging.info(logstring)
        elif type == "warning":
            logging.warning(logstring)
        else:
            logging.error(logstring)

    def __del__(self):
        self.session.close()
