import sqlite3

from datetime import datetime
import socket
import logging
from inspect import currentframe, getframeinfo

# converts data rows into python dict


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DataBase:

    def __init__(self):
        self.connection = sqlite3.connect("Inventory.db")
        self.connection.row_factory = dict_factory  # this must come before the cursor
        self.cursor = self.connection.cursor()
        return

    def createUser(self, first_name, last_name, email, encrypted_password):
        # INPUTS: all table fields
        # OUTPUTS: none

        # Data Binding (Security Feature to ovoid SQL INGECTION)

        data = [first_name, last_name, email, encrypted_password]

        # OVOID SQL INGECTION: DO NOT CONCATINATE DATABASE QUERYS
        self.cursor.execute(
            "INSERT INTO Users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", data)
        # Commit after every write operation
        self.connection.commit()

        item_id = self.cursor.lastrowid

        if item_id == None:
            return False
        return True

    def findUserByEmail(self, email):
        # INPUTS: which item?
        # OUTPUTS: A single Item/row
        data = [email]
        self.cursor.execute("SELECT * FROM Users WHERE email = ?", data)
        return self.cursor.fetchone()

    def createItem(self, lot_num, item_name, vendor, exp_date):
        # INPUTS: all table fields
        # OUTPUTS: none

        # Data Binding (Security Feature to ovoid SQL INGECTION)

        data = [lot_num, item_name, vendor, 0, exp_date]

        # OVOID SQL INGECTION: DO NOT CONCATINATE DATABASE QUERYS
        self.cursor.execute(
            "INSERT INTO Inventory (lot_num, item_name, vendor, Inv, exp_date) VALUES (?, ?, ?, ?, ?)", data)
        # Commit after every write operation
        self.connection.commit()

        item_id = self.cursor.lastrowid

        if item_id == None:
            return False

        return True

    def getAllItems(self):
        self.cursor.execute("SELECT * FROM Inventory")
        return self.cursor.fetchall()

    def getOneItem(self, item_id):
        # INPUTS: which item?
        # OUTPUTS: A single Item/row
        data = [item_id]
        self.cursor.execute("SELECT * FROM Inventory WHERE item_id = ?", data)
        return self.cursor.fetchone()

    def updateItem(self, item_id, lot_num, item_name, vendor, exp_date):
        # INPUTS: id and update fields
        # OUTPUTS: none
        data = [lot_num, item_name, vendor, exp_date, item_id]
        self.cursor.execute(
            "UPDATE Inventory SET lot_num = ?, item_name = ?, vendor = ?, exp_date = ? WHERE item_id = ?", data)
        self.connection.commit()

        passedTest = True
        item = self.getOneItem(item_id)

        if item['lot_num'] != lot_num:
            passedTest = False
            self.handleReports('ERROR - lot_num was not updated to: ' +
                               lot_num, getframeinfo(currentframe()), "error")
        if item['item_name'] != item_name:
            passedTest = False
            self.handleReports('ERROR - item_name was not updated to: ' +
                               item_name, getframeinfo(currentframe()), "error", False)
        if item['vendor'] != vendor:
            passedTest = False
            self.handleReports('ERROR - vendor was not updated to: ' +
                               vendor, getframeinfo(currentframe()), "error")
        if item['exp_date'] != exp_date:
            passedTest = False
            self.handleReports('ERROR - exp_date was not updated to: ' +
                               exp_date, getframeinfo(currentframe()), "error")

        return passedTest

    def patchInv(self, item_id, ammount):
        # INPUTS: id and update fields
        # OUTPUTS: none
        item = self.getOneItem(item_id)
        newInv = item['Inv'] + ammount
        data = [newInv, item_id]
        self.cursor.execute(
            "UPDATE Inventory SET Inv = ? WHERE item_id = ?", data)
        self.connection.commit()

        item = self.getOneItem(item_id)
        if item['Inv'] != newInv:
            self.handleReports('ERROR - Inv for' + item_id + 'was not updated to: ' +
                               newInv, getframeinfo(currentframe()), "error")
            return False

        return True

    def deleteItem(self, item_id):
        # INPUTS: which Item?
        # OUTPUTS: none
        data = [item_id]
        self.cursor.execute("DELETE FROM Inventory WHERE item_id = ?", data)
        self.connection.commit()

        item = self.getOneItem(item_id)
        if item != None:
            self.handleReports(
                "ERROR - " + item + " was not deleted.", getframeinfo(currentframe()), "error")
            return False

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
