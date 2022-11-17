from http.server import BaseHTTPRequestHandler, HTTPServer
# improves python to help communication to client
from socketserver import ThreadingMixIn
import json
from urllib.parse import parse_qs

from datetime import datetime
import socket
import logging
from inspect import currentframe, getframeinfo


from database import DataBase

'''
https://restapitutorial.com/lessons/httpmethods.html
'''


class MyRequestHandler(BaseHTTPRequestHandler):

    def createItem(self):
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

        data = []

        List = [lot_num, item_name, vendor, Inv, exp_date]

        # the keys is specified by the client

        db = DataBase()
        itemInserted = db.createItem(lot_num, item_name, vendor, exp_date)

        if itemInserted:
            # Respond with success (201)
            self.send_response(201, "New Item Inserted")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return True
        else:
            # Respond with failure
            self.send_response(500, "Database Failure")
            self.send_header("Access-Control-Allow-Orgin", "*")
            self.end_headers()
            return False

    def listItems(self):
        # send status code: OK
        self.send_response(200, "Item List Sent")

        # create headers
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")

        # end headers and start body/data
        self.end_headers()
        db = DataBase()
        TABLE = db.getAllItems()

        # write to the "wfile" response body
        self.wfile.write(bytes(json.dumps(TABLE), "utf-8"))

    def retrieveItem(self, item_id):

        db = DataBase()

        oneItem = db.getOneItem(item_id)

        if (oneItem):
            self.send_response(200, "Item Sent")
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(oneItem), "utf=8"))
        else:
            self.handleNotFound("Item not Found")

    def updateItem(self, item_id):
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
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.send_header("Access-Control-Allow-Orgin", "*")
                self.end_headers()
                return False
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

    def updateItemInv(self, item_id):
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
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                return True
            else:
                # Respond with failure
                self.send_response(500, "Database Failure")
                self.send_header("Access-Control-Allow-Orgin", "*")
                self.end_headers()
                return False
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

    def deleteItem(self, item_id):
        db = DataBase()
        itemExists = db.getOneItem(item_id)
        if itemExists != None:
            db.deleteItem(item_id)
            self.send_response(200, "Item Deleted")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            message = 'ERROR - Item id: ' + item_id + '  - does not exist.'
            self.handleReports(message, getframeinfo(currentframe()), "error")
            self.handleNotFound(message)
            return False

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
        self.send_header("Access-Control-Allow-Orgin", "*")
        self.end_headers()

    def handleNotFound(self, message):
        # send status code: NOT FOUND
        self.send_response(404, message)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_POST(self):
        if self.path == "/items":
            self.createItem()
        else:
            self.handleNotFound("Unknown Request")

    def do_GET(self):
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
        else:
            self.handleNotFound("Unknown Request")

    def do_PUT(self):
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
        else:
            self.handleNotFound("Unknown Request")

    def do_OPTIONS(self):
        # Approves all communication, for more security ask more if then
        # statements on the self.path and check the orgin
        self.send_response(200, "Option Verified")
        self.send_header("Access-Control-Allow-Origin", "*")
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
