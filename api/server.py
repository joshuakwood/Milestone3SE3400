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
            # Turn off the next to lines for 
            # enabling testing with postman
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
            if bcrypt.verify(password, user["encrypted_password"]):
                # SUCCESS! respond with 201 status code
                self.send_response(201, "User Logged In")
                self.sessionData["user_id"] = user["user_id"]
                self.sessionData["user_email"] = email
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

    def updateUserAccount(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]
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
            new_first_name = parsed_body["first_name"][0]
        except KeyError:
            message = 'ERROR - Missing first name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            new_last_name = parsed_body["last_name"][0]
        except KeyError:
            message = 'ERROR - Missing last name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()
        if (db.findUserByEmail(email)):
            userUpdated = db.updateUser(
                db.findUserByEmail(email)["user_id"], new_first_name, new_last_name)
            if userUpdated:
                # Respond with success (201)
                self.send_response(201, "New User Updated")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User does not exist")  # conflict code
            self.end_headers()
            return False

    def changeUserPassword(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]
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
            password = parsed_body["new_password"][0]
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
        if (db.findUserByEmail(email)):
            passwordUpdated = db.updateUserPassword(db.findUserByEmail(email)["user_id"], encrypted_password)
            if passwordUpdated:
                # Respond with success (201)
                self.send_response(201, "Password Updated")
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

    def updateWebisteSettings(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

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
            website = parsed_body["website"][0]
        except KeyError:
            message = 'ERROR - Missing website name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        try:
            new_filter_settings = dict(json.loads(parsed_body["new_filter_settings"][0]))
        except KeyError:
            message = 'ERROR - Missing new filter settings Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()
        if (db.findUserByEmail(email)):
            websiteUpdated = db.updateWebsiteSettings(website, email, new_filter_settings)
            if websiteUpdated:
                # Respond with success (201)
                self.send_response(201, "Website Filter Updated")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Filter Does not Exist.")
                self.end_headers()
                return False
        else:
            message = 'INFO - User Does not exist yet.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User Does not exist yet")  # conflict code
            self.end_headers()
            return False

    def updateFilterSettings(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

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
            new_filter_settings = parsed_body["filters"][0]
        except KeyError:
            message = 'ERROR - Missing filters name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()
        if (db.findUserByEmail(email)):
            filterUpdated = db.updateFilterSettings(
                email, new_filter_settings)
            if filterUpdated:
                # Respond with success (201)
                self.send_response(201, "Filters Updated")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Invalid Filter Settings")
                self.end_headers()
                return False
        else:
            message = 'INFO - User Does not exist yet.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User Does not exist yet")  # conflict code
            self.end_headers()
            return False

    def addFilter(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

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
            website = parsed_body["website"][0]
        except KeyError:
            message = 'ERROR - Missing website name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()
        if (db.findUserByEmail(email)):
            filterCreated = db.addFilter(website, email)
            if filterCreated:
                # Respond with success (201)
                self.send_response(201, "Website Filter Created")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User Does not exist yet.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User Does not exist yet")  # conflict code
            self.end_headers()
            return False

    def sendUserData(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

        db = DataBase()
        if (db.findUserByEmail(email)):
            userData = db.getUserData(email)
            if userData:
                # Respond with success (201)
                self.send_response(201, "Data Sent")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(userData), "utf=8"))
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User Does not exist yet.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User Does not exist yet")  # conflict code
            self.end_headers()
            return False

    def sendData(self):
        # retrive data from json
        f = open('data.json')
        data = json.load(f)
        self.send_response(200, "Data Sent")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), "utf=8"))

    def deleteUser(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

        db = DataBase()
        if (db.findUserByEmail(email)):
            userDeleted = db.deleteUser(db.findUserByEmail(email)["user_id"])
            if userDeleted:
                # Respond with success (201)
                self.send_response(201, "User Deleted")
                self.end_headers()
                self.handleLogOutSession()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User does not exist")  # conflict code
            self.end_headers()
            return False

    def deleteFilter(self):
        if 'user_id' not in self.sessionData:
            self.send_response(401, "Not Logged In")
            self.end_headers()
            return
        email = self.sessionData["user_email"]

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
            website = parsed_body["website"][0]
        except KeyError:
            message = 'ERROR - Missing website name Entry.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleBadEntry(message)
            return False

        db = DataBase()
        if (db.findUserByEmail(email)):
            filterDeleted = db.deleteFilter(website, db.findUserByEmail(email)["user_id"])
            if filterDeleted:
                # Respond with success (201)
                self.send_response(201, "Filter Deleted")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.end_headers()
                return False
        else:
            message = 'INFO - User does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "info")
            self.send_response(422, "User does not exist")  # conflict code
            self.end_headers()
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
        if self.path == "/filters":
            self.addFilter()
        elif self.path == "/users":
            self.createUser()
        elif self.path == "/sessions":
            self.handleCreateAuthenticatedSession()
        else:
            self.handleNotFound("Unknown Request")

    def do_GET(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        if pathList[1] == "data":
            self.sendData()

        elif pathList[1] == "sessions":
            self.sendUserData()

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
        else:
            self.handleNotFound("Unknown Request")
            return False

    def do_PUT(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        if pathList[1] == "users":
            if pathList[2] == "account-settings":
                self.updateUserAccount()
                return None
            elif pathList[2] == "change-password":
                self.changeUserPassword()
                return None
            elif pathList[2] == "filter-settings":
                self.updateFilterSettings()
                return None
            elif pathList[2] == "website-settings":
                self.updateWebisteSettings()
                return None
            else:
                self.handleNotFound("Unknown Request")
        else:
            self.handleNotFound("Unknown Request")
        
    #def do_PATCH(self):
        self.handleNotFound("Unknown Request")

    def do_DELETE(self):
        self.loadSessionData()
        pathList = self.path.split("/")
        if pathList[1] == "users":
            if pathList[2] == "account":
                self.deleteUser()
                return None
            elif pathList[2] == "filters":
                self.deleteFilter()
                return None
            else:
                self.handleNotFound("Unknown Request")
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

# Threaded server helps communication to client (THIS IS IMPORTANT)
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
