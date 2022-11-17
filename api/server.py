from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
# improves python to help communication to client
from socketserver import ThreadingMixIn
import json
from urllib.parse import parse_qs
from passlib.hash import bcrypt

from datetime import datetime
import socket
import logging
from inspect import currentframe, getframeinfo


from database import DataBase
from sessionstore import SessionStore

SESSION_STORE = SessionStore()

'''
https://restapitutorial.com/lessons/httpmethods.html
'''


class MyRequestHandler(BaseHTTPRequestHandler):

    # override end_headers to include cookies with normal function
    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        super().end_headers()

    # =================================================
    '''
    cookie & session funcitons
    '''

    # C -> cookie -> S
    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            # create empty cookie object if no cookie yet exsists
            self.cookie = cookies.SimpleCookie()
        return None

    # S -> setcookie -> C
    def send_cookie(self):
        for morsel in self.cookie.values():
            morsel["samesite"] = "None"  # prevent postman to work
            morsel["secure"] = True  # prevent postman to work
            self.send_header("Set-Cookie", morsel.OutputString())
        return None

    # Notes
    # pip3 install bcrypt passlib
    # if (response.status)==201) {};
    # POST /users
    # POST /sessions
    # DELETE /sessions

    def handleCreateAuthenticatedSession(self):  # sign in to account

        length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(request_body)
        # GIVEN: an attempted email and password from the CLIENT
        try:
            email = parsed_body["email"][0]
        except KeyError:
            message = 'INFO - Missing email Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.handleBadEntry(message)
            return False
        try:
            password = parsed_body["password"][0]
        except KeyError:
            message = 'INFO - Missing password Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.handleBadEntry(message)
            return False
        #print(email,password)
        # step 1: check users database if account/email exists
        db = DataBase()
        user = db.findUserByEmail(email)
        # IF valid user record was found:
        if user != None:
            # step 2: compare the given password to the encrypted password in the DataBase
            # HINT: use bcrypt.verify()
            # IF password matches:
            if bcrypt.verify(password, user["password"]):
                # SUCCESS! respond with 201 status code
                self.send_response(201)
                self.sessionData["user_id"] = user["user_id"]
                self.end_headers()
                # remember the users authenticated state
            else:
                # FAILURE! respond with 401 status code
                self.send_response(401, "User Doesn't Exist")  # Wrond Password
                self.end_headers()
        else:
            # report that the user doesn't exist
            self.send_response(401, "User Doesn't Exist")
            self.end_headers()

    def handleLogOutSession(self):  # sign in to account
        length = self.headers["Content-Length"]

        try:
            # Logout the user
            del self.sessionData["user_id"]
            self.send_response(200, "User Logged Out")
            self.end_headers()

        except:
            # report that the user doesn't exist
            self.send_response(401, "User Doesn't Exist")
            self.end_headers()

    def loadSessionData(self):
        self.load_cookie()
        # check for an existing session ID cookie
        if "sessionId" in self.cookie:
            # get the session id and load it from the session store
            sessionId = self.cookie["sessionId"].value
            # load_session_data
            self.sessionData = SESSION_STORE.loadSessionData(sessionId)
            # check if the session data was loaded
            if self.sessionData == None:
                # create a new session Id/data
                sessionId = SESSION_STORE.createEmptySession()
                # sessionData is a dictionary of dictionaries, one per session
                self.sessionData = SESSION_STORE.loadSessionData(sessionId)
                # set a new session Id cookie
                self.cookie["sessionId"] = sessionId
        else:
            # create a new session Id/data
            sessionId = SESSION_STORE.createEmptySession()
            # sessionData is a dictionary of dictionaries, one per session
            self.sessionData = SESSION_STORE.loadSessionData(sessionId)
            # set a new session Id cookie
            self.cookie["sessionId"] = sessionId
        #print("MY SESSION DATA:", self.sessionData)

    # =================================================

    def createUser(self):
        length = self.headers["Content-Length"]
        request_body = self.rfile
        # Capture input (the entry) from the CLIENT REQUEST

        # 1) read the content length from the request header
        Content_Length = self.headers["Content-Length"]

        # 2) Read from the "rfile" request body
        request_body = self.rfile.read(int(Content_Length)).decode("utf-8")

        # 3) parse the URL-encoded request body
        parsed_body = parse_qs(request_body)

        # 4) Append the new entry to the Dictionary above (TABLE)
        try:
            first_name = parsed_body["first_name"][0]
        except KeyError:
            message = 'ERROR - Missing first name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            last_name = parsed_body["last_name"][0]
        except KeyError:
            message = 'ERROR - Missing last name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            email = parsed_body["email"][0]
        except KeyError:
            message = 'ERROR - Missing email Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            password = parsed_body["password"][0]
        except KeyError:
            message = 'ERROR - Missing password Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        # Encrypt password
        # 422 unprossessable request (User already exsists)
        # use db.findUserByEmail(email)
        encrypted_password = bcrypt.hash(password)

        # the keys is specified by the client

        db = DataBase()
        if not (db.findUserByEmail(email)):
            userCreated = db.createUser(
                first_name, last_name, email, encrypted_password)
            if userCreated:
                # Respond with success (201)
                self.send_response(201, "New User Created")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User Already Exists.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User Already Exists")  # conflict code
            self.end_headers()
            return False

    def createItem(self):
        if 'userId' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        # Capture input (the entry) from the CLIENT REQUEST

        # 1) read the content length from the request header
        Content_Length = self.headers["Content-Length"]

        # 2) Read from the "rfile" request body
        request_body = self.rfile.read(int(Content_Length)).decode("utf-8")

        # 3) parse the URL-encoded request body
        parsed_body = parse_qs(request_body)

        # 4) Append the new entry to the Dictionary above (TABLE)
        try:
            lot_num = parsed_body["lot_num"][0]
        except KeyError:
            message = 'ERROR - Missing Lot Number Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            item_name = parsed_body["item_name"][0]
        except KeyError:
            message = 'ERROR - Missing Item Name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            vendor = parsed_body["vendor"][0]
        except KeyError:
            message = 'ERROR - Missing Vendor Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        Inv = 0

        try:
            exp_date = parsed_body["exp_date"][0]
        except KeyError:
            message = 'ERROR - Missing Exp Date Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        # 422 unprossessable request
        # 400 bad request

        # the keys is specified by the client

        db = DataBase()
        itemInserted = db.createItem(lot_num, item_name, vendor, exp_date)

        if itemInserted:
            # Respond with success (201)
            self.send_response(201, "New Item Inserted")
            self.end_headers()
            return True
        else:
            # Respond with failure
            self.send_response(500, "Database Failure")
            self.end_headers()
            return False

    def listItems(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "User Not Logged In")
            self.end_headers()
            return False
        # send status code: OK
        self.send_response(200, "Item List Sent")

        # create headers
        self.send_header("Content-Type", "application/json")

        # end headers and start body/data
        self.end_headers()
        db = DataBase()
        TABLE = db.getAllItems()

        # write to the "wfile" response body
        self.wfile.write(bytes(json.dumps(TABLE), "utf-8"))

    def retrieveItem(self, item_id):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "User Not Logged In")
            return False
        db = DataBase()

        oneItem = db.getOneItem(item_id)

        if (oneItem):
            self.send_response(200, "Item Sent")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(oneItem), "utf=8"))
        else:
            self.handleNotFound("Item not Found")

    def updateItem(self, item_id):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "User Not Logged In")
            self.end_headers()
            return False
        # Capture input (the entry) from the CLIENT REQUEST

        # 1) read the content length from the request header
        Content_Length = self.headers["Content-Length"]

        # 2) Read from the "rfile" request body
        request_body = self.rfile.read(int(Content_Length)).decode("utf-8")

        # 3) parse the URL-encoded request body
        parsed_body = parse_qs(request_body)

        # 4) Append the new entry to the Dictionary above (TABLE)
        try:
            lot_num = parsed_body["lot_num"][0]
        except KeyError:
            message = 'ERROR - Missing Lot Number Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            item_name = parsed_body["item_name"][0]
        except KeyError:
            message = 'ERROR - Missing Item Name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            vendor = parsed_body["vendor"][0]
        except KeyError:
            message = 'ERROR - Missing rm Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            exp_date = parsed_body["exp_date"][0]
        except KeyError:
            message = 'ERROR - Missing Exp Date Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        # 422 unprossessable request
        # 400 bad request

        # the keys is specified by the client
        db = DataBase()
        itemExists = db.getOneItem(item_id)
        if itemExists != None:
            itemInserted = db.updateItem(
                item_id, lot_num, item_name, vendor, exp_date)

            if itemInserted:
                # Respond with success (201)
                self.send_response(200, "Item Updated")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

    def updateItemInv(self, item_id):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "User Not Logged In")
            self.end_headers()
            return False

        Content_Length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(Content_Length)).decode("utf-8")
        parsed_body = parse_qs(request_body)

        try:
            rm = int(parsed_body["rm"][0])
        except KeyError:
            message = 'ERROR - Missing rm Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            add = int(parsed_body["add"][0])
        except KeyError:
            message = 'ERROR - Missing add Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()

        itemExists = db.getOneItem(item_id)
        if itemExists != None:

            itemInvUpdated = db.patchInv(item_id, add - rm)

            if itemInvUpdated:
                self.send_response(200, "Inventory Updated")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

    def deleteItem(self, item_id):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "User Not Logged In")
            self.end_headers()
            return False

        db = DataBase()
        itemExists = db.getOneItem(item_id)
        if itemExists != None:
            db.deleteItem(item_id)
            self.send_response(200, "Item Deleted")
            self.end_headers()
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

    '''
    handler functions
    '''

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

    def handleBadEntry(self, message):
        self.send_response(422, message)
        self.end_headers()

    def handleNotFound(self, message):
        # send status code: NOT FOUND
        self.send_response(404, message)
        self.end_headers()

    def do_POST(self):
        self.loadSessionData()
        if self.path == "/items":
            self.createItem()
        elif self.path == "/users":
            self.createUser()
        elif self.path == "/sessions":
            self.handleCreateAuthenticatedSession()
        else:
            self.handleNotFound("Unknown Request")

    def do_GET(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        # INPUT '/items/3' OUTPUT '['','items','3']'
        if len(pathList) > 2:
            collection_name = pathList[1]
            item_id = pathList[2]
        else:
            collection_name = pathList[1]
            item_id = None

        if pathList[1] == "items":
            if item_id != None:
                # retrieve a single item by member_id
                self.retrieveItem(item_id)
            elif item_id == None:
                # retrieve all items
                self.listItems()
            else:
                self.handleNotFound("Item Not Found")

        elif pathList[1] == "sessions":
            self.handleCreateAuthenticatedSession()

        else:
            self.handleNotFound("Unknown Request")

        # This elif is a test example to ensure that cookies are working
        '''
        elif collection_name == "cookiemonster":
            self.load_cookie()
            print("flavor: ", self.cookie)
            self.cookie["flavor"] = "Chocolate Chip"

            self.send_response(200)
            self.send_cookie()
            self.end_headers()
            self.wrile.write(bytes("cookie for you!","uft-8"))
        '''
        # this elif statement above is not perminent

    def do_PUT(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        # INPUT '/get_inventory/3' OUTPUT '['','get_inventory','3']'
        if len(pathList) > 2:
            collection_name = pathList[1]
            item_id = pathList[2]
        else:
            collection_name = pathList[1]
            item_id = None

        if pathList[1] == "items":
            if item_id != None:
                self.updateItem(item_id)
            else:
                self.handleNotFound("Item Not Found")
        else:
            self.handleNotFound("Unknown Request")

    def do_PATCH(self):
        self.loadSessionData()
        pathList = self.path.split("/")

        if len(pathList) > 2:
            collection_name = pathList[1]
            item_id = pathList[2]
        else:
            collection_name = pathList[1]
            item_id = None

        if collection_name == "items":
            if item_id != None:
                self.updateItemInv(item_id)
            else:
                self.handleNotFound("Item Not Found")
        else:
            self.handleNotFound("Unknown Request")

    def do_DELETE(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        # INPUT '/get_inventory/3' OUTPUT '['','get_inventory','3']'
        if len(pathList) > 2:
            collection_name = pathList[1]
            item_id = pathList[2]
        else:
            collection_name = pathList[1]
            item_id = None

        if pathList[1] == "items":
            if item_id != None:
                # delete a single item by member_id
                self.deleteItem(item_id)
            else:
                self.handleNotFound("Item Not Found")
        elif pathList[1] == "sessions":
            self.handleLogOutSession()
        else:
            self.handleNotFound("Unknown Request")

    def do_OPTIONS(self):
        self.loadSessionData()
        # Approves all communication, for more security ask more if then
        # statements on the self.path and check the orgin
        self.send_response(200, "Option Verified")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# Threaded server helps communication to client
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass  # no implementation


def run():
    # Address for server
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)

    # Run the server loop
    startipAddress = str(socket.gethostbyname(socket.gethostname()))
    startdatetime = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    print(startipAddress + " - - [" +
          startdatetime + ']  "Server Status: ACTIVE')
    server.serve_forever()


if __name__ == "__main__":
    run()
